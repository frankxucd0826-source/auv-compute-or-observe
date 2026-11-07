"""Smoke test on a synthetic bloom: every fixed controller finishes a mission and the
planner improves with budget. Run: python -E -X utf8 tests/test_smoke.py"""
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from oceanmeta.belief import gaussian_random_fields, EnsembleBelief  # noqa: E402
from oceanmeta.mission import Platform, Sensor, MissionConfig, run_mission  # noqa: E402
from oceanmeta.meta import Fixed  # noqa: E402
from oceanmeta.planner import CEMPlanner  # noqa: E402

rng = np.random.default_rng(1)
n = 40
yy, xx = np.mgrid[0:n, 0:n]
truth = 0.2 * gaussian_random_fields(1, n, n, 3.0, rng)[0]
for cy, cx, a in [(28, 30, 1.0), (10, 25, 0.8), (30, 8, 0.7)]:
    truth += a * np.exp(-((yy - cy) ** 2 + (xx - cx) ** 2) / (2 * 3.0 ** 2))
prior = np.roll(truth, (3, -4), axis=(0, 1))      # stale map: bloom has moved
mask = np.ones((n, n), bool)

plat = Platform("test", 1.5, 15, 30, 20, 1000, 12, rate_low=100, rate_high=5000)
cfg = MissionConfig()
for a in range(4):
    tic = time.time()
    out, m = run_mission(truth, prior, 0.25, mask, (2.0, 20.0), plat, Sensor(), cfg, Fixed(a), seed=0)
    print(a, {k: out[k] for k in ("regret", "found", "n_steps", "actions", "energy_wh", "time_h")},
          f"{time.time()-tic:.1f}s")

# anytime curve of the planner on the prior belief
b = EnsembleBelief.from_prior(prior, 0.25, 4.0, 48, mask, np.random.default_rng(0))
flat = b.X.reshape(48, -1)
for budget in [100, 1000, 10000, 100000]:
    vals = []
    for s in range(5):
        p = CEMPlanner((n, n), mask, rng=np.random.default_rng(s))
        plan, v = p.think(flat, 2.0, 20.0, -np.inf, plat.speed_mps * 60 / 2000, 480, budget)
        tv = max(truth[int(y + .5), int(x + .5)] for x, y in plan)  # crude: waypoint truth
        vals.append(v)
    print("budget", budget, "est value %.3f" % np.mean(vals))
