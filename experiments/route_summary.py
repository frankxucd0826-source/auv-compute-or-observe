"""Score the route-decision policies from the per-mission records (experiments/route_eval.py).

Everything that is tuned is tuned on the development years (2019-2021) and applied unchanged to the
test years (2022-2024):
  r      plausible-set radius: the smallest r whose range of margins covers the real margin in
         >= 90% of development missions
  eps    numerical tolerance: 95th percentile of |cheap-solver margin - expensive-solver margin|
  tau_*  per kind of observation, the worst plausible regret above which the vehicle observes
  p0     ensemble gate: the flip probability above which the vehicle probes
Confidence intervals: 95%, bootstrap over days (missions on the same day move together).

    python -E -X utf8 experiments/route_summary.py main [surface_cost_h]  -> results/route_summary_main.json
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
UNITS = {"L0": 1, "L1": 8, "L2": 64}          # relative cost of one route solve (number of edges)
SURFACE_H = 1.0                                # surfacing to download a map
TAUS = (0.0, 0.25, 0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 1e9)


def load(tag, split):
    f = ROOT / "results" / f"route_{tag}_{split}" / "results.jsonl"
    recs = [json.loads(l) for l in open(f, encoding="utf-8")]
    return [r for r in recs if "skip" not in r]


def side(d):
    return "L" if d < 0 else "R"


def devs(r, rad):
    """Plausible range of the real margin minus the expensive map margin, radius rad (searched at
    r = 1 and 2; linear in between, proportional outside)."""
    d1 = r["dJ_map_L1"]
    p1 = (r["cx_lo_1.0"] - d1, r["cx_hi_1.0"] - d1)
    p2 = (r["cx_lo_2.0"] - d1, r["cx_hi_2.0"] - d1)
    if rad <= 1.0:
        lo, hi = p1[0] * rad, p1[1] * rad
    elif rad <= 2.0:
        w = rad - 1.0
        lo, hi = (1 - w) * p1[0] + w * p2[0], (1 - w) * p1[1] + w * p2[1]
    else:
        lo, hi = p2[0] * rad / 2, p2[1] * rad / 2
    return min(lo, 0.0), max(hi, 0.0)


def worst_regret(r, a, rad):
    lo, hi = devs(r, rad)
    d = r["dJ_map_L2"]
    return max(0.0, d + hi) if a == "L" else max(0.0, -(d + lo))


def ens_l2(r, n=None):
    return np.array(r["ens"][:n] if n else r["ens"]) - r["dJ_map_L1"] + r["dJ_map_L2"]


def outcomes(r, P):
    """Real trip time (h) of every policy for one mission; P holds the thresholds."""
    J = r["JT"]
    aL0, aL1, aL2 = side(r["dJ_map_L0"]), side(r["dJ_map_L1"]), side(r["dJ_map_L2"])
    a_num = aL2 if abs(r["dJ_map_L0"]) < P["eps"] else aL0
    e = ens_l2(r)
    a_bayes = side(e.mean())
    p_flip = float(np.mean(np.sign(e) != np.sign(r["dJ_map_L2"])))
    a_rob = min("LR", key=lambda a: worst_regret(r, a, P["r"]))
    R = worst_regret(r, aL2, P["r"])
    surf = J[side(r["dJ_map_fresh"])] + P["surface_h"]
    surf05 = J[side(r["dJ_map_fresh05"])] + P["surface_h"]
    o = {
        "地图+粗算": J[aL0], "地图+标准": J[aL1], "地图+精算": J[aL2], "按需精算": J[a_num],
        "集合期望（贝叶斯）": J[a_bayes], "保守（最坏后悔最小）": J[a_rob],
        "原地停留测": r["hover"]["total_h"],
        "总是沿途测30km": r["probe_30"]["total_h"], "总是沿途测60km": r["probe_60"]["total_h"],
        "总是沿途测30km后保守": r["probe_30"]["total_robust_h"],
        "总是绕行定点测": r["targeted"]["total_h"],
        "总是上浮取当天1°图": surf, "总是上浮取当天0.5°图": surf05,
        "反例门控→沿途测": r["probe_30"]["total_h"] if R > P["tau_probe"] else J[a_num],
        "反例门控→上浮取图": surf if R > P["tau_surface"] else J[a_num],
        "反例门控→上浮取0.5°图": surf05 if R > P["tau_surface05"] else J[a_num],
        "反例门控→绕行定点测": r["targeted"]["total_h"] if R > P["tau_targeted"] else J[a_num],
        "反例门控→保守": J[a_rob] if R > P["tau_robust"] else J[a_num],
        # proposed after the Gulf Stream test results (both sides' worst regrets near the cap): switch only
        # when the two worst regrets differ by more than the numerical tolerance; no new parameter is tuned
        "反例门控→保守（差距超过容限才改选）": (J[a_rob] if R - worst_regret(r, a_rob, P["r"]) > P["eps"] else J[aL2])
                                    if R > P["tau_robust"] else J[a_num],
        "反例门控→贝叶斯": J[a_bayes] if R > P["tau_bayes"] else J[a_num],
        "集合门控→沿途测": r["probe_30"]["total_h"] if p_flip > P["p0"] else J[aL2],
        "知道真相": min(J.values()),
    }
    info = dict(R=R, num_amb=abs(r["dJ_map_L0"]) < P["eps"], p_flip=p_flip, a_true=side(r["dJ_true"]),
                aL0=aL0, aL2=aL2, a_bayes=a_bayes, a_rob=a_rob)
    return o, info


GATES = {"tau_probe": "反例门控→沿途测", "tau_surface": "反例门控→上浮取图", "tau_surface05": "反例门控→上浮取0.5°图",
         "tau_targeted": "反例门控→绕行定点测", "tau_robust": "反例门控→保守", "tau_bayes": "反例门控→贝叶斯"}


def boot(vals, groups, B=2000, seed=0):
    rng = np.random.default_rng(seed)
    g = np.asarray(groups)
    ug = np.unique(g)
    idx = {k: np.where(g == k)[0] for k in ug}
    v = np.asarray(vals, float)
    means = [np.mean(np.concatenate([v[idx[k]] for k in rng.choice(ug, len(ug))])) for _ in range(B)]
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def auc(score, label):
    s, y = np.asarray(score, float), np.asarray(label, bool)
    pos, neg = s[y], s[~y]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    return float(np.mean(pos[:, None] > neg[None, :]) + 0.5 * np.mean(pos[:, None] == neg[None, :]))


def covered(r, rad):
    lo, hi = devs(r, rad)
    return r["dJ_map_L2"] + lo - 1e-9 <= r["dJ_true"] <= r["dJ_map_L2"] + hi + 1e-9


def calibrate(dev, surface_h):
    rads = [round(x, 2) for x in np.arange(0.25, 3.01, 0.25)]
    cover = {rad: float(np.mean([covered(r, rad) for r in dev])) for rad in rads}
    r_cal = next((rad for rad in rads if cover[rad] >= 0.9), rads[-1])
    eps = float(np.percentile([abs(r["dJ_map_L0"] - r["dJ_map_L2"]) for r in dev], 95))
    P = dict(r=r_cal, eps=eps, p0=0.0, surface_h=surface_h, **{k: 0.0 for k in GATES})
    for key, name in GATES.items():
        scores = [(np.mean([outcomes(r, dict(P, **{key: t}))[0][name] for r in dev]), t) for t in TAUS]
        P[key] = min(scores)[1]
    scores = [(np.mean([outcomes(r, dict(P, p0=p))[0]["集合门控→沿途测"] for r in dev]), p) for p in (0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 1.01)]
    P["p0"] = min(scores)[1]
    return P, cover


def summarise(recs, P):
    rows = [outcomes(r, P) for r in recs]
    names = list(rows[0][0])
    groups = [r["k"] for r in recs]
    oracle = np.array([o["知道真相"] for o, _ in rows])
    base = np.array([o["地图+精算"] for o, _ in rows])
    table = {}
    for n in names:
        v = np.array([o[n] for o, _ in rows])
        table[n] = dict(mean_h=float(v.mean()), regret_h=float((v - oracle).mean()), regret_ci=boot(v - oracle, groups),
                        minus_map=float((v - base).mean()), minus_map_ci=boot(v - base, groups),
                        median_regret_h=float(np.median(v - oracle)), p90_regret_h=float(np.percentile(v - oracle, 90)))
    info = [i for _, i in rows]
    wrong2 = np.array([i["aL2"] != i["a_true"] for i in info])
    wrong0 = np.array([i["aL0"] != i["a_true"] for i in info])
    reg2 = np.array([r["JT"][i["aL2"]] - min(r["JT"].values()) for r, i in zip(recs, info)])
    reg0 = np.array([r["JT"][i["aL0"]] - min(r["JT"].values()) for r, i in zip(recs, info)])
    amb = {str(rad): float(np.mean([worst_regret(r, side(r["dJ_map_L2"]), rad) > 0 for r in recs])) for rad in (0.25, 0.5, 1.0, 1.5, 2.0)}
    cats = dict(
        share_flip_possible_by_radius=amb,
        share_num_ambiguous=float(np.mean([i["num_amb"] for i in info])),
        wrong_cheap=float(wrong0.mean()), wrong_expensive=float(wrong2.mean()),
        regret_cheap=float(reg0.mean()), regret_expensive=float(reg2.mean()),
        cheap_errors_fixed_by_compute=float(np.mean(~wrong2[wrong0])) if wrong0.any() else float("nan"),
        expensive_errors=int(wrong2.sum()), costly_expensive_errors=int((reg2 > 1).sum()),
        share_regret_from_top10pct=float(np.sort(reg2)[::-1][:max(1, len(reg2) // 10)].sum() / max(reg2.sum(), 1e-9)),
        wrong_bayes=float(np.mean([i["a_bayes"] != i["a_true"] for i in info])),
        wrong_robust=float(np.mean([i["a_rob"] != i["a_true"] for i in info])),
    )
    costly = reg2 > 1.0
    n_match = int(round(np.mean([r["cx_solves_1.0"] for r in recs]) / 2))
    det = {"n_costly": int(costly.sum()), "n": len(recs),
           "auc_margin": auc([-abs(r["dJ_map_L2"]) for r in recs], costly),
           "auc_ensemble_32": auc([i["p_flip"] for i in info], costly),
           "auc_ensemble_compute_matched": auc([float(np.mean(np.sign(ens_l2(r, n_match)) != np.sign(r["dJ_map_L2"]))) for r in recs], costly),
           "n_match": n_match,
           "auc_counterexample": auc([i["R"] for i in info], costly),
           "auc_linear": auc([P["r"] * r["grad_norm"] - abs(r["dJ_map_L2"]) for r in recs], costly)}
    return dict(n=len(recs), n_days=len(set(groups)), mean_trip_h=float(oracle.mean()), table=table,
                categories=cats, detection=det)


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "main"
    surface_h = float(sys.argv[2]) if len(sys.argv) > 2 else SURFACE_H
    dev = load(tag, "dev")
    has_test = (ROOT / "results" / f"route_{tag}_test" / "done").exists()
    test = load(tag, "test") if has_test else dev
    P, cover = calibrate(dev, surface_h)
    out = dict(params=P, coverage_dev=cover, coverage_test_at_r=float(np.mean([covered(r, P["r"]) for r in test])),
               dev=summarise(dev, P), test=summarise(test, P), has_test=has_test)
    suffix = "" if surface_h == SURFACE_H else f"_surf{surface_h}"
    json.dump(out, open(ROOT / "results" / f"route_summary_{tag}{suffix}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("params", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in P.items()}, "test coverage", round(out["coverage_test_at_r"], 3))
    for split in ("dev", "test") if has_test else ("dev",):
        S = out[split]
        print(f"== {split}: {S['n']} missions on {S['n_days']} days, mean best trip {S['mean_trip_h']:.1f} h")
        for n, v in S["table"].items():
            print(f"  {n:16s} regret {v['regret_h']:5.2f} {np.round(v['regret_ci'], 2)}  vs map {v['minus_map']:+6.2f} {np.round(v['minus_map_ci'], 2)}  median {v['median_regret_h']:.2f} p90 {v['p90_regret_h']:.1f}")
        print("  categories", json.dumps(S["categories"], ensure_ascii=False))
        print("  detection", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in S["detection"].items()})


if __name__ == "__main__":
    main()
