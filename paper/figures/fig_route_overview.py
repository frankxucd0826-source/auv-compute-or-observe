"""Fig. 1: the question and the method on one real test mission (2022-01-18).
(a) the 1-degree map made 3 days earlier: the two sides look equal; (b) a current field that agrees with
the map as well as the real ocean does (radius set on the development years) in which the map's side
is much slower; (c) the real ocean; (d) the decision: computation for numerical ambiguity, the
counterexample check for environmental ambiguity, then observe or hedge depending on the cost."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style as st  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch  # noqa: E402
import matplotlib.patheffects as pe  # noqa: E402

SPEED = LinearSegmentedColormap.from_list("speed", ["#F7FAFC", "#D6E8F3", "#9DC8E3", "#5A9FCE", "#2C6FA8", "#1B4473"])
LEFT, RIGHT = "#F08C00", "#7048E8"
BOX = {"step": ("#E7F1FB", "#1C7ED6"), "compute": ("#E7F1FB", "#1C7ED6"), "check": ("#FDECEC", "#E03131"),
       "observe": ("#E6F4EA", "#2F9E44"), "hedge": ("#F1ECFD", "#7048E8"), "go": ("#F1F3F5", "#495057")}
HALO = [pe.withStroke(linewidth=2.6, foreground="white")]


def draw_map(ax, D, M, name, title):
    X, Y = D["X"], D["Y"]
    u, v = D[name + "_u"], D[name + "_v"]
    spd = np.where(D["water"], np.hypot(u, v), np.nan)
    ext = [X.min(), X.max(), Y.min(), Y.max()]
    ax.imshow(spd, origin="lower", extent=ext, cmap=SPEED, vmin=0, vmax=1.4, interpolation="bilinear")
    land = np.where(D["water"], np.nan, 1.0)
    ax.imshow(land, origin="lower", extent=ext, cmap=LinearSegmentedColormap.from_list("l", ["#D9D4CC", "#D9D4CC"]),
              interpolation="nearest")
    q = 6
    ax.quiver(X[::q, ::q], Y[::q, ::q], u[::q, ::q], v[::q, ::q], color="#1F2A36", scale=14, width=0.005,
              headwidth=3.6, alpha=0.7)
    ax.add_patch(Circle(tuple(D["c"]), 15.0, facecolor="#ADB5BD", edgecolor="#495057", lw=1.0, hatch="///", alpha=0.9))
    tL, tR = M[f"{name}_time_L"], M[f"{name}_time_R"]
    best = "L" if tL < tR else "R"
    for a, col in (("L", LEFT), ("R", RIGHT)):
        r = D[f"{name}_route_{a}"]
        ax.plot(r[:, 0], r[:, 1], color="white", lw=4.6 if a == best else 3.2, solid_capstyle="round", zorder=3)
        ax.plot(r[:, 0], r[:, 1], color=col, lw=3.0 if a == best else 1.6, ls="-" if a == best else (0, (3, 2)), zorder=4)
    ax.scatter(*D["s"], marker="o", s=42, color="#1F2A36", zorder=5)
    ax.scatter(*D["g"], marker="*", s=120, color="#1F2A36", zorder=5)
    ax.text(0.03, 0.97, title, transform=ax.transAxes, fontsize=8.8, va="top", ha="left", color=st.INK, path_effects=HALO)
    for i, (a, col, t) in enumerate((("L", LEFT, tL), ("R", RIGHT, tR))):
        ax.text(0.03, 0.12 - 0.09 * i, f"{'左' if a == 'L' else '右'}侧 {t:.1f} 小时", transform=ax.transAxes,
                fontsize=8.6, color=col, fontweight="bold" if a == best else "normal", path_effects=HALO)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    keys = ["map_route_L", "map_route_R", "truth_route_L", "truth_route_R"]
    xs = np.r_[D["s"][0], D["g"][0], np.concatenate([D[k][:, 0] for k in keys])]
    ys = np.r_[D["s"][1], D["g"][1], np.concatenate([D[k][:, 1] for k in keys])]
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    half = max(xs.max() - xs.min(), ys.max() - ys.min()) / 2 + 8
    ax.set_xlim(cx - half, cx + half)
    ax.set_ylim(cy - half, cy + half)
    for s_ in ax.spines.values():
        s_.set_visible(True)
        s_.set_color("#3B4652")


def box(ax, x, y, w, h, text, kind, fs=8.4):
    fc, ec = BOX[kind]
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.008,rounding_size=0.02",
                                fc=fc, ec=ec, lw=1.6))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=st.INK)


def arrow(ax, p, q, col="#3B4652"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11, lw=1.5, color=col, shrinkA=2, shrinkB=2))


def main():
    st.setup()
    D = np.load(st.ROOT / "results" / "route_example.npz")
    M = json.load(open(st.ROOT / "results" / "route_example.json", encoding="utf-8"))
    H = 116 * st.MM
    fig = plt.figure(figsize=(st.TEXTW, H))
    W = 0.305
    axs = [fig.add_axes([0.012 + i * (W + 0.025), 0.50, W, W * st.TEXTW / H]) for i in range(3)]
    draw_map(axs[0], D, M, "map", "3 天前的 1° 粗图")
    draw_map(axs[1], D, M, "counter", "同样符合粗图的另一种海流")
    draw_map(axs[2], D, M, "truth", "真实海流（当天）")
    gain = M["truth_time_L"] - M["truth_time_R"]
    for ax, cap in zip(axs, ("(a) 粗图上两侧几乎一样快", "(b) 合理反例：左侧慢得多", f"(c) 真实海流：右侧快 {gain:.1f} 小时")):
        st.caption(ax, cap, y=-0.035)
    ax = fig.add_axes([0.0, 0.075, 1.0, 0.33])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    box(ax, 0.085, 0.45, 0.15, 0.30, "粗图上算出\n左右航时差", "step")
    box(ax, 0.31, 0.83, 0.20, 0.26, "差值小于数值误差：\n加密网格再算", "compute")
    box(ax, 0.31, 0.36, 0.20, 0.42, "合理反例检验：在合理\n集合中找使另一侧更快\n的流场，得最大后悔值", "check")
    box(ax, 0.555, 0.64, 0.17, 0.26, "最大后悔值小：\n按粗图选边", "go")
    box(ax, 0.555, 0.17, 0.17, 0.26, "最大后悔值大：\n粗图不可信", "check")
    box(ax, 0.835, 0.50, 0.24, 0.26, "观测便宜：\n上浮取新图后再定", "observe")
    box(ax, 0.835, 0.16, 0.24, 0.26, "观测太贵：选最大\n后悔值较小的一侧", "hedge")
    arrow(ax, (0.16, 0.55), (0.21, 0.76))
    arrow(ax, (0.16, 0.40), (0.21, 0.38))
    arrow(ax, (0.31, 0.70), (0.31, 0.57))
    arrow(ax, (0.41, 0.46), (0.47, 0.60))
    arrow(ax, (0.41, 0.26), (0.47, 0.20))
    arrow(ax, (0.64, 0.23), (0.715, 0.45))
    arrow(ax, (0.64, 0.16), (0.715, 0.16))
    ax.text(0.5, -0.12, "(d) 数值歧义靠多算，环境歧义靠取新信息", fontsize=9.0, ha="center", va="top", color=st.INK)
    st.save(fig, "fig_route_overview")


if __name__ == "__main__":
    main()
