"""Anytime route planner: cross-entropy search over waypoint routes, each route scored on
imagined fields (ensemble members). One "rollout" = one route scored on one member; the
planner is given a budget of rollouts and spends it in batches.

Route value on a member = the highest field value the vehicle would pass before the time
budget runs out (never below the best value already found), i.e. how dense a patch the
route reaches. A route is a polyline from the vehicle through K waypoints (cell coords)."""
import numpy as np
from numba import njit


@njit(cache=True)
def _route_cells(px, py, wps, step, speed, t_left, mask, out_cells, out_t):
    """Rasterize a polyline; returns number of distinct consecutive cells reached in time.
    speed in cells per minute, t_left in minutes."""
    ny, nx = mask.shape
    n = 0
    t = 0.0
    x, y = px, py
    last = -1
    for k in range(wps.shape[0]):
        tx, ty = wps[k, 0], wps[k, 1]
        dx, dy = tx - x, ty - y
        dist = np.sqrt(dx * dx + dy * dy)
        nsteps = int(dist / step) + 1
        for s in range(1, nsteps + 1):
            fx = x + dx * s / nsteps
            fy = y + dy * s / nsteps
            t += dist / nsteps / speed
            if t > t_left:
                return n
            ix = int(fx + 0.5)
            iy = int(fy + 0.5)
            if ix < 0 or iy < 0 or ix >= nx or iy >= ny:
                return n
            if not mask[iy, ix]:
                return n
            c = iy * nx + ix
            if c != last:
                out_cells[n] = c
                out_t[n] = t
                n += 1
                last = c
        x, y = tx, ty
    return n


@njit(cache=True)
def score_routes(px, py, W, members, member_idx, best, speed, t_left, mask, t_eval):
    """W: (B, K, 2) waypoints; members: (N, ny*nx) flattened fields; member_idx: (m,) which
    members to use. Returns (B, m) route values.

    Value of a route on an imagined ocean = the best water found so far, averaged over the
    rest of the evaluation window t_eval: it rises when the route reaches denser water, so
    arriving sooner is worth more; after the cruising time t_left runs out the best value is
    frozen until the window ends."""
    B = W.shape[0]
    m = member_idx.shape[0]
    out = np.empty((B, m))
    cells = np.empty(4096, np.int64)
    ts = np.empty(4096)
    span = max(t_eval, 1e-6)
    for b in range(B):
        n = _route_cells(px, py, W[b], 0.5, speed, t_left, mask, cells, ts)
        for j in range(m):
            row = member_idx[j]
            run = best
            acc = 0.0
            t_prev = 0.0
            for i in range(n):
                f = members[row, cells[i]]
                if run == -np.inf:
                    run = f
                    t_prev = ts[i]
                    continue
                acc += run * (ts[i] - t_prev)
                t_prev = ts[i]
                if f > run:
                    run = f
            if run == -np.inf:
                out[b, j] = best
            else:
                acc += run * (span - t_prev)
                out[b, j] = acc / (span - (0.0 if best != -np.inf else ts[0] if n > 0 else 0.0))
    return out


class CEMPlanner:
    """Keeps a Gaussian over K waypoints (continuous cell coords) and refines it as rollouts
    are spent; the best route found so far is the plan. State persists between calls
    (warm start), but the plan is re-scored when the belief changes."""

    def __init__(self, shape, mask, n_waypoints=2, batch=64, members_per_route=16,
                 elite_frac=0.15, explore_frac=0.3, rng=None, n_holdout=0):
        self.ny, self.nx = shape
        self.mask = mask
        self.K = n_waypoints
        self.batch = batch
        self.m = members_per_route
        self.elite = max(2, int(elite_frac * batch))
        self.explore = explore_frac
        self.rng = rng or np.random.default_rng(0)
        self.mu = None
        self.sd = None
        self.plan = None
        self.plan_value = -np.inf
        self.spent = 0
        self.history = []
        self.elites = None      # (E, K, 2) best distinct routes seen in the last call
        self.trace = []         # (rollouts spent in the last call, plan value) after each batch
        self.gain_all = 0.0     # plan improvement of the last call, scored on all members
        self.gain_holdout = 0.0 # the same improvement scored only on held-out members
        self.trace_holdout = [] # (rollouts spent in the last call, plan value on held-out members)
        self.used_last = 0      # rollouts spent in the last call
        self.n_holdout = n_holdout  # the last n_holdout members are never used by the search

    def reset(self, px, py):
        self.mu = np.tile([[self.nx / 2, self.ny / 2]], (self.K, 1)).astype(float)
        self.mu[:, 0] = px
        self.mu[:, 1] = py
        self.sd = np.full((self.K, 2), max(self.nx, self.ny) / 3)
        self.plan = None
        self.plan_value = -np.inf

    def _sample(self, n, px, py):
        W = self.mu[None] + self.sd[None] * self.rng.standard_normal((n, self.K, 2))
        n_exp = int(self.explore * n)
        if n_exp:
            W[:n_exp] = self.rng.uniform([0, 0], [self.nx - 1, self.ny - 1], (n_exp, self.K, 2))
        W[..., 0] = np.clip(W[..., 0], 0, self.nx - 1)
        W[..., 1] = np.clip(W[..., 1], 0, self.ny - 1)
        return W

    def think(self, belief_flat, px, py, best, speed, t_left, budget, t_eval=None):
        """Spend `budget` rollouts. Returns the plan (K, 2) and its estimated value.
        t_left: cruising minutes left; t_eval: minutes left in the evaluation window."""
        if t_eval is None:
            t_eval = t_left
        if self.mu is None:
            self.reset(px, py)
        N_all = belief_flat.shape[0]
        N = N_all - self.n_holdout     # members the search may look at
        m = min(self.m, N)
        used = 0
        self.trace = []
        self.trace_holdout = []
        pool_W, pool_v = [], []
        plan_before = None if self.plan is None else self.plan.copy()
        # re-score the current plan on the current belief with fresh members
        if self.plan is not None:
            idx = self.rng.choice(N, m, replace=False)
            v = score_routes(px, py, self.plan[None], belief_flat, idx, best, speed, t_left, self.mask, t_eval)
            self.plan_value = v.mean()
            budget -= m
            used += m
            pool_W.append(self.plan[None].copy())
            pool_v.append(np.array([self.plan_value]))
            self.trace.append((used, self.plan_value))
        while budget >= m * 4:
            B = min(self.batch, budget // m)
            W = self._sample(B, px, py)
            if self.plan is not None:
                W[0] = self.plan
            idx = self.rng.choice(N, m, replace=False)
            V = score_routes(px, py, W, belief_flat, idx, best, speed, t_left, self.mask, t_eval)
            vals = V.mean(axis=1)
            order = np.argsort(-vals)
            if vals[order[0]] > self.plan_value or self.plan is None:
                self.plan = W[order[0]].copy()
                self.plan_value = vals[order[0]]
            el = W[order[:self.elite]]
            pool_W.append(el.copy())
            pool_v.append(vals[order[:self.elite]])
            self.mu = 0.7 * el.mean(axis=0) + 0.3 * self.mu
            self.sd = np.maximum(0.7 * el.std(axis=0) + 0.3 * self.sd, 0.5)
            budget -= B * m
            used += B * m
            self.trace.append((used, self.plan_value))
            if self.n_holdout:
                ho = np.arange(N, N_all)
                vh = score_routes(px, py, self.plan[None], belief_flat, ho, best, speed, t_left, self.mask, t_eval)
                self.trace_holdout.append((used, float(vh.mean())))
        self.spent += used
        if pool_W:
            Wp = np.concatenate(pool_W)
            vp = np.concatenate(pool_v)
            keep = np.argsort(-vp)[:32]
            self.elites = Wp[keep]
        # improvement of this call judged on every member, which the search saw only in part
        self.gain_all = 0.0
        self.gain_holdout = 0.0
        if plan_before is not None and self.plan is not None and used > m:
            pair = np.stack([plan_before, self.plan])
            v = score_routes(px, py, pair, belief_flat, np.arange(N_all), best, speed, t_left, self.mask, t_eval)
            self.gain_all = float(v[1].mean() - v[0].mean())
            if self.n_holdout:
                self.gain_holdout = float(v[1, N:].mean() - v[0, N:].mean())
        self.used_last = used
        self.history.append((self.spent, self.plan_value))
        return self.plan, self.plan_value
