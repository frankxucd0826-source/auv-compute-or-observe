"""Paired comparison of controllers across experiments, with confidence intervals from a
bootstrap over bloom weeks (missions in the same calendar week of the same year share a bloom
and are not independent).

    python experiments/compare.py main_v1_strongcpu main_v1_weakcpu --ref fixed-0
"""
import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load(exp):
    df = pd.DataFrame([json.loads(l) for l in open(ROOT / "results" / exp / "results.jsonl", encoding="utf-8")])
    df["exp"] = exp
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exps", nargs="+")
    ap.add_argument("--ref", default="fixed-0")
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
    week = {int(r["id"]): np.datetime64(r["date"]).astype("datetime64[W]").astype(int) for r in rows}
    out = []
    rng = np.random.default_rng(0)
    for exp in a.exps:
        df = load(exp)
        piv = df.pivot_table(index=["mission", "lag"], columns="controller", values="regret")
        found = df.pivot_table(index=["mission", "lag"], columns="controller", values="found")
        weeks = np.array([week[m] for m, _ in piv.index])
        uw = np.unique(weeks)
        groups = [np.where(weeks == w)[0] for w in uw]
        for c in piv.columns:
            d = (piv[c] - piv[a.ref]).to_numpy()
            ok = np.isfinite(d)
            bs = []
            for _ in range(a.boot):
                pick = np.concatenate([groups[k] for k in rng.integers(len(groups), size=len(groups))])
                pick = pick[ok[pick]]
                bs.append(d[pick].mean())
            lo, hi = np.percentile(bs, [2.5, 97.5])
            out.append(dict(exp=exp, controller=c, n=int(ok.sum()), regret=piv[c].mean(),
                            found=found[c].mean(), diff=np.nanmean(d), lo=lo, hi=hi,
                            better=float((d[ok] < -1e-9).mean()), worse=float((d[ok] > 1e-9).mean())))
    t = pd.DataFrame(out)
    pd.set_option("display.width", 200)
    print(t.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
