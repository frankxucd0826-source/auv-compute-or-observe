"""Draw one mission (for checking behaviour, not a paper figure): the stale map the vehicle
starts with, the real field, the track coloured by how each interval was spent, the reported
water and the true densest water.

    python experiments/plot_mission.py --mission 5 --controllers fixed-0 fixed-1 --out check.png
"""
import argparse
import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))
from oceanmeta.belief import gaussian_random_fields  # noqa: E402
from oceanmeta.mission import Sensor, MissionConfig, run_mission  # noqa: E402
from oceanmeta.platforms import auv  # noqa: E402
from run import make_controller  # noqa: E402

COLORS = ["#2b7bba", "#e8590c", "#2f9e44", "#9c36b5"]
LABELS = ["go, low-power planning", "go, deep planning", "drift and resample", "drift, deep planning"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mission", type=int, required=True)
    ap.add_argument("--controllers", nargs="+", default=["fixed-0", "fixed-1"])
    ap.add_argument("--lag", type=int, default=3)
    ap.add_argument("--rate-low", type=float, default=100)
    ap.add_argument("--p-think", type=float, default=20)
    ap.add_argument("--sat-err", type=float, default=0.15)
    ap.add_argument("--noise", type=float, default=0.1)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    M = np.load(ROOT / "data" / "missions" / "chl_missions.npz")
    rows = list(csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
    stats = json.load(open(ROOT / "data" / "missions" / "prior_stats.json", encoding="utf-8"))
    i = a.mission
    li = list(M["lags"]).index(a.lag)
    mask = M["mask"][i]
    truth = M["truth"][i] + a.sat_err * gaussian_random_fields(1, 40, 40, 3.0, np.random.default_rng(7919 * i + 1))[0]
    prior = M["prior"][i, li]
    sd = float(np.hypot(stats["sd"][str(a.lag)], a.sat_err))
    start = (float(rows[i]["start_x"]), float(rows[i]["start_y"]))
    plat = auv(rate_low=a.rate_low, rate_high=50 * a.rate_low, p_think=a.p_think)
    cfg = MissionConfig(prior_length_cells=stats["length_cells"][str(a.lag)])
    k = len(a.controllers)
    fig, ax = plt.subplots(1, k + 1, figsize=(4.2 * (k + 1), 4.2))
    vmin, vmax = np.percentile(truth[mask], [2, 99.8])
    ax[0].imshow(np.where(mask, prior, np.nan), origin="lower", vmin=vmin, vmax=vmax, cmap="viridis")
    ax[0].set_title(f"map {a.lag} days old ({rows[i]['date']})", fontsize=9)
    ty, tx = np.unravel_index(np.argmax(np.where(mask, truth, -9)), truth.shape)
    for j, spec in enumerate(a.controllers):
        out, m = run_mission(truth, prior, sd, mask, start, plat, Sensor(noise_sd=a.noise), cfg,
                             make_controller(spec), seed=1000 + i)
        A = ax[j + 1]
        A.imshow(np.where(mask, truth, np.nan), origin="lower", vmin=vmin, vmax=vmax, cmap="viridis")
        pos = [start] + m.log.positions
        for t, act in enumerate(m.log.actions):
            (x0, y0), (x1, y1) = pos[t], pos[t + 1]
            A.plot([x0, x1], [y0, y1], color=COLORS[act], lw=2.2)
            if act in (2, 3):
                A.plot(x1, y1, "o", color=COLORS[act], ms=4)
        A.plot(*start, "w^", ms=8, mec="k")
        A.plot(tx, ty, "r*", ms=13, mec="k")
        if "cell" in out:
            A.plot(out["cell"][1], out["cell"][0], "s", mfc="none", mec="w", ms=10, mew=2)
        A.set_title(f"{spec}: regret {out['regret']:.3f}, {out['time_h']:.1f} h", fontsize=9)
    for j, l in enumerate(LABELS):
        ax[0].plot([], [], color=COLORS[j], lw=3, label=l)
    ax[0].legend(fontsize=7, loc="lower left")
    plt.tight_layout()
    plt.savefig(a.out, dpi=90)
    print("saved", a.out)


if __name__ == "__main__":
    main()
