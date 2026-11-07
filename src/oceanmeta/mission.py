"""One survey mission: a vehicle looks for the densest water of a bloom (highest log10
chlorophyll) and reports its location at the end. Everything happens in the frame that moves
with the surface water, so the bloom is static and currents only matter through the age of the
prior map (which the satellite data already contain).

Every decision interval the controller picks one of four actions:
    0 GO           follow the current plan, low-power computer keeps replanning
    1 GO_THINK     follow the current plan, high-performance computer replans
    2 DRIFT        motor off, drift with the water and resample it, low-power computer
    3 DRIFT_THINK  motor off, drift, high-performance computer
The plan computed during an interval uses the belief at the start of that interval and is
adopted at its end; the samples taken during the interval are assimilated at its end.
The mission ends when the next interval would exceed the time limit or the battery."""
from dataclasses import dataclass, field
import numpy as np

from .belief import EnsembleBelief
from .planner import CEMPlanner

GO, GO_THINK, DRIFT, DRIFT_THINK = range(4)
ACTION_NAMES = ["GO", "GO_THINK", "DRIFT", "DRIFT_THINK"]


@dataclass
class Platform:
    name: str
    speed_mps: float      # through-water cruise speed
    p_hotel: float        # W: sensors, navigation, low-power computer
    p_prop: float         # W: propulsion at cruise speed
    p_think: float        # W: extra draw of the high-performance computer
    energy_wh: float      # usable battery energy
    t_max_h: float        # mission time limit
    rate_low: float       # imagined rollouts per minute, low-power computer
    rate_high: float      # imagined rollouts per minute, high-performance computer


@dataclass
class Sensor:
    noise_sd: float = 0.1            # log10 units per independent sample
    samples_per_cell: float = 2.0    # independent samples per cell length travelled
    drift_sample_min: float = 4.0    # minutes per independent sample while drifting


@dataclass
class MissionConfig:
    cell_km: float = 2.0
    interval_min: float = 20.0
    n_members: int = 48
    prior_length_cells: float = 4.0
    n_waypoints: int = 2
    members_per_route: int = 16
    n_holdout: int = 16         # imagined oceans the planner never searches on (kept for honest self-assessment)


@dataclass
class MissionLog:
    actions: list = field(default_factory=list)
    positions: list = field(default_factory=list)
    plan_values: list = field(default_factory=list)
    times: list = field(default_factory=list)
    energy: list = field(default_factory=list)


class Mission:
    def __init__(self, truth, prior_mean, prior_sd, mask, start, platform, sensor, cfg, rng):
        self.truth = truth
        self.mask = mask
        self.platform = platform
        self.sensor = sensor
        self.cfg = cfg
        self.rng = rng
        self.belief = EnsembleBelief.from_prior(prior_mean, prior_sd, cfg.prior_length_cells,
                                                cfg.n_members, mask, rng)
        self.planner = CEMPlanner(truth.shape, mask, cfg.n_waypoints,
                                  members_per_route=cfg.members_per_route, rng=rng,
                                  n_holdout=cfg.n_holdout)
        self.prior_sd0 = float(self.belief.std()[mask].mean())   # how uncertain the map starts
        self.px, self.py = float(start[0]), float(start[1])
        self.t = 0.0          # minutes
        self.e = 0.0          # Wh
        self.visited = {}     # cell -> number of samples
        self.speed = platform.speed_mps * 60 / (cfg.cell_km * 1000)   # cells per minute
        self.log = MissionLog()
        self.done = False
        self.pending = []     # samples taken this interval: (iy, ix, value)
        self.exec_plan = None # plan being executed (adopted at the end of the last interval)
        self._wp_i = 0
        self._acc = 0.0
        self.t_eval = platform.t_max_h * 60   # the operations centre's window, minutes
        self.route_rule = None   # survey rules that steer without the planner set this (meta.RouteRule)
        iy, ix = int(self.py + 0.5), int(self.px + 0.5)
        self.answers = [(0.0, float(truth[iy, ix]))]   # (time, true value of the reported water)

    # ---- quantities the controllers may read -------------------------------------------
    def best_visited(self):
        if not self.visited:
            return -np.inf, None
        mu = self.belief.mean()
        cells = list(self.visited)
        vals = [mu[c] for c in cells]
        i = int(np.argmax(vals))
        return vals[i], cells[i]

    def time_left(self):
        p = self.platform
        t_energy = (p.energy_wh - self.e) / (p.p_hotel + p.p_prop) * 60
        return max(0.0, min(p.t_max_h * 60 - self.t, t_energy))

    def time_left_after(self, action):
        """Cruising minutes left once this interval, spent on `action`, is over."""
        p = self.platform
        e_after = self.e + self.interval_cost(action)
        t_energy = (p.energy_wh - e_after) / (p.p_hotel + p.p_prop) * 60
        return max(0.0, min(p.t_max_h * 60 - self.t - self.cfg.interval_min, t_energy))

    def interval_cost(self, action):
        p = self.platform
        w = p.p_hotel + (p.p_prop if action in (GO, GO_THINK) else 0) + \
            (p.p_think if action in (GO_THINK, DRIFT_THINK) else 0)
        return w * self.cfg.interval_min / 60

    # ---- simulation ----------------------------------------------------------------------
    def _sample(self, x, y):
        ix, iy = int(x + 0.5), int(y + 0.5)
        if not self.mask[iy, ix]:
            return
        v = self.truth[iy, ix] + self.sensor.noise_sd * self.rng.standard_normal()
        self.pending.append((iy, ix, v))
        self.visited[(iy, ix)] = self.visited.get((iy, ix), 0) + 1

    def _walk(self, minutes):
        """Where following the executed plan for `minutes` leads, without changing anything:
        returns (end x, end y, waypoint index, distance since last sample, sample positions,
        idle minutes once the plan is exhausted or blocked by out-of-bounds water)."""
        px, py, wp_i, acc = self.px, self.py, self._wp_i, self._acc
        samples = []
        if self.exec_plan is None:
            return px, py, wp_i, acc, samples, minutes
        dist_left = self.speed * minutes
        step = 1.0 / self.sensor.samples_per_cell
        while dist_left > 1e-9 and wp_i < len(self.exec_plan):
            tx, ty = self.exec_plan[wp_i]
            dx, dy = tx - px, ty - py
            d = float(np.hypot(dx, dy))
            if d < 1e-6:
                wp_i += 1
                continue
            go = min(d, dist_left)
            done = 0.0
            blocked = False
            while done < go - 1e-9:
                piece = min(step - acc, go - done)
                nx_, ny_ = px + dx / d * piece, py + dy / d * piece
                if not self.mask[int(ny_ + 0.5), int(nx_ + 0.5)]:
                    blocked = True
                    break
                px, py = nx_, ny_
                done += piece
                acc += piece
                if acc >= step - 1e-9:
                    acc = 0.0
                    samples.append((px, py))
            dist_left -= done
            if blocked:
                wp_i = len(self.exec_plan)
                break
            if go >= d - 1e-9:
                wp_i += 1
        return px, py, wp_i, acc, samples, dist_left / self.speed

    def predict_leg(self, minutes, with_waypoint=False):
        """Cells the vehicle would sample and where it would be after following its plan
        (and, if asked, the index of the next waypoint it would then be heading for)."""
        px, py, wp_i, _, samples, _ = self._walk(minutes)
        cells = [(int(y + 0.5), int(x + 0.5)) for x, y in samples
                 if self.mask[int(y + 0.5), int(x + 0.5)]]
        return (cells, (px, py), wp_i) if with_waypoint else (cells, (px, py))

    def _move(self, minutes):
        """Follow the executed plan for `minutes`, sampling on the way. Returns idle minutes."""
        self.px, self.py, self._wp_i, self._acc, samples, idle = self._walk(minutes)
        for x, y in samples:
            self._sample(x, y)
        return idle

    def _drift(self, minutes):
        n = int(minutes / self.sensor.drift_sample_min)
        for _ in range(n):
            self._sample(self.px, self.py)

    def step(self, action):
        if self.done:
            return
        cost = self.interval_cost(action)
        dt = self.cfg.interval_min
        if self.t + dt > self.platform.t_max_h * 60 or self.e + cost > self.platform.energy_wh:
            self.done = True
            return
        p = self.platform
        rate = p.rate_high if action in (GO_THINK, DRIFT_THINK) else p.rate_low
        budget = int(rate * dt)
        best, _ = self.best_visited()
        if not np.isfinite(best):
            best = self.belief.mean()[int(self.py + 0.5), int(self.px + 0.5)]
        flat = self.belief.X.reshape(self.belief.N, -1)
        # The planner works on the belief at the start of the interval while the vehicle
        # executes the previous plan. Like any planner with a known computation delay, it plans
        # from where the vehicle will be when the new plan takes over, for the time left then.
        if action in (GO, GO_THINK):
            _, (fx, fy) = self.predict_leg(dt)
        else:
            fx, fy = self.px, self.py
        if getattr(self, "route_rule", None) is not None:
            new_plan, val = self.route_rule(self, fx, fy), float("nan")
        else:
            new_plan, val = self.planner.think(flat, fx, fy, best, self.speed,
                                               self.time_left_after(action), budget,
                                               t_eval=self.t_eval - self.t - dt)
        new_plan = None if new_plan is None else new_plan.copy()
        if action in (GO, GO_THINK):
            idle = self._move(dt)
            if idle > 0:
                self._drift(idle)
        else:
            self._drift(dt)
        # end of interval: adopt the plan computed on the old belief, assimilate samples
        self.exec_plan = new_plan
        self._wp_i = 0
        self.belief.update_many([(a, b) for a, b, _ in self.pending],
                                [v for _, _, v in self.pending], self.sensor.noise_sd ** 2)
        self.pending = []
        self.t += dt
        self.e += cost
        _, cell = self.best_visited()
        if cell is not None:
            self.answers.append((self.t, float(self.truth[cell])))
        self.log.actions.append(action)
        self.log.positions.append((self.px, self.py))
        self.log.plan_values.append(val)
        self.log.times.append(self.t)
        self.log.energy.append(self.e)

    def report(self):
        """Score. The operations centre can ask at any time where the densest water is; the
        vehicle answers with the visited cell of highest estimated chlorophyll (before its first
        sample: where it is). regret_avg = true maximum minus the true value of the answer,
        averaged over the evaluation window (the answer is frozen once the mission ends);
        regret = the same at the end."""
        _, cell = self.best_visited()
        tmax = float(np.nanmax(np.where(self.mask, self.truth, -np.inf)))
        ts = [a for a, _ in self.answers] + [self.t_eval]
        vs = [v for _, v in self.answers]
        avg = sum((ts[k + 1] - ts[k]) * (tmax - vs[k]) for k in range(len(vs))) / self.t_eval
        final = tmax - vs[-1]
        out = dict(regret_avg=float(avg), regret=float(final), true_max=tmax, found=float(final <= 0.1))
        hit = [a for a, v in self.answers if tmax - v <= 0.1]
        out["t_found_h"] = float(hit[0] / 60) if hit else float("nan")
        if cell is not None:
            out["cell"] = cell
        return out


def run_mission(truth, prior_mean, prior_sd, mask, start, platform, sensor, cfg, controller, seed):
    rng = np.random.default_rng(seed)
    m = Mission(truth, prior_mean, prior_sd, mask, start, platform, sensor, cfg, rng)
    controller.reset(m)
    while not m.done:
        a = controller.act(m)
        m.step(a)
    out = m.report()
    out["n_steps"] = len(m.log.actions)
    out["actions"] = np.bincount(np.array(m.log.actions, dtype=int), minlength=4).tolist()
    out["energy_wh"] = m.e
    out["time_h"] = m.t / 60
    return out, m
