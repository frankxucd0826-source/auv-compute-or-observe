#!/usr/bin/env bash
# Second round of experiments (11-05): recognized survey baselines; the main comparison with the
# same-day satellite map itself as the true ocean (no added small-scale field); one-step
# metareasoning with held-out valuation on the remaining two vehicles; ablations of rehearsal
# (number of imagined truths, mis-scaled uncertainty); map age; the phase diagram with the
# satellite map as truth. Settings already complete are skipped.
# Usage: bash experiments/rev2.sh [workers]
cd "$(dirname "$0")/.." || exit 1
W=${1:-6}
FIXED="fixed-0 fixed-1 periodic-100 periodic-300 periodic-200"
RULES="lawnmower greedy ucb thompson"
run() {  # name split n controllers rate_low p_think sat_err lags [extra run.py args...]
  local name=$1 split=$2 n=$3 ctl=$4 rl=$5 pt=$6 se=$7 lags=$8; shift 8
  local d="results/$name"
  if [ -f "$d/done" ]; then return; fi
  rm -rf "$d"
  python -E -X utf8 experiments/run.py --exp "$name" --split "$split" --n "$n" --lags $lags \
    --controllers $ctl --platform-kw "{\"rate_low\": $rl, \"rate_high\": $(( rl * 50 )), \"p_think\": $pt}" \
    --sat-err "$se" --noise 0.1 --workers "$W" "$@" > "results/$name.log" 2>&1 && touch "$d/done"
  echo "$(date -u +%H:%M)Z $name done"
}
VEH=("weak 5 20" "moderate 20 20" "strong 100 20" "efficient 20 5")

# 1. survey rules (no route planning, so one run per truth model serves every vehicle)
run r2_rules_se0.15_test test 400 "$RULES" 20 20 0.15 3
run r2_rules_se0_test test 400 "$RULES" 20 20 0 3
# 2. main comparison with the same-day satellite map as the true ocean
for v in "${VEH[@]}"; do
  set -- $v
  run "r2_se0_dev_$1" dev 120 "$FIXED" "$2" "$3" 0 3
  run "r2_se0_test_$1" test 400 "$FIXED rational rehearsal" "$2" "$3" 0 3
done
# 3. one-step metareasoning valued on held-out oceans, fast computer and efficient accelerator
run r2_dbl_test_strong test 400 double 100 20 0.15 3
run r2_dbl_test_efficient test 400 double 20 5 0.15 3
# 4. rehearsal with 1, 2 and 8 imagined truths (4 in the main runs)
run r2_k_test_weak test 400 "rehearsal-k1 rehearsal-k2 rehearsal-k8" 5 20 0.15 3
run r2_k_test_moderate test 400 "rehearsal-k1 rehearsal-k2 rehearsal-k8" 20 20 0.15 3
# 5. map uncertainty not calibrated from the data: half and twice the calibrated spread
for s in 0.5 2; do
  run "r2_sd${s}_test_weak" test 400 "$FIXED rehearsal" 5 20 0.15 3 --sd-scale "$s"
  run "r2_sd${s}_test_moderate" test 400 "$FIXED rehearsal" 20 20 0.15 3 --sd-scale "$s"
done
# 6. a map one day old instead of three
for v in "weak 5 20" "moderate 20 20"; do
  set -- $v
  run "r2_lag1_dev_$1" dev 120 "$FIXED" "$2" "$3" 0.15 1
  run "r2_lag1_test_$1" test 400 "$FIXED rational rehearsal" "$2" "$3" 0.15 1
done
# 7. phase diagram column with the satellite map as truth (same 60 development missions)
for rl in 5 10 20 50 100 200; do
  run "phase_v3_rl${rl}_se0" dev 60 "$FIXED" "$rl" 20 0 3
done
echo "$(date -u +%H:%M)Z all done"
