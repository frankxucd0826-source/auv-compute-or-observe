"""Summarise results/<exp>/results.jsonl: mean regret (log10 chlorophyll between the true
densest water and the reported water), share of missions that found the core (within 0.1
log10), action shares, with a paired comparison against a reference controller.

    python experiments/summarize.py pilot0_2018 [--ref fixed-0] [--by lag]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load(exp):
    rows = [json.loads(l) for l in open(ROOT / "results" / exp / "results.jsonl", encoding="utf-8")]
    df = pd.DataFrame(rows)
    acts = np.array(df["actions"].tolist(), dtype=float)
    acts = acts / acts.sum(1, keepdims=True)
    for k, n in enumerate(["go", "go_think", "drift", "drift_think"]):
        df["f_" + n] = acts[:, k]
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exp")
    ap.add_argument("--ref", default="fixed-0")
    ap.add_argument("--by", nargs="*", default=["lag"])
    a = ap.parse_args()
    df = load(a.exp)
    keys = a.by + ["controller"]
    g = df.groupby(keys).agg(n=("regret", "size"), avg=("regret_avg", "mean"), regret=("regret", "mean"), found=("found", "mean"),
                             hours=("time_h", "mean"), wh=("energy_wh", "mean"),
                             go=("f_go", "mean"), think=("f_go_think", "mean"),
                             drift=("f_drift", "mean"), drift_think=("f_drift_think", "mean"))
    # paired difference to the reference controller (same mission, same lag)
    ref = df[df.controller == a.ref].set_index(a.by + ["mission"])["regret_avg"]
    diffs = []
    for k, sub in df.groupby(keys):
        s = sub.set_index(a.by + ["mission"])["regret_avg"]
        d = (s - ref.reindex(s.index)).dropna()
        se = d.std(ddof=1) / np.sqrt(len(d)) if len(d) > 1 else np.nan
        diffs.append((k, d.mean(), se, (d < -1e-9).mean(), (d > 1e-9).mean()))
    dd = pd.DataFrame([dict(zip(keys, k if isinstance(k, tuple) else (k,)), d_vs_ref=m, se=s, better=b, worse=w)
                       for k, m, s, b, w in diffs]).set_index(keys)
    out = g.join(dd)
    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", 30)
    print(out.round(3).to_string())


if __name__ == "__main__":
    main()
