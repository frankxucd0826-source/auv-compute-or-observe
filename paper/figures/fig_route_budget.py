"""Fig.: what the counterexample search buys on a vehicle with little computation (test years).
(a) Mean loss of choosing the side with the smaller expected time over n random plausible fields
    (2n route solves), against the route solves spent; the counterexample search with the conservative
    choice (about 71 solves) is one point; the map with the expensive solver is the reference line.
(b) Share of the map's total loss held by the 20% of missions a score ranks riskiest: the expected
    regret of keeping the map's side and the flip share over the same n random fields, against the
    solves spent; the worst regret of the search is one point.
Numbers come from results/route_ensemble_size.json (experiments/route_ensemble_analysis.py)."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style as st  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

OURS, ENS, MAP = "#E03131", "#7048E8", "#5C6B7A"
NS = (8, 16, 32, 64, 128, 256, 512, 1024)


def main():
    st.setup()
    R = json.load(open(st.ROOT / "results" / "route_ensemble_size.json", encoding="utf-8"))["test"]
    solves = np.array([2 * n for n in NS])
    cx = R["worst_regret"]["route_solves"]
    fig = plt.figure(figsize=(st.TEXTW, 66 * st.MM))
    axa = fig.add_axes([0.09, 0.22, 0.37, 0.72])
    axb = fig.add_axes([0.595, 0.22, 0.37, 0.72])

    exp_loss = [R[f"expected_{n}"]["loss"] for n in NS]
    axa.axhline(R["map"]["loss"], color=MAP, lw=1.6, ls=(0, (2, 2)))
    axa.text(2900, R["map"]["loss"] + 0.04, "基线：按粗图选边", color=MAP, fontsize=8.2, ha="right")
    axa.plot(solves, exp_loss, color=ENS, lw=2.2, marker="o", ms=4.5)
    axa.text(150, 1.40, "集合平均选边\n（n 个集合成员）", color=ENS, fontsize=8.2, ha="left", va="center")
    axa.plot([cx], [R["worst_regret"]["loss"]], color=OURS, marker="D", ms=7, ls="none")
    axa.text(cx * 0.92, R["worst_regret"]["loss"] - 0.13, "选最大后悔值较小的一侧（本文）", color=OURS, fontsize=8.2, ha="left")
    axa.set_xscale("log", base=2)
    axa.set_xticks(solves)
    axa.set_xticklabels([str(s) for s in solves])
    axa.set_xlim(12, 2900)
    axa.set_ylim(0.4, 1.8)
    axa.set_xlabel("每个任务的航线求解次数")
    axa.set_ylabel("平均额外航时（小时）")

    flip = [100 * R["top20_loss_share"][f"flip_share_{n}"] for n in NS]
    expr = [100 * R["top20_loss_share"][f"expected_regret_{n}"] for n in NS]
    axb.plot(solves, expr, color=ENS, lw=2.2, marker="o", ms=4.5)
    axb.plot(solves, flip, color=ENS, lw=2.2, marker="o", ms=4.5, ls=(0, (3, 2)), mfc="white")
    axb.axhline(100 * R["top20_loss_share"]["map_margin"], color=MAP, lw=1.6, ls=(0, (2, 2)))
    axb.plot([cx], [100 * R["top20_loss_share"]["worst_regret"]], color=OURS, marker="D", ms=7, ls="none")
    axb.text(2900, expr[-1] + 4.0, "后悔值的集合平均", color=ENS, fontsize=8.2, ha="right")
    axb.text(2900, max(flip[-2:]) + 4.5, "改变选边的成员比例", color=ENS, fontsize=8.2, ha="right")
    axb.text(2900, 100 * R["top20_loss_share"]["map_margin"] - 5.5, "粗图左右航时差", color=MAP, fontsize=8.2, ha="right")
    axb.text(14, 72.5, "最大后悔值（本文）", color=OURS, fontsize=8.2, ha="left")
    axb.set_xscale("log", base=2)
    axb.set_xticks(solves)
    axb.set_xticklabels([str(s) for s in solves])
    axb.set_xlim(12, 2900)
    axb.set_ylim(20, 80)
    axb.set_xlabel("每个任务的航线求解次数")
    axb.set_ylabel("风险排前 20% 的任务所占额外航时（%）")
    for ax in (axa, axb):
        ax.tick_params(axis="x", labelsize=7.2)
        for s_ in ("top", "right"):
            ax.spines[s_].set_visible(True)
    st.caption(axa, "(a) 选哪一侧", y=-0.22)
    st.caption(axb, "(b) 哪些任务危险", y=-0.22)
    st.save(fig, "fig_route_budget")
    print("expected-time loss", dict(zip(NS, np.round(exp_loss, 2))), "search", round(R["worst_regret"]["loss"], 2), "at", round(cx, 1))


if __name__ == "__main__":
    main()
