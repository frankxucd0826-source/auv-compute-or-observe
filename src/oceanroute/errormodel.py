"""Statistical model of what a stale coarse current map misses, fitted on the development years.

delta = real current - coarse map made `lag` snapshots earlier. From all development snapshots:
  sigma(x)  RMS of each component at each place (smoothed): where the map tends to be wrong
  ell       correlation length (km) of delta, from its spatial autocorrelation
Plausible fields for a mission: map + sum_j z_j phi_j, z ~ N(0, I). The modes phi_j come from a
Gaussian-correlated stream function psi (Karhunen-Loeve modes on a control grid), so every mode
is divergence-free (u = -dpsi/dy, v = dpsi/dx); they are then rescaled so the pointwise variance
equals sigma(x)^2. A measurement therefore informs the currents within about ell of it."""
from pathlib import Path

import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.ndimage import gaussian_filter

from .fields import DX_KM, DY_KM, MAP_SOURCE, REGION

ROOT = Path(__file__).resolve().parents[2]


def fit(S, deg, lag, idx, max_lag_km=200.0):
    """sigma maps and correlation length from snapshots idx (development years)."""
    YY, XX = np.meshgrid(S.y, S.x, indexing="ij")
    du2 = np.zeros(S.u.shape[1:])
    dv2 = np.zeros(S.u.shape[1:])
    n = 0
    lags_x = np.arange(1, int(max_lag_km / DX_KM) + 1)
    lags_y = np.arange(1, int(max_lag_km / DY_KM) + 1)
    cx = np.zeros(len(lags_x))
    cy = np.zeros(len(lags_y))
    var = 0.0
    for j in idx:
        if j - lag < 0:
            continue
        cu, cv = S.coarse_at(j - lag, deg, XX, YY)
        du, dv = S.u[j] - cu, S.v[j] - cv
        w = np.isfinite(du) & np.isfinite(dv)
        du, dv = np.where(w, du, 0.0), np.where(w, dv, 0.0)
        du2 += du ** 2
        dv2 += dv ** 2
        n += 1
        if n % 4 == 0:              # autocorrelation on a subsample of days
            for f in (du, dv):
                var += np.sum(f[w] ** 2) / w.sum()
                for i, L in enumerate(lags_x):
                    m = w[:, L:] & w[:, :-L]
                    cx[i] += np.sum((f[:, L:] * f[:, :-L])[m]) / max(m.sum(), 1)
                for i, L in enumerate(lags_y):
                    m = w[L:, :] & w[:-L, :]
                    cy[i] += np.sum((f[L:, :] * f[:-L, :])[m]) / max(m.sum(), 1)
    su = np.sqrt(du2 / n)
    sv = np.sqrt(dv2 / n)
    water = S.water
    su = np.where(water, gaussian_filter(su, 2), 0.0)
    sv = np.where(water, gaussian_filter(sv, 2), 0.0)
    rx, ry = cx / var, cy / var
    dist = np.r_[lags_x * DX_KM, lags_y * DY_KM]
    rho = np.r_[rx, ry]
    ok = (rho > 0.05) & (dist <= max_lag_km)
    # Gaussian correlation exp(-d^2 / (2 ell^2)): log rho = -d^2 / (2 ell^2)
    ell = float(np.sqrt(np.sum(dist[ok] ** 4) / (2 * np.sum(dist[ok] ** 2 * -np.log(rho[ok])))))
    return dict(su=su, sv=sv, ell=ell, rho_x=rx.tolist(), rho_y=ry.tolist(), dist_x=(lags_x * DX_KM).tolist(),
                dist_y=(lags_y * DY_KM).tolist(), n=n, deg=deg, lag=lag)


def cache_path(deg, lag):
    sfx = ("" if REGION == "kuroshio" else "_" + REGION) + ("_altimetry" if MAP_SOURCE == "altimetry" and deg >= 1.0 else "")
    return ROOT / "results" / f"route_errormodel{sfx}_deg{deg}_lag{lag}.npz"


def load_or_fit(S, deg, lag, idx):
    f = cache_path(deg, lag)
    if f.exists():
        D = np.load(f)
        return dict(su=D["su"], sv=D["sv"], ell=float(D["ell"]))
    M = fit(S, deg, lag, idx)
    np.savez(f, su=M["su"], sv=M["sv"], ell=M["ell"], rho_x=M["rho_x"], rho_y=M["rho_y"],
             dist_x=M["dist_x"], dist_y=M["dist_y"])
    return M


def modes(S, M, X, Y, water, box, var_kept=0.95, scale=1.0):
    """Divergence-free modes (K, ny, nx, 2) on a mission grid (X, Y km, spacing h). The control
    grid depends only on the mission box, so grids of different spacing get the same modes."""
    ell = M["ell"] * scale
    h = float(X[0, 1] - X[0, 0])
    sp = ell / 3.0
    x0, x1, y0, y1 = box[0] - ell, box[1] + ell, box[2] - ell, box[3] + ell
    gx = np.arange(x0, x1 + sp, sp)
    gy = np.arange(y0, y1 + sp, sp)
    GX, GY = np.meshgrid(gx, gy)
    P = np.stack([GX.ravel(), GY.ravel()], -1)
    d2 = ((P[:, None, :] - P[None, :, :]) ** 2).sum(-1)
    C = np.exp(-d2 / (2 * ell ** 2))
    w, V = np.linalg.eigh(C)
    w, V = w[::-1], V[:, ::-1]
    k = int(np.searchsorted(np.cumsum(w) / w.sum(), var_kept)) + 1
    out = []
    pts = np.stack([Y.ravel(), X.ravel()], -1)
    for j in range(k):
        psi = (V[:, j] * np.sqrt(w[j])).reshape(len(gy), len(gx))
        f = RegularGridInterpolator((gy, gx), psi, method="cubic")(pts).reshape(X.shape)
        dpy, dpx = np.gradient(f, h, h)
        out.append(np.stack([-dpy, dpx], -1))
    A = np.stack(out)                                     # (K, ny, nx, 2)
    # rescale so that the pointwise variance of each component equals sigma(x)^2
    pts2 = np.stack([Y.ravel(), X.ravel()], -1)
    su = RegularGridInterpolator((S.y, S.x), M["su"], bounds_error=False, fill_value=0.0)(pts2).reshape(X.shape)
    sv = RegularGridInterpolator((S.y, S.x), M["sv"], bounds_error=False, fill_value=0.0)(pts2).reshape(X.shape)
    vu = np.sqrt((A[..., 0] ** 2).sum(0)) + 1e-12
    vv = np.sqrt((A[..., 1] ** 2).sum(0)) + 1e-12
    A[..., 0] *= su / vu
    A[..., 1] *= sv / vv
    A[:, ~water] = 0.0
    return A
