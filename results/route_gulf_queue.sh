#!/bin/bash
# Replication in the Gulf Stream: the main procedure unchanged, region chosen by OCEANROUTE_REGION
# (radius and thresholds are calibrated on the Gulf Stream's own development years by route_summary.py).
cd "/d/海洋大数据"
export OCEANROUTE_REGION=gulfstream
until grep -q "^done" data/download_gulfstream.log; do sleep 20; done
for split in dev test; do python -E -X utf8 experiments/route_eval.py --split $split --workers 4 --tag gulf --deg 1.0 --lag 1 --sigma 0.15 2>&1 | grep -v Warning | tail -3; done
python -E -X utf8 experiments/route_summary.py gulf
echo gulf-done
