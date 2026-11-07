#!/bin/bash
# The vehicle carries a real satellite current map (plan written in NOTEBOOK.md before the data were
# downloaded): Kuroshio region, HYCOM truth, map = NOAA near-real-time altimetry geostrophic currents from
# 3 days before (OCEANROUTE_MAP=altimetry); everything else as in the main runs; radius and thresholds are
# calibrated on the development years by route_summary.py.
cd "/d/海洋大数据"
export OCEANROUTE_MAP=altimetry
until grep -q "^done" data/download_altimetry.log; do sleep 20; done
for split in dev test; do python -E -X utf8 experiments/route_eval.py --split $split --workers 4 --tag altimetry --deg 1.0 --lag 1 --sigma 0.15 2>&1 | grep -v Warning | tail -3; done
python -E -X utf8 experiments/route_summary.py altimetry
echo altimetry-done
