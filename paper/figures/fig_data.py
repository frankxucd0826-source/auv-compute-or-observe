"""Figure 2: what eight years of satellite chlorophyll tell the vehicle, and what they cannot.
(a)-(d) spread of the 3-day change of log10 chlorophyll per season (all 3197 days), with the
        spring mission windows; (e) error of a k-day-old map in the mission windows (development
        years), against the difference between satellite and in-situ chlorophyll; (f) a deep
        spatio-temporal forecaster against simply keeping the latest map (test years).
Data: results/atlas/atlas_stats.npz, data/missions/prior_stats.json, results/worldmodel_eval.json,
data/missions/chl_missions.csv
"""
import csv
import json

import numpy as np
import style as S
from style import plt

S.setup()
A = np.load(S.ROOT / "results" / "atlas" / "atlas_stats.npz")
lat, lon = A["lat"], A["lon"]
land = np.load(S.ROOT / "data" / "missions" / "land_mask.npy")
rows = list(csv.DictReader(open(S.ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
st = json.load(open(S.ROOT / "data" / "missions" / "prior_stats.json", encoding="utf-8"))
wm = json.load(open(S.ROOT / "results" / "worldmodel_eval.json", encoding="utf-8"))
wm = wm[next(iter(wm))]

fig = plt.figure(figsize=(S.TEXTW, 120 * S.MM))
gs_top = fig.add_gridspec(1, 4, left=0.065, right=0.885, top=0.945, bottom=0.585, wspace=0.07)
ext = [lon[0], lon[-1], lat[0], lat[-1]]
seasons = [("spring", "春季（3–5 月）"), ("summer", "夏季（6–8 月）"), ("autumn", "秋季（9–11 月）"),
           ("winter", "冬季（12–2 月）")]
for k, (s, title) in enumerate(seasons):
    ax = fig.add_subplot(gs_top[0, k])
    v = A[f"sd_{s}_3"]
    im = ax.imshow(v, origin="lower", extent=ext, cmap=S.CHANGE, vmin=0.0, vmax=0.30, interpolation="bilinear")
    ax.imshow(np.where(land, 1.0, np.nan), origin="lower", extent=ext, cmap="Greys", vmin=0, vmax=3.2,
              interpolation="nearest")
    med = float(np.nanmedian(v))
    ax.text(0.96, 0.95, f"中位数 {med:.3f}", transform=ax.transAxes, ha="right", va="top", fontsize=7.6,
            color=S.INK, bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.85))
    if s == "spring":
        for split, kw in (("dev", dict(mfc="white", mec=S.INK, mew=0.5)), ("test", dict(mfc=S.INK, mec="white", mew=0.3))):
            xs = [float(r["lon0"]) for r in rows if r["split"] == split]
            ys = [float(r["lat0"]) for r in rows if r["split"] == split]
            ax.plot(xs, ys, "o", ms=2.6, ls="", **kw)
        ax.plot([], [], "o", ms=3.5, mfc="white", mec=S.INK, mew=0.6, ls="", label="开发任务 274")
        ax.plot([], [], "o", ms=3.5, mfc=S.INK, mec="white", ls="", label="测试任务 148")
        ax.legend(loc="lower left", fontsize=7.0, handletextpad=0.1, borderpad=0.25, frameon=True,
                  framealpha=0.92, edgecolor="none", borderaxespad=0.3)
    ax.set_title(title, fontsize=8.8, pad=3)
    ax.set_xticks([120, 123, 126], ["120°E", "123°E", "126°E"], fontsize=7.4)
    ax.set_yticks([26, 28, 30, 32], ["26°N", "28°N", "30°N", "32°N"] if k == 0 else [], fontsize=7.4)
    ax.grid(False)
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_color("#6B7A89")
    ax.text(0.04, 0.95, "abcd"[k], transform=ax.transAxes, fontsize=9, fontweight="bold", va="top",
            bbox=dict(boxstyle="circle,pad=0.12", fc="white", ec="none", alpha=0.9))
cax = fig.add_axes([0.897, 0.605, 0.012, 0.32])
cb = fig.colorbar(im, cax=cax)
cb.outline.set_visible(False)
cb.set_ticks([0, 0.1, 0.2, 0.3])
cb.ax.tick_params(labelsize=7.4)
cb.set_label("3 天内对数浓度变化的标准差", fontsize=7.8)

# (e) how wrong a stale map is, by age
gs_bot = fig.add_gridspec(1, 2, left=0.085, right=0.975, top=0.445, bottom=0.135, wspace=0.30)
ax = fig.add_subplot(gs_bot[0, 0])
ks = [1, 2, 3]
sk = [st["sd"][str(k)] for k in ks]
ax.bar(ks, sk, width=0.58, color=["#9CC3E6", "#5B9BD5", "#2E5E8C"], zorder=3)
ax.bar([4.35], [0.15], width=0.58, color="white", edgecolor=S.MUTED, hatch="////", lw=0.9, zorder=3)
for k, v in zip(ks + [4.35], sk + [0.15]):
    ax.text(k, v + 0.006, f"{v:.3f}" if k != 4.35 else "≈0.15", ha="center", va="bottom", fontsize=8.2, color=S.INK)
ax.axvline(3.68, color="#C5CED8", lw=0.8, ls=":")
ax.set_xticks(ks + [4.35], ["1 天前", "2 天前", "3 天前", "卫星与实测" + chr(10) + "（同一天）"])
ax.set_xlim(0.45, 4.9)
ax.set_ylim(0, 0.25)
ax.set_ylabel("旧图误差 $s_k$（对数浓度）")
ax.grid(axis="x", visible=False)
S.caption(ax, "(e) 旧图越旧误差越大，3 天时超过卫星自身误差", y=-0.30)

# (f) a deep forecaster does not beat keeping the latest map
ax = fig.add_subplot(gs_bot[0, 1])
leads = [1, 2, 3]
rm = [wm[str(k)]["rmse_model"] for k in leads]
rp = [wm[str(k)]["rmse_persistence"] for k in leads]
for k, a, b in zip(leads, rm, rp):
    ax.plot([k - 0.13, k + 0.13], [b, a], color="#C5CED8", lw=1.6, zorder=2)
ax.plot([k - 0.13 for k in leads], rp, "o", ms=7, color=S.MUTED, zorder=3, label="沿用最新的卫星图")
ax.plot([k + 0.13 for k in leads], rm, "D", ms=6.4, color=S.GO, zorder=3, label="深度时空预测模型（550 万参数）")
for k, a, b in zip(leads, rm, rp):
    ax.text(k, max(a, b) + 0.0035, S.minus((a - b) / b * 100, "{:+.1f}") + "%", ha="center", fontsize=7.8,
            color=S.INK)
ax.set_xticks(leads, ["提前 1 天", "提前 2 天", "提前 3 天"])
ax.set_xlim(0.5, 3.5)
ax.set_ylim(0.11, 0.172)
ax.set_ylabel("预报误差（对数浓度）")
ax.legend(loc="upper left", fontsize=7.6, handletextpad=0.3, borderaxespad=0.1)
ax.text(3.45, 0.1135, "百分数：模型比沿用最新图多出的误差", fontsize=7.2, color=S.MUTED, va="bottom", ha="right")
ax.grid(axis="x", visible=False)
S.caption(ax, "(f) 深度预测不比沿用最新图更准（测试年份）", y=-0.30)
S.save(fig, "fig_data")
