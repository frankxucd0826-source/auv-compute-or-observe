"""Does rehearsal in imagination predict reality? For every test mission, compare the regret
each strategy got in the vehicle's imagined missions (honest: truths it never searched on;
self-assessed: truths it searched on) with the regret the same strategy really got (the fixed
strategy runs use the same mission and seed).

    python experiments/imagination_check.py v3 moderate strong efficient
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MAP = {"go": "fixed-0", "think": "fixed-1", "think 1 in 3": "periodic-100",
       "stop and think 1 in 3": "periodic-300", "stop and resample 1 in 3": "periodic-200"}


def main():
    tag, conds = sys.argv[1], sys.argv[2:]
    rows = []
    for c in conds:
        f = ROOT / "results" / f"main_{tag}_test_{c}" / "results.jsonl"
        df = pd.DataFrame([json.loads(l) for l in open(f, encoding="utf-8")])
        real = df[df.controller.isin(MAP.values())].pivot_table(index="mission", columns="controller", values="regret_avg")
        for kind in ("rehearsal", "rehearsal-self"):
            sub = df[(df.controller == kind) & df["imagined"].notna()] if "imagined" in df else df.iloc[:0]
            for _, r in sub.iterrows():
                if r.mission not in real.index:
                    continue
                for s, spec in MAP.items():
                    rows.append(dict(cond=c, kind=kind, mission=r.mission, strategy=s,
                                     imagined=r.imagined[s], real=real.loc[r.mission, spec], chosen=(r.choice == s)))
    T = pd.DataFrame(rows)
    if T.empty:
        print("no rehearsal scores recorded yet")
        return
    T["bias"] = T.imagined - T.real
    pd.set_option("display.width", 200)
    print("mean imagined minus real regret, by strategy:")
    print(T.pivot_table(index=["cond", "kind"], columns="strategy", values="bias").round(3).to_string())
    # the imagined and the real advantage of thinking over going
    out = []
    for (c, k), g in T.groupby(["cond", "kind"]):
        p = g.pivot_table(index="mission", columns="strategy", values=["imagined", "real"])
        adv_i = (p["imagined"]["think"] - p["imagined"]["go"]).mean()
        adv_r = (p["real"]["think"] - p["real"]["go"]).mean()
        best_real = p["real"].min(axis=1)
        chosen = g[g.chosen].set_index("mission")["real"]
        out.append(dict(cond=c, kind=k, n=len(p), think_minus_go_imagined=adv_i, think_minus_go_real=adv_r,
                        regret_of_choice=(chosen - best_real.reindex(chosen.index)).mean(),
                        choice_share=g[g.chosen].strategy.value_counts(normalize=True).round(2).to_dict()))
    print(pd.DataFrame(out).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
