"""One route decision: start s, goal g (km), a circular no-go zone centred midway, two sides.

Truth: the HYCOM snapshot. Map: its coarse version (block means). Plausible fields: map + a
combination of sub-grid anomalies borrowed from K historical snapshots whose coarse maps look
most like today's (analogues), u = map + sum_j z_j a_j / sqrt(K), z ~ N(0, I) a priori.
Measurements (current at points, noise sigma) update z by a linear Gaussian (Kalman) step.

Margin dJ = J_L - J_R (hours): positive means the right side is faster."""
from dataclasses import dataclass

import numpy as np

from .solver import Grid, Side, Router

LEVELS = {0: (8.0, 8), 1: (4.0, 16), 2: (2.0, 32)}     # grid spacing (km), directions
CAP = 200.0                                              # hours; stands in for "impassable"


@dataclass
class Spec:
    k: int            # snapshot index
    s: tuple
    g: tuple
    c: tuple
    radius: float
    box: tuple        # x0, x1, y0, y1 (km)


def sample_specs(S, k, rng, n, dist=(100.0, 140.0), margin=60.0, radius=15.0, clear=20.0, tries=400,
                 min_speed=0.0, deg=0.5, lag=0):
    """Up to n missions on snapshot k: both ends and the zone in open water, box inside the data,
    and (if min_speed > 0) a mean current speed on the coarse map over the box of at least
    min_speed m/s -- missions where the currents matter, chosen from what the vehicle knows."""
    xs, ys = S.x, S.y
    out = []
    for _ in range(tries):
        if len(out) == n:
            break
        D = rng.uniform(*dist)
        th = rng.uniform(0, 2 * np.pi)
        sx = rng.uniform(xs[0] + margin, xs[-1] - margin)
        sy = rng.uniform(ys[0] + margin, ys[-1] - margin)
        gx, gy = sx + D * np.cos(th), sy + D * np.sin(th)
        cx, cy = (sx + gx) / 2, (sy + gy) / 2
        box = (min(sx, gx) - margin, max(sx, gx) + margin, min(sy, gy) - margin, max(sy, gy) + margin)
        if box[0] < xs[0] or box[1] > xs[-1] or box[2] < ys[0] or box[3] > ys[-1]:
            continue
        P = np.array([[sx, gx, cx], [sy, gy, cy]])
        d = S.land_distance_at(P[0], P[1])
        if d[0] < clear or d[1] < clear or d[2] < radius + 10:
            continue
        XX, YY = np.meshgrid(np.linspace(box[0], box[1], 25), np.linspace(box[2], box[3], 25))
        wet = S.land_distance_at(XX, YY) > 0
        if wet.mean() < 0.7:
            continue
        if min_speed > 0:
            cu, cv = S.coarse_at(k - lag, deg, XX, YY)
            if np.hypot(cu, cv)[wet].mean() < min_speed:
                continue
        out.append(Spec(k, (sx, sy), (gx, gy), (cx, cy), radius, box))
    return out


class Level:
    """One planning grid for a mission, with the truth, the map and the analogue anomalies."""

    def __init__(self, S, spec, level, deg, analogues, lag=0):
        h, nd = LEVELS[level]
        x0, x1, y0, y1 = spec.box
        nx, ny = int(np.ceil((x1 - x0) / h)) + 1, int(np.ceil((y1 - y0) / h)) + 1
        X, Y = np.meshgrid(x0 + h * np.arange(nx), y0 + h * np.arange(ny))
        water = S.land_distance_at(X, Y) > 0
        self.grid = Grid(x0, y0, h, nx, ny, water, nd)
        self.start, self.goal = self.grid.node(*spec.s), self.grid.node(*spec.g)
        self.side = {a: Side(self.grid, spec.s, spec.g, spec.c, spec.radius, a).ok for a in "LR"}
        zone = np.hypot(X - spec.c[0], Y - spec.c[1]) <= spec.radius
        zf = zone.ravel()
        gr = self.grid
        mx, my = (gr.px + gr.qx) / 2, (gr.py + gr.qy) / 2
        self.free = gr.base_ok & ~zf[gr.src] & ~zf[gr.dst] & (np.hypot(mx - spec.c[0], my - spec.c[1]) > spec.radius)
        tu, tv = S.field_at(spec.k, X, Y)
        self.truth = (np.nan_to_num(tu), np.nan_to_num(tv))
        self.map = S.coarse_at(spec.k - lag, deg, X, Y)        # the coarse map, `lag` snapshots old
        self.Phi = None
        if analogues is not None:
            A = np.stack([np.stack(S.anomaly_at(j, deg, X, Y, lag), -1) for j in analogues])  # (K, ny, nx, 2)
            A[:, ~water] = 0.0
            self.Phi = A / np.sqrt(len(analogues))
        self.X, self.Y = X, Y

    def field(self, z=None):
        if z is None or self.Phi is None:
            return self.map
        d = np.tensordot(z, self.Phi, axes=(0, 0))
        return self.map[0] + d[..., 0], self.map[1] + d[..., 1]

    def times(self, field, V, source, sides="LR"):
        """Optimal time to the goal on each side from node `source`, and the routers' predecessors."""
        R = Router(self.grid, field[0], field[1], V)
        out = {}
        for a in sides:
            d, pred = R.solve(self.side[a], source)
            out[a] = (float(d[self.goal]), pred)
        return R, out


def margin(lv, field, V, src):
    R, out = lv.times(field, V, src)
    tl, tr = min(out["L"][0], CAP), min(out["R"][0], CAP)
    return tl - tr, R, out


def _grad_w(lv, R, out, sign, Lc):
    G = np.zeros((lv.grid.ny, lv.grid.nx, 2))                    # sides that are impassable add nothing
    if out["L"][0] < CAP:
        G += R.gradient(R.path(out["L"][1], lv.goal))
    if out["R"][0] < CAP:
        G -= R.gradient(R.path(out["R"][1], lv.goal))
    G *= sign
    gz = np.tensordot(lv.Phi, G, axes=([1, 2, 3], [0, 1, 2]))
    return Lc.T @ gz


def extreme_margin(lv, V, src, sign, r, m=None, Lc=None, iters=6, w_init=None):
    """Largest sign * dJ over plausible fields z = m + Lc w, |w| <= r.
    Start at the centre, jump to the ball's edge along the gradient (the exact answer if dJ were
    linear in z), then refine: from the best point so far, step along its gradient with steps
    r, r/2, r/4 (projected back into the ball) and keep any improvement.
    Returns (dJ at the best point, z there, w there, number of route solves)."""
    K = lv.Phi.shape[0]
    m = np.zeros(K) if m is None else m
    Lc = np.eye(K) if Lc is None else Lc
    solves = 0

    def evaluate(w):
        z = m + Lc @ w
        d, R, out = margin(lv, lv.field(z), V, src)
        return (sign * d, d, z, w, R, out)

    def proj(w):
        n = np.linalg.norm(w)
        return w * (r / n) if n > r else w

    best = evaluate(np.zeros(K))
    solves += 2
    starts = []
    g = _grad_w(lv, best[4], best[5], sign, Lc)
    if np.linalg.norm(g) > 1e-12:
        starts.append(r * g / np.linalg.norm(g))
    if w_init is not None:
        starts.append(proj(np.asarray(w_init, float)))
    for w in starts:
        cand = evaluate(w)
        solves += 2
        if cand[0] > best[0] + 1e-9:
            best = cand
    for _ in range(iters):
        g = _grad_w(lv, best[4], best[5], sign, Lc)
        n = np.linalg.norm(g)
        if n < 1e-12:
            break
        improved = False
        for eta in (r, r / 2, r / 4):
            cand = evaluate(proj(best[3] + eta * g / n))
            solves += 2
            if cand[0] > best[0] + 1e-6:
                best, improved = cand, True
                break
        if not improved:
            break
    return best[1], best[2], best[3], solves


def posterior(lv, nodes, values, sigma, prior=None):
    """Gaussian update of z from current measurements (u, v) at grid nodes."""
    K = lv.Phi.shape[0]
    m0, P0 = (np.zeros(K), np.eye(K)) if prior is None else prior
    Pf = lv.Phi.reshape(K, -1, 2)                           # (K, n_nodes, 2)
    H = np.concatenate([Pf[:, nodes, 0].T, Pf[:, nodes, 1].T], 0)       # (2n, K)
    mu = np.concatenate([lv.map[0].ravel()[nodes], lv.map[1].ravel()[nodes]])
    y = np.concatenate([values[0], values[1]]) - mu
    Pi = np.linalg.inv(P0)
    P = np.linalg.inv(Pi + H.T @ H / sigma ** 2)
    m = P @ (Pi @ m0 + H.T @ y / sigma ** 2)
    return m, P
