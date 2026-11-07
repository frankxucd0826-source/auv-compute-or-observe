#!/usr/bin/env bash
# Main comparison. Four vehicles (computer speed / computer power), map 3 days old.
#   dev split: the five fixed strategies, to find the best fixed strategy per vehicle
#              (an engineer tuning each vehicle on past missions)
#   test split (2023-2026): fixed strategies, classic one-step metareasoning, and rehearsal
#              in imagination (honest = imagined truths the planner never searched on;
#              self = imagined truths it did search on)
# Usage: bash experiments/main_eval.sh <tag> [workers]
cd "$(dirname "$0")/.." || exit 1
TAG=$1; W=${2:-4}
FIXED="fixed-0 fixed-1 periodic-100 periodic-300 periodic-200"
run() {  # split controllers name rate_low p_think
  N=400; [ "$1" = "dev" ] && N=120
  d="results/main_${TAG}_$1_$3"
  if [ -f "$d/results.jsonl" ] && [ -f "$d/done" ]; then return; fi
  rm -rf "$d"
  python -E -X utf8 experiments/run.py --exp "main_${TAG}_$1_$3" --split "$1" --n "$N" --lags 3 \
    --controllers $2 --platform-kw "{\"rate_low\": $4, \"rate_high\": $(( $4 * 50 )), \"p_think\": $5}" \
    --sat-err 0.15 --noise 0.1 --workers "$W" > /dev/null 2>&1 && touch "$d/done"
  echo "$1 $3 done"
}
for cond in "weak 5 20" "moderate 20 20" "strong 100 20" "efficient 20 5"; do
  set -- $cond
  run test "$FIXED rational rehearsal rehearsal-self" "$1" "$2" "$3"
  run dev "$FIXED" "$1" "$2" "$3"
done
