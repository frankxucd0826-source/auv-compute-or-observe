"""Satellite fields of the East China Sea box and mission windows cut from them.

Raw monthly files (data/raw/<name>/<name>_YYYY-MM.nc) are packed by scripts/preprocess.py
into data/processed/<name>.npy (float16, days x lat x lon, latitude ascending) with
<name>_dates.npy, <name>_lat.npy, <name>_lon.npy. Chlorophyll is stored as log10(mg m^-3).
"""
from pathlib import Path

import netCDF4
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.ndimage import distance_transform_edt

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data" / "processed"
KM_PER_DEG_LAT = 111.32


def open_nc(path):
    """netCDF-C cannot open non-ASCII Windows paths, so read the bytes first."""
    return netCDF4.Dataset("inmemory.nc", memory=Path(path).read_bytes())


class Fields:
    def __init__(self, name):
        self.name = name
        self.F = np.load(PROC / f"{name}.npy", mmap_mode="r")
        self.dates = np.load(PROC / f"{name}_dates.npy").astype("datetime64[D]")
        self.lat = np.load(PROC / f"{name}_lat.npy")
        self.lon = np.load(PROC / f"{name}_lon.npy")
        self._index = {d: i for i, d in enumerate(self.dates)}
        self.land = None

    def day(self, d):
        i = self._index.get(np.datetime64(d, "D"))
        return None if i is None else np.asarray(self.F[i], dtype=np.float32)

    def land_mask(self):
        """Pixels that are NaN on every one of 60 sampled days are land. Frozen in
        data/missions/land_mask.npy (kept in the repository), so mission windows do not change when
        more days are downloaded."""
        if self.land is None and (ROOT / "data" / "missions" / "land_mask.npy").exists():
            self.land = np.load(ROOT / "data" / "missions" / "land_mask.npy")
        if self.land is None:
            idx = np.linspace(0, len(self.dates) - 1, 60).astype(int)
            nan_all = np.ones(self.F.shape[1:], bool)
            for i in idx:
                nan_all &= ~np.isfinite(np.asarray(self.F[i], dtype=np.float32))
            self.land = nan_all
        return self.land

    def km_from_land(self):
        land = self.land_mask()
        dy = KM_PER_DEG_LAT * abs(self.lat[1] - self.lat[0])
        dx = KM_PER_DEG_LAT * np.cos(np.deg2rad(self.lat.mean())) * abs(self.lon[1] - self.lon[0])
        return distance_transform_edt(~land, sampling=(dy, dx))


def window(field, lat, lon, lat0, lon0, n=40, cell_km=2.0):
    """Bilinear interpolation of a lat/lon field onto an n x n local grid of cell_km squares
    centred on (lat0, lon0). Row 0 is the southern edge, column 0 the western edge."""
    half = (n - 1) / 2 * cell_km
    ys = (np.arange(n) * cell_km - half) / KM_PER_DEG_LAT + lat0
    xs = (np.arange(n) * cell_km - half) / (KM_PER_DEG_LAT * np.cos(np.deg2rad(lat0))) + lon0
    f = RegularGridInterpolator((lat, lon), field, bounds_error=False, fill_value=np.nan)
    YY, XX = np.meshgrid(ys, xs, indexing="ij")
    return f(np.stack([YY.ravel(), XX.ravel()], -1)).reshape(n, n)
