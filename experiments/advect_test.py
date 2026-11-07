"""Can a simple physical extrapolation of the stale map beat persistence on real data?

For every mission window (422; map 3 days old) the bloom's motion is estimated from the two
satellite days before the stale map (dense optical flow, or one shift for the whole window by
phase correlation) and the stale map is carried forward along it for 3 days (semi-Lagrangian,
steady flow). Compared with persistence (use the stale map as it is):
  rmse          log10 chlorophyll over the window's water cells
  regret_tele   true maximum minus the true value at the forecast's densest cell
                (as if that cell could be reported without going there)
A 1-day check (forecast the day after the stale map) is included, and the mean of the stale map
and the two days before it (persistent features rather than motion). No parameter is tuned.

    python -E -X utf8 experiments/advect_test.py  -> results/advect_test.json
"""
import csv
import json
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from oceanmeta.data import Fields, window  # noqa: E402

N, MARGIN, CELL_KM = 40, 8, 2.0
NB = N + 2 * MARGIN


def to_u8(a, b):
    both = np.concatenate([a[np.isfinite(a)], b[np.isfinite(b)]])
    lo, hi = np.percentile(both, 1), np.percentile(both, 99)
    out = []
    for x in (a, b):
        x = np.where(np.isfinite(x), x, np.nanmean(x))
        out.append(np.clip((x - lo) / (hi - lo + 1e-9) * 255, 0, 255).astype(np.uint8))
    return out


def flow(a, b):
    """Displacement (cells) carrying field a onto field b: b(x + v(x)) ~ a(x)."""
    ua, ub = to_u8(a, b)
    return cv2.calcOpticalFlowFarneback(ua, ub, None, 0.5, 2, 9, 3, 5, 1.1, 0)


def shift(a, b):
    fa = np.where(np.isfinite(a), a, np.nanmean(a)).astype(np.float32)
    fb = np.where(np.isfinite(b), b, np.nanmean(b)).astype(np.float32)
    win = cv2.createHanningWindow((NB, NB), cv2.CV_32F)
    (dx, dy), _ = cv2.phaseCorrelate(fa, fb, win)
    v = np.zeros((NB, NB, 2), np.float32)
    v[..., 0], v[..., 1] = dx, dy
    return v


def carry(f, v, k):
    """Field f carried k steps along the steady displacement v (semi-Lagrangian)."""
    yy, xx = np.mgrid[0:NB, 0:NB].astype(np.float32)
    src = np.where(np.isfinite(f), f, np.nanmean(f)).astype(np.float32)
    return cv2.remap(src, xx - k * v[..., 0], yy - k * v[..., 1], cv2.INTER_LINEAR,
                     borderMode=cv2.BORDER_REPLICATE)


def crop(f):
    return f[MARGIN:MARGIN + N, MARGIN:MARGIN + N]


def scores(fc, truth, mask):
    ok = mask & np.isfinite(truth) & np.isfinite(fc)
    rmse = float(np.sqrt(np.mean((fc[ok] - truth[ok]) ** 2)))
    t = np.where(ok, truth, -np.inf)
    k = int(np.argmax(np.where(ok, fc, -np.inf)))
    return rmse, float(t.max() - t.flat[k])


def main():
    F = Fields("chl")
    M = np.load(ROOT / "data" / "missions" / "chl_missions.npz")
    rows = list(csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
    li3 = list(M["lags"]).index(3)
    recs, check = [], []
    for r in rows:
        i, d = int(r["id"]), np.datetime64(r["date"], "D")
        lat0, lon0 = float(r["lat0"]), float(r["lon0"])
        days = {}
        for lag in (0, 2, 3, 4, 5):
            f = F.day(d - np.timedelta64(lag, "D"))
            days[lag] = None if f is None else window(f, F.lat, F.lon, lat0, lon0, NB, CELL_KM)
        if any(days[k] is None for k in (0, 3, 4)):
            continue
        mask = M["mask"][i]
        check.append(float(np.nanmax(np.abs(crop(days[3]) - M["prior"][i, li3]))))
        truth = crop(days[0])
        v1 = flow(days[4], days[3])
        rec = dict(mission=i, split=r["split"])
        fcs = {"persistence": crop(days[3]),
               "flow_1day_x3": crop(carry(days[3], v1, 3.0)),
               "flow_1day_x1.5": crop(carry(days[3], v1, 1.5)),
               "shift_1day_x3": crop(carry(days[3], shift(days[4], days[3]), 3.0))}
        if days[5] is not None:
            fcs["flow_2day_x1.5"] = crop(carry(days[3], flow(days[5], days[3]), 1.5))
            fcs["mean_3to5"] = crop(np.nanmean(np.stack([days[3], days[4], days[5]]), axis=0))
        for name, fc in fcs.items():
            rec[name] = scores(fc, truth, mask)
        if days[2] is not None:     # 1-day horizon: the day after the stale map
            t1 = crop(days[2])
            rec["h1_persistence"] = scores(crop(days[3]), t1, mask)
            rec["h1_flow"] = scores(crop(carry(days[3], v1, 1.0)), t1, mask)
        recs.append(rec)
    names = sorted({k for r in recs for k in r if k not in ("mission", "split")})
    rng = np.random.default_rng(0)
    summary = {}
    for split in ("all", "test"):
        sub = [r for r in recs if split == "all" or r["split"] == split]
        for name in names:
            base = "h1_persistence" if name.startswith("h1_") else "persistence"
            pair = [(r[name], r[base]) for r in sub if name in r and base in r]
            a = np.array([p[0] for p in pair])
            b = np.array([p[1] for p in pair])
            out = {"n": len(pair)}
            for j, metric in enumerate(("rmse", "regret_tele")):
                diff = a[:, j] - b[:, j]
                boots = [diff[rng.integers(0, len(diff), len(diff))].mean() for _ in range(2000)]
                out[metric] = float(a[:, j].mean())
                out[metric + "_minus_persistence"] = float(diff.mean())
                out[metric + "_ci95"] = [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]
                out[metric + "_share_better"] = float(np.mean(diff < 0))
            summary[f"{split}/{name}"] = out
    res = dict(window_check_max_abs_diff=float(np.max(check)), n_windows=len(recs), summary=summary)
    json.dump(dict(res, per_window=recs), open(ROOT / "results" / "advect_test.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
