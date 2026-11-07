# Facts sheet for the writer

Everything here must hold in the paper. Structure, wording, terminology and emphasis are the
writer's choice. All runs have finished; no TBD remains except the repository address. Numbers are log10
chlorophyll unless stated.

## Setting
- Course: Ocean Big Data, Zhejiang University, autumn 2026 (instructor Zhang Fan). Paper in
  Chinese, ZJU course paper format, about 12-16 pages.
- Scenario: harmful algal bloom (HAB) emergency survey off Zhejiang, East China Sea.
  Prorocentrum donghaiense blooms occur every late spring and early summer in the East China Sea
  (zhao2025distinguishing: in 2021 and 2023 between late April and early June off Taizhou,
  Wenzhou and Ningbo); Lou & Hu 2014 (lou2014diurnal) tracked one such bloom in May 2011 with
  hourly GOCI images and saw the patches drift with the tides. Do not quote a chlorophyll
  threshold for bloom water from the literature (the source could not be re-checked); the
  mission windows use our own criterion of 5 mg m^-3.
- Vehicle: REMUS 100 class AUV, 1.5 m/s, 1 kWh, about 22 h at 3 kn, so about 45 W in cruise
  (15 W hotel, 30 W propulsion); an embedded GPU module (Jetson Orin NX class, 10-25 W, 20 W
  used) for deep planning; a low-power processor always replans in the background.
- Each 20-minute interval: body = follow the plan and sample on the way, or switch the motor
  off and drift with the water, resampling it; brain = keep replanning on the low-power
  computer, or plan deeply on the GPU at extra energy. Computing and moving run at the same
  time; the new plan is computed for where the vehicle will be when it takes over (latency
  compensation) and replaces the old one at the end of the interval. Mission ends at 24 h or
  when the battery runs out.
- Everything is described in the frame that drifts with the surface water: the bloom does not
  move relative to the water, so the vehicle does not "chase" it against the current; currents
  matter through the age of the satellite map, which the data contain.
- Score: the operations centre can ask at any moment where the densest water is; the vehicle
  answers with the visited place of highest estimated chlorophyll. Regret = log10 chlorophyll
  of the true densest water minus that of the answer; averaged over a 24 h window (answer
  frozen after the mission ends). Also reported: the regret at the end, and whether the end
  answer is within 0.1 (26%) of the maximum.

## Data (ocean big data)
- Chlorophyll-a: NOAA CoastWatch, merged VIIRS (S-NPP, NOAA-20) and Sentinel-3A OLCI,
  gap-filled with DINEOF, 2 km, daily, 2018-01-01 to 2026-10-23 (3197 days), CC0
  (ERDDAP noaacwNPPN20S3ASCIDINEOF2kmDaily). Box 25-33 N, 119.5-127 E, 385 x 361 pixels/day.
- SST: JPL MUR v4.1 (produced by NASA JPL), 0.01 deg, daily, gap-free, subsampled to 0.04 deg;
  both datasets downloaded from NOAA CoastWatch ERDDAP servers (jplMURSST41).
- Mission windows: April-June days; strongest smoothed local maximum above 5 mg m^-3 on the
  shelf off Zhejiang (26.5-31.5 N, 121.5-125 E) at least 30 km from land; 80 km x 80 km window
  (40 x 40 cells of 2 km), centre shifted at random by up to 16 km; cells within 15 km of land
  out of bounds; >= 80% navigable; bloom contrast >= 0.3. Development 2018-2022: 274 windows;
  test 2023-2026: 148 windows. The vehicle starts at a random point on the window edge.
- Stale-map error (development windows, truth minus k-day-old map): sd 0.125 / 0.176 / 0.210
  for 1 / 2 / 3 days; spatial correlation ~5 cells (10 km); mean bias +0.016/+0.032/+0.045.
- Gap-filled maps are smooth in time; the real ocean also differs from a same-day satellite map
  (validation in the East and South China Seas: unbiased percentage difference about 39%,
  HY-1C COCTS, IEEE TGRS 2020, doi 10.1109/TGRS.2020.3036963). The simulated real ocean adds a
  spatially correlated field of 0.15 (correlation 3 cells) to the satellite map; 0.05-0.3 tested.
- Sensor: fluorometer error 0.1 per independent sample; one sample per km while moving, one per
  4 min while drifting.
- Geometry of one 20-minute interval: moving at 1.5 m/s covers 1.8 km (less than one 2-km cell)
  and takes about 2 samples; drifting takes 5 samples of the same water. In 24 h the vehicle
  can cover about 120-130 km (battery permitting), i.e. cross the 80-km window about 1.5 times.
- Staleness atlas (all 3197 days): spread of the 3-day change, median over the box: spring
  0.127, summer 0.107 (90th percentile 0.204, a band along the Zhejiang-Fujian coast and the
  Changjiang plume front reaching 0.25-0.3), autumn 0.103, winter 0.081.
- World model (JEPA, 5.5 M parameters; input: the last 3 days of chlorophyll and SST anomaly;
  trained 2018-2021 March-June, validated 2022): 1-3 day
  forecasts of the gap-filled map are no better than the latest map on the test years
  (RMSE 0.1229 vs 0.1226, 0.1439 vs 0.1439, 0.1487 vs 0.1474 for leads 1, 2, 3; spread/error
  0.70-0.93), 1.4% better on the validation year. Small-scale information has to be observed.

## Method
- The vehicle's map and memory: 48 imagined oceans (ensemble) drawn around the stale map with the
  data-calibrated uncertainty; updated with every sample by a serial ensemble adjustment Kalman
  filter (Anderson 2001) with Gaspari-Cohn localisation.
- Thinking = imagination: the planner scores candidate routes (polylines through two
  waypoints) on imagined oceans; a rollout = one route on one imagined ocean; route value =
  the best water found so far, averaged over the rest of the window (arriving sooner is worth
  more). Cross-entropy search, warm-started between intervals. The search uses 32 imagined
  oceans; 16 are never searched on (held out).
- Low-power computer 5-200 rollouts per minute (swept); GPU 50 times faster.
- Proposed controller: rehearsal in imagination. Before setting off, the vehicle takes 4
  held-out imagined oceans as "truths" and runs a complete imagined mission for each of five
  time-allocation strategies (always go; always think; think one interval in three; stop and
  think one in three; stop and resample one in three), with its own planner, computer speeds
  and battery, the same imagined truths and noise for every strategy; it follows the strategy
  with the lowest imagined regret. Self-assessed rehearsal (control) takes the truths from the
  imagined oceans the planner searches on.
- Where the rehearsal runs: before launch, on the support ship's or the shore computer (the
  vehicle is still on deck and linked); it simulates the vehicle's own computers (their speeds
  and power), it does not run on them. Its cost in our simulator: about 1.9 million rollouts per
  mission for the slow vehicle (would take about 125 h on that vehicle's own GPU), 4.6 s / 7.8 s /
  about 25 s per mission on one core of an ordinary desktop PC for the slow / moderate / fast
  vehicle. During the mission the vehicle is underwater with almost no communication, so all
  in-mission planning has to be done on board; that is why the onboard computer's speed matters.
- Why computer speed is given in rollouts per minute and swept (5-200): our two-waypoint planner
  and surface field are a simplified stand-in; a real vehicle's route evaluation (currents, depth,
  safety constraints) is far more expensive, so the speed of the computer relative to the
  planning problem is the quantity that matters and is varied.
- Baselines: the five fixed strategies; the fixed strategy that was best on the development
  years for that vehicle (per-vehicle tuning); classic one-step metareasoning (value of
  computation from the planner's own improvement trace, value of information by preposterior
  analysis over imagined oceans; Russell & Wefald 1991 style).

## Formulas (use these symbols or rename consistently)
- Field: $c(\mathbf{x})$ = log10 chlorophyll on a 40 x 40 grid of 2 km cells; the vehicle's
  answer at time $t$: $\hat{\mathbf{x}}(t) = \arg\max_{\mathbf{x}\in\mathcal{V}(t)} \bar{c}_t(\mathbf{x})$ over
  visited cells $\mathcal{V}(t)$, $\bar{c}_t$ = ensemble mean.
- Score (time-averaged regret over the window $T=24$ h):
  $R = \frac{1}{T}\int_0^T [\max_{\mathbf{x}} c(\mathbf{x}) - c(\hat{\mathbf{x}}(t))]\,dt$.
- Prior ensemble: $c^{(i)} = c_{\text{map}} + \sigma_k\, z^{(i)}$, $i=1..48$, $z^{(i)}$ Gaussian random fields with
  squared-exponential correlation of length $\ell$ (5 cells), $\sigma_k = \sqrt{s_k^2 + s_{\text{sat}}^2}$
  ($s_k$ = stale-map error for a $k$-day-old map, $s_{\text{sat}}$ = 0.15 satellite-vs-ocean error).
- Observation: $y = c(\mathbf{x}) + \varepsilon$, $\varepsilon \sim N(0, 0.1^2)$; serial EAKF update of every member
  with Gaspari-Cohn localisation (half-width $2\ell$).
- Route value on imagined ocean $i$: with $m_i(\tau)$ the best value met by time $\tau$ along the
  route (starting from the current best estimate),
  $V_i = \frac{1}{T_{\text{left}}}\int_0^{T_{\text{left}}} m_i(\tau)\,d\tau$ (frozen once cruising time runs out).
  Route chosen by the mean of $V_i$ over the 32 searched members; judged honestly by the mean
  over the 16 held-out members.
- Energy: hotel 15 W, propulsion 30 W when moving, GPU +20 W when thinking; 1 kWh; the mission ends
  at 24 h or when energy is exhausted.
- Rehearsal: for $j$ in 4 held-out members, for each strategy $s$ in 5 strategies, run the
  whole mission in imagination with truth $c^{(j)}$, get $R_{s,j}$; follow
  $s^* = \arg\min_s \frac{1}{4}\sum_j R_{s,j}$.

## Results
- Planning budget (80 development windows x 3 seeds, map 3 days old, first 8 h; results/curse3_dev):
  real route value 0.749 (64 rollouts), 0.793 (2000), 0.803 (200,000); the planner's own score
  during search 0.762, 0.833, 0.917; the same routes judged on the 16 held-out imagined oceans
  0.745, 0.794, 0.802 - within 0.005 of reality at every budget when the map uncertainty is
  calibrated. Halving the stated uncertainty biases the held-out judgement by -0.06, 1.5x by
  +0.07, but the improvement with budget stays right (64 -> 200,000: held-out +0.059/+0.054,
  real +0.054/+0.047).
- Main comparison on the test years (148 windows 2023-2026, map 3 days old, satellite-vs-ocean
  error 0.15, sensor 0.1; results/main_v3_test_*). Time-averaged regret (lower is better);
  "tuned" = the fixed strategy best on 120 development windows for that vehicle; differences to
  tuned with 95% intervals from a bootstrap over bloom weeks:
  | controller | slow computer (5/min) | moderate (20/min) | fast (100/min) | efficient accelerator (20/min, +5 W) |
  |---|---|---|---|---|
  | always go | 0.374 (+0.104) | 0.266 (-0.002) | 0.267 (tuned) | 0.266 (-0.000) |
  | always think | 0.273 (+0.003) | 0.269 (+0.000) | 0.269 (+0.003) | 0.267 (tuned) |
  | think 1 in 3 | 0.270 (tuned) | 0.269 (tuned) | 0.265 (-0.001) | 0.266 (-0.001) |
  | stop and think 1 in 3 | 0.331 (+0.061) | 0.328 (+0.059) | 0.327 (+0.060) | 0.327 (+0.060) |
  | stop and resample 1 in 3 | 0.408 (+0.138) | 0.335 (+0.066) | 0.331 (+0.065) | 0.335 (+0.068) |
  | one-step metareasoning | 0.287 (+0.017; +0.009 to +0.025) | 0.287 (+0.018; +0.011 to +0.026) | 0.282 (+0.015; +0.005 to +0.024) | 0.278 (+0.011; +0.005 to +0.017) |
  | rehearsal (held-out truths) | 0.276 (+0.007; -0.001 to +0.014) | 0.265 (-0.003; -0.009 to +0.003) | 0.268 (+0.002; -0.005 to +0.008) | 0.266 (-0.001; -0.006 to +0.005) |
  | rehearsal (searched truths) | 0.273 (+0.003; -0.003 to +0.010) | 0.268 (-0.000; -0.005 to +0.004) | 0.271 (+0.004; -0.000 to +0.010) | 0.265 (-0.002; -0.009 to +0.007) |
  The table for the paper is generated from the results: paper/tables/main_table.tex
  (\input it; do not retype numbers). "Tuned" is chosen on the development years 2018-2022 and
  then evaluated on the untouched test years: it is a strong baseline that needs past missions
  with that vehicle, not an oracle and not chosen after seeing the test results.
- Moderate computer: always go 0.266, always think 0.269, think 1 in 3 0.269 differ by at most
  0.003 - within noise (always go minus tuned: -0.002, interval -0.010 to +0.005). Do not
  explain this tiny difference with a mechanism.
- Rehearsal minus one-step metareasoning (paired, 95% interval, bootstrap over bloom weeks):
  slow -0.011 (-0.019 to -0.002), moderate -0.022 (-0.030 to -0.013), fast -0.013 (-0.020 to
  -0.007), efficient accelerator -0.012 (-0.019 to -0.004).
  There are no p-values; use these intervals.
- What one-step metareasoning does with its intervals: slow computer - thinks on the GPU in 80%
  of intervals and is stopped (drifting) in 34%; moderate - thinks in 93% (63% while moving, 30%
  stopped to think) and is stopped in 33%; fast - thinks in 97%, stopped 33%; efficient
  accelerator - thinks in 94%, stopped 33%.
- Which strategy rehearsal picks (share of test missions), moderate computer: think 1 in 3 43%,
  always go 30%, always think 25%, stop and resample 1 in 3 1%. Slow and fast computers and the
  efficient accelerator: see below.
- Fast computer (100 rollouts/min, +20 W GPU), test years, 148 missions; tuned on the development
  years = always go (development: always go 0.298, think 1 in 3 0.299, always think 0.310, the
  stopping strategies 0.365-0.366): always go 0.267 (tuned), think 1 in 3 0.265 (-0.001), always
  think 0.269 (+0.003), stop and think 0.327 (+0.060), stop and resample 0.331 (+0.065), one-step
  metareasoning 0.282 (+0.015; 0.005 to 0.024), rehearsal 0.268 (+0.002; -0.005 to 0.008),
  searched-truth rehearsal 0.271 (+0.004). Rehearsal minus one-step metareasoning -0.013 (-0.020
  to -0.007). One-step metareasoning thinks in 97% of intervals and is stopped in 33%. Rehearsal
  picks always go 47%, think 1 in 3 28%, always think 22%, a stopping strategy 3%; held-out and
  searched rehearsal agree on 37% of missions. Rehearsal costs 37 million rollouts per mission
  here (25 s on one PC core).
- Efficient accelerator (moderate computer, 20 rollouts/min, but the GPU costs only +5 W), test
  years, 148 missions; tuned on the development years = always think (development: always think
  0.292, think 1 in 3 0.296, always go 0.299, stopping 0.358-0.362): always think 0.267 (tuned),
  always go 0.266 (-0.000), think 1 in 3 0.266 (-0.001), stop and think 0.327 (+0.060), stop and
  resample 0.335 (+0.068), one-step metareasoning 0.278 (+0.011; 0.005 to 0.017), rehearsal 0.266
  (-0.001; -0.006 to 0.005), searched-truth rehearsal 0.265 (-0.002). Rehearsal minus one-step
  metareasoning -0.012 (-0.019 to -0.004). One-step metareasoning thinks in 94% of intervals and
  is stopped in 33%. Rehearsal picks always think 43%, think 1 in 3 35%, always go 20%, stopping
  1% (compare the moderate computer with the +20 W GPU: always go 30%, always think 25%) - with
  cheap thinking it thinks more often, as it should; held-out and searched rehearsal agree on 39%
  of missions. Random pick among the three moving strategies 0.267; best per mission in
  hindsight 0.242.
- Across all four vehicles: rehearsal is within the interval of the per-vehicle tuned strategy
  (differences +0.007, -0.003, +0.002, -0.001) and better than one-step metareasoning in every
  case (-0.011, -0.022, -0.013, -0.012, all intervals below zero). The tuned strategy itself
  differs by vehicle (think 1 in 3, think 1 in 3, always go, always think), but apart from the
  slow computer the three moving strategies are within 0.004 of each other on the test years
  (moderate 0.003, fast 0.004 - always think 0.269 vs think 1 in 3 0.265 -, efficient 0.001).
- Slow computer, which strategy rehearsal picks (rerun with the choice recorded; the regrets of the
  rerun are identical to the first run on all 148 missions - runs are exactly reproducible):
  think 1 in 3 55%, always think 39%, always go 1%, a stopping strategy 4%. So where always going
  is costly (+0.104), rehearsal almost never picks it. Held-out and searched rehearsal agree on
  41% of missions. Random pick among the five fixed strategies 0.331, among the three moving ones
  0.306, best per mission in hindsight 0.250, rehearsal 0.276.
- Rehearsal's share of always go grows with the computer: slow 1%, moderate 30%, fast 47%; with the
  cheap accelerator it picks always think most (43%).
- Check of the mechanism (test years, slow and moderate computers, same missions and seeds): the
  same one-step metareasoning, but judging the value of more planning and of looking on the 16
  held-out imagined oceans instead of the 32 searched ones (selection on the searched, valuation
  on the held-out - the double-estimation idea of van Hasselt 2010; nothing else changed):
  - intervals spent thinking fall from 80% to 30% (slow) and from 93% to 38% (moderate); intervals
    standing still fall from 34% to 17% and from 33% to 17%;
  - regret 0.278 vs 0.287 (slow; difference -0.009, interval -0.018 to +0.000) and 0.270 vs 0.287
    (moderate; -0.017, -0.025 to -0.009);
  - no clear difference from rehearsal (+0.002, -0.007 to +0.010; +0.005, -0.003 to +0.011).
  Reading: most of one-step metareasoning's over-planning comes from valuing computation with the
  planner's own score on the oceans it searched; judging on held-out oceans removes most of it.
  The remaining stops (17%) still cost, since stopping never pays here. The held-out idea is
  what both working controllers share: rehearsal uses held-out oceans as imagined truths for whole
  missions, the corrected one-step controller uses them to value the next interval.
- Phase diagram (fig_phase; development missions, 60 per cell, 18 cells: low-power computer 5, 10,
  20, 50, 100, 200 rollouts/min x real-ocean departure from the map 0.05, 0.15, 0.3):
  - thinking one interval in three beats always going clearly only on the slowest computer
    (5/min): -0.086, -0.109, -0.138 for departures 0.05, 0.15, 0.3 - the worse the map, the more
    thinking pays there; at 10/min one cell (departure 0.15) is marginal (-0.017, interval -0.035
    to -0.001); from 20/min up no strategy is clearly better than always going in any cell;
  - the better stopping strategy is worse than the best moving strategy in every cell, by 0.063 to
    0.118 (all intervals above zero);
  - always going's regret grows with the map's departure (at 20/min: 0.273, 0.342, 0.495).
- Mission-to-mission spread of regret (standard deviation over test missions) is about 0.13 for
  the good strategies, while the good strategies differ from each other by 0.01 or less; one
  mission says little about which strategy is better, which is why the comparison uses 148
  missions and paired differences.
- Imagined regrets are higher than real by 0.05-0.07 for every strategy alike (the reason is not
  established; do not explain it); because the offset is common, it does not by itself change
  the ranking.
- What rehearsal does and does not achieve (moderate computer, 148 test missions; fast computer
  similar on its first 134): it almost never picks a stopping strategy and so avoids the bad
  options, which is where its advantage over a random pick comes from (random pick among the
  five fixed strategies: 0.293; rehearsal 0.265). Among the three good strategies, whose real
  differences are 0.003 or less, its per-mission pick is no better than chance: random pick
  among those three gives 0.268; held-out and searched rehearsal pick the same strategy on only
  38% of missions (about what two independent picks with these shares would give), although
  they pick each strategy equally often overall (43/30/25% vs 44/32/23%); the strategy picked is
  on average 0.022 worse than the best one for that mission, and always using the best one per
  mission (known only in hindsight) would give 0.243. So rehearsal adapts to the vehicle, not to
  the individual mission: four imagined missions cannot separate strategies whose real
  difference (0.01 or less) is far below the mission-to-mission spread. On the slow computer it
  rarely picks always go (1%), which costs +0.104 there.
- Example mission (2023-04-15, slow computer; first test mission in date order where the two
  strategies differ by more than 0.1): the vehicle starts on the east edge; the 3-day-old map is
  low in the north-east and higher towards the west and south-west; the true densest water is in
  the south-west corner. Always go heads south-west to the middle of the window and then moves
  back and forth there; its answer stays about 0.4 off (time-average 0.43). Thinking one interval
  in three crosses the window to the south-west corner; its answer reaches the true densest
  water after about 19 h (error 0; time-average 0.31).
- Earlier (final-regret objective, superseded, not for the paper unless useful as motivation):
  learning a strategy selector from noisy mission outcomes failed (strategy differences <= 0.01
  vs mission-to-mission spread ~0.08).
