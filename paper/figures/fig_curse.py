"""Figure 3: thinking longer makes the planner believe more, not achieve more; imagined oceans kept
out of the search tell the truth.
(a) value of the chosen route against the planning budget: the planner's own score during the search,
    the same route on the 16 held-out imagined oceans, and in the real ocean;
(b) estimate minus reality: the search score, and the held-out score with the map uncertainty as
    calibrated, halved and enlarged 1.5 times.
Data: results/curse3_dev/results.jsonl (80 development windows x 3 seeds, map 3 days old, the first
8 hours planned from the start point). Values in log10 chlorophyll.
"""
import json

import numpy as np
import pandas as pd
import style as S
from style import plt

S.setup()
df = pd.DataFrame([json.loads(l) for l in open(S.ROOT / "results" / "curse3_dev" / "results.jsonl", encoding="utf-8")])
b = np.array(sorted(df.budget.unique()), dtype=float)
cal = df[df.scale == 1.0]

fig, ax = plt.subplots(1, 2, figsize=(S.TEXTW, 64 * S.MM), gridspec_kw=dict(width_ratios=[1.05, 1]))
fig.subplots_adjust(left=0.085, right=0.975, top=0.96, bottom=0.27, wspace=0.30)
A = ax[0]
ends = {}
for key, col, ls, lab in (("believed", S.SEARCH, "-", "规划器对自身航线的估值"),
                          ("true", S.REAL, "-", "真实海洋中的价值"),
                          ("believed_holdout", S.HELD, (0, (3.2, 1.6)), "检验用模拟海洋上的评估")):
    g = cal.groupby("budget")[key]
    m, se = g.mean().reindex(b).values, g.sem().reindex(b).values
    A.fill_between(b, m - 1.96 * se, m + 1.96 * se, color=col, alpha=0.10, lw=0)
    A.plot(b, m, color=col, ls=ls, lw=2.3, marker="o", ms=3.8, zorder=3)
    ends[key] = m
A.set_xscale("log")
A.set_xlim(45, 3.6e5)
A.set_ylim(0.70, 0.95)
A.set_xticks([1e2, 1e3, 1e4, 1e5], ["100", "1000", "1万", "10万"])
A.set_xlabel("每次决策的模拟推演次数")
A.set_ylabel("所选航线的价值（对数浓度）")
x_end = b[-1]
A.annotate("", xy=(x_end * 1.32, ends["believed"][-1]), xytext=(x_end * 1.32, ends["true"][-1]),
           arrowprops=dict(arrowstyle="<->", color=S.SEARCH, lw=1.1, shrinkA=0, shrinkB=0))
A.text(x_end * 1.18, (ends["believed"][-1] + ends["true"][-1]) / 2, f"虚高\n{ends['believed'][-1] - ends['true'][-1]:.3f}",
       color=S.SEARCH, fontsize=8, ha="right", va="center", fontweight="bold")
A.text(1.6e3, 0.872, "规划器对自身航线的估值", color=S.SEARCH, fontsize=8.2, ha="right", va="bottom", fontweight="bold")
A.text(2.2e5, 0.788, "真实价值", color=S.INK, fontsize=8.2, ha="right", va="top", fontweight="bold")
A.text(80, 0.728, "检验用模拟海洋上的评估", color=S.HELD, fontsize=8.2, ha="left", va="top", fontweight="bold")
S.caption(A, "(a) 推演越多，估值越高，真实价值却不再提高", y=-0.30)

B = ax[1]
gg = df.assign(search_gap=df.believed - df["true"], held_gap=df.believed_holdout - df["true"])
B.axhline(0, color=S.INK, lw=0.9)
lines = [(1.0, "search_gap", S.SEARCH, "-", 2.3, "规划器估值"),
         (1.5, "held_gap", "#9775FA", (0, (1, 1.4)), 1.8, "检验样本评估，不确定性 ×1.5"),
         (1.0, "held_gap", S.HELD, (0, (3.2, 1.6)), 2.3, "检验样本评估，不确定性按数据标定"),
         (0.5, "held_gap", "#9775FA", (0, (1, 1.4)), 1.8, "检验样本评估，不确定性 ×0.5")]
for sc, key, col, ls, lw, lab in lines:
    m = gg[gg.scale == sc].groupby("budget")[key].mean().reindex(b).values
    B.plot(b, m, color=col, ls=ls, lw=lw, marker="o", ms=3.2 if lw < 2 else 3.8, zorder=3)
    y_lab = {"规划器估值": m[-1] + 0.012, "检验样本评估，不确定性按数据标定": -0.016}.get(lab, m[0] + (0.022 if sc > 1 else -0.020))
    x_lab = b[-1] if lab == "规划器估值" else b[0]
    B.text(x_lab, y_lab, lab, color=col if col != "#9775FA" else "#7048E8", fontsize=7.9,
           ha="right" if lab == "规划器估值" else "left", va="center", fontweight="bold" if lw > 2 else "normal")
B.set_xscale("log")
B.set_xlim(45, 3.6e5)
B.set_ylim(-0.095, 0.135)
B.set_xticks([1e2, 1e3, 1e4, 1e5], ["100", "1000", "1万", "10万"])
B.set_xlabel("每次决策的模拟推演次数")
B.set_ylabel("估计 − 真实（对数浓度）")
S.caption(B, "(b) 检验样本上的评估无偏", y=-0.30)
S.save(fig, "fig_curse")
print(cal.groupby("budget")[["believed", "believed_holdout", "true"]].mean().round(3).to_string())
