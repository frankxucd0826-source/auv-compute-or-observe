"""Run controllers on mission windows in parallel and append one JSON line per mission.

    python experiments/run.py --exp pilot_fixed --split dev --n 60 --lags 1 3 \
        --controllers fixed-0 fixed-1 fixed-2 fixed-3 --workers 8

Results: results/<exp>/results.jsonl and results/<exp>/config.json.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

_M = None


def _init():
    for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[k] = "1"
    global _M
    import numpy as np
    _M = dict(np.load(ROOT / "data" / "missions" / "chl_missions.npz"))
    prior = os.environ.get("OCEANMETA_PRIOR", "")
    if prior:
        W = np.load(ROOT / "data" / "missions" / f"chl_missions_{prior}.npz")
        _M["wm_mean"], _M["wm_sd"] = W["mean"], W["sd"]


def make_controller(spec):
    from oceanmeta import meta
    kind, _, arg = spec.partition("-")
    if kind == "fixed":
        return meta.Fixed(int(arg))
    if kind == "periodic":
        return meta.Periodic([int(c) for c in arg])
    if hasattr(meta, "make") and meta.make(spec) is not None:
        return meta.make(spec)
    raise ValueError(spec)


def _job(job):
    import numpy as np
    from oceanmeta.mission import Sensor, MissionConfig, run_mission
    from oceanmeta.platforms import PRESETS
    i, lag, spec, cfgd = job
    from oceanmeta.belief import gaussian_random_fields
    li = list(_M["lags"]).index(lag)
    truth, prior, mask = _M["truth"][i], _M["prior"][i, li], _M["mask"][i]
    # The real ocean differs from even a same-day satellite map (retrieval error, unresolved
    # patches): add a spatially correlated error field, the same for every controller and lag.
    if cfgd["sat_err"] > 0:
        g = gaussian_random_fields(1, *truth.shape, cfgd["sat_len"], np.random.default_rng(7919 * i + 1))[0]
        truth = truth + cfgd["sat_err"] * g
    plat = PRESETS[cfgd["platform"]](**cfgd.get("platform_kw", {}))
    sensor = Sensor(noise_sd=cfgd["noise"])
    mkw = dict(cfgd.get("mission_kw", {}))
    mkw.setdefault("prior_length_cells", cfgd["prior_len"][str(lag)])
    mcfg = MissionConfig(**mkw)
    sd = np.hypot(cfgd["prior_sd"][str(lag)], cfgd["sat_err"]) * cfgd.get("sd_scale", 1.0)
    if "wm_mean" in _M:      # the world model's forecast replaces the stale map
        prior = _M["wm_mean"][i, li]
        sd = np.hypot(_M["wm_sd"][i, li], cfgd["sat_err"]) * cfgd.get("sd_scale", 1.0)
    start = (cfgd["starts"][i][0], cfgd["starts"][i][1])
    tic = time.time()
    ctl = make_controller(spec)
    out, m = run_mission(truth, prior, sd, mask, start, plat, sensor, mcfg, ctl,
                         seed=cfgd["seed"] * 100003 + i * 31 + lag)
    if getattr(ctl, "scores", None):          # rehearsal: what imagination predicted per strategy
        out["choice"] = ctl.choice
        out["imagined"] = ctl.scores
    out.update(mission=int(i), lag=int(lag), controller=spec, wall_s=round(time.time() - tic, 2))
    out.pop("cell", None)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", required=True)
    ap.add_argument("--split", default="dev")
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--lags", type=int, nargs="+", default=[1, 2, 3])
    ap.add_argument("--controllers", nargs="+", required=True)
    ap.add_argument("--platform", default="auv")
    ap.add_argument("--platform-kw", default="{}")
    ap.add_argument("--mission-kw", default="{}")
    ap.add_argument("--noise", type=float, default=0.1)
    ap.add_argument("--sat-err", type=float, default=0.15, help="log10 sd of real ocean minus satellite map")
    ap.add_argument("--sat-len", type=float, default=3.0, help="its correlation length in cells")
    ap.add_argument("--sd-scale", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--prior", default="", help="world model name; empty = stale satellite map")
    a = ap.parse_args()
    os.environ["OCEANMETA_PRIOR"] = a.prior

    import csv
    import numpy as np
    from multiprocessing import Pool
    rows = list(csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
    stats = json.load(open(ROOT / "data" / "missions" / "prior_stats.json", encoding="utf-8"))
    ids = [int(r["id"]) for r in rows if r["split"] == a.split]
    rng = np.random.default_rng(a.seed)
    ids = sorted(rng.choice(ids, min(a.n, len(ids)), replace=False).tolist())
    cfgd = dict(platform=a.platform, platform_kw=json.loads(a.platform_kw),
                mission_kw=json.loads(a.mission_kw), noise=a.noise, sd_scale=a.sd_scale,
                sat_err=a.sat_err, sat_len=a.sat_len,
                prior_sd=stats["sd"], prior_len=stats["length_cells"], seed=a.seed,
                starts={int(r["id"]): (float(r["start_x"]), float(r["start_y"])) for r in rows})
    out = ROOT / "results" / a.exp
    out.mkdir(parents=True, exist_ok=True)
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                                capture_output=True, text=True).stdout.strip()
    except Exception:
        commit = ""
    cfg_dump = dict(vars(a), missions=ids, commit=commit, prior_sd=stats["sd"],
                    started=time.strftime("%Y-%m-%d %H:%M:%S"))
    json.dump(cfg_dump, open(out / "config.json", "w", encoding="utf-8"), indent=1)
    jobs = [(i, lag, c, cfgd) for i in ids for lag in a.lags for c in a.controllers]
    tic = time.time()
    with Pool(a.workers, initializer=_init) as pool, \
            open(out / "results.jsonl", "a", encoding="utf-8") as fh:
        for k, res in enumerate(pool.imap_unordered(_job, jobs, chunksize=1)):
            fh.write(json.dumps(res) + "\n")
            fh.flush()
            if (k + 1) % 50 == 0:
                print(f"{k+1}/{len(jobs)} {time.time()-tic:.0f}s", flush=True)
    print("done", len(jobs), f"{time.time()-tic:.0f}s")


if __name__ == "__main__":
    main()
