"""Vehicle presets. Numbers are anchored to published specifications (see notes/参数依据.md).

AUV: REMUS 100 class, 1 kWh battery, about 22 h at 3 kn (1.5 m/s), i.e. about 45 W in
cruise, split here into 15 W hotel load (navigation, sensors, a low-power ARM computer)
and 30 W propulsion. High-performance computer: an embedded GPU module drawing 10-25 W
(NVIDIA Jetson Orin NX); we use 20 W on top of the hotel load.

Rollout rates are free parameters swept in the experiments; the defaults put the
high-performance computer 50 times faster than the low-power one.
"""
from .mission import Platform


def auv(rate_low=100.0, rate_high=5000.0, p_think=20.0, t_max_h=24.0, energy_wh=1000.0):
    return Platform("AUV", speed_mps=1.5, p_hotel=15.0, p_prop=30.0, p_think=p_think,
                    energy_wh=energy_wh, t_max_h=t_max_h, rate_low=rate_low, rate_high=rate_high)


PRESETS = {"auv": auv}
