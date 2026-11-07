"""Fig.: the counterexample finds where the losses are, and decides when an observation is worth it.
(a) Missions ranked by a risk score, most risky first; the curve shows how much of the map's total
    loss (test years) the top fraction of missions holds: ideal (ranked by the real loss), the worst
    plausible regret found by the counterexample search (this paper), the flip share of a 32-member
    ensemble, the closeness of the two sides on the map, and random order.
(b) Mean loss against the time one surfacing costs: always surface for today's 0.5-degree map,
    surface only when the counterexample's worst regret exceeds a threshold set on the development
    years, the map alone, and the conservative choice on flagged missions (no surfacing)."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style as st  # noqa: E402

sys.path.insert(0, str(st.ROOT / "experiments"))
from route_summary import load, side, worst_regret, ens_l2, calibrate, outcomes  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

OURS, ENS, MARGIN, IDEAL, RANDOM = "#E03131", "#7048E8", "#1C7ED6", "#1F2A36", "#ADB5BD"
SURF, ROB, MAP = "#0B7285", "#E03131", "#5C6B7A"


def gains(score, loss):
    o = np.argsort(-np.asarray(score), kind="stable")
    c = np.cumsum(np.asarray(loss)[o])
    return np.r_[0, np.arange(1, len(o) + 1) / len(o)], np.r_[0, c / c[-1]]


def main():
    st.setup()
    test, dev = load("main", "test"), load("main", "dev")
    P = json.load(open(st.ROOT / "results" / "route_summary_main.json", encoding="utf-8"))["params"]
    loss = np.array([r["JT"][side(r["dJ_map_L2"])] - min(r["JT"].values()) for r in test])
    scores = {
        "按真实额外航时排序（上限）": (loss, IDEAL, "-"),
        "最大后悔值（本文）": ([worst_regret(r, side(r["dJ_map_L2"]), P["r"]) for r in test], OURS, "-"),
        "32 个集合成员中改变选边的比例": ([float(np.mean(np.sign(ens_l2(r)) != np.sign(r["dJ_map_L2"]))) for r in test], ENS, "-"),
        "粗图左右航时差越小越危险": ([-abs(r["dJ_map_L2"]) for r in test], MARGIN, "-"),
    }
    fig = plt.figure(figsize=(st.TEXTW, 66 * st.MM))
    axa = fig.add_axes([0.09, 0.22, 0.37, 0.72])
    axb = fig.add_axes([0.595, 0.22, 0.37, 0.72])
    axa.plot([0, 100], [0, 100], color=RANDOM, lw=1.6, ls=(0, (3, 2)))
    for name, (sc, col, ls) in scores.items():
        x, y = gains(sc, loss)
        axa.plot(x * 100, y * 100, color=col, lw=2.4 if col != IDEAL else 1.6, ls=ls)
    axa.axvline(20, color=st.MUTED, lw=0.9, ls=(0, (2, 2)))
    axa.text(98, 34, "排在前 20% 的任务所占额外航时", color=st.INK, fontsize=8.2, ha="right")
    short = {"按真实额外航时排序（上限）": "按真实额外航时（上限）", "最大后悔值（本文）": "最大后悔值（本文）",
             "32 个集合成员中改变选边的比例": "改变选边的成员比例", "粗图左右航时差越小越危险": "粗图左右航时差越小越危险"}
    yy = 27
    for name, (sc, col, ls) in scores.items():
        x, y = gains(sc, loss)
        v = float(np.interp(0.2, x, y)) * 100
        axa.text(98, yy, f"{short[name]}  {v:.0f}%", color=col, fontsize=8.0, ha="right")
        yy -= 6.2
    axa.text(98, yy, "随机排序  20%", color="#868E96", fontsize=8.0, ha="right")
    axa.set_xlim(0, 100)
    axa.set_ylim(0, 102)
    axa.set_xlabel("按风险从高到低排在前面的任务（%）")
    axa.set_ylabel("这些任务占基线总额外航时（%）")
    costs = [0.0, 0.5, 1.0, 2.0, 3.0, 4.0]
    lines = {"总是上浮取当天 0.5° 图": [], "超阈值时上浮取图（本文）": [], "超阈值时保守改选（本文）": [], "基线：按粗图选边": []}
    for c in costs:
        Pc, _ = calibrate(dev, c)
        rows = [outcomes(r, Pc)[0] for r in test]
        orc = np.array([o["知道真相"] for o in rows])
        lines["总是上浮取当天 0.5° 图"].append(np.mean([o["总是上浮取当天0.5°图"] for o in rows] - orc))
        lines["超阈值时上浮取图（本文）"].append(np.mean([o["反例门控→上浮取0.5°图"] for o in rows] - orc))
        lines["超阈值时保守改选（本文）"].append(np.mean([o["反例门控→保守"] for o in rows] - orc))
        lines["基线：按粗图选边"].append(np.mean([o["地图+精算"] for o in rows] - orc))
    style = {"总是上浮取当天 0.5° 图": (SURF, (0, (4, 2)), "o"), "超阈值时上浮取图（本文）": (SURF, "-", "s"),
             "超阈值时保守改选（本文）": (ROB, "-", "D"), "基线：按粗图选边": (MAP, (0, (2, 2)), None)}
    for name, vals in lines.items():
        col, ls, mk = style[name]
        axb.plot(costs, vals, color=col, lw=2.2, ls=ls, marker=mk, ms=5)
    axb.text(0.78, 1.45, "总是上浮取图", color=SURF, fontsize=8.2, ha="left")
    axb.text(2.0, 0.40, "超阈值时上浮取图（本文）", color=SURF, fontsize=8.2, ha="center")
    axb.text(3.1, 0.58, "超阈值时保守改选（本文）", color=ROB, fontsize=8.2, ha="center")
    axb.text(3.3, 1.11, "基线：按粗图选边", color=MAP, fontsize=8.2, ha="center")
    axb.set_xlabel("一次上浮取图的代价（小时）")
    axb.set_ylabel("平均额外航时（小时）")
    axb.set_xlim(-0.1, 4.1)
    axb.set_ylim(0, 1.65)
    for ax in (axa, axb):
        for s_ in ("top", "right"):
            ax.spines[s_].set_visible(True)
    st.caption(axa, "(a) 谁该被标为高风险", y=-0.22)
    st.caption(axb, "(b) 观测代价与阈值判据", y=-0.22)
    st.save(fig, "fig_route_risk")
    print({k: [round(v, 3) for v in vals] for k, vals in lines.items()})


if __name__ == "__main__":
    main()
