"""Train the latent world model on 2018-2021 satellite days, validate on 2022, and save it.

    python experiments/train_worldmodel.py --name wm_jepa                 # JEPA + decoder
    python experiments/train_worldmodel.py --name wm_direct --w-latent 0  # same network, no JEPA loss

Outputs: results/<name>/model.pt, log.jsonl, config.json
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from oceanmeta.worldmodel import WorldModel, HIST  # noqa: E402

CHL_MU, CHL_SD = -0.16, 0.5      # log10 chlorophyll normalisation
SST_MU, SST_SD = 20.0, 5.0


class Cube:
    """Daily chlorophyll and SST on the chlorophyll grid, normalised, with an ocean mask."""

    def __init__(self):
        P = ROOT / "data" / "processed"
        self.chl = np.load(P / "chl.npy", mmap_mode="r")
        self.dates = np.load(P / "chl_dates.npy").astype("datetime64[D]")
        self.sst = np.load(P / "sst_on_chl.npy", mmap_mode="r")
        self.ocean = np.load(P / "ocean_mask.npy")
        self.idx = {d: i for i, d in enumerate(self.dates)}
        self.years = self.dates.astype("datetime64[Y]").astype(int) + 1970

    def frame(self, i, y0, x0, n):
        c = np.asarray(self.chl[i, y0:y0 + n, x0:x0 + n], dtype=np.float32)
        s = np.asarray(self.sst[i, y0:y0 + n, x0:x0 + n], dtype=np.float32)
        oc = self.ocean[y0:y0 + n, x0:x0 + n] & np.isfinite(c)
        c = np.where(oc, (c - CHL_MU) / CHL_SD, 0.0)
        s = np.where(np.isfinite(s) & oc, (s - SST_MU) / SST_SD, 0.0)
        return np.stack([c, s, oc.astype(np.float32)])

    def example(self, rng, years, n=64, max_lead=3):
        key = tuple(sorted(years))
        if not hasattr(self, "_valid"):
            self._valid = {}
        if key not in self._valid:
            ok = np.isin(self.years, list(years))
            ok[:HIST - 1] = False
            ok[len(ok) - max_lead:] = False
            self._valid[key] = np.where(ok)[0]
        valid = self._valid[key]
        for _ in range(200):
            i = int(valid[rng.integers(len(valid))])
            lead = int(rng.integers(1, max_lead + 1))
            d = self.dates[i]
            need = [d - np.timedelta64(h, "D") for h in range(HIST - 1, -1, -1)] + [d + np.timedelta64(lead, "D")]
            if any(x not in self.idx for x in need):
                continue
            y0 = int(rng.integers(0, self.chl.shape[1] - n))
            x0 = int(rng.integers(0, self.chl.shape[2] - n))
            if self.ocean[y0:y0 + n, x0:x0 + n].mean() < 0.5:
                continue
            fr = np.stack([self.frame(self.idx[x], y0, x0, n) for x in need[:-1]])
            tg = self.frame(self.idx[need[-1]], y0, x0, n)
            return fr, tg, lead
        raise RuntimeError("no example found")

    def batch(self, rng, years, B, device):
        ex = [self.example(rng, years) for _ in range(B)]
        fr = torch.from_numpy(np.stack([e[0] for e in ex])).to(device)
        tg = torch.from_numpy(np.stack([e[1] for e in ex])).to(device)
        ld = torch.tensor([e[2] for e in ex], device=device)
        return fr, tg, ld


def evaluate(model, cube, years, device, n_batches=40, seed=123):
    """Forecast scores on held-out days: RMSE and negative log-likelihood of the model, RMSE of
    persistence (the latest map), all in log10 chlorophyll on ocean pixels."""
    rng = np.random.default_rng(seed)
    model.eval()
    se_m = se_p = nll = n = 0.0
    with torch.no_grad():
        for _ in range(n_batches):
            fr, tg, ld = cube.batch(rng, years, 32, device)
            _, mean, log_sd = model(fr, ld)
            oc = tg[:, 2] > 0.5
            y = tg[:, 0]
            se_m += (((mean - y) * CHL_SD)[oc] ** 2).sum().item()
            se_p += (((fr[:, -1, 0] - y) * CHL_SD)[oc] ** 2).sum().item()
            sd = log_sd.exp()
            nll += (log_sd + 0.5 * ((y - mean) / sd) ** 2)[oc].sum().item()
            n += oc.sum().item()
    model.train()
    return dict(rmse_model=(se_m / n) ** 0.5, rmse_persistence=(se_p / n) ** 0.5, nll=nll / n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--steps", type=int, default=12000)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--w-latent", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    torch.manual_seed(a.seed)
    rng = np.random.default_rng(a.seed)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    cube = Cube()
    out = ROOT / "results" / a.name
    out.mkdir(parents=True, exist_ok=True)
    json.dump(vars(a), open(out / "config.json", "w"), indent=1)
    model = WorldModel().to(dev)
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=a.lr, weight_decay=0.05)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, a.lr, total_steps=a.steps, pct_start=0.05)
    train_years, val_years = {2018, 2019, 2020, 2021}, {2022}
    log = open(out / "log.jsonl", "a")
    tic = time.time()
    for step in range(1, a.steps + 1):
        fr, tg, ld = cube.batch(rng, train_years, a.batch, dev)
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=dev == "cuda"):
            loss, parts = model.loss(fr, tg, ld, w_latent=a.w_latent)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        model.ema = 0.996 + (1 - 0.996) * step / a.steps
        model.update_target()
        if step % 500 == 0 or step == a.steps:
            ev = evaluate(model, cube, val_years, dev)
            rec = dict(step=step, loss=loss.item(), **parts, **{f"val_{k}": v for k, v in ev.items()},
                       sec=round(time.time() - tic))
            log.write(json.dumps(rec) + "\n")
            log.flush()
            print(rec, flush=True)
    torch.save(model.state_dict(), out / "model.pt")


if __name__ == "__main__":
    main()
