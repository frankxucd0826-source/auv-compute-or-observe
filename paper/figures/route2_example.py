"""Fig. 2: one test mission (2022-01-18, chosen by a stated rule in experiments/route_example.py).
(a) the 1-degree map made 3 days earlier: the two sides look equally fast; (b) a plausible counterexample,
a field inside the calibrated plausible set (radius 1.5) in which the map's side is much slower; (c) the
real current of that day; (d) the fastest time of each side in the three fields."""
import json

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import Normalize

import rstyle as st
import rmaps as rm

PANELS = [("map", "(a) 3 天前的 1° 粗图", "两侧几乎一样快，按粗图选左侧", st.MAP),
          ("counter", "(b) 合理反例", "合理集合内的一个流场：左侧慢得多", st.OURS),
          ("truth", "(c) 当天真实海流", "右侧快 11.7 小时，按粗图选错", "#2B3A4A")]


def main():
    st.setup()
    D = np.load(st.ROOT / "results" / "route_example.npz")
    M = json.load(open(st.ROOT / "results" / "route_example.json", encoding="utf-8"))
    W_MM, H_MM = 154, 106
    fig = plt.figure(figsize=(W_MM * st.MM, H_MM * st.MM))
    w, gap, left = 0.300, 0.035, 0.0125
    h = w * W_MM / H_MM
    yb = 0.432
    for i, (name, title, sub, col) in enumerate(PANELS):
        x = left + i * (w + gap)
        ax = fig.add_axes([x, yb, w, h])
        times = {a: M[f"{name}_time_{a}"] for a in "LR"}
        rm.draw(ax, D, name, times, frame=col, scale_bar=(i == 0))
        fig.text(x, yb + h + 0.072, "●", color=col, fontsize=8, va="bottom", ha="left")
        fig.text(x + 0.016, yb + h + 0.068, title, fontproperties=st.bold(9.4), color=st.INK, va="bottom", ha="left")
        fig.text(x, yb + h + 0.018, sub, fontsize=8.4, color=st.MUTED, va="bottom", ha="left")
        if i < 2:
            rm.hollow_arrow(fig, x + w + gap / 2, yb + h / 2)
    # legend band
    band = fig.add_axes([0.0, 0.318, 1.0, 0.072])
    band.set_xlim(0, 1)
    band.set_ylim(0, 1)
    band.axis("off")
    band.add_patch(Rectangle((0, 0), 1, 1, fc=rm.NIGHT, ec="none"))
    items = [("line", rm.GOLD, "-", "左侧航线"), ("line", rm.PINK, "-", "右侧航线"),
             ("line", "#C9D3DD", (0, (2.6, 1.6)), "较慢一侧"), ("marker", "o", None, "起点"),
             ("marker", "*", None, "终点"), ("zone", None, None, "禁航区")]
    xx = 0.018
    for kind, a, b, label in items:
        if kind == "line":
            band.plot([xx, xx + 0.032], [0.5, 0.5], color=a, lw=2.2, ls=b, solid_capstyle="round")
            xx += 0.040
        elif kind == "marker":
            band.scatter([xx + 0.008], [0.5], marker=a, s=40 if a == "o" else 90, color="white", edgecolor=rm.NIGHT)
            xx += 0.020
        else:
            band.scatter([xx + 0.008], [0.5], marker="o", s=70, color="#E8616B", edgecolor="white", lw=0.9)
            xx += 0.020
        t = band.text(xx, 0.5, label, color="white", va="center", ha="left", fontsize=8.2)
        fig.canvas.draw()
        bb = t.get_window_extent().transformed(band.transData.inverted())
        xx = bb.x1 + 0.022
    cax = fig.add_axes([0.80, 0.360, 0.17, 0.017])
    cb = ColorbarBase(cax, cmap=rm.SEA, norm=Normalize(0, rm.SEA_VMAX), orientation="horizontal", ticks=[0, 0.5, 1.0])
    cb.outline.set_edgecolor("white")
    cb.outline.set_linewidth(0.6)
    cax.tick_params(colors="white", labelsize=7.6, length=2, pad=1.0)
    cax.set_xticklabels(["0", "0.5", "1.0"])
    fig.text(0.792, 0.354, "流速（米/秒）", color="white", fontsize=8.0, ha="right", va="center")
    # (d) fastest time of each side
    ax = fig.add_axes([0.205, 0.088, 0.60, 0.160])
    rows = [("map", "(a) 粗图"), ("counter", "(b) 合理反例"), ("truth", "(c) 真实海流")]
    for j, (name, label) in enumerate(rows):
        y = 2 - j
        tL, tR = M[f"{name}_time_L"], M[f"{name}_time_R"]
        ax.plot([tL, tR], [y, y], color=st.GRID if False else "#C5CED8", lw=3.0, solid_capstyle="round", zorder=1)
        for a, t in (("L", tL), ("R", tR)):
            ax.scatter([t], [y], s=62, color=rm.SIDE_D[a], edgecolor="white", lw=1.2, zorder=3)
        fast = "左" if tL < tR else "右"
        d = abs(tL - tR)
        col = rm.SIDE_D["L" if tL < tR else "R"]
        st.note(ax, 58.6, y, f"{fast}侧快 {d:.1f} 小时", col=col, size=8.6, weight="bold", ha="left")
        ax.text(-0.012, y, label, transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=8.6, color=st.INK)
    for k, (a, lab) in enumerate((("L", "左侧"), ("R", "右侧"))):
        ax.scatter([0.775 + 0.125 * k], [1.07], s=42, color=rm.SIDE_D[a], edgecolor="white", lw=1.0,
                   transform=ax.transAxes, clip_on=False)
        ax.text(0.792 + 0.125 * k, 1.07, lab, transform=ax.transAxes, va="center", ha="left", fontsize=8.4)
    ax.set_xlim(35, 58)
    ax.set_ylim(-0.55, 2.55)
    ax.set_yticks([])
    ax.set_xticks([36, 40, 44, 48, 52, 56])
    ax.set_xlabel("两侧最快航时（小时）", labelpad=2)
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    fig.text(0.0125, 0.268, "(d) 三种海流下两侧的最快航时", fontproperties=st.bold(9.4), color=st.INK, va="bottom")
    st.save(fig, "route2_example")


if __name__ == "__main__":
    main()
