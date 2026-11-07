"""Two checks on the slow and moderate computers (test years):
1. Rerun of rehearsal on the slow computer with its choices recorded: are the regrets identical to
   the first run (same seeds), and which strategies does it pick?
2. One-step metareasoning that judges more planning and more looking on the held-out imagined
   oceans ("double") against the usual one that judges them on the searched ones ("rational"):
   regret, how it spends its intervals, paired difference with a 95% interval (bootstrap over
   bloom weeks).
    python -E -X utf8 experiments/ablation_extra.py v3
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIXED = ["fixed-0", "fixed-1", "periodic-100", "periodic-300", "periodic-200"]


def load(exp):
    p = ROOT / "results" / exp / "results.jsonl"
    return pd.DataFrame([json.loads(l) for l in open(p, encoding="utf-8")]) if p.exists() else None


def shares(df, ctl):
    A = np.array(df[df.controller == ctl].actions.tolist(), dtype=float)
    s = A.sum(0) / A.sum()
    return dict(go=round(s[0], 3), go_think=round(s[1], 3), drift=round(s[2], 3), drift_think=round(s[3], 3),
                think=round(s[1] + s[3], 3), stopped=round(s[2] + s[3], 3))


def main(tag):
    rows = list(csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
    week = {int(r["id"]): str(np.datetime64(r["date"]).astype("datetime64[W]")) for r in rows}
    rng = np.random.default_rng(2)
    base = load(f"main_{tag}_test_weak")
    re_ = load(f"main_{tag}_test_weak_choice")
    if base is not None and re_ is not None:
        print("== slow computer, rehearsal rerun")
        for k in ("rehearsal", "rehearsal-self"):
            a = base[base.controller == k].set_index("mission").regret_avg
            b = re_[re_.controller == k].set_index("mission").regret_avg
            j = a.index.intersection(b.index)
            print(f"  {k}: {len(j)} missions, max |difference| to the first run = {np.abs(a[j] - b[j]).max():.2e}")
            print(f"  {k} picks:", re_[re_.controller == k].choice.value_counts(normalize=True).round(3).to_dict())
        a = re_[re_.controller == "rehearsal"].set_index("mission").choice
        b = re_[re_.controller == "rehearsal-self"].set_index("mission").choice
        print("  held-out and searched rehearsal pick the same strategy on", round((a == b.reindex(a.index)).mean(), 3), "of missions")
        p = base.pivot_table(index="mission", columns="controller", values="regret_avg")
        print("  random pick among the five:", round(p[FIXED].mean(axis=1).mean(), 4), " among the three moving:",
              round(p[FIXED[:3]].mean(axis=1).mean(), 4), " best per mission in hindsight:", round(p[FIXED].min(axis=1).mean(), 4),
              " rehearsal:", round(p["rehearsal"].mean(), 4))
    for c in ("weak", "moderate"):
        te, db = load(f"main_{tag}_test_{c}"), load(f"main_{tag}_test_{c}_double")
        if te is None or db is None or "double" not in set(db.controller):
            continue
        print(f"== {c} computer: one-step metareasoning judged on held-out oceans ('double') vs searched ('rational')")
        both = pd.concat([te[te.controller.isin(["rational", "rehearsal"] + FIXED)], db])
        p = both.pivot_table(index="mission", columns="controller", values="regret_avg").dropna()
        print("  n =", len(p), " mean regret:", p[["rational", "double", "rehearsal"]].mean().round(4).to_dict())
        print("  rational intervals:", shares(te, "rational"))
        print("  double intervals:  ", shares(db, "double"))
        weeks = np.array([week[m] for m in p.index])
        groups = [np.where(weeks == w)[0] for w in np.unique(weeks)]
        for a, b in (("double", "rational"), ("double", "rehearsal")):
            d = (p[a] - p[b]).to_numpy()
            bs = [d[np.concatenate([groups[k] for k in rng.integers(len(groups), size=len(groups))])].mean() for _ in range(2000)]
            print(f"  {a} minus {b}: {d.mean():+.4f} [{np.percentile(bs, 2.5):+.4f}, {np.percentile(bs, 97.5):+.4f}]")
        print("  computing time per mission (s):", both.groupby("controller").wall_s.mean().round(1).reindex(["rational", "double"]).to_dict())


if __name__ == "__main__":
    main(sys.argv[1])
