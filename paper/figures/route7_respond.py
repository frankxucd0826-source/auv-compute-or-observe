"""Fig. 7: what to do once the map is judged untrustworthy for a decision.
(a) change of the mean extra time against the baseline (test missions, hours) for responses that get no new
    information and responses that do, in the four settings; bars: point estimate; whiskers: 95% interval
    (bootstrap over days); light hatched bars: interval contains zero. In the altimetry setting surfacing
    fetches a same-day 0.5-degree model map (ideal reference).
(b) Kuroshio: mean extra time against the time one surfacing costs; thresholds re-tuned on the
    development years for every cost.
(c) share of test missions with one side impassable in the real current."""
import json
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

import rstyle as st

sys.path.insert(0, str(st.ROOT / "experiments"))
from route_summary import load, calibrate, outcomes  # noqa: E402

SETTINGS = [("main", "黑潮"), ("gulf", "湾流"), ("agulhas", "阿古拉斯回流区"), ("altimetry", "黑潮（卫星测高图）")]
XLIM = {"main": (-0.75, 0.75), "gulf": (-4.2, 2.6), "agulhas": (-7.2, 2.6), "altimetry": (-0.75, 0.75)}
XT = {"main": [-0.5, 0, 0.5], "gulf": [-4, -2, 0, 2], "agulhas": [-6, -3, 0], "altimetry": [-0.5, 0, 0.5]}
ROWS = [  # group, label, key, colour
    ("none", "集合平均选边", "集合期望（贝叶斯）", st.ENS),
    ("none", "超阈值时保守改选（本文）", "反例门控→保守", st.OURS),
    ("info", "沿途测流 30 千米", "总是沿途测30km", st.SPOT),
    ("info", "总是上浮取当天 0.5° 图", "总是上浮取当天0.5°图", "#6CC0B5"),
    ("info", "超阈值时上浮取图（本文）", "反例门控→上浮取0.5°图", st.OBS),
]
GROUP = {"none": ("不取\n新信息", st.MAP), "info": ("取\n新信息", st.OBS)}


def main():
    st.setup()
    fig = plt.figure(figsize=(st.TEXTW, 122 * st.MM))
    top, h = 0.855, 0.355
    x0, wcol, gcol = 0.300, 0.153, 0.022
    ys = [4.5, 3.4, 1.8, 0.7, -0.4]
    for j, (tag, name) in enumerate(SETTINGS):
        S = json.load(open(st.ROOT / "results" / f"route_summary_{tag}.json", encoding="utf-8"))["test"]["table"]
        ax = fig.add_axes([x0 + j * (wcol + gcol), top - h, wcol, h])
        ax.axvline(0, color=st.INK, lw=0.9, zorder=1)
        for (grp, label, key, col), y in zip(ROWS, ys):
            d, (lo, hi) = S[key]["minus_map"], S[key]["minus_map_ci"]
            sig = lo > 0 or hi < 0
            ax.barh([y], [d], height=0.62, color=col if sig else "white", edgecolor=col, lw=1.1,
                    hatch=None if sig else "////", alpha=1.0, zorder=2)
            ax.plot([lo, hi], [y, y], color=st.INK, lw=0.9, zorder=3)
            for e in (lo, hi):
                ax.plot([e, e], [y - 0.13, y + 0.13], color=st.INK, lw=0.9, zorder=3)
            xa, xb = XLIM[tag]
            txt = st.minus(d)
            # the number sits on the side of zero opposite to the bar, clear of the interval
            if d < 0:
                xt, ha = max(hi, 0) + 0.03 * (xb - xa), "left"
            else:
                xt, ha = min(lo, 0) - 0.03 * (xb - xa), "right"
            st.note(ax, xt, y, txt, col=col if sig else st.MUTED, size=7.6, weight="bold" if sig else None,
                    ha=ha, va="center")
        ax.set_xlim(*XLIM[tag])
        ax.set_ylim(-1.1, 5.2)
        ax.set_yticks([])
        ax.set_xticks(XT[tag])
        ax.set_xticklabels([st.minus(t, "{:g}") if t != 0 else "0" for t in XT[tag]], fontsize=7.8)
        ax.grid(axis="y", visible=False)
        ax.spines["left"].set_visible(False)
        ax.axhline(2.6, color=st.GRID, lw=0.8, zorder=0)
        base = S["地图+精算"]["regret_h"]
        ax.text(0.5, 1.115, name, transform=ax.transAxes, ha="center", va="bottom", fontproperties=st.bold(8.6))
        ax.text(0.5, 1.02, f"基线 {base:.2f} 小时", transform=ax.transAxes, ha="center", va="bottom", fontsize=7.6,
                color=st.MUTED)
        if j == 0:
            for (grp, label, key, col), y in zip(ROWS, ys):
                ax.text(-0.06, y, label, transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=8.0,
                        color=st.INK)
    # group tags
    tagax = fig.add_axes([0.0, top - h, 0.072, h])
    tagax.set_xlim(0, 1)
    tagax.set_ylim(-1.1, 5.2)
    tagax.axis("off")
    for grp, (y_lo, y_hi) in (("none", (2.85, 5.05)), ("info", (-0.95, 2.35))):
        text, col = GROUP[grp]
        tagax.add_patch(FancyBboxPatch((0.06, y_lo), 0.88, y_hi - y_lo, boxstyle="round,pad=0,rounding_size=0.15",
                                       fc=col, ec="none", mutation_aspect=5.0))
        tagax.text(0.5, (y_lo + y_hi) / 2, text, ha="center", va="center", color="white", fontproperties=st.bold(7.8),
                   linespacing=1.15)
    fig.text(x0 + 2 * (wcol + gcol) - gcol / 2, top - h - 0.058, "相对基线的平均额外航时变化（小时），负值为改善",
             ha="center", va="top", fontsize=8.4)
    lg = fig.add_axes([0.40, 0.955, 0.58, 0.03])
    lg.axis("off")
    lg.set_xlim(0, 1)
    lg.set_ylim(0, 1)
    xx = 0.0
    for kind, label in (("sig", "显著（95% 区间不含 0）"), ("ns", "不显著"), ("ci", "95% 区间")):
        if kind == "sig":
            lg.add_patch(Rectangle((xx, 0.15), 0.035, 0.7, fc=st.MAP, ec=st.MAP))
        elif kind == "ns":
            lg.add_patch(Rectangle((xx, 0.15), 0.035, 0.7, fc="white", ec=st.MAP, hatch="////"))
        else:
            lg.plot([xx, xx + 0.035], [0.5, 0.5], color=st.INK, lw=0.9)
            for e in (xx, xx + 0.035):
                lg.plot([e, e], [0.3, 0.7], color=st.INK, lw=0.9)
        t = lg.text(xx + 0.048, 0.5, label, va="center", fontsize=7.8)
        fig.canvas.draw()
        xx = t.get_window_extent().transformed(lg.transData.inverted()).x1 + 0.05
    fig.text(0.0, 0.97, "(a) 各种应对相对基线的变化", fontproperties=st.bold(9.4), va="center")
    # (b) surfacing cost, Kuroshio
    axb = fig.add_axes([0.085, 0.072, 0.43, 0.25])
    test, dev = load("main", "test"), load("main", "dev")
    costs = [0.0, 0.5, 1.0, 2.0, 3.0, 4.0]
    lines = {k: [] for k in ("always", "gate_surf", "gate_cons", "map")}
    for c in costs:
        Pc, _ = calibrate(dev, c)
        rows = [outcomes(r, Pc)[0] for r in test]
        lines["always"].append(np.mean([o["总是上浮取当天0.5°图"] - o["知道真相"] for o in rows]))
        lines["gate_surf"].append(np.mean([o["反例门控→上浮取0.5°图"] - o["知道真相"] for o in rows]))
        lines["gate_cons"].append(np.mean([o["反例门控→保守"] - o["知道真相"] for o in rows]))
        lines["map"].append(np.mean([o["地图+精算"] - o["知道真相"] for o in rows]))
    print({k: [round(v, 2) for v in vals] for k, vals in lines.items()})
    axb.plot(costs, lines["map"], color=st.MAP, lw=1.3, ls=(0, (4, 2)))
    axb.plot(costs, lines["always"], color="#6CC0B5", lw=1.8, ls=(0, (3, 1.5)), marker="o", ms=3.8, mfc="white", mew=1.2)
    axb.plot(costs, lines["gate_surf"], color=st.OBS, lw=2.2, marker="o", ms=4.2)
    axb.plot(costs, lines["gate_cons"], color=st.OURS, lw=2.2, marker="D", ms=3.8)
    st.note(axb, 4.05, lines["map"][-1] - 0.05, "基线", col=st.MAP, size=7.8, ha="right", va="top")
    st.note(axb, 1.62, 1.38, "总是上浮", col="#4FA79B", size=7.8, ha="left", va="center")
    st.note(axb, 3.0, 1.13, "超阈值时上浮取图", col=st.OBS, size=7.8, ha="center", va="bottom")
    st.note(axb, 3.1, lines["gate_cons"][-1] - 0.10, "超阈值时保守改选", col=st.OURS, size=7.8, ha="center", va="top")
    gap_ = np.array(lines["gate_surf"]) - np.array(lines["gate_cons"])
    k = int(np.argmax(gap_ > 0))
    xc = costs[k - 1] + (costs[k] - costs[k - 1]) * (-gap_[k - 1]) / (gap_[k] - gap_[k - 1])
    print("crossover at", round(xc, 2), "h")
    axb.axvspan(0, xc, color=st.COOL_BG, lw=0, zorder=0)
    axb.text(xc / 2 + 0.02, 1.92, "上浮便宜\n先取新图", ha="center", va="top", fontsize=7.4, color=st.OBS)
    axb.text(xc + 0.05, 0.06, f"约 {xc:.1f} 小时", ha="left", va="bottom", fontsize=7.6, color=st.OBS)
    axb.set_xlim(0, 4.1)
    axb.set_ylim(0, 2.0)
    axb.set_xticks([0, 1, 2, 3, 4])
    axb.set_yticks([0, 0.5, 1.0, 1.5, 2.0])
    axb.set_xlabel("一次上浮取图的代价（小时）", labelpad=2)
    axb.set_ylabel("平均额外航时（小时）", labelpad=2)
    st.panel_title(axb, "(b) 上浮代价与应对方式（黑潮）", x=-0.17, y=1.07)
    # (c) one side impassable
    axc = fig.add_axes([0.725, 0.072, 0.255, 0.25])
    CAP = 200.0
    for i, (tag, name) in enumerate(SETTINGS):
        T = load(tag, "test")
        b = 100 * np.mean([max(r["JT"].values()) >= CAP - 1e-6 for r in T])
        y = len(SETTINGS) - 1 - i
        hot = tag in ("gulf", "agulhas")
        axc.barh([y], [b], height=0.58, color=st.COMPUTE_LIGHT if not hot else "#F2A97E", edgecolor="none")
        st.note(axc, b + 0.5, y, f"{b:.1f}%", size=7.8, weight="bold" if hot else None, ha="left", va="center")
        axc.text(-0.04, y, name.replace("黑潮（卫星测高图）", "黑潮（测高图）"), transform=axc.get_yaxis_transform(),
                 ha="right", va="center", fontsize=8.0)
    axc.set_xlim(0, 21)
    axc.set_ylim(-0.6, len(SETTINGS) - 0.4)
    axc.set_yticks([])
    axc.set_xticks([0, 10, 20])
    axc.set_xlabel("任务比例（%）", labelpad=2)
    axc.grid(axis="y", visible=False)
    axc.spines["left"].set_visible(False)
    st.panel_title(axc, "(c) 一侧无法通行的任务", x=-0.62, y=1.07)
    st.save(fig, "route7_respond")


if __name__ == "__main__":
    main()
