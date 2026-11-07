"""The example mission of the overview figure, chosen by a stated rule: the first test mission (date
order) where the expensive map decision is wrong by more than 3 h, a plausible counterexample flips it,
and the gated conservative choice picks the faster side. Saves the map, the counterexample and the
real field with each side's fastest route (expensive solver).

    python -E -X utf8 experiments/route_example.py  -> results/route_example.npz, .json
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))
from route_summary import load, side, worst_regret  # noqa: E402


def main():
    from oceanroute.fields import Snapshots
    from oceanroute.mission import Spec, Level, extreme_margin, margin, CAP
    from oceanroute.solver import Router
    from oceanroute import errormodel as EM
    P = json.load(open(ROOT / "results" / "route_summary_main.json", encoding="utf-8"))["params"]
    cfg = json.load(open(ROOT / "results" / "route_main_test" / "config.json", encoding="utf-8"))["cfg"]
    test = sorted(load("main", "test"), key=lambda r: (r["date"], r["s"][0]))
    pick = None
    for r in test:
        a_map, a_true = side(r["dJ_map_L2"]), side(r["dJ_true"])
        reg = r["JT"][a_map] - min(r["JT"].values())
        Rw = worst_regret(r, a_map, P["r"])
        a_rob = min("LR", key=lambda a: worst_regret(r, a, P["r"]))
        if a_map != a_true and reg > 3 and Rw > P["tau_robust"] and a_rob == a_true:
            pick = r
            break
    print("picked", pick["date"], "map", side(pick["dJ_map_L2"]), "true", side(pick["dJ_true"]), "JT", pick["JT"])
    S = Snapshots()
    yr = S.times.astype("datetime64[Y]").astype(int) + 1970
    dev = [int(j) for j in np.where((yr >= 2019) & (yr <= 2021))[0]]
    spec = Spec(pick["k"], tuple(pick["s"]), tuple(pick["g"]), tuple(pick["c"]), 15.0,
                (min(pick["s"][0], pick["g"][0]) - 60, max(pick["s"][0], pick["g"][0]) + 60,
                 min(pick["s"][1], pick["g"][1]) - 60, max(pick["s"][1], pick["g"][1]) + 60))
    lag, deg, V = cfg["lag"], cfg["deg"], cfg["V"]
    L1 = Level(S, spec, 1, deg, None, lag)
    L2 = Level(S, spec, 2, deg, None, lag)
    M = EM.load_or_fit(S, deg, lag, dev)
    for lv in (L1, L2):
        lv.Phi = EM.modes(S, M, lv.X, lv.Y, lv.grid.water, spec.box)
    a_map = side(pick["dJ_map_L2"])
    sign = +1 if a_map == "L" else -1          # make the map's side worse
    d, z, w, n = extreme_margin(L1, V, L1.start, sign, P["r"], iters=cfg["iters"])
    fields = {"map": L2.map, "counter": L2.field(z), "truth": L2.truth}
    out = dict(X=L2.X, Y=L2.Y, water=L2.grid.water, c=np.array(spec.c), s=np.array(spec.s), g=np.array(spec.g))
    meta = dict(date=pick["date"], map_side=a_map, true_side=side(pick["dJ_true"]), radius=P["r"], z_norm=float(np.linalg.norm(z)))
    for name, (u, v) in fields.items():
        out[name + "_u"], out[name + "_v"] = u, v
        R = Router(L2.grid, u, v, V)
        for a in "LR":
            dist, pred = R.solve(L2.side[a], L2.start)
            nodes = R.path(pred, L2.goal)
            out[f"{name}_route_{a}"] = np.array([L2.grid.xy(k) for k in nodes])
            meta[f"{name}_time_{a}"] = round(min(float(dist[L2.goal]), CAP), 2)
    np.savez(ROOT / "results" / "route_example.npz", **out)
    json.dump(meta, open(ROOT / "results" / "route_example.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(meta)


if __name__ == "__main__":
    main()
