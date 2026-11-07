"""Checks of the route solver against cases with known answers.

    python -E -X utf8 tests/test_route_solver.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from oceanroute.solver import Grid, Side, Router  # noqa: E402


def grid(n_dirs=16, h=2.0):
    nx, ny = 81, 41
    return Grid(0.0, -40.0, h, nx, ny, np.ones((ny, nx), bool), n_dirs) if h == 2.0 else \
        Grid(0.0, -40.0, h, int(160 / h) + 1, int(80 / h) + 1, np.ones((int(80 / h) + 1, int(160 / h) + 1), bool), n_dirs)


def test_still_water():
    for nd, tol in ((8, 0.09), (16, 0.03), (32, 0.012)):
        g = grid(nd)
        R = Router(g, np.zeros((g.ny, g.nx)), np.zeros((g.ny, g.nx)), 1.0)
        s, t = g.node(0, 0), g.node(160, 0)
        d, _ = R.solve(None, s)
        exact = 160e3 / 1.0 / 3600
        assert abs(d[t] - exact) / exact < 1e-9, (nd, d[t], exact)   # straight along a grid line
        t2 = g.node(150, 34)
        exact2 = np.hypot(150, 34) * 1e3 / 3600
        assert 0 <= (d[t2] - exact2) / exact2 < tol, (nd, d[t2] / exact2)
    print("still water ok")


def test_uniform_current():
    g = grid(16)
    U = 0.5
    R = Router(g, np.full((g.ny, g.nx), U), np.zeros((g.ny, g.nx)), 1.0)
    d, _ = R.solve(None, g.node(0, 0))
    assert abs(d[g.node(160, 0)] - 160e3 / 1.5 / 3600) < 1e-9          # following current
    d, _ = R.solve(None, g.node(160, 0))
    assert abs(d[g.node(0, 0)] - 160e3 / 0.5 / 3600) < 1e-9            # head current
    # cross current: ground speed sqrt(V^2 - U^2)
    R = Router(g, np.zeros((g.ny, g.nx)), np.full((g.ny, g.nx), U), 1.0)
    d, _ = R.solve(None, g.node(0, 0))
    assert abs(d[g.node(160, 0)] - 160e3 / np.sqrt(0.75) / 3600) < 1e-9
    # current stronger than the vehicle: no way upstream
    R = Router(g, np.full((g.ny, g.nx), 1.2), np.zeros((g.ny, g.nx)), 1.0)
    d, _ = R.solve(None, g.node(160, 0))
    assert np.isinf(d[g.node(0, 0)])
    print("uniform current ok")


def side_of_path(g, nodes, s, t, c):
    """+1 if the path passes the zone centre on the traveller's left, -1 on the right: the sign of
    the path's offset from the s-t line where it crosses the centre's along-track position."""
    ex, ey = t[0] - s[0], t[1] - s[1]
    L = np.hypot(ex, ey)
    ex, ey = ex / L, ey / L
    pts = np.array([g.xy(k) for k in nodes])
    along = (pts[:, 0] - s[0]) * ex + (pts[:, 1] - s[1]) * ey
    left = -(pts[:, 0] - s[0]) * ey + (pts[:, 1] - s[1]) * ex
    ca = (c[0] - s[0]) * ex + (c[1] - s[1]) * ey
    i = int(np.argmin(np.abs(along - ca)))
    return np.sign(left[i])


def test_sides_and_symmetry():
    g = grid(16)
    rng = np.random.default_rng(3)
    for trial in range(6):                          # random trip directions, zone in the middle
        th = rng.uniform(0, 2 * np.pi)
        cx_, cy_ = 80.0, 0.0
        s = (cx_ - 35 * np.cos(th), cy_ - 35 * np.sin(th))
        t = (cx_ + 35 * np.cos(th), cy_ + 35 * np.sin(th))
        R = Router(g, np.zeros((g.ny, g.nx)), np.zeros((g.ny, g.nx)), 1.0)
        res = {}
        for side in "LR":
            sd = Side(g, s, t, (cx_, cy_), 8.0, side)
            d, pred = R.solve(sd.ok, g.node(*s))
            nodes = R.path(pred, g.node(*t))
            res[side] = d[g.node(*t)]
            want = 1 if side == "L" else -1
            assert side_of_path(g, nodes, s, t, (cx_, cy_)) == want, (trial, side)
        assert abs(res["L"] - res["R"]) / res["L"] < 0.03, (trial, res)
    s, t, c = (0.0, 0.0), (160.0, 0.0), (80.0, 0.0)
    # a current toward +y north of the zone: the left (north) side gets a cross current
    for sgn in (1, -1):
        v = np.where(sgn * g.Y > 0, 0.6, 0.0)
        R = Router(g, np.zeros((g.ny, g.nx)), v, 1.0)
        tl = R.solve(Side(g, s, t, c, 10.0, "L").ok, g.node(*s))[0][g.node(*t)]
        tr = R.solve(Side(g, s, t, c, 10.0, "R").ok, g.node(*s))[0][g.node(*t)]
        assert (tl > tr) if sgn == 1 else (tr > tl), (sgn, tl, tr)
    print("sides ok", round(tl, 3), round(tr, 3))


def test_gradient():
    g = grid(16)
    rng = np.random.default_rng(1)
    yy, xx = g.Y, g.X
    u = 0.3 * np.sin(xx / 25) * np.cos(yy / 30)
    v = 0.3 * np.cos(xx / 35) * np.sin(yy / 20)
    s, t = g.node(0, 0), g.node(160, 10)
    R = Router(g, u, v, 1.0)
    d, pred = R.solve(None, s)
    nodes = R.path(pred, t)
    G = R.gradient(nodes)
    du = rng.standard_normal(u.shape) * 1e-4
    dv = rng.standard_normal(u.shape) * 1e-4
    # fixed-path time change
    R2 = Router(g, u + du, v + dv, 1.0)
    code = g.src.astype(np.int64) * g.n + g.dst
    want = np.array([a * g.n + b for a, b in zip(nodes[:-1], nodes[1:])], np.int64)
    sel = np.isin(code, want)
    fd = R2.t[sel].sum() - R.t[sel].sum()
    lin = float((G[..., 0] * du).sum() + (G[..., 1] * dv).sum())
    assert abs(fd - lin) < 1e-3 * abs(fd) + 1e-9, (fd, lin)
    print("gradient ok", fd, lin)


if __name__ == "__main__":
    test_still_water()
    test_uniform_current()
    test_sides_and_symmetry()
    test_gradient()
