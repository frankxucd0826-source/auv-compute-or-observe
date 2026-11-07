"""Where does the regret come from? Test missions (148, map 3 days old), both truth models.

Policies (all always GO; the route rules steer straight to one target, no planner):
  oracle_goto   knows the real ocean and heads straight for its densest cell
                (what motion alone costs: the vehicle must reach the water it reports)
  map_goto      trusts the stale map and heads straight for the map's densest cell
  fresh_planner the normal planner (low-power computer, moderate vehicle) given a same-day map
                instead of the 3-day-old one (what a perfect forecast of the map could buy)
Also, without simulation: distance from the start and from the stale map's densest cell to the
real densest cell, and the regret if the stale map's densest cell could be reported unvisited.

Start: "edge" = the mission's launch point on the window edge (as in all other experiments);
"mapmax" = the ship launches the vehicle at the stale map's densest cell. With "mapmax" the five
fixed time-allocation strategies are run too, to see how much the allocation matters there.

    python -E -X utf8 experiments/headroom.py edge|mapmax [workers]  -> results/headroom_<start>.json
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
LAG = 3
SAT_LEN = 3.0
_M = None


def _fixed(a):
    from oceanmeta import meta
    return lambda: meta.Fixed(a)


def _periodic(code):
    from oceanmeta import meta
    return lambda: meta.Periodic([int(c) for c in code])


STRATEGIES = {"fixed-0": _fixed(0), "fixed-1": _fixed(1), "periodic-100": _periodic("100"),
              "periodic-300": _periodic("300"), "periodic-200": _periodic("200")}


def _init():
    for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[k] = "1"
    global _M
    _M = dict(np.load(ROOT / "data" / "missions" / "chl_missions.npz"))


def _truth(i, sat_err):
    from oceanmeta.belief import gaussian_random_fields
    t = _M["truth"][i].astype(np.float64)
    if sat_err > 0:   # same small-scale field as experiments/run.py
        g = gaussian_random_fields(1, *t.shape, SAT_LEN, np.random.default_rng(7919 * i + 1))[0]
        t = t + sat_err * g
    return t


def _argmax(f, mask):
    k = int(np.argmax(np.where(mask, f, -np.inf)))
    return divmod(k, f.shape[1])        # (iy, ix)


def _job(job):
    from oceanmeta.mission import Mission, Sensor, MissionConfig, GO, run_mission
    from oceanmeta.platforms import PRESETS
    from oceanmeta import meta
    i, sat_err, policy, start, stats, start_mode = job
    li = list(_M["lags"]).index(LAG)
    truth, mask = _truth(i, sat_err), _M["mask"][i]
    plat = PRESETS["auv"](rate_low=20, rate_high=1000, p_think=20)     # moderate vehicle
    cfg = MissionConfig(prior_length_cells=stats["length_cells"][str(LAG)])
    sensor = Sensor(noise_sd=0.1)
    seed = i * 31 + LAG
    if start_mode == "mapmax":
        sy, sx = _argmax(_M["prior"][i, li], mask)
        start = (float(sx), float(sy))
    if policy in STRATEGIES:
        prior = _M["prior"][i, li].astype(np.float64)
        sd = np.hypot(stats["sd"][str(LAG)], sat_err)
        ctl = STRATEGIES[policy]()
        out, _ = run_mission(truth, prior, sd, mask, start, plat, sensor, cfg, ctl, seed)
    elif policy == "fresh_planner":
        prior = _M["truth"][i].astype(np.float64)          # same-day satellite map
        sd = np.hypot(0.02, sat_err)
        out, _ = run_mission(truth, prior, sd, mask, start, plat, sensor, cfg, meta.Fixed(0), seed)
    else:
        prior = _M["prior"][i, li].astype(np.float64)
        sd = np.hypot(stats["sd"][str(LAG)], sat_err)
        m = Mission(truth, prior, sd, mask, start, plat, sensor, cfg, np.random.default_rng(seed))
        ty, tx = _argmax(truth if policy == "oracle_goto" else prior, mask)
        target = np.array([[float(tx), float(ty)]])
        m.route_rule = lambda m_, fx, fy: target
        while not m.done:
            m.step(GO)
        out = m.report()
    return dict(mission=i, sat_err=sat_err, policy=policy, regret_avg=out["regret_avg"],
                regret_end=out["regret"])


def main():
    start_mode = sys.argv[1] if len(sys.argv) > 1 else "edge"
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    policies = ["oracle_goto", "map_goto", "fresh_planner"] if start_mode == "edge" else         ["oracle_goto", "fresh_planner"] + list(STRATEGIES)
    rows = [r for r in csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8"))
            if r["split"] == "test"]
    stats = json.load(open(ROOT / "data" / "missions" / "prior_stats.json", encoding="utf-8"))
    _init()
    li = list(_M["lags"]).index(LAG)
    geo = {}
    for sat_err in (0.15, 0.0):
        d_start, d_map, tele = [], [], []
        for r in rows:
            i = int(r["id"])
            t, mask = _truth(i, sat_err), _M["mask"][i]
            ty, tx = _argmax(t, mask)
            py, px = _argmax(_M["prior"][i, li], mask)
            d_start.append(2.0 * np.hypot(tx - float(r["start_x"]), ty - float(r["start_y"])))
            d_map.append(2.0 * np.hypot(tx - px, ty - py))
            tele.append(float(t[ty, tx] - t[py, px]))
        geo[str(sat_err)] = dict(
            km_start_to_max_median=float(np.median(d_start)),
            km_map_max_to_true_max_median=float(np.median(d_map)),
            share_map_max_within_4km=float(np.mean(np.array(d_map) <= 4.0)),
            regret_report_map_max_unvisited=float(np.mean(tele)))
    jobs = [(int(r["id"]), s, p, (float(r["start_x"]), float(r["start_y"])), stats, start_mode)
            for s in (0.15, 0.0) for p in policies for r in rows]
    with Pool(workers, initializer=_init) as pool:
        res = pool.map(_job, jobs, chunksize=4)
    summary = {}
    for s in (0.15, 0.0):
        for p in policies:
            v = np.array([x["regret_avg"] for x in res if x["sat_err"] == s and x["policy"] == p])
            summary[f"{s}/{p}"] = dict(mean=float(v.mean()), se=float(v.std(ddof=1) / np.sqrt(len(v))), n=len(v))
        strat = [p for p in policies if p in STRATEGIES]
        if strat:   # best of the five in hindsight, per mission (the allocation's headroom)
            per = {}
            for x in res:
                if x["sat_err"] == s and x["policy"] in strat:
                    per.setdefault(x["mission"], []).append(x["regret_avg"])
            best = np.array([min(v) for v in per.values()])
            summary[f"{s}/hindsight_best_strategy"] = dict(mean=float(best.mean()), n=len(best))
    out = dict(geometry=geo, regret_avg=summary, per_mission=res)
    json.dump(out, open(ROOT / "results" / f"headroom_{start_mode}.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps(dict(geometry=geo, regret_avg=summary), indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
