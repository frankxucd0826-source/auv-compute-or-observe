"""Write the one-change diagnostic numbers (results/rev2_diag_summary.json) into the mechanism
paragraph of paper/sections/experiments.tex, replacing the sentences with \\TBD placeholders.
    python -E -X utf8 experiments/fill_diag_text.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = json.load(open(ROOT / "results" / "rev2_diag_summary.json", encoding="utf-8"))
w, m = D["weak"], D["moderate"]


def pc(x):
    return f"{x * 100:.0f}\\%"


def d(r):
    return f"${r['mean']:+.3f}$（$[{r['lo']:+.3f}, {r['hi']:+.3f}]$）"


new = (
    "为分离两项改动的作用，我们在慢计算机与中等计算机上（相同148个任务与种子）分别只做其中一项改动（图\\ref{fig:mech}a、b中的空心标记）。"
    f"只改为留出估值时，深想时段占比即由{pc(w['rational']['think'])}与{pc(m['rational']['think'])}降至{pc(w['double-noguard']['think'])}与{pc(m['double-noguard']['think'])}，"
    f"但停下占比仍为{pc(w['double-noguard']['stopped'])}与{pc(m['double-noguard']['stopped'])}，遗憾为${w['double-noguard']['mean']:.3f}$与${m['double-noguard']['mean']:.3f}$"
    f"（相对经典方法分别为{d(w['double-noguard']['minus_rational'])}与{d(m['double-noguard']['minus_rational'])}）；"
    f"只加两倍标准误规则时，深想占比仍为{pc(w['rational-guard']['think'])}与{pc(m['rational-guard']['think'])}，停下占比降至{pc(w['rational-guard']['stopped'])}与{pc(m['rational-guard']['stopped'])}，"
    f"遗憾为${w['rational-guard']['mean']:.3f}$与${m['rational-guard']['mean']:.3f}$（{d(w['rational-guard']['minus_rational'])}与{d(m['rational-guard']['minus_rational'])}）；"
    f"两处同时改动才把停下占比降至{pc(w['double']['stopped'])}与{pc(m['double']['stopped'])}，遗憾降至${w['double']['mean']:.3f}$与${m['double']['mean']:.3f}$"
    f"（{d(w['double']['minus_rational'])}与{d(m['double']['minus_rational'])}），达到预演水平。"
    "可见过度深想源于在搜索用海洋上估计计算收益，过多停船源于对微小样本差值的反应，二者须同时纠正：单独任一改动在中等计算机上都未明显降低遗憾，"
    "在深想本身有益的慢计算机上也只有保守切换规则单独有效。"
)
p = ROOT / "paper" / "sections" / "experiments.tex"
t = p.read_text(encoding="utf-8")
a = t.index("为分离留出估值变体中两项改动各自的作用")
b = t.index("留出估值变体同时消除了这两项偏差。") + len("留出估值变体同时消除了这两项偏差。")
p.write_text(t[:a] + new + t[b:], encoding="utf-8")
print(new)
