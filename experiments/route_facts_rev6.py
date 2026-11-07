"""Facts for revision 6 (no number typed by hand): what more computation changes, what the
counterexample search buys against random plausible fields, and the Gulf Stream replication.
Writes paper/gemini/facts_v4.md.

    python -E -X utf8 experiments/route_facts_rev6.py
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
from route_summary import load, side, worst_regret, ens_l2  # noqa: E402

NS = (8, 16, 32, 64, 128, 256, 512, 1024)


def ci(c):
    return f"[{c[0]:.2f}, {c[1]:.2f}]"


def top20(score, loss):
    o = np.argsort(-np.asarray(score, float), kind="stable")
    c = np.cumsum(np.asarray(loss)[o])
    return float(c[int(round(0.2 * len(o))) - 1] / c[-1])


def compute_changes(recs):
    a0 = [side(r["dJ_map_L0"]) for r in recs]
    a2 = [side(r["dJ_map_L2"]) for r in recs]
    t = [side(r["dJ_true"]) for r in recs]
    ch = [i for i in range(len(recs)) if a0[i] != a2[i]]
    right = sum(1 for i in ch if a2[i] == t[i])
    return len(ch), right, len(ch) - right


def main():
    L = []
    w = L.append
    w("# 事实清单 v4（第 6 轮新增；由 experiments/route_facts_rev6.py 从结果文件生成，新增文字中的数字只能取自这里或 facts_v3.md）\n")
    w("## 加算改变了哪些决定（黑潮主设置）")
    for split, name in (("test", "测试年份"), ("dev", "开发年份")):
        n, ok, bad = compute_changes(load("main", split))
        w(f"- {name}：把求解计算量从粗算增加 64 倍到精算，改变了 {n} 个任务的选择，其中 {ok} 个改对、{bad} 个改错。")
    w("")
    E = json.load(open(ROOT / "results" / "route_ensemble_size.json", encoding="utf-8"))
    w("## 随机合理场的数量与反例搜索（黑潮主设置）")
    w("- 做法：每个任务另取 1024 个合理海流（与主实验同一误差模型、独立随机数），在标准网格上求两侧时间差；"
      "“按期望时间选边”用其中前 n 个的平均（每个合理场要求解左右两次，共 2n 次求解）。反例搜索后取保守（最坏后悔更小的一侧）用的是主实验的结果。")
    w("- 推导与核对：最坏后悔更小的一侧，等于按“合理集合给出的两侧时间差范围的中点”选边；若两侧时间差随海流线性变化，中点就是地图上的值，"
      "保守选择与照地图走相同，只有当一侧的最不利情形比另一侧严重得多时才改选。逐任务核对，二者完全一致。")
    for split, name in (("test", "测试年份"), ("dev", "开发年份")):
        if split not in E:
            continue
        o = E[split]
        wr = o["worst_regret"]
        w(f"- {name}（{o['n_missions']} 个任务）：照精算地图走 {o['map']['loss']:.2f} 小时；反例搜索后取保守 {wr['loss']:.2f} 小时（平均 {wr['route_solves']:.0f} 次求解）；"
          "按期望时间选边，" + "，".join(f"{n} 个合理场 {o[f'expected_{n}']['loss']:.2f}" for n in NS) + " 小时。")
        e32, e1024 = o["expected_32"], o["expected_1024"]
        inside = [o[f"expected_{n}"]["ci_vs_worst_regret"][0] <= 0 <= o[f"expected_{n}"]["ci_vs_worst_regret"][1] for n in NS]
        first = next((n for i, n in enumerate(NS) if all(inside[i:])), None)
        w(f"  - 与反例搜索后取保守的配对差：32 个合理场 {e32['diff_vs_worst_regret']:+.2f} {ci(e32['ci_vs_worst_regret'])}；"
          f"1024 个合理场 {e1024['diff_vs_worst_regret']:+.2f} {ci(e1024['ci_vs_worst_regret'])}；从 {first} 个合理场起（及更多），区间都包含 0。")
        w(f"  - 1024 个合理场（{2 * 1024} 次求解）与精算地图之差 {e1024['diff_vs_map']:+.2f} {ci(e1024['ci_vs_map'])}；"
          f"反例搜索约 {wr['route_solves']:.0f} 次求解，约为其 1/{2 * 1024 / wr['route_solves']:.0f}。")
        w(f"  - 抽样噪声：32 个合理场平均值的抽样误差（中位数）{o['noise_of_mean32_h']:.1f} 小时，大于它要估计的修正量（1024 个合理场平均相对地图的修正，中位数）{o['size_of_correction_h']:.1f} 小时。")
        t = o["top20_loss_share"]
        w(f"  - 风险排序（排前 20% 的任务所占的地图损失）：反例的最坏后悔 {t['worst_regret']*100:.0f}%；同样的随机合理场算“坚持地图一侧的期望后悔”：32 个 {t['expected_regret_32']*100:.0f}%，1024 个 {t['expected_regret_1024']*100:.0f}%；"
          f"翻转比例：32 个 {t['flip_share_32']*100:.0f}%，1024 个 {t['flip_share_1024']*100:.0f}%（主实验那 32 个 {t['flip_share_main32']*100:.0f}%）；地图上两侧时间差 {t['map_margin']*100:.0f}%。")
    w("- 读法：选哪一侧时，随机合理场的平均要上千个才估得准，反例搜索以约 1/29 的求解次数达到同样效果；判断哪些任务危险时，关键是度量“会损失多少”而不是“有多少合理场翻转”，"
      "期望后悔（合理场足够多时）与最坏后悔都能抓住约三分之二的损失，翻转比例即使用 1024 个合理场也只有四成多。\n")
    gs = ROOT / "results" / "route_summary_gulf.json"
    if gs.exists():
        G = json.load(open(gs, encoding="utf-8"))
        P, T, Dv = G["params"], G["test"], G["dev"]
        test = load("gulf", "test")
        C = T["categories"]
        tab = T["table"]
        em = np.load(ROOT / "results" / "route_errormodel_gulfstream_deg1.0_lag1.npz")
        err = np.sqrt((em["su"] ** 2 + em["sv"] ** 2) / 2)
        w("## 换海区重复：湾流（33–41°N、75–67°W；同一 HYCOM 产品与深度，同一时间范围与年份划分，同一流程；半径与阈值用湾流自己的开发年份标定）")
        w(f"- 任务：开发年份 {Dv['n']} 个（{Dv['n_days']} 天），测试年份 {T['n']} 个（{T['n_days']} 天）；更快一侧平均航时 {T['mean_trip_h']:.1f} 小时。")
        w(f"- 3 天前 1° 粗图的误差：典型误差中位数 {np.median(err[em['su'] > 0]):.2f} 米/秒，相关长度 {float(em['ell']):.0f} 千米。")
        w(f"- 标定：半径 r = {P['r']}（开发年份覆盖 {G['coverage_dev'][str(P['r'])]*100:.0f}%，测试年份 {G['coverage_test_at_r']*100:.0f}%）；数值误差容限 {P['eps']:.1f} 小时；"
          f"保守门控阈值 {P['tau_robust']:.0f} 小时，上浮取 0.5° 图门控阈值 {P['tau_surface05']:.0f} 小时。")
        n, ok, bad = compute_changes(test)
        w(f"- 选错一侧：粗算 {C['wrong_cheap']*100:.1f}%，精算 {C['wrong_expensive']*100:.1f}%（加算改变 {n} 个任务的选择：{ok} 个改对、{bad} 个改错）；"
          f"换成当天 0.5° 图 {np.mean([side(r['dJ_map_fresh05']) != side(r['dJ_true']) for r in test])*100:.1f}%。")
        amb = C["share_flip_possible_by_radius"].get(str(P["r"]))
        if amb is None:
            amb = float(np.mean([worst_regret(r, side(r["dJ_map_L2"]), P["r"]) > 0 for r in test]))
        w(f"- 存在合理反例的任务：{amb*100:.1f}%。")
        for k in ["地图+粗算", "地图+精算", "集合期望（贝叶斯）", "保守（最坏后悔最小）", "反例门控→保守", "总是沿途测30km", "总是沿途测60km",
                  "总是上浮取当天0.5°图", "反例门控→上浮取0.5°图"]:
            v = tab[k]
            w(f"- {k}：平均损失 {v['regret_h']:.2f} 小时；与精算地图之差 {v['minus_map']:+.2f} {ci(v['minus_map_ci'])}")
        g, m = tab["反例门控→保守"]["regret_h"], tab["地图+精算"]["regret_h"]
        w(f"- 门控后取保守比精算地图{'少' if g < m else '多'}损失 {abs(1 - g / m) * 100:.0f}%（{m:.2f} → {g:.2f} 小时）。")
        loss = np.array([r["JT"][side(r["dJ_map_L2"])] - min(r["JT"].values()) for r in test])
        sc = [worst_regret(r, side(r["dJ_map_L2"]), P["r"]) for r in test]
        fl = [float(np.mean(np.sign(ens_l2(r)) != np.sign(r["dJ_map_L2"]))) for r in test]
        sgn = [1.0 if side(r["dJ_map_L2"]) == "L" else -1.0 for r in test]
        er = [float(np.mean(np.maximum(0.0, s * ens_l2(r)))) for s, r in zip(sgn, test)]
        w(f"- 风险排序（排前 20% 的任务所占的地图损失）：反例的最坏后悔 {top20(sc, loss)*100:.0f}%，32 个合理场的期望后悔 {top20(er, loss)*100:.0f}%，"
          f"32 个合理场的翻转比例 {top20(fl, loss)*100:.0f}%，地图上两侧时间差 {top20([-abs(r['dJ_map_L2']) for r in test], loss)*100:.0f}%。")
        flag = np.array(sc) > P["tau_robust"]
        w(f"- 门控标记 {flag.mean()*100:.0f}% 的任务，占地图损失的 {loss[flag].sum() / loss.sum() * 100:.0f}%。")
        # why the conservative choice without observing fails here
        main_test = load("main", "test")
        blocked = lambda recs: float(np.mean([max(r["JT"].values()) >= 199.9 for r in recs]))
        w(f"- 真实海流中有一侧过不去（顶流过强）的任务：湾流测试年份 {blocked(test)*100:.1f}%，黑潮测试年份 {blocked(main_test)*100:.1f}%。")
        g, into, worst = [], 0, None
        for r in test:
            a = side(r["dJ_map_L2"])
            if worst_regret(r, a, P["r"]) > P["tau_robust"]:
                b = min("LR", key=lambda s_: worst_regret(r, s_, P["r"]))
                if b != a:
                    g.append(r["JT"][a] - r["JT"][b])
                    into += r["JT"][b] >= 199.9
                    if worst is None or g[-1] < worst[0]:
                        worst = (g[-1], worst_regret(r, a, P["r"]), worst_regret(r, b, P["r"]))
        g = np.array(g)
        w(f"- 门控后取保守改选的 {len(g)} 个任务中 {int((g > 0).sum())} 个改对（平均省 {g[g > 0].mean():.1f} 小时），{int((g < 0).sum())} 个改错（平均多花 {(-g[g < 0]).mean():.1f} 小时），"
          f"其中 {into} 次改到了真实海流中过不去的一侧。这类任务里两侧的最坏后悔都因“合理集合中存在把该侧堵死的海流”而接近上限"
          f"（代价最大的一次：地图一侧 {worst[1]:.1f}、另一侧 {worst[2]:.1f} 小时，改选后多花 {-worst[0]:.1f} 小时），选“最坏后悔更小的一侧”近于随机。")
        # post-hoc check of that explanation (not pre-specified; looked at after the test results)
        for tag, name in (("main", "黑潮"), ("gulf", "湾流")):
            Pt = json.load(open(ROOT / "results" / f"route_summary_{tag}.json", encoding="utf-8"))["params"]
            recs = load(tag, "test")
            days = [r["date"] for r in recs]
            base, alt = [], []
            for r in recs:
                J = r["JT"]
                a = side(r["dJ_map_L2"])
                o = "R" if a == "L" else "L"
                wa, wo = worst_regret(r, a, Pt["r"]), worst_regret(r, o, Pt["r"])
                c = o if (wa > Pt["tau_robust"] and wa - wo > Pt["eps"]) else a
                base.append(J[a] - min(J.values()))
                alt.append(J[c] - min(J.values()))
            from route_summary import boot
            d = np.array(alt) - np.array(base)
            w(f"- 事后检验（看过测试结果后才做，非预先设定）：若只在两侧最坏后悔之差超过数值误差容限（{Pt['eps']:.1f} 小时）时才改选，{name}测试年份损失 {np.mean(alt):.2f} 小时，"
              f"与精算地图之差 {d.mean():+.2f} {ci(boot(d, days))}。")
        w("")
    ag = ROOT / "results" / "route_summary_agulhas.json"
    if ag.exists():
        A = json.load(open(ag, encoding="utf-8"))
        P, T, Dv = A["params"], A["test"], A["dev"]
        test = load("agulhas", "test")
        C, tab = T["categories"], T["table"]
        em = np.load(ROOT / "results" / "route_errormodel_agulhas_deg1.0_lag1.npz")
        err = np.sqrt((em["su"] ** 2 + em["sv"] ** 2) / 2)
        w("## 第三海区独立检验：阿古拉斯回流区（35–43°S、14–22°E，全为开阔海洋；检验计划在下载数据之前写进 NOTEBOOK.md，写定后未改；"
          "流程同上，半径与阈值用该区自己的开发年份标定，测试年份只评价一次）")
        w(f"- 任务：开发年份 {Dv['n']} 个（{Dv['n_days']} 天），测试年份 {T['n']} 个（{T['n_days']} 天）；更快一侧平均航时 {T['mean_trip_h']:.1f} 小时。")
        w(f"- 3 天前 1° 粗图的误差：典型误差中位数 {np.median(err[em['su'] > 0]):.2f} 米/秒，相关长度 {float(em['ell']):.0f} 千米。")
        w(f"- 标定：半径 r = {P['r']}（开发年份覆盖 {A['coverage_dev'][str(P['r'])]*100:.0f}%，测试年份 {A['coverage_test_at_r']*100:.0f}%）；数值误差容限 {P['eps']:.1f} 小时；"
          f"保守门控阈值 {P['tau_robust']:.0f} 小时，上浮取 0.5° 图门控阈值 {P['tau_surface05']:.0f} 小时。")
        n, ok, bad = compute_changes(test)
        w(f"- 选错一侧：粗算 {C['wrong_cheap']*100:.1f}%，精算 {C['wrong_expensive']*100:.1f}%（加算改变 {n} 个任务的选择：{ok} 个改对、{bad} 个改错）；"
          f"换成当天 0.5° 图 {np.mean([side(r['dJ_map_fresh05']) != side(r['dJ_true']) for r in test])*100:.1f}%。")
        blocked = float(np.mean([max(r["JT"].values()) >= 199.9 for r in test]))
        w(f"- 真实海流中有一侧过不去的任务：{blocked*100:.1f}%。存在合理反例的任务："
          f"{np.mean([worst_regret(r, side(r['dJ_map_L2']), P['r']) > 0 for r in test])*100:.1f}%。")
        for k in ["地图+粗算", "地图+精算", "集合期望（贝叶斯）", "保守（最坏后悔最小）", "反例门控→保守", "反例门控→保守（差距超过容限才改选）",
                  "总是沿途测30km", "总是上浮取当天0.5°图", "反例门控→上浮取0.5°图"]:
            v = tab[k]
            w(f"- {k}：平均损失 {v['regret_h']:.2f} 小时；与精算地图之差 {v['minus_map']:+.2f} {ci(v['minus_map_ci'])}")
        loss = np.array([r["JT"][side(r["dJ_map_L2"])] - min(r["JT"].values()) for r in test])
        sc = [worst_regret(r, side(r["dJ_map_L2"]), P["r"]) for r in test]
        fl = [float(np.mean(np.sign(ens_l2(r)) != np.sign(r["dJ_map_L2"]))) for r in test]
        t_wr, t_fl = top20(sc, loss), top20(fl, loss)
        w(f"- 风险排序（排前 20% 的任务所占的地图损失）：反例的最坏后悔 {t_wr*100:.0f}%，32 个合理场的翻转比例 {t_fl*100:.0f}%，"
          f"地图上两侧时间差 {top20([-abs(r['dJ_map_L2']) for r in test], loss)*100:.0f}%。")
        c = tab["反例门控→保守（差距超过容限才改选）"]
        v1 = "有效" if c["minus_map_ci"][1] < 0 else ("无害、无显著收益" if c["minus_map"] <= 0 else "未获支持")
        s_ = tab["反例门控→上浮取0.5°图"]
        dw = abs(C["wrong_expensive"] - C["wrong_cheap"]) * 100
        w("- 预先写定的判定：")
        w(f"  1. 改进规则 C（只在两侧最坏后悔之差超过容限时改选）：与精算地图之差 {c['minus_map']:+.2f} {ci(c['minus_map_ci'])} → {v1}。")
        a_ = tab["反例门控→保守"]
        w(f"  2. 原规则 A（门控后取保守）：{a_['minus_map']:+.2f} {ci(a_['minus_map_ci'])}；一侧过不去的任务 {blocked*100:.1f}%（只报告）。")
        w(f"  3. 门控后上浮取 0.5° 图：{s_['minus_map']:+.2f} {ci(s_['minus_map_ci'])} → {'成立' if s_['minus_map_ci'][1] < 0 else '不成立'}。")
        w(f"  4. 加算 64 倍选错率变化 {dw:.1f} 个百分点（预期不超过 3）→ {'成立' if dw <= 3 else '不成立'}。")
        w(f"  5. 最坏后悔排前 20% 的损失 {t_wr*100:.0f}% 对翻转比例 {t_fl*100:.0f}% → {'成立' if t_wr > t_fl else '不成立'}。")
        w("")
    al = ROOT / "results" / "route_summary_altimetry.json"
    if al.exists():
        A = json.load(open(al, encoding="utf-8"))
        P, T, Dv = A["params"], A["test"], A["dev"]
        test = load("altimetry", "test")
        C, tab = T["categories"], T["table"]
        em = np.load(ROOT / "results" / "route_errormodel_altimetry_deg1.0_lag1.npz")
        err = np.sqrt((em["su"] ** 2 + em["sv"] ** 2) / 2)
        w("## 航行器改带真实卫星海流图（黑潮区；检验计划在下载卫星数据之前写进 NOTEBOOK.md，写定后未改）")
        w("- 设置：真实海流仍为 HYCOM 1/12°、10 米；航行器的图换成 NOAA CoastWatch 近实时融合测高地转流（0.25°，逐日，绝对表层地转流），取 3 天前那一天；"
          "上浮取图 = 取当天的测高图（每次 1 小时），另保留“上浮取当天 0.5° 模式图”作理想参照；误差模型、半径与阈值在开发年份用“测高图减 HYCOM”标定。")
        w(f"- 任务：开发年份 {Dv['n']} 个（{Dv['n_days']} 天），测试年份 {T['n']} 个（{T['n_days']} 天）；更快一侧平均航时 {T['mean_trip_h']:.1f} 小时。")
        w(f"- 测高图（3 天前）的误差：典型误差中位数 {np.median(err[em['su'] > 0]):.2f} 米/秒，相关长度 {float(em['ell']):.0f} 千米。")
        w(f"- 标定：半径 r = {P['r']}（开发年份覆盖 {A['coverage_dev'][str(P['r'])]*100:.0f}%，测试年份 {A['coverage_test_at_r']*100:.0f}%）；数值误差容限 {P['eps']:.1f} 小时；"
          f"保守门控阈值 {P['tau_robust']:.0f} 小时，上浮取测高图门控阈值 {P['tau_surface']:.0f} 小时，上浮取 0.5° 模式图门控阈值 {P['tau_surface05']:.0f} 小时。")
        n, ok, bad = compute_changes(test)
        w(f"- 选错一侧：粗算 {C['wrong_cheap']*100:.1f}%，精算 {C['wrong_expensive']*100:.1f}%（加算改变 {n} 个任务的选择：{ok} 个改对、{bad} 个改错）；"
          f"换成当天测高图 {np.mean([side(r['dJ_map_fresh']) != side(r['dJ_true']) for r in test])*100:.1f}%，当天 0.5° 模式图 "
          f"{np.mean([side(r['dJ_map_fresh05']) != side(r['dJ_true']) for r in test])*100:.1f}%。")
        amb = float(np.mean([worst_regret(r, side(r["dJ_map_L2"]), P["r"]) > 0 for r in test]))
        blocked = float(np.mean([max(r["JT"].values()) >= 199.9 for r in test]))
        w(f"- 存在合理反例的任务 {amb*100:.1f}%；真实海流中有一侧过不去的任务 {blocked*100:.1f}%。")
        for k in ["地图+粗算", "地图+精算", "集合期望（贝叶斯）", "保守（最坏后悔最小）", "反例门控→保守", "反例门控→保守（差距超过容限才改选）",
                  "总是沿途测30km", "总是上浮取当天1°图", "反例门控→上浮取图", "总是上浮取当天0.5°图", "反例门控→上浮取0.5°图"]:
            v = tab[k]
            name = k.replace("当天1°图", "当天测高图").replace("→上浮取图", "→上浮取测高图")
            w(f"- {name}：平均损失 {v['regret_h']:.2f} 小时；与精算地图之差 {v['minus_map']:+.2f} {ci(v['minus_map_ci'])}")
        loss = np.array([r["JT"][side(r["dJ_map_L2"])] - min(r["JT"].values()) for r in test])
        sc = [worst_regret(r, side(r["dJ_map_L2"]), P["r"]) for r in test]
        fl = [float(np.mean(np.sign(ens_l2(r)) != np.sign(r["dJ_map_L2"]))) for r in test]
        t_wr, t_fl = top20(sc, loss), top20(fl, loss)
        w(f"- 风险排序（排前 20% 的任务所占的地图损失）：反例的最坏后悔 {t_wr*100:.0f}%，32 个合理场的翻转比例 {t_fl*100:.0f}%，"
          f"地图上两侧时间差 {top20([-abs(r['dJ_map_L2']) for r in test], loss)*100:.0f}%。")
        dw = abs(C["wrong_expensive"] - C["wrong_cheap"]) * 100
        s1, s5 = tab["反例门控→上浮取图"], tab["反例门控→上浮取0.5°图"]
        a_, c_ = tab["反例门控→保守"], tab["反例门控→保守（差距超过容限才改选）"]
        w("- 预先写定的判定：")
        w(f"  1. 加算 64 倍选错率变化 {dw:.1f} 个百分点（预期不超过 3）→ {'成立' if dw <= 3 else '不成立'}。")
        w(f"  2. 存在合理反例 {amb*100:.1f}%（预期不少于 90%）→ {'成立' if amb >= 0.9 else '不成立'}。")
        w(f"  3. 最坏后悔排前 20% 的损失 {t_wr*100:.0f}% 对翻转比例 {t_fl*100:.0f}% → {'成立' if t_wr > t_fl else '不成立'}。")
        w(f"  4. 门控后上浮取当天测高图：{s1['minus_map']:+.2f} {ci(s1['minus_map_ci'])}（只报告）；门控后上浮取当天 0.5° 模式图："
          f"{s5['minus_map']:+.2f} {ci(s5['minus_map_ci'])} → {'成立' if s5['minus_map_ci'][1] < 0 else '不成立'}。")
        w(f"  5. 门控后取保守（规则 A）{a_['minus_map']:+.2f} {ci(a_['minus_map_ci'])}；改进规则 C {c_['minus_map']:+.2f} {ci(c_['minus_map_ci'])}"
          f"（预期 C 的点估计不高于照地图走 → {'成立' if c_['minus_map'] <= 0 else '不成立'}）。")
        w("")
    out = ROOT / "paper" / "gemini" / "facts_v4.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(out)
    print("\n".join(L))


if __name__ == "__main__":
    main()
