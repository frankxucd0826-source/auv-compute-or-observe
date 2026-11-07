#!/usr/bin/env bash
# One change at a time inside one-step metareasoning (11-05). The held-out variant ("double")
# differs from the classic one ("rational") in two places: the value of thinking and of looking is
# judged on held-out oceans, and the vehicle leaves "go" only for a gain above two standard errors.
# Here each change is made alone, on the same test missions and seeds as results/main_v3_test_*:
#   double-noguard   held-out valuation, plain maximum
#   rational-guard   searched valuation, two-standard-error rule
# Waits for experiments/rev2.sh to finish. Usage: bash experiments/rev2_diag.sh [workers]
cd "$(dirname "$0")/.." || exit 1
W=${1:-6}
while [ ! -f results/phase_v3_rl200_se0/done ]; do sleep 30; done
for v in "weak 5" "moderate 20"; do
  set -- $v
  d="results/r2_diag_test_$1"
  if [ -f "$d/done" ]; then continue; fi
  rm -rf "$d"
  python -E -X utf8 experiments/run.py --exp "r2_diag_test_$1" --split test --n 400 --lags 3 \
    --controllers double-noguard rational-guard --platform-kw "{\"rate_low\": $2, \"rate_high\": $(( $2 * 50 )), \"p_think\": 20}" \
    --sat-err 0.15 --noise 0.1 --workers "$W" > "results/r2_diag_test_$1.log" 2>&1 && touch "$d/done"
  echo "$(date -u +%H:%M)Z r2_diag_test_$1 done"
done
