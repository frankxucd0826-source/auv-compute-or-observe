# Facts sheet for the writer (revision 4)

Everything here must hold in the paper; nothing outside it may be stated as a result. Values are
log10 chlorophyll (mg m^-3) unless stated. "Interval" = 95% interval of a paired difference from a
bootstrap over bloom weeks (missions of the same week resampled together). No p-values.

## Setting
- Course paper, Zhejiang University, 《海洋大数据技术原理与应用》, autumn 2026 (instructor 张帆).
- Scenario: harmful algal bloom emergency survey off Zhejiang, East China Sea. Prorocentrum
  donghaiense blooms recur in late spring and early summer (zhao2025distinguishing: records of 2021
  and 2023 between late April and early June off Taizhou, Wenzhou and Ningbo); Lou & Hu 2014
  (lou2014diurnal) tracked one bloom in May 2011 with hourly geostationary images: the patches
  drifted back and forth with the tides. 2023 national bulletin (mnr2024bulletin): 46 red tides,
  about 1500 km^2, 29 of them toxic or harmful. Do not quote a bloom chlorophyll threshold from the
  literature; the mission windows use our own criterion of 5 mg m^-3.
- The operations centre sends one autonomous underwater vehicle into an 80 km x 80 km window for
  24 h; at any moment it may ask where the densest water is; the vehicle reports the visited place
  of highest estimated chlorophyll. Underwater there is almost no communication, so all in-mission
  planning is on board.
- Vehicle (REMUS 100 class, remus100): 1.5 m/s, 1 kWh battery, about 22 h at 3 kn, i.e. about 45 W
  in cruise = 15 W hotel (navigation, sensors, a low-power processor that always replans in the
  background) + 30 W propulsion. High-performance computer: an embedded graphics-processor module
  (jetsonorinnx, 10-25 W), +20 W when on (the "efficient accelerator" vehicle: +5 W), 50 times the
  rollouts of the low-power processor.
- Every 20-minute interval the body either goes (follows the plan, 1.8 km, about 2 samples) or
  stops (motor off, drifts with the water, 5 samples of the same water), and the brain either
  keeps the background planning or plans deeply on the high-performance computer. Computing and
  moving run in parallel; the new plan is computed for where the vehicle will be when it takes
  over and replaces the old plan at the end of the interval. Mission ends at 24 h or when the
  battery is empty. In 24 h the vehicle can cover about 120-130 km (about 1.5 crossings).
- Frame drifting with the surface water: the bloom does not move relative to the water; currents
  act through the age of the satellite map, which the data contain.
- Sensor: fluorometer error 0.1 per independent sample.
- Score: time-averaged regret R = (1/T) integral over T=24 h of [max_x c(x) - c(x_hat(t))] dt
  (the answer is frozen after the mission ends). Lower is better; arriving sooner is worth more.
  0.1 corresponds to roughly 20% lower concentration than the densest water, 0.3 to about half.

## Data (ocean big data)
- Chlorophyll-a: NOAA CoastWatch merged VIIRS (S-NPP, NOAA-20) and Sentinel-3A OLCI, gap-filled
  with DINEOF (beckers2003dineof), 2 km, daily, 2018-01-01 to 2026-10-23 = 3197 days, box
  25-33 N, 119.5-127 E, 385 x 361 pixels per day. SST: JPL MUR v4.1 (chin2017mur), 0.01 deg,
  subsampled to 0.04 deg. Both from NOAA CoastWatch ERDDAP servers.
- Mission windows: April-June; strongest smoothed local maximum above 5 mg m^-3 on the shelf off
  Zhejiang (26.5-31.5 N, 121.5-125 E) at least 30 km from land; 80 km window (40 x 40 cells of
  2 km), centre shifted at random by up to 16 km; cells within 15 km of land out of bounds;
  >= 80% navigable; contrast >= 0.3. Development 2018-2022: 274 windows; test 2023-2026: 148.
  The vehicle starts at a random navigable point on the window edge.
- Stale-map error in the development windows (map of the day minus k-day-old map): sd 0.125 /
  0.176 / 0.210 for k = 1/2/3; spatial correlation about 5 cells (10 km); mean bias +0.016 /
  +0.032 / +0.045.
- Seasonal atlas (all 3197 days, spread of the 3-day change, median over the box): spring 0.127,
  summer 0.107, autumn 0.103, winter 0.081; in summer a band along the Zhejiang-Fujian coast and
  the Changjiang plume front reaches 0.25-0.3.
- A same-day satellite map also differs from the real ocean: in-situ validation of HY-1C COCTS
  in the East and South China Seas (ye2021cocts) gives an unbiased percentage difference of about
  39%, about 0.15 in log units.
- Deep spatio-temporal forecaster (joint-embedding predictive architecture, assran2025vjepa2;
  5.5 million parameters; input: the last 3 days of chlorophyll and SST anomaly; trained on
  2018-2021 March-June, validated on 2022, where it was 1.4% better than keeping the latest map):
  on the test years its errors for 1/2/3-day leads are 0.1229 / 0.1439 / 0.1487 against
  0.1226 / 0.1439 / 0.1474 for keeping the latest map (spread/error 0.70-0.93). No skill: small
  scales have to be observed.

## True ocean (two models; both built on the real satellite map of the mission day)
- Main setting ("当天卫星图 + 小尺度变化"): the satellite map of the mission day plus a spatially
  correlated field of standard deviation 0.15 and correlation length 3 cells (6 km), standing for
  what a satellite map misses (sub-pixel patches and retrieval error, calibrated by ye2021cocts).
- All-real-data setting ("当天卫星图"): the satellite map of the mission day itself.
- In both, the vehicle carries the real satellite map of 3 days earlier. The prior uncertainty is
  sigma_k = sqrt(s_k^2 + s_sat^2) with s_sat = 0.15 or 0 respectively (sigma_3 about 0.26 or 0.21).

## Method
- Imagined oceans: 48 members c^(i) = c_map + sigma_k z^(i), z^(i) Gaussian random fields with
  squared-exponential correlation of length 5 cells (10 km); updated with every sample by a serial
  ensemble adjustment Kalman filter (anderson2001eakf) with Gaspari-Cohn localisation of half-width
  10 cells (gaspari1999correlation). Observation y = c(x) + e, e ~ N(0, 0.1^2).
- Planning = imagination: candidate routes are polylines through two waypoints; one rollout = one
  route on one imagined ocean; route value on member i: V_i = (1/T_left) integral of m_i(tau),
  m_i = best value met so far along the route (from the current best estimate), frozen when the
  cruising time runs out. Cross-entropy search (deboer2005cem), warm-started across intervals.
- Separation of search and judgement: 32 members are searched; 16 are held out (also assimilated,
  never used by the search). Optimizer's curse: smith2006curse; double estimation: vanhasselt2010double.
- Low-power processor 5, 20 or 100 rollouts per minute (sweep 5-200); high-performance computer 50x.
  Why rollouts per minute: the two-waypoint planner on a 2-D surface field is a simplified stand-in
  for real underwater route evaluation (currents, depth, safety), so the computer's speed relative
  to the planning problem is what matters and is varied.
- Five time-allocation strategies (names in terms.md): 一直走; 一直深想; 三段深想一段; 三段停下深想一段;
  三段停下复测一段 (in the last two, one interval in three is spent stopped).
- Pre-launch rehearsal (proposed): before launch, while the vehicle is on deck and linked, the
  support ship's or shore computer takes 4 held-out imagined oceans as imagined truths; for each
  truth and each strategy it runs a complete 24-h imagined mission with the vehicle's own planner,
  computer speeds and battery (same imagined truths and noise for every strategy) and records the
  imagined regret R_{s,j}; the vehicle follows s* = argmin_s (1/4) sum_j R_{s,j}. Strategies are
  compared by their outcome on the imagined truth, not by the planner's own score.
  Cost in our simulator: about 1.9 million rollouts per mission for the slow vehicle (about 125 h
  on its own high-performance computer); on one core of an ordinary desktop PC 4.6 s / 7.8 s /
  about 25 s per mission for the slow / moderate / fast vehicle.
- The same principle online ("单步元推理（留出估值）"): classic one-step metareasoning (Russell &
  Wefald style, russell1991right) values one more interval of deep planning by the improvement of
  the planner's own search score and the value of resampling by a preposterior analysis over the
  imagined oceans; the held-out variant computes both values on the 16 held-out oceans instead of
  the 32 searched ones (selection on the searched, valuation on the held-out); nothing else changes.

## Compared controllers (names exactly as in terms.md)
- Fixed strategies (five). Methods that need past missions: 调好的固定策略 = the fixed strategy with
  the lowest mean regret on 120 development missions for that vehicle and truth model (chosen on
  2018-2022, evaluated on 2023-2026: a strong baseline, not an oracle); 按历史任务学习的选择器 =
  gradient-boosted regressions trained on the same development missions that predict each
  strategy's regret from features of the stale map known before launch (maximum, median, contrast,
  spread, distance from the start to the map maximum, navigable fraction, map value at the start,
  share of cells near the maximum) and pick the lowest per mission (the learned compute-budget
  selection of magnino2026metareasoning is the closest published idea). Online metareasoning:
  单步元推理, 单步元推理（留出估值）. Survey rules without route planning (the vehicle always goes,
  the map is updated in the same way): 割草机式全覆盖 = parallel lanes 16 km apart from the launch
  edge (galceran2013coverage); 贪心：驶向估计最浓处 = head for the unvisited cell of highest
  estimated chlorophyll; 上置信界采样 = the same with mean + 2 standard deviations
  (srinivas2012gpucb); 汤普森采样 = every interval draw one imagined ocean and head for its densest
  unvisited cell (russo2018thompson). Reference only: 每次任务事后最优 = the best of the five fixed
  strategies chosen per mission in hindsight. Also: random pick among the five / three moving
  strategies.

## Results

### R1 Planning budget (80 development windows x 3 seeds, map 3 days old, first 8 h; main truth model)
- Real route value 0.749 (64 rollouts), 0.793 (2000), 0.803 (200,000); the planner's search score
  0.762, 0.833, 0.917 (0.114 above reality at the largest budget); the same routes on the 16
  held-out oceans 0.745, 0.794, 0.802 - within 0.005 of reality at every budget.
- Halving the stated uncertainty shifts the held-out judgement by -0.06, 1.5 times by +0.07, but
  the gain from 64 to 200,000 rollouts stays right (held-out +0.059/+0.054, real +0.054/+0.047).

### R2 Main comparison (148 test missions 2023-2026, map 3 days old, sensor 0.1)
Time-averaged regret (Table 2). Main truth model (slow / moderate / fast / efficient accelerator):
- rehearsal 0.276 / 0.265 / 0.268 / 0.266; tuned fixed 0.270 / 0.269 / 0.267 / 0.267 (tuned =
  三段深想一段, 三段深想一段, 一直走, 一直深想); learned selector 0.278 / 0.269 / 0.273 / 0.266;
  one-step metareasoning 0.287 / 0.287 / 0.282 / 0.278; one-step with held-out valuation 0.278 /
  0.270 / 0.270 / 0.267; greedy 0.285; upper confidence bound 0.299; Thompson 0.332; lawnmower
  0.424 (rules do not plan, same for every vehicle); per-mission best in hindsight 0.250 / 0.243 /
  0.243 / 0.242; always go 0.374 / 0.267 / 0.267 / 0.267.
- Rehearsal minus (interval): tuned +0.007 (-0.000, +0.014), -0.003 (-0.009, +0.003), +0.002
  (-0.005, +0.008), -0.001 (-0.006, +0.005); learned -0.001, -0.004, -0.004, +0.000 (all
  intervals include 0); one-step metareasoning -0.011 (-0.019, -0.002), -0.022 (-0.030, -0.013),
  -0.013 (-0.020, -0.007), -0.012 (-0.019, -0.004); held-out one-step -0.002, -0.005, -0.001,
  -0.001 (all intervals include 0); greedy -0.009 (-0.022, +0.004) on the slow computer, -0.020,
  -0.017, -0.019 on the others (intervals below 0); upper confidence bound -0.023 to -0.034;
  Thompson -0.056 to -0.067; lawnmower -0.148 to -0.159 (all below 0); per-mission best in
  hindsight +0.022 to +0.027.
- All-real-data truth model (same-day satellite map as truth): regrets are lower for every
  controller (the truth has no unresolved small scales); rehearsal 0.197 / 0.191 / 0.195 / 0.191;
  tuned 0.194 / 0.196 / 0.191 / 0.191 (tuned = 三段深想一段, 一直走, 三段深想一段, 三段深想一段);
  one-step metareasoning 0.202 / 0.202 / 0.204 / 0.199. Rehearsal minus tuned +0.003, -0.004,
  +0.003, -0.001 (all intervals include 0); minus learned -0.005 to +0.003 (include 0); minus
  one-step metareasoning -0.006 (-0.011, -0.000), -0.010 (-0.016, -0.004), -0.010 (-0.017,
  -0.002), -0.010 (-0.014, -0.006); minus greedy -0.010 to -0.016 (all below 0); minus upper
  confidence bound -0.027 to -0.034; Thompson -0.059 to -0.066; lawnmower -0.132 to -0.139;
  per-mission best in hindsight +0.010 to +0.015. The better stopping strategy is 0.054-0.059 worse
  than the best moving strategy here as well (main truth model: 0.061-0.062).
- Summary: on every vehicle and under both truth models, rehearsal is within the interval of the
  two methods that need past missions, below one-step metareasoning, and below every survey rule
  except greedy on the slow computer under the main truth model (tie).
- Mission-to-mission spread of regret (sd over the 148 missions) about 0.13 (main) and 0.11-0.12
  (all-real-data), while good strategies differ by 0.01 or less.
- Table 2 footnote (use as is): a 调好的固定策略在主设置下依次为三段深想一段、三段深想一段、一直走、
  一直深想，在“当天卫星图”真值下依次为三段深想一段、一直走、三段深想一段、三段深想一段。

### R3 Mechanism: why one-step metareasoning loses (main truth model)
- One-step metareasoning has the high-performance computer on in 80% / 93% / 97% / 94% of
  intervals and is stopped in 33-34% (slow / moderate / fast / efficient); with held-out valuation:
  on in 30% / 38% / 44% / 39%, stopped in 15-18%; rehearsal's strategies: on in 54% / 35% / 26% /
  54%, stopped in 0.5-1.8%.
- Held-out valuation lowers regret by 0.009 (slow; interval -0.018 to 0.000) and 0.017 (moderate;
  -0.025 to -0.009), and 0.012 / 0.010 on the fast / efficient vehicles (rational 0.282 -> 0.270,
  0.278 -> 0.267), reaching rehearsal's level everywhere (differences within 0.005, intervals include
  0). Reading: most of the over-planning comes from valuing computation (and looking) with the
  planner's own score on the oceans it searched; the remaining stops still cost, since stopping
  never pays here.
- Rehearsal is insensitive to whether its imagined truths come from held-out or searched oceans
  (differences -0.004 to +0.004, intervals include 0), because it compares strategies by their
  outcomes on the imagined truth, not by the planner's score; the planner's score is what the
  one-step controller trusts.

### R4 What rehearsal picks (main truth model; share of the 148 missions)
- slow: 三段深想一段 55%, 一直深想 39%, 一直走 1%, stopping 4%; moderate: 三段深想一段 43%,
  一直走 30%, 一直深想 25%, stopping 1%; fast: 一直走 47%, 三段深想一段 28%, 一直深想 22%,
  stopping 3%; efficient accelerator (+5 W): 一直深想 43%, 三段深想一段 35%, 一直走 20%, stopping 1%.
- So the share of 一直走 grows with the computer (1% -> 30% -> 47%) and cheap computing raises
  一直深想 (25% -> 43% at the same speed). Where always going is costly (slow computer, +0.104 worse
  than tuned) rehearsal almost never picks it.
- Rehearsal's advantage over a random pick comes from avoiding bad options (random among the five
  0.331 / 0.293 / 0.292 / 0.292; among the three moving strategies 0.306 on the slow computer, 0.267-
  0.268 on the others). Among the three moving strategies, whose real differences are 0.004 or less
  except on the slow computer, its per-mission pick is no better than chance: held-out and searched
  rehearsal pick the same strategy on only 37-41% of missions.

### R5 Ablation (main truth model, slow / moderate computer; rehearsal variant minus full method)
- Imagined truths 1: +0.013 (-0.000, +0.027) / +0.010 (-0.001, +0.020); 2: +0.010 (-0.001, +0.022)
  / +0.006 (-0.002, +0.013); 8: -0.007 (-0.012, -0.001) / +0.003 (-0.004, +0.009). Fewer truths
  hurt, more help only on the slow computer; 4 is a reasonable cost.
- Truths from searched oceans: -0.004 / +0.003 (include 0) - see R3.
- Uncertainty not calibrated from the data: half the calibrated value +0.002 / +0.004 (include 0);
  twice +0.011 (+0.001, +0.020) / +0.020 (+0.011, +0.030). With doubled uncertainty every strategy
  gets worse (moderate computer: moving strategies 0.275-0.283 instead of 0.267-0.269), and
  rehearsal no longer matches the best fixed strategy (0.286 vs 0.275).
- Whole-mission rehearsal replaced by interval-by-interval held-out valuation: +0.002 / +0.005
  (include 0) - both uses of the principle work.
- No rehearsal, random pick among the five strategies: +0.055 / +0.028; among the three moving
  strategies: +0.029 / +0.003.
- Reference, methods that need past missions: tuned -0.007 / +0.003, learned +0.001 / +0.004
  (include 0).

### R6 Scope
- Phase diagram (Fig. 8; 60 development missions per cell, five fixed strategies): thinking (the
  better of 一直深想 and 三段深想一段) beats 一直走 clearly only on the slowest computer (5 per
  minute, i.e. about 100 rollouts per 20-minute interval, far below the about 2000 where real value
  saturates): -0.086 / -0.109 / -0.138 for departures 0.05 / 0.15 / 0.30 - the worse the map, the
  more thinking pays; at 10 per minute one cell is marginal (-0.017, -0.035 to -0.001); from 20 per
  minute up no cell shows a clear gain. Stopping: the better stopping strategy is worse than the
  best moving one in every cell, by 0.063 to 0.118 (all intervals above 0). Fourth row (departure 0, the satellite map itself
  as truth): thinking beats always going clearly only at 5 per minute (-0.080, -0.119 to -0.043);
  no clear gain from 10 per minute up; stopping is worse in every cell of this row by 0.061-0.076.
  Over all 24 cells, the better stopping strategy is worse than the best moving one by 0.061-0.118.
- Why stopping does not pay: resampling one place five times lowers its measurement error from
  0.1 to about 0.045, but the bottleneck is the unvisited water (prior uncertainty about 0.26), and
  stopping a third of the time delays reaching the dense water, which the time-averaged score
  penalises.
- Fresher map (1 day old, main truth model): slow computer: tuned = 一直深想 0.250, rehearsal 0.251
  (+0.001, -0.005 to +0.011), one-step metareasoning 0.260 (rehearsal minus -0.009, -0.018 to
  +0.001); moderate computer: tuned = 一直走 0.250, rehearsal 0.243
  (-0.007, -0.014 to -0.002: here rehearsal is lower than the tuned strategy), one-step metareasoning
  0.260 (rehearsal minus -0.017, -0.022 to -0.013); 三段深想一段 0.239 is the best fixed strategy on the
  test years although 一直走 was best on the development years.

### R7 Example mission (Fig. 6): 2023-04-15, slow computer - see figures_rev4.md.

### R8 Limits (5.8, one paragraph)
- The true ocean is the real satellite map of the day (with or without a calibrated small-scale
  field), not in-situ measurements; a 2-D surface field and a two-waypoint planner stand in for 3-D
  underwater planning; the drifting frame ignores horizontal shear and the diel vertical migration of
  algae; rehearsal runs once before launch and is not repeated during the mission; four imagined
  missions adapt the choice to the vehicle, not to the individual mission (per-mission best in
  hindsight is 0.022-0.027 lower).
- Imagined regrets are higher than real ones by 0.05-0.07 for every strategy alike (reason not
  established; do not explain it); the offset is common and does not change the ranking by itself.

### R9 Reproducibility
- Seeds are fixed per mission; rerunning rehearsal on the slow computer reproduced all 148 regrets
  exactly. All controllers on a mission share the same true ocean and sensor noise (paired).

## Do not claim
- No p-values; no claim that rehearsal adapts to individual missions; no claim that rehearsal beats
  the tuned strategy or the learned selector; no explanation of the 0.05-0.07 offset; no
  chlorophyll threshold from the literature; no number not listed here.
