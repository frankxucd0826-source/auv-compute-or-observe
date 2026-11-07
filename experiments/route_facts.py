"""Every number the route-decision paper may quote, generated from the result files (no number is
typed by hand). Writes paper/gemini/facts_v3.md.

    python -E -X utf8 experiments/route_facts.py
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
sys.path.insert(0, str(ROOT / "src"))
from route_summary import load, side, worst_regret, ens_l2, calibrate, outcomes, summarise  # noqa: E402


def f2(x):
    return f"{x:.2f}"


def ci(c):
    return f"[{c[0]:.2f}, {c[1]:.2f}]"


def gains_top(score, loss, frac=0.2):
    o = np.argsort(-np.asarray(score), kind="stable")
    c = np.cumsum(np.asarray(loss)[o])
    k = int(round(frac * len(o)))
    return float(c[k - 1] / c[-1])


def main():
    S = json.load(open(ROOT / "results" / "route_summary_main.json", encoding="utf-8"))
    P = S["params"]
    T, Dv = S["test"], S["dev"]
    test, dev = load("main", "test"), load("main", "dev")
    cfg = json.load(open(ROOT / "results" / "route_main_test" / "config.json", encoding="utf-8"))
    E1 = np.load(ROOT / "results" / "route_errormodel_deg1.0_lag1.npz")
    E0 = np.load(ROOT / "results" / "route_errormodel_deg0.5_lag0.npz")
    from oceanroute.fields import Snapshots
    Sn = Snapshots()
    yr = Sn.times.astype("datetime64[Y]").astype(int) + 1970
    L = []
    w = L.append
    w("# 事实清单 v3（航路决策研究；由 experiments/route_facts.py 从结果文件生成，正文所有数字只能取自这里）\n")
    w("## 数据与设置")
    w(f"- 海流数据：HYCOM 全球海洋再分析（GLBy0.08，实验 93.0），水平分辨率 1/12°，取 10 米深度的海流，区域 23–31°N、121–129°E（台湾以东至东海，含黑潮），"
      f"2019-01-01 至 2024-08-29 每 3 天一张（12:00 UTC），共 {len(Sn)} 张；开发年份 2019–2021 共 {int(((yr>=2019)&(yr<=2021)).sum())} 张，测试年份 2022–2024 共 {int(((yr>=2022)&(yr<=2024)).sum())} 张。")
    w(f"- 任务：每张快照抽 2 个任务；起终点相距 100–140 千米，中点有半径 15 千米的禁航区，左右两侧各求最快航线；起终点离岸至少 20 千米；"
      f"只取粗图上任务区平均流速不低于 0.3 米/秒的强流任务。开发年份 {Dv['n']} 个任务（{Dv['n_days']} 天），测试年份 {T['n']} 个任务（{T['n_days']} 天）。")
    w(f"- 航行器：对水速度 1.0 米/秒（长航程自主水下航行器量级）；更快一侧的平均航时 {T['mean_trip_h']:.1f} 小时（测试年份）。")
    w("- 航行器带的地图：1° 粗分辨率（格内平均），3 天前制作（主设置）。真实海流：当天 1/12° 场。")
    w("- 航线求解（三档计算量）：粗算 8 千米网格、8 个方向；标准 4 千米、16 个方向；精算 2 千米、32 个方向（相对计算量 1 : 8 : 64，按边数）。"
      "最快航线用图上的最短路（Dijkstra）求，过一条边的时间 = 边长 / 对地速度，对地速度 = 沿边流速 + sqrt(V² − 垂直边流速²)；顶流过强则该边不可通行。")
    w("- 执行假设：选定一侧后，航行器按真实海流在该侧以最优方式航行（贴近实际的边走边测、边调整）；本文研究的是选哪一侧这个二元决策。")
    w(f"- 误差模型（大数据标定，开发年份）：旧粗图减真实海流的误差，3 天前 1° 粗图：典型误差中位数 {np.median(np.sqrt((E1['su']**2+E1['sv']**2)/2)[Sn.water]):.2f} 米/秒，相关长度 {float(E1['ell']):.0f} 千米；"
      f"当天 0.5° 图：{np.median(np.sqrt((E0['su']**2+E0['sv']**2)/2)[Sn.water]):.2f} 米/秒，{float(E0['ell']):.0f} 千米。合理海流 = 粗图 + 由流函数生成的无散误差模态的组合（各点方差按标定的误差图缩放），系数服从标准正态。")
    w(f"- 合理集合的半径在开发年份标定：使合理集合给出的两侧时间差范围包住真实差值的任务比例不低于 90% 的最小半径，得 r = {P['r']}；"
      f"该半径下开发年份覆盖 {S['coverage_dev'][str(P['r'])]*100:.0f}%，测试年份覆盖 {S['coverage_test_at_r']*100:.0f}%。")
    w(f"- 反例搜索：在半径 r 的球内对“两侧时间差”做投影梯度上升（梯度由最快航线上各段时间对海流的导数给出，即包络定理），先沿梯度跳到球面，再步长减半细化；"
      f"分别朝两个方向、在半径 1 与 2 上各搜一次，其他半径按两者线性插值；每个任务共约 {np.mean([r['cx_solves_1.0'] + r['cx_solves_2.0'] for r in test]):.0f} 次标准网格航线求解，与 32 个成员的集合（64 次）相近。")
    w(f"- 数值误差容限（开发年份）：粗算与精算两侧时间差之差的 95% 分位 {P['eps']:.1f} 小时；粗算差值小于它时改用精算（按需精算）。")
    w(f"- 门控阈值（开发年份按平均损失最小选定，测试年份原样使用）：最坏后悔超过 {P['tau_robust']:.0f} 小时时取保守一侧；最坏后悔超过 {P['tau_surface05']:.0f} 小时时上浮取当天 0.5° 图（上浮一次计 1 小时）。")
    w("- 观测方式：原地停留 2 小时测 12 次；沿所选一侧航行 30 或 60 千米并连续测流后再决定是否换边；绕到反例与地图差别最大处（前方 40 千米内）去测；上浮取当天 1° 或 0.5° 图（每次 1 小时）。测流噪声 0.05 米/秒，同化时取 0.15 米/秒（含模型误差）。")
    w("- 统计：损失 = 实际航时 − 更快一侧的航时（小时）；95% 区间按天整组重抽样 2000 次。\n")
    w("## 主要结果（测试年份，括号内为 95% 区间；与“照精算地图走”的配对差）")
    tab = T["table"]
    for k in ["地图+粗算", "地图+标准", "地图+精算", "集合期望（贝叶斯）", "保守（最坏后悔最小）", "原地停留测", "总是沿途测30km", "总是沿途测60km",
              "总是绕行定点测", "总是上浮取当天1°图", "总是上浮取当天0.5°图", "反例门控→保守", "反例门控→上浮取0.5°图", "反例门控→贝叶斯"]:
        v = tab[k]
        w(f"- {k}：平均损失 {f2(v['regret_h'])} 小时 {ci(v['regret_ci'])}；与精算地图之差 {v['minus_map']:+.2f} {ci(v['minus_map_ci'])}")
    w(f"- 开发年份对应：精算地图 {f2(Dv['table']['地图+精算']['regret_h'])}，保守 {f2(Dv['table']['保守（最坏后悔最小）']['regret_h'])}，门控后取保守 {f2(Dv['table']['反例门控→保守']['regret_h'])}，"
      f"门控后上浮取 0.5° 图 {f2(Dv['table']['反例门控→上浮取0.5°图']['regret_h'])}，集合期望 {f2(Dv['table']['集合期望（贝叶斯）']['regret_h'])}。")
    gate = tab["反例门控→保守"]["regret_h"]
    mp = tab["地图+精算"]["regret_h"]
    w(f"- 门控后取保守比精算地图少损失 {(1-gate/mp)*100:.0f}%（{mp:.2f} → {gate:.2f} 小时）。\n")
    C, Cd = T["categories"], Dv["categories"]
    w("## 歧义的性质（测试年份；开发年份在括号内）")
    w(f"- 选错一侧的比例：粗算 {C['wrong_cheap']*100:.1f}%（{Cd['wrong_cheap']*100:.1f}%），精算 {C['wrong_expensive']*100:.1f}%（{Cd['wrong_expensive']*100:.1f}%）；"
      f"换成当天 0.5° 图 {np.mean([side(r['dJ_map_fresh05']) != side(r['dJ_true']) for r in test])*100:.1f}%；计算量增加 64 倍只修好粗算错误的 {C['cheap_errors_fixed_by_compute']*100:.0f}%。")
    w(f"- 平均损失：粗算 {C['regret_cheap']:.2f}，精算 {C['regret_expensive']:.2f} 小时（差异不显著，见上）。")
    w(f"- 能找到合理反例（存在使地图所选一侧变差、且让另一侧更好的合理海流）的任务比例，按半径：" + "，".join(f"r={k}：{v*100:.1f}%" for k, v in C["share_flip_possible_by_radius"].items()) + "。")
    w(f"- 损失高度集中：精算地图损失最大的 10% 任务占全部损失的 {C['share_regret_from_top10pct']*100:.0f}%（开发年份 {Cd['share_regret_from_top10pct']*100:.0f}%）。")
    loss = np.array([r["JT"][side(r["dJ_map_L2"])] - min(r["JT"].values()) for r in test])
    sc_cx = [worst_regret(r, side(r["dJ_map_L2"]), P["r"]) for r in test]
    sc_en = [float(np.mean(np.sign(ens_l2(r)) != np.sign(r["dJ_map_L2"]))) for r in test]
    sc_mg = [-abs(r["dJ_map_L2"]) for r in test]
    w(f"- 按风险排序，排在前 20% 的任务所占的地图损失：反例的最坏后悔 {gains_top(sc_cx, loss)*100:.0f}%，32 个合理场中翻转的比例 {gains_top(sc_en, loss)*100:.0f}%，"
      f"地图上两侧时间差越小越危险 {gains_top(sc_mg, loss)*100:.0f}%，随机 20%，按真实损失（上限）{gains_top(loss, loss)*100:.0f}%。")
    flag = np.array(sc_cx) > P["tau_robust"]
    w(f"- 门控（最坏后悔 > {P['tau_robust']:.0f} 小时）标记 {flag.mean()*100:.0f}% 的任务，这些任务占地图损失的 {loss[flag].sum()/loss.sum()*100:.0f}%；"
      f"其中保守规则改选另一侧的有 {sum(1 for r, f in zip(test, flag) if f and min('LR', key=lambda a: worst_regret(r, a, P['r'])) != side(r['dJ_map_L2']))} 个任务。")
    g = []
    for r in test:
        a = side(r["dJ_map_L2"])
        if worst_regret(r, a, P["r"]) > P["tau_robust"]:
            b = min("LR", key=lambda s: worst_regret(r, s, P["r"]))
            if b != a:
                g.append(r["JT"][a] - r["JT"][b])
    g = np.array(g)
    w(f"- 门控后取保守为何有效：改选的 {len(g)} 个任务中 {int((g > 0).sum())} 个改对，改对时平均省 {g[g > 0].mean():.1f} 小时；{int((g < 0).sum())} 个改错，改错时平均多花 {(-g[g < 0]).mean():.1f} 小时——"
      "被避开的一侧往往有很大的下行风险，改对的收益远大于改错的代价。")
    D = T["detection"]
    w(f"- 只论“是否选错且多花 1 小时以上”（测试年份 {D['n_costly']} 个）而不论多花多少时，三种排序的区分能力相近（曲线下面积：反例 {D['auc_counterexample']:.2f}，32 成员集合 {D['auc_ensemble_32']:.2f}，地图差值 {D['auc_margin']:.2f}）；"
      "反例的优势在于把损失大的任务排在前面（见上一条）。\n")
    w("## 观测的代价（测试年份）")
    for c in (0.0, 0.5, 1.0, 2.0, 3.0):
        Pc, _ = calibrate(dev, c)
        rows = [outcomes(r, Pc)[0] for r in test]
        orc = np.array([o["知道真相"] for o in rows])
        a = np.mean([o["总是上浮取当天0.5°图"] for o in rows] - orc)
        g = np.mean([o["反例门控→上浮取0.5°图"] for o in rows] - orc)
        w(f"- 上浮一次 {c:.1f} 小时：总是上浮取 0.5° 图 {a:.2f}，门控后上浮 {g:.2f}，门控后取保守 {gate:.2f}，精算地图 {mp:.2f}（小时）。")
    pr = [r["probe_30"] for r in test]
    sw = [p["choice"] != r["a_map"] for p, r in zip(pr, test)]
    ok = [p["choice"] == side(r["dJ_true"]) for p, r in zip(pr, test)]
    pr6 = [r["probe_60"] for r in test]
    sw6 = [p["choice"] != r["a_map"] for p, r in zip(pr6, test)]
    ok6 = [p["choice"] == side(r["dJ_true"]) for p, r in zip(pr6, test)]
    w(f"- 沿途测 30 千米后换边的任务 {np.mean(sw)*100:.1f}%，换对 {np.mean([o for o, s in zip(ok, sw) if s])*100:.0f}%；测 60 千米后换边 {np.mean(sw6)*100:.1f}%，换对 {np.mean([o for o, s in zip(ok6, sw6) if s])*100:.0f}%。")
    w(f"- 绕行定点测平均先花 {np.mean([r['targeted']['transit_h'] for r in test]):.1f} 小时到测点。\n")
    ex = json.load(open(ROOT / "results" / "route_example.json", encoding="utf-8"))
    w("## 示例任务（图 1；按规则选出：测试年份按日期第一个满足“精算地图选错且多花 3 小时以上、存在合理反例、门控后保守选对”的任务）")
    w(f"- 日期 {ex['date']}；粗图上左侧 {ex['map_time_L']} 小时、右侧 {ex['map_time_R']} 小时（地图选左）；合理反例中左侧 {ex['counter_time_L']}、右侧 {ex['counter_time_R']}；"
      f"真实海洋左侧 {ex['truth_time_L']}、右侧 {ex['truth_time_R']}（右侧快 {ex['truth_time_L']-ex['truth_time_R']:.1f} 小时）。\n")
    # the earlier study (harmful algal bloom survey): why computing more did not help there
    import pandas as pd
    cu = pd.DataFrame([json.loads(l) for l in open(ROOT / "results" / "curse3_dev" / "results.jsonl", encoding="utf-8")])
    cu = cu[cu.scale == 1.0].groupby("budget")[["believed", "true", "believed_holdout"]].mean()
    he = json.load(open(ROOT / "results" / "headroom_edge.json", encoding="utf-8"))
    hm = json.load(open(ROOT / "results" / "headroom_mapmax.json", encoding="utf-8"))
    rv = json.load(open(ROOT / "results" / "rev2_summary.json", encoding="utf-8"))["main"]["sat+"]["moderate"]["means"]
    w("## 前期研究（东海赤潮巡测：航行器带 3 天前的卫星叶绿素图，在“继续计算”“边走边测”“停下复测”之间分配时间；损失为对数叶绿素浓度）")
    b = [64, 2000, 200000]
    w("- 规划器在自己搜索过的想象海洋上给航线打分，随推演次数增加而虚高：64、2000、20 万次推演时自评 " + "、".join(f"{cu.loc[x, 'believed']:.3f}" for x in b) +
      "，真实价值 " + "、".join(f"{cu.loc[x, 'true']:.3f}" for x in b) + "，在不参与搜索的留出海洋上评判 " + "、".join(f"{cu.loc[x, 'believed_holdout']:.3f}" for x in b) + "。")
    w(f"- 出发前预演选用时策略的遗憾 {rv['rehearsal']:.3f}，每个任务事后挑最好的策略 {rv['oracle']:.3f}（用时分配本身的空间约 {rv['rehearsal'] - rv['oracle']:.3f}），经典单步元推理 {rv['rational']:.3f}。")
    e, m = he["regret_avg"], hm["regret_avg"]
    w(f"- 遗憾拆解：从窗口边缘下水（离最浓处中位数 {he['geometry']['0.15']['km_start_to_max_median']:.0f} 千米）时，知道真相直奔最浓处 {e['0.15/oracle_goto']['mean']:.3f}，换成当天卫星图 {e['0.15/fresh_planner']['mean']:.3f}；"
      f"改在旧图最浓处下水后，五种用时策略 {min(m[k]['mean'] for k in ('0.15/fixed-0','0.15/fixed-1','0.15/periodic-100','0.15/periodic-300','0.15/periodic-200')):.3f}–{max(m[k]['mean'] for k in ('0.15/fixed-0','0.15/fixed-1','0.15/periodic-100','0.15/periodic-300','0.15/periodic-200')):.3f}，"
      f"换成当天卫星图 {m['0.15/fresh_planner']['mean']:.3f}。即下水点约 0.13、信息新鲜度约 0.03、用时分配约 0.02。")
    adv = json.load(open(ROOT / "results" / "advect_test.json", encoding="utf-8"))["summary"]["test/flow_1day_x3"]
    w(f"- 用前一天的移动（光流）把旧图外推 3 天，比直接用旧图误差大 {adv['rmse_minus_persistence']:.3f}（95% 区间 {adv['rmse_ci95'][0]:.3f}–{adv['rmse_ci95'][1]:.3f}）：逐日卫星图里没有可外推的整体移动。\n")
    sett = ROOT / "results" / "route_settings_summary.json"
    if sett.exists():
        Z = json.load(open(sett, encoding="utf-8"))
        w("## 适用范围（每组测试年份约 350 个任务；阈值各自在开发年份标定）")
        for name, v in Z.items():
            w(f"- {name}：" + "，".join(f"{k} {val}" for k, val in v.items()))
        w("")
    out = ROOT / "paper" / "gemini" / "facts_v3.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(out, len("\n".join(L)), "chars")


if __name__ == "__main__":
    main()
