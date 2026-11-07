"""Fig. 5: the maximum regret finds where the extra time is.
(a) Kuroshio test missions ranked by a risk score, riskiest first: share of the baseline's total extra time
    held by the top fraction; ideal order (by the real extra time), maximum regret (this paper), the share of
    32 ensemble members that change the side, the closeness of the two sides on the map, random order;
    the dot marks the missions the threshold rule flags.
(b) share of the extra time held by the riskiest 20% under each score, in the four settings."""
import json
import sys

import numpy as np
import matplotlib.pyplot as plt

import rstyle as st

sys.path.insert(0, str(st.ROOT / "experiments"))
from route_summary import load, side, worst_regret, ens_l2  # noqa: E402

SETTINGS = [("main", "黑潮"), ("gulf", "湾流"), ("agulhas", "阿古拉斯回流区"), ("altimetry", "黑潮（卫星测高图）")]


def gains(score, loss):
    o = np.argsort(-np.asarray(score, float), kind="stable")
    c = np.cumsum(np.asarray(loss, float)[o])
    return np.r_[0, np.arange(1, len(o) + 1) / len(o)], np.r_[0, c / c[-1]]


def scores(tag):
    T = load(tag, "test")
    P = json.load(open(st.ROOT / "results" / f"route_summary_{tag}.json", encoding="utf-8"))["params"]
    loss = np.array([r["JT"][side(r["dJ_map_L2"])] - min(r["JT"].values()) for r in T])
    S = {"ideal": loss,
         "regret": np.array([worst_regret(r, side(r["dJ_map_L2"]), P["r"]) for r in T]),
         "flip": np.array([float(np.mean(np.sign(ens_l2(r)) != np.sign(r["dJ_map_L2"]))) for r in T]),
         "margin": np.array([-abs(r["dJ_map_L2"]) for r in T])}
    return S, loss, P


def top(score, loss, f=0.2):
    x, y = gains(score, loss)
    return 100 * float(np.interp(f, x, y))


def main():
    st.setup()
    fig = plt.figure(figsize=(st.TEXTW, 66 * st.MM))
    axa = fig.add_axes([0.085, 0.165, 0.36, 0.67])
    axb = fig.add_axes([0.665, 0.165, 0.315, 0.67])
    S, loss, P = scores("main")
    style = [("ideal", "按真实额外航时（上限）", st.INK, 1.3, (0, (1, 0))),
             ("regret", "最大后悔值（本文）", st.OURS, 2.6, "-"),
             ("flip", "改变选边的成员比例", st.ENS, 2.0, "-"),
             ("margin", "粗图左右航时差", st.MAP, 1.8, (0, (4, 2)))]
    axa.plot([0, 100], [0, 100], color=st.FAINT, lw=1.2, ls=(0, (2, 2)))
    axa.axvspan(0, 20, color=st.COOL_BG, lw=0, zorder=0)
    for key, name, col, lw, ls in style:
        x, y = gains(S[key], loss)
        axa.plot(100 * x, 100 * y, color=col, lw=lw, ls=ls, zorder=3 if key == "regret" else 2)
    # values at 20%
    lab_y = {"ideal": 103, "regret": None, "flip": None, "margin": None}
    vals = {k: top(S[k], loss) for k in S}
    for key, name, col, lw, ls in style[1:]:
        axa.scatter([20], [vals[key]], s=30, color=col, edgecolor="white", lw=0.9, zorder=4)
    rows = [("regret", f"最大后悔值（本文）  {vals['regret']:.0f}%", st.OURS, "bold"),
            ("flip", f"改变选边的成员比例  {vals['flip']:.0f}%", st.ENS, None),
            ("margin", f"粗图左右航时差  {vals['margin']:.0f}%", st.MAP, None)]
    axa.text(98, 31.0, "前 20% 的任务所占额外航时", ha="right", va="center", fontsize=7.8, color=st.INK)
    for j, (key, text, col, wt) in enumerate(rows):
        st.note(axa, 98, 23.0 - 7.6 * j, text, col=col, size=7.8, weight=wt, ha="right", va="center")
    st.note(axa, 6.0, 96.0, "上限", col=st.INK, size=7.8, ha="left")
    st.note(axa, 66.0, 58.0, "随机", col=st.MUTED, size=7.6, ha="center", rotation=38)
    # the threshold rule on the regret curve
    flag = S["regret"] > P["tau_robust"]
    fx, fy = 100 * flag.mean(), 100 * loss[flag].sum() / loss.sum()
    axa.scatter([fx], [fy], s=150, color=st.OURS, alpha=0.18, lw=0, zorder=4)
    axa.scatter([fx], [fy], s=34, marker="D", color="white", edgecolor=st.OURS, lw=1.4, zorder=5)
    st.note(axa, fx, fy + 8.5, "阈值判据", col=st.OURS, size=7.8, ha="center", va="bottom")
    print("threshold flags", round(fx, 1), "% holding", round(fy, 1), "%")
    axa.set_xlim(0, 100)
    axa.set_ylim(0, 108)
    axa.set_xticks([0, 20, 40, 60, 80, 100])
    axa.set_yticks([0, 25, 50, 75, 100])
    axa.set_xlabel("按风险从高到低排在前面的任务（%）", labelpad=2)
    axa.set_ylabel("所占的基线额外航时（%）", labelpad=2)
    st.panel_title(axa, "(a) 风险排序（黑潮）", x=-0.20, y=1.13)
    axa.text(-0.20, 1.05, "曲线越靠左上，额外航时越集中在被排在前面的任务", transform=axa.transAxes, fontsize=7.6, color=st.MUTED, ha="left", va="bottom")
    # (b) top-20% share in four settings
    marks = [("margin", st.MAP, "s", "粗图左右航时差"), ("flip", st.ENS, "o", "改变选边的成员比例"),
             ("regret", st.OURS, "o", "最大后悔值（本文）")]
    for i, (tag, name) in enumerate(SETTINGS):
        y = len(SETTINGS) - 1 - i
        Sx, lx, _ = scores(tag) if tag != "main" else (S, loss, P)
        v = {k: top(Sx[k], lx) for k in ("margin", "flip", "regret")}
        lo, hi = min(v.values()), max(v.values())
        axb.plot([lo, hi], [y, y], color=st.GRID, lw=3.0, solid_capstyle="round", zorder=1)
        for key, col, mk, _ in marks:
            if key == "regret":
                axb.scatter([v[key]], [y], s=150, color=col, alpha=0.18, lw=0, zorder=2)
            axb.scatter([v[key]], [y], s=46 if key == "regret" else 34, marker=mk, color=col, edgecolor="white",
                        lw=0.9, zorder=3)
        st.note(axb, v["regret"] + 3.0, y, f"{v['regret']:.0f}%", col=st.OURS, size=8.2, weight="bold", ha="left")
        st.note(axb, v["flip"], y + 0.30, f"{v['flip']:.0f}%", col=st.ENS, size=7.6, ha="center", va="bottom")
        axb.text(-0.03, y, name, transform=axb.get_yaxis_transform(), ha="right", va="center", fontsize=8.4)
    axb.axvline(20, color=st.FAINT, lw=1.0, ls=(0, (2, 2)))
    axb.text(20.8, -0.52, "随机 20%", color=st.MUTED, fontsize=7.6, ha="left", va="center")
    axb.set_xlim(10, 90)
    axb.set_ylim(-0.7, len(SETTINGS) - 0.35)
    axb.set_yticks([])
    axb.set_xticks([20, 40, 60, 80])
    axb.set_xlabel("前 20% 的任务所占额外航时（%）", labelpad=2)
    axb.grid(axis="y", visible=False)
    axb.spines["left"].set_visible(False)
    lx, ly = -0.62, 1.075
    for key, col, mk, label in marks:
        axb.scatter([lx + 0.015], [ly], s=30, marker=mk, color=col, edgecolor="white", lw=0.8,
                    transform=axb.transAxes, clip_on=False)
        t = axb.text(lx + 0.04, ly, label, transform=axb.transAxes, va="center", ha="left", fontsize=7.8)
        fig.canvas.draw()
        lx = t.get_window_extent().transformed(axb.transAxes.inverted()).x1 + 0.05
    st.panel_title(axb, "(b) 四种设置的对比", x=-0.62, y=1.13)
    st.save(fig, "route5_rank")


if __name__ == "__main__":
    main()
