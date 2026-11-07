"""One-change diagnostic inside one-step metareasoning (results/r2_diag_test_*): for the slow and
moderate computers, the classic controller, each single change (held-out valuation only; the
two-standard-error rule only) and both changes, with regret, the share of intervals with the
high-performance computer on and the share spent stopped, and paired differences (95% intervals from
a bootstrap over bloom weeks).
    python -E -X utf8 experiments/rev2_diag_summary.py   -> results/rev2_diag_summary.json
"""
import json

import numpy as np
import pandas as pd
from rev2_summary import ROOT, load, paired, shares, cat

OUT = {}
rng = np.random.default_rng(3)
for v in ("weak", "moderate"):
    te = cat(load(f"main_v3_test_{v}"), load(f"main_v3_test_{v}_double"), load(f"r2_diag_test_{v}"))
    if te is None or "double-noguard" not in set(te.controller):
        continue
    piv = te.pivot_table(index="mission", columns="controller", values="regret_avg")
    keys = ["rational", "double-noguard", "rational-guard", "double", "rehearsal"]
    R = {k: dict(mean=float(piv[k].mean()), **(shares(te, k) or {})) for k in keys if k in piv}
    for k in ("double-noguard", "rational-guard", "double"):
        R[k]["minus_rational"] = paired(piv, k, "rational", rng)
        R[k]["minus_rehearsal"] = paired(piv, k, "rehearsal", rng)
    OUT[v] = R
    print(f"=== {v}")
    for k, r in R.items():
        extra = ""
        if "minus_rational" in r:
            a, b = r["minus_rational"], r["minus_rehearsal"]
            extra = f" | minus classic {a['mean']:+.3f} [{a['lo']:+.3f}, {a['hi']:+.3f}] | minus rehearsal {b['mean']:+.3f} [{b['lo']:+.3f}, {b['hi']:+.3f}]"
        print(f"  {k:15s} regret {r['mean']:.3f} think {r.get('think', float('nan')):.2f} stopped {r.get('stopped', float('nan')):.2f}{extra}")
json.dump(OUT, open(ROOT / "results" / "rev2_diag_summary.json", "w", encoding="utf-8"), indent=1)
