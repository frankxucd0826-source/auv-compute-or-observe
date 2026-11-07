#!/usr/bin/env bash
# Which fixed way of spending time wins, as the low-power computer gets faster and the
# satellite map gets less accurate. Five strategies on the same development missions:
#   go (fixed-0), think while going (fixed-1), think one interval in three (periodic-100),
#   stop and think one interval in three (periodic-300), stop and resample one in three (periodic-200)
# Settings already complete are skipped; incomplete ones are rerun from scratch.
# Usage: bash experiments/phase.sh <tag> [n_missions] [workers]
cd "$(dirname "$0")/.." || exit 1
TAG=$1; N=${2:-60}; W=${3:-4}
# Before the sweep: rerun rehearsal on the slow-computer test missions, now recording which
# strategy it picked (the first run predates that record; seeds are per mission, so the
# regrets must come out the same as in results/main_${TAG}_test_weak).
d="results/main_${TAG}_test_weak_choice"
if [ ! -f "$d/done" ]; then
  rm -rf "$d"
  python -E -X utf8 experiments/run.py --exp "main_${TAG}_test_weak_choice" --split test --n 400 --lags 3     --controllers rehearsal rehearsal-self --platform-kw '{"rate_low": 5, "rate_high": 250, "p_think": 20}'     --sat-err 0.15 --noise 0.1 --workers "$W" > /dev/null 2>&1 && touch "$d/done"
  echo "weak rehearsal rerun done"
fi
# Ablation before the sweep: one-step metareasoning that judges more planning (and more looking)
# on the held-out imagined oceans instead of the searched ones ("double"), slow and moderate
# computers, same test missions and seeds as results/main_${TAG}_test_*.
for cond in "weak 5" "moderate 20"; do
  set -- $cond
  d="results/main_${TAG}_test_$1_double"
  if [ -f "$d/done" ]; then continue; fi
  rm -rf "$d"
  python -E -X utf8 experiments/run.py --exp "main_${TAG}_test_$1_double" --split test --n 400 --lags 3     --controllers double --platform-kw "{\"rate_low\": $2, \"rate_high\": $(( $2 * 50 )), \"p_think\": 20}"     --sat-err 0.15 --noise 0.1 --workers "$W" > /dev/null 2>&1 && touch "$d/done"
  echo "$1 double done"
done
for rl in 5 10 20 50 100 200; do
  for se in 0.05 0.15 0.3; do
    d="results/phase_${TAG}_rl${rl}_se${se}"
    if [ -f "$d/done" ]; then continue; fi
    rm -rf "$d"
    python -E -X utf8 experiments/run.py --exp "phase_${TAG}_rl${rl}_se${se}" --split dev --n "$N" --lags 3 \
      --controllers fixed-0 fixed-1 periodic-100 periodic-300 periodic-200 \
      --platform-kw "{\"rate_low\": $rl, \"rate_high\": $(( rl * 50 )), \"p_think\": 20}" \
      --sat-err "$se" --noise 0.1 --workers "$W" > /dev/null 2>&1 && touch "$d/done"
    echo "rl${rl} se${se} done"
  done
done
