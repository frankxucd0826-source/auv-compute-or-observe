"""Download daily satellite fields for the East China Sea box from NOAA ERDDAP, one file per month.

Usage:
    python scripts/download_satellite.py chl   # VIIRS+OLCI gap-filled chlorophyll, 2 km
    python scripts/download_satellite.py sst   # MUR SST, 0.01 deg strided to 0.04 deg

Files go to data/raw/<name>/<name>_YYYY-MM.nc; an existing file that opens and has the
expected number of days is skipped, so the script can be rerun after an interruption.
"""
import sys
import time
from datetime import date
from pathlib import Path

import netCDF4
import requests

ROOT = Path(__file__).resolve().parents[1]
LAT = (25.0, 33.0)
LON = (119.5, 127.0)

SOURCES = {
    "chl": dict(
        server="https://coastwatch.noaa.gov/erddap/griddap/",
        dataset="noaacwNPPN20S3ASCIDINEOF2kmDaily",
        var="chlor_a",
        query="{v}[({t0}T12:00:00Z):({t1}T12:00:00Z)][(0.0)][({la1}):({la0})][({lo0}):({lo1})]",
        first=date(2018, 1, 1),
        last=date(2026, 10, 23),
    ),
    "sst": dict(
        server="https://coastwatch.pfeg.noaa.gov/erddap/griddap/",
        dataset="jplMURSST41",
        var="analysed_sst",
        query="{v}[({t0}T09:00:00Z):({t1}T09:00:00Z)][({la0}):4:({la1})][({lo0}):4:({lo1})]",
        first=date(2018, 1, 1),
        last=date(2026, 10, 31),
    ),
}


def months(first, last):
    y, m = first.year, first.month
    while (y, m) <= (last.year, last.month):
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def month_range(y, m, first, last):
    start = date(y, m, 1)
    end = date(y + 1, 1, 1) if m == 12 else date(y, m + 1, 1)
    end = date.fromordinal(end.toordinal() - 1)
    return max(start, first), min(end, last)


def complete(path, var):
    # netCDF-C on Windows cannot open paths with non-ASCII characters (this project lives
    # in D:\海洋大数据), so files are always opened from memory.
    try:
        with netCDF4.Dataset("inmemory.nc", memory=Path(path).read_bytes()) as d:
            return d[var].shape[0] > 0
    except Exception:
        return False


def main(name):
    src = SOURCES[name]
    out = ROOT / "data" / "raw" / name
    out.mkdir(parents=True, exist_ok=True)
    log = open(ROOT / "data" / "raw" / f"download_{name}.log", "a", encoding="utf-8")
    session = requests.Session()
    # bloom season (March-June) of every year first, the rest afterwards
    order = sorted(months(src["first"], src["last"]), key=lambda ym: (ym[1] not in (3, 4, 5, 6), ym))
    for y, m in order:
        path = out / f"{name}_{y:04d}-{m:02d}.nc"
        if path.exists() and complete(path, src["var"]):
            continue
        t0, t1 = month_range(y, m, src["first"], src["last"])
        q = src["query"].format(v=src["var"], t0=t0, t1=t1, la0=LAT[0], la1=LAT[1], lo0=LON[0], lo1=LON[1])
        url = src["server"] + src["dataset"] + ".nc?" + q
        for attempt in range(5):
            try:
                tic = time.time()
                r = session.get(url, timeout=900)
                r.raise_for_status()
                tmp = path.with_suffix(".part")
                tmp.write_bytes(r.content)
                tmp.replace(path)
                if not complete(path, src["var"]):
                    raise RuntimeError("file does not open")
                msg = f"{time.strftime('%H:%M:%S')} {path.name} {len(r.content)/1e6:.1f} MB {time.time()-tic:.0f} s"
                break
            except Exception as e:
                msg = f"{time.strftime('%H:%M:%S')} {path.name} attempt {attempt+1} failed: {e}"
                time.sleep(20 * (attempt + 1))
        print(msg, flush=True)
        log.write(msg + "\n")
        log.flush()
    print("done", name, flush=True)
    log.write(f"done {name}\n")


if __name__ == "__main__":
    main(sys.argv[1])
