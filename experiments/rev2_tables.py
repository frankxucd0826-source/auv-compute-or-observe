"""Table 2 of the paper (main results) from results/rev2_summary.json: time-averaged regret of every
controller on the 148 test missions, four vehicles, two models of the true ocean. Bold: lowest in the
column among controllers that can be run (the per-mission best in hindsight is a reference only).

    python -E -X utf8 experiments/rev2_tables.py   -> paper/tables/main_table.tex
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "paper"))
from terms import CONTROLLER, STRATEGY, VEHICLE  # noqa: E402

R = json.load(open(ROOT / "results" / "rev2_summary.json", encoding="utf-8"))["main"]
V = ["weak", "moderate", "strong", "efficient"]
TRUTHS = ["sat+", "sat"]
GROUPS = [("固定策略", ["fixed-0", "fixed-1", "periodic-100", "periodic-300", "periodic-200"]),
          ("需要历史任务", ["tuned", "learned"]),
          ("在线元推理", ["rational", "double"]),
          ("巡测规则", ["lawnmower", "greedy", "ucb", "thompson"]),
          ("本文", ["rehearsal"]),
          ("参考", ["oracle"])]


def val(t, v, k):
    m = R.get(t, {}).get(v, {}).get("means", {})
    return m.get(k)


best = {}
for t in TRUTHS:
    for v in V:
        cands = [val(t, v, k) for _, ks in GROUPS[:-1] for k in ks if val(t, v, k) is not None]
        best[(t, v)] = min(cands) if cands else None
lines = [r"\begin{tabular}{@{}ll" + "c" * 8 + r"@{}}", r"\toprule",
         r" & & \multicolumn{4}{c}{真值：当天卫星图 + 小尺度变化} & \multicolumn{4}{c}{真值：当天卫星图} \\",
         r"\cmidrule(lr){3-6}\cmidrule(l){7-10}",
         r"类别 & 控制方式 & " + " & ".join(VEHICLE[v] for v in V) * 1 + " & " + " & ".join(VEHICLE[v] for v in V) + r" \\",
         r"\midrule"]
for g, keys in GROUPS:
    for j, k in enumerate(keys):
        name = CONTROLLER[k].replace("（本文）", "").replace("（参考）", "")
        if k == "tuned":
            tuned = [STRATEGY.get(R.get(t, {}).get(v, {}).get("tuned", ""), "") for t in TRUTHS for v in V]
            name = r"调好的固定策略$^{a}$"
        cells = []
        for t in TRUTHS:
            for v in V:
                x = val(t, v, k)
                if x is None:
                    cells.append("--")
                elif best[(t, v)] is not None and abs(x - best[(t, v)]) < 5e-4 and k != "oracle":
                    cells.append(r"\textbf{" + f"{x:.3f}" + "}")
                else:
                    cells.append(f"{x:.3f}")
        row = (g if j == 0 else "") + " & " + name + " & " + " & ".join(cells) + r" \\"
        if k == "rehearsal":
            row = r"\rowcolor{violet!8}" + row
        lines.append(row)
    lines.append(r"\midrule" if g != GROUPS[-1][0] else r"\bottomrule")
lines.append(r"\end{tabular}")
note = "调好的固定策略在两种真值下依次为：" + "；".join(
    f"{VEHICLE[v]}{STRATEGY[R[t][v]['tuned']]}" + ("" if t == "sat+" else "")
    for t in TRUTHS for v in V if v in R.get(t, {}))
out = ROOT / "paper" / "tables" / "main_table.tex"
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
(ROOT / "paper" / "tables" / "main_table_note.txt").write_text(note, encoding="utf-8")
print(out, "\n", note)
