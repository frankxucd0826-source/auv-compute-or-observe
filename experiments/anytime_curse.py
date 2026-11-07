"""Does thinking longer on a stale map give better routes? For each mission, plan from the
start position on the prior belief with growing rollout budgets and compare the value the
planner believes its route has with the value the route really has (scored on the true field).
Repeated with the map's uncertainty stated honestly (calibrated) and understated (the map
treated as more accurate than it is).

    python experiments/anytime_curse.py --out curse0 --split dev --n 60
"""
import argparse
import csv
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

BUDGETS = [64, 200, 600, 2000, 6000, 20000, 60000, 200000]
SCALES = [0.25, 0.5, 1.0, 1.5]


def _job(job):
    for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[k] = "1"
    import numpy as np
    from oceanmeta.belief import EnsembleBelief, gaussian_random_fields
    from oceanmeta.planner import CEMPlanner, score_routes
    i, start, lag, sat_err, stats = job
    M = np.load(ROOT / "data" / "missions" / "chl_missions.npz")
    li = list(M["lags"]).index(lag)
    mask = M["mask"][i]
    truth = M["truth"][i] + sat_err * gaussian_random_fields(1, 40, 40, 3.0, np.random.default_rng(7919 * i + 1))[0]
    prior = M["prior"][i, li]
    sd0 = float(np.hypot(stats["sd"][str(lag)], sat_err))
    speed = 1.5 * 60 / 2000          # cells per minute
    t_left = 8 * 60                  # plan the first 8 hours
    out = []
    for scale in SCALES:
        for seed in range(3):
            rng = np.random.default_rng(1000 * seed + i)
            B = EnsembleBelief.from_prior(prior, sd0 * scale, stats["length_cells"][str(lag)], 48, mask, rng)
            X = B.X.reshape(48, -1)
            T = truth.reshape(1, -1)
            for b in BUDGETS:
                # the search sees the first 32 imagined oceans; the last 16 are kept aside
                p = CEMPlanner((40, 40), mask, rng=np.random.default_rng(seed), n_holdout=16)
                plan, v = p.think(X, start[0], start[1], -np.inf, speed, t_left, b)
                if plan is None:
                    continue
                V = score_routes(start[0], start[1], plan[None], X, np.arange(48), -np.inf, speed, t_left, mask, t_left)[0]
                v_true = score_routes(start[0], start[1], plan[None], T, np.arange(1), -np.inf, speed, t_left, mask, t_left)[0, 0]
                out.append(dict(mission=int(i), scale=scale, seed=seed, budget=b, believed=float(v),
                                believed_all=float(V.mean()), believed_holdout=float(V[32:].mean()),
                                true=float(v_true), true_max=float(truth[mask].max())))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--split", default="dev")
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--lag", type=int, default=3)
    ap.add_argument("--sat-err", type=float, default=0.15)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    import numpy as np
    from multiprocessing import Pool
    rows = [r for r in csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8"))
            if r["split"] == a.split]
    stats = json.load(open(ROOT / "data" / "missions" / "prior_stats.json", encoding="utf-8"))
    rng = np.random.default_rng(0)
    rows = [rows[j] for j in rng.choice(len(rows), min(a.n, len(rows)), replace=False)]
    jobs = [(int(r["id"]), (float(r["start_x"]), float(r["start_y"])), a.lag, a.sat_err, stats) for r in rows]
    out = ROOT / "results" / a.out
    out.mkdir(parents=True, exist_ok=True)
    json.dump(vars(a), open(out / "config.json", "w"), indent=1)
    with Pool(a.workers) as pool, open(out / "results.jsonl", "w", encoding="utf-8") as fh:
        for res in pool.imap_unordered(_job, jobs):
            for r in res:
                fh.write(json.dumps(r) + "\n")
    import pandas as pd
    df = pd.DataFrame([json.loads(l) for l in open(out / "results.jsonl", encoding="utf-8")])
    df["gap"] = df["believed_holdout"] - df["true"]
    print(df.groupby(["scale", "budget"])[["believed", "believed_holdout", "true", "gap"]].mean().round(3).to_string())


if __name__ == "__main__":
    main()
