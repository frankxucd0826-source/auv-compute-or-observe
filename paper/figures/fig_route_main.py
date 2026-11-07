"""Fig.: what each response to an ambiguous route decision costs, test years (623 missions).
Mean regret = real trip time minus the faster side's time, hours; rows grouped by the kind of
response; responses that cost more than the axis shows are written at its right edge."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style as st  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

GROUPS = [
    ("同一张粗图上多算", "#1C7ED6", [("粗网格（8 千米、8 向）", "地图+粗算"), ("中网格（4 千米、16 向）", "地图+标准"),
                                   ("细网格（2 千米、32 向）", "地图+精算")]),
    ("不取新信息、改变决策准则", "#7048E8", [("集合平均选边", "集合期望（贝叶斯）"), ("选最大后悔值较小的一侧", "保守（最坏后悔最小）")]),
    ("就地取新信息", "#2F9E44", [("原地停留 2 小时测流", "原地停留测"), ("沿途测流 30 千米再定", "总是沿途测30km"),
                                ("沿途测流 60 千米再定", "总是沿途测60km"), ("绕行定点测流", "总是绕行定点测")]),
    ("上浮取新图（每次 1 小时）", "#0B7285", [("取当天 1° 图", "总是上浮取当天1°图"), ("取当天 0.5° 图", "总是上浮取当天0.5°图")]),
    ("最大后悔值超过阈值时（本文）", "#E03131", [("保守改选", "反例门控→保守"), ("上浮取当天 0.5° 图", "反例门控→上浮取0.5°图")]),
]
XMAX = 3.2
REF = 1.0


def main():
    st.setup()
    S = json.load(open(st.ROOT / "results" / "route_summary_main.json", encoding="utf-8"))
    T = S["test"]["table"]
    rows = []
    for g, col, items in GROUPS:
        rows.append(("group", g, col))
        for label, key in items:
            rows.append(("item", label, col, T[key]["regret_h"]))
    fig = plt.figure(figsize=(st.TEXTW, 92 * st.MM))
    ax = fig.add_axes([0.34, 0.14, 0.62, 0.84])
    y = 0
    yt, yl = [], []
    best = T["反例门控→保守"]["regret_h"]
    global REF
    REF = T["地图+精算"]["regret_h"]
    for r in rows:
        if r[0] == "group":
            y -= 0.35
            ax.text(-0.02, y, r[1], transform=ax.get_yaxis_transform(), ha="right", va="center",
                    fontsize=8.8, color=r[2], fontweight="bold")
            y -= 0.85
            continue
        _, label, col, v = r
        yt.append(y)
        yl.append(label)
        x = min(v, XMAX)
        ax.plot([0, x], [y, y], color=col, lw=1.6, alpha=0.35, solid_capstyle="butt")
        if abs(v - best) < 1e-9:
            ax.scatter([x], [y], s=230, color=col, alpha=0.18, lw=0, zorder=2)
        ax.scatter([x], [y], s=46, color=col, zorder=3, lw=0)
        if v > XMAX:
            ax.text(XMAX - 0.03, y + 0.28, f"{v:.1f} →", ha="right", va="bottom", fontsize=8.4, color=col)
        elif v < REF - 0.02:
            ax.text(x - 0.06, y - 0.05, f"{v:.2f}", ha="right", va="center", fontsize=8.4, color=col,
                    bbox=dict(boxstyle="square,pad=0.05", fc="white", ec="none"))
        else:
            ax.text(x + 0.06, y, f"{v:.2f}", ha="left", va="center", fontsize=8.4, color=col)
        y -= 1.0
    ref = T["地图+精算"]["regret_h"]
    ax.axvline(ref, color=st.MUTED, lw=1.0, ls=(0, (3, 2)))
    ax.text(ref + 0.04, -0.15, "基线：按粗图选边", color=st.MUTED, fontsize=8.2, va="center")
    ax.set_yticks(yt)
    ax.set_yticklabels(yl, fontsize=8.4)
    ax.set_xlim(0, XMAX)
    ax.set_ylim(y + 0.2, 0.2)
    ax.set_xlabel("平均额外航时（小时），测试年份 623 个任务")
    ax.grid(axis="y", visible=False)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(True)
    st.save(fig, "fig_route_main")


if __name__ == "__main__":
    main()
