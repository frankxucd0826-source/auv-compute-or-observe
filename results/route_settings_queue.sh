#!/bin/bash
# Scope and ablation runs, started only after the main test run has finished (4 worker processes at a time).
cd "/d/海洋大数据"
until [ -f results/route_main_test/done ]; do sleep 20; done
for split in dev test; do python -E -X utf8 experiments/route_eval.py --split $split --workers 4 --tag fresh05 --deg 0.5 --lag 0 --sigma 0.15 --limit 350 2>&1 | grep -v Warning | tail -1; done
for split in dev test; do python -E -X utf8 experiments/route_eval.py --split $split --workers 4 --tag slow --deg 1.0 --lag 1 --sigma 0.15 --V 0.75 --limit 350 2>&1 | grep -v Warning | tail -1; done
for split in dev test; do python -E -X utf8 experiments/route_eval.py --split $split --workers 4 --tag analog --deg 1.0 --lag 1 --sigma 0.15 --basis analog --limit 350 2>&1 | grep -v Warning | tail -1; done
echo all-settings-done
