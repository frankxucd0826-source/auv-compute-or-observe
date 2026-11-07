"""Fig. 4: computing more on the same map does not tell the two kinds of currents apart.
(a) share of test missions whose chosen side is wrong, in the four settings, when the route is solved on
    the vehicle's map with 1x and 64x computation, and when the map is replaced by a same-day
    0.5-degree map (new information);
(b) Kuroshio: as the plausible set grows, how often it covers the real left-right time difference
    (development years) and how often it holds a plausible counterexample (test years); the other
    settings at their own calibrated radius are listed."""
import json
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

import rstyle as st

sys.path.insert(0, str(st.ROOT / "experiments"))
from route_summary import load, side, worst_regret, covered  # noqa: E402

SETTINGS = [("main", "黑潮"), ("gulf", "湾流"), ("agulhas", "阿古拉斯回流区"), ("altimetry", "黑潮（卫星测高图）")]


def wrong(recs, key):
    return 100 * np.mean([side(r[key]) != side(r["dJ_true"]) for r in recs])


def main():
    st.setup()
    fig = plt.figure(figsize=(st.TEXTW, 64 * st.MM))
    axa = fig.add_axes([0.185, 0.17, 0.355, 0.62])
    axb = fig.add_axes([0.745, 0.17, 0.24, 0.62])
    # (a) one row per setting: 1x and 64x computation on the map, then a same-day map
    for i, (tag, name) in enumerate(SETTINGS):
        y = len(SETTINGS) - 1 - i
        T = load(tag, "test")
        w1, w8, w64, wn = (wrong(T, k) for k in ("dJ_map_L0", "dJ_map_L1", "dJ_map_L2", "dJ_map_fresh05"))
        axa.add_patch(FancyArrowPatch((w64 - 0.9, y), (wn + 1.0, y), arrowstyle="-|>", mutation_scale=11,
                                      color=st.OBS, lw=1.6, zorder=2))
        lo, hi = min(w1, w8, w64), max(w1, w8, w64)
        axa.plot([lo, hi], [y, y], color=st.COMPUTE, lw=5.0, alpha=0.25, solid_capstyle="round", zorder=2)
        axa.scatter([w1], [y], s=46, color="white", edgecolor=st.COMPUTE, lw=1.4, zorder=3)
        axa.scatter([w64], [y], s=46, color=st.COMPUTE, edgecolor="white", lw=0.9, zorder=4)
        axa.scatter([wn], [y], s=52, color=st.OBS, edgecolor="white", lw=0.9, zorder=4)
        st.note(axa, (w1 + w64) / 2, y + 0.22, f"{w1:.1f}→{w64:.1f}%", col=st.COMPUTE, size=8.0, ha="center", va="bottom")
        st.note(axa, wn - 1.3, y + 0.04, f"{wn:.1f}%", col=st.OBS, size=8.0, ha="right", weight="bold")
        axa.text(-0.02, y, name, transform=axa.get_yaxis_transform(), ha="right", va="center", fontsize=8.6)
        Pt = json.load(open(st.ROOT / "results" / f"route_summary_{tag}.json", encoding="utf-8"))["params"]
        cx = 100 * np.mean([worst_regret(r, side(r["dJ_map_L2"]), Pt["r"]) > 0 for r in T])
        st.note(axa, 1.16, y, f"{cx:.1f}%", col=st.OURS, size=8.4, weight="bold", ha="center",
                transform=axa.get_yaxis_transform(), clip_on=False)
    axa.set_xlim(0, 36)
    axa.set_ylim(-0.6, len(SETTINGS) - 0.4)
    axa.set_yticks([])
    axa.set_xticks([0, 10, 20, 30])
    axa.set_xlabel("选错一侧的任务（%）", labelpad=2)
    axa.grid(axis="y", visible=False)
    axa.spines["left"].set_visible(False)
    # legend above the rows
    lx, ly = -0.49, 1.06
    for kind, label in (("hollow", "粗网格（1 倍计算）"), ("solid", "细网格（64 倍计算）"), ("new", "当天 0.5° 图")):
        if kind == "hollow":
            axa.scatter([lx + 0.012], [ly], s=34, color="white", edgecolor=st.COMPUTE, lw=1.3, transform=axa.transAxes, clip_on=False)
        else:
            axa.scatter([lx + 0.012], [ly], s=34, color=st.COMPUTE if kind == "solid" else st.OBS, edgecolor="white",
                        lw=0.9, transform=axa.transAxes, clip_on=False)
        t = axa.text(lx + 0.040, ly, label, transform=axa.transAxes, va="center", ha="left", fontsize=8.0)
        fig.canvas.draw()
        lx = t.get_window_extent().transformed(axa.transAxes.inverted()).x1 + 0.045
    axa.text(1.16, 0.98, "存在\n合理反例", transform=axa.transAxes, ha="center", va="bottom", fontsize=8.0,
             color=st.OURS, linespacing=1.1)
    st.panel_title(axa, "(a) 加算与取新信息", x=-0.49, y=1.17)
    # (b) coverage and counterexamples against the radius (Kuroshio)
    T, Dv = load("main", "test"), load("main", "dev")
    P = json.load(open(st.ROOT / "results" / "route_summary_main.json", encoding="utf-8"))["params"]
    rads = np.round(np.arange(0.25, 2.01, 0.25), 2)
    cover = [100 * np.mean([covered(r, x) for r in Dv]) for x in rads]
    flip = [100 * np.mean([worst_regret(r, side(r["dJ_map_L2"]), x) > 0 for r in T]) for x in rads]
    axb.axhline(90, color=st.FAINT, lw=0.9, ls=(0, (2, 2)))
    axb.plot(rads, cover, color=st.OURS, lw=1.8, ls=(0, (4, 2)), marker="o", ms=4.2, mfc="white", mew=1.2)
    axb.plot(rads, flip, color=st.OURS, lw=2.2, marker="o", ms=4.6)
    axb.axvline(P["r"], color=st.MUTED, lw=0.9, ls=(0, (3, 2)))
    i = list(rads).index(P["r"])
    st.note(axb, 0.30, 103.0, "存在合理反例", col=st.OURS, size=8.2, va="bottom")
    st.note(axb, 1.98, 52.0, "合理集合包住\n真实左右航时差", col=st.OURS, size=8.0, ha="right", va="center")
    st.note(axb, P["r"] + 0.06, 108.0, f"{flip[i]:.1f}%", col=st.OURS, size=8.2, weight="bold", va="center")
    st.note(axb, P["r"] + 0.06, cover[i] - 7.0, f"{cover[i]:.0f}%", col=st.OURS, size=8.0, va="center")
    st.note(axb, P["r"] - 0.05, 5.0, f"标定半径 {P['r']:.1f}", col=st.MUTED, size=7.8, ha="right", va="bottom")
    axb.set_xlim(0.2, 2.05)
    axb.set_ylim(0, 115)
    axb.set_xticks([0.5, 1.0, 1.5, 2.0])
    axb.set_yticks([0, 25, 50, 75, 100])
    axb.set_xlabel("合理集合的半径", labelpad=2)
    axb.set_ylabel("任务比例（%）", labelpad=2)
    st.panel_title(axb, "(b) 合理集合越大，反例越普遍", x=-0.33, y=1.17)
    axb.text(-0.33, 1.06, "黑潮；虚线为开发年份，实线为测试年份", transform=axb.transAxes, fontsize=7.6, color=st.MUTED, ha="left", va="bottom")
    st.save(fig, "route4_compute")


if __name__ == "__main__":
    main()
