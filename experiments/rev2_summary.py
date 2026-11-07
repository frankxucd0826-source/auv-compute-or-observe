"""Numbers of the second round (11-05), for the paper's tables and figures.

Main comparison on the 148 test missions under two models of the true ocean:
  "sat"   the satellite map of the mission day itself (all real data)
  "sat+"  the same map plus the small-scale variability a satellite misses (0.15, main setting)
for the four vehicles; every controller is compared with rehearsal by paired differences with 95%
intervals from a bootstrap over bloom weeks. Also: a strategy selector learned from the development
missions (features of the stale map known before launch), random picks, the per-mission best in
hindsight, ablations of rehearsal, map age, choice shares and what one-step metareasoning does.

    python -E -X utf8 experiments/rev2_summary.py      -> results/rev2_summary.json
"""
import csv
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

os.environ.setdefault("OMP_NUM_THREADS", "1")
ROOT = Path(__file__).resolve().parents[1]
VEH = ["weak", "moderate", "strong", "efficient"]
FIXED = ["fixed-0", "fixed-1", "periodic-100", "periodic-300", "periodic-200"]
MOVE = ["fixed-0", "fixed-1", "periodic-100"]
RULES = ["lawnmower", "greedy", "ucb", "thompson"]
rows_csv = list(csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
WEEK = {int(r["id"]): str(np.datetime64(r["date"]).astype("datetime64[W]")) for r in rows_csv}
START = {int(r["id"]): (float(r["start_x"]), float(r["start_y"])) for r in rows_csv}


def load(exp):
    p = ROOT / "results" / exp / "results.jsonl"
    if not p.exists() or (exp.startswith("r2_") and not (ROOT / "results" / exp / "done").exists()):
        return None
    return pd.DataFrame([json.loads(l) for l in open(p, encoding="utf-8")])


def cat(*dfs):
    dfs = [d for d in dfs if d is not None]
    return pd.concat(dfs, ignore_index=True) if dfs else None


def paired(piv, a, b, rng, n=2000):
    """Mean of a - b over missions with a 95% interval from a bootstrap over bloom weeks."""
    if a not in piv or b not in piv:
        return None
    d = (piv[a] - piv[b]).to_numpy()
    ok = np.isfinite(d)
    d, idx = d[ok], piv.index[ok]
    weeks = np.array([WEEK[m] for m in idx])
    groups = [np.where(weeks == w)[0] for w in np.unique(weeks)]
    bs = [d[np.concatenate([groups[k] for k in rng.integers(len(groups), size=len(groups))])].mean() for _ in range(n)]
    return dict(mean=float(d.mean()), lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)), n=int(len(d)))


# ---------- a strategy selector learned from past missions ----------
M = np.load(ROOT / "data" / "missions" / "chl_missions.npz")
LI = {int(l): k for k, l in enumerate(M["lags"])}


def features(i, lag=3):
    prior, mask = M["prior"][i, LI[lag]], M["mask"][i]
    v = prior[mask]
    iy, ix = np.unravel_index(np.argmax(np.where(mask, prior, -9)), prior.shape)
    sx, sy = START[i]
    return [v.max(), np.median(v), v.max() - np.median(v), v.std(), np.hypot(ix - sx, iy - sy) * 2.0,
            mask.mean(), prior[int(sy + 0.5), int(sx + 0.5)], float((v > v.max() - 0.1).mean())]


def learned_pick(dev_piv, test_index, lag=3):
    from sklearn.ensemble import GradientBoostingRegressor
    Xd = np.array([features(i, lag) for i in dev_piv.index])
    Xt = np.array([features(i, lag) for i in test_index])
    pred = {}
    for s in FIXED:
        m = GradientBoostingRegressor(n_estimators=150, max_depth=2, learning_rate=0.05, subsample=0.8, random_state=0)
        m.fit(Xd, dev_piv[s].to_numpy())
        pred[s] = m.predict(Xt)
    P = pd.DataFrame(pred, index=test_index)
    return P.idxmin(axis=1)


def frames(truth, v):
    if truth == "sat+":
        dbl = load(f"main_v3_test_{v}_double") if v in ("weak", "moderate") else load(f"r2_dbl_test_{v}")
        te = cat(load(f"main_v3_test_{v}"), dbl, load("r2_rules_se0.15_test"))
        dev = load(f"main_v3_dev_{v}")
        if v == "weak":     # the slow-computer rerun recorded rehearsal's choices (regrets identical)
            ch = load("main_v3_test_weak_choice")
    else:
        te = cat(load(f"r2_se0_test_{v}"), load("r2_rules_se0_test"))
        dev = load(f"r2_se0_dev_{v}")
    if te is None or dev is None or not set(FIXED) <= set(dev.controller):
        return None
    piv = te.pivot_table(index="mission", columns="controller", values="regret_avg")
    dpiv = dev.pivot_table(index="mission", columns="controller", values="regret_avg")
    tuned = dpiv[FIXED].mean().idxmin()
    piv["tuned"] = piv[tuned]
    piv["random5"] = piv[FIXED].mean(axis=1)
    piv["random3"] = piv[MOVE].mean(axis=1)
    piv["oracle"] = piv[FIXED].min(axis=1)
    pick = learned_pick(dpiv, piv.index)
    piv["learned"] = [piv.loc[m, s] for m, s in pick.items()]
    out = dict(piv=piv, tuned=tuned, te=te, dev_means=dpiv[FIXED].mean().round(4).to_dict(),
               learned_shares=pick.value_counts(normalize=True).round(3).to_dict())
    if truth == "sat+" and v == "weak":
        out["choice_df"] = ch
    return out


def shares(df, key):
    s = df[df.controller == key]
    if not len(s):
        return None
    A = np.array(s.actions.tolist(), dtype=float)
    tot = A.sum()
    return dict(think=float((A[:, 1].sum() + A[:, 3].sum()) / tot), stopped=float((A[:, 2].sum() + A[:, 3].sum()) / tot))


def main():
    rng = np.random.default_rng(1)
    R = {"main": {}, "ablation": {}, "lag1": {}}
    for truth in ("sat+", "sat"):
        R["main"][truth] = {}
        for v in VEH:
            F = frames(truth, v)
            if F is None:
                continue
            piv, te = F["piv"], F["te"]
            means = piv.mean().round(4).to_dict()
            comps = {}
            for b in ["tuned", "rational", "double", "rehearsal-self", "learned", "random5", "random3", "oracle"] + RULES + FIXED:
                r = paired(piv, "rehearsal", b, rng)
                if r:
                    comps[b] = r
            vs_tuned = {b: paired(piv, b, "tuned", rng) for b in ["rational", "double", "learned"] + RULES if b in piv}
            chdf = F.get("choice_df", te)
            ch = chdf[chdf.controller == "rehearsal"]
            choice = ch.choice.value_counts(normalize=True).round(3).to_dict() if "choice" in ch and ch.choice.notna().any() else None
            R["main"][truth][v] = dict(n=int(len(piv)), tuned=F["tuned"], dev_means=F["dev_means"], means=means,
                                       rehearsal_minus=comps, minus_tuned=vs_tuned, choice=choice,
                                       learned_shares=F["learned_shares"],
                                       meta_shares=shares(te, "rational"), double_shares=shares(te, "double"),
                                       rehearsal_shares=shares(te, "rehearsal"), tuned_shares=shares(te, F["tuned"]),
                                       sd=float(piv["rehearsal"].std()))
            print(f"\n=== {truth} {v}: n={len(piv)} tuned={F['tuned']}")
            print("  means:", {k: round(x, 3) for k, x in means.items()})
            for b, r in comps.items():
                print(f"  rehearsal - {b:15s} {r['mean']:+.3f} [{r['lo']:+.3f}, {r['hi']:+.3f}]")
            print("  choice:", choice, " learned picks:", F["learned_shares"])
            print("  meta:", shares(te, "rational"), " double:", shares(te, "double"))
    # ablations of rehearsal (main truth model), slow and moderate computers
    for v in ("weak", "moderate"):
        base = load(f"main_v3_test_{v}")
        if base is None:
            continue
        bp = base.pivot_table(index="mission", columns="controller", values="regret_avg")
        A = {}
        k = load(f"r2_k_test_{v}")
        if k is not None:
            kp = k.pivot_table(index="mission", columns="controller", values="regret_avg")
            for c in kp.columns:
                j = bp[["rehearsal"]].join(kp[[c]], how="inner")
                A[c] = dict(mean=float(j[c].mean()), diff=paired(j, c, "rehearsal", rng))
        A["rehearsal-self"] = dict(mean=float(bp["rehearsal-self"].mean()), diff=paired(bp, "rehearsal-self", "rehearsal", rng))
        F = frames("sat+", v)
        if F is not None:
            for c in ("double", "random5", "random3", "tuned", "learned"):
                if c in F["piv"]:
                    A[c] = dict(mean=float(F["piv"][c].mean()), diff=paired(F["piv"], c, "rehearsal", rng))
        for s in ("0.5", "2"):
            d = load(f"r2_sd{s}_test_{v}")
            if d is None:
                continue
            dp = d.pivot_table(index="mission", columns="controller", values="regret_avg")
            if "rehearsal" not in dp:
                continue
            j = bp[["rehearsal"]].join(dp.add_suffix(f"@{s}"), how="inner")
            A[f"sd{s}"] = dict(mean=float(dp["rehearsal"].mean()), diff=paired(j, f"rehearsal@{s}", "rehearsal", rng),
                               fixed=dp[[c for c in FIXED if c in dp]].mean().round(4).to_dict(),
                               choice=d[d.controller == "rehearsal"].choice.value_counts(normalize=True).round(3).to_dict()
                               if "choice" in d else None)
        R["ablation"][v] = A
        print(f"\n=== ablation {v}")
        for c, r in A.items():
            dd = r["diff"]
            print(f"  {c:16s} mean {r['mean']:.3f}  minus main rehearsal {dd['mean']:+.3f} [{dd['lo']:+.3f}, {dd['hi']:+.3f}]" if dd else c)
    # map one day old
    for v in ("weak", "moderate"):
        te, dev = load(f"r2_lag1_test_{v}"), load(f"r2_lag1_dev_{v}")
        if te is None or dev is None or not set(FIXED) <= set(dev.controller):
            continue
        piv = te.pivot_table(index="mission", columns="controller", values="regret_avg")
        dp = dev.pivot_table(index="mission", columns="controller", values="regret_avg")
        tuned = dp[FIXED].mean().idxmin()
        piv["tuned"] = piv[tuned]
        R["lag1"][v] = dict(tuned=tuned, means=piv.mean().round(4).to_dict(),
                            vs_tuned=paired(piv, "rehearsal", "tuned", rng), vs_meta=paired(piv, "rehearsal", "rational", rng),
                            choice=te[te.controller == "rehearsal"].choice.value_counts(normalize=True).round(3).to_dict())
        print(f"\n=== lag 1 {v}: tuned {tuned}", {k: round(x, 3) for k, x in piv.mean().items()})
        print("  rehearsal - tuned", R["lag1"][v]["vs_tuned"], " - meta", R["lag1"][v]["vs_meta"])
    json.dump(R, open(ROOT / "results" / "rev2_summary.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("\nwritten results/rev2_summary.json")


if __name__ == "__main__":
    main()
