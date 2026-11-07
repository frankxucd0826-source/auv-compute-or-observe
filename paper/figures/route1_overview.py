"""Fig. 1: the decision, the test and the responses around one 3-D scene.
Centre: the example mission's sea (real current of 2022-01-18), the no-go zone, both fastest routes, the vehicle,
the stack of plausible fields (coarse map in the middle, counterexample on top) and a satellite (new map).
(a) the side choice under a coarse map: what the vehicle has, and the two sides' times on the map and in
    the real current; (b) the plausible counterexample test; (c) compute or observe.
The 3-D scene is rendered by blender/render_route.py (textures by blender/make_route_textures.py)."""
import json

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Arc, Polygon, Rectangle
from matplotlib.font_manager import FontProperties
from PIL import Image

import rstyle as st
import rmaps as rm

W, H = 154.0, 122.0
PANEL = {"a": "#E9F1FA", "b": "#EAF4EE", "c": "#FBF1E6"}
EDGE = {"a": "#B9CCE3", "b": "#B7D5C1", "c": "#E7C9A6"}
SERIF = ["Times New Roman", "SimSun"]


def fp(size=8.0, bold=False):
    return FontProperties(family=["Times New Roman", "SimHei"] if bold else SERIF, size=size,
                          weight="bold" if bold else "normal")


def T(ax, x, y, s, size=8.0, bold=False, col=st.INK, ha="left", va="center", **kw):
    return ax.text(x, y, s, fontproperties=fp(size, bold), color=col, ha=ha, va=va, **kw)


def rbox(ax, x, y, w, h, fc, ec="none", lw=1.0, r=2.0, z=0, alpha=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw,
                                zorder=z, alpha=alpha))


def num(ax, x, y, k, col, r=2.1):
    ax.add_patch(Circle((x, y), r, fc=col, ec="white", lw=0.8, zorder=6))
    T(ax, x, y - 0.1, str(k), size=7.6, bold=True, col="white", ha="center", zorder=7)


def block_arrow(ax, p, q, col="#F5B83D", width=3.2, head=6.0, z=5):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=f"simple,head_width={head},head_length={head * 0.8},tail_width={width}",
                                 mutation_scale=1.0, fc=col, ec="#C98A0B", lw=0.8, zorder=z))


def icon_chip(ax, x, y, s=3.2, col=st.MUTED):
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc="white", ec=col, lw=0.9, zorder=5))
    ax.add_patch(Rectangle((x - s / 4, y - s / 4), s / 2, s / 2, fc=col, ec="none", zorder=5))
    for k in (-0.25, 0.25):
        for a, b in (((x + k * s, y + s / 2), (x + k * s, y + s / 2 + 0.6)), ((x + k * s, y - s / 2), (x + k * s, y - s / 2 - 0.6)),
                     ((x + s / 2, y + k * s), (x + s / 2 + 0.6, y + k * s)), ((x - s / 2, y + k * s), (x - s / 2 - 0.6, y + k * s))):
            ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=0.8, zorder=5)


def icon_wave(ax, x, y, col=st.ENS):
    ax.add_patch(Circle((x - 1.3, y), 0.45, fc=col, ec="none", zorder=5))
    for r in (1.0, 1.8, 2.6):
        ax.add_patch(Arc((x - 1.3, y), 2 * r, 2 * r, theta1=-45, theta2=45, color=col, lw=0.9, zorder=5))


def icon_up(ax, x, y, col=st.OBS):
    xs = np.linspace(x - 1.8, x + 1.8, 30)
    ax.plot(xs, y - 1.2 + 0.35 * np.sin(xs * 3.0), color=col, lw=0.9, zorder=5)
    ax.add_patch(FancyArrowPatch((x, y - 0.9), (x, y + 1.9), arrowstyle="-|>", mutation_scale=6, color=col, lw=1.0,
                                 zorder=5))


def time_bars(ax, x, y, label, tL, tR, w=26.0, tmax=56.0):
    T(ax, x, y + 3.3, label, size=7.8)
    for k, (a, t) in enumerate((("L", tL), ("R", tR))):
        yy = y - 1.0 - 2.9 * k
        ax.add_patch(Rectangle((x, yy - 1.0), w * t / tmax, 2.0, fc=rm.SIDE_D[a], ec="none", zorder=4))
        best = t == min(tL, tR)
        T(ax, x + w * t / tmax + 0.8, yy, f"{'左' if a == 'L' else '右'} {t:.1f} 小时", size=7.6, bold=best,
          col=rm.SIDE_D[a])


def main():
    st.setup()
    fig = plt.figure(figsize=(W * st.MM, H * st.MM))
    bg = fig.add_axes([0, 0, 1, 1])
    bg.set_xlim(0, W)
    bg.set_ylim(0, H)
    bg.axis("off")
    # panels
    ya = 63.0
    rbox(bg, 0.4, ya, W - 0.8, H - ya - 0.4, PANEL["a"], EDGE["a"], 0.8, r=3.0)
    rbox(bg, 0.4, 0.4, W / 2 - 1.2, ya - 2.0, PANEL["b"], EDGE["b"], 0.8, r=3.0)
    rbox(bg, W / 2 + 0.8, 0.4, W / 2 - 1.2, ya - 2.0, PANEL["c"], EDGE["c"], 0.8, r=3.0)
    T(bg, 3.0, H - 4.0, "(a) 粗图下的左右选边", size=9.2, bold=True)
    T(bg, 3.0, 4.3, "(b) 合理反例检验：求解误差还是粗图误差", size=9.2, bold=True)
    T(bg, W - 3.0, 4.3, "(c) 计算还是观测", size=9.2, bold=True, ha="right")

    # ---- centre render ----
    im = Image.open(st.OUT / "renders" / "route_scene.png")
    A = json.load(open(st.OUT / "renders" / "route_anchors.json"))
    alpha = np.array(im)[:, :, 3]
    ys_, xs_ = np.where(alpha > 8)
    cx0, cx1, cy0, cy1 = xs_.min() - 4, xs_.max() + 4, ys_.min() - 4, ys_.max() + 4
    crop = im.crop((cx0, cy0, cx1, cy1))
    rw = 70.0
    rh = rw * (cy1 - cy0) / (cx1 - cx0)
    rx, ry = 41.0, H - 6.0 - rh
    ra = fig.add_axes([rx / W, ry / H, rw / W, rh / H])
    ra.imshow(crop)
    ra.axis("off")
    ra.set_zorder(2)

    def P(name):
        px, py = A[name]
        return rx + (px - cx0) / (cx1 - cx0) * rw, ry + rh - (py - cy0) / (cy1 - cy0) * rh

    ov = fig.add_axes([0, 0, 1, 1])
    ov.set_xlim(0, W)
    ov.set_ylim(0, H)
    ov.axis("off")
    ov.set_zorder(3)
    # labels on the scene
    x, y = P("nogo")
    st.note(ov, x, y + 0.2, "禁航区", col="#B02525", size=7.6, ha="center", weight="bold")
    xn, yn = x, y
    x, y = P("routeR")
    st.note(ov, x - 1.0, y - 4.2, "右侧：真实海流中更快", col=rm.PINK_D, size=7.6, weight="bold", ha="center")
    st.note(ov, xn + 1.0, yn + 5.2, "左侧：粗图上略快", col=rm.GOLD_D, size=7.6, weight="bold", ha="center")
    x, y = P("auv")
    st.note(ov, x - 1.0, y - 3.8, "航行器", size=7.6, ha="center")
    xs, ys = P("sheet_cx")
    st.note(ov, xs + 2.8, ys + 0.6, "合理反例", col=st.OURS, size=7.8, weight="bold", ha="left")
    xm, ym = P("sheet_map")
    st.note(ov, xm + 3.6, ym, "粗图", col=st.MAP, size=7.8, ha="left")
    xl, yl = P("sheet_low")
    xb_ = max(xs, xl) + 13.5
    ov.plot([xb_ - 0.8, xb_, xb_, xb_ - 0.8], [ys + 1.2, ys + 1.2, yl - 0.8, yl - 0.8], color=st.INK, lw=0.8)
    st.note(ov, xb_ + 1.0, (ys + yl) / 2, "合理流场\n集合", col=st.INK, size=7.6, ha="left")
    xa, ya_ = P("auv")
    xsat, ysat = P("sat")
    ov.annotate("", xy=(xsat + 1.0, ysat - 2.6), xytext=(xa - 1.5, ya_ + 2.0),
                arrowprops=dict(arrowstyle="-|>", color=st.OBS, lw=1.1, ls=(0, (3, 2)), mutation_scale=8,
                                connectionstyle="arc3,rad=-0.15"))
    st.note(ov, xsat - 4.0, ysat - 6.5, "上浮\n取新图", col=st.OBS, size=7.6, ha="right", va="top")

    # ---- (a) left: what the vehicle has ----
    T(ov, 3.0, H - 10.5, "航行器端侧", size=8.2, bold=True)
    rows = [(icon_chip, "算力与电量有限"), (icon_wave, "水下只能低速水声通信"), (icon_up, "上浮取图约 1 小时")]
    for k, (ic, txt) in enumerate(rows):
        yy = H - 16.5 - 6.0 * k
        ic(ov, 5.6, yy)
        T(ov, 9.6, yy, txt, size=7.8)
    rbox(ov, 2.6, H - 48.0, 36.0, 10.0, "white", st.MAP, 0.8, r=1.5, z=4)
    T(ov, 4.0, H - 41.0, "携带 3 天前的 1° 粗图", size=7.8, bold=True, zorder=5)
    T(ov, 4.0, H - 45.2, "绕禁航区：左侧还是右侧？", size=7.6, zorder=5)
    # ---- (a) right: the two sides' times ----
    xr = W - 38.0
    T(ov, xr, H - 10.5, "两侧最快航时", size=8.2, bold=True)
    time_bars(ov, xr, H - 18.5, "粗图上：两侧几乎一样", 37.7, 38.0, w=19.0)
    time_bars(ov, xr, H - 33.5, "当天真实海流：右侧快得多", 53.4, 41.7, w=19.0)
    rbox(ov, xr - 1.0, H - 52.5, 36.5, 7.2, "white", "#E03131", 0.9, r=1.5, z=4)
    T(ov, xr + 17.25, H - 48.9, "按粗图选左侧：多花 11.7 小时", size=7.6, bold=True, col="#C92A2A", ha="center", zorder=5)

    # ---- (b) the test ----
    zx = fig.add_axes([2.5 / W, 9.0 / H, 27.0 / W, 27.0 / H])
    zx.set_xlim(-1.35, 1.35)
    zx.set_ylim(-1.35, 1.35)
    zx.set_aspect("equal")
    zx.axis("off")
    zx.set_zorder(4)
    zx.add_patch(Circle((0, 0), 1.0, fc=st.OURS_LIGHT, ec=st.OURS, lw=1.2, alpha=0.9))
    for rr in (0.33, 0.66):
        zx.add_patch(Circle((0, 0), rr, fc="none", ec=st.OURS, lw=0.5, alpha=0.4, ls=(0, (2, 2))))
    zx.scatter([0], [0], s=26, color=st.MAP, edgecolor="white", lw=0.8, zorder=4)
    ang = np.deg2rad(35)
    zx.annotate("", xy=(np.cos(ang) * 0.97, np.sin(ang) * 0.97), xytext=(0.06, 0.04),
                arrowprops=dict(arrowstyle="-|>", color=st.OURS, lw=1.6, mutation_scale=9))
    zx.scatter([np.cos(ang)], [np.sin(ang)], s=120, marker="*", color="#E03131", edgecolor="white", lw=0.8, zorder=5)
    zx.text(0.0, -0.22, "粗图", ha="center", va="top", fontproperties=fp(7.6), color=st.MAP)
    zx.text(np.cos(ang) + 0.04, np.sin(ang) + 0.16, "合理反例", ha="center", va="bottom", fontproperties=fp(7.6, True),
            color="#C92A2A")
    zx.text(0.0, -1.10, "合理流场集合（半径 r）", ha="center", va="top", fontproperties=fp(7.4), color=st.OURS)
    steps = [("多年误差标定集合", "误差大小、相关长度与半径\n由开发年份的误差确定"),
             ("梯度搜索最大后悔值", "导数沿最快航线累加\n约 71 次航线求解"),
             ("判断误差来源", "航时差小于求解误差：加密求解\n最大后悔值超过阈值：观测")]
    for k, (head, body) in enumerate(steps):
        yy = 50.5 - 14.0 * k
        num(ov, 33.3, yy, k + 1, st.OURS)
        T(ov, 36.4, yy, head, size=7.8, bold=True)
        T(ov, 36.4, yy - 2.6, body, size=7.0, col=st.MUTED, va="top", linespacing=1.25)

    # ---- (c) compute or observe ----
    cards = [("加密求解", st.COMPUTE, "航时差小于\n求解误差容限", "改用细网格\n再算一次"),
             ("观测", st.OBS, "最大后悔值\n超过阈值", "上浮取当天\n海流图再选"),
             ("保守改选", st.OURS, "超过阈值且\n不能上浮", "选最大后悔值\n较小的一侧")]
    cw, ch, gx = 21.5, 33.0, 2.6
    x0c = W / 2 + 4.5
    for k, (head, col, cond, act) in enumerate(cards):
        xc = x0c + k * (cw + gx)
        rbox(ov, xc, 13.0, cw, ch, "white", col, 1.5, r=1.8, z=4)
        num(ov, xc + 3.2, 13.0 + ch - 3.4, k + 1, col)
        T(ov, xc + 6.2, 13.0 + ch - 3.4, head, size=8.2, bold=True, col=col, zorder=5)
        T(ov, xc + cw / 2, 13.0 + ch - 9.5, cond, size=7.4, ha="center", va="top", col=st.MUTED, zorder=5, linespacing=1.2)
        ov.add_patch(FancyArrowPatch((xc + cw / 2, 13.0 + ch - 17.6), (xc + cw / 2, 13.0 + ch - 20.6), arrowstyle="-|>",
                                     mutation_scale=7, color=col, lw=1.0, zorder=5))
        T(ov, xc + cw / 2, 13.0 + ch - 21.6, act, size=7.6, bold=True, ha="center", va="top", col=st.INK, zorder=5,
          linespacing=1.2)
    T(ov, x0c, 9.0, "最大后悔值不超过阈值：粗图可信，按粗图选边", size=7.6, col=st.MAP)
    block_arrow(ov, (72.3, 20.0), (W / 2 + 3.8, 20.0), width=3.0, head=6.0)
    st.save(fig, "route1_overview")


if __name__ == "__main__":
    main()
