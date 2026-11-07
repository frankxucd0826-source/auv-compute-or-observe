"""Fig. 3: the three study regions and what a stale coarse current map gets wrong (development years).
(a)-(c) typical error of the 1-degree map made 3 days earlier (RMS of map minus real current), with the
mean current at 10 m (streamlines) and the no-go zones of the test missions (dots);
(d) typical error against how far the error stays correlated, for every map a vehicle carries in the
experiments (three regions' stale 1-degree maps, the stale altimetry map, and a same-day 0.5-degree map)."""
import json

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.colorbar import ColorbarBase

import rstyle as st

ERR = LinearSegmentedColormap.from_list("err", ["#FFF9F0", "#FCE3BF", "#F6BE7E", "#EA8F45", "#CC6224", "#963C14", "#5E220A"])
VMAX = 0.6
LAND = "#CED4DA"
REG = [  # tag, npz, error model, lat0, lon0, lat_ref, title, extent text
    ("main", "hycom_uv10m.npz", "route_errormodel_deg1.0_lag1.npz", 23.0, 121.0, 27.0, "(a) 黑潮", "23°–31°N，121°–129°E"),
    ("gulf", "hycom_uv10m_gulfstream.npz", "route_errormodel_gulfstream_deg1.0_lag1.npz", 33.0, 285.0, 37.0,
     "(b) 湾流", "33°–41°N，75°–67°W"),
    ("agulhas", "hycom_uv10m_agulhas.npz", "route_errormodel_agulhas_deg1.0_lag1.npz", -43.0, 14.0, -39.0,
     "(c) 阿古拉斯回流区", "35°–43°S，14°–22°E"),
]


def typical(E):
    e = np.sqrt((E["su"] ** 2 + E["sv"] ** 2) / 2)
    return float(np.median(e[E["su"] > 0])), float(E["ell"])


def region_map(ax, reg):
    tag, npz, em, lat0, lon0, lat_ref, title, ext_txt = reg
    D = np.load(st.ROOT / "data" / "processed" / npz)
    lat, lon = D["lat"], D["lon"]
    years = np.array([int(str(t)[:4]) for t in D["times"]])
    dev = (years >= 2019) & (years <= 2021)
    u, v = D["u"][dev], D["v"][dev]
    water = np.isfinite(D["u"]).all(axis=0) & np.isfinite(D["v"]).all(axis=0)
    mu, mv = np.nanmean(u, 0), np.nanmean(v, 0)
    del u, v
    E = np.load(st.ROOT / "results" / em)
    err = np.sqrt((E["su"] ** 2 + E["sv"] ** 2) / 2)
    err = np.where(water & (E["su"] > 0), err, np.nan)
    ext = [lon[0], lon[-1], lat[0], lat[-1]]
    asp = 1.0 / np.cos(np.deg2rad(lat_ref))
    ax.set_facecolor(LAND)
    ax.imshow(err, origin="lower", extent=ext, cmap=ERR, vmin=0, vmax=VMAX, aspect=asp, interpolation="bilinear", zorder=0)
    su, sv = np.where(water, mu, np.nan), np.where(water, mv, np.nan)
    spd = np.hypot(su, sv)
    lw = 0.3 + 1.2 * np.clip(np.nan_to_num(spd) / 0.8, 0, 1)
    ax.streamplot(np.linspace(lon[0], lon[-1], len(lon)), np.linspace(lat[0], lat[-1], len(lat)),
                  np.nan_to_num(su), np.nan_to_num(sv), density=0.7, color="#1F2A36", linewidth=lw,
                  arrowsize=0.45, zorder=2)
    for c in ax.collections[-1:]:
        c.set_alpha(0.55)
    km_lat, km_lon = 110.57, 111.32 * np.cos(np.deg2rad(lat_ref))
    f = st.ROOT / "results" / f"route_{tag}_test" / "results.jsonl"
    C = np.array([json.loads(l)["c"] for l in open(f, encoding="utf-8") if "skip" not in l])
    ax.scatter(lon0 + C[:, 0] / km_lon, lat0 + C[:, 1] / km_lat, s=2.6, color=st.OURS, alpha=0.45, lw=0, zorder=3)
    ax.set_xlim(ext[0], ext[1])
    ax.set_ylim(ext[2], ext[3])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for s_ in ax.spines.values():
        s_.set_visible(True)
        s_.set_color("#3B4652")
        s_.set_linewidth(0.9)
    # 100 km scale bar
    L = 100.0 / km_lon
    xb, yb = ext[0] + 0.05 * (ext[1] - ext[0]), ext[2] + 0.045 * (ext[3] - ext[2])
    ax.plot([xb, xb + L], [yb, yb], color="#1F2A36", lw=2.0, solid_capstyle="butt", zorder=4)
    st.note(ax, xb, yb + 0.035 * (ext[3] - ext[2]), "100 千米", size=7.4, ha="left", va="bottom")
    st.panel_title(ax, title, y=1.12)
    ax.text(0.0, 1.02, ext_txt, transform=ax.transAxes, fontsize=7.8, color=st.MUTED, ha="left", va="bottom")
    del D


def main():
    st.setup()
    H_MM = 62
    fig = plt.figure(figsize=(st.TEXTW, H_MM * st.MM))
    hmap, y0, gap = 0.635, 0.175, 0.011
    x = 0.006
    for reg in REG:
        w = hmap * (H_MM / 154) * np.cos(np.deg2rad(reg[5]))
        ax = fig.add_axes([x, y0, w, hmap])
        region_map(ax, reg)
        x += w + gap
    cax = fig.add_axes([x - gap + 0.008, y0, 0.010, hmap])
    cb = ColorbarBase(cax, cmap=ERR, norm=Normalize(0, VMAX), ticks=[0, 0.2, 0.4, 0.6])
    cb.outline.set_linewidth(0.6)
    cax.tick_params(labelsize=8.0, length=2, pad=1.5)
    cax.set_title("米/秒", fontsize=8.0, pad=3)
    lg = fig.add_axes([0.006, 0.02, 0.70, 0.10])
    lg.set_xlim(0, 1)
    lg.set_ylim(0, 1)
    lg.axis("off")
    xx = 0.0
    for kind, label in (("patch", "颜色：粗图的典型误差"), ("line", "开发年份平均海流（越粗越强）"),
                        ("dot", "测试任务的禁航区")):
        if kind == "patch":
            lg.add_patch(plt.Rectangle((xx, 0.32), 0.03, 0.36, fc="#E39A55", ec="none"))
        elif kind == "line":
            lg.plot([xx, xx + 0.03], [0.5, 0.5], color="#1F2A36", lw=1.6, alpha=0.7)
        else:
            lg.scatter([xx + 0.012], [0.5], s=10, color=st.OURS, alpha=0.85, lw=0)
        t = lg.text(xx + 0.038, 0.5, label, va="center", fontsize=8.0)
        fig.canvas.draw()
        xx = t.get_window_extent().transformed(lg.transData.inverted()).x1 + 0.04
    # (d) typical error against correlation length
    ax = fig.add_axes([0.805, y0, 0.185, hmap])
    pts = [("黑潮", "route_errormodel_deg1.0_lag1.npz", st.MAP, "o", (-0.018, 0.0, "right")),
           ("湾流", "route_errormodel_gulfstream_deg1.0_lag1.npz", st.MAP, "o", (0.026, 0.0, "left")),
           ("阿古拉斯", "route_errormodel_agulhas_deg1.0_lag1.npz", st.MAP, "o", (0.0, -10.0, "center")),
           ("测高图", "route_errormodel_altimetry_deg1.0_lag1.npz", st.MAP, "D", (0.0, 9.5, "center")),
           ("当天 0.5° 图", "route_errormodel_deg0.5_lag0.npz", st.OBS, "s", (0.022, 0.0, "left"))]
    for name, f, col, mk, (dx, dy, ha) in pts:
        e, ell = typical(np.load(st.ROOT / "results" / f))
        ax.scatter([e], [ell], s=50 if mk != "D" else 40, marker=mk, color=col, edgecolor="white", lw=1.0, zorder=3)
        st.note(ax, e + dx, ell + dy, name, col=col if col != st.MAP else st.INK, size=8.0, ha=ha)
    ax.set_xlim(0, 0.50)
    ax.set_ylim(0, 100)
    ax.set_xticks([0, 0.2, 0.4])
    ax.set_xticklabels(["0", "0.2", "0.4"])
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xlabel("典型误差（米/秒）", labelpad=2)
    ax.set_ylabel("相关长度（千米）", labelpad=1)
    st.panel_title(ax, "(d) 误差大小与相关长度", x=-0.30, y=1.12)
    ax.text(-0.30, 1.02, "灰：3 天前的图", transform=ax.transAxes, fontsize=7.8, color=st.MUTED, ha="left", va="bottom")
    st.save(fig, "route3_data")


if __name__ == "__main__":
    main()
