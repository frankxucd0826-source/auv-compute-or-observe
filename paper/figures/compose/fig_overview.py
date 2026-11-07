"""Figure 1: overview, in the grammar of the student's earlier overview figures (SCS Fig. 2 style):
pastel panels that tile the canvas, the central Blender render pressing on the panel borders,
boxes with thick outlines carrying the paper's symbols and numbers, small data insets drawn from
the results, thick arrows (black for data flow, yellow for the pre-launch decision).
  (A) ocean big data: eight years of daily satellite chlorophyll; how wrong a map gets with age;
      where the ocean changes fastest; the mission windows; a deep forecaster does not help
  (B) before launch: 48 imagined oceans around the stale map, 32 searched and 16 held out;
      rehearsal of five time-allocation strategies on held-out oceans (one real mission's scores)
  (C) during the mission: go / think / stop every 20 minutes; why the value of thinking must be
      judged on held-out oceans (planning-budget results); the score
Usage: python -E -X utf8 paper/figures/compose/fig_overview.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import figkit as K  # noqa: E402

ROOT = Path(HERE).resolve().parents[2]
FIG = os.path.join(HERE, "..")
REN = os.path.join(FIG, "renders")
TEX = os.path.join(REN, "textures")
TMP = os.path.join(REN, "_inset")
os.makedirs(TMP, exist_ok=True)
W, H = 154.0, 104.0
INK, TITLE = "#1F2A36", "#2B3F55"
PANEL = {"A": "#CFE0F1", "B": "#DDEBD5", "C": "#F4E3CC"}
EDGE = {"A": "#2E5E8C", "B": "#4F7A45", "C": "#9A6A35"}
GO, THINK, STOP, HELD, SEARCH = "#1C7ED6", "#F08C00", "#2F9E44", "#E8590C", "#1F3A5F"
LW, PT = 0.55, 0.3528


def tbox(F, x, y, w, h, lines, fill="#FFFFFF", edge=INK, sizes=(7.4, 6.6), color=INK, bold=(0,), r=1.4,
         lw=LW, lead=1.30):
    F.rect(x, y, w, h, fill, edge, lw, r)
    szs = [sizes[min(k, len(sizes) - 1)] for k in range(len(lines))]
    steps = [szs[k] * lead * PT for k in range(len(lines))]
    yy = y + h / 2 - sum(steps[1:]) / 2 + 0.34 * szs[0] * PT
    for k, s in enumerate(lines):
        if k:
            yy += steps[k]
        tw = K.text_width(s, szs[k], k in bold, "serif")
        if tw > w - 1.4:
            print(f"  ! text too wide ({tw:.1f} > {w - 1.4:.1f} mm): {s}")
        F.text(x + w / 2, yy, s, szs[k], color, k in bold, "middle", "serif")


def plate(F, x, y, s, size=6.6, anchor="middle", color=INK, pad=0.7, bold=True):
    w = K.text_width(s, size, bold, "serif")
    x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
    hh = size * PT
    top, bot = y - hh * 0.95 - pad * 0.6, y + hh * 0.30 + pad * 0.6
    F.rect(x0 - pad, top, w + 2 * pad, bot - top, "#FFFFFF", "#5A6B7B", 0.25, 1.0, 0.94)
    F.text(x0 + w / 2, y, s, size, color, bold, "middle", "serif")


def arrow(F, pts, color=INK, width=0.75, head=2.0):
    F.line(pts, color, width, arrow=True, head=head)


def block_arrow(F, x, y0, y1, w=5.0, color="#F5C518", edge="#9C7A00"):
    """A fat downward arrow from y0 to y1 centred on x."""
    hh = 2.6
    F.polygon([(x - w / 4, y0), (x + w / 4, y0), (x + w / 4, y1 - hh), (x + w / 2, y1 - hh), (x, y1),
               (x - w / 2, y1 - hh), (x - w / 4, y1 - hh)], color, edge, 0.35)


def season_maps():
    """Spread of the 3-day change of log chlorophyll in each season (all 3197 days)."""
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import cm
    d = np.load(ROOT / "results" / "atlas" / "atlas_stats.npz")
    out = {}
    for s in ("spring", "summer", "autumn", "winter"):
        a = d[f"sd_{s}_3"][::-1]                  # row 0 = north
        rgba = cm.get_cmap("YlGnBu")(np.clip(a / 0.30, 0, 1))
        rgba[np.isnan(a)] = (0.80, 0.80, 0.80, 1.0)
        p = os.path.join(TMP, f"season_{s}.png")
        Image.fromarray((rgba * 255).astype(np.uint8)).resize((240, 256)).save(p)
        out[s] = p
    return out


def curse_numbers():
    df = pd.DataFrame([json.loads(l) for l in open(ROOT / "results" / "curse3_dev" / "results.jsonl", encoding="utf-8")])
    d = df[df.scale == 1.0].groupby("budget")[["believed", "believed_holdout", "true"]].mean()
    return d


def rehearsal_scores():
    """Imagined regrets of the five strategies in the rehearsal of the overview mission (moderate computer)."""
    meta = json.load(open(os.path.join(TEX, "meta.json"), encoding="utf-8"))
    for l in open(ROOT / "results" / "main_v3_test_moderate" / "results.jsonl", encoding="utf-8"):
        r = json.loads(l)
        if r["mission"] == meta["mission"] and r["controller"] == "rehearsal":
            return r["imagined"], r["choice"]
    raise SystemExit("rehearsal row not found")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    K.use_cjk()
    F = K.Figure(W, H)
    # ---------------- panels ----------------
    F.rect(1.5, 1.5, 54.5, 101.0, PANEL["A"], None, 0.0, 4.5)
    F.rect(58.0, 1.5, 94.5, 36.0, PANEL["B"], None, 0.0, 4.5)
    F.rect(58.0, 39.5, 94.5, 63.0, PANEL["C"], None, 0.0, 4.5)
    F.text(4.0, 7.6, "(A) 海洋大数据：旧卫星图会错多少", 8.4, TITLE, True, family="title")
    F.text(61.0, 7.6, "(B) 出发前：在想象海洋里预演", 8.4, TITLE, True, family="title")
    F.text(61.0, 100.4, "(C) 航行中：每 20 分钟选一次", 8.4, TITLE, True, family="title")

    # ---------------- (A) ----------------
    tbox(F, 4.0, 10.5, 49.5, 9.6, ["东海卫星叶绿素与海表温度", "2018–2026 年 · 逐日 · 2 km · 3197 天"],
         fill="#EEF4FB", edge=EDGE["A"], sizes=(7.4, 6.6))
    th = 18.5
    F.image(os.path.join(TEX, "stale.png"), 5.0, 22.6, w=th, h=th)
    F.image(os.path.join(TEX, "sat_day.png"), 33.5, 22.6, w=th, h=th)
    F.rect(5.0, 22.6, th, th, None, EDGE["A"], 0.5)
    F.rect(33.5, 22.6, th, th, None, EDGE["A"], 0.5)
    arrow(F, [(24.6, 31.8), (32.3, 31.8)], EDGE["A"], 0.7, 1.7)
    F.text(28.4, 30.2, "3 天", 6.4, EDGE["A"], True, "middle", "serif")
    F.text(14.25, 44.6, "3 天前的卫星图 $c_{map}$", 6.4, INK, True, "middle", "serif")
    F.text(42.75, 44.6, "任务当天的卫星图", 6.4, INK, True, "middle", "serif")
    # stale-map error by age (development windows)
    F.text(15.0, 50.6, "旧图误差 $s_k$", 6.8, INK, True, "middle", "serif")
    base, top = 69.0, 54.6
    sk = [(1, 0.125), (2, 0.176), (3, 0.210)]
    F.line([(5.0, base), (25.5, base)], INK, 0.35)
    for j, (k, v) in enumerate(sk):
        x = 7.0 + j * 6.4
        h = (base - top) * v / 0.21
        F.rect(x, base - h, 4.6, h, EDGE["A"] if k == 3 else "#7FA6CC", None, 0.0, 0.3)
        F.text(x + 2.3, base - h - 0.9, f"{v:.3f}", 5.6, INK, False, "middle", "serif")
        F.text(x + 2.3, base + 2.6, f"{k} 天", 5.8, INK, False, "middle", "serif")
    # seasons
    F.text(40.5, 50.6, "3 天变化的季节图谱", 6.8, INK, True, "middle", "serif")
    sm = season_maps()
    names = {"spring": "春", "summer": "夏", "autumn": "秋", "winter": "冬"}
    s = 10.6
    for j, key in enumerate(("spring", "summer", "autumn", "winter")):
        x, y = 29.6 + (j % 2) * (s + 0.6), 52.4 + (j // 2) * (s + 0.6)
        F.image(sm[key], x, y, w=s, h=s)
        F.rect(x, y, s, s, None, "#41556B", 0.3)
        F.rect(x + 0.4, y + 0.4, 3.6, 3.2, "#FFFFFF", None, 0.0, 0.5, 0.85)
        F.text(x + 2.2, y + 2.9, names[key], 5.6, INK, True, "middle", "serif")
    tbox(F, 4.0, 75.6, 49.5, 9.4, ["切出 422 个赤潮任务窗口，各 80 km 见方", "开发 274 个 · 测试 148 个（2023 年起）"],
         edge=EDGE["A"], sizes=(6.9, 6.2))
    tbox(F, 4.0, 86.8, 49.5, 9.4, ["深度时空预测模型（550 万参数）", "提前 3 天误差 0.149 ≈ 沿用最新图 0.147"],
         edge=EDGE["A"], sizes=(6.9, 6.2))
    F.text(28.75, 100.2, "小尺度变化只能靠现场观测", 7.0, EDGE["A"], True, "middle", "serif")

    # ---------------- (B) ----------------
    tbox(F, 61.0, 10.5, 46.0, 9.6, ["48 个想象海洋（随采样同化更新）", "$c^{(i)}=c_{map}+σ_k z^{(i)}$，$σ_k$ 由八年数据标定"],
         fill="#F2F8EE", edge=EDGE["B"], sizes=(6.9, 6.4))
    tbox(F, 61.0, 21.8, 22.4, 7.4, ["32 个：搜索航线"], edge=SEARCH, sizes=(6.6,), lw=0.7)
    tbox(F, 84.6, 21.8, 22.4, 7.4, ["16 个：留出评判"], edge=HELD, sizes=(6.6,), lw=0.7)
    # rehearsal: one real mission's imagined regrets
    scores, choice = rehearsal_scores()
    order = [("go", [0]), ("think", [1]), ("think 1 in 3", [1, 0, 0]),
             ("stop and think 1 in 3", [3, 0, 0]), ("stop and resample 1 in 3", [2, 0, 0])]
    colmap = {0: GO, 1: THINK, 2: STOP, 3: STOP}
    F.rect(109.0, 10.5, 41.5, 25.6, "#FFFFFF", EDGE["B"], LW, 1.4)
    F.text(129.75, 14.3, "预演：4 个留出海洋当真值，各跑 24 h", 6.2, INK, True, "middle", "serif")
    F.text(129.75, 17.6, "选想象遗憾 $\\bar{R}_s$ 最小的用时策略 $s^*$", 6.0, INK, False, "middle", "serif")
    for k, (name, pat) in enumerate(order):
        y = 19.6 + k * 3.25
        for q in range(6):
            a = pat[q % len(pat)]
            F.rect(110.6 + q * 2.35, y, 2.05, 2.4, colmap[a], None, 0.0, 0.25)
            if a == 3:     # stop and think: a stopped interval with the computer on
                F.rect(110.6 + q * 2.35 + 0.55, y + 0.6, 0.95, 1.2, THINK, None, 0.0, 0.1)
        v = scores[name]
        L = 26.0 * v
        chosen = name == choice
        F.rect(125.4, y + 0.15, L * 0.62, 2.1, "#5C7CA0" if chosen else "#C9D3DD", INK if chosen else None,
               0.35, 0.3)
        F.text(125.4 + L * 0.62 + 0.8, y + 1.95, f"{v:.3f}", 5.4, INK, chosen, "start", "serif")
        if chosen:
            F.text(125.4 + L * 0.62 + 7.4, y + 2.0, "← $s^*$", 5.8, EDGE["B"], True, "start", "serif")
    # data flow A -> B
    arrow(F, [(53.6, 15.3), (60.6, 15.3)], INK, 0.8, 2.0)

    # ---------------- central render ----------------
    im = Image.open(os.path.join(REN, "overview.png"))
    bb = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    rw = 60.0
    rx, ry = 52.0, 33.4
    crop = os.path.join(REN, "_cut_overview.png")
    im.crop(bb).save(crop)
    F.image(crop, rx, ry, w=rw)
    an = json.load(open(os.path.join(REN, "overview_anchors.json"), encoding="utf-8"))
    sx = rw / (bb[2] - bb[0])

    def P(name):
        px, py = an[name]
        return rx + (px - bb[0]) * sx, ry + (py - bb[1]) * sx

    c = P("core")
    plate(F, c[0] + 9.0, c[1] - 6.4, "赤潮最浓处", 6.2)
    F.line([(c[0] + 5.0, c[1] - 4.7), c], INK, 0.3)
    a = P("auv")
    t = P("think_seg")
    plate(F, a[0] + 9.5, a[1] + 9.0, "航行器", 6.2)
    F.line([(a[0] + 7.0, a[1] + 7.2), a], INK, 0.3)
    plate(F, t[0] - 2.0, t[1] + 12.5, "航迹：蓝 = 走，橙 = 深想", 6.0)
    F.line([(t[0] - 1.0, t[1] + 10.2), t], INK, 0.3)
    top = P("imag_top")
    F.line([(95.8, 29.2), (95.8, 31.8), (top[0] + 1.2, 31.8), (top[0] + 1.2, top[1] + 0.8)], HELD, 0.6, arrow=True, head=1.5)

    # ---------------- (C) ----------------
    # the value of thinking, judged two ways (planning-budget experiment, development windows)
    d = curse_numbers()
    x0, x1, y0, y1 = 118.0, 148.5, 52.5, 67.5
    F.rect(114.0, 48.6, 38.0, 23.6, "#FFFFFF", EDGE["C"], LW, 1.4)
    F.text(133.0, 52.0, "多想的收益：搜索自评会虚高", 6.2, INK, True, "middle", "serif")
    lb = np.log10(d.index.values.astype(float))
    lo, hi = 0.72, 0.94

    def XY(b, v):
        return x0 + (b - lb.min()) / (lb.max() - lb.min()) * (x1 - x0), y1 - (v - lo) / (hi - lo) * (y1 - 55.0)
    F.line([(x0, 55.0), (x0, y1), (x1, y1)], "#8696A7", 0.3)
    for key, col, dash, lab in (("believed", "#D9480F", None, "搜索自评"), ("true", INK, None, "真实"),
                                ("believed_holdout", "#1971C2", (1.0, 0.7), "留出评判")):
        pts = [XY(b, v) for b, v in zip(lb, d[key].values)]
        F.line(pts, col, 0.6, dash=dash)
        for p in pts[::2] + [pts[-1]]:
            F.circle(p[0], p[1], 0.45, col)
    p_hi = XY(lb[-1], d["believed"].values[-1])
    p_mid = XY(lb[len(lb) // 2], d["believed"].values[len(lb) // 2])
    F.text(p_mid[0] - 0.6, p_mid[1] - 1.4, "搜索自评", 5.4, "#D9480F", True, "end", "serif")
    p_t = XY(lb[-1], d["true"].values[-1])
    F.text(p_t[0] - 0.8, p_t[1] + 3.4, "真实 ≈ 留出评判", 5.4, INK, True, "end", "serif")
    F.text(x0, y1 + 2.6, "64", 5.2, INK, False, "middle", "serif")
    F.text(x1, y1 + 2.6, "20 万", 5.2, INK, False, "middle", "serif")
    F.text((x0 + x1) / 2, y1 + 2.6, "每次决策的推演次数", 5.2, INK, False, "middle", "serif")
    # the query and the score
    tbox(F, 114.0, 73.6, 38.0, 9.4, ["应急中心随时问：最浓处在哪？", "评分 $R$：浓度差的 24 h 平均"], fill="#FBF2E6",
         edge=EDGE["C"], sizes=(6.4, 6.0))
    # the three uses of an interval
    cards = [(GO, "走", ["沿航线前行 1.8 km", "测 2 个点 · 45 W"]),
             (THINK, "深想", ["开高功耗芯片规划", "快 50 倍 · +20 W"]),
             (STOP, "停下", ["随水漂，原地测 5 次", "只耗 15 W"])]
    for k, (col, head, sub) in enumerate(cards):
        x = 61.0 + k * 30.6
        F.rect(x, 84.4, 29.4, 12.0, "#FFFFFF", col, 0.8, 1.4)
        F.rect(x, 84.4, 8.0, 12.0, col, col, 0.8, 1.4)
        F.text(x + 4.0, 91.9, head, 7.0 if len(head) == 1 else 6.4, "#FFFFFF", True, "middle", "serif")
        F.lines(x + 9.0, 89.2, sub, 5.9, INK, False, "start", 1.35, "serif")
    # the chosen strategy goes to sea
    block_arrow(F, 111.6, 36.4, 47.0, 5.4)
    F.text(115.4, 45.2, "按 $s^*$ 下水执行", 6.4, INK, True, "start", "serif")
    out = os.path.join(FIG, "fig_overview")
    F.save_pdf(out + ".pdf")
    F.save_svg(out + ".svg")
    print("saved", out)


if __name__ == "__main__":
    main()
