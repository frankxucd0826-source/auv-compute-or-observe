"""Where should the ship launch the vehicle? Test missions (148, map 3 days old), both truth models,
moderate vehicle, always GO with the low-power computer (fixed-0).

Candidates: the K strongest local maxima of the stale map (at least 5 cells = 10 km apart; the
first is the map's densest cell). Rehearsed choice: for each candidate, simulate the mission on
J imagined oceans drawn from the calibrated prior (stale map + correlated error), pick the
candidate with the lowest mean imagined regret, then run the real mission from it. Reported:
real regret when launching at the map's densest cell, at the rehearsed choice, and at the best
candidate in hindsight.

    python -E -X utf8 experiments/launch_choice.py [workers] -> results/launch_choice.json
"""
import csv
import json
import os
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
LAG, SAT_LEN, K, J, SEP = 3, 3.0, 5, 4, 5
_M = None


def _init():
    for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[k] = "1"
    global _M
    _M = dict(np.load(ROOT / "data" / "missions" / "chl_missions.npz"))


def candidates(f, mask):
    g = np.where(mask, f, -np.inf)
    order = np.argsort(g, axis=None)[::-1]
    out = []
    for k in order:
        iy, ix = divmod(int(k), f.shape[1])
        if not np.isfinite(g[iy, ix]):
            break
        if all(np.hypot(iy - y, ix - x) >= SEP for y, x in out):
            out.append((iy, ix))
        if len(out) == K:
            break
    return out


def _job(job):
    from oceanmeta.belief import gaussian_random_fields
    from oceanmeta.mission import Sensor, MissionConfig, run_mission
    from oceanmeta.platforms import PRESETS
    from oceanmeta import meta
    i, sat_err, stats = job
    li = list(_M["lags"]).index(LAG)
    truth = _M["truth"][i].astype(np.float64)
    if sat_err > 0:   # same small-scale field as experiments/run.py
        truth = truth + sat_err * gaussian_random_fields(1, *truth.shape, SAT_LEN, np.random.default_rng(7919 * i + 1))[0]
    mask, prior = _M["mask"][i], _M["prior"][i, li].astype(np.float64)
    sd = np.hypot(stats["sd"][str(LAG)], sat_err)
    length = stats["length_cells"][str(LAG)]
    plat = PRESETS["auv"](rate_low=20, rate_high=1000, p_think=20)
    cfg = MissionConfig(prior_length_cells=length)
    sensor = Sensor(noise_sd=0.1)
    seed = i * 31 + LAG
    cands = candidates(prior, mask)
    rng = np.random.default_rng(seed + 424242)
    imagined = prior[None] + sd * gaussian_random_fields(J, *prior.shape, length, rng)
    imag, real = [], []
    for c, (cy, cx) in enumerate(cands):
        start = (float(cx), float(cy))
        r = [run_mission(imagined[j], prior, sd, mask, start, plat, sensor, cfg, meta.Fixed(0),
                         seed + 1000 * (c + 1) + j)[0]["regret_avg"] for j in range(J)]
        imag.append(float(np.mean(r)))
        real.append(run_mission(truth, prior, sd, mask, start, plat, sensor, cfg, meta.Fixed(0), seed)[0]["regret_avg"])
    pick = int(np.argmin(imag))
    return dict(mission=i, sat_err=sat_err, n_cands=len(cands), map_max=real[0], rehearsed=real[pick],
                hindsight=min(real), pick=pick, imagined=imag, real=real)


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    rows = [r for r in csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8"))
            if r["split"] == "test"]
    stats = json.load(open(ROOT / "data" / "missions" / "prior_stats.json", encoding="utf-8"))
    jobs = [(int(r["id"]), s, stats) for s in (0.15, 0.0) for r in rows]
    with Pool(workers, initializer=_init) as pool:
        res = pool.map(_job, jobs, chunksize=2)
    rng = np.random.default_rng(0)
    summary = {}
    for s in (0.15, 0.0):
        sub = [x for x in res if x["sat_err"] == s]
        out = {k: float(np.mean([x[k] for x in sub])) for k in ("map_max", "rehearsed", "hindsight")}
        d = np.array([x["rehearsed"] - x["map_max"] for x in sub])
        boots = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(2000)]
        out["rehearsed_minus_map_max_ci95"] = [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]
        out["share_picked_map_max"] = float(np.mean([x["pick"] == 0 for x in sub]))
        out["n"] = len(sub)
        summary[str(s)] = out
    json.dump(dict(summary=summary, per_mission=res), open(ROOT / "results" / "launch_choice.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
