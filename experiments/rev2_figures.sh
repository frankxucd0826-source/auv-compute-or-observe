#!/usr/bin/env bash
# Regenerate everything the paper shows from the results (second round): summary, Table 2, figures.
cd "$(dirname "$0")/.." || exit 1
python -E -X utf8 experiments/rev2_summary.py > results/rev2_summary.log 2>&1 || { tail -20 results/rev2_summary.log; exit 1; }
python -E -X utf8 experiments/rev2_tables.py
cd paper/figures || exit 1
for f in fig_data fig_curse fig_main fig_mech fig_example fig_ablation; do
  python -E -X utf8 "$f.py" 2>&1 | grep -v -i warn | tail -1
done
python -E -X utf8 fig_phase.py v3 2>&1 | grep -v -i warn | head -1
python -E -X utf8 compose/fig_overview.py 2>&1 | grep -v -i warn | grep -v get_cmap | tail -1
