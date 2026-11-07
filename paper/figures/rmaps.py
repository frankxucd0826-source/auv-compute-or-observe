"""Dark top-view maps of one mission: current speed, streamlines, the no-go zone and both routes."""
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, FancyBboxPatch, Polygon
from matplotlib import patheffects as pe
from matplotlib.font_manager import FontProperties

import rstyle as st

SEA = LinearSegmentedColormap.from_list(
    "sea", ["#0D1F33", "#14365A", "#1C5583", "#2A78A6", "#4D9EC2", "#86C6DB", "#C4E8F0"])
SEA_VMAX = 1.0
NIGHT = "#0D1F33"          # darkest sea; also the legend band
GOLD, PINK = "#FFC53D", "#FF6B9A"   # left and right side on dark maps
GOLD_D, PINK_D = "#D99A00", "#D6336C"   # the same sides on white paper
SIDE = {"L": GOLD, "R": PINK}
SIDE_D = {"L": GOLD_D, "R": PINK_D}
NAME = {"L": "左侧", "R": "右侧"}


def view(D, pad=10.0):
    keys = [k for k in D.keys() if "_route_" in k]
    xs = np.r_[D["s"][0], D["g"][0], np.concatenate([D[k][:, 0] for k in keys])]
    ys = np.r_[D["s"][1], D["g"][1], np.concatenate([D[k][:, 1] for k in keys])]
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    half = max(xs.max() - xs.min(), ys.max() - ys.min()) / 2 + pad
    return cx - half, cx + half, cy - half, cy + half


def draw(ax, D, name, times, frame="#8A99A8", tags=True, lw=2.6, stream=True, scale_bar=False):
    """One field with both fastest routes; the faster side solid, the slower dashed."""
    X, Y = D["X"], D["Y"]
    u, v = D[name + "_u"], D[name + "_v"]
    spd = np.hypot(u, v)
    ext = [X.min(), X.max(), Y.min(), Y.max()]
    ax.imshow(spd, origin="lower", extent=ext, cmap=SEA, vmin=0, vmax=SEA_VMAX, interpolation="bicubic", zorder=0)
    if stream:
        ax.streamplot(X[0, :], Y[:, 0], u, v, density=1.25, color="white", linewidth=0.45, arrowsize=0.55,
                      arrowstyle="-|>", broken_streamlines=True, zorder=1)
        for c in ax.collections[-1:]:
            c.set_alpha(0.38)
        for p in ax.patches[-200:]:
            p.set_alpha(0.38)
    c = tuple(D["c"])
    ax.add_patch(Circle(c, 15.0, facecolor="#E03131", alpha=0.42, edgecolor="none", zorder=2))
    ax.add_patch(Circle(c, 15.0, facecolor="none", edgecolor="#FFC9C9", hatch="////", lw=0, zorder=2))
    ax.add_patch(Circle(c, 15.0, facecolor="none", edgecolor="white", lw=1.0, zorder=3))
    best = min("LR", key=lambda a: times[a])
    for a in "LR":
        r = D[f"{name}_route_{a}"]
        w = lw if a == best else lw * 0.62
        ls = "-" if a == best else (0, (2.6, 1.6))
        ax.plot(r[:, 0], r[:, 1], color=NIGHT, lw=w + 2.2, solid_capstyle="round", zorder=4, alpha=0.9)
        ax.plot(r[:, 0], r[:, 1], color=SIDE[a], lw=w, ls=ls, solid_capstyle="round", dash_capstyle="round", zorder=5)
    ax.scatter(*D["s"], marker="o", s=34, color="white", edgecolor=NIGHT, lw=1.0, zorder=6)
    ax.scatter(*D["g"], marker="*", s=110, color="white", edgecolor=NIGHT, lw=0.8, zorder=6)
    x0, x1, y0, y1 = view(D)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for s_ in ax.spines.values():
        s_.set_visible(True)
        s_.set_color(frame)
        s_.set_linewidth(1.8)
    if tags:
        for a in "LR":
            tag_side(ax, D, name, a, times[a], bold=(a == best))
    if scale_bar:
        L = 50.0
        xb, yb = x0 + 0.06 * (x1 - x0), y0 + 0.06 * (y1 - y0)
        ax.plot([xb, xb + L], [yb, yb], color="white", lw=2.0, solid_capstyle="butt", zorder=7)
        ax.text(xb + L / 2, yb + 0.025 * (y1 - y0), "50 千米", color="white", ha="center", va="bottom",
                fontsize=7.6, zorder=7)
    return best


def tag_side(ax, D, name, a, t, bold=False):
    """Time label just outside the route's widest point, in a dark rounded box."""
    r = D[f"{name}_route_{a}"]
    s, g = np.asarray(D["s"], float), np.asarray(D["g"], float)
    d = (g - s) / np.linalg.norm(g - s)
    n = np.array([-d[1], d[0]])                       # left normal of the start-goal line
    off = (r - s) @ n
    i = int(np.argmax(off) if a == "L" else np.argmin(off))
    p = r[i] + n * (9.0 if a == "L" else -9.0)
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    p[0] = np.clip(p[0], x0 + 0.17 * (x1 - x0), x1 - 0.17 * (x1 - x0))
    p[1] = np.clip(p[1], y0 + 0.08 * (y1 - y0), y1 - 0.08 * (y1 - y0))
    fp = FontProperties(family=["Times New Roman", "SimHei"] if bold else ["Times New Roman", "SimSun"],
                        size=8.2, weight="bold" if bold else "normal")
    ax.text(p[0], p[1], f"{NAME[a][0]} {t:.1f} 小时", color=SIDE[a], ha="center", va="center", fontproperties=fp,
            zorder=8, bbox=dict(boxstyle="round,pad=0.22,rounding_size=0.35", fc=NIGHT, ec=SIDE[a], lw=0.8, alpha=0.92))


def hollow_arrow(fig, x, y, w=0.014, h=0.05, col="#8A99A8"):
    """A hollow triangle pointing right, in figure coordinates (x, y = centre)."""
    tri = Polygon([[x - w / 2, y - h / 2], [x - w / 2, y + h / 2], [x + w / 2, y]], closed=True,
                  transform=fig.transFigure, fc="white", ec=col, lw=1.3)
    fig.patches.append(tri)


def dark_tag(ax, x, y, text, col="white", size=8.0, **kw):
    fp = FontProperties(family=["Times New Roman", "SimSun"], size=size)
    return ax.text(x, y, text, color=col, fontproperties=fp, zorder=8,
                   bbox=dict(boxstyle="round,pad=0.25,rounding_size=0.3", fc=NIGHT, ec="none", alpha=0.85), **kw)
