"""Figure: one test mission with a slow onboard computer (5 rollouts per minute).
(a) the 3-day-old satellite map the vehicle carries; (b) the ocean it actually meets, with the
tracks of "always go" and "think one interval in three" (thick where the high-performance
computer ran) and the true densest water; (c) how far the vehicle's answer is from the densest
water, over the 24-hour window.
Mission choice (stated rule): the first test mission, in date order, on which the two
strategies differ by more than 0.1 in time-averaged regret (results/main_v3_test_weak).
"""
import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "paper"))
from terms import STRATEGY  # noqa: E402
from oceanmeta.belief import gaussian_random_fields  # noqa: E402
from oceanmeta.mission import Sensor, MissionConfig, run_mission  # noqa: E402
from oceanmeta.platforms import auv  # noqa: E402
from oceanmeta.meta import Fixed, Periodic  # noqa: E402

import style as SS  # noqa: E402
SS.setup()
from scipy.ndimage import zoom  # noqa: E402
import matplotlib.patheffects as pe  # noqa: E402
CHL = LinearSegmentedColormap.from_list("chl", ["#2f80a6", "#4aa096", "#6eaa60", "#96963c", "#a0692d", "#823c23"])

df = pd.DataFrame([json.loads(l) for l in open(ROOT / "results" / "main_v3_test_weak" / "results.jsonl", encoding="utf-8")])
rows = list(csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
p = df[df.controller.isin(["fixed-0", "periodic-100"])].pivot_table(index="mission", columns="controller", values="regret_avg")
p["diff"] = p["fixed-0"] - p["periodic-100"]
cand = [int(r["id"]) for r in sorted(rows, key=lambda r: r["date"]) if int(r["id"]) in p.index and p.loc[int(r["id"]), "diff"] > 0.1]
i = cand[0]
row = rows[i]
M = np.load(ROOT / "data" / "missions" / "chl_missions.npz")
st = json.load(open(ROOT / "data" / "missions" / "prior_stats.json", encoding="utf-8"))
li = list(M["lags"]).index(3)
mask = M["mask"][i]
truth = M["truth"][i] + 0.15 * gaussian_random_fields(1, 40, 40, 3.0, np.random.default_rng(7919 * i + 1))[0]
prior = M["prior"][i, li]
sd = float(np.hypot(st["sd"]["3"], 0.15))
start = (float(row["start_x"]), float(row["start_y"]))
plat = auv(rate_low=5, rate_high=250, p_think=20)
cfg = MissionConfig(prior_length_cells=st["length_cells"]["3"])
runs = {}
GO, T3 = STRATEGY["fixed-0"], STRATEGY["periodic-100"]
for name, ctl in ((GO, Fixed(0)), (T3, Periodic([1, 0, 0]))):
    out, m = run_mission(truth, prior, sd, mask, start, plat, Sensor(noise_sd=0.1), cfg, ctl, seed=0 * 100003 + i * 31 + 3)
    runs[name] = (out, m)


fig = plt.figure(figsize=(SS.TEXTW, 66 * SS.MM))
vmin, vmax = np.percentile(truth[mask], [2, 99.5])
ext = [0, 80, 0, 80]          # cell k spans 2k..2k+2 km; positions in cells map to 2x+1 km


def smooth(f):
    big = zoom(np.where(mask, f, np.nanmedian(f[mask])), 8, order=3)
    m = zoom(mask.astype(float), 8, order=0) > 0.5
    return np.where(m, big, np.nan)


def draw_map(ax, f):
    ax.set_facecolor("#D9DEE3")
    im = ax.imshow(smooth(f), origin="lower", cmap=CHL, vmin=vmin, vmax=vmax, extent=ext, interpolation="bilinear")
    ax.set_xticks([0, 40, 80], ["0", "40", "80 km"])
    ax.set_yticks([0, 40, 80], ["0", "40", "80"])
    ax.grid(False)
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_color("#6B7A89")
    return im


ax0 = fig.add_axes([0.040, 0.24, 0.235, 0.70])
draw_map(ax0, prior)
ax0.plot(start[0] * 2 + 1, start[1] * 2 + 1, "^", ms=9, color="white", mec=SS.INK, mew=1.2, zorder=5)
ax0.text(start[0] * 2 - 2, start[1] * 2 - 5, "出发", ha="right", fontsize=8, color="white", fontweight="bold",
         path_effects=[pe.withStroke(linewidth=2.2, foreground=SS.INK)])
ax1 = fig.add_axes([0.300, 0.24, 0.235, 0.70])
im = draw_map(ax1, truth)
ty, tx = np.unravel_index(np.argmax(np.where(mask, truth, -9)), truth.shape)
cols = {GO: SS.GO, T3: SS.THINK}
halo = [pe.Stroke(linewidth=4.6, foreground="white"), pe.Normal()]
for name, (out, m) in runs.items():
    pos = [start] + m.log.positions
    xs = [p_[0] * 2 + 1 for p_ in pos]
    ys = [p_[1] * 2 + 1 for p_ in pos]
    ax1.plot(xs, ys, color=cols[name], lw=2.2, path_effects=halo, zorder=3)
    for t, a in enumerate(m.log.actions):
        if a in (1, 3):
            ax1.plot(xs[t:t + 2], ys[t:t + 2], color=cols[name], lw=4.2, solid_capstyle="round", zorder=4)
    ax1.plot(xs[-1], ys[-1], "o", ms=5.5, color=cols[name], mec="white", mew=1.0, zorder=5)
ax1.plot(tx * 2 + 1, ty * 2 + 1, "o", ms=17, color="white", alpha=0.55, zorder=4)
ax1.plot(tx * 2 + 1, ty * 2 + 1, "*", ms=14, color="#FFD43B", mec=SS.INK, mew=0.9, zorder=6)
ax1.plot(start[0] * 2 + 1, start[1] * 2 + 1, "^", ms=9, color="white", mec=SS.INK, mew=1.2, zorder=6)
ax1.text(tx * 2 + 5, ty * 2 + 4, "真实最浓处", fontsize=7.8, color="white", fontweight="bold", zorder=7,
         path_effects=[pe.withStroke(linewidth=2.2, foreground=SS.INK)])
fig.canvas.draw()
b1 = ax1.get_position()
cax = fig.add_axes([b1.x1 + 0.008, b1.y0, 0.009, b1.height])
cb = fig.colorbar(im, cax=cax)
cb.outline.set_visible(False)
cb.ax.tick_params(labelsize=7.2)
cb.set_label("对数叶绿素浓度", fontsize=7.6)
ax2 = fig.add_axes([0.705, 0.24, 0.275, 0.70])
for name, (out, m) in runs.items():
    tmax = out["true_max"]
    ts = [a for a, _ in m.answers] + [24 * 60]
    vs = [tmax - v for _, v in m.answers]
    ax2.step(np.array(ts[:-1]) / 60, vs, where="post", color=cols[name], lw=2.4)
    ax2.hlines(vs[-1], ts[-2] / 60, 24, color=cols[name], lw=2.4)
ax2.set_xlim(0, 24)
ax2.set_ylim(-0.02, 0.75)
ax2.set_xticks([0, 6, 12, 18, 24])
ax2.text(1.0, -0.085, "h", transform=ax2.transAxes, ha="left", va="top", fontsize=8)
ax2.set_ylabel("所报位置与最浓处之差（对数浓度）", fontsize=7.8)
ax2.text(23.6, 0.55, f"{GO}：平均 {runs[GO][0]['regret_avg']:.2f}", color=cols[GO], fontsize=8, ha="right", va="bottom",
         fontweight="bold")
ax2.text(0.6, 0.05, f"{T3}" + chr(10) + f"平均 {runs[T3][0]['regret_avg']:.2f}", color=cols[T3], fontsize=8, ha="left", va="bottom",
         fontweight="bold")
fig.canvas.draw()
for ax_, t_ in ((ax0, "(a) 携带的 3 天前卫星图"), (ax1, "(b) 真实海洋与两条航迹"), (ax2, "(c) 应急中心随时得到的答案")):
    bb = ax_.get_position()
    fig.text((bb.x0 + bb.x1) / 2, 0.03, t_, ha="center", va="bottom", fontsize=9.0, color=SS.INK)
SS.save(fig, "fig_example")
print("mission", i, row["date"], {k: round(v[0]["regret_avg"], 3) for k, v in runs.items()})
