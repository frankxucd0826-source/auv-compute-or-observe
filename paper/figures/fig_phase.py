"""Figure 8: which fixed way of spending time wins depends on the vehicle and the map.
Grid: speed of the low-power computer (x) by how far the real ocean departs from the satellite
map (y); 60 development missions per cell, the five fixed strategies on the same missions.
(a) the strategy with the lowest time-averaged regret, coloured only where it beats always
    going clearly (95% interval of the paired difference below zero); the number is its regret
    minus that of always going; grey "≈" = nothing clearly better than always going.
(b) how much worse the better of the two stopping strategies is than the best strategy that
    never stops (positive everywhere = stopping never pays).
Data: results/phase_<tag>_rl*_se*/results.jsonl     python -E -X utf8 paper/figures/fig_phase.py v3
"""
import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "paper"))
from terms import STRATEGY as NAMES  # noqa: E402

TAG = sys.argv[1] if len(sys.argv) > 1 else "v3"
import style as SS  # noqa: E402
SS.setup()
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm  # noqa: E402
ORDER = list(NAMES)                          # fixed-0, fixed-1, periodic-100, periodic-300, periodic-200
COLORS = {"fixed-1": "#ff8787", "periodic-100": "#ffc078", "periodic-300": "#b197fc", "periodic-200": "#8ce99a"}
TIE = "#e9ecef"
MOVE, STOP = ["fixed-0", "fixed-1", "periodic-100"], ["periodic-300", "periodic-200"]
rng = np.random.default_rng(0)


def ci(d, n=2000):
    d = d[np.isfinite(d)]
    bs = [d[rng.integers(len(d), size=len(d))].mean() for _ in range(n)]
    return d.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5)


rows = []
for d in sorted((ROOT / "results").glob(f"phase_{TAG}_rl*_se*")):
    m = re.search(r"rl([\d.]+)_se([\d.]+)", d.name)
    f = d / "results.jsonl"
    if not (d / "done").exists() or not f.exists():
        continue
    df = pd.DataFrame([json.loads(l) for l in open(f, encoding="utf-8")])
    P = df.pivot_table(index=["mission", "lag"], columns="controller", values="regret_avg")
    if not set(ORDER) <= set(P.columns):
        continue
    P = P[ORDER].dropna()
    best = P.mean().idxmin()
    r = dict(rl=float(m.group(1)), se=float(m.group(2)), n=len(P), best=best, **P.mean().to_dict())
    think = min(["fixed-1", "periodic-100"], key=lambda c: P[c].mean())
    r["think"] = think
    r["gain"], r["lo"], r["hi"] = ci((P[think] - P["fixed-0"]).to_numpy())
    # better stopping strategy minus best moving strategy (means over missions); interval by resampling missions
    r["stop"] = P[STOP].mean().min() - P[MOVE].mean().min()
    X = P.to_numpy()
    bs = []
    for _ in range(1000):
        mu = X[rng.integers(len(X), size=len(X))].mean(axis=0)
        bs.append(mu[[ORDER.index(c) for c in STOP]].min() - mu[[ORDER.index(c) for c in MOVE]].min())
    r["stop_lo"], r["stop_hi"] = np.percentile(bs, 2.5), np.percentile(bs, 97.5)
    rows.append(r)
T = pd.DataFrame(rows)
if T.empty:
    sys.exit("no finished phase runs for tag " + TAG)
rls, ses = sorted(T.rl.unique()), sorted(T.se.unique())


fig, ax = plt.subplots(1, 2, figsize=(SS.TEXTW, 62 * SS.MM), gridspec_kw=dict(width_ratios=[1, 1]))
fig.subplots_adjust(left=0.135, right=0.985, top=0.95, bottom=0.30, wspace=0.10)
A, B = ax
DIV = LinearSegmentedColormap.from_list("gain", ["#E8590C", "#FFC078", "#FFF4E6", "#F1F3F5", "#DEE2E6"])
SEQ = LinearSegmentedColormap.from_list("stop", ["#EBFBEE", "#B2F2BB", "#69DB7C", "#2F9E44", "#1B5E20"])
G = np.full((len(ses), len(rls)), np.nan)
Sg = np.full((len(ses), len(rls)), np.nan)
for _, r in T.iterrows():
    G[ses.index(r.se), rls.index(r.rl)] = r.gain
    Sg[ses.index(r.se), rls.index(r.rl)] = r.stop
imA = A.imshow(G, origin="lower", cmap=DIV, norm=TwoSlopeNorm(vmin=-0.14, vcenter=0.0, vmax=0.02), aspect="auto")
imB = B.imshow(Sg, origin="lower", cmap=SEQ, vmin=0.0, vmax=0.13, aspect="auto")
for _, r in T.iterrows():
    i, j = ses.index(r.se), rls.index(r.rl)
    clear = r.hi < 0
    A.text(j, i, SS.minus(r.gain), ha="center", va="center", fontsize=7.6,
           color="white" if r.gain < -0.07 else SS.INK, fontweight="bold" if clear else "normal")
    if clear:
        A.add_patch(plt.Rectangle((j - 0.48, i - 0.48), 0.96, 0.96, fill=False, ec=SS.INK, lw=1.3))
    B.text(j, i, SS.minus(r.stop), ha="center", va="center", fontsize=7.6,
           color="white" if r.stop > 0.085 else SS.INK, fontweight="bold" if r.stop_lo > 0 else "normal")
ylab = {0.0: "0（当天卫星图）", 0.05: "0.05", 0.15: "0.15", 0.3: "0.30"}
for a in (A, B):
    a.set_xticks(range(len(rls)), [f"{v:g}" for v in rls])
    a.set_yticks(range(len(ses)), [ylab.get(v, f"{v:g}") for v in ses] if a is A else [])
    a.set_xlabel("低功耗计算机速度（次推演/分钟）")
    a.grid(False)
    a.tick_params(length=0)
    for sp in a.spines.values():
        sp.set_visible(False)
A.set_ylabel("真实海洋偏离卫星图的程度")
SS.caption(A, "(a) 深想相对一直走的遗憾差（加框：显著更好）", y=-0.36)
SS.caption(B, "(b) 中途停下比不停多出的遗憾（全部显著）", y=-0.36)
SS.save(fig, "fig_phase")
print(T[["rl", "se", "n", "think", "gain", "lo", "hi", "stop", "stop_lo", "stop_hi"]].round(3).to_string())
