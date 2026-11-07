"""Where does the left/right decision depend on information the coarse map lacks?
For development missions: the real margin and the map margin (expensive solver) for several map
resolutions, map ages (the map is the coarse field of an earlier snapshot) and vehicle speeds;
reports how often the map picks the wrong side and the mean regret (hours).

    python -E -X utf8 experiments/route_scan.py [n_missions] [workers] -> results/route_scan.json
"""
import json
import os
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
_S = None
DEGS, LAGS, SPEEDS = (0.25, 0.5, 1.0), (0, 1, 2), (0.75, 1.0, 1.5)   # lags in snapshots (3 days each)


def _init():
    for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[k] = "1"
    global _S
    from oceanroute.fields import Snapshots
    _S = Snapshots()


def _job(spec):
    from oceanroute.mission import Level, CAP
    from oceanroute.solver import Router
    S = _S
    lv = Level(S, spec, 2, 0.5, None)
    out = dict(k=spec.k)
    for V in SPEEDS:
        R = Router(lv.grid, lv.truth[0], lv.truth[1], V)
        JT = {a: min(float(R.solve(lv.side[a], lv.start)[0][lv.goal]), CAP) for a in "LR"}
        out[f"JT_{V}"] = JT
        for deg in DEGS:
            for lag in LAGS:
                if spec.k - lag < 0:
                    continue
                mu, mv = S.coarse_at(spec.k - lag, deg, lv.X, lv.Y)
                Rm = Router(lv.grid, mu, mv, V)
                JM = {a: min(float(Rm.solve(lv.side[a], lv.start)[0][lv.goal]), CAP) for a in "LR"}
                out[f"dJm_{V}_{deg}_{lag}"] = JM["L"] - JM["R"]
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 160
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    _init()
    from oceanroute.mission import sample_specs
    yr = _S.times.astype("datetime64[Y]").astype(int) + 1970
    dev = np.where((yr >= 2019) & (yr <= 2021))[0]
    rng = np.random.default_rng(11)
    specs = []
    for k in rng.choice(dev[3:], n, replace=False):
        specs += sample_specs(_S, int(k), np.random.default_rng(int(k)), 1, min_speed=0.3)
    with Pool(workers, initializer=_init) as pool:
        res = pool.map(_job, specs, chunksize=2)
    summary = {}
    for V in SPEEDS:
        for deg in DEGS:
            for lag in LAGS:
                key = f"dJm_{V}_{deg}_{lag}"
                rows = [r for r in res if key in r and min(r[f"JT_{V}"].values()) < 200]
                wrong = [("L" if r[key] < 0 else "R") != ("L" if r[f"JT_{V}"]["L"] < r[f"JT_{V}"]["R"] else "R") for r in rows]
                reg = [r[f"JT_{V}"]["L" if r[key] < 0 else "R"] - min(r[f"JT_{V}"].values()) for r in rows]
                stake = [abs(r[f"JT_{V}"]["L"] - r[f"JT_{V}"]["R"]) for r in rows]
                summary[key] = dict(n=len(rows), wrong=float(np.mean(wrong)), regret_h=float(np.mean(reg)),
                                    costly_1h=float(np.mean(np.array(reg) > 1)), median_stake_h=float(np.median(stake)),
                                    mean_trip_h=float(np.mean([min(r[f"JT_{V}"].values()) for r in rows])))
    json.dump(dict(summary=summary, per_mission=res), open(ROOT / "results" / "route_scan.json", "w", encoding="utf-8"), indent=1)
    for k, v in summary.items():
        print(k, {a: round(b, 3) for a, b in v.items()})


if __name__ == "__main__":
    main()
