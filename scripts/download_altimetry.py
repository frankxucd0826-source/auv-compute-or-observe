"""Download the map a real vehicle could carry: NOAA CoastWatch near-real-time blended altimetry
surface geostrophic currents (noaacwBLENDEDNRTcurrentsDaily: 0.25 deg, daily, absolute geostrophic
currents with the CNES/CLS 2013 mean dynamic topography; public ERDDAP, no account), over the study
region, 2018-12-01 to 2024-08-31.

One request per month is saved to data/raw/altimetry_<region>/<year>_<month>.nc; a final merge writes
data/processed/altimetry_<region>.npz (dates, lat, lon, u, v in m/s, NaN where missing or land).

    python -E -X utf8 scripts/download_altimetry.py [--region kuroshio]
"""
import argparse
import time
import urllib.request
from pathlib import Path

import netCDF4
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
URL = "https://coastwatch.noaa.gov/erddap/griddap/noaacwBLENDEDNRTcurrentsDaily.nc"
REGIONS = {"kuroshio": ((23.0, 31.0), (121.0, 129.0))}
def month_spans(first=(2018, 12), last=(2024, 8)):
    """One request per month (a year at once trips the server's proxy now and then)."""
    import calendar
    y, m = first
    out = []
    while (y, m) <= last:
        out.append((f"{y}-{m:02d}-01", f"{y}-{m:02d}-{calendar.monthrange(y, m)[1]:02d}"))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


SPANS = month_spans()


def get(url, tries=4):
    for a in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=600) as r:
                return r.read()
        except Exception as e:          # the server drops connections now and then
            print("retry", a + 1, repr(e)[:120], flush=True)
            time.sleep(20 * (a + 1))
    raise RuntimeError("ERDDAP request failed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", default="kuroshio", choices=sorted(REGIONS))
    a = ap.parse_args()
    (la0, la1), (lo0, lo1) = REGIONS[a.region]
    raw = ROOT / "data" / "raw" / f"altimetry_{a.region}"
    raw.mkdir(parents=True, exist_ok=True)
    parts = []
    for t0, t1 in SPANS:
        f = raw / f"{t0[:4]}_{t0[5:7]}.nc"
        if not f.exists():
            sel = f"%5B({t0}T00:00:00Z):1:({t1}T00:00:00Z)%5D%5B({la0}):1:({la1})%5D%5B({lo0}):1:({lo1})%5D"   # brackets percent-encoded
            f.write_bytes(get(f"{URL}?u_current{sel},v_current{sel}"))
            print("got", f.name, f.stat().st_size // 1024, "KB", flush=True)
        ds = netCDF4.Dataset("mem", memory=f.read_bytes())     # netCDF-C cannot open paths with Chinese characters
        tv = ds["time"]
        dates = netCDF4.num2date(tv[:], tv.units, only_use_cftime_datetimes=False)
        parts.append(dict(dates=np.array([str(d)[:10] for d in dates]),
                          lat=np.asarray(ds["latitude"][:], np.float64), lon=np.asarray(ds["longitude"][:], np.float64),
                          u=np.ma.filled(ds["u_current"][:].astype(np.float32), np.nan),
                          v=np.ma.filled(ds["v_current"][:].astype(np.float32), np.nan)))
        ds.close()
    out = ROOT / "data" / "processed" / f"altimetry_{a.region}.npz"
    np.savez_compressed(out, dates=np.concatenate([p["dates"] for p in parts]), lat=parts[0]["lat"], lon=parts[0]["lon"],
                        u=np.concatenate([p["u"] for p in parts]), v=np.concatenate([p["v"] for p in parts]))
    n = sum(len(p["dates"]) for p in parts)
    print("done", out, n, "days", flush=True)


if __name__ == "__main__":
    main()
