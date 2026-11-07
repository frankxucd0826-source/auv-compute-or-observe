"""Shared style of the route-decision figures.

Serif type as in the body text (Times New Roman for Latin and numbers, SimSun for Chinese, SimHei for
bold Chinese headings); figures are drawn at the printed width (154 mm text width) so that text prints
at its set size. Colour carries meaning and keeps it in every figure:
  this paper (maximum regret, plausible counterexample test)  blue
  ensemble methods (random members)                           violet
  the coarse map and the baseline that follows it             slate grey
  getting new information (surfacing for a new map)           teal
  computing more on the same map                              amber
  measuring on the spot                                       green
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import patheffects as pe  # noqa: E402
from matplotlib.font_manager import FontProperties  # noqa: E402

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
MM = 1 / 25.4
TEXTW = 154 * MM

INK, MUTED, FAINT, GRID = "#1F2A36", "#5C6B7A", "#9AA5B1", "#E3E8EE"
OURS, OURS_LIGHT = "#1F5FAE", "#C9DBF2"
ENS, ENS_LIGHT = "#7B4FB8", "#E2D6F3"
MAP, MAP_LIGHT = "#5F6B7A", "#DDE2E8"
OBS, OBS_LIGHT = "#0F8A7E", "#CDEBE7"
COMPUTE, COMPUTE_LIGHT = "#D9480F", "#FBE3D3"
SPOT = "#3B8C2E"
LEFT, RIGHT = "#F59F00", "#E64980"          # the two sides of the no-go zone
WARM_BG, COOL_BG = "#FBEFE6", "#E7F0FA"     # bands that name regimes

SERIF = ["Times New Roman", "SimSun"]
BOLD = ["Times New Roman", "SimHei"]


def setup():
    plt.rcParams.update({
        "font.family": SERIF, "font.size": 9.0, "axes.titlesize": 9.5, "axes.labelsize": 9.0,
        "xtick.labelsize": 8.5, "ytick.labelsize": 8.5, "legend.fontsize": 8.5,
        "axes.linewidth": 0.9, "axes.edgecolor": "#3B4652", "axes.labelcolor": INK, "text.color": INK,
        "xtick.color": "#3B4652", "ytick.color": "#3B4652", "xtick.major.width": 0.9, "ytick.major.width": 0.9,
        "xtick.major.size": 3.0, "ytick.major.size": 3.0,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.7, "axes.axisbelow": True,
        "axes.spines.top": False, "axes.spines.right": False,
        "mathtext.fontset": "stix", "axes.unicode_minus": False,
        "savefig.dpi": 300, "pdf.fonttype": 42, "svg.fonttype": "none",
    })


def bold(size=9.5):
    return FontProperties(family=BOLD, weight="bold", size=size)


def panel_title(ax, text, x=0.0, y=1.03, size=9.5):
    """'(a) ...' above the panel, left aligned, in bold heading type."""
    ax.text(x, y, text, transform=ax.transAxes, ha="left", va="bottom", fontproperties=bold(size), color=INK)


def halo(artist, w=3.0, col="white"):
    artist.set_path_effects([pe.withStroke(linewidth=w, foreground=col)])
    return artist


def note(ax, x, y, text, col=INK, size=8.5, ha="left", va="center", weight=None, w=2.6, **kw):
    """Text with a white halo so that it stays readable over lines and grid."""
    fp = bold(size) if weight == "bold" else FontProperties(family=SERIF, size=size)
    t = ax.text(x, y, text, color=col, ha=ha, va=va, fontproperties=fp, **kw)
    return halo(t, w)


def minus(v, fmt="{:.2f}"):
    """A signed number with a true minus sign."""
    s = fmt.format(abs(v))
    return ("−" if v < 0 else "+") + s


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf")
    fig.savefig(OUT / f"{name}.png", dpi=300)
    plt.close(fig)
    print("saved", name)
