"""Time-optimal routes for a vehicle of fixed through-water speed V in a steady 2-D current field.

The field lives on a regular grid (km, x east, y north). Each grid node links to its neighbours
(8, 16 or 32 directions; more directions = a finer solution, i.e. "more computation"). Crossing an
edge takes length / ground speed, where the vehicle heads so that its ground track follows the
edge: ground speed = u.e + sqrt(V^2 - (u.n)^2), u = current (mean of the edge's two end nodes),
e = edge direction, n = its normal. Edges whose ground speed is not positive (the current is too
strong) are impassable. Land, a circular no-go zone and, per side, a cut line are removed, so the
shortest path of side "L" passes the zone on the traveller's left and side "R" on the right.
Times are in hours."""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

NEIGHBOURS = {
    8: [(1, 0), (0, 1), (1, 1), (1, -1)],
    16: [(1, 0), (0, 1), (1, 1), (1, -1), (1, 2), (2, 1), (1, -2), (2, -1)],
    32: [(1, 0), (0, 1), (1, 1), (1, -1), (1, 2), (2, 1), (1, -2), (2, -1),
         (1, 3), (3, 1), (1, -3), (3, -1), (2, 3), (3, 2), (2, -3), (3, -2)],
}
MIN_GROUND = 0.02     # m/s; slower edges count as impassable


class Grid:
    """Nodes (iy, ix) at x = x0 + ix h, y = y0 + iy h. `water` marks usable nodes."""

    def __init__(self, x0, y0, h, nx, ny, water, n_dirs=16):
        self.x0, self.y0, self.h, self.nx, self.ny = x0, y0, h, nx, ny
        self.water = water.astype(bool)
        xs, ys = x0 + h * np.arange(nx), y0 + h * np.arange(ny)
        self.X, self.Y = np.meshgrid(xs, ys)
        src, dst = [], []
        idx = np.arange(ny * nx).reshape(ny, nx)
        for dx, dy in NEIGHBOURS[n_dirs]:
            for sx, sy in ((dx, dy), (-dx, -dy)):
                a = idx[max(0, -sy):ny - max(0, sy), max(0, -sx):nx - max(0, sx)]
                b = idx[max(0, sy):ny + min(0, sy), max(0, sx):nx + min(0, sx)]
                src.append(a.ravel())
                dst.append(b.ravel())
        self.src, self.dst = np.concatenate(src), np.concatenate(dst)
        xf, yf = self.X.ravel(), self.Y.ravel()
        self.px, self.py = xf[self.src], yf[self.src]
        self.qx, self.qy = xf[self.dst], yf[self.dst]
        dxk, dyk = self.qx - self.px, self.qy - self.py
        self.length = np.hypot(dxk, dyk)                    # km
        self.ex, self.ey = dxk / self.length, dyk / self.length
        w = self.water.ravel()
        # an edge is usable if both ends and its midpoint are water
        mx, my = (self.px + self.qx) / 2, (self.py + self.qy) / 2
        mi = np.clip(np.rint((my - y0) / h).astype(int), 0, ny - 1)
        mj = np.clip(np.rint((mx - x0) / h).astype(int), 0, nx - 1)
        self.base_ok = w[self.src] & w[self.dst] & self.water[mi, mj]
        self.n = ny * nx
        code = self.src.astype(np.int64) * self.n + self.dst
        self._order = np.argsort(code)
        self._code = code[self._order]

    def edges_of(self, nodes):
        """Edge indices along a node path."""
        want = np.array([a * self.n + b for a, b in zip(nodes[:-1], nodes[1:])], np.int64)
        pos = np.searchsorted(self._code, want)
        return self._order[pos]

    def node(self, x, y):
        """Nearest water node to (x, y) km."""
        d = (self.X - x) ** 2 + (self.Y - y) ** 2
        d[~self.water] = np.inf
        return int(np.argmin(d))

    def xy(self, k):
        return float(self.X.flat[k]), float(self.Y.flat[k])


class Side:
    """Edges usable by one side of a circular no-go zone of radius `radius` centred at c, for a
    trip from s to g. side "L": the traveller keeps the zone on its right (passes on the left)."""

    def __init__(self, grid, s, g, c, radius, side):
        ex, ey = g[0] - s[0], g[1] - s[1]
        L = np.hypot(ex, ey)
        nlx, nly = -ey / L, ex / L                    # left normal of the trip
        wx, wy = (nlx, nly) if side == "R" else (-nlx, -nly)   # cut toward the other side
        # remove edges crossing the ray c + t w, t >= 0
        px, py, qx, qy = grid.px, grid.py, grid.qx, grid.qy
        cross_pq = wx * (qy - py) - wy * (qx - px)
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (wx * (c[1] - py) - wy * (c[0] - px)) / cross_pq
            ix_ = px + t * (qx - px) - c[0]
            iy_ = py + t * (qy - py) - c[1]
        hits = (np.abs(cross_pq) > 1e-12) & (t >= 0) & (t <= 1) & (ix_ * wx + iy_ * wy >= 0)
        # the no-go zone itself
        zone = np.hypot(grid.X - c[0], grid.Y - c[1]) <= radius
        z = zone.ravel()
        mx, my = (px + qx) / 2, (py + qy) / 2
        mid_in = np.hypot(mx - c[0], my - c[1]) <= radius
        self.ok = grid.base_ok & ~hits & ~z[grid.src] & ~z[grid.dst] & ~mid_in
        self.side = side


def edge_times(grid, u, v, V):
    """Hours to cross each edge in current (u, v) (m/s, node arrays shaped like the grid)."""
    uf, vf = u.ravel(), v.ravel()
    ue = 0.5 * (uf[grid.src] + uf[grid.dst])
    ve = 0.5 * (vf[grid.src] + vf[grid.dst])
    upar = ue * grid.ex + ve * grid.ey
    uperp = -ue * grid.ey + ve * grid.ex
    disc = V * V - uperp * uperp
    g = upar + np.sqrt(np.clip(disc, 0, None))
    ok = (disc > 0) & (g > MIN_GROUND)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(ok, grid.length * 1000.0 / g / 3600.0, np.inf)
    return t, upar, uperp, g, ok


class Router:
    """Shortest travel times on one grid for a given current field and vehicle speed."""

    def __init__(self, grid, u, v, V):
        self.grid, self.V = grid, V
        self.t, self.upar, self.uperp, self.g, self.ok = edge_times(grid, u, v, V)

    def solve(self, side_ok, source):
        """Travel time (h) from node `source` to every node, using edges allowed by side_ok
        (a boolean edge mask; None = all usable edges), and the predecessor array."""
        m = self.ok & (side_ok if side_ok is not None else self.grid.base_ok)
        A = csr_matrix((self.t[m], (self.grid.src[m], self.grid.dst[m])), shape=(self.grid.n, self.grid.n))
        d, pred = dijkstra(A, directed=True, indices=source, return_predecessors=True)
        return d, pred

    def path(self, pred, target):
        nodes = [target]
        while pred[nodes[-1]] >= 0:
            nodes.append(int(pred[nodes[-1]]))
        return nodes[::-1]

    def gradient(self, nodes):
        """d(travel time along the node path)/d(current at each node), h per (m/s), shape (ny, nx, 2).
        By the envelope theorem this is also the gradient of the optimal time."""
        grid = self.grid
        sel = np.zeros(len(grid.src), bool)
        if len(nodes) > 1:
            sel[grid.edges_of(nodes)] = True
            sel &= self.ok
        G = np.zeros((grid.n, 2))
        if sel.any():
            L = grid.length[sel] * 1000.0 / 3600.0
            g = self.g[sel]
            s = np.sqrt(np.clip(self.V ** 2 - self.uperp[sel] ** 2, 1e-12, None))
            ex, ey = grid.ex[sel], grid.ey[sel]
            nx_, ny_ = -ey, ex
            # dg/du = e - (u.n / s) n ;  dt/du = -L / g^2 * dg/du
            c = self.uperp[sel] / s
            dgx, dgy = ex - c * nx_, ey - c * ny_
            dtx, dty = -L / g ** 2 * dgx, -L / g ** 2 * dgy
            for idx_arr in (grid.src[sel], grid.dst[sel]):
                np.add.at(G[:, 0], idx_arr, 0.5 * dtx)
                np.add.at(G[:, 1], idx_arr, 0.5 * dty)
        return G.reshape(grid.ny, grid.nx, 2)
