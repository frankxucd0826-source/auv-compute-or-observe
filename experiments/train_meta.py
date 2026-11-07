"""Fit the learned controller on counterfactual missions.

For each non-default action a (think while going, drift, drift and think) a gradient-boosted
regression tree model predicts how much the mission's final regret changes if the next interval
is spent on a instead of going on with low-power planning. Missions are split into folds so no
mission contributes to both fitting and checking.

    python experiments/train_meta.py --data cf0 --out meta0
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
from oceanmeta.features import NAMES  # noqa: E402


def load(names):
    rows = []
    for n in names:
        rows += [json.loads(l) for l in open(ROOT / "results" / n / "data.jsonl", encoding="utf-8")]
    X = np.array([r["x"] for r in rows])
    R = np.array([r["regret"] for r in rows])
    g = np.array([r.get("date", r["mission"]) for r in rows])
    return X, R, g


def fit(X, y):
    return HistGradientBoostingRegressor(max_depth=4, learning_rate=0.05, max_iter=300,
                                         min_samples_leaf=40, l2_regularization=1.0).fit(X, y)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    X, R, g = load(a.data)
    A = R[:, 1:] - R[:, :1]          # advantage over going on (negative = better)
    print("examples", len(X), "missions", len(set(g)))
    print("mean advantage (think, drift, drift+think):", A.mean(0).round(4),
          "share better than going:", (A < -1e-9).mean(0).round(3))
    # cross-validated choice quality: regret of the chosen action vs always going / oracle
    oof = np.zeros_like(A)
    for tr, te in GroupKFold(5).split(X, groups=g):
        for k in range(3):
            oof[te, k] = fit(X[tr], A[tr, k]).predict(X[te])
    choice = np.where(oof.min(1) < 0, oof.argmin(1) + 1, 0)
    chosen = R[np.arange(len(R)), choice]
    print("cross-validated one-step regret: going %.4f, learned choice %.4f, best-in-hindsight %.4f"
          % (R[:, 0].mean(), chosen.mean(), R.min(1).mean()))
    print("learned choice shares:", np.bincount(choice, minlength=4) / len(choice))
    models = [fit(X, A[:, k]) for k in range(3)]
    out = ROOT / "results" / a.out
    out.mkdir(parents=True, exist_ok=True)
    pickle.dump(dict(models=models, names=NAMES), open(out / "models.pkl", "wb"))
    json.dump(dict(data=a.data, n=len(X), cv_going=float(R[:, 0].mean()), cv_learned=float(chosen.mean()),
                   cv_hindsight=float(R.min(1).mean())), open(out / "summary.json", "w"), indent=1)


if __name__ == "__main__":
    main()
