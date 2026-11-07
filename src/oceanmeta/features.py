"""What the vehicle can know about itself at a decision point, as a fixed-length vector.
These are the inputs of the learned controller; all are computable on board."""
import numpy as np

from .planner import score_routes

NAMES = [
    "time_used", "energy_used", "minutes_left",
    "plan_value", "best_found", "plan_gain", "plan_spread",
    "local_sd", "local_gap", "leg_sd", "mean_sd",
    "log_rate_low", "log_speedup", "think_power_share",
    "noise", "prior_sd", "search_slope", "since_think",
]


def features(m):
    p = m.platform
    B = m.belief
    mu = B.mean()
    sd = B.std()
    best = m.best_visited()[0]
    iy, ix = int(m.py + 0.5), int(m.px + 0.5)
    if not np.isfinite(best):
        best = mu[iy, ix]
    plan_value, spread = best, 0.0
    leg_sd = sd[iy, ix]
    if m.exec_plan is not None:
        X = B.X.reshape(B.N, -1)
        v = score_routes(m.px, m.py, m.exec_plan[None], X, np.arange(B.N), best, m.speed,
                         m.time_left(), m.mask, max(m.t_eval - m.t, m.time_left()))[0]
        plan_value, spread = float(v.mean()), float(v.std())
        tx, ty = m.exec_plan[min(m._wp_i, len(m.exec_plan) - 1)]
        d = np.hypot(tx - m.px, ty - m.py)
        k = np.linspace(0, 1, 6)[1:]
        xs = np.clip((m.px + k * (tx - m.px) * min(1.0, 2.0 / max(d, 1e-6))).round().astype(int), 0, m.mask.shape[1] - 1)
        ys = np.clip((m.py + k * (ty - m.py) * min(1.0, 2.0 / max(d, 1e-6))).round().astype(int), 0, m.mask.shape[0] - 1)
        leg_sd = float(sd[ys, xs].mean())
    tr = m.planner.trace
    slope = 0.0
    if len(tr) >= 2 and tr[-1][0] > tr[0][0]:
        r0 = max(tr[0][0], 1)
        slope = max(0.0, tr[-1][1] - tr[0][1]) / np.log((tr[-1][0] + r0) / (tr[0][0] + r0))
    acts = m.log.actions
    since = len(acts) - 1 - max([i for i, a in enumerate(acts) if a in (1, 3)], default=-1) if acts else 0
    return np.array([
        m.t / (p.t_max_h * 60), m.e / p.energy_wh, m.time_left() / 1440,
        plan_value, best, plan_value - best, spread,
        sd[iy, ix], mu[iy, ix] - best, leg_sd, float(sd[m.mask].mean()),
        np.log10(p.rate_low), np.log10(p.rate_high / p.rate_low), p.p_think / (p.p_hotel + p.p_prop),
        m.sensor.noise_sd, m.prior_sd0, slope, min(since, 20) / 20,
    ], dtype=np.float64)
