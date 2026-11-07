"""Fig. 6: what the gradient search buys on a vehicle with little computation (Kuroshio test missions).
(a) mean extra time of choosing the side with the shorter mean time over n random ensemble members (2n
    route solves), against the route solves spent; filled markers: significantly worse than the gradient
    search (paired bootstrap over days); the gradient search with the choice of the side whose maximum
    regret is smaller (about 71 solves) is one point; the baseline is the dashed line.
(b) share of the baseline's extra time held by the riskiest 20% of missions, for two ensemble scores computed
    on the same n members (the mean regret of keeping the map's side, and the share of members that change
    the side), against the route solves spent; the maximum regret of the search is one point.
Numbers from results/route_ensemble_size.json (experiments/route_ensemble_analysis.py)."""
import json

import numpy as np
import matplotlib.pyplot as plt

import rstyle as st

NS = (8, 16, 32, 64, 128, 256, 512, 1024)


def main():
    st.setup()
    R = json.load(open(st.ROOT / "results" / "route_ensemble_size.json", encoding="utf-8"))["test"]
    solves = np.array([2 * n for n in NS], float)
    cx = R["worst_regret"]["route_solves"]
    fig = plt.figure(figsize=(st.TEXTW, 62 * st.MM))
    axa = fig.add_axes([0.085, 0.18, 0.375, 0.64])
    axb = fig.add_axes([0.595, 0.18, 0.375, 0.64])
    # (a) side choice
    loss = np.array([R[f"expected_{n}"]["loss"] for n in NS])
    sig = np.array([R[f"expected_{n}"]["ci_vs_worst_regret"][0] > 0 for n in NS])
    base = R["map"]["loss"]
    axa.axhline(base, color=st.MAP, lw=1.3, ls=(0, (4, 2)))
    st.note(axa, 3600, base + 0.035, f"基线 {base:.2f} 小时", col=st.MAP, size=7.8, ha="right", va="bottom")
    axa.plot(solves, loss, color=st.ENS, lw=2.0, zorder=2)
    axa.scatter(solves[sig], loss[sig], s=34, color=st.ENS, edgecolor="white", lw=0.9, zorder=3)
    axa.scatter(solves[~sig], loss[~sig], s=34, color="white", edgecolor=st.ENS, lw=1.4, zorder=3)
    for n, x, y in zip(NS, solves, loss):
        if n in (8, 32, 1024):
            st.note(axa, x * (1.12 if n != 1024 else 1.0), y + (0.06 if n != 1024 else -0.06), f"{n} 个成员",
                    col=st.ENS, size=7.6, ha="left" if n != 1024 else "center", va="center" if n != 1024 else "top")
    y0 = R["worst_regret"]["loss"]
    axa.annotate("", xy=(2048 * 0.93, y0), xytext=(cx * 1.15, y0),
                 arrowprops=dict(arrowstyle="-|>", color=st.ENS, lw=1.1, ls=(0, (3, 2)), mutation_scale=9))
    axa.text(300, y0 - 0.05, "约 29 倍求解次数", color=st.ENS, fontsize=7.8, ha="center", va="top")
    axa.scatter([cx], [y0], s=230, color=st.OURS, alpha=0.18, lw=0, zorder=4)
    axa.scatter([cx], [y0], s=56, marker="D", color=st.OURS, edgecolor="white", lw=1.0, zorder=5)
    st.note(axa, cx, y0 - 0.17, f"梯度搜索\n{cx:.0f} 次求解，{y0:.2f} 小时", col=st.OURS, size=7.8, weight="bold",
            ha="center", va="top")
    axa.annotate("更好", xy=(10.2, 0.36), xytext=(14.5, 0.68), fontsize=7.8, color=st.MUTED, ha="center",
                 va="center", arrowprops=dict(arrowstyle="-|>", color=st.MUTED, lw=1.0, mutation_scale=8))
    axa.set_xscale("log", base=2)
    axa.set_xticks([16, 64, 256, 1024, 2048])
    axa.set_xticklabels(["16", "64", "256", "1024", "2048"])
    axa.minorticks_off()
    axa.set_xlim(9, 4000)
    axa.set_ylim(0.3, 1.85)
    axa.set_yticks([0.5, 1.0, 1.5])
    axa.set_xlabel("每个任务的航线求解次数", labelpad=2)
    axa.set_ylabel("平均额外航时（小时）", labelpad=2)
    st.panel_title(axa, "(a) 选哪一侧：集合平均选边", x=-0.20, y=1.12)
    axa.text(-0.20, 1.03, "实心：显著差于梯度搜索；空心：差异不显著", transform=axa.transAxes, fontsize=7.6,
             color=st.MUTED, ha="left", va="bottom")
    # (b) which missions are risky
    T20 = R["top20_loss_share"]
    expr = np.array([100 * T20[f"expected_regret_{n}"] for n in NS])
    flip = np.array([100 * T20[f"flip_share_{n}"] for n in NS])
    mm = 100 * T20["map_margin"]
    axb.axhline(mm, color=st.MAP, lw=1.3, ls=(0, (4, 2)))
    st.note(axb, 3600, mm - 2.5, f"粗图左右航时差 {mm:.0f}%", col=st.MAP, size=7.8, ha="right", va="top")
    axb.plot(solves, expr, color=st.ENS, lw=2.0, zorder=2)
    axb.scatter(solves, expr, s=30, color=st.ENS, edgecolor="white", lw=0.9, zorder=3)
    axb.plot(solves, flip, color=st.ENS, lw=1.6, ls=(0, (3, 2)), zorder=2)
    axb.scatter(solves, flip, s=30, color="white", edgecolor=st.ENS, lw=1.3, zorder=3)
    st.note(axb, 3600, expr[-1] + 3.0, f"后悔值的集合平均 {expr[-1]:.0f}%", col=st.ENS, size=7.8, ha="right", va="bottom")
    st.note(axb, 3600, 50.5, f"改变选边的成员比例 {flip[-1]:.0f}%", col=st.ENS, size=7.8, ha="right",
            va="bottom")
    v = 100 * T20["worst_regret"]
    axb.scatter([cx], [v], s=230, color=st.OURS, alpha=0.18, lw=0, zorder=4)
    axb.scatter([cx], [v], s=56, marker="D", color=st.OURS, edgecolor="white", lw=1.0, zorder=5)
    st.note(axb, cx * 1.25, v + 5.0, f"最大后悔值 {v:.0f}%", col=st.OURS, size=7.8, weight="bold", ha="right", va="bottom")
    axb.set_xscale("log", base=2)
    axb.set_xticks([16, 64, 256, 1024, 2048])
    axb.set_xticklabels(["16", "64", "256", "1024", "2048"])
    axb.minorticks_off()
    axb.set_xlim(9, 4000)
    axb.set_ylim(20, 85)
    axb.set_yticks([20, 40, 60, 80])
    axb.set_xlabel("每个任务的航线求解次数", labelpad=2)
    axb.set_ylabel("前 20% 所占额外航时（%）", labelpad=2)
    st.panel_title(axb, "(b) 哪些任务危险：两种集合指标", x=-0.20, y=1.12)
    axb.text(-0.20, 1.03, "同一批集合成员；成员越多，求解越多", transform=axb.transAxes, fontsize=7.6,
             color=st.MUTED, ha="left", va="bottom")
    st.save(fig, "route6_budget")
    print({n: (round(l, 2), bool(s)) for n, l, s in zip(NS, loss, sig)})


if __name__ == "__main__":
    main()
