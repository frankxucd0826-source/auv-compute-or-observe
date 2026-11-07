"""Fig.: the study region and what a stale coarse current map gets wrong.
(a) mean current at 10 m (2019-2021, HYCOM) with the Kuroshio, and the test missions' no-go zones;
(b) typical error of the 1-degree map made 3 days earlier (RMS over the development years);
(c) how far that error stays correlated, for the stale 1-degree map and a same-day 0.5-degree map."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style as st  # noqa: E402

sys.path.insert(0, str(st.ROOT / "src"))
from oceanroute.fields import Snapshots, LAT0, LON0, KM_LAT, KM_LON  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patheffects as pe  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

SPEED = LinearSegmentedColormap.from_list("speed", ["#F4F8FB", "#C9E2F0", "#7DB8DA", "#3B8BC2", "#1F5F99", "#16325C"])
ERR = LinearSegmentedColormap.from_list("err", ["#FBF7F0", "#F5DEB3", "#EDB36B", "#D9822B", "#B5541C", "#7A2E12"])
LAND = LinearSegmentedColormap.from_list("land", ["#D9D4CC", "#D9D4CC"])
STALE, FRESH = "#B5541C", "#3B8BC2"


def binned(d, r, step=8.0, top=200.0):
    xs, ys = [0.0], [1.0]
    for a in np.arange(0, top, step):
        m = (d >= a) & (d < a + step)
        if m.any():
            xs.append(a + step / 2)
            ys.append(float(r[m].mean()))
    return np.array(xs), np.array(ys)


def main():
    st.setup()
    S = Snapshots()
    yr = S.times.astype("datetime64[Y]").astype(int) + 1970
    dev = (yr >= 2019) & (yr <= 2021)
    mu, mv = np.nanmean(S.u[dev], 0), np.nanmean(S.v[dev], 0)
    spd = np.where(S.water, np.hypot(mu, mv), np.nan)
    E1 = np.load(st.ROOT / "results" / "route_errormodel_deg1.0_lag1.npz")
    E0 = np.load(st.ROOT / "results" / "route_errormodel_deg0.5_lag0.npz")
    err = np.where(S.water, np.sqrt((E1["su"] ** 2 + E1["sv"] ** 2) / 2), np.nan)
    H = 64 * st.MM
    fig = plt.figure(figsize=(st.TEXTW, H))
    w = 0.25
    h = w * st.TEXTW * (KM_LAT / KM_LON) / H
    axa = fig.add_axes([0.07, 0.20, w, h])
    caa = fig.add_axes([0.07 + w + 0.008, 0.20, 0.010, h])
    axb = fig.add_axes([0.395, 0.20, w, h])
    cab = fig.add_axes([0.395 + w + 0.008, 0.20, 0.010, h])
    axc = fig.add_axes([0.785, 0.20, 0.20, h])
    ext = [S.lon[0], S.lon[-1], S.lat[0], S.lat[-1]]
    asp = KM_LAT / KM_LON
    land = np.where(S.water, np.nan, 1.0)
    for ax in (axa, axb):
        ax.imshow(land, origin="lower", extent=ext, cmap=LAND, aspect=asp, interpolation="nearest")
        ax.set_xticks([122, 125, 128])
        ax.set_xticklabels(["122°E", "125°E", "128°E"])
        ax.set_yticks([24, 26, 28, 30])
        ax.set_yticklabels(["24°N", "26°N", "28°N", "30°N"])
        ax.grid(False)
        for s_ in ax.spines.values():
            s_.set_visible(True)
    im = axa.imshow(spd, origin="lower", extent=ext, cmap=SPEED, vmin=0, vmax=1.0, aspect=asp, interpolation="bilinear")
    LON, LAT = np.meshgrid(S.lon, S.lat)
    sel = (slice(6, None, 14), slice(3, None, 7))
    axa.quiver(LON[sel], LAT[sel], mu[sel], mv[sel], color="#20303F", scale=7, width=0.004, headwidth=3.5, alpha=0.85)
    f = st.ROOT / "results" / "route_main_test" / "results.jsonl"
    if f.exists():
        C = np.array([json.loads(l)["c"] for l in open(f, encoding="utf-8") if "skip" not in l])
        axa.scatter(LON0 + C[:, 0] / KM_LON, LAT0 + C[:, 1] / KM_LAT, s=4, color="#F08C00", alpha=0.6, lw=0)
    axa.text(126.6, 27.15, "黑潮", fontsize=9.5, color="#16325C", rotation=38, ha="center", va="center",
             path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])
    cb = fig.colorbar(im, cax=caa, ticks=[0, 0.5, 1.0])
    cb.ax.set_title("米/秒", fontsize=8, pad=4)
    cb.ax.tick_params(labelsize=8)
    axb.set_yticklabels([])
    im2 = axb.imshow(err, origin="lower", extent=ext, cmap=ERR, vmin=0, vmax=0.3, aspect=asp, interpolation="bilinear")
    cb2 = fig.colorbar(im2, cax=cab, ticks=[0, 0.1, 0.2, 0.3])
    cb2.ax.set_title("米/秒", fontsize=8, pad=4)
    cb2.ax.tick_params(labelsize=8)
    for E, col in ((E1, STALE), (E0, FRESH)):
        d = np.r_[E["dist_x"], E["dist_y"]]
        r = np.r_[E["rho_x"], E["rho_y"]]
        x, y = binned(d, r)
        axc.plot(x, y, color=col, lw=2.2)
        axc.axvline(float(E["ell"]), color=col, lw=1.0, ls=(0, (3, 2)))
    axc.text(22, 0.98, "当天 0.5° 图\n约 18 千米", color=FRESH, fontsize=8.2, va="top")
    axc.text(82, 0.70, "3 天前 1° 粗图\n约 76 千米", color=STALE, fontsize=8.2, va="top")
    axc.set_xlim(0, 200)
    axc.set_xticks([0, 100, 200])
    axc.set_ylim(-0.15, 1.02)
    axc.set_ylabel("误差的相关系数")
    for s_ in ("top", "right"):
        axc.spines[s_].set_visible(True)
    st.caption(axa, "(a) 研究海区与平均海流", y=-0.17)
    st.caption(axb, "(b) 3 天前 1° 粗图的典型误差", y=-0.17)
    st.caption(axc, "(c) 相关系数随两点距离（千米）", y=-0.17)
    st.save(fig, "fig_route_data")


if __name__ == "__main__":
    main()
