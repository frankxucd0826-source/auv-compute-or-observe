#!/bin/bash
# Independent test in the Agulhas retroflection (plan written in NOTEBOOK.md before the data were downloaded):
# the main procedure unchanged, region chosen by OCEANROUTE_REGION; radius and thresholds calibrated on the
# region's own development years by route_summary.py.
cd "/d/海洋大数据"
export OCEANROUTE_REGION=agulhas
until grep -q "^done" data/download_agulhas.log; do sleep 20; done
for split in dev test; do python -E -X utf8 experiments/route_eval.py --split $split --workers 4 --tag agulhas --deg 1.0 --lag 1 --sigma 0.15 2>&1 | grep -v Warning | tail -3; done
python -E -X utf8 experiments/route_summary.py agulhas
echo agulhas-done
