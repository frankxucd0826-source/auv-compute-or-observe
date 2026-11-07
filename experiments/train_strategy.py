"""Fit the strategy selector on strategy-level counterfactual missions.

One gradient-boosted regression tree model per strategy predicts how much worse (or better)
the final regret would be than going on with low-power planning, from the vehicle's features
at the decision point. The selector follows the strategy with the lowest prediction, if that
prediction beats going by a margin. Cross-validation splits by mission date.

    python experiments/train_strategy.py --data cfs1 --out sel1
"""
import argparse
import json
import pickle
import sys
from pathlib import Path

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))
from oceanmeta.features import NAMES  # noqa: E402
from counterfactual_strategy import STRATEGIES, STRATEGY_NAMES  # noqa: E402


def load(names):
    rows = []
    for n in names:
        rows += [json.loads(l) for l in open(ROOT / "results" / n / "data.jsonl", encoding="utf-8")]
    X = np.array([r["x"] for r in rows])
    R = np.array([r["regret"] for r in rows])
    g = np.array([r["date"] for r in rows])
    return X, R, g, rows


def fit(X, y):
    return HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=250,
                                         min_samples_leaf=30, l2_regularization=1.0).fit(X, y)


def choose(pred, margin):
    k = pred.argmin(1)
    return np.where(pred[np.arange(len(pred)), k] < -margin, k + 1, 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    X, R, g, rows = load(a.data)
    A = R[:, 1:] - R[:, :1]
    S = len(STRATEGIES)
    print("examples", len(X), "dates", len(set(g)))
    print("mean regret per strategy:", dict(zip(STRATEGY_NAMES, R.mean(0).round(4))))
    print("best-in-hindsight share:", np.bincount(R.argmin(1), minlength=S) / len(R))
    oof = np.zeros_like(A)
    for tr, te in GroupKFold(5).split(X, groups=g):
        for k in range(S - 1):
            oof[te, k] = fit(X[tr], A[tr, k]).predict(X[te])
    res = {}
    for margin in (0.0, 0.005, 0.01, 0.02):
        c = choose(oof, margin)
        res[margin] = R[np.arange(len(R)), c].mean()
        print(f"margin {margin}: cross-validated regret {res[margin]:.4f}  shares {np.bincount(c, minlength=S) / len(c)}")
    # best single fixed strategy for comparison, and per-condition best (an engineer's tuning)
    print("always go %.4f | best single strategy %.4f | hindsight %.4f"
          % (R[:, 0].mean(), R.mean(0).min(), R.min(1).mean()))
    margin = min(res, key=res.get)
    models = [fit(X, A[:, k]) for k in range(S - 1)]
    out = ROOT / "results" / a.out
    out.mkdir(parents=True, exist_ok=True)
    imp = {}
    pickle.dump(dict(models=models, names=NAMES, strategies=STRATEGIES, margin=margin), open(out / "models.pkl", "wb"))
    json.dump(dict(data=a.data, n=len(X), margin=margin, cv=res, always_go=float(R[:, 0].mean()),
                   hindsight=float(R.min(1).mean())), open(out / "summary.json", "w"), indent=1)
    print("saved, margin", margin)


if __name__ == "__main__":
    main()
