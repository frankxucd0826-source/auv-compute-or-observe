"""Numbers the paper quotes beside the main table, for every condition with test results:
which strategy rehearsal picked, what one-step metareasoning did with its intervals, rehearsal
minus metareasoning (paired, 95% interval from a bootstrap over bloom weeks), computing time per
mission on this PC, and the mission-to-mission spread of regret. Also writes the main table as
LaTeX (paper/tables/main_table.tex) from results/main_<tag>_table.csv.

    python -E -X utf8 experiments/main_extra.py v3
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "paper"))
from terms import CONTROLLER, TUNED, VEHICLE
CONDS = ["weak", "moderate", "strong", "efficient"]
FIXED = ["fixed-0", "fixed-1", "periodic-100", "periodic-300", "periodic-200"]
NAME = CONTROLLER
COLS = VEHICLE
SUB = {"weak": "5 次/分，+20 W", "moderate": "20 次/分，+20 W", "strong": "100 次/分，+20 W", "efficient": "20 次/分，+5 W"}


def load(exp):
    p = ROOT / "results" / exp / "results.jsonl"
    return pd.DataFrame([json.loads(l) for l in open(p, encoding="utf-8")]) if p.exists() else None


def boot(d, groups, rng, n=2000):
    return [np.nanmean(d[np.concatenate([groups[k] for k in rng.integers(len(groups), size=len(groups))])])
            for _ in range(n)]


def extras(tag):
    rows = list(csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
    week = {int(r["id"]): str(np.datetime64(r["date"]).astype("datetime64[W]")) for r in rows}
    rng = np.random.default_rng(1)
    for c in CONDS:
        te = load(f"main_{tag}_test_{c}")
        if te is None:
            continue
        print(f"\n===== {c} ({COLS[c]}): {te.mission.nunique()} missions")
        for k in ("rehearsal", "rehearsal-self"):
            s = te[te.controller == k]
            if len(s) and "choice" in s:
                print(f"  {k} choices:", s.choice.value_counts(normalize=True).round(3).to_dict())
        r = te[te.controller == "rational"]
        if len(r):
            A = np.array(r.actions.tolist(), dtype=float)
            print("  one-step metareasoning action shares [go, go+think, drift, drift+think]:",
                  (A.sum(0) / A.sum()).round(3).tolist(), " any think:", round((A[:, 1].sum() + A[:, 3].sum()) / A.sum(), 3),
                  " stopped:", round((A[:, 2].sum() + A[:, 3].sum()) / A.sum(), 3))
        piv = te.pivot_table(index="mission", columns="controller", values="regret_avg")
        weeks = np.array([week[m] for m in piv.index])
        groups = [np.where(weeks == w)[0] for w in np.unique(weeks)]
        for a, b in (("rehearsal", "rational"), ("rehearsal", "fixed-0"), ("rehearsal", "rehearsal-self")):
            if a in piv and b in piv:
                d = (piv[a] - piv[b]).to_numpy()
                bs = boot(d, groups, rng)
                print(f"  {a} minus {b}: {np.nanmean(d):+.4f}  [{np.percentile(bs, 2.5):+.4f}, {np.percentile(bs, 97.5):+.4f}]")
        print("  computing time per mission on this PC (s):", te.groupby("controller").wall_s.mean().round(1).to_dict())
        print("  spread of regret across missions (sd):", piv.std().round(3).to_dict())


def table(tag):
    f = ROOT / "results" / f"main_{tag}_table.csv"
    t = pd.read_csv(f)
    t["ctl"] = t.controller.str.replace(" (tuned fixed)", "", regex=False)
    t["tuned"] = t.controller.str.endswith("(tuned fixed)")
    order = FIXED + ["rational", "rehearsal", "rehearsal-self"]
    lines = [r"\resizebox{\linewidth}{!}{%", r"\begin{tabular}{l" + "c" * len(CONDS) + "}", r"\toprule",
             "控制方式 & " + " & ".join(COLS[c] for c in CONDS) + r" \\",
             " & " + " & ".join(r"{\footnotesize " + SUB[c] + "}" for c in CONDS) + r" \\", r"\midrule"]
    for k in order:
        cells, ci = [], []
        for c in CONDS:
            r = t[(t.condition == c) & (t.ctl == k)]
            if r.empty:
                cells.append(r"\TBD{待填}")
                ci.append("")
                continue
            r = r.iloc[0]
            if r.tuned:
                cells.append(f"{r.regret_avg:.3f}（{TUNED}）")
                ci.append("")
            else:
                cells.append(f"{r.regret_avg:.3f}（${r.vs_tuned:+.3f}$）")
                ci.append(r"{\footnotesize $[" + f"{r.lo:+.3f}, {r.hi:+.3f}" + r"]$}" if k in ("rational", "rehearsal", "rehearsal-self") else "")
        if k == "rational":
            lines.append(r"\midrule")
        lines.append(NAME[k] + " & " + " & ".join(cells) + r" \\")
        if any(ci):
            lines.append(" & " + " & ".join(ci) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}}"]
    out = ROOT / "paper" / "tables" / "main_table.tex"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\nwrote", out)


if __name__ == "__main__":
    extras(sys.argv[1])
    table(sys.argv[1])
