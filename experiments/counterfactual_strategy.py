"""Strategy-level counterfactual missions for learning the controller.

A single 20-minute choice changes the final outcome by about 0.01 (log10 chlorophyll) and the
effect is buried in noise. Here, at a few decision points of a mission, the mission is copied
once per strategy and each copy follows that strategy to the end:
    0 go                          (always go, low-power planning)
    1 think while going           (always use the high-performance computer)
    2 think one interval in three
    3 stop and think one interval in three
    4 stop and resample one interval in three
Common random numbers are used for the copies. One example = the features at that point and
the five final regrets.

    python experiments/counterfactual_strategy.py --out cfs1 --n 274 --repeat 2 --workers 4
"""
import argparse
import copy
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))

STRATEGIES = [[0], [1], [1, 0, 0], [3, 0, 0], [2, 0, 0]]
STRATEGY_NAMES = ["go", "think while going", "think 1 in 3", "stop and think 1 in 3", "stop and resample 1 in 3"]


def _init():
    for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[k] = "1"
    import counterfactual as cf
    cf._init()


def follow(m, pattern):
    k = 0
    while not m.done:
        m.step(pattern[k % len(pattern)])
        k += 1
    return m.report()["regret"]


def _job(job):
    import numpy as np
    import counterfactual as cf
    from oceanmeta.features import features
    i, start, seed, date = job
    rng = np.random.default_rng(seed)
    c = cf.draw_conditions(rng)
    m, _ = cf.build(i, c, start, seed)
    n_steps = int(min(m.platform.t_max_h * 60, m.platform.energy_wh / 45 * 60) / m.cfg.interval_min)
    # branch at the first decision with a plan, and at two random later points
    later = sorted(rng.choice(np.arange(4, max(5, n_steps - 6)), 2, replace=False).tolist())
    branch_at = {1, *later}
    base = STRATEGIES[int(rng.integers(len(STRATEGIES)))]   # behaviour before branching
    out = []
    k = 0
    while not m.done:
        if k in branch_at and m.exec_plan is not None:
            x = features(m)
            regrets = []
            for s in STRATEGIES:
                mc = copy.deepcopy(m)
                mc.rng = np.random.default_rng(seed * 7 + k)
                mc.planner.rng = mc.rng
                regrets.append(follow(mc, s))
            out.append(dict(mission=int(i), date=date, step=k, cond=c, x=x.tolist(), regret=regrets))
        m.step(base[k % len(base)])
        k += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=274)
    ap.add_argument("--repeat", type=int, default=2)
    ap.add_argument("--seed", type=int, default=2)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    import csv
    import numpy as np
    from multiprocessing import Pool
    rows = list(csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
    dev = [r for r in rows if r["split"] == "dev"]
    rng = np.random.default_rng(a.seed)
    pick = rng.choice(len(dev), min(a.n, len(dev)), replace=False)
    jobs = [(int(dev[j]["id"]), (float(dev[j]["start_x"]), float(dev[j]["start_y"])),
             int(rng.integers(1 << 30)), dev[j]["date"]) for _ in range(a.repeat) for j in pick]
    out = ROOT / "results" / a.out
    out.mkdir(parents=True, exist_ok=True)
    json.dump(dict(vars(a), strategies=STRATEGIES), open(out / "config.json", "w"), indent=1)
    tic = time.time()
    n = 0
    with Pool(a.workers, initializer=_init) as pool, open(out / "data.jsonl", "a", encoding="utf-8") as fh:
        for res in pool.imap_unordered(_job, jobs, chunksize=1):
            for r in res:
                fh.write(json.dumps(r) + "\n")
                n += 1
            fh.flush()
    print("done", n, "examples", f"{time.time()-tic:.0f}s")


if __name__ == "__main__":
    main()
