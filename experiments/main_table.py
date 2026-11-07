"""Main comparison table: for each condition, test-year regret and core-found rate of every
controller, plus the fixed strategy that was best on the development years ("tuned fixed").
Differences to the tuned fixed strategy come with 95% intervals from a bootstrap over bloom
weeks.

    python experiments/main_table.py --tag v1
"""
import argparse
import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CONDS = ["weak", "moderate", "strong", "efficient"]
FIXED = ["fixed-0", "fixed-1", "periodic-100", "periodic-300", "periodic-200"]


def load(exp):
    p = ROOT / "results" / exp / "results.jsonl"
    return pd.DataFrame([json.loads(l) for l in open(p, encoding="utf-8")]) if p.exists() else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
    week = {int(r["id"]): str(np.datetime64(r["date"]).astype("datetime64[W]")) for r in rows}
    rng = np.random.default_rng(0)
    out = []
    for c in CONDS:
        dv, te = load(f"main_{a.tag}_dev_{c}"), load(f"main_{a.tag}_test_{c}")
        if te is None:
            continue
        tuned = dv.groupby("controller")["regret_avg"].mean().reindex(FIXED).idxmin() if dv is not None else "fixed-0"
        piv = te.pivot_table(index=["mission", "lag"], columns="controller", values="regret_avg")
        fin = te.pivot_table(index=["mission", "lag"], columns="controller", values="regret")
        fnd = te.pivot_table(index=["mission", "lag"], columns="controller", values="found")
        weeks = np.array([week[m] for m, _ in piv.index])
        groups = [np.where(weeks == w)[0] for w in np.unique(weeks)]
        for ctl in piv.columns:
            d = (piv[ctl] - piv[tuned]).to_numpy()
            bs = [np.nanmean(d[np.concatenate([groups[k] for k in rng.integers(len(groups), size=len(groups))])])
                  for _ in range(a.boot)]
            out.append(dict(condition=c, controller=ctl + (" (tuned fixed)" if ctl == tuned else ""),
                            n=int(piv[ctl].notna().sum()), regret_avg=piv[ctl].mean(), regret_end=fin[ctl].mean(),
                            found=fnd[ctl].mean(),
                            vs_tuned=np.nanmean(d), lo=np.percentile(bs, 2.5), hi=np.percentile(bs, 97.5)))
    t = pd.DataFrame(out)
    pd.set_option("display.width", 220)
    print(t.round(3).to_string(index=False))
    t.to_csv(ROOT / "results" / f"main_{a.tag}_table.csv", index=False)


if __name__ == "__main__":
    main()
