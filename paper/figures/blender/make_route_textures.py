"""Textures and geometry for the 3-D scene of Fig. 1 (run with the ordinary Python, not Blender).

The sea surface is the real current of the example mission (2022-01-18); the stacked sheets above it are
fields of the plausible set along the line from the coarse map to the counterexample,
u(t) = map + t (counterexample - map), t = -1 ... 1 (all inside the set, |t z*| <= r); t = 0 is the coarse map.
Writes ../renders/textures/route_*.png and route_meta.json (routes, start, goal and no-go zone in sheet units 0..1).
"""
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import rstyle as st  # noqa: E402
import rmaps as rm  # noqa: E402

TEX = os.path.join(HERE, "..", "renders", "textures")
SEA3D = LinearSegmentedColormap.from_list("sea3d", ["#0E2742", "#143E66", "#1B5A8C", "#2A79AA", "#4E9CC4", "#86C3DB", "#BFE4EF"])


def sheet(D, u, v, name, px=1600, vmax=1.0, stream_alpha=0.55, lw=0.9):
    x0, x1, y0, y1 = rm.view(D)
    fig = plt.figure(figsize=(px / 200, px / 200), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    X, Y = D["X"], D["Y"]
    ax.imshow(np.hypot(u, v), origin="lower", extent=[X.min(), X.max(), Y.min(), Y.max()], cmap=SEA3D, vmin=0,
              vmax=vmax, interpolation="bicubic")
    ax.streamplot(X[0, :], Y[:, 0], u, v, density=1.6, color="white", linewidth=lw, arrowsize=0.9)
    for c in ax.collections:
        c.set_alpha(stream_alpha)
    for p in ax.patches:
        p.set_alpha(stream_alpha)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.axis("off")
    fig.savefig(os.path.join(TEX, f"route_{name}.png"))
    plt.close(fig)


def main():
    os.makedirs(TEX, exist_ok=True)
    D = np.load(os.path.join(st.ROOT, "results", "route_example.npz"))
    M = json.load(open(os.path.join(st.ROOT, "results", "route_example.json"), encoding="utf-8"))
    sheet(D, D["truth_u"], D["truth_v"], "sea", px=2400, lw=1.1)
    mu, mv = D["map_u"], D["map_v"]
    du, dv = D["counter_u"] - mu, D["counter_v"] - mv
    for k, t in enumerate((-1.0, -0.5, 0.0, 0.5, 1.0)):
        sheet(D, mu + t * du, mv + t * dv, f"stack{k}", px=900, lw=1.4, stream_alpha=0.6)
    x0, x1, y0, y1 = rm.view(D)

    def uv(p):
        return [(float(p[0]) - x0) / (x1 - x0), (float(p[1]) - y0) / (y1 - y0)]

    meta = dict(start=uv(D["s"]), goal=uv(D["g"]), centre=uv(D["c"]), radius=15.0 / (x1 - x0),
                route_L=[uv(p) for p in D["truth_route_L"]], route_R=[uv(p) for p in D["truth_route_R"]],
                times={k: M[k] for k in M if "_time_" in k})
    json.dump(meta, open(os.path.join(TEX, "route_meta.json"), "w"), indent=1)
    print("textures written", meta["start"], meta["goal"], meta["centre"], meta["radius"])


if __name__ == "__main__":
    main()
