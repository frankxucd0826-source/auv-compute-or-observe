"""Figure 7: ablation of rehearsal, one design choice changed at a time (148 test missions, main
truth model, slow and moderate computers). Bars: change of time-averaged regret relative to the full
method (4 imagined truths drawn from held-out oceans, uncertainty calibrated from eight years of
data, whole-mission rehearsal); whiskers: 95% intervals from a bootstrap over bloom weeks; right of
zero = worse.
Data: results/rev2_summary.json
"""
import json

import numpy as np
import style as S
from style import plt

S.setup()
A = json.load(open(S.ROOT / "results" / "rev2_summary.json", encoding="utf-8"))["ablation"]
GROUPS = [("想象真值的个数（本文 4 个）", [("rehearsal-k1", "1 个"), ("rehearsal-k2", "2 个"), ("rehearsal-k8", "8 个")]),
          ("想象真值的来源（本文：留出海洋）", [("rehearsal-self", "改用搜索过的海洋")]),
          ("不确定性（本文：按八年数据标定）", [("sd0.5", "设为标定值的一半"), ("sd2", "设为标定值的两倍")]),
          ("决策方式（本文：整场预演）", [("double", "改为逐段判断（单步、留出估值）")]),
          ("不做预演", [("random3", "三种不停策略中随机选"), ("random5", "五种策略中随机选")]),
          ("参考：需要历史任务", [("tuned", "调好的固定策略"), ("learned", "按历史任务学习的选择器")])]
VEH = [("weak", "慢计算机", "#343A40"), ("moderate", "中等计算机", "#A5B4C4")]
rows, gy, y = [], [], 0.0
for g, items in GROUPS:
    gy.append((g, y))
    y += 0.8
    for key, lab in items:
        rows.append((key, lab, y))
        y += 1.0
    y += 0.3
fig, ax = plt.subplots(figsize=(S.TEXTW, 86 * S.MM))
fig.subplots_adjust(left=0.30, right=0.97, top=0.92, bottom=0.12)
ax.axvline(0, color=S.REHEARSAL, lw=1.6, zorder=1)
for key, lab, yy in rows:
    for j, (v, vn, c) in enumerate(VEH):
        r = A.get(v, {}).get(key)
        if not r or not r.get("diff"):
            continue
        d = r["diff"]
        off = -0.2 + 0.4 * j
        ax.barh(yy + off, d["mean"], height=0.36, color=c, zorder=2)
        ax.plot([d["lo"], d["hi"]], [yy + off, yy + off], color=S.INK, lw=0.9, zorder=3)
        sig = d["lo"] > 0 or d["hi"] < 0
        if sig:
            x = d["hi"] + 0.002 if d["mean"] > 0 else d["lo"] - 0.002
            ax.text(x, yy + off, "*", ha="left" if d["mean"] > 0 else "right", va="center", fontsize=9, color=S.INK)
ax.set_yticks([yy for _, _, yy in rows], [lab for _, lab, _ in rows], fontsize=7.9)
ax.tick_params(axis="y", length=0)
for g, yy in gy:
    ax.text(-0.015, yy + 0.05, g, transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=7.7,
            color=S.MUTED, fontweight="bold")
    ax.axhline(yy - 0.3, color="#DEE2E6", lw=0.6, zorder=0)
ax.set_ylim(y - 0.2, -0.4)
ax.set_xlim(-0.032, 0.072)
ax.set_xticks([-0.03, -0.015, 0, 0.015, 0.03, 0.045, 0.06], ["−0.03", "−0.015", "0", "0.015", "0.03", "0.045", "0.06"])
ax.grid(axis="y", visible=False)
ax.set_xlabel("与完整方法相比的时间平均遗憾变化（越靠右越差；* 表示 95% 置信区间不含 0）")
hh = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in VEH]
ax.legend(hh, [vn for _, vn, _ in VEH], loc="lower right", fontsize=7.8, ncol=1, borderaxespad=0.3)
S.save(fig, "fig_ablation")
