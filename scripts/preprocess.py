"""Pack monthly ERDDAP files into one float16 array per variable (latitude ascending).

    python scripts/preprocess.py chl    -> data/processed/chl.npy  (log10 mg m^-3)
    python scripts/preprocess.py sst    -> data/processed/sst.npy  (deg C)
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from oceanmeta.data import open_nc  # noqa: E402

VARS = {"chl": "chlor_a", "sst": "analysed_sst"}


def main(name):
    files = sorted((ROOT / "data" / "raw" / name).glob(f"{name}_*.nc"))
    out_dir = ROOT / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open_nc(files[0]) as d:
        lat = np.array(d["latitude"][:], dtype=np.float64)
        lon = np.array(d["longitude"][:], dtype=np.float64)
    flip = lat[0] > lat[-1]
    if flip:
        lat = lat[::-1]
    days, chunks = [], []
    for f in files:
        with open_nc(f) as d:
            t = np.array(d["time"][:], dtype=np.float64)
            v = np.ma.filled(d[VARS[name]][:].astype(np.float32), np.nan)
        v = v.reshape(v.shape[0], v.shape[-2], v.shape[-1])
        if flip:
            v = v[:, ::-1, :]
        if name == "chl":
            v = np.log10(np.clip(v, 0.01, 100.0))
        if name == "sst" and np.nanmean(v) > 200:
            v = v - 273.15
        days.append((t // 86400).astype("int64"))
        chunks.append(v.astype(np.float16))
        print(f.name, v.shape, flush=True)
    F = np.concatenate(chunks)
    dates = np.concatenate(days).astype("datetime64[D]")
    order = np.argsort(dates)
    F, dates = F[order], dates[order]
    keep = np.r_[True, dates[1:] != dates[:-1]]
    F, dates = F[keep], dates[keep]
    np.save(out_dir / f"{name}.npy", F)
    np.save(out_dir / f"{name}_dates.npy", dates)
    np.save(out_dir / f"{name}_lat.npy", lat)
    np.save(out_dir / f"{name}_lon.npy", lon)
    print("saved", name, F.shape, dates[0], dates[-1])


def sst_on_chl():
    """SST interpolated onto the chlorophyll grid and dates (NaN where a date is missing),
    and the ocean mask of the chlorophyll grid (pixels with data on at least one of 60 days)."""
    from scipy.interpolate import RegularGridInterpolator
    P = ROOT / "data" / "processed"
    chl = np.load(P / "chl.npy", mmap_mode="r")
    cd = np.load(P / "chl_dates.npy").astype("datetime64[D]")
    clat, clon = np.load(P / "chl_lat.npy"), np.load(P / "chl_lon.npy")
    sst = np.load(P / "sst.npy", mmap_mode="r")
    sd = np.load(P / "sst_dates.npy").astype("datetime64[D]")
    slat, slon = np.load(P / "sst_lat.npy"), np.load(P / "sst_lon.npy")
    si = {d: i for i, d in enumerate(sd)}
    YY, XX = np.meshgrid(clat, clon, indexing="ij")
    pts = np.stack([YY.ravel(), XX.ravel()], -1)
    out = np.lib.format.open_memmap(P / "sst_on_chl.npy", mode="w+", dtype=np.float16, shape=chl.shape)
    for k, d in enumerate(cd):
        if d in si:
            f = RegularGridInterpolator((slat, slon), np.asarray(sst[si[d]], dtype=np.float32),
                                        bounds_error=False, fill_value=np.nan)
            out[k] = f(pts).reshape(chl.shape[1:]).astype(np.float16)
        else:
            out[k] = np.nan
    out.flush()
    idx = np.linspace(0, len(cd) - 1, 60).astype(int)
    ocean = np.zeros(chl.shape[1:], bool)
    for i in idx:
        ocean |= np.isfinite(np.asarray(chl[i], dtype=np.float32))
    np.save(P / "ocean_mask.npy", ocean)
    print("sst_on_chl", out.shape, "ocean fraction", ocean.mean())


if __name__ == "__main__":
    if sys.argv[1] == "sst_on_chl":
        sst_on_chl()
    else:
        main(sys.argv[1])
