"""Route decisions under a coarse current map: everything needed to score the policies offline.

For each mission (two per HYCOM snapshot; development years 2019-2021, test years 2022-2024):
  truth     optimal time on each side on the real field (2 km grid, 32 directions)
  map       margin dJ = J_L - J_R on the coarse map with a cheap (8 km, 8 dir), standard (4 km, 16)
            and expensive (2 km, 32) solver -- "more computation"
  ensemble  dJ on M plausible fields (map + analogue sub-grid anomalies, z ~ N(0, I)), standard solver
  counter   largest and smallest dJ over plausible fields |z| <= r (gradient search), r = 1.5 and 3,
            and the linear estimate dJ0 +- r |grad| for any r
  measure   probe: follow the map's route for 30 or 60 km, measuring the current on the way, then
            keep the side or switch; targeted: go to the point (ahead, within 40 km) where the
            counterexample field differs most from the map, measuring on the way, then decide;
            hover: 2 h at the start, 12 measurements, then decide.
Every outcome is the real travel time (hours) including the measuring trip.

    python -E -X utf8 experiments/route_eval.py --split dev --limit 120 --workers 4 --tag pilot
"""
import argparse
import json
import os
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
_S = None
SPLIT_YEARS = {"dev": (2019, 2021), "test": (2022, 2024)}


def _init():
    for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[k] = "1"
    global _S
    from oceanroute.fields import Snapshots
    _S = Snapshots()


def years(S):
    return S.times.astype("datetime64[Y]").astype(int) + 1970


def line_nodes(lv, p, q, step=4.0):
    n = max(2, int(np.hypot(q[0] - p[0], q[1] - p[1]) / step) + 1)
    pts = [(p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t) for t in np.linspace(0, 1, n)]
    return sorted({lv.grid.node(*pt) for pt in pts})


def measure_and_decide(lv1, lv2, cfg, src_xy, dst_xy, nodes, sigma, rng, T_transit, extra_h=0.0):
    """Measure the real current at `nodes` of the standard grid (+ noise), update the analogue
    weights, decide at dst_xy on the posterior-mean field with the expensive solver; return the
    record with the real time of the whole trip."""
    from oceanroute.mission import posterior, margin, CAP
    tu, tv = lv1.truth
    vals = (tu.ravel()[nodes] + cfg["noise"] * rng.standard_normal(len(nodes)),
            tv.ravel()[nodes] + cfg["noise"] * rng.standard_normal(len(nodes)))
    m, P = posterior(lv1, nodes, vals, cfg["sigma"])
    src2 = lv2.grid.node(*dst_xy)
    dpost, _, _ = margin(lv2, lv2.field(m), cfg["V"], src2)
    a = "L" if dpost < 0 else "R"
    # the same choice made conservatively: the side whose worst plausible regret (posterior
    # ellipsoid, radius r_post) is smaller, found by the counterexample search on the standard grid
    from oceanroute.mission import extreme_margin
    Lc = np.linalg.cholesky(P + 1e-12 * np.eye(len(m)))
    src1 = lv1.grid.node(*dst_xy)
    d1m, _, _ = margin(lv1, lv1.field(m), cfg["V"], src1)
    hi, _, _, _ = extreme_margin(lv1, cfg["V"], src1, +1, cfg["r_post"], m=m, Lc=Lc, iters=4)
    lo, _, _, _ = extreme_margin(lv1, cfg["V"], src1, -1, cfg["r_post"], m=m, Lc=Lc, iters=4)
    reg_L = max(0.0, dpost + (hi - d1m))
    reg_R = max(0.0, -(dpost + (lo - d1m)))
    a_rob = "L" if reg_L < reg_R else "R"
    from oceanroute.solver import Router
    R = Router(lv2.grid, lv2.truth[0], lv2.truth[1], cfg["V"])
    JT = {}
    for s in "LR":
        d, _ = R.solve(lv2.side[s], src2)
        JT[s] = min(float(d[lv2.goal]), CAP)
    return dict(choice=a, dJ_post=float(dpost), transit_h=float(T_transit), extra_h=extra_h,
                total_h=float(T_transit + extra_h + JT[a]), JT_from=JT, n_meas=len(nodes),
                choice_robust=a_rob, total_robust_h=float(T_transit + extra_h + JT[a_rob]),
                post_lo=float(dpost + (lo - d1m)), post_hi=float(dpost + (hi - d1m)))


def _job(job):
    from oceanroute.mission import Level, margin, extreme_margin, CAP
    from oceanroute.solver import Router
    spec, cfg, pool = job
    S = _S
    tic = time.time()
    V, deg = cfg["V"], cfg["deg"]
    rng = np.random.default_rng(cfg["seed"] * 7919 + spec.k * 31 + int(spec.s[0] * 10) % 997)
    K = None
    box = spec.box
    t0 = S.times[spec.k]
    lag = cfg["lag"]
    cand = [j for j in pool if j - lag >= 0 and abs(int((S.times[j] - t0).astype(int))) > cfg["exclude_days"]]
    dist = np.array([S.coarse_distance(spec.k - lag, j - lag, deg, box) for j in cand])
    analogues = [cand[i] for i in np.argsort(dist)[:cfg["K"]]]
    use_analogues = cfg["basis"] == "analog"
    L0 = Level(S, spec, 0, deg, None, lag)
    L1 = Level(S, spec, 1, deg, analogues if use_analogues else None, lag)
    L2 = Level(S, spec, 2, deg, analogues if use_analogues else None, lag)
    if not use_analogues:            # calibrated error model: divergence-free, locally correlated
        from oceanroute import errormodel as EM
        M = EM.load_or_fit(S, deg, lag, pool)
        for lv in (L1, L2):
            lv.Phi = EM.modes(S, M, lv.X, lv.Y, lv.grid.water, spec.box, scale=cfg["ell_scale"])
    rec = dict(k=int(spec.k), date=str(t0), map_age_days=int((t0 - S.times[spec.k - lag]).astype(int)),
               s=spec.s, g=spec.g, c=spec.c, analogue_dist=float(np.sort(dist)[cfg["K"] - 1]))
    # truth from the start: both sides and the free-water transit times
    Rt = Router(L2.grid, L2.truth[0], L2.truth[1], V)
    JT = {}
    for a in "LR":
        d, _ = Rt.solve(L2.side[a], L2.start)
        JT[a] = min(float(d[L2.goal]), CAP)
    if JT["L"] >= CAP and JT["R"] >= CAP:
        rec["skip"] = "both sides impassable"
        return rec
    d_free, _ = Rt.solve(L2.free, L2.start)
    rec.update(JT=JT, dJ_true=JT["L"] - JT["R"])
    # the map, three solver budgets
    for name, lv in (("L0", L0), ("L1", L1), ("L2", L2)):
        rec["dJ_map_" + name] = margin(lv, lv.map, V, lv.start)[0]
    # remote observation: surface and download today's map (same resolution, and a finer one)
    for name, d_fresh in (("fresh", deg), ("fresh05", 0.5)):
        fm = S.coarse_at(spec.k, d_fresh, L2.X, L2.Y)
        rec["dJ_map_" + name] = margin(L2, fm, V, L2.start)[0]
    # ensemble
    Z = rng.standard_normal((cfg["M"], L1.Phi.shape[0]))
    rec["ens"] = [float(margin(L1, L1.field(z), V, L1.start)[0]) for z in Z]
    # gradient of dJ at the map (linear estimate for any radius)
    d0, R1, out1 = margin(L1, L1.map, V, L1.start)
    G = np.zeros((L1.grid.ny, L1.grid.nx, 2))
    if out1["L"][0] < CAP:
        G += R1.gradient(R1.path(out1["L"][1], L1.goal))
    if out1["R"][0] < CAP:
        G -= R1.gradient(R1.path(out1["R"][1], L1.goal))
    gz = np.tensordot(L1.Phi, G, axes=([1, 2, 3], [0, 1, 2]))
    rec["grad_norm"] = float(np.linalg.norm(gz))
    # counterexamples (nested radii: the larger search also starts from the smaller one's answer)
    cx = {}
    prev = None
    for r in cfg["radii"]:
        ih = None if prev is None else prev[0] * (r / prev[2])
        il = None if prev is None else prev[1] * (r / prev[2])
        hi, zhi, whi, n1 = extreme_margin(L1, V, L1.start, +1, r, iters=cfg["iters"], w_init=ih)
        lo, zlo, wlo, n2 = extreme_margin(L1, V, L1.start, -1, r, iters=cfg["iters"], w_init=il)
        rec[f"cx_hi_{r}"], rec[f"cx_lo_{r}"], rec[f"cx_solves_{r}"] = float(hi), float(lo), n1 + n2
        cx[r] = (zhi, zlo)
        prev = (whi, wlo, r)
    # targeted measurement point from the counterexample against the expensive map decision
    r0 = cfg["radii"][0]
    a_map = "L" if rec["dJ_map_L2"] < 0 else "R"
    zc = cx[r0][0] if a_map == "L" else cx[r0][1]
    diff = np.tensordot(zc, L1.Phi, axes=(0, 0))
    mag = np.hypot(diff[..., 0], diff[..., 1])
    gx, gy = L1.grid.X, L1.grid.Y
    ahead = (gx - spec.s[0]) * (spec.c[0] - spec.s[0]) + (gy - spec.s[1]) * (spec.c[1] - spec.s[1]) >= 0
    ok = L1.grid.water & ahead & (np.hypot(gx - spec.s[0], gy - spec.s[1]) <= cfg["reach_km"]) & \
        (np.hypot(gx - spec.c[0], gy - spec.c[1]) > spec.radius + 4)
    mag = np.where(ok, mag, -1)
    kx = int(np.argmax(mag))
    xs = L1.grid.xy(kx)
    T_x = float(d_free[L2.grid.node(*xs)])
    nodes = line_nodes(L1, spec.s, xs)
    rec["targeted"] = measure_and_decide(L1, L2, cfg, spec.s, xs, nodes, cfg["sigma"], rng, min(T_x, CAP))
    rec["targeted"]["xy"] = xs
    rec["targeted"]["diff_ms"] = float(mag.flat[kx])
    # probe on the way: travel the first probe_km of the side the map chose (as everywhere here, the
    # vehicle is assumed to sail each side optimally for the real currents), measuring the current,
    # then keep the side or switch (decided on the posterior-mean field with the expensive solver).
    # Keeping the side costs nothing extra; switching costs the trip back across.
    _, pred_t = Rt.solve(L2.side[a_map], L2.start)
    route = Rt.path(pred_t, L2.goal)
    pts = np.array([L2.grid.xy(n) for n in route])
    seg = np.r_[0.0, np.cumsum(np.hypot(np.diff(pts[:, 0]), np.diff(pts[:, 1])))]
    for km in cfg["probe_km"]:
        j = min(max(int(np.searchsorted(seg, km)), 1), len(route) - 1)
        part = route[:j + 1]
        T_p = float(Rt.t[L2.grid.edges_of(part)].sum())
        nodes1 = sorted({L1.grid.node(*L2.grid.xy(n)) for n in part[::2]})
        res = measure_and_decide(L1, L2, cfg, spec.s, L2.grid.xy(part[-1]), nodes1, cfg["sigma"], rng, min(T_p, CAP))
        if res["choice"] == a_map:              # stays on the optimal path of its side
            res["total_h"] = JT[a_map]
        if res["choice_robust"] == a_map:
            res["total_robust_h"] = JT[a_map]
        rec[f"probe_{int(km)}"] = res
    rec["a_map"] = a_map
    # hover at the start
    n0 = L1.start
    rec["hover"] = measure_and_decide(L1, L2, cfg, spec.s, spec.s, [n0] * 12, cfg["sigma"], rng, 0.0,
                                      extra_h=cfg["hover_h"])
    rec["wall_s"] = round(time.time() - tic, 1)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="dev")
    ap.add_argument("--per-snap", type=int, default=2)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--tag", default="main")
    ap.add_argument("--deg", type=float, default=1.0)
    ap.add_argument("--V", type=float, default=1.0)
    ap.add_argument("--K", type=int, default=40)
    ap.add_argument("--M", type=int, default=32)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--min-speed", type=float, default=0.3)
    ap.add_argument("--lag", type=int, default=1, help="map age in snapshots (3 days each)")
    ap.add_argument("--basis", default="gp", choices=["gp", "analog"])
    ap.add_argument("--ell-scale", type=float, default=1.0)
    ap.add_argument("--sigma", type=float, default=0.08)
    a = ap.parse_args()
    cfg = dict(V=a.V, deg=a.deg, K=a.K, M=a.M, seed=a.seed, radii=[1.0, 2.0], iters=6, noise=0.05,
               sigma=0.10, reach_km=40.0, probe_km=[30.0, 60.0], hover_h=2.0, exclude_days=15,
               min_speed=a.min_speed, lag=a.lag, basis=a.basis, ell_scale=a.ell_scale)
    cfg["sigma"] = a.sigma
    cfg["r_post"] = 1.5
    _init()
    S = _S
    from oceanroute.mission import sample_specs
    yr = years(S)
    dev = [int(j) for j in np.where((yr >= 2019) & (yr <= 2021))[0]]
    lo, hi = SPLIT_YEARS[a.split]
    snaps = [int(j) for j in np.where((yr >= lo) & (yr <= hi))[0] if j - a.lag >= 0]
    if S.alt is not None:      # satellite map: skip days whose map would be more than a day older than intended
        fresh = lambda j: S.alt_age_days[j] <= 1                     # (the product has gaps, one of 99 days in 2019)
        dev = [j for j in dev if j - a.lag >= 0 and fresh(j - a.lag)]
        snaps = [k for k in snaps if fresh(k) and fresh(k - a.lag)]
        print("satellite map: kept", len(snaps), "snapshots,", len(dev), "development snapshots for the error model", flush=True)
    rng = np.random.default_rng(a.seed + (0 if a.split == "dev" else 1000))
    specs = []
    for k in snaps:
        specs += sample_specs(S, k, np.random.default_rng(rng.integers(1 << 31)), a.per_snap,
                              min_speed=a.min_speed, deg=a.deg, lag=a.lag)
    if a.limit:
        idx = np.random.default_rng(5).choice(len(specs), min(a.limit, len(specs)), replace=False)
        specs = [specs[i] for i in sorted(idx)]
    if a.basis == "gp":
        from oceanroute import errormodel as EM
        M = EM.load_or_fit(S, a.deg, a.lag, dev)
        print("error model: ell", round(float(M["ell"]), 1), "km", flush=True)
    out = ROOT / "results" / f"route_{a.tag}_{a.split}"
    out.mkdir(parents=True, exist_ok=True)
    json.dump(dict(vars(a), cfg=cfg, n_specs=len(specs), started=time.strftime("%Y-%m-%d %H:%M:%S")),
              open(out / "config.json", "w", encoding="utf-8"), indent=1)
    print(len(specs), "missions", flush=True)
    jobs = [(sp, cfg, dev) for sp in specs]
    tic = time.time()
    with Pool(a.workers, initializer=_init) as pool, open(out / "results.jsonl", "w", encoding="utf-8") as fh:
        for i, rec in enumerate(pool.imap_unordered(_job, jobs, chunksize=1)):
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            if (i + 1) % 20 == 0:
                print(f"{i + 1}/{len(jobs)} {time.time() - tic:.0f}s", flush=True)
    (out / "done").write_text("ok")
    print("done", f"{time.time() - tic:.0f}s", flush=True)


if __name__ == "__main__":
    main()
