"""Does the expected-time rule lose to the worst-regret rule only because 32 plausible fields are too few?

Re-creates the missions of experiments/route_eval.py (same seed, same sampling) and, for each one,
computes the margin dJ = J_L - J_R with the standard solver (4 km, 16 directions) on M plausible
fields drawn from the same calibrated error model, with a random stream independent of the main run.
experiments/route_ensemble_analysis.py then scores the expected-time rule with the first n of these
fields, n = 8 ... M, next to the worst-regret rule of the main run.

    python -E -X utf8 experiments/route_ensemble_size.py --split test --M 1024 --workers 4
        -> results/route_ens1024_test/results.jsonl.gz
"""
import argparse
import json
import os
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))
_S = None
SPLIT_YEARS = {"dev": (2019, 2021), "test": (2022, 2024)}


def _init():
    for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[k] = "1"
    global _S
    from oceanroute.fields import Snapshots
    _S = Snapshots()


def _job(job):
    from oceanroute.mission import Level, margin
    from oceanroute import errormodel as EM
    spec, cfg, pool = job
    S = _S
    tic = time.time()
    L1 = Level(S, spec, 1, cfg["deg"], None, cfg["lag"])
    M = EM.load_or_fit(S, cfg["deg"], cfg["lag"], pool)
    L1.Phi = EM.modes(S, M, L1.X, L1.Y, L1.grid.water, spec.box)
    rng = np.random.default_rng([cfg["stream"], int(spec.k), int(spec.s[0] * 1000), int(spec.s[1] * 1000)])
    Z = rng.standard_normal((cfg["M"], L1.Phi.shape[0]))
    d_map = float(margin(L1, L1.map, cfg["V"], L1.start)[0])
    ens = [float(margin(L1, L1.field(z), cfg["V"], L1.start)[0]) for z in Z]
    return dict(k=int(spec.k), s=list(spec.s), dJ_map_L1=d_map, ens=ens, wall_s=round(time.time() - tic, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="test")
    ap.add_argument("--M", type=int, default=256)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--stream", type=int, default=20261106, help="seed of the plausible fields, independent of the main run")
    a = ap.parse_args()
    main_cfg = json.load(open(ROOT / "results" / f"route_main_{a.split}" / "config.json", encoding="utf-8"))
    cfg = dict(V=main_cfg["V"], deg=main_cfg["deg"], lag=main_cfg["lag"], M=a.M, stream=a.stream)
    _init()
    S = _S
    from oceanroute.mission import sample_specs
    from route_eval import years
    yr = years(S)
    dev = [int(j) for j in np.where((yr >= 2019) & (yr <= 2021))[0]]
    lo, hi = SPLIT_YEARS[a.split]
    snaps = [int(j) for j in np.where((yr >= lo) & (yr <= hi))[0] if j - cfg["lag"] >= 0]
    rng = np.random.default_rng(main_cfg["seed"] + (0 if a.split == "dev" else 1000))   # as route_eval.py
    specs = []
    for k in snaps:
        specs += sample_specs(S, k, np.random.default_rng(rng.integers(1 << 31)), main_cfg["per_snap"],
                              min_speed=main_cfg["min_speed"], deg=cfg["deg"], lag=cfg["lag"])
    assert len(specs) == main_cfg["n_specs"], (len(specs), main_cfg["n_specs"])
    if a.limit:
        specs = specs[:a.limit]
    out = ROOT / "results" / f"route_ens{a.M}_{a.split}"
    out.mkdir(parents=True, exist_ok=True)
    json.dump(dict(vars(a), cfg=cfg, n_specs=len(specs), started=time.strftime("%Y-%m-%d %H:%M:%S")),
              open(out / "config.json", "w", encoding="utf-8"), indent=1)
    print(len(specs), "missions", flush=True)
    jobs = [(sp, cfg, dev) for sp in specs]
    tic = time.time()
    with Pool(a.workers, initializer=_init) as pool, open(out / "results.jsonl", "w", encoding="utf-8") as fh:
        for i, rec in enumerate(pool.imap_unordered(_job, jobs, chunksize=1)):
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            if (i + 1) % 20 == 0:
                print(f"{i + 1}/{len(jobs)} {time.time() - tic:.0f}s", flush=True)
    if not a.limit:
        import gzip
        import shutil
        with open(out / "results.jsonl", "rb") as src, gzip.open(out / "results.jsonl.gz", "wb") as dst:
            shutil.copyfileobj(src, dst)            # stored compressed (about 13 MB as text per split)
        (out / "results.jsonl").unlink()
        (out / "done").write_text("ok")
    print("done", f"{time.time() - tic:.0f}s", flush=True)


if __name__ == "__main__":
    main()
