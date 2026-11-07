"""Figure: how fast the satellite chlorophyll map of the East China Sea goes stale.
Rows: spread of the change of log10 chlorophyll over 3 days, per season (from all days
2018-2026); dots: development and test mission windows (spring).
Data: results/atlas/atlas_stats.npz, data/missions/chl_missions.csv
"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
plt.rcParams.update({"font.family": ["Microsoft YaHei"], "font.size": 10, "axes.unicode_minus": False})
A = np.load(ROOT / "results" / "atlas" / "atlas_stats.npz")
lat, lon = A["lat"], A["lon"]
land = np.load(ROOT / "data" / "missions" / "land_mask.npy")
rows = list(csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
seasons = [("spring", "春季（3–5 月）"), ("summer", "夏季（6–8 月）"), ("autumn", "秋季（9–11 月）"), ("winter", "冬季（12–2 月）")]
fig, ax = plt.subplots(1, 4, figsize=(7.16, 2.5), sharey=True)
ext = [lon[0], lon[-1], lat[0], lat[-1]]
for k, (s, title) in enumerate(seasons):
    v = A[f"sd_{s}_3"]
    im = ax[k].imshow(v, origin="lower", extent=ext, cmap="YlOrRd", vmin=0.0, vmax=0.35)
    ax[k].imshow(np.where(land, 1.0, np.nan), origin="lower", extent=ext, cmap="Greys", vmin=0, vmax=2.5)
    if s == "spring":
        for r in rows:
            ax[k].plot(float(r["lon0"]), float(r["lat0"]), ".", ms=2,
                       color="#1864ab" if r["split"] == "dev" else "#2b8a3e")
    ax[k].set_title(title, fontsize=9.5)
    ax[k].set_xlabel("经度（°E）", fontsize=9)
    ax[k].set_xticks([120, 123, 126], ["120", "123", "126"])
    ax[k].set_yticks([26, 28, 30, 32], ["26", "28", "30", "32"])
ax[0].set_ylabel("纬度（°N）", fontsize=9)
from matplotlib.lines import Line2D
ax[0].legend(handles=[Line2D([], [], ls="", marker=".", ms=6, color="#1864ab", label="开发 2018–2022"),
                      Line2D([], [], ls="", marker=".", ms=6, color="#2b8a3e", label="测试 2023–2026")],
             loc="lower right", fontsize=6.5, frameon=True, framealpha=0.9, handletextpad=0.1, borderpad=0.3)
fig.subplots_adjust(left=0.075, right=0.875, bottom=0.2, top=0.88, wspace=0.12)
fig.canvas.draw()
p0, p3 = ax[0].get_position(), ax[3].get_position()
cax = fig.add_axes([p3.x1 + 0.015, p3.y0, 0.012, p3.height])
cb = fig.colorbar(im, cax=cax)
cb.set_label("3 天内对数叶绿素" + chr(10) + "变化的标准差", fontsize=8)
plt.savefig(ROOT / "paper" / "figures" / "fig_atlas.png", dpi=300, bbox_inches=None)
plt.savefig(ROOT / "paper" / "figures" / "fig_atlas.pdf")
print("saved")
