"""Shared style of the paper's data figures.

Colour carries meaning and keeps it in every figure:
  actions      go = blue, think (high-performance computer) = orange, stop = green
  valuation    the planner's own search score = red, held-out imagined oceans = violet, reality = ink
  controllers  rehearsal on held-out oceans (this paper) = violet, one-step metareasoning that trusts
               the search = red, the same valuing on held-out oceans = light violet, tuned fixed
               strategy = dark grey, survey rules = warm greys
Figures are drawn at the printed width (154 mm text width) so that text prints at its set size.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
MM = 1 / 25.4
TEXTW = 154 * MM

INK, MUTED, GRID = "#1F2A36", "#5C6B7A", "#E6EBF0"
GO, THINK, STOP = "#1C7ED6", "#F08C00", "#2F9E44"
THINK3 = "#FFB547"          # think one interval in three: a lighter orange
STOPTHINK = "#8BBF5A"       # stop and think one in three
SEARCH, HELD, REAL = "#E03131", "#7048E8", INK
REHEARSAL, META, META_HELD, TUNED = "#6741D9", "#E03131", "#B197FC", "#495057"
RULES = {"lawnmower": "#C9B79C", "greedy": "#A68A64", "ucb": "#8D6E4C", "thompson": "#B08968"}
STRAT_COLOR = {"fixed-0": GO, "fixed-1": THINK, "periodic-100": THINK3, "periodic-300": STOPTHINK, "periodic-200": STOP}
CHL = LinearSegmentedColormap.from_list("chl", ["#2f80a6", "#4aa096", "#6eaa60", "#96963c", "#a0692d", "#823c23"])
CHANGE = LinearSegmentedColormap.from_list("change", ["#F7FBF8", "#C7E9DA", "#7CC4B6", "#3A9AA6", "#22577A", "#1B2F4B"])


def setup():
    plt.rcParams.update({
        "font.family": ["Microsoft YaHei"], "font.size": 8.5, "axes.titlesize": 9.0, "axes.labelsize": 8.5,
        "xtick.labelsize": 8.0, "ytick.labelsize": 8.0, "legend.fontsize": 8.0,
        "axes.linewidth": 0.8, "axes.edgecolor": "#3B4652", "axes.labelcolor": INK, "text.color": INK,
        "xtick.color": "#3B4652", "ytick.color": "#3B4652", "xtick.major.width": 0.8, "ytick.major.width": 0.8,
        "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
        "grid.linewidth": 0.7, "axes.axisbelow": True, "legend.frameon": False,
        "mathtext.fontset": "custom", "mathtext.rm": "Cambria", "mathtext.it": "Cambria:italic",
        "mathtext.bf": "Cambria:bold", "axes.unicode_minus": True, "savefig.dpi": 300, "pdf.fonttype": 42,
        "lines.solid_capstyle": "round",
    })


def caption(ax, text, y=-0.30, x=0.5, fig=None):
    """Sub-caption '(a) ...' centred under a panel."""
    ax.text(x, y, text, transform=ax.transAxes, ha="center", va="top", fontsize=9.0, color=INK)


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf")
    fig.savefig(OUT / f"{name}.png", dpi=300)
    print("saved", name)


def minus(x, fmt="{:+.3f}"):
    """Signed number with a true minus sign."""
    return fmt.format(x).replace("-", "−")
