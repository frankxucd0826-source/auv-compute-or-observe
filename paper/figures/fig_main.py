"""Figure 4: every compared controller against rehearsal on the 148 test missions, for the four
vehicles and both models of the true ocean. Each mark is a controller's time-averaged regret minus
rehearsal's (paired by mission; bar = 95% interval from a bootstrap over bloom weeks); right of zero
= worse than rehearsal. Filled: the satellite map of the day plus small-scale variability (main
setting); hollow: the satellite map of the day itself.
Data: results/rev2_summary.json (experiments/rev2_summary.py)
"""
import json
import sys

import numpy as np
import style as S
from style import plt

sys.path.insert(0, str(S.ROOT / "paper"))
from terms import CONTROLLER, VEHICLE, VEHICLE_SUB  # noqa: E402

S.setup()
R = json.load(open(S.ROOT / "results" / "rev2_summary.json", encoding="utf-8"))["main"]
GROUPS = [("需要历史任务", ["tuned", "learned"]),
          ("在线元推理", ["rational", "double"]),
          ("巡测规则（不规划航线）", ["greedy", "ucb", "thompson", "lawnmower"]),
          ("参考", ["oracle"])]
COL = {"tuned": S.TUNED, "learned": "#868E96", "rational": S.META, "double": S.META_HELD,
       "greedy": S.RULES["greedy"], "ucb": S.RULES["ucb"], "thompson": S.RULES["thompson"],
       "lawnmower": S.RULES["lawnmower"], "oracle": S.INK}
XMAX, XMIN = 0.075, -0.038
rows, labels, gy = [], [], []
y = 0
for g, keys in GROUPS:
    gy.append((g, y))
    y += 0.75
    for k in keys:
        rows.append((k, y))
        y += 1.0
    y += 0.35
H = y
fig, axes = plt.subplots(1, 4, figsize=(S.TEXTW, 96 * S.MM), sharey=True)
fig.subplots_adjust(left=0.235, right=0.99, top=0.835, bottom=0.13, wspace=0.08)
for j, v in enumerate(["weak", "moderate", "strong", "efficient"]):
    ax = axes[j]
    ax.axvline(0, color=S.REHEARSAL, lw=1.6, zorder=1)
    ax.axvspan(XMIN, 0, color="#F3F0FF", zorder=0, lw=0)
    for k, yy in rows:
        for truth, dy, filled in (("sat+", -0.16, True), ("sat", 0.16, False)):
            r = R.get(truth, {}).get(v, {}).get("rehearsal_minus", {}).get(k)
            if not r:
                continue
            m, lo, hi = -r["mean"], -r["hi"], -r["lo"]
            c = COL[k]
            if m > XMAX:
                ax.plot([XMAX - 0.006], [yy + dy], marker=">", ms=5.5, color=c, mfc=c if filled else "white", mew=1.1)
                ax.text(XMAX - 0.012, yy + dy, S.minus(m, "{:+.2f}"), fontsize=6.6, color="#6B5B45", ha="right", va="center")
                continue
            ax.plot([max(lo, XMIN), min(hi, XMAX)], [yy + dy, yy + dy], color=c, lw=1.4, solid_capstyle="butt")
            ax.plot([m], [yy + dy], "o", ms=4.6, color=c, mfc=c if filled else "white", mew=1.2, zorder=3)
    ax.set_xlim(XMIN, XMAX)
    ax.set_xticks([-0.03, 0, 0.03, 0.06], ["−0.03", "0", "0.03", "0.06"])
    ax.set_ylim(H - 0.1, -0.3)
    ax.grid(axis="y", visible=False)
    ax.set_title(f"{VEHICLE[v]}\n{VEHICLE_SUB[v]}", fontsize=8.4, pad=4)
    if j == 0:
        ax.set_yticks([yy for _, yy in rows], [CONTROLLER[k] for k, _ in rows], fontsize=7.7)
        ax.tick_params(axis="y", length=0)
    for g, yy in gy:
        if j == 0:
            ax.text(-0.02, yy + 0.05, g, transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=7.6,
                    color=S.MUTED, fontweight="bold")
        ax.axhline(yy - 0.3, color="#DEE2E6", lw=0.6, zorder=0)
fig.text(0.61, 0.03, "对照方法的时间平均遗憾 − 出发前预演（越靠右越差；横线为 95% 置信区间）", ha="center", fontsize=8.6)
h1, = axes[0].plot([], [], "o", ms=5, color=S.INK, label="真值：当天卫星图 + 小尺度变化（主设置）")
h2, = axes[0].plot([], [], "o", ms=5, color=S.INK, mfc="white", mew=1.2, label="真值：当天卫星图")
h3, = axes[0].plot([], [], color=S.REHEARSAL, lw=1.6, label="出发前预演（本文）= 0")
fig.legend(handles=[h1, h2, h3], loc="upper center", ncol=3, fontsize=7.8, bbox_to_anchor=(0.61, 1.005),
           handletextpad=0.4, columnspacing=1.4)
S.save(fig, "fig_main")
