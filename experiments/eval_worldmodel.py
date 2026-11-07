"""Forecast skill of world models on held-out years, per lead time: error of the forecast mean
and of persistence (the latest map), negative log-likelihood, and calibration (ratio of the
mean forecast spread to the actual error; 1 = well calibrated).

    python experiments/eval_worldmodel.py wm_jepa_v0 wm_direct_v0 --years 2023 2024 2025 2026
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))
from oceanmeta.worldmodel import WorldModel  # noqa: E402
from train_worldmodel import Cube, CHL_SD  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("models", nargs="+")
    ap.add_argument("--years", type=int, nargs="+", default=[2023, 2024, 2025, 2026])
    ap.add_argument("--batches", type=int, default=60)
    a = ap.parse_args()
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    cube = Cube()
    out = {}
    for name in a.models:
        model = WorldModel().to(dev)
        model.load_state_dict(torch.load(ROOT / "results" / name / "model.pt", map_location=dev))
        model.eval()
        rng = np.random.default_rng(2026)
        acc = {k: dict(se_m=0.0, se_p=0.0, nll=0.0, var=0.0, n=0) for k in (1, 2, 3)}
        with torch.no_grad():
            for _ in range(a.batches):
                fr, tg, ld = cube.batch(rng, set(a.years), 32, dev)
                _, mean, log_sd = model(fr, ld)
                oc = tg[:, 2] > 0.5
                y = tg[:, 0]
                for k in (1, 2, 3):
                    sel = (ld == k)[:, None, None] & oc
                    if sel.sum() == 0:
                        continue
                    e_m = ((mean - y) * CHL_SD)[sel]
                    e_p = ((fr[:, -1, 0] - y) * CHL_SD)[sel]
                    sd = (log_sd.exp() * CHL_SD)[sel]
                    acc[k]["se_m"] += (e_m ** 2).sum().item()
                    acc[k]["se_p"] += (e_p ** 2).sum().item()
                    acc[k]["var"] += (sd ** 2).sum().item()
                    acc[k]["nll"] += (torch.log(sd) + 0.5 * (e_m / sd) ** 2).sum().item()
                    acc[k]["n"] += sel.sum().item()
        res = {}
        for k, v in acc.items():
            n = max(v["n"], 1)
            rm, rp = (v["se_m"] / n) ** 0.5, (v["se_p"] / n) ** 0.5
            res[k] = dict(rmse_model=rm, rmse_persistence=rp, skill=1 - rm / rp,
                          spread_over_error=(v["var"] / n) ** 0.5 / rm, nll=v["nll"] / n)
            print(f"{name} lead {k} d: rmse {rm:.4f} vs persistence {rp:.4f} (skill {1 - rm / rp:+.3f}), "
                  f"spread/error {res[k]['spread_over_error']:.2f}")
        out[name] = res
    dst = ROOT / "results" / "worldmodel_eval.json"
    old = json.load(open(dst)) if dst.exists() else {}
    old.update({f"{k}|{'-'.join(map(str, a.years))}": v for k, v in out.items()})
    json.dump(old, open(dst, "w"), indent=1)


if __name__ == "__main__":
    main()
