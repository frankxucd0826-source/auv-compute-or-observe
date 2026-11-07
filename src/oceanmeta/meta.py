"""Controllers that decide, every interval, how the vehicle spends it (see mission.py)."""
import numpy as np

from .mission import GO, GO_THINK, DRIFT, DRIFT_THINK
from .planner import score_routes


class Fixed:
    """Always the same action."""

    def __init__(self, action):
        self.a = action
        self.name = f"fixed-{action}"

    def reset(self, m):
        pass

    def act(self, m):
        return self.a


class Periodic:
    """Repeat a pattern of actions, e.g. [GO_THINK, GO, GO] = think hard one interval in three."""

    def __init__(self, pattern):
        self.p = list(pattern)
        self.i = 0
        self.name = "periodic-" + "".join(map(str, pattern))

    def reset(self, m):
        self.i = 0

    def act(self, m):
        a = self.p[self.i % len(self.p)]
        self.i += 1
        return a


def _leg_cells(m, minutes):
    """Cells the executed plan would sample in the next `minutes`, and the end position."""
    return m.predict_leg(minutes)


class Rational:
    """One-step rational metareasoning. Every action is valued in the mission's own currency,
    the expected value (log10 chlorophyll) of the densest water the best route reaches:

    GO           routes re-scored from where the next leg ends, with one interval less, on the
                 belief updated by the samples that leg would take (preposterior over imagined
                 truths drawn from the ensemble)
    DRIFT        same, but staying put and resampling the current cell
    *_THINK      the above plus the plan improvement predicted from the planner's own
                 anytime trace, minus the value lost to the extra energy the computer draws

    `allow` restricts the choice, giving the two single-axis baselines."""

    def __init__(self, allow=(GO, GO_THINK, DRIFT, DRIFT_THINK), n_hyp=16, name="rational", double=False,
                 guard=None):
        self.allow = tuple(allow)
        self.n_hyp = n_hyp
        self.name = name
        self.double = double    # judge on imagined oceans that were not used for choosing
        # leave "go" only when another use of the interval is better by more than two standard
        # errors over the imagined truths; by default on together with the held-out valuation
        self.guard = double if guard is None else guard
        self.last = {}

    def reset(self, m):
        self.rng = np.random.default_rng(12345)

    def _route_value(self, m, B, pos, best, t_left, W):
        """Value of the best candidate route. Single estimate: choose and judge on the same
        imagined oceans (biased upward by the choice). Double estimate: choose on the members
        the search uses, judge on the held-out members."""
        X = B.X.reshape(B.N, -1)
        t_eval = max(m.t_eval - m.t - m.cfg.interval_min, t_left)
        V = score_routes(pos[0], pos[1], W, X, np.arange(B.N), best, m.speed, t_left, m.mask, t_eval)
        h = m.planner.n_holdout
        if self.double and h > 0:
            k = int(V[:, :B.N - h].mean(axis=1).argmax())
            return float(V[k, B.N - h:].mean())
        return float(V.mean(axis=1).max())

    def _best_after(self, m, B, cells):
        mu = B.mean()
        vals = [mu[c] for c in list(m.visited) + list(cells)]
        return max(vals) if vals else mu[int(m.py + 0.5), int(m.px + 0.5)]

    def _preposterior(self, m, cells, pos, t_left, W, js, z):
        """Best route value after observing `cells`, once per imagined truth js[k] (with
        observation noise z[k]); the same truths and noise are used for every action, so the
        actions are compared pairwise.

        Mid-mission, an observation is worth what it changes in the next route: the floor of
        the route value (the best water found so far) is held at its present estimate. Sharper
        knowledge of which visited water to report only pays at the end, and can be bought
        then; crediting it earlier makes the vehicle stop to resample too soon. In the last two
        intervals the floor is updated with the imagined observations."""
        final = t_left <= 2 * m.cfg.interval_min
        best_now = self._best_after(m, m.belief, [])
        if not cells:
            v = self._route_value(m, m.belief, pos, best_now, t_left, W)
            return np.full(len(js), v)
        out = np.empty(len(js))
        r = m.sensor.noise_sd ** 2
        for k, j in enumerate(js):
            B = m.belief.copy()
            ys = [m.belief.X[j][c] + m.sensor.noise_sd * z[k, i % z.shape[1]] for i, c in enumerate(cells)]
            B.update_many(cells, ys, r)
            floor = self._best_after(m, B, cells) if final else best_now
            out[k] = self._route_value(m, B, pos, floor, t_left, W)
        return out

    def _voc(self, m):
        """Predicted extra plan value from the high-power budget this interval: the last call's
        improvement, judged on all members (less selection bias than the search's own scores),
        per log-rollout, extrapolated with diminishing returns."""
        pl = m.planner
        p = m.platform
        r0 = 4 * pl.m
        dt = m.cfg.interval_min
        if self.double and pl.n_holdout > 0:
            if pl.used_last <= r0:
                return 0.0
            slope = max(0.0, pl.gain_holdout) / np.log((pl.used_last + r0) / r0)
        else:
            # the planner's own view: improvement of its search scores during the last call
            tr = pl.trace
            if len(tr) < 2 or tr[-1][0] <= tr[0][0]:
                return 0.0
            slope = max(0.0, tr[-1][1] - tr[0][1]) / np.log((tr[-1][0] + r0) / (tr[0][0] + r0))
        return slope * np.log((p.rate_high * dt + r0) / (p.rate_low * dt + r0))

    def act(self, m):
        if m.exec_plan is None or m.planner.elites is None:
            return GO_THINK if GO_THINK in self.allow else GO
        p, dt = m.platform, m.cfg.interval_min
        E = m.planner.elites
        leg, pos_go, wp_after = m.predict_leg(dt, with_waypoint=True)

        def with_rest(i0):
            # the plan being executed is always a candidate, continued from waypoint i0
            rest = m.exec_plan[i0:] if i0 < len(m.exec_plan) else m.exec_plan[-1:]
            rest = np.concatenate([rest, np.repeat(rest[-1:], E.shape[1], 0)])[:E.shape[1]]
            return np.concatenate([rest[None], E])
        W_go, W_stay = with_rest(wp_after), with_rest(m._wp_i)
        # cruising time left after each choice (drifting saves propulsion energy, the
        # high-performance computer costs energy)
        t_after = {a: m.time_left_after(a) for a in (GO, GO_THINK, DRIFT, DRIFT_THINK)}

        n_drift = int(dt / m.sensor.drift_sample_min)
        here = (int(m.py + 0.5), int(m.px + 0.5))
        dwell = [here] * n_drift if m.mask[here] else []
        vals = {}
        voc = self._voc(m)
        js = self.rng.choice(m.belief.N, self.n_hyp, replace=False)
        z = self.rng.standard_normal((self.n_hyp, 16))
        for a, cells, pos, W in ((GO, leg, pos_go, W_go), (GO_THINK, leg, pos_go, W_go),
                                 (DRIFT, dwell, (m.px, m.py), W_stay), (DRIFT_THINK, dwell, (m.px, m.py), W_stay)):
            if a not in self.allow:
                continue
            same = {GO_THINK: GO, DRIFT_THINK: DRIFT}.get(a)
            if same in vals and abs(t_after[a] - t_after[same]) < 1e-9:
                vals[a] = vals[same] + voc          # thinking costs no cruising time here
                continue
            v = self._preposterior(m, cells, pos, t_after[a], W, js, z)
            vals[a] = v + (voc if a in (GO_THINK, DRIFT_THINK) else 0.0)
        # Keep going unless another use of the interval is better by more than two standard
        # errors of the paired difference over imagined truths (the single estimate takes the
        # plain maximum, as a planner trusting its own numbers would).
        default = GO if GO in self.allow else self.allow[0]
        means = {a: float(np.mean(v)) for a, v in vals.items()}
        if self.guard:
            choice, best_gain = default, 0.0
            for a, v in vals.items():
                if a == default:
                    continue
                d = v - vals[default]
                se = d.std(ddof=1) / np.sqrt(len(d))
                if d.mean() - 2 * se > 0 and d.mean() > best_gain:
                    choice, best_gain = a, d.mean()
            self.last = dict(vals=means, voc=voc)
            return choice
        vals = means
        a = max(vals, key=vals.get)
        self.last = dict(vals=vals, voc=voc)
        return a


class Honest:
    """The proposed controller. Keep going with low-power planning by default.
    * Think (high-performance computer) when the plan improvement that more search is still
      producing, measured on imagined oceans the search never saw, is worth more than the
      energy: marginal held-out gain per log-rollout over the second half of the last planning
      call, extrapolated to the high-power budget, must exceed `price`.
    * Stop and resample only in the final hour, if imagined observations of the current water,
      judged on held-out oceans, would improve the final report by more than two standard
      errors. Stopping mid-mission is dominated: the same check can be made at the end.
    `self_assessed=True` replaces the held-out measurements by the planner's own search scores
    (what a vehicle trusting its planner would use)."""

    def __init__(self, price=0.005, name="honest", self_assessed=False, allow_dwell=True, n_hyp=16):
        self.price = price
        self.name = name
        self.self_assessed = self_assessed
        self.allow_dwell = allow_dwell
        self.n_hyp = n_hyp

    def reset(self, m):
        self.rng = np.random.default_rng(54321)

    def voc(self, m):
        """Predicted plan improvement from one interval on the high-performance computer."""
        pl, p, dt = m.planner, m.platform, m.cfg.interval_min
        r0 = 4 * pl.m
        tr = pl.trace if self.self_assessed else pl.trace_holdout
        if len(tr) >= 4:
            # marginal improvement over the second half of the last call
            (ra, va), (rb, vb) = tr[len(tr) // 2], tr[-1]
            slope = max(0.0, vb - va) / np.log(rb / ra) if rb > ra else 0.0
        else:
            # too few batches (slow computer): improvement over the whole last call
            if pl.used_last <= 0:
                return 0.0
            gain = (tr[-1][1] - pl.trace[0][1]) if (self.self_assessed and len(tr) >= 1) else pl.gain_holdout
            slope = max(0.0, gain) / np.log((pl.used_last + r0) / r0)
        r_low, r_high = p.rate_low * dt, p.rate_high * dt
        return slope * np.log((r_high + r0) / (r_low + r0))

    def act(self, m):
        dt = m.cfg.interval_min
        if m.exec_plan is None:
            return GO_THINK
        if self.allow_dwell and m.time_left_after(DRIFT) <= 3 * dt:
            here = (int(m.py + 0.5), int(m.px + 0.5))
            if m.mask[here] and self._dwell_gain(m, here) > 0:
                return DRIFT
        return GO_THINK if self.voc(m) > self.price else GO

    def _dwell_gain(self, m, here):
        """Paired gain in the expected true value of the final report from resampling the
        current water for one interval, judged on held-out members (lower confidence bound)."""
        B0 = m.belief
        N, h = B0.N, m.planner.n_holdout
        cells = list(m.visited)
        if not cells:
            return 0.0
        n = int(dt_samples(m))
        js = self.rng.choice(N, self.n_hyp, replace=False)
        r = m.sensor.noise_sd ** 2
        gains = []
        for j in js:
            B = B0.copy()
            ys = [B0.X[j][here] + m.sensor.noise_sd * self.rng.standard_normal() for _ in range(n)]
            B.update_many([here] * n, ys, r)
            mu_a = B.X[:N - h].mean(axis=0) if (h and not self.self_assessed) else B.mean()
            mu_0 = B0.X[:N - h].mean(axis=0) if (h and not self.self_assessed) else B0.mean()
            pick_a = max(cells, key=lambda c: mu_a[c])
            pick_0 = max(cells, key=lambda c: mu_0[c])
            judge = B.X[N - h:] if (h and not self.self_assessed) else B.X
            gains.append(float(judge[:, pick_a[0], pick_a[1]].mean() - judge[:, pick_0[0], pick_0[1]].mean()))
        g = np.array(gains)
        return g.mean() - 2 * g.std(ddof=1) / np.sqrt(len(g))


def dt_samples(m):
    return max(1, int(m.cfg.interval_min / m.sensor.drift_sample_min))


STRATEGIES = {"go": [GO], "think": [GO_THINK], "think 1 in 3": [GO_THINK, GO, GO],
              "stop and think 1 in 3": [DRIFT_THINK, GO, GO], "stop and resample 1 in 3": [DRIFT, GO, GO]}


class Rehearsal:
    """The proposed controller: before setting off, rehearse the mission in imagination and
    follow the time-allocation strategy that did best.

    The vehicle's prior is an ensemble of imagined oceans. For each of `k` of them used as the
    "true" ocean, every candidate strategy runs a complete imagined mission with the vehicle's
    own planner, computer speeds and battery (same imagined truths and noise for every
    strategy). Honest rehearsal draws the imagined truths from the members the planner never
    searches on; self-assessed rehearsal draws them from the members it does search on, so the
    planner partly knows the answer and looks better the longer it thinks."""

    def __init__(self, k=4, honest=True, strategies=None, name="rehearsal"):
        self.k = k
        self.honest = honest
        self.strategies = strategies or STRATEGIES
        self.name = name
        self.choice = None
        self.scores = {}

    def reset(self, m):
        import copy as _copy
        from .mission import Mission
        N, h = m.belief.N, m.planner.n_holdout
        pool = np.arange(N - h, N) if (self.honest and h > 0) else np.arange(0, N - h if h else N)
        rng = np.random.default_rng(97)
        truths = rng.choice(pool, self.k, replace=False)
        scores = {}
        for name, pattern in self.strategies.items():
            vals = []
            for t, j in enumerate(truths):
                im = Mission.__new__(Mission)
                im.__dict__.update(_copy.deepcopy({k: v for k, v in m.__dict__.items() if k not in ("truth",)}))
                im.truth = m.belief.X[j].copy()
                im.answers = [(0.0, float(im.truth[int(im.py + 0.5), int(im.px + 0.5)]))]
                im.rng = np.random.default_rng(1000 + t)
                im.planner.rng = im.rng
                i = 0
                while not im.done:
                    im.step(pattern[i % len(pattern)])
                    i += 1
                vals.append(im.report()["regret_avg"])
            scores[name] = float(np.mean(vals))
        self.scores = scores
        self.choice = min(scores, key=scores.get)
        self.pattern = self.strategies[self.choice]
        self.i = 0

    def act(self, m):
        a = self.pattern[self.i % len(self.pattern)]
        self.i += 1
        return a


class Learned:
    """Picks the action whose predicted change of final regret, relative to going on with
    low-power planning, is most negative (models from experiments/train_meta.py)."""

    def __init__(self, path, name="learned"):
        import pickle
        d = pickle.load(open(path, "rb"))
        self.models = d["models"]
        self.name = name

    def reset(self, m):
        pass

    def act(self, m):
        from .features import features
        if m.exec_plan is None:
            return GO
        x = features(m)[None]
        adv = np.array([mdl.predict(x)[0] for mdl in self.models])
        k = int(adv.argmin())
        return k + 1 if adv[k] < 0 else GO


class StrategySelector:
    """Every `hold` intervals, predict from the vehicle's features which time-allocation
    strategy leads to the lowest final regret from here on, and follow it."""

    def __init__(self, path, hold=3, name="selector"):
        import pickle
        d = pickle.load(open(path, "rb"))
        self.models = d["models"]
        self.strategies = d["strategies"]
        self.margin = d["margin"]
        self.hold = hold
        self.name = name

    def reset(self, m):
        self.k = 0
        self.cur = self.strategies[0]
        self.phase = 0
        self.chosen = []

    def act(self, m):
        from .features import features
        if m.exec_plan is not None and self.k % self.hold == 0:
            x = features(m)[None]
            pred = np.array([mdl.predict(x)[0] for mdl in self.models])
            j = int(pred.argmin())
            s = j + 1 if pred[j] < -self.margin else 0
            if self.strategies[s] is not self.cur:
                self.cur = self.strategies[s]
                self.phase = 0
            self.chosen.append(s)
        self.k += 1
        a = self.cur[self.phase % len(self.cur)]
        self.phase += 1
        return a


def _clear(mask, x0, y0, x1, y1):
    """True if the straight segment from (x0, y0) to (x1, y1) stays in navigable water."""
    d = float(np.hypot(x1 - x0, y1 - y0))
    n = int(d / 0.5) + 1
    for s in range(n + 1):
        x = x0 + (x1 - x0) * s / n
        y = y0 + (y1 - y0) * s / n
        if not mask[int(y + 0.5), int(x + 0.5)]:
            return False
    return True


class RouteRule:
    """Survey rules from ocean sampling practice that steer without imagined rollouts (the
    vehicle always goes; its computers do not plan routes):
      lawnmower  pre-planned parallel lanes 16 km apart, run across the window from the launch
                 edge (the standard coverage survey)
      greedy     head for the unvisited cell of highest estimated chlorophyll (ensemble mean)
      ucb        the same with mean + 2 standard deviations (upper-confidence-bound sampling)
      thompson   draw one imagined ocean every interval and head for its densest unvisited cell
    The vehicle's map is updated from its samples and the report is made exactly as for the
    other controllers."""

    def __init__(self, kind, beta=2.0, spacing=8):
        self.kind = kind
        self.beta = beta
        self.spacing = spacing
        self.name = kind

    def reset(self, m):
        self.rng = np.random.default_rng(4242)
        m.route_rule = self.route
        if self.kind == "lawnmower":
            self.lanes = self._lanes(m)
            self.k = 0

    def act(self, m):
        return GO

    def _lanes(self, m):
        ny, nx = m.mask.shape
        x0, y0 = m.px, m.py
        d = {"w": x0, "e": nx - 1 - x0, "s": y0, "n": ny - 1 - y0}
        edge = min(d, key=d.get)
        across_x = edge in ("w", "e")                 # lanes run along x when starting west/east
        size_v = ny if across_x else nx
        v0 = y0 if across_x else x0
        u_ends = ([nx - 1, 0] if edge == "w" else [0, nx - 1]) if across_x else \
                 ([ny - 1, 0] if edge == "s" else [0, ny - 1])
        step = self.spacing if v0 < size_v / 2 else -self.spacing
        pts, v, k = [], v0, 0
        while 0 <= v <= size_v - 1:
            u = u_ends[k % 2]
            pts.append((u, v) if across_x else (v, u))
            v += step
            if 0 <= v <= size_v - 1:
                pts.append((u, v) if across_x else (v, u))
            k += 1
        return [(float(x), float(y)) for x, y in pts]

    def route(self, m, fx, fy):
        if self.kind == "lawnmower":
            while self.k < len(self.lanes) and np.hypot(self.lanes[self.k][0] - fx,
                                                        self.lanes[self.k][1] - fy) < 1.0:
                self.k += 1
            while self.k < len(self.lanes):
                tx, ty = self.lanes[self.k]
                if _clear(m.mask, fx, fy, tx, ty):
                    plan = [(tx, ty)]
                    if self.k + 1 < len(self.lanes) and _clear(m.mask, tx, ty, *self.lanes[self.k + 1]):
                        plan.append(self.lanes[self.k + 1])
                    return np.array(plan)
                self.k += 1
            score = m.belief.mean()            # lanes exhausted or blocked: head for the densest water
        elif self.kind == "greedy":
            score = m.belief.mean()
        elif self.kind == "ucb":
            score = m.belief.mean() + self.beta * m.belief.std()
        elif self.kind == "thompson":
            score = m.belief.X[int(self.rng.integers(m.belief.N))]
        else:
            raise ValueError(self.kind)
        s = np.where(m.mask, score, -np.inf)
        for c in m.visited:
            s[c] = -np.inf
        for idx in np.argsort(-s, axis=None)[:300]:
            iy, ix = divmod(int(idx), s.shape[1])
            if not np.isfinite(s[iy, ix]):
                break
            if _clear(m.mask, fx, fy, ix, iy):
                return np.array([[float(ix), float(iy)]])
        return None


def make(spec):
    if spec in ("lawnmower", "greedy", "ucb", "thompson"):
        return RouteRule(spec)
    if spec in ("rehearsal", "rehearsal-self"):
        return Rehearsal(honest=(spec == "rehearsal"), name=spec)
    if spec.startswith("rehearsal-k"):
        return Rehearsal(k=int(spec.split("k")[1]), name=spec)
    if spec.startswith("honest"):
        # honest, honest-0.01 (price), honest-nodwell, selfassessed-0.005
        parts = spec.split("-")
        price = float(parts[1]) if len(parts) > 1 and parts[1][0].isdigit() else 0.005
        return Honest(price=price, name=spec, allow_dwell="nodwell" not in spec)
    if spec.startswith("selfassessed"):
        parts = spec.split("-")
        price = float(parts[1]) if len(parts) > 1 else 0.005
        return Honest(price=price, name=spec, self_assessed=True)
    if spec == "rational":
        return Rational()
    if spec == "rational-compute":
        return Rational(allow=(GO, GO_THINK), name=spec)
    if spec == "rational-sense":
        return Rational(allow=(GO, DRIFT), name=spec)
    if spec == "double":
        return Rational(name=spec, double=True)
    if spec == "double-noguard":      # held-out valuation, plain maximum (one change from "rational")
        return Rational(name=spec, double=True, guard=False)
    if spec == "rational-guard":      # searched valuation, two-standard-error rule (the other change)
        return Rational(name=spec, double=False, guard=True)
    if spec == "double-compute":
        return Rational(allow=(GO, GO_THINK), name=spec, double=True)
    if spec == "double-sense":
        return Rational(allow=(GO, DRIFT), name=spec, double=True)
    if spec.startswith("selector:"):
        from pathlib import Path
        root = Path(__file__).resolve().parents[2]
        return StrategySelector(root / "results" / spec.split(":", 1)[1] / "models.pkl", name=spec)
    if spec.startswith("learned:"):
        from pathlib import Path
        root = Path(__file__).resolve().parents[2]
        return Learned(root / "results" / spec.split(":", 1)[1] / "models.pkl", name=spec)
    return None
