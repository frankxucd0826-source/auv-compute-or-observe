"""Why does choosing the side with the smaller expected time (32 plausible fields) lose to choosing the
side with the smaller worst plausible regret? Scores, on the same missions:
  map            the expensive solver on the coarse map
  expected(n)    the side with the smaller mean time over the first n of 1024 fresh plausible fields
  midpoint(n)    the side favoured by the midpoint of the 6.7%-93.3% range of those n margins
                 (the sampled counterpart of the worst-regret rule: for a margin that is linear in the
                 field both equal the map's choice; they differ only where the response is lopsided)
  worst regret   the main run's rule (gradient search, radius 1.5, about 71 route solves)
and measures how well each rule's correction of the map margin predicts the real correction, and how
much of the map's loss each risk score puts in its top 20% of missions (worst regret of the search;
flip share and expected regret of keeping the map's side over n random plausible fields).
Margins on the standard solver are moved to the expensive one as in route_summary.py.

    python -E -X utf8 experiments/route_ensemble_analysis.py -> results/route_ensemble_size.json
"""
import gzip
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
import route_summary as RS  # noqa: E402

NS = (8, 16, 32, 64, 128, 256, 512, 1024)
Q = 0.0668                       # two-sided 1.5-sigma quantiles, matching the radius r = 1.5


def joined(split, M=1024):
    main = {(r["k"], round(r["s"][0], 3), round(r["s"][1], 3)): r for r in RS.load("main", split)}
    out = []
    f = ROOT / "results" / f"route_ens{M}_{split}" / "results.jsonl"
    fh = gzip.open(f.with_suffix(".jsonl.gz"), "rt", encoding="utf-8") if f.with_suffix(".jsonl.gz").exists() else open(f, encoding="utf-8")
    for e in map(json.loads, fh):
        r = main.get((e["k"], round(e["s"][0], 3), round(e["s"][1], 3)))
        if r is None:
            continue                                     # skipped in the main run (both sides impassable)
        assert abs(r["dJ_map_L1"] - e["dJ_map_L1"]) < 1e-6
        out.append((r, np.array(e["ens"]) - r["dJ_map_L1"] + r["dJ_map_L2"]))
    return out


def score(rows, choose, P):
    J = [r["JT"] for r, _ in rows]
    best = [min(j.values()) for j in J]
    a = [choose(r, e) for r, e in rows]
    loss = np.array([j[x] - b for j, x, b in zip(J, a, best)])
    amap = [RS.side(r["dJ_map_L2"]) for r, _ in rows]
    atrue = [RS.side(r["dJ_true"]) for r, _ in rows]
    sw = [i for i in range(len(rows)) if a[i] != amap[i]]
    right = [i for i in sw if a[i] == atrue[i]]
    lmap = np.array([j[x] - b for j, x, b in zip(J, amap, best)])
    days = [r["date"] for r, _ in rows]
    return dict(loss=float(loss.mean()), wrong=float(np.mean([x != t for x, t in zip(a, atrue)])),
                switches=len(sw), right=len(right),
                diff_vs_map=float((loss - lmap).mean()), ci_vs_map=RS.boot(loss - lmap, days)), loss


def main():
    P = json.load(open(ROOT / "results" / "route_summary_main.json", encoding="utf-8"))["params"]
    res = {"radius": P["r"], "quantile": Q}
    for split in ("dev", "test"):
        f = ROOT / "results" / f"route_ens1024_{split}" / "done"
        if not f.exists():
            continue
        rows = joined(split)
        days = [r["date"] for r, _ in rows]
        rob = lambda r, e: min("LR", key=lambda a: RS.worst_regret(r, a, P["r"]))
        out = {"n_missions": len(rows)}
        out["map"], lmap = score(rows, lambda r, e: RS.side(r["dJ_map_L2"]), P)
        out["worst_regret"], lrob = score(rows, rob, P)
        out["worst_regret"]["route_solves"] = float(np.mean([r["cx_solves_1.0"] + r["cx_solves_2.0"] for r, _ in rows]))
        out["expected_main32"], _ = score(rows, lambda r, e: RS.side(RS.ens_l2(r).mean()), P)
        for n in NS:
            s, l = score(rows, lambda r, e: RS.side(e[:n].mean()), P)
            s["route_solves"] = 2 * n
            s["diff_vs_worst_regret"] = float((l - lrob).mean())
            s["ci_vs_worst_regret"] = RS.boot(l - lrob, days)
            out[f"expected_{n}"] = s
            s, l = score(rows, lambda r, e: RS.side(np.quantile(e[:n], Q) + np.quantile(e[:n], 1 - Q)), P)
            s["route_solves"] = 2 * n
            s["diff_vs_worst_regret"] = float((l - lrob).mean())
            s["ci_vs_worst_regret"] = RS.boot(l - lrob, days)
            out[f"midpoint_{n}"] = s
        # how well does each rule's correction of the map margin predict the real correction?
        d = np.array([r["dJ_map_L2"] for r, _ in rows])
        t = np.array([r["dJ_true"] for r, _ in rows])
        mid = np.array([sum(RS.devs(r, P["r"])) / 2 for r, _ in rows])
        corr = {"worst_regret_midpoint": float(np.corrcoef(t - d, mid)[0, 1])}
        for n in (32, 1024):
            corr[f"mean_{n}"] = float(np.corrcoef(t - d, np.array([e[:n].mean() for _, e in rows]) - d)[0, 1])
            corr[f"midpoint_{n}"] = float(np.corrcoef(t - d, np.array(
                [(np.quantile(e[:n], Q) + np.quantile(e[:n], 1 - Q)) / 2 for _, e in rows]) - d)[0, 1])
        corr["main_mean_32"] = float(np.corrcoef(t - d, np.array([RS.ens_l2(r).mean() for r, _ in rows]) - d)[0, 1])
        out["corr_with_real_correction"] = corr
        # slope of the real correction on the predicted one (1 = the predicted shift has the right size)
        m1024 = np.array([e.mean() for _, e in rows]) - d
        out["slope_real_on_predicted"] = {"worst_regret_midpoint": float(np.polyfit(mid, t - d, 1)[0]),
                                          "mean_1024": float(np.polyfit(m1024, t - d, 1)[0])}
        # ranking missions by risk: share of the map's total loss held by the top 20% of missions, for the
        # worst regret of the search and for scores computed from n random plausible fields
        loss = np.array([r["JT"][RS.side(r["dJ_map_L2"])] - min(r["JT"].values()) for r, _ in rows])

        def top20(score):
            o = np.argsort(-np.asarray(score, float), kind="stable")
            c = np.cumsum(loss[o])
            return float(c[int(round(0.2 * len(o))) - 1] / c[-1])

        sgn = np.array([1.0 if RS.side(r["dJ_map_L2"]) == "L" else -1.0 for r, _ in rows])
        rank = {"worst_regret": top20([RS.worst_regret(r, RS.side(r["dJ_map_L2"]), P["r"]) for r, _ in rows]),
                "map_margin": top20(-np.abs(d)),
                "flip_share_main32": top20([np.mean(np.sign(RS.ens_l2(r)) != np.sign(r["dJ_map_L2"])) for r, _ in rows])}
        for n in NS:
            rank[f"flip_share_{n}"] = top20([np.mean(np.sign(e[:n]) != np.sign(r["dJ_map_L2"])) for r, e in rows])
            rank[f"expected_regret_{n}"] = top20([np.mean(np.maximum(0.0, s * e[:n])) for s, (r, e) in zip(sgn, rows)])
        out["top20_loss_share"] = rank
        # sampling noise of a 32-field mean against the size of the correction it estimates
        sd = np.array([e.std() for _, e in rows])
        out["noise_of_mean32_h"] = float(np.median(sd / np.sqrt(32)))
        out["size_of_correction_h"] = float(np.median(np.abs(np.array([e.mean() for _, e in rows]) - d)))
        out["skew_median"] = float(np.median([((e - e.mean()) ** 3).mean() / e.std() ** 3 for _, e in rows]))
        res[split] = out
    dst = ROOT / "results" / "route_ensemble_size.json"
    json.dump(res, open(dst, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for split in ("dev", "test"):
        if split not in res:
            continue
        o = res[split]
        print(f"== {split}: {o['n_missions']} missions")
        for k in ["map", "worst_regret", "expected_main32"] + [f"{p}_{n}" for p in ("expected", "midpoint") for n in NS]:
            s = o[k]
            extra = f"  vs worst regret {s['diff_vs_worst_regret']:+.2f} {np.round(s['ci_vs_worst_regret'], 2)}" if "diff_vs_worst_regret" in s else ""
            print(f"{k:16s} loss {s['loss']:.2f}  wrong {s['wrong']:.3f}  switch {s['switches']:3d} right {s['right']:3d}"
                  f"  vs map {s['diff_vs_map']:+.2f} {np.round(s['ci_vs_map'], 2)}{extra}")
        print("correlation with the real correction", {k: round(v, 3) for k, v in o["corr_with_real_correction"].items()})
        print("slope of the real correction on the predicted one", {k: round(v, 2) for k, v in o["slope_real_on_predicted"].items()})
        print("share of the map's loss in the top 20% by each score", {k: round(v, 3) for k, v in o["top20_loss_share"].items()})
        print("noise of a 32-field mean (median, h)", round(o["noise_of_mean32_h"], 2), "| size of the mean correction", round(o["size_of_correction_h"], 2), "| skew", round(o["skew_median"], 2))


if __name__ == "__main__":
    main()
