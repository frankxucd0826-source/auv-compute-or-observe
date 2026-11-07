"""Counterfactual missions for learning the controller.

Missions on development windows are run with a random behaviour policy under randomly drawn
conditions (computer speed, computer power, map error, sensor noise, map age). At a few random
decision points the mission is copied four times; each copy takes one of the four actions and
then finishes with the continuation policy (always go, low-power planning). The four final
regrets, with the features of the decision point, are one training example: which use of the
next 20 minutes leads to the better outcome from here.

    python experiments/counterfactual.py --out cf0 --n 120 --branches 3 --workers 8
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

_M = None
_S = None
RANGES = dict(rate_low=(10, 300), p_think=(5, 30), sat_err=(0.05, 0.3), noise=(0.05, 0.3))


def _init():
    for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[k] = "1"
    global _M, _S
    import numpy as np
    _M = dict(np.load(ROOT / "data" / "missions" / "chl_missions.npz"))
    _S = json.load(open(ROOT / "data" / "missions" / "prior_stats.json", encoding="utf-8"))


def draw_conditions(rng):
    import numpy as np
    lo, hi = RANGES["rate_low"]
    c = dict(rate_low=float(np.exp(rng.uniform(np.log(lo), np.log(hi)))),
             p_think=float(rng.uniform(*RANGES["p_think"])),
             sat_err=float(rng.uniform(*RANGES["sat_err"])),
             noise=float(rng.uniform(*RANGES["noise"])),
             lag=int(rng.choice(_M["lags"])))
    return c


def build(i, c, start, seed):
    import numpy as np
    from oceanmeta.belief import gaussian_random_fields
    from oceanmeta.mission import Mission, Sensor, MissionConfig
    from oceanmeta.platforms import auv
    li = list(_M["lags"]).index(c["lag"])
    truth = _M["truth"][i] + c["sat_err"] * gaussian_random_fields(
        1, 40, 40, 3.0, np.random.default_rng(7919 * i + 1))[0]
    sd = float(np.hypot(_S["sd"][str(c["lag"])], c["sat_err"]))
    plat = auv(rate_low=c["rate_low"], rate_high=50 * c["rate_low"], p_think=c["p_think"])
    cfg = MissionConfig(prior_length_cells=_S["length_cells"][str(c["lag"])])
    m = Mission(truth, _M["prior"][i, li], sd, _M["mask"][i], start, plat, Sensor(noise_sd=c["noise"]),
                cfg, np.random.default_rng(seed))
    return m, sd


def finish(m, policy):
    while not m.done:
        m.step(policy(m))
    return m.report()["regret"]


def _job(job):
    import numpy as np
    from oceanmeta.features import features
    i, start, seed, n_branch, date = job
    rng = np.random.default_rng(seed)
    c = draw_conditions(rng)
    m, sd = build(i, c, start, seed)
    n_steps = int(min(m.platform.t_max_h * 60, m.platform.energy_wh / 45 * 60) / m.cfg.interval_min)
    branch_at = set(rng.choice(np.arange(1, max(2, n_steps - 2)), n_branch, replace=False).tolist())
    probs = np.array([0.55, 0.2, 0.15, 0.1])
    out = []
    k = 0
    while not m.done:
        if k in branch_at and m.exec_plan is not None:
            x = features(m)
            regrets = []
            for a in range(4):
                mc = copy.deepcopy(m)
                mc.rng = np.random.default_rng(seed * 7 + k)      # common random numbers
                mc.planner.rng = mc.rng
                mc.step(a)
                regrets.append(finish(mc, lambda mm: 0))
            out.append(dict(mission=int(i), date=date, step=k, cond=c, x=x.tolist(), regret=regrets))
        a = int(rng.choice(4, p=probs))
        m.step(a)
        k += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=120)
    ap.add_argument("--branches", type=int, default=3)
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    import csv
    import numpy as np
    from multiprocessing import Pool
    rows = list(csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
    dev = [r for r in rows if r["split"] == "dev"]
    rng = np.random.default_rng(a.seed)
    pick = rng.choice(len(dev), min(a.n, len(dev)), replace=False)
    jobs = []
    for rep in range(a.repeat):
        for j in pick:
            r = dev[j]
            jobs.append((int(r["id"]), (float(r["start_x"]), float(r["start_y"])),
                         int(rng.integers(1 << 30)), a.branches, r["date"]))
    out = ROOT / "results" / a.out
    out.mkdir(parents=True, exist_ok=True)
    json.dump(dict(vars(a), ranges=RANGES), open(out / "config.json", "w"), indent=1)
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
