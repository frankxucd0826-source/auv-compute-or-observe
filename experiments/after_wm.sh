#!/usr/bin/env bash
# After the world model has finished training: repack the data (more months have arrived),
# cut the test-year mission windows, score the world model on held-out years, write
# world-model priors for every mission, then train the ablation without the JEPA loss.
cd "$(dirname "$0")/.." || exit 1
until [ -f results/wm_jepa_v0/model.pt ]; do sleep 20; done
sleep 5
py() { python -E -X utf8 "$@"; }
py scripts/preprocess.py chl | tail -1
py scripts/preprocess.py sst_on_chl | tail -1
py scripts/make_missions.py | tail -1
py scripts/prior_stats.py | tail -3
py experiments/eval_worldmodel.py wm_jepa_v0 --years 2022
py experiments/eval_worldmodel.py wm_jepa_v0 --years 2023 2024 2025 2026
py experiments/wm_priors.py --model wm_jepa_v0
echo "after_wm done"
