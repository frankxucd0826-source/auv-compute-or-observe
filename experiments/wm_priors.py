"""Turn the world model's forecasts into the vehicle's prior for every mission window.

For a mission on day d with maps k days old, the model reads the three latest available days
(d-k-2, d-k-1, d-k) on a 64 x 64 pixel patch around the window and forecasts day d (lead k).
Forecast mean and standard deviation are interpolated onto the 40 x 40 mission grid.

    python experiments/wm_priors.py --model wm_jepa
    -> data/missions/chl_missions_<model>.npz with mean (M, lags, 40, 40), sd (M, lags, 40, 40)
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))
from oceanmeta.data import window  # noqa: E402
from oceanmeta.worldmodel import WorldModel, HIST  # noqa: E402
from train_worldmodel import Cube, CHL_MU, CHL_SD  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    a = ap.parse_args()
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    model = WorldModel().to(dev)
    model.load_state_dict(torch.load(ROOT / "results" / a.model / "model.pt", map_location=dev))
    model.eval()
    cube = Cube()
    lat = np.load(ROOT / "data" / "processed" / "chl_lat.npy")
    lon = np.load(ROOT / "data" / "processed" / "chl_lon.npy")
    M = np.load(ROOT / "data" / "missions" / "chl_missions.npz")
    lags = list(M["lags"])
    rows = list(csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
    n = len(rows)
    mean = np.full((n, len(lags), 40, 40), np.nan, np.float32)
    sd = np.full_like(mean, np.nan)
    P = 64
    for r in rows:
        i = int(r["id"])
        d = np.datetime64(r["date"])
        lat0, lon0 = float(r["lat0"]), float(r["lon0"])
        iy = int(np.argmin(np.abs(lat - lat0)))
        ix = int(np.argmin(np.abs(lon - lon0)))
        y0 = int(np.clip(iy - P // 2, 0, len(lat) - P))
        x0 = int(np.clip(ix - P // 2, 0, len(lon) - P))
        for j, k in enumerate(lags):
            days = [d - np.timedelta64(k + h, "D") for h in range(HIST - 1, -1, -1)]
            if any(x not in cube.idx for x in days):
                continue
            fr = np.stack([cube.frame(cube.idx[x], y0, x0, P) for x in days])[None]
            with torch.no_grad():
                _, mu, log_sd = model(torch.from_numpy(fr).to(dev), torch.tensor([k], device=dev))
            mu = mu[0].cpu().numpy() * CHL_SD + CHL_MU
            s = np.exp(log_sd[0].cpu().numpy()) * CHL_SD
            plat, plon = lat[y0:y0 + P], lon[x0:x0 + P]
            mean[i, j] = window(mu, plat, plon, lat0, lon0, 40, 2.0)
            sd[i, j] = window(s, plat, plon, lat0, lon0, 40, 2.0)
    # where the patch does not cover the window (rare), fall back to the stale map
    bad = ~np.isfinite(mean)
    mean[bad] = M["prior"][bad]
    sd[bad] = np.nanmedian(sd)
    np.savez_compressed(ROOT / "data" / "missions" / f"chl_missions_{a.model}.npz", mean=mean, sd=sd, lags=np.array(lags))
    print("saved", n, "missions; fallback cells", int(bad.sum()))


if __name__ == "__main__":
    main()
