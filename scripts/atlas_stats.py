"""How fast does a satellite chlorophyll map of the East China Sea go stale? For every 2 km
pixel and season, the spread of the change between a day and k days earlier (log10
chlorophyll), from all days 2018-2026, and the e-folding time of day-to-day correlation of
the deseasonalised field. Output: results/atlas/atlas_stats.npz

    python scripts/atlas_stats.py
"""
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import uniform_filter1d

ROOT = Path(__file__).resolve().parents[1]
SEASONS = {"spring": (3, 4, 5), "summer": (6, 7, 8), "autumn": (9, 10, 11), "winter": (12, 1, 2)}
LAGS = (1, 3, 7)


def main():
    P = ROOT / "data" / "processed"
    F = np.load(P / "chl.npy", mmap_mode="r")
    dates = np.load(P / "chl_dates.npy").astype("datetime64[D]")
    ocean = np.load(P / "ocean_mask.npy")
    n = len(dates)
    # complete daily axis (missing days NaN) so that lags are calendar lags
    day0 = dates[0]
    full_n = int((dates[-1] - day0).astype(int)) + 1
    pos = (dates - day0).astype(int)
    months = ((day0 + np.arange(full_n)).astype("datetime64[M]").astype(int) % 12) + 1
    ny, nx = F.shape[1:]
    out = {}
    # deseasonalise with a 31-day running mean along time, computed in row blocks
    for season, ms in SEASONS.items():
        sel = np.isin(months, ms)
        for k in LAGS:
            out[f"sd_{season}_{k}"] = np.full((ny, nx), np.nan, np.float32)
            out[f"n_{season}_{k}"] = np.zeros((ny, nx), np.int32)
        out[f"tau_{season}"] = np.full((ny, nx), np.nan, np.float32)
        out[f"mean_{season}"] = np.full((ny, nx), np.nan, np.float32)
    block = 16
    for r0 in range(0, ny, block):
        r1 = min(ny, r0 + block)
        C = np.full((full_n, r1 - r0, nx), np.nan, np.float32)
        C[pos] = np.asarray(F[:, r0:r1, :], dtype=np.float32)
        filled = np.where(np.isfinite(C), C, 0.0)
        cnt = uniform_filter1d(np.isfinite(C).astype(np.float32), 31, axis=0, mode="nearest")
        smooth = uniform_filter1d(filled, 31, axis=0, mode="nearest") / np.maximum(cnt, 1e-6)
        A = C - smooth
        for season, ms in SEASONS.items():
            sel = np.isin(months, ms)
            out[f"mean_{season}"][r0:r1] = np.nanmean(C[sel], axis=0)
            var_a = np.nanvar(A[sel], axis=0)
            rhos = []
            for k in LAGS:
                d = C[k:] - C[:-k]
                s = sel[k:]
                out[f"sd_{season}_{k}"][r0:r1] = np.nanstd(d[s], axis=0)
                out[f"n_{season}_{k}"][r0:r1] = np.isfinite(d[s]).sum(0)
                da = A[k:] - A[:-k]
                rhos.append(1 - np.nanvar(da[s], axis=0) / np.maximum(2 * var_a, 1e-9))
            # e-folding time from the lag-1 and lag-3 correlations of anomalies
            rho = np.clip(np.stack(rhos), 1e-3, 0.999)
            ks = np.array(LAGS, dtype=np.float32)[:, None, None]
            tau = -(ks[:2] / np.log(rho[:2])).mean(0)
            out[f"tau_{season}"][r0:r1] = tau
        print(f"rows {r0}-{r1}", flush=True)
    for key in list(out):
        if key.startswith(("sd_", "tau_", "mean_")):
            out[key] = np.where(ocean, out[key], np.nan).astype(np.float32)
    out["lat"] = np.load(P / "chl_lat.npy")
    out["lon"] = np.load(P / "chl_lon.npy")
    dst = ROOT / "results" / "atlas"
    dst.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(dst / "atlas_stats.npz", **out)
    for season in SEASONS:
        v = out[f"sd_{season}_3"]
        print(season, "3-day change sd: median %.3f, 90th pct %.3f" % (np.nanmedian(v), np.nanpercentile(v, 90)))


if __name__ == "__main__":
    main()
