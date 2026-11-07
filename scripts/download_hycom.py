"""Download HYCOM GOFS 3.1 reanalysis currents (GLBy0.08, expt_93.0; 1/12 deg, no account needed)
at 10 m depth, one snapshot at 12:00 UTC every 3 days from 2019-01-01 to 2024-08-31, over
  kuroshio    the Kuroshio east of Taiwan and the southern East China Sea (23-31 N, 121-129 E)
  gulfstream  the Gulf Stream after it leaves Cape Hatteras (33-41 N, 75-67 W), a replication region
  agulhas     the Agulhas retroflection south of Africa (43-35 S, 14-22 E; open ocean), a second one

Resumable: each block of snapshots is saved to data/raw/hycom[_<region>]/; a final merge writes
data/processed/hycom_uv10m[_<region>].npz (lat, lon, times, u, v in m/s, NaN on land).

    python -E -X utf8 scripts/download_hycom.py [--region gulfstream]
"""
import argparse
import datetime as dt
import time
from pathlib import Path

import netCDF4
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
URL = "https://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0/uv3z"
REGIONS = {"kuroshio": ((23.0, 31.0), (121.0, 129.0)), "gulfstream": ((33.0, 41.0), (285.0, 293.0)),
           "agulhas": ((-43.0, -35.0), (14.0, 22.0))}
DEPTH = 10.0
START, END, EVERY_DAYS, HOUR = dt.datetime(2019, 1, 1), dt.datetime(2024, 8, 31), 3, 12
BLOCK = 12


def read(var, idx, sy, sx, k, tries=4):
    for a in range(tries):
        try:
            return np.ma.filled(var[idx, k, sy, sx].astype(np.float32), np.nan)
        except Exception as e:      # the server drops connections now and then
            print("retry", a + 1, repr(e)[:120], flush=True)
            time.sleep(15 * (a + 1))
    raise RuntimeError("HYCOM read failed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", default="kuroshio", choices=sorted(REGIONS))
    a = ap.parse_args()
    LAT, LON = REGIONS[a.region]
    sfx = "" if a.region == "kuroshio" else "_" + a.region
    RAW = ROOT / "data" / "raw" / ("hycom" + sfx)
    OUT = ROOT / "data" / "processed" / f"hycom_uv10m{sfx}.npz"
    RAW.mkdir(parents=True, exist_ok=True)
    ds = netCDF4.Dataset(URL)
    lat, lon, dep = ds["lat"][:], ds["lon"][:], ds["depth"][:]
    tv = ds["time"]
    times = netCDF4.num2date(tv[:], tv.units, only_use_cftime_datetimes=False)
    times = np.array([dt.datetime(t.year, t.month, t.day, t.hour) for t in times])
    iy = np.where((lat >= LAT[0]) & (lat <= LAT[1]))[0]
    ix = np.where((lon >= LON[0]) & (lon <= LON[1]))[0]
    sy, sx = slice(iy[0], iy[-1] + 1), slice(ix[0], ix[-1] + 1)
    k = int(np.where(dep == DEPTH)[0][0])
    pos = {t: i for i, t in enumerate(times)}
    want = []
    d = START + dt.timedelta(hours=HOUR)
    while d <= END + dt.timedelta(hours=HOUR):
        if d in pos:
            want.append(pos[d])
        d += dt.timedelta(days=EVERY_DAYS)
    print(len(want), "snapshots wanted", flush=True)
    blocks = [want[i:i + BLOCK] for i in range(0, len(want), BLOCK)]
    tic = time.time()
    for b, idx in enumerate(blocks):
        f = RAW / f"block_{b:04d}.npz"
        if f.exists():
            continue
        steps = np.diff(idx)
        got = None
        if len(idx) > 1 and np.all(steps == steps[0]):
            try:
                s = slice(idx[0], idx[-1] + 1, int(steps[0]))
                got = (list(idx), read(ds["water_u"], s, sy, sx, k, tries=2), read(ds["water_v"], s, sy, sx, k, tries=2))
            except RuntimeError:
                got = None
        if got is None:            # one snapshot at a time; a snapshot the server cannot deliver is skipped
            keep, us, vs = [], [], []
            for i in idx:
                try:
                    us.append(read(ds["water_u"], i, sy, sx, k, tries=3))
                    vs.append(read(ds["water_v"], i, sy, sx, k, tries=3))
                    keep.append(i)
                except RuntimeError:
                    print("skipped", times[i], flush=True)
            got = (keep, np.stack(us) if us else np.zeros((0, len(iy), len(ix)), np.float32),
                   np.stack(vs) if vs else np.zeros((0, len(iy), len(ix)), np.float32))
        keep, u, v = got
        np.savez_compressed(f, idx=np.array(keep), times=np.array([str(times[i]) for i in keep]), u=u, v=v)
        print(f"block {b + 1}/{len(blocks)} {time.time() - tic:.0f}s", flush=True)
    parts = [np.load(RAW / f"block_{b:04d}.npz") for b in range(len(blocks))]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(OUT, lat=np.asarray(lat[sy], np.float64), lon=np.asarray(lon[sx], np.float64),
                        times=np.concatenate([p["times"] for p in parts]),
                        u=np.concatenate([p["u"] for p in parts]), v=np.concatenate([p["v"] for p in parts]))
    print("done", OUT, flush=True)


if __name__ == "__main__":
    main()
