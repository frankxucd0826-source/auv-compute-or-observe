"""Fig.: more computation sharpens the answer but does not tell the two worlds apart.
(a) how often the map's side is wrong (test years) for three solver budgets, compared with what new
    information gives (today's 0.5-degree map) and with knowing the real ocean;
(b) as the plausible set grows, how often it covers the real margin (development years) and how
    often a plausible field flips the map's decision (test years)."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style as st  # noqa: E402

sys.path.insert(0, str(st.ROOT / "experiments"))
from route_summary import load, side, devs, worst_regret  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

COMPUTE = "#1C7ED6"
INFO = "#2F9E44"
COVER, FLIP = "#6741D9", "#E03131"


def main():
    st.setup()
    test, dev = load("main", "test"), load("main", "dev")
    P = json.load(open(st.ROOT / "results" / "route_summary_main.json", encoding="utf-8"))["params"]

    def wrong(recs, key):
        return 100 * np.mean([side(r[key]) != side(r["dJ_true"]) for r in recs])

    def regret(recs, key, extra=0.0):
        return np.mean([r["JT"][side(r[key])] - min(r["JT"].values()) for r in recs]) + extra

    fig = plt.figure(figsize=(st.TEXTW, 62 * st.MM))
    axa = fig.add_axes([0.075, 0.25, 0.37, 0.66])
    axb = fig.add_axes([0.585, 0.25, 0.37, 0.66])
    budgets = [("粗网格\n8 千米、8 向", "dJ_map_L0", 2), ("中网格\n4 千米、16 向", "dJ_map_L1", 16), ("细网格\n2 千米、32 向", "dJ_map_L2", 128)]
    xs = np.arange(3)
    w = [wrong(test, k) for _, k, _ in budgets]
    axa.plot(xs, w, color=COMPUTE, lw=2.4, marker="o", ms=8, zorder=3)
    for x, v in zip(xs, w):
        axa.text(x, v + 1.4, f"{v:.1f}%", ha="center", color=COMPUTE, fontsize=8.6)
    fresh = wrong(test, "dJ_map_fresh05")
    axa.axhline(fresh, color=INFO, lw=2.0, ls=(0, (4, 2)))
    axa.text(2.2, fresh - 1.2, f"换成当天 0.5° 图：{fresh:.1f}%", color=INFO, fontsize=8.6, ha="right", va="top")
    axa.axhline(0, color=st.INK, lw=1.2)
    axa.text(2.2, 1.0, "已知真实海流：0%", color=st.INK, fontsize=8.6, ha="right")
    axa.set_xticks(xs)
    axa.set_xticklabels([b[0] for b in budgets], fontsize=8.2)
    axa.set_xlim(-0.35, 2.35)
    axa.set_ylim(-2, 32)
    axa.set_yticks([0, 5, 10, 15, 20, 25])
    axa.set_ylabel("选错一侧的任务（%）")
    axa.text(1.0, 30.5, f"计算量增加 64 倍\n选错比例只降 {w[0] - w[2]:.1f} 个百分点", ha="center", va="top", color=COMPUTE, fontsize=8.4)
    rads = np.round(np.arange(0.25, 2.01, 0.25), 2)
    cover = [100 * np.mean([r["dJ_map_L2"] + devs(r, x)[0] - 1e-9 <= r["dJ_true"] <= r["dJ_map_L2"] + devs(r, x)[1] + 1e-9 for r in dev]) for x in rads]
    flip = [100 * np.mean([worst_regret(r, side(r["dJ_map_L2"]), x) > 0 for r in test]) for x in rads]
    axb.plot(rads, cover, color=COVER, lw=2.4, marker="o", ms=6)
    axb.plot(rads, flip, color=FLIP, lw=2.4, marker="s", ms=6)
    axb.axvline(P["r"], color=st.MUTED, lw=1.0, ls=(0, (3, 2)))
    axb.text(P["r"] - 0.04, 8, f"标定半径 {P['r']:.1f}", color=st.MUTED, fontsize=8.4, ha="right")
    axb.text(1.12, 52, "合理集合包住\n真实差值", color=COVER, fontsize=8.6, va="top")
    axb.text(0.27, 104, "存在合理反例", color=FLIP, fontsize=8.6, va="top")
    i = list(rads).index(P["r"])
    axb.text(P["r"] + 0.05, flip[i] + 3.0, f"{flip[i]:.0f}%", color=FLIP, fontsize=8.6)
    axb.text(P["r"] + 0.05, cover[i] - 8.5, f"{cover[i]:.0f}%", color=COVER, fontsize=8.6)
    axb.set_xlim(0.2, 2.05)
    axb.set_ylim(0, 116)
    axb.set_yticks([0, 20, 40, 60, 80, 100])
    axb.set_xlabel("合理集合的半径")
    axb.set_ylabel("任务比例（%）")
    for ax in (axa, axb):
        for s_ in ("top", "right"):
            ax.spines[s_].set_visible(True)
    st.caption(axa, "(a) 多算与换信息", y=-0.30)
    st.caption(axb, "(b) 合理集合的覆盖与反例", y=-0.30)
    st.save(fig, "fig_route_ambiguity")


if __name__ == "__main__":
    main()
