"""Cut mission windows around chlorophyll hotspots of the East China Sea bloom season.

For every day of April-June with the three previous days available: smooth the day's field,
take the strongest local maximum above 5 mg m^-3 (log10 0.7) that lies on the shelf off
Zhejiang (26.5-31.5 N, 121.5-125 E) at least 30 km from land, shift the window centre by up
to 16 km at random so the hotspot is not always in the middle, and cut an 80 km x 80 km
window (40 x 40 cells of 2 km) from the day itself (the truth) and from 1, 2 and 3 days
earlier (the stale maps a vehicle would carry). Days from 2018-2022 are the development set,
2023-2026 the test set.

    python scripts/make_missions.py   -> data/missions/chl_missions.npz and .csv
"""
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter, maximum_filter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from oceanmeta.data import Fields, window  # noqa: E402

N_CELLS = 40
CELL_KM = 2.0
LAGS = (1, 2, 3)
BOX = dict(lat=(26.5, 31.5), lon=(121.5, 125.0))
MIN_LOG10 = np.log10(5.0)
MIN_KM_LAND = 30.0       # hotspot centre at least this far from land
COAST_BUFFER_KM = 15.0   # cells closer to land are out of bounds for the vehicle
MAX_SHIFT_KM = 16.0
MIN_OCEAN = 0.8
MIN_CONTRAST = 0.3


def boundary_start(mask, rng):
    n = mask.shape[0]
    edge = [(0, i) for i in range(n)] + [(n - 1, i) for i in range(n)] + \
           [(i, 0) for i in range(n)] + [(i, n - 1) for i in range(n)]
    ok = [(y, x) for y, x in edge if mask[y, x]]
    y, x = ok[rng.integers(len(ok))]
    return float(x), float(y)


def main():
    F = Fields("chl")
    dist = F.km_from_land()
    lat, lon = F.lat, F.lon
    LA, LO = np.meshgrid(lat, lon, indexing="ij")
    inbox = (LA >= BOX["lat"][0]) & (LA <= BOX["lat"][1]) & (LO >= BOX["lon"][0]) & (LO <= BOX["lon"][1])
    allowed = inbox & (dist >= MIN_KM_LAND)
    rows, truths, priors, masks = [], [], [], []
    for d in F.dates:
        md = int(str(d)[5:7])
        if md not in (4, 5, 6):
            continue
        prev = [F.day(d - np.timedelta64(k, "D")) for k in LAGS]
        if any(p is None for p in prev):
            continue
        f = F.day(d)
        g = gaussian_filter(np.nan_to_num(f, nan=-2.0), 2.0)
        peaks = (g == maximum_filter(g, size=15)) & allowed & (g >= MIN_LOG10)
        if not peaks.any():
            continue
        iy, ix = np.unravel_index(np.argmax(np.where(peaks, g, -9)), g.shape)
        rng = np.random.default_rng(int(str(d).replace("-", "")))
        dy, dx = rng.uniform(-MAX_SHIFT_KM, MAX_SHIFT_KM, 2)
        lat0 = lat[iy] + dy / 111.32
        lon0 = lon[ix] + dx / (111.32 * np.cos(np.deg2rad(lat[iy])))
        T = window(f, lat, lon, lat0, lon0, N_CELLS, CELL_KM)
        P = [window(p, lat, lon, lat0, lon0, N_CELLS, CELL_KM) for p in prev]
        coast = window(dist, lat, lon, lat0, lon0, N_CELLS, CELL_KM)
        mask = np.isfinite(T) & np.all([np.isfinite(p) for p in P], axis=0) & (coast >= COAST_BUFFER_KM)
        if mask.mean() < MIN_OCEAN:
            continue
        tv = T[mask]
        if tv.max() - np.median(tv) < MIN_CONTRAST:
            continue
        fill = np.median(tv)
        T = np.where(mask, T, fill)
        P = [np.where(mask, p, fill) for p in P]
        sx, sy = boundary_start(mask, rng)
        year = int(str(d)[:4])
        rows.append(dict(id=len(rows), date=str(d), lat0=lat0, lon0=lon0, start_x=sx, start_y=sy,
                         split="dev" if year <= 2022 else "test", ocean=float(mask.mean()),
                         tmax=float(tv.max()), tmed=float(np.median(tv))))
        truths.append(T.astype(np.float32))
        priors.append(np.stack(P).astype(np.float32))
        masks.append(mask)
        if len(rows) % 50 == 0:
            print(len(rows), d, flush=True)
    out = ROOT / "data" / "missions"
    out.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out / "chl_missions.npz", truth=np.stack(truths), prior=np.stack(priors),
                        mask=np.stack(masks), lags=np.array(LAGS))
    import csv
    with open(out / "chl_missions.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    n_dev = sum(r["split"] == "dev" for r in rows)
    print(f"{len(rows)} missions ({n_dev} development, {len(rows) - n_dev} test)")


if __name__ == "__main__":
    main()
