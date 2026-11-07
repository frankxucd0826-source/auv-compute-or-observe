"""How wrong is a k-day-old satellite map? Statistics of truth minus stale map (log10
chlorophyll) over the development missions: spread and spatial correlation length. These set
the vehicle's prior uncertainty.

    python scripts/prior_stats.py -> data/missions/prior_stats.json
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def corr_length(D, mask):
    """Average autocorrelation of the masked difference fields; the lag (cells) at which a
    squared-exponential fit exp(-r^2/2l^2) reaches exp(-1/2)."""
    n = D.shape[-1]
    acc = np.zeros((2 * n, 2 * n))
    for d, m in zip(D, mask):
        x = np.where(m, d - d[m].mean(), 0.0)
        f = np.fft.rfft2(x, s=(2 * n, 2 * n))
        c = np.fft.irfft2(f * np.conj(f), s=(2 * n, 2 * n))
        w = np.fft.irfft2(np.abs(np.fft.rfft2(m.astype(float), s=(2 * n, 2 * n))) ** 2, s=(2 * n, 2 * n))
        acc += c / np.maximum(w, 1)
    acc = np.fft.fftshift(acc)
    acc /= acc[n, n]
    yy, xx = np.mgrid[-n:n, -n:n]
    r = np.hypot(yy, xx)
    prof = [acc[(r >= k - 0.5) & (r < k + 0.5)].mean() for k in range(n)]
    prof = np.array(prof)
    below = np.where(prof < np.exp(-0.5))[0]
    if len(below) == 0:
        return float(n), prof
    k = below[0]
    # linear interpolation between k-1 and k
    l = k - 1 + (prof[k - 1] - np.exp(-0.5)) / (prof[k - 1] - prof[k])
    return float(l), prof


def main():
    M = np.load(ROOT / "data" / "missions" / "chl_missions.npz")
    rows = list(csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
    dev = np.array([r["split"] == "dev" for r in rows])
    T, P, K = M["truth"][dev], M["prior"][dev], M["mask"][dev]
    out = dict(sd={}, length_cells={}, bias={}, n_dev=int(dev.sum()), profile={})
    for j, lag in enumerate(M["lags"]):
        D = T - P[:, j]
        v = D[K]
        out["sd"][str(lag)] = float(v.std())
        out["bias"][str(lag)] = float(v.mean())
        l, prof = corr_length(D, K)
        out["length_cells"][str(lag)] = l
        out["profile"][str(lag)] = [round(float(p), 4) for p in prof[:20]]
        print(f"lag {lag} d: sd {v.std():.3f} log10, bias {v.mean():+.3f}, corr length {l:.2f} cells")
    json.dump(out, open(ROOT / "data" / "missions" / "prior_stats.json", "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
