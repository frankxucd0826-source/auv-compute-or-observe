"""Textures for the overview render, made from real data (normal Python, not Blender).

sea.png        the "real ocean" of one test mission: satellite chlorophyll of the day plus the
               simulated retrieval-error field, as the vehicle would meet it
stale.png      the 3-day-old satellite map the vehicle carries
imagined_k.png six imagined oceans drawn around the stale map with the calibrated uncertainty
The mission is the test window with the largest bloom contrast (rule stated, not hand-picked).
Writes ../renders/textures/*.png and ../renders/textures/meta.json
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import zoom

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from oceanmeta.belief import EnsembleBelief, gaussian_random_fields  # noqa: E402

OUT = ROOT / "paper" / "figures" / "renders" / "textures"
OUT.mkdir(parents=True, exist_ok=True)
# bloom colour ramp: clear blue-green water -> green -> brown-red tide
STOPS = [(-0.3, (47, 128, 166)), (0.3, (74, 160, 150)), (0.7, (110, 170, 96)), (1.0, (150, 150, 60)),
         (1.3, (160, 105, 45)), (1.6, (130, 60, 35))]


def colour(L):
    x = np.clip(L, STOPS[0][0], STOPS[-1][0])
    out = np.zeros(L.shape + (3,))
    for (a, ca), (b, cb) in zip(STOPS[:-1], STOPS[1:]):
        sel = (x >= a) & (x <= b)
        w = ((x - a) / (b - a))[sel][:, None]
        out[sel] = (1 - w) * np.array(ca) + w * np.array(cb)
    return out.astype(np.uint8)


def save(L, mask, name, px=1024):
    big = zoom(np.where(mask, L, np.nan_to_num(np.nanmedian(L))), px / L.shape[0], order=3)
    img = colour(big)[::-1]          # row 0 = north for an image
    Image.fromarray(img).save(OUT / name)


def main():
    M = np.load(ROOT / "data" / "missions" / "chl_missions.npz")
    rows = list(csv.DictReader(open(ROOT / "data" / "missions" / "chl_missions.csv", encoding="utf-8")))
    st = json.load(open(ROOT / "data" / "missions" / "prior_stats.json", encoding="utf-8"))
    test = [r for r in rows if r["split"] == "test"]
    pick = max(test, key=lambda r: float(r["tmax"]) - float(r["tmed"]))
    i = int(pick["id"])
    mask = M["mask"][i]
    truth = M["truth"][i] + 0.15 * gaussian_random_fields(1, 40, 40, 3.0, np.random.default_rng(7919 * i + 1))[0]
    prior = M["prior"][i, list(M["lags"]).index(3)]
    sd = float(np.hypot(st["sd"]["3"], 0.15))
    save(truth, mask, "sea.png")
    save(prior, mask, "stale.png")
    save(M["truth"][i], mask, "sat_day.png", px=512)     # the satellite map of the mission day itself
    B = EnsembleBelief.from_prior(prior, sd, st["length_cells"]["3"], 48, mask, np.random.default_rng(3))
    for k in range(6):
        save(B.X[k], mask, f"imagined_{k}.png", px=512)
    ty, tx = np.unravel_index(np.argmax(np.where(mask, truth, -9)), truth.shape)
    meta = dict(mission=i, date=pick["date"], lat0=float(pick["lat0"]), lon0=float(pick["lon0"]),
                start=[float(pick["start_x"]), float(pick["start_y"])], core=[int(tx), int(ty)],
                truth_max=float(truth[mask].max()))
    json.dump(meta, open(OUT / "meta.json", "w"), indent=1)
    print(meta)


if __name__ == "__main__":
    main()
