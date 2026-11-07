"""Current fields: HYCOM snapshots on their native grid, the coarse map a vehicle would carry,
sub-grid anomalies, and interpolation onto a mission's planning grid.

Coordinates: km on a fixed equirectangular projection of the study region (Kuroshio: x east from
121 E, y north from 23 N, scale at 27 N; the region is chosen by the environment variable
OCEANROUTE_REGION, default kuroshio, gulfstream for the replication). The coarse map is the block mean of the field over cells of
`coarse_deg` degrees (water points only), interpolated back to any point; the vehicle also knows
the coastline. The sub-grid anomaly of a snapshot is the field minus its own coarse map."""
import os
from pathlib import Path

import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.ndimage import distance_transform_edt

ROOT = Path(__file__).resolve().parents[2]
REGIONS = {   # south-west corner (deg N, deg E), reference latitude, native grid spacing in km (north, east)
    "kuroshio": dict(lat0=23.0, lon0=121.0, lat_ref=27.0, dy=4.42, dx=7.94, npz="hycom_uv10m.npz"),
    "gulfstream": dict(lat0=33.0, lon0=285.0, lat_ref=37.0, dy=4.42, dx=7.11, npz="hycom_uv10m_gulfstream.npz"),
    "agulhas": dict(lat0=-43.0, lon0=14.0, lat_ref=-39.0, dy=4.42, dx=6.92, npz="hycom_uv10m_agulhas.npz"),
}
REGION = os.environ.get("OCEANROUTE_REGION", "kuroshio")
_R = REGIONS[REGION]
# The vehicle's map in the 1-degree setting: "block" = block means of the HYCOM field (default);
# "altimetry" = NOAA near-real-time blended altimetry geostrophic currents (scripts/download_altimetry.py),
# the day's product or the latest one before it. Finer maps (0.5 degree) stay HYCOM block means.
MAP_SOURCE = os.environ.get("OCEANROUTE_MAP", "block")
LAT0, LON0, KM_LAT, KM_LON = _R["lat0"], _R["lon0"], 110.57, 111.32 * np.cos(np.deg2rad(_R["lat_ref"]))
DY_KM, DX_KM = _R["dy"], _R["dx"]


class Snapshots:
    def __init__(self, path=None):
        path = path or os.environ.get("HYCOM_NPZ") or ROOT / "data" / "processed" / _R["npz"]
        D = np.load(path)
        self.lat, self.lon = D["lat"], D["lon"]
        self.times = np.array([str(t)[:10] for t in D["times"]], dtype="datetime64[D]")
        self.u, self.v = D["u"], D["v"]                     # (N, ny, nx), NaN on land
        self.y = (self.lat - LAT0) * KM_LAT                # native axes in km
        self.x = (self.lon - LON0) * KM_LON
        self.water = np.isfinite(self.u).all(axis=0) & np.isfinite(self.v).all(axis=0)
        self.km_to_land = distance_transform_edt(self.water, sampling=(DY_KM, DX_KM))
        self._coarse = {}
        self.alt = None
        if MAP_SOURCE == "altimetry":
            A = np.load(ROOT / "data" / "processed" / f"altimetry_{REGION}.npz")
            dates = A["dates"].astype("datetime64[D]")
            self.alt = dict(u=A["u"], v=A["v"], ay=(A["lat"] - LAT0) * KM_LAT, ax=(A["lon"] - LON0) * KM_LON)
            self.alt_index = np.clip(np.searchsorted(dates, self.times, side="right") - 1, 0, None)
            self.alt_age_days = (self.times - dates[self.alt_index]).astype(int)

    def _uses_alt(self, deg):
        return self.alt is not None and deg >= 1.0

    def __len__(self):
        return len(self.times)

    # ---- coarse map ---------------------------------------------------------------------
    def coarse_cells(self, deg):
        if self._uses_alt(deg):
            ay, ax = self.alt["ay"], self.alt["ax"]
            return None, None, len(ay), len(ax), ay, ax
        iy = np.floor((self.lat - LAT0) / deg).astype(int)
        ix = np.floor((self.lon - LON0) / deg).astype(int)
        ny, nx = iy.max() + 1, ix.max() + 1
        cy = LAT0 + deg * (np.arange(ny) + 0.5)
        cx = LON0 + deg * (np.arange(nx) + 0.5)
        return iy, ix, ny, nx, (cy - LAT0) * KM_LAT, (cx - LON0) * KM_LON

    def coarse(self, k, deg):
        """Block means of snapshot k (cells of `deg` degrees): (u, v) arrays on the coarse grid,
        with cells that hold no water filled from the nearest cell that does."""
        key = (k, deg)
        if key in self._coarse:
            return self._coarse[key]
        if self._uses_alt(deg):                       # the altimetry product of that day, gaps filled from the nearest cell
            j = self.alt_index[k]
            out = []
            for f in (self.alt["u"][j], self.alt["v"][j]):
                m = np.array(f, dtype=float)
                if np.isnan(m).all():
                    m = np.zeros_like(m)
                elif np.isnan(m).any():
                    _, (ii, jj) = distance_transform_edt(np.isnan(m), return_indices=True)
                    m = m[ii, jj]
                out.append(m)
            self._coarse[key] = tuple(out)
            return self._coarse[key]
        iy, ix, ny, nx, _, _ = self.coarse_cells(deg)
        out = []
        for f in (self.u[k], self.v[k]):
            s = np.zeros((ny, nx))
            c = np.zeros((ny, nx))
            w = np.isfinite(f)
            np.add.at(s, (iy[:, None].repeat(len(ix), 1)[w], ix[None, :].repeat(len(iy), 0)[w]), f[w])
            np.add.at(c, (iy[:, None].repeat(len(ix), 1)[w], ix[None, :].repeat(len(iy), 0)[w]), 1)
            m = np.where(c > 0, s / np.maximum(c, 1), np.nan)
            if np.isnan(m).any():
                bad = np.isnan(m)
                _, (ii, jj) = distance_transform_edt(bad, return_indices=True)
                m = m[ii, jj]
            out.append(m)
        if len(self._coarse) > 4000:
            self._coarse.clear()
        self._coarse[key] = tuple(out)
        return self._coarse[key]

    def coarse_at(self, k, deg, X, Y):
        """The coarse map of snapshot k evaluated at points (X, Y) km (bilinear between cell centres)."""
        _, _, _, _, cy, cx = self.coarse_cells(deg)
        cu, cv = self.coarse(k, deg)
        pts = np.stack([np.clip(Y.ravel(), cy[0], cy[-1]), np.clip(X.ravel(), cx[0], cx[-1])], -1)
        fu = RegularGridInterpolator((cy, cx), cu)(pts).reshape(X.shape)
        fv = RegularGridInterpolator((cy, cx), cv)(pts).reshape(X.shape)
        return fu, fv

    # ---- native field at arbitrary points --------------------------------------------------
    def field_at(self, k, X, Y, u=None, v=None):
        """Snapshot k (or the given native arrays) at points (X, Y) km, bilinear; NaN on land."""
        u = self.u[k] if u is None else u
        v = self.v[k] if v is None else v
        pts = np.stack([Y.ravel(), X.ravel()], -1)
        fu = RegularGridInterpolator((self.y, self.x), u, bounds_error=False, fill_value=np.nan)(pts)
        fv = RegularGridInterpolator((self.y, self.x), v, bounds_error=False, fill_value=np.nan)(pts)
        return fu.reshape(X.shape), fv.reshape(X.shape)

    def anomaly_at(self, k, deg, X, Y, lag=0):
        """What the map misses: snapshot k minus the coarse map of snapshot k - lag (lag 0: the
        sub-grid detail only; lag > 0 also the change since the map was made), at points (X, Y);
        zero where there is no water."""
        fu, fv = self.field_at(k, X, Y)
        cu, cv = self.coarse_at(k - lag, deg, X, Y)
        du, dv = fu - cu, fv - cv
        return np.nan_to_num(du), np.nan_to_num(dv)

    def land_distance_at(self, X, Y):
        pts = np.stack([Y.ravel(), X.ravel()], -1)
        d = RegularGridInterpolator((self.y, self.x), self.km_to_land, bounds_error=False, fill_value=0.0)(pts)
        return d.reshape(X.shape)

    def coarse_distance(self, k1, k2, deg, box):
        """RMS difference of two snapshots' coarse maps over the cells inside box (x0, x1, y0, y1)."""
        _, _, _, _, cy, cx = self.coarse_cells(deg)
        sel_y = (cy >= box[2]) & (cy <= box[3])
        sel_x = (cx >= box[0]) & (cx <= box[1])
        a, b = self.coarse(k1, deg), self.coarse(k2, deg)
        d = [(a[i][np.ix_(sel_y, sel_x)] - b[i][np.ix_(sel_y, sel_x)]) ** 2 for i in (0, 1)]
        return float(np.sqrt(np.mean(d[0] + d[1])))
