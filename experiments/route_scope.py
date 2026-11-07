"""Table 2: how the findings change with the map, the vehicle, the plausible set and the region. For every
setting the thresholds and the radius are set on its own development missions and applied to its test
missions (the Gulf Stream runs use OCEANROUTE_REGION=gulfstream).

    python -E -X utf8 experiments/route_scope.py -> results/route_settings_summary.json, paper/tables/route_scope.tex
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
from route_summary import load, calibrate, summarise, side, worst_regret  # noqa: E402

SETTINGS = [("main", "黑潮主设置"), ("fresh05", "粗图换成当天0.5°图"),
            ("slow", "航速降至0.75米/秒"), ("analog", "消融：合理集合改用相似日差值"),
            ("gulf", "湾流"),
            ("agulhas", "阿古拉斯回流区"),
            ("altimetry", "改带卫星测高地转流图")]


def top20(recs, P):
    loss = np.array([r["JT"][side(r["dJ_map_L2"])] - min(r["JT"].values()) for r in recs])
    sc = np.array([worst_regret(r, side(r["dJ_map_L2"]), P["r"]) for r in recs])
    o = np.argsort(-sc, kind="stable")
    c = np.cumsum(loss[o])
    return float(c[int(round(0.2 * len(o))) - 1] / c[-1]) if c[-1] > 0 else float("nan")


def main():
    out, rows = {}, []
    for tag, name in SETTINGS:
        if not (ROOT / "results" / f"route_{tag}_test" / "done").exists():
            continue
        dev, test = load(tag, "dev"), load(tag, "test")
        P, cover = calibrate(dev, 1.0)
        T = summarise(test, P)
        t = T["table"]
        C = T["categories"]
        rec = {"测试任务": T["n"], "标定半径": P["r"],
               "精算地图选错": f"{C['wrong_expensive']*100:.1f}%", "粗算选错": f"{C['wrong_cheap']*100:.1f}%",
               "精算地图损失": f"{t['地图+精算']['regret_h']:.2f}",
               "门控后取保守": f"{t['反例门控→保守']['regret_h']:.2f}",
               "门控后取保守与地图之差": f"{t['反例门控→保守']['minus_map']:+.2f} [{t['反例门控→保守']['minus_map_ci'][0]:.2f}, {t['反例门控→保守']['minus_map_ci'][1]:.2f}]",
               "门控后上浮取图": f"{t['反例门控→上浮取0.5°图']['regret_h']:.2f}",
               "存在合理反例": f"{max(C['share_flip_possible_by_radius'].get(str(P['r']), 0), 0)*100:.1f}%" if str(P['r']) in C['share_flip_possible_by_radius']
               else f"{np.mean([worst_regret(r, side(r['dJ_map_L2']), P['r']) > 0 for r in test])*100:.1f}%",
               "反例前20%所占损失": f"{top20(test, P)*100:.0f}%",
               "平均最快航时": f"{T['mean_trip_h']:.1f}"}
        out[name] = rec
        rows.append((name, rec))
    json.dump(out, open(ROOT / "results" / "route_settings_summary.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    C = r">{\centering\arraybackslash}p{0.088\linewidth}"
    lines = [r"\begin{tabular}{@{}p{0.19\linewidth}" + C * 7 + "@{}}", r"\toprule",
             r"设置 & 测试任务 & 存在合理反例 & 基线选错率 & 基线额外航时 & 超阈值时保守改选 & 超阈值时上浮取图 & 最大后悔值前20\%所占额外航时 \\",
             r"\midrule"]
    for name, r in rows:
        lines.append(f"{name} & {r['测试任务']} & {r['存在合理反例'].replace('%', chr(92) + '%')} & {r['精算地图选错'].replace('%', chr(92) + '%')} & "
                     f"{r['精算地图损失']} & {r['门控后取保守']} & {r['门控后上浮取图']} & {r['反例前20%所占损失'].replace('%', chr(92) + '%')} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (ROOT / "paper" / "tables" / "route_scope.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    for name, r in rows:
        print(name, r)


if __name__ == "__main__":
    main()
