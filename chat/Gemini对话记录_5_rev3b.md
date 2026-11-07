# 与 Gemini 的对话记录 5：第 3b 次修改

时间（回复保存时间）：2026-11-04 19:51 UTC。调用方式：Claude 用命令行工具 ask-gemini 把下面“发送内容”作为附件发给 Gemini，并附一句简短指令（按附件中的写作要求完成各节）；回复原样存档后再由 Claude 核对数字与引用、拆分进论文各节。下面两部分都是原文，未作删改。

本轮的写作要求见下方发送内容里的附件 `brief_rev3b.md`。

## 发送内容

<details><summary>展开（共 63069 字符）</summary>

```
########## ATTACHED FILE: brief_rev3b.md ##########

# Revision 3b (final tightening, second attempt)

The previous attempt shortened the paper far too much (body down to about 3,500 characters, lists
instead of paragraphs) and cannot be used. Please EDIT draft 3 (attached as the current
sections/*.tex) rather than rewrite it: keep every section and subsection, every paragraph and its
first sentence, all equations, figures, the table, all citations and all numbers, except for the
specific cuts and fixes below. Target length of the body: 8,300 to 8,800 Chinese characters
(draft 3 has about 9,600). Both abstracts stay as they are except fix 6.

## Cuts (about 1,000 characters in total)
1. 1.1: merge the two paragraphs into one by removing what the second repeats (about 250).
2. 4.3, last paragraph of the method: shorten the cost sentence, keeping: runs on the ship or shore
   computer; about 1.9 million rollouts for the slow vehicle, about 125 h on its own GPU; a few
   seconds per mission on one desktop core (about 80).
3. 5.3, first paragraph: drop the development-year regrets (0.298/0.299/0.310 and 0.292/0.296/
   0.299); keep which strategy was tuned for each vehicle (about 150).
4. 5.3, fourth paragraph (held-out versus searched rehearsal): keep the findings but with fewer
   numbers - similar overall shares; agreement on individual missions only 37-41%; rehearsal
   avoids the bad options (stopping everywhere, always going on the slow computer), which is
   where its gain over a random pick comes from (slow: 0.276 versus 0.306 for a random pick among
   the three moving strategies); among strategies whose real differences are 0.01 or less its
   per-mission pick is no better than chance; the per-mission best in hindsight (0.243 on the
   moderate computer versus 0.265) shows the room left (about 400).
5. Conclusion: do not repeat numbers already given in the results where a phrase suffices
   (about 150).

## Precise fixes
1. Apart from the slow computer, the three moving strategies differ by at most 0.004 on the test
   years (moderate 0.003, fast 0.004, efficient 0.001), not "不超过0.003" (twice in draft 3).
2. Conclusion, item 3: "30\%—38%" - the second percent sign must be escaped (38\%). Check every %.
3. 5.4: replace "这证实……主要源于用规划用海洋上的自评得分衡量计算价值" by a statement that the
   over-planning mostly comes from choosing and valuing on the same searched oceans ("表明"; both
   the value of planning more and of looking more were moved to the held-out oceans).
4. 5.3 (fourth paragraph) and limitation (5): delete the explanation "由于任务间遗憾标准差（约0.13）
   远大于策略间的真实差异" - it was not tested; state only the observation (fix 4 in the cuts).
5. The imagined-minus-real offset is "大致相同" for all strategies (0.05-0.07), not identical.
6. Chinese abstract, last sentence: "无需先验任务调参" -> "无需历史任务调参".
7. 1.2: the dates late April to early June come from Zhao et al.'s 2021 and 2023 records; say so,
   or keep only "晚春至初夏".

## Output
The five files, each preceded by a line "===== FILE: sections/<name>.tex =====": title, subtitle,
abstract, body, appendix. The appendix stays as in draft 3.


########## ATTACHED FILE: facts.md ##########

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


########## ATTACHED FILE: figures.md ##########

# Figures (file names without extension; width = \linewidth unless noted)

PNG copies of the finished figures are attached; describe only what is in them.

- fig_overview (Figure 1). Centre: a 3D block of the East China Sea window of one test mission
  (2025-04-04), its top surface coloured by the real chlorophyll the vehicle meets; a REMUS-class
  AUV with its track (light blue = going with low-power planning, orange = planning on the GPU);
  a pale ring at the true densest water ("赤潮最浓处"); above the block a small stack of imagined
  oceans, the top two framed orange (held out), the others framed dark blue (searched).
  (A, blue) ocean big data: 2018-2026 daily 2-km satellite chlorophyll, 3197 days; the real
  ocean the vehicle meets is not the 3-day-old satellite map (two thumbnails, "≠"); how wrong an
  old map is (1/2/3 days: 0.13/0.18/0.21; coastal fronts in summer up to 0.3 in 3 days); 422
  bloom-season missions cut from the data (development 2018-2022: 274; test 2023-2026: 148);
  "small-scale information has to be observed on site". An arrow labelled "出发前装入" goes from
  the old map to the stack. (B, green) the vehicle's imagination: 48 imagined oceans generated
  from the old map and the data-calibrated error; 32 used to plan routes, 16 held out to judge;
  "出发前预演": the five time-allocation strategies are each run once in imagination, one is
  chosen by the result on held-out oceans. (C, sand) every 20 minutes: 走 (follow the plan,
  sampling on the way), 深想 (plan on the high-performance computer, +20 W), 停下 (drift with
  the water, resample in place); the operations centre may ask at any time where the densest
  water is. No satellite is drawn.
- fig_atlas: four seasonal maps of the East China Sea box (25-33 N, 119.5-127 E): spread of the
  3-day change of log10 chlorophyll from all 3197 days; land grey; dots in the spring panel are
  mission windows (blue development 2018-2022, green test 2023-2026).
- fig_curse: (a) value of the planned route (y axis converted to mg/m3, time-averaged best
  concentration along the route) against imagined rollouts per decision (64 to 200,000, log
  axis): the planner's own score during search (red, keeps rising), the same route judged on
  the held-out imagined oceans (blue dashed), and its real value (black); shaded bands = spread
  over missions; real and held-out flatten after about 2000. (b) estimate minus reality in log
  units: search score (red) grows to about +0.11; held-out with calibrated uncertainty (blue
  dashed) stays at zero; held-out with the uncertainty stated 1.5 times too large (orange dotted)
  is about +0.07 at every budget, with it stated half as large (light blue dotted) about -0.06.
- fig_phase (attached PNG): a grid of low-power computer speed (5, 10, 20, 50, 100, 200 rollouts
  per minute) x how far the real ocean departs from the satellite map (0.05, 0.15, 0.3); 60
  development missions per cell, the five fixed strategies on the same missions. (a) a cell is
  coloured by the strategy with the lowest time-averaged regret only where it beats always going
  clearly (95% interval of the paired difference below zero), and the number is its regret minus
  that of always going; grey "≈" = no strategy clearly better than always going. (b) how much
  worse the better of the two stopping strategies is than the best strategy that never stops
  (positive = stopping costs).
- fig_example: one test mission (2023-04-15, slow computer): (a) the 3-day-old map the vehicle
  carries (start = white triangle on the east edge); (b) the real ocean, the track of always going
  (blue) and of thinking one interval in three (orange), the true densest water (star, south-west
  corner); (c) the error of the answer the operations centre gets, over 24 h (always going stays
  near 0.4, average 0.43; thinking one in three reaches 0 after about 19 h, average 0.31).
- No fig_main: the main comparison is the table paper/tables/main_table.tex.


########## ATTACHED FILE: terms.md ##########

imagined oceans: 想象中的海洋
held-out: 留出
held-out imagined oceans: 留出的想象海洋 / 留出海洋
searched imagined oceans: 规划用海洋
rollout: 想象推演
pre-mission rehearsal: 出发前预演
go (cruise and sample): 走
think deeply (plan on GPU): 深想
stop (drift and resample): 停下
always go: 一直走
always think: 一直深想
think one in three: 三段深想一段
stop and think one in three: 三段停下深想一段
stop and resample one in three: 三段停下复测一段
tuned strategy: 调好的
one-step metareasoning: 单步元推理
rehearsal (held-out truths): 出发前预演（留出海洋，本文）
rehearsal (searched truths): 出发前预演（规划用海洋，对照）
slow computer: 慢计算机
moderate computer: 中等计算机
fast computer: 快计算机
efficient accelerator: 省电加速器


########## ATTACHED FILE: tables/main_table.tex (generated) ##########

\resizebox{\linewidth}{!}{%
\begin{tabular}{lcccc}
\toprule
控制方式 & 慢计算机 & 中等计算机 & 快计算机 & 省电加速器 \\
 & {\footnotesize 5 次/分，+20 W} & {\footnotesize 20 次/分，+20 W} & {\footnotesize 100 次/分，+20 W} & {\footnotesize 20 次/分，+5 W} \\
\midrule
一直走 & 0.374（$+0.104$） & 0.266（$-0.002$） & 0.267（调好的） & 0.266（$-0.000$） \\
一直深想 & 0.273（$+0.003$） & 0.269（$+0.000$） & 0.269（$+0.003$） & 0.267（调好的） \\
三段深想一段 & 0.270（调好的） & 0.269（调好的） & 0.265（$-0.001$） & 0.266（$-0.001$） \\
三段停下深想一段 & 0.331（$+0.061$） & 0.328（$+0.059$） & 0.327（$+0.060$） & 0.327（$+0.060$） \\
三段停下复测一段 & 0.408（$+0.138$） & 0.335（$+0.066$） & 0.331（$+0.065$） & 0.335（$+0.068$） \\
\midrule
单步元推理 & 0.287（$+0.017$） & 0.287（$+0.018$） & 0.282（$+0.015$） & 0.278（$+0.011$） \\
 & {\footnotesize $[+0.009, +0.025]$} & {\footnotesize $[+0.011, +0.026]$} & {\footnotesize $[+0.005, +0.024]$} & {\footnotesize $[+0.005, +0.017]$} \\
出发前预演（留出海洋，本文） & 0.276（$+0.007$） & 0.265（$-0.003$） & 0.268（$+0.002$） & 0.266（$-0.001$） \\
 & {\footnotesize $[-0.001, +0.014]$} & {\footnotesize $[-0.009, +0.003]$} & {\footnotesize $[-0.005, +0.008]$} & {\footnotesize $[-0.006, +0.005]$} \\
出发前预演（规划用海洋，对照） & 0.273（$+0.003$） & 0.268（$-0.000$） & 0.271（$+0.004$） & 0.265（$-0.002$） \\
 & {\footnotesize $[-0.003, +0.010]$} & {\footnotesize $[-0.005, +0.004]$} & {\footnotesize $[-0.000, +0.010]$} & {\footnotesize $[-0.009, +0.007]$} \\
\bottomrule
\end{tabular}}


########## ATTACHED FILE: refs.bib ##########

% Only entries whose bibliographic details were checked against the publisher or the
% preprint record are listed here; see notes/文献调研.md for links.

@article{fossum2019,
  author = {Fossum, Trygve O. and Fragoso, Glaucia M. and Davies, Emlyn J. and others},
  title = {Toward adaptive robotic sampling of phytoplankton in the coastal ocean},
  journal = {Science Robotics},
  volume = {4}, number = {27}, pages = {eaav3041}, year = {2019},
  doi = {10.1126/scirobotics.aav3041}
}

@inproceedings{sung2021quit,
  author = {Sung, Yoonchang and Kaelbling, Leslie Pack and Lozano-P{\'e}rez, Tom{\'a}s},
  title = {Learning When to Quit: Meta-Reasoning for Motion Planning},
  booktitle = {IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  year = {2021}
}

@misc{magnino2026metareasoning,
  author = {Magnino, Lorenzo and Marino, Antonio and Amir, Michael and Shishika, Daigo and Prorok, Amanda},
  title = {Learning Robot Metareasoning: Adaptive Computation Budgets for Real-Time Control},
  howpublished = {\url{https://arxiv.org/abs/2610.23662}},
  year = {2026}
}

@inproceedings{shen2025thinking,
  author = {Shen, Junhong and others},
  title = {Thinking vs. Doing: Improving Agent Reasoning by Scaling Test-Time Interaction},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume = {38}, year = {2025}
}

@misc{cuadron2025overthinking,
  author = {Cuadron, Alejandro and others},
  title = {The Danger of Overthinking: Examining the Reasoning-Action Dilemma in Agentic Tasks},
  howpublished = {\url{https://arxiv.org/abs/2502.08235}},
  year = {2025}
}

@inproceedings{lin2015metareasoning,
  author = {Lin, Christopher H. and Kolobov, Andrey and Kamar, Ece and Horvitz, Eric},
  title = {Metareasoning for Planning Under Uncertainty},
  booktitle = {International Joint Conference on Artificial Intelligence (IJCAI)},
  year = {2015}
}

@inproceedings{horvitz1987reasoning,
  author = {Horvitz, Eric J.},
  title = {Reasoning About Beliefs and Actions Under Computational Resource Constraints},
  booktitle = {Proceedings of the Third Conference on Uncertainty in Artificial Intelligence (UAI)},
  year = {1987}
}

@inproceedings{xiao2020thinking,
  author = {Xiao, Ted and Jang, Eric and Kalashnikov, Dmitry and Levine, Sergey and Ibarz, Julian and Hausman, Karol and Herzog, Alexander},
  title = {Thinking While Moving: Deep Reinforcement Learning with Concurrent Control},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year = {2020}
}

@inproceedings{elboher2023formal,
  author = {Elboher, Amihay and Shperberg, Shahaf S. and Shimony, Solomon Eyal},
  title = {A Formal Metareasoning Model of Concurrent Planning and Execution},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence},
  year = {2023}
}

@inproceedings{jiang2015horizon,
  author = {Jiang, Nan and Kulesza, Alex and Singh, Satinder and Lewis, Richard},
  title = {The Dependence of Effective Planning Horizon on Model Accuracy},
  booktitle = {International Conference on Autonomous Agents and Multiagent Systems (AAMAS)},
  pages = {1181--1189}, year = {2015}
}

@article{smith2006curse,
  author = {Smith, James E. and Winkler, Robert L.},
  title = {The Optimizer's Curse: Skepticism and Postdecision Surprise in Decision Analysis},
  journal = {Management Science},
  volume = {52}, number = {3}, pages = {311--322}, year = {2006},
  doi = {10.1287/mnsc.1050.0451}
}

@inproceedings{vanhasselt2010double,
  author = {van Hasselt, Hado},
  title = {Double {Q}-learning},
  booktitle = {Advances in Neural Information Processing Systems (NIPS)},
  volume = {23}, year = {2010}
}

@article{hunt2021formalizing,
  author = {Hunt, Laurence T. and Daw, Nathaniel D. and Kaanders, Paula and others},
  title = {Formalizing planning and information search in naturalistic decision-making},
  journal = {Nature Neuroscience},
  volume = {24}, number = {8}, pages = {1051--1064}, year = {2021}
}

@article{anderson2001eakf,
  author = {Anderson, Jeffrey L.},
  title = {An Ensemble Adjustment {Kalman} Filter for Data Assimilation},
  journal = {Monthly Weather Review},
  volume = {129}, number = {12}, pages = {2884--2903}, year = {2001},
  doi = {10.1175/1520-0493(2001)129<2884:AEAKFF>2.0.CO;2}
}

@article{beckers2003dineof,
  author = {Beckers, J. M. and Rixen, M.},
  title = {{EOF} Calculations and Data Filling from Incomplete Oceanographic Datasets},
  journal = {Journal of Atmospheric and Oceanic Technology},
  volume = {20}, number = {12}, pages = {1839--1856}, year = {2003},
  doi = {10.1175/1520-0426(2003)020<1839:ECADFF>2.0.CO;2}
}

@misc{assran2025vjepa2,
  author = {Assran, Mido and others},
  title = {{V-JEPA} 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning},
  howpublished = {\url{https://arxiv.org/abs/2506.09985}},
  year = {2025}
}

@article{lou2014diurnal,
  author = {Lou, Xiulin and Hu, Chuanmin},
  title = {Diurnal changes of a harmful algal bloom in the {East China Sea}: Observations from {GOCI}},
  journal = {Remote Sensing of Environment},
  volume = {140}, pages = {562--572}, year = {2014},
  doi = {10.1016/j.rse.2013.09.031}
}

@article{chin2017mur,
  author = {Chin, Toshio M. and Vazquez-Cuervo, Jorge and Armstrong, Edward M.},
  title = {A multi-scale high-resolution analysis of global sea surface temperature},
  journal = {Remote Sensing of Environment},
  volume = {200}, pages = {154--169}, year = {2017}
}

@article{ye2021cocts,
  author = {Ye, X. M. and Liu, J. Q. and Lin, M. S. and Ding, J. and Zou, B. and Song, Q. J.},
  title = {Global Ocean Chlorophyll-a Concentrations Derived From {COCTS} Onboard the {HY-1C} Satellite and Their Preliminary Evaluation},
  journal = {IEEE Transactions on Geoscience and Remote Sensing},
  volume = {59}, number = {12}, pages = {9914--9926}, year = {2021},
  doi = {10.1109/TGRS.2020.3036963}
}

@article{gaspari1999correlation,
  author = {Gaspari, Gregory and Cohn, Stephen E.},
  title = {Construction of correlation functions in two and three dimensions},
  journal = {Quarterly Journal of the Royal Meteorological Society},
  volume = {125}, number = {554}, pages = {723--757}, year = {1999},
  doi = {10.1002/qj.49712555417}
}

@article{deboer2005cem,
  author = {de Boer, Pieter-Tjerk and Kroese, Dirk P. and Mannor, Shie and Rubinstein, Reuven Y.},
  title = {A Tutorial on the Cross-Entropy Method},
  journal = {Annals of Operations Research},
  volume = {134}, number = {1}, pages = {19--67}, year = {2005},
  doi = {10.1007/s10479-005-5724-z}
}

@book{russell1991right,
  author = {Russell, Stuart J. and Wefald, Eric H.},
  title = {Do the Right Thing: Studies in Limited Rationality},
  publisher = {MIT Press}, address = {Cambridge, MA}, year = {1991},
  isbn = {0262181444}
}

@misc{remus100,
  author = {{Kongsberg Maritime}},
  title = {{REMUS} 100 Autonomous Underwater Vehicle: product information (1 {kWh} lithium-ion battery; up to 22 h at 3 kn; 100 m depth rating)},
  howpublished = {\url{https://en.wikipedia.org/wiki/REMUS_(vehicle)}; \url{https://geo-matching.com/products/remus-100}},
  year = {2026}, note = {accessed 2026-11-05}
}

@misc{jetsonorinnx,
  author = {{NVIDIA}},
  title = {{Jetson Orin NX} modules: configurable module power 10--25 {W} (16 {GB}), up to 100 sparse {INT8} {TOPS}},
  howpublished = {\url{https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/}},
  year = {2026}, note = {accessed 2026-11-05}
}

Checked (People's Daily, 2024-04-24, p. 14, reporting the bulletin): 46 red tides in 2023, about 1500 km2 in total, 29 of them toxic or harmful.
@misc{mnr2024bulletin,
  author = {{自然资源部}},
  title = {2023 年中国海洋灾害公报},
  howpublished = {\url{https://paper.people.com.cn/rmrb/html/2024-04/24/nw.D110000renmrb_20240424_1-14.htm}},
  year = {2024}
}

@article{zhao2025distinguishing,
  author = {Zhao, Min and Li, Hao and Zhang, Xuan and Ding, Xiaosong and Gong, Fang},
  title = {A novel method for distinguishing different algal blooms in the {East China Sea} via geostationary ocean color satellite observations},
  journal = {Frontiers in Marine Science},
  volume = {12},
  pages = {1549711},
  year = {2025},
  doi = {10.3389/fmars.2025.1549711}
}


########## ATTACHED FILE: main.tex (template) ##########

% 浙江大学《海洋大数据》课程论文。编译：latexmk -xelatex main.tex
\documentclass[zihao=-4, a4paper, oneside]{ctexart}

% ---------- 版面 ----------
\usepackage[top=2.54cm, bottom=2.54cm, left=3.0cm, right=2.6cm, headheight=15pt]{geometry}
\usepackage{setspace}
\setstretch{1.5}
\setmainfont{Times New Roman}
\setCJKmainfont[BoldFont=SimHei, ItalicFont=KaiTi]{SimSun}
\setCJKsansfont{SimHei}
\setCJKfamilyfont{hei}{SimHei}
\setCJKfamilyfont{kai}{KaiTi}
\usepackage{amsmath, amssymb, bm}
\usepackage{graphicx, subcaption, booktabs, multirow, array}
\usepackage{xcolor}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[sort&compress, square, comma, numbers]{natbib}
\usepackage{caption}
\usepackage{placeins}

\captionsetup{font=small, labelsep=quad, labelfont=bf}
\captionsetup[figure]{name=图}
\captionsetup[table]{name=表}
\graphicspath{{figures/}}

% 标题样式：1 绪论 / 1.1 研究背景 / 1.1.1
\ctexset{
  section = {format=\zihao{3}\heiti, beforeskip=18pt, afterskip=12pt, name={,}, number=\arabic{section}},
  subsection = {format=\zihao{4}\heiti, beforeskip=12pt, afterskip=6pt},
  subsubsection = {format=\zihao{-4}\heiti, beforeskip=6pt, afterskip=3pt},
}

% 页眉页脚
\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{\zihao{5}\songti 海洋大数据\quad 课程论文}
\fancyfoot[C]{\zihao{5}\thepage}
\renewcommand{\headrulewidth}{0.6pt}

\newcommand{\coverline}[2]{\makebox[5em][s]{#1}：\underline{\makebox[16em][c]{#2}}}
\newcommand{\TBD}[1]{\textcolor{red}{[待补：#1]}}

\begin{document}

% ---------- 封面 ----------
\begin{titlepage}
  \centering
  \singlespacing
  \vspace*{2.0cm}
  {\zihao{2}\songti 海洋大数据\par}
  \vspace{0.9cm}
  {\zihao{0}\heiti 课\hspace{0.5em}程\hspace{0.5em}论\hspace{0.5em}文\par}
  \vspace{2.4cm}
  {\zihao{2}\heiti \input{sections/title}\par}
  \vspace{0.5cm}
  {\zihao{3}\songti \input{sections/subtitle}\par}
  \vfill
  {\zihao{4}\songti
  \begin{tabular}{l}
    \coverline{课程}{海洋大数据}\\[12pt]
    \coverline{姓名}{徐陈栋}\\[12pt]
    \coverline{学号}{3240100538}\\[12pt]
    \coverline{专业}{海洋工程与技术}\\[12pt]
    \coverline{任课教师}{张帆\ 研究员}\\[12pt]
    \coverline{提交日期}{2026 年 11 月\ \ \ 日}
  \end{tabular}\par}
  \vspace{2.0cm}
\end{titlepage}

% ---------- 摘要与目录 ----------
\pagenumbering{Roman}
\input{sections/abstract}
\clearpage
\tableofcontents
\clearpage
\pagenumbering{arabic}

% ---------- 正文 ----------
\input{sections/body}

% ---------- 参考文献 ----------
\clearpage
\phantomsection
\addcontentsline{toc}{section}{参考文献}
\bibliographystyle{gbt7714-numerical}
\bibliography{refs}

% ---------- 附录 ----------
\clearpage
\appendix
\input{sections/appendix}

\end{document}


########## ATTACHED FILE: sections/title.tex (current draft) ##########

基于想象海洋出发前预演的自主水下航行器思考与行动权衡研究


########## ATTACHED FILE: sections/subtitle.tex (current draft) ##########

——以八年卫星叶绿素数据驱动的东海赤潮应急巡测为例


########## ATTACHED FILE: sections/abstract.tex (current draft) ##########

\section*{摘\quad 要}
\addcontentsline{toc}{section}{摘要}

携带卫星先验底图的自主水下航行器（AUV）在现场巡测时受机载算力、电池与作业时间制约。因卫星图存在数日滞后与小尺度平滑偏差，航行器需在每个控制周期权衡：开启高功耗图形处理器（GPU）深想、靠低功耗规划继续走并采样，或停下随水漂流复测。固定规则难以适应不同硬件，单步元推理则会因规划器在有限样本上的过拟合而高估计算价值。本文提出基于留出想象海洋的集合同化与出发前预演方法：利用八年东海卫星叶绿素数据标定底图误差，围绕旧图生成48个想象海洋并随采样同化更新，32个用于规划航线，16个留出用于评判；下水前由母船或岸上计算机以4个留出海洋为假想真值，按机载算力与功耗模拟五种用时策略的24小时任务并择优。在2018至2026年东海3197天数据构建的422个赤潮窗口上的实验表明：留出评判在64至200,000次推演下与真实价值之差不超过0.005；深想仅在基础算力过慢时有益，停下始终不划算；在四种硬件、148个测试任务上，预演遗憾为0.265至0.276，与调好策略之差的95\%置信区间均包含0，且比单步元推理低0.011至0.022；改用留出评判的单步元推理同样消除了大部分过度规划。这表明将海洋遥感大数据转化为留出想象海洋可抑制计算自评偏差，使航行器无需先验任务调参即可适配机载算力与观测约束。

\vspace{1em}
\noindent\textbf{关键词：}海洋大数据；自主水下航行器；元推理；数据同化；赤潮巡测；计算与行动权衡

\clearpage
\section*{Abstract}
\addcontentsline{toc}{section}{Abstract}

Autonomous underwater vehicles (AUVs) carrying satellite prior maps must trade off computation against movement under onboard processor, battery, and mission-time constraints. Because satellite maps are several days old and smooth out small-scale features, the vehicle must decide at every control interval whether to activate a high-power graphics processing unit (GPU) to plan deeply, continue cruising and sampling under low-power background planning, or stop propulsion to drift and resample locally. Fixed time-allocation rules do not generalise across hardware platforms, while classic one-step metareasoning overestimates the value of computation by trusting the planner's own search trace on finite ensemble members. We propose an ensemble data assimilation and pre-mission rehearsal method using held-out imagined oceans. Using eight years of satellite chlorophyll-a data over the East China Sea to calibrate stale-map uncertainty, the vehicle generates 48 imagined oceans around the stale map and updates them with in-situ fluorometer samples via a localised ensemble adjustment Kalman filter. Thirty-two members are searched by a cross-entropy route planner and 16 are held out for evaluation. Before launch, a shipboard or shore computer treats 4 held-out members as synthetic truths and simulates complete 24-hour missions for five time-allocation strategies under the vehicle's actual compute speed and battery budget, selecting the strategy with the lowest mean regret. Across 422 spring bloom windows from 3,197 daily maps (2018--2026), held-out evaluation stays within 0.005 of true route value from 64 to 200,000 rollouts, GPU planning helps only when baseline compute is too slow, and stopping never pays. Across four hardware configurations on 148 test missions, rehearsal achieves time-averaged regrets of 0.265--0.276, matching development-tuned strategies (all 95\% confidence intervals of differences include zero) and reducing regret by 0.011--0.022 relative to one-step metareasoning; evaluating computation on held-out oceans within one-step metareasoning similarly removes most over-planning. These findings show that converting historical satellite ocean data into uncertainty-calibrated held-out imagined oceans curbs planner self-assessment bias either before launch or online, allowing autonomous vehicles to adapt computation allocation to onboard hardware without prior mission tuning.

\vspace{1em}
\noindent\textbf{Keywords: }Ocean big data; Autonomous underwater vehicle; Metareasoning; Data assimilation; Harmful algal bloom survey; Thinking-acting trade-off


########## ATTACHED FILE: sections/body.tex (current draft) ##########

\section{绪论}

\subsection{现场移动观测中的思考与行动权衡}

携带先验地图的移动观测平台在未知自然环境中作业时，需要在内部路线规划与外部现场采样之间分配有限的时间与能量\cite{horvitz1987reasoning, russell1991right, shen2025thinking}。野外自主平台受制于电池容量、嵌入式计算速率与固定的作业时间窗口\cite{xiao2020thinking, magnino2026metareasoning}。历史观测构成的先验底图能够给出大尺度空间分布，但因环境演变与观测盲区，底图往往滞后于现场实际状态且缺失小尺度结构\cite{fossum2019, beckers2003dineof}。若航行器仅靠低频粗糙规划维持航行，容易在复杂梯度中偏离目标核心区；反之，若频繁开启高功耗计算模块开展密集航线搜索，或关停推进器在原地重复测量以降低传感器随机误差，则会消耗本可用于推进的电能或缩减空间探索里程\cite{cuadron2025overthinking, elboher2023formal}。因此，在算力、能量与底图误差的共同约束下，何时应当继续计算、何时应当继续采样，是自主移动观测系统需要回答的基本问题\cite{hunt2021formalizing}。

当航行器边走边想时，机体机动与大脑规划虽在同一周期内并行执行，但两者仍通过电池能量消耗与先验模型不确定性紧密耦合\cite{xiao2020thinking, elboher2023formal}。维持常规巡航只需低功耗处理器在后台持续更新航线，而唤醒高功耗机载GPU开展大规模推演会抬升整机功率，缩短电池耗尽前的总巡航时间。同时，规划器的航线推演完全建立在内部环境模型之上：当底图本身存在明显的不确定性时，持续增加搜索算力能否转化为现场采样收益，取决于当前搜索深度是否已触及底图所含信息的上限\cite{jiang2015horizon, smith2006curse}。

\subsection{东海赤潮应急巡测与卫星底图的局限}

卫星遥感数据驱动的东海有害赤潮应急巡测，是检验上述思考与行动权衡的具体场景\cite{fossum2019, lou2014diurnal}。根据2023年中国海洋灾害公报，我国海域全年发现赤潮46次，累计面积约1500平方千米，其中有毒有害赤潮29次\cite{mnr2024bulletin}。在浙江近海与长江口外海域，晚春至初夏（4月下旬至6月上旬）常暴发东海原甲藻赤潮\cite{zhao2025distinguishing}，表层藻华斑块随潮汐发生往复漂移\cite{lou2014diurnal}。赤潮暴发时，应急指挥中心派出自主水下航行器（AUV）进入目标海域开展24小时巡测，要求航行器尽早找到叶绿素浓度最高的水体，并随时响应指挥中心对最浓处位置的查询\cite{fossum2019, remus100}。由于AUV在水下作业期间几乎无法与母船或岸站实时通信，航行途中的航线重规划必须全部由机载计算机独立完成。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_overview}
  \caption{海洋大数据驱动的AUV赤潮应急巡测与用时策略选择总览。中央为东海一次测试任务（2025年4月4日）的三维海洋窗口，顶面颜色表示航行器遇到的真实叶绿素浓度；图中标示了AUV及其航迹（浅蓝色为走并由低功耗处理器后台规划，橙色为开启GPU深想）以及赤潮最浓处的浅色圆环；海面块体上方为一叠想象中的海洋，最上方两个橙色边框样本留出用于评判，其余深蓝色边框样本用于规划航线。（A）海洋大数据：2018至2026年共3197天逐日2千米卫星叶绿素数据，航行器遇到的真实海洋不同于3天前的卫星图，从中切出422个赤潮季任务窗口，小尺度信息需靠现场观测获取；（B）航行器的想象：由旧图和数据标定的误差生成48个想象中的海洋，32个用来规划航线，16个留出来评判，并在出发前对五种用时策略各跑一遍预演；（C）每20分钟的选择：走、深想、停下，应急中心可随时询问最浓处位置。}
  \label{fig:overview}
\end{figure}

卫星水色遥感提供了大尺度背景场，但时间滞后与空间平滑使其无法替代AUV的现场观测\cite{beckers2003dineof, ye2021cocts}。东海春夏多云雨，业务化叶绿素产品通常利用经验正交函数插值方法填补云区盲区，生成空间连续的2千米逐日融合底图\cite{beckers2003dineof}。如图\ref{fig:overview}所示，受遥感产品处理合成与调查船奔赴作业海域航渡时间的限制，AUV出发前装入的往往是1至3天前的旧卫星图，在此期间赤潮斑块已随水体演变；此外，缺测插值平滑了小尺度结构，卫星反演与现场海水之间也存在固有偏差\cite{ye2021cocts}。因此，AUV必须把旧卫星图及历史误差统计转化为概率化的内部记忆，一边用机载荧光计沿途采样修正地图，一边合理分配计算与机动资源。

\subsection{现有控制方法的不足与本文方法}

面对计算与采样的分配问题，固定分配规则、经典单步元推理以及基于历史任务结果的学习器均存在明显局限。第一种直接做法是采用固定的用时规则（如一直走或按固定比例开启GPU深想），但固定规则无法兼顾不同的机载计算机速度与功耗：在慢计算机上一直走会因搜索不足而走弯路，在算力已够用的计算机上频繁开启高功耗GPU则会多耗电却不改善航线。第二种做法是采用人工智能中的经典单步元推理\cite{horvitz1987reasoning, russell1991right, lin2015metareasoning, sung2021quit}，在每个周期在线评估额外规划的计算收益与原位复测的信息收益；但该方法直接用规划器在搜索样本上的内部得分增量来估计计算收益，当搜索预算较大时，规划器会迎合有限样本中的随机正涨落而虚报收益，并且单步评估无法反映当前耗电对24小时全程续航的影响\cite{cuadron2025overthinking}。第三种做法是从历史巡测任务的最终表现中直接学习策略选择器\cite{magnino2026metareasoning}；但在本场景中，不同任务窗口之间的遗憾标准差约为0.13，而几种较好策略之间的平均差距不超过0.01，单次任务结果包含很大的环境背景波动。

针对上述问题，本文提出利用多年卫星数据标定底图不确定性、将航线搜索与价值评判分离，并在出发前通过完整任务预演选择用时策略的方法。全文工作包括三个部分：第一，利用2018至2026年东海3197天卫星叶绿素数据标定滞后底图误差，围绕旧图生成48个想象中的海洋并随现场观测同化更新，同时验证了深度时空预测模型无法在测试年份上改善1至3天的底图外推；第二，将48个想象中的海洋分为32个规划用样本与16个留出评判样本，消除航线搜索对有限样本的过拟合偏差；第三，在AUV下水前由母船或岸上计算机以4个留出海洋为假想真值，按机载计算机速度与电池功耗将五种用时策略各完整预演一遍，选出平均遗憾最低的策略投入实海执行，并进一步在单步元推理中检验了留出评判消除过度规划的作用机制。

\section{东海叶绿素遥感数据与底图不确定性}

\subsection{八年卫星数据集与赤潮任务窗口}

本文使用2018至2026年东海多源卫星融合叶绿素a数据集构建赤潮巡测任务窗口与先验误差统计。该数据集下载自美国国家海洋和大气管理局海岸观测网的ERDDAP服务器，融合了多颗极轨卫星水色传感器的观测，并采用经验正交函数缺失数据插值算法填补云层遮挡区\cite{beckers2003dineof}。数据空间分辨率为2千米，时间分辨率为逐日，覆盖2018年1月1日至2026年10月23日共3197天；研究区域取东海北纬$25^\circ\text{--}33^\circ$、东经$119.5^\circ\text{--}127^\circ$，每日包含$385\times 361$个网格像素。同时，为检验海表温度对叶绿素演变的辅助预测作用，本文还从美国国家海洋和大气管理局海岸观测网的ERDDAP服务器下载了美国国家航空航天局喷气推进实验室制作的多尺度超分辨率海表温度逐日无云产品（版本4.1）\cite{chin2017mur}，将其从$0.01^\circ$重采样至$0.04^\circ$。文中除特别注明外，所有叶绿素浓度、误差与遗憾均以$\log_{10}(\text{叶绿素a浓度}/\text{mg m}^{-3})$为单位。

为聚焦离岸赤潮高发场景，本文按统一条件从每年4月至6月的卫星序列中切出正方形巡测任务窗口。具体做法是在浙江外海陆架区（北纬$26.5^\circ\text{--}31.5^\circ$，东经$121.5^\circ\text{--}125^\circ$）寻找离岸至少30千米、经空间平滑后局部峰值超过$5\text{ mg/m}^3$的藻华中心，将该中心随机平移至多16千米后，截取$80\text{ km}\times 80\text{ km}$（$40\times 40$个2千米网格）的窗口；距离陆地或岛屿15千米以内的网格设为禁航区，仅保留可航行水域不少于80\%且窗内对数叶绿素极差不低于0.3的窗口。按此标准共切出422个赤潮任务窗口，其中2018至2022年的274个窗口作为开发集（用于标定误差统计和选择调好的基线策略），2023至2026年的148个窗口作为测试集。每次任务开始时，AUV从窗口边缘随机选取的一个可航行网格出发。

\subsection{底图滞后误差图谱与小尺度偏差}

航行器携带的旧卫星底图与现场真实海洋之间的差异，来自底图滞后数日内的海洋演变以及同日卫星图对小尺度结构的平滑。利用全部3197天数据计算相隔3天的对数叶绿素变化标准差，可得到四季分布图谱（图\ref{fig:atlas}）。全海域3天变化标准差的中位数在春季最高（0.127），夏季为0.107，秋季为0.103，冬季降至0.081；夏季空间差异显著，全海域90\%分位数达0.204，在浙闽沿岸与长江冲淡水锋面一带形成3天变化标准差达0.25至0.3的条带。在274个开发集任务窗口内，任务当日卫星图减去$k$天前旧图的误差统计显示：当滞后天数$k=1, 2, 3$天时，误差标准差分别为$s_1=0.125$、$s_2=0.176$与$s_3=0.210$，空间相关尺度约为$\ell=5$个网格（10千米），均值偏差分别为$+0.016$、$+0.032$与$+0.045$。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_atlas}
  \caption{东海海域（北纬$25^\circ\text{--}33^\circ$，东经$119.5^\circ\text{--}127^\circ$）全部3197天对数叶绿素3天变化标准差的四季分布图。陆地标为灰色；春季子图中的圆点为切出的赤潮任务窗口位置，蓝色为2018至2022年开发集（274个），绿色为2023至2026年测试集（148个）。}
  \label{fig:atlas}
\end{figure}

即便是任务当天的缺测填补卫星图，也与现场海水存在小尺度差异\cite{beckers2003dineof, ye2021cocts}。针对海洋一号丙星水色传感器在东海与南海的现场验证表明，卫星反演叶绿素与实测值之间的无偏相对百分比差异约为39\%（折合对数空间约0.15）\cite{ye2021cocts}。因此，仿真环境在任务当日卫星图上叠加一个标准差为$s_{\text{sat}}=0.15$、空间相关尺度为3个网格（6千米）的高斯随机场来生成航行器遇到的真实海洋，并在参数扫描实验中将$s_{\text{sat}}$在0.05至0.3之间变化。

\subsection{时空预测模型的检验}

为检验能否用深度学习模型在出发前将旧卫星图向前推演以减小滞后误差，本文训练了一个含550万参数的联合嵌入预测架构模型\cite{assran2025vjepa2}。该模型以过去3天的叶绿素a和海表温度异常场为输入，使用2018至2021年3月至6月数据训练并在2022年数据上验证（验证集均方根误差仅比直接沿用最新底图低1.4\%）；但在2023至2026年测试集上，模型提前1、2、3天预报缺测填补叶绿素图的均方根误差分别为0.1229、0.1439与0.1487（集合离散度与误差之比为0.70至0.93），并未优于直接将最新可用卫星图作为预报值的基线（0.1226、0.1439与0.1474），说明无法靠日均卫星图的时间外推恢复小尺度信息，必须依靠AUV现场观测。

\section{随水漂移参考系下的采样与决策模型}

\subsection{随水漂移参考系与评价指标}

本文假设斑块随表层水体一同移动，并将AUV运动、叶绿素场与数据同化全部建立在随表层水体漂移的参考系中。这一假设的依据在于，静止轨道卫星对2011年5月东海一次赤潮的逐时连续追踪表明，表层藻华斑块主要随潮汐与表层水体发生往复漂移\cite{lou2014diurnal}。在随表层水体漂移的参考系下，赤潮斑块相对于水体不移动，AUV无需逆流追赶斑块，而海流的作用则体现在卫星图滞后期间的演变统计中。

在由$40\times 40$个2千米网格组成的任务窗口内，记网格$\mathbf{x}$处的真实对数叶绿素浓度为$c(\mathbf{x})$。在$T=24\text{ h}$的任务窗口内，应急指挥中心可随时询问最浓处在哪里；AUV从截至时刻$t$已实际造访的网格集合$\mathcal{V}(t)$中，选出内部集合均值$\bar{c}_t(\mathbf{x})$最高的位置作为回答：
\begin{equation}
  \hat{\mathbf{x}}(t) = \arg\max_{\mathbf{x}\in\mathcal{V}(t)} \bar{c}_t(\mathbf{x})
  \label{eq:answer}
\end{equation}
任务在满24小时或电池耗尽时结束，结束后的回答保持不变。定义24小时时间平均遗憾$R$为评价指标（越低越好）：
\begin{equation}
  R = \frac{1}{T}\int_0^T \left[\max_{\mathbf{x}} c(\mathbf{x}) - c\big(\hat{\mathbf{x}}(t)\big)\right] dt
  \label{eq:regret}
\end{equation}

\subsection{航行器功耗模型与二十分钟决策周期}

航行器机电参数参照百米级轻型AUV\cite{remus100}与嵌入式边缘GPU模块\cite{jetsonorinnx}设定。AUV对水巡航速度为$1.5\text{ m/s}$（约3节），携带$1\text{ kWh}$电池，在3节航速下续航约22小时，对应巡航总功率$45\text{ W}$，其中基础航电功率$15\text{ W}$（含导航、传感器及常驻后台运行的低功耗处理器），推进功率$30\text{ W}$。机载嵌入式GPU模块（功率范围$10\text{--}25\text{ W}$，基准设定取$+20\text{ W}$，省电加速器设定取$+5\text{ W}$）用于深度航线规划，其推演速度为低功耗处理器的50倍。由于本文的折线规划器与二维表层场是对真实水下三维路径评估（需计入海流、深度与安全约束）的简化替代，决定规划质量的是计算机相对于规划问题的速度；因此实验以“每分钟想象推演次数”度量低功耗处理器速度，并在5至200次/分的范围内变化。

整个24小时任务按每段20分钟划分为连续的决策周期。在每个20分钟周期内，AUV的机体与大脑并行动作\cite{xiao2020thinking, elboher2023formal}：
\begin{itemize}
  \item \textbf{机体动作：}选择“走”时，开启推进器（$30\text{ W}$）沿当前航线以$1.5\text{ m/s}$航行，20分钟走过$1.8\text{ km}$（不足一个2千米网格），机载荧光计每走$1\text{ km}$采样1次，每周期获得约2个样本；在电池允许时，24小时可航行约$120\text{--}130\text{ km}$，约能横穿80千米窗口1.5次。选择“停下”时，关停推进器（推进功率$0\text{ W}$，仅耗电$15\text{ W}$）随水漂流，荧光计每4分钟对同一水体采样1次，每周期获得5个样本。每次独立采样的观测模型为：
  \begin{equation}
    y = c(\mathbf{x}) + \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, 0.1^2)
    \label{eq:obs}
  \end{equation}
  \item \textbf{大脑规划：}维持低功耗处理器后台规划（额外功耗$0\text{ W}$），或开启GPU“深想”（额外功耗$+20\text{ W}$或$+5\text{ W}$，推演速度提高至50倍）。新航线以AUV在当前20分钟周期结束时的预计位置为起点进行计算（时延补偿），并在周期结束时替换旧航线。
\end{itemize}

\section{想象中的海洋与出发前预演方法}

\subsection{想象中的海洋与现场观测同化}

航行器在内部维护48个“想象中的海洋”来表达对叶绿素分布的先验认识与当前记忆。出发前，围绕滞后$k$天的卫星图$c_{\text{map}}(\mathbf{x})$生成48个样本：
\begin{equation}
  c^{(i)}(\mathbf{x}) = c_{\text{map}}(\mathbf{x}) + \sigma_k\, z^{(i)}(\mathbf{x}), \quad i = 1, \dots, 48
  \label{eq:prior}
\end{equation}
其中$\sigma_k = \sqrt{s_k^2 + s_{\text{sat}}^2}$为合成先验标准差（当$k=3$天、$s_3=0.210$、$s_{\text{sat}}=0.15$时，$\sigma_3 \approx 0.26$），$z^{(i)}(\mathbf{x})$为具有平方指数空间相关结构（相关长度$\ell = 5$个网格，即10千米）的独立标准高斯随机场。

巡测过程中，每当荧光计获得一个样本$y$，AUV采用序列集合调整卡尔曼滤波\cite{anderson2001eakf}更新全部48个想象中的海洋。为消除小集合在远距离网格间产生的伪相关，更新时乘以半宽为$2\ell$（10个网格，20千米）的五阶分段有理局地化函数\cite{gaspari1999correlation}，使单点观测仅修正周围空间相关范围内的水体估计。

\subsection{规划搜索与留出评判分离}

在每个20分钟周期内，规划器通过想象推演寻找连接当前周期终点与两个中间航路点的折线航线。将一条候选航线在单个想象海洋$c^{(i)}$上模拟航行一次称为一次想象推演：记沿该航线航行至剩余任务时刻$\tau \in [0, T_{\text{left}}]$时所遇最高叶绿素浓度为$m_i(\tau)$（以当前已访最佳估计为初值，当可用巡航电池时间耗尽后保持冻结），则该航线在样本$i$上的价值定义为剩余窗口内的时间均值：
\begin{equation}
  V_i = \frac{1}{T_{\text{left}}}\int_0^{T_{\text{left}}} m_i(\tau)\, d\tau
  \label{eq:route_value}
\end{equation}
这一定义直接对应式\eqref{eq:regret}的时间平均遗憾目标：越早到达浓水区，$V_i$越高。规划器采用周期之间热启动的交叉熵方法\cite{deboer2005cem}搜索航路点。

当规划器在有限个想象海洋上搜索航线时，若同时用这批样本的平均得分来评判航线好坏，就会受到“优化器诅咒”的影响\cite{smith2006curse, vanhasselt2010double}。其原因在于，当推演次数大幅增加时，优化器能够精细调整航路点位置，使折线恰好穿过这批特定样本中偶然重合的随机高值点；此时规划器看到的内部自评得分会随推演次数增加而持续上升，但在未参与搜索的真实海洋中，这种针对样本随机涨落的微调并不提高实际收益。为此，本文将48个想象中的海洋固定分为两组（图\ref{fig:overview}B）：32个作为规划用海洋，供交叉熵规划器搜索并选出均值最高的航线；其余16个作为留出海洋，它们同样随现场观测同化更新，但从不参与航线搜索。当先验底图不确定性经数据如实标定时，留出海洋能够对选出的航线给出近乎无偏的价值评判。

\subsection{出发前预演控制器与对比基线}

为在全任务周期尺度上权衡走、深想与停下，本文定义了五种候选时间分配策略：（1）一直走：全程巡航采样，仅用低功耗处理器后台规划；（2）一直深想：全程巡航采样，同时每周期开启GPU深想；（3）三段深想一段：全程巡航采样，每3个周期中开启1个周期GPU深想；（4）三段停下深想一段：每3个周期中有1个周期停下漂流并开启GPU深想，其余2个周期走并用后台规划；（5）三段停下复测一段：每3个周期中有1个周期停下漂流原位复测且仅用后台规划，其余2个周期走并用后台规划。

在AUV下水前，当航行器仍位于母船甲板或岸站并保持有线连接时，母船或岸上计算机运行“出发前预演”来选定本次任务的策略。预演程序从16个留出海洋中取出4个样本$\{c^{(j)}\}_{j=1}^4$作为假想的“真实海洋”；对每个假想真值$c^{(j)}$和五种策略中的每一种策略$s$，按AUV自身的规划器、机载计算机速度与$1\text{ kWh}$电池模型完整模拟一遍24小时巡测任务，得到假想遗憾$R_{s,j}$。五种策略在同一个假想真值上使用相同的初始集合与观测噪声序列，最后选出4个假想真值上平均遗憾最低的策略执行：
\begin{equation}
  s^* = \arg\min_{s} \frac{1}{4}\sum_{j=1}^4 R_{s,j}
  \label{eq:rehearsal}
\end{equation}
出发前预演模拟的是机载计算机的速度与功耗，但其本身运行在母船或岸上计算机上，无法在机载计算机上直接运行：以慢计算机和快计算机配置为例，单次任务预演分别需约190万次和3700万次想象推演（慢计算机配置若在AUV自身的GPU上运行需耗时约125小时），而在普通台式机单个处理器核心上，慢、中、快三种计算机配置的单次任务预演仅分别耗时4.6秒、7.8秒与约25秒。

实验将出发前预演与四类基线对比：（1）上述五种固定策略；（2）调好的固定策略，即针对每一种硬件配置，先在2018至2022年120个开发集窗口上找出平均遗憾最低的固定策略，再用于测试集（该基线需要该型航行器的历史任务数据，而出发前预演不需要）；（3）单步元推理\cite{russell1991right}，在每个周期根据规划器在规划用海洋上的搜索改进轨迹估计计算价值，并通过想象海洋上的预后验分析估计采样信息价值；（4）规划用海洋上的出发前预演对照，其流程与式\eqref{eq:rehearsal}相同，但4个假想真值取自32个规划用海洋。

\section{实验结果与分析}

\subsection{规划预算与留出海洋评判的准确性}

在80个开发集窗口（每窗口3个随机种子，3天前卫星图，任务前8小时）上的预算扩展实验表明，留出的想象海洋能够消除规划器的自评高估并准确反映航线价值的饱和过程（图\ref{fig:curse}）。当每次决策的想象推演次数从64次增至2000次再增至200,000次（跨度约三个半数量级）时，所选航线在真实海洋中的价值从0.749升至0.793，随后平缓收敛至0.803；规划器在32个规划用海洋上的搜索自评得分则从0.762升至0.833并继续攀升至0.917，在最高预算下比真实值高出0.114。相比之下，同一批航线在16个留出海洋上的评判均值分别为0.745、0.794与0.802，当底图不确定性经数据标定时，在所有预算下与真实价值之差均在0.005以内（图\ref{fig:curse}b蓝色虚线）。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_curse}
  \caption{每次决策的想象推演次数从64次增至200,000次时的航线价值与评判偏差（80个开发集窗口$\times 3$个种子，3天前卫星图）。（a）航线的时间平均最佳浓度（折算为$\text{mg/m}^3$）：规划器搜索时的自评（红线）随推演次数持续上升，留出的想象海洋上的评价（蓝色虚线）与真实海洋中的结果（黑线）在约2000次后一同趋于平缓，阴影带表示任务间的离散度；（b）估计减去真实的对数浓度偏差：不确定性如实标定时留出评价保持在0附近（蓝色虚线），不确定性设大到1.5倍（橙色点线）或设小一半（浅蓝色点线）时分别产生约$+0.07$与$-0.06$的平移。}
  \label{fig:curse}
\end{figure}

即便先验不确定性幅值标定存在偏差，留出海洋对增加算力所获相对提升的判断依然稳健（图\ref{fig:curse}b）。当人为将先验标准差设小一半或设大到1.5倍时，留出评价虽分别产生$-0.06$（浅蓝色点线）与$+0.07$（橙色点线）的整体偏移，但推演次数从64次增至200,000次时留出评价估计的增益（$+0.059$与$+0.054$）仍与真实海洋中的实际增益（$+0.054$与$+0.047$）接近。

\subsection{算力与底图误差相图及典型任务分析}

在低功耗处理器速度（每分钟5至200次推演）与真实海洋偏离卫星图程度（0.05、0.15、0.30）构成的18格二维网格（每格60个开发集任务）上，五种固定策略的表现呈现出清晰的相图分界（图\ref{fig:phase}）。首先，开启GPU深想仅在基础算力相对于规划问题过慢时才显著优于“一直走”（图\ref{fig:phase}a）：在最慢的计算机（5次/分）上，后台每20分钟仅完成100次推演，远低于图\ref{fig:curse}a中约2000次的饱和区，此时“三段深想一段”（单次深想推演5000次）显著优于“一直走”，且底图越不准，深想收益越大，当偏离程度为0.05、0.15与0.30时配对遗憾差值分别为$-0.086$、$-0.109$与$-0.138$；在10次/分且偏离0.15的格点上仅存在微弱优势（差值$-0.017$，95\%置信区间$[-0.035, -0.001]$）；从20次/分起（后台每20分钟推演400次以上），所有格点中均无任何固定策略显著优于“一直走”（图\ref{fig:phase}a灰色“$\approx$”区域），而“一直走”自身的绝对遗憾则随底图偏离程度增大而上升（在20次/分下，偏离0.05、0.15与0.30时的平均遗憾分别为0.273、0.342与0.495）。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_phase}
  \caption{低功耗计算机速度（5、10、20、50、100、200次推演/分钟）与真实海洋偏离卫星图程度（0.05、0.15、0.30）网格上的固定策略相图（每格60个开发集任务）。（a）最好的固定策略相对“一直走”的时间平均遗憾差值：仅在配对差值的95\%置信区间低于0时标出显著优于“一直走”的策略颜色（橙色为“三段深想一段”）及差值，灰色“$\approx$”表示无策略显著优于“一直走”；（b）两个停下类策略中较好者比不停的最好策略多出的遗憾（正值表示停下带来损失）。}
  \label{fig:phase}
\end{figure}

其次，在全部18个格点的算力与底图误差组合下，两个停下类策略中较好者的表现均显著劣于不停的最好策略，多出的遗憾达$+0.063$至$+0.118$，所有格点的95\%置信区间均高于0（图\ref{fig:phase}b）。从采样几何与不确定性尺度可以解释这一现象：AUV以$1.5\text{ m/s}$航行20分钟走过$1.8\text{ km}$并采集约2个样本，而停下漂流20分钟对同一水体采集5个样本；在原地重复采样5次虽能将该点处的测量误差从单次$0.1$压低至约$0.1/\sqrt{5}\approx 0.045$，但决定回答质量的瓶颈是尚未造访水域的高先验不确定性（标准差约$0.26$），且将三分之一的时间用于停下会使航行器更晚到达浓水区，从而受到时间平均遗憾的惩罚。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_example}
  \caption{一次测试集任务（2023年4月15日，慢计算机5次/分）中两种策略的对比。（a）航行器携带的3天前卫星图，东侧边缘白色三角形为起点；（b）真实海洋及“一直走”（蓝线）与“三段深想一段”（橙线）的航迹，西南角五角星为真实最浓处；（c）24小时内应急中心随时得到的答案误差，“一直走”停留在0.4附近（平均0.43），“三段深想一段”在约19小时后到达真实最浓处（误差降至0，平均0.31）。}
  \label{fig:example}
\end{figure}

图\ref{fig:example}展示了按日期顺序第一个策略差距超过0.1的测试集任务实例（2023年4月15日，慢计算机）。AUV从东侧边缘（白色三角形）出发；3天前的卫星图在东北部浓度较低，向西和西南方向浓度较高（图\ref{fig:example}a），而真实最浓处位于西南角（图\ref{fig:example}b五角星）。在慢计算机上，“一直走”（蓝线）向西南航行至窗口中部后便在中部来回移动，其回答误差一直停留在0.4左右，24小时平均遗憾为0.43（图\ref{fig:example}c）；“三段深想一段”（橙线）则直接横穿窗口驶向西南角，在约19小时后到达真实最浓处（回答误差降至0），24小时平均遗憾降至0.31。

\subsection{不同硬件平台上的控制器对比}

在2023至2026年全部148个测试任务窗口上，表\ref{tab:main}对比了四种硬件配置下各控制方式的表现。按120个开发集窗口选出的“调好的”固定策略随硬件而异：慢计算机（5次/分，$+20\text{ W}$）与中等计算机（20次/分，$+20\text{ W}$）上均为“三段深想一段”（测试集遗憾分别为0.270与0.269），快计算机（100次/分，$+20\text{ W}$）上为“一直走”（开发集0.298优于“三段深想一段”0.299与“一直深想”0.310，测试集0.267），省电加速器（20次/分，GPU功耗仅$+5\text{ W}$）上则为“一直深想”（开发集0.292优于“三段深想一段”0.296与“一直走”0.299，测试集0.267）。在测试集上，除慢计算机上“一直走”遗憾高达0.374（比调好策略高$+0.104$）外，其余三种硬件配置下持续航行的三种策略（一直走、一直深想、三段深想一段）之间的平均遗憾差距均不超过0.003，处于统计噪声范围内（例如中等计算机上“一直走”减去调好策略为$-0.002$，95\%置信区间为$[-0.010, +0.005]$）；而包含停下动作的两种策略在全部四种硬件上均比调好策略差$+0.059$至$+0.138$。

\begin{table}[htbp]
  \centering
  \caption{2023至2026年148个测试集任务（3天前卫星图，真实海洋偏离0.15，传感器误差0.1）上各控制方式的时间平均遗憾（越低越好）。“调好的”指在该型航行器的120个开发集任务上表现最好的固定策略；括号内为相对于“调好的”策略的差值，方括号内为按赤潮周自助重采样得到的95\%置信区间。}
  \label{tab:main}
  \input{tables/main_table.tex}
\end{table}

经典单步元推理在慢、中、快计算机与省电加速器上的时间平均遗憾分别为0.287、0.287、0.282与0.278，比各硬件调好的策略分别高出$+0.017$、$+0.018$、$+0.015$与$+0.011$（表\ref{tab:main}）。单步元推理利用规划器在搜索样本上的内部改进轨迹评估计算价值，并通过想象海洋上的预后验分析评估原位复测价值；在四种硬件上，它分别在80\%、93\%（其中63\%边走边想，30\%停下深想）、97\%与94\%的周期内开启GPU深想，并分别有34\%、33\%、33\%与33\%的周期处于停下漂流状态，损耗了巡航时间与电池能量。

本文提出的留出海洋出发前预演在四种硬件上分别取得0.276、0.265、0.268与0.266的时间平均遗憾，相对于各硬件调好策略的差值分别为$+0.007$（$[-0.001, +0.014]$）、$-0.003$（$[-0.009, +0.003]$）、$+0.002$（$[-0.005, +0.008]$）与$-0.001$（$[-0.006, +0.005]$），95\%置信区间均包含0；与单步元推理作配对比较，出发前预演减去单步元推理的遗憾差值分别为$-0.011$（$[-0.019, -0.002]$）、$-0.022$（$[-0.030, -0.013]$）、$-0.013$（$[-0.020, -0.007]$）与$-0.012$（$[-0.019, -0.004]$），置信区间全部位于0以下。对慢计算机全部148个测试任务重新运行预演，所得每次任务的遗憾与首次运行完全一致，验证了实验的精确可重复性。从选出的策略比例看，出发前预演能够随硬件特征自适应调整：在“一直走”代价高昂的慢计算机上，预演选出“三段深想一段”占55\%、“一直深想”占39\%、“一直走”仅占1\%、停下类策略占4\%；随着基础算力提高，“一直走”的入选比例从慢计算机的1\%升至中等计算机的30\%（“三段深想一段”43\%、“一直深想”25\%、停下类1\%）和快计算机的47\%（“三段深想一段”28\%、“一直深想”22\%、停下类3\%）；而在GPU功耗降至$+5\text{ W}$的省电加速器上，预演最常选择“一直深想”（43\%，“三段深想一段”35\%、“一直走”20\%、停下类1\%）。

对比表\ref{tab:main}最后两行可见，用规划用海洋作为假想真值的预演对照在四种硬件上的平均遗憾（0.273、0.268、0.271、0.265）与留出海洋预演接近，两者在全测试集上选出各策略的总体比例也几乎相同（如中等计算机上三种不停策略占比分别为43\%/30\%/25\%与44\%/32\%/23\%），但在单个具体任务上，两种预演选出同一策略的比例仅为37\%至41\%（慢、中、快计算机与省电加速器上分别为41\%、38\%、37\%与39\%），与按上述总体比例独立随机抽取两次的一致率相当。这一结果揭示了出发前预演能够做到与不能做到的事：预演在所有硬件上几乎不选停下类策略（1\%至4\%），并在慢计算机上避开了“一直走”（1\%），从而消除了劣质选项、实现了对航行器硬件的适配（在慢计算机上，从五种策略或三种不停策略中均匀随机选取的平均遗憾分别为0.331与0.306，预演降至0.276；在中等计算机上，五种策略均匀随机为0.293，预演降至0.265）。然而，在真实平均差距不超过0.01（除慢计算机外不超过0.003）的三种持续航行策略之间，由于任务间遗憾标准差（约0.13）远大于策略间的真实差异，仅靠出发前4个假想真值的预演无法分辨单次任务的最优策略，其单任务选择表现与在三种不停策略间随机抽取相当（中等计算机与省电加速器上三种不停策略随机抽取遗憾分别为0.268与0.267；中等计算机上预演所选策略平均比该任务事后最优固定策略差0.022，若事后针对每个任务挑出最佳固定策略，慢、中计算机与省电加速器的遗憾可分别达0.250、0.243与0.242）。此外，预演内部假想任务的遗憾比真实海洋普遍高出0.05至0.07，但因该偏移对各候选策略相同，不影响剔除劣质策略的排序。

\subsection{留出评判消除过度规划的机制检验}

为直接检验第5.1节的规划自评偏差是否是导致第5.3节单步元推理过度规划的主要原因，本文在慢计算机与中等计算机的148个测试任务（保持相同随机种子）上测试了改用留出评判的单步元推理：保持单步元推理其余流程不变，仅将“多想一步的计算收益”和“原位复测的信息收益”改为在16个留出想象海洋上评判（即在32个规划用海洋上搜索选出航线、在16个留出海洋上评估其价值，对应双估计思想\cite{vanhasselt2010double}）。

实验结果显示，改用留出评判后，单步元推理开启GPU深想的周期比例在慢计算机上从80\%大幅降至30\%，在中等计算机上从93\%降至38\%；处于停下漂流状态的周期比例分别从34\%降至17\%和从33\%降至17\%（均减少一半）。相应地，其时间平均遗憾在慢计算机上从0.287降至0.278（配对差值$-0.009$，95\%置信区间$[-0.018, +0.000]$），在中等计算机上从0.287降至0.270（配对差值$-0.017$，95\%置信区间$[-0.025, -0.009]$）；与出发前预演相比，修正后的单步元推理在慢、中计算机上的配对差值分别为$+0.002$（$[-0.007, +0.010]$）与$+0.005$（$[-0.003, +0.011]$），置信区间均包含0。这证实经典单步元推理的过度计算主要源于用规划用海洋上的自评得分衡量计算价值；改在留出海洋上评判即可消除大部分过度规划（剩余17\%的停下周期仍带来少量损失）。由此可见，本文两种有效控制器共享同一核心机制——在未参与搜索的留出想象海洋上评判计算的价值：出发前预演在任务下水前将这一准则用于完整任务尺度，而修正后的单步元推理则在航行途中将其用于每个20分钟控制周期。

\section{结论}

本文依托2018至2026年东海3197天多源融合卫星叶绿素数据与422个春季赤潮任务窗口，研究了携带滞后卫星图的AUV在巡测中如何权衡走、深想与停下复测的时间与能量。主要结论如下：
\begin{enumerate}
  \item 深度时空预测模型在测试年份上对1至3天缺测填补叶绿素图的预报精度未超过直接沿用最新卫星图，小尺度藻华结构必须依靠AUV现场采样获取。
  \item 将内部集合划分为32个规划用海洋与16个留出海洋可有效消除优化器诅咒：当单次决策推演次数从64次增至200,000次时，规划用海洋上的搜索自评得分因迎合样本噪声而持续攀升，而在先验不确定性经数据标定时，留出海洋上的评判均值在所有预算下与真实航线价值之差均不超过0.005。
  \item 在未参与搜索的留出想象海洋上评判计算价值，是抑制过度计算的核心机制。开启高功耗GPU深想仅在基础算力过慢（5次/分）时显著优于“一直走”，中途停下复测在所有算力与底图误差下均造成0.06至0.14的遗憾损失。出发前预演在任务尺度上应用留出评判，能够避开停下策略并在慢计算机上避开“一直走”，从而在无需历史任务调参的条件下适配四种硬件配置（与调好策略之差的95\%置信区间均包含0，且比经典单步元推理低0.011至0.022）；将留出评判按周期引入单步元推理同样能将深想比例从80\%—93\%压低至30\%—38%，达到与出发前预演相当的遗憾水平。
\end{enumerate}

本研究仍存在以下局限：（1）随表层水体漂移的参考系忽略了80千米窗口内的水平流剪切与藻华昼夜垂直迁移；（2）仿真中的“真实海洋”是在任务当日卫星图上叠加按发表文献标定的空间相关随机场生成的，并非现场实测真值；（3）二维表层场上的双航路点折线规划器是对真实水下三维路径规划的简化替代，因此机载算力需按相对于规划问题的推演速度来表征；（4）出发前预演需在AUV下水前依赖母船或岸基计算机运行，且仅在出发前执行一次而未在任务中途重选策略；（5）受任务间较大环境波动（标准差约0.13）的限制，4个假想真值的预演仅能实现针对硬件平台的策略适配，无法在真实差距不超过0.01的几种持续航行策略间做出优于随机的单任务选择（中等计算机上事后逐任务最优选择的遗憾为0.243，而预演为0.265）。后续工作将结合三维海流预报集合与实海观测数据，进一步探讨多台航行器协同巡测中的在线计算与采样分配问题。


########## ATTACHED FILE: sections/appendix.tex (current draft) ##########

\section{代码与数据说明}

本研究的数据处理、集合同化、航线规划器、时空预测模型、出发前预演与论文图表的完整代码、原始实验结果数据，以及学生与Claude的研究讨论对话记录（已隐去涉及学生其他未发表工作的内容）均开源于：\TBD{GitHub 仓库地址}。

实验使用的两套卫星遥感数据集均下载自美国国家海洋和大气管理局海岸观测网（NOAA CoastWatch）的ERDDAP服务器：
\begin{enumerate}
  \item \textbf{东海多源融合叶绿素a逐日数据集（2018—2026年）：} 融合了S-NPP与NOAA-20卫星上的VIIRS传感器以及Sentinel-3A卫星上的OLCI传感器观测，并经DINEOF方法填补云区盲区，空间分辨率2千米，时间分辨率逐日，遵循CC0开放许可，数据集标识为\texttt{noaacwNPPN20S3ASCIDINEOF2kmDaily}。
  \item \textbf{多尺度超分辨率海表温度数据集（2018—2026年）：} 由美国国家航空航天局喷气推进实验室（NASA JPL）制作（MUR v4.1），原始空间分辨率$0.01^\circ$，时间分辨率逐日，数据集标识为\texttt{jplMURSST41}。
\end{enumerate}

\section{人工智能工具使用说明}

在本课程论文的研究与写作过程中，人工智能工具的使用情况与各环节分工如下：
\begin{enumerate}
  \item 学生提出了本文的研究问题（海洋航行器在巡测过程中何时应当继续计算、何时应当继续观测），设定了研究方向与各项要求，并对提交的论文承担全部责任。
  \item Claude（Anthropic）完成了文献调研，与学生讨论细化了选题，编写了实验代码，运行了全部数值实验并绘制了论文图表。
  \item Gemini（Google）根据Claude整理的实验事实清单撰写了论文初稿与修改稿的文字。
  \item Claude对照实验结果与原始文献逐一核查了文中的全部数值与文献引用。
\end{enumerate}
```

</details>

## Gemini 的回复

<details><summary>展开（共 21036 字符）</summary>

```
===== FILE: sections/title.tex =====
基于想象海洋出发前预演的自主水下航行器思考与行动权衡研究

===== FILE: sections/subtitle.tex =====
——以八年卫星叶绿素数据驱动的东海赤潮应急巡测为例

===== FILE: sections/abstract.tex =====
\section*{摘\quad 要}
\addcontentsline{toc}{section}{摘要}

携带卫星先验底图的自主水下航行器（AUV）在现场巡测时受机载算力、电池与作业时间制约。因卫星图存在数日滞后与小尺度平滑偏差，航行器需在每个控制周期权衡：开启高功耗图形处理器（GPU）深想、靠低功耗规划继续走并采样，或停下随水漂流复测。固定规则难以适应不同硬件，单步元推理则会因规划器在有限样本上的过拟合而高估计算价值。本文提出基于留出想象海洋的集合同化与出发前预演方法：利用八年东海卫星叶绿素数据标定底图误差，围绕旧图生成48个想象海洋并随采样同化更新，32个用于规划航线，16个留出用于评判；下水前由母船或岸上计算机以4个留出海洋为假想真值，按机载算力与功耗模拟五种用时策略的24小时任务并择优。在2018至2026年东海3197天数据构建的422个赤潮窗口上的实验表明：留出评判在64至200,000次推演下与真实价值之差不超过0.005；深想仅在基础算力过慢时有益，停下始终不划算；在四种硬件、148个测试任务上，预演遗憾为0.265至0.276，与调好策略之差的95\%置信区间均包含0，且比单步元推理低0.011至0.022；改用留出评判的单步元推理同样消除了大部分过度规划。这表明将海洋遥感大数据转化为留出想象海洋可抑制计算自评偏差，使航行器无需历史任务调参即可适配机载算力与观测约束。

\vspace{1em}
\noindent\textbf{关键词：}海洋大数据；自主水下航行器；元推理；数据同化；赤潮巡测；计算与行动权衡

\clearpage
\section*{Abstract}
\addcontentsline{toc}{section}{Abstract}

Autonomous underwater vehicles (AUVs) carrying satellite prior maps must trade off computation against movement under onboard processor, battery, and mission-time constraints. Because satellite maps are several days old and smooth out small-scale features, the vehicle must decide at every control interval whether to activate a high-power graphics processing unit (GPU) to plan deeply, continue cruising and sampling under low-power background planning, or stop propulsion to drift and resample locally. Fixed time-allocation rules do not generalise across hardware platforms, while classic one-step metareasoning overestimates the value of computation by trusting the planner's own search trace on finite ensemble members. We propose an ensemble data assimilation and pre-mission rehearsal method using held-out imagined oceans. Using eight years of satellite chlorophyll-a data over the East China Sea to calibrate stale-map uncertainty, the vehicle generates 48 imagined oceans around the stale map and updates them with in-situ fluorometer samples via a localised ensemble adjustment Kalman filter. Thirty-two members are searched by a cross-entropy route planner and 16 are held out for evaluation. Before launch, a shipboard or shore computer treats 4 held-out members as synthetic truths and simulates complete 24-hour missions for five time-allocation strategies under the vehicle's actual compute speed and battery budget, selecting the strategy with the lowest mean regret. Across 422 spring bloom windows from 3,197 daily maps (2018--2026), held-out evaluation stays within 0.005 of true route value from 64 to 200,000 rollouts, GPU planning helps only when baseline compute is too slow, and stopping never pays. Across four hardware configurations on 148 test missions, rehearsal achieves time-averaged regrets of 0.265--0.276, matching development-tuned strategies (all 95\% confidence intervals of differences include zero) and reducing regret by 0.011--0.022 relative to one-step metareasoning; evaluating computation on held-out oceans within one-step metareasoning similarly removes most over-planning. These findings show that converting historical satellite ocean data into uncertainty-calibrated held-out imagined oceans curbs planner self-assessment bias either before launch or online, allowing autonomous vehicles to adapt computation allocation to onboard hardware without prior mission tuning.

\vspace{1em}
\noindent\textbf{Keywords: }Ocean big data; Autonomous underwater vehicle; Metareasoning; Data assimilation; Harmful algal bloom survey; Thinking-acting trade-off

===== FILE: sections/body.tex =====
\section{绪论}

\subsection{现场移动观测中的思考与行动权衡}

携带先验地图的移动观测平台在未知自然环境中作业时，需要在内部路线规划与外部现场采样之间分配有限的时间与能量\cite{horvitz1987reasoning, russell1991right, shen2025thinking}。野外自主平台受制于电池容量、嵌入式计算速率与固定的作业时间窗口\cite{xiao2020thinking, magnino2026metareasoning}。历史观测构成的先验底图能够给出大尺度空间分布，但因环境演变与观测盲区，底图往往滞后于现场实际状态且缺失小尺度结构\cite{fossum2019, beckers2003dineof}。即使机体机动与低功耗后台规划并行执行，若航行器仅靠粗糙规划维持巡航，仍易在复杂梯度中偏离目标核心区；反之，若频繁唤醒高功耗GPU开展密集航线搜索，或关停推进器在原地重复测量以降低传感器随机误差，则会消耗推进电能、缩短总巡航时间或缩减空间探索里程\cite{cuadron2025overthinking, elboher2023formal}，且持续增加搜索算力能否转化为现场收益还受底图自身信息上限的制约\cite{jiang2015horizon, smith2006curse}。因此，在算力、能量与底图误差的共同约束下，何时应当继续计算、何时应当继续采样，是自主移动观测系统需要回答的基本问题\cite{hunt2021formalizing}。

\subsection{东海赤潮应急巡测与卫星底图的局限}

卫星遥感数据驱动的东海有害赤潮应急巡测，是检验上述思考与行动权衡的具体场景\cite{fossum2019, lou2014diurnal}。根据2023年中国海洋灾害公报，我国海域全年发现赤潮46次，累计面积约1500平方千米，其中有毒有害赤潮29次\cite{mnr2024bulletin}。在浙江近海与长江口外海域，晚春至初夏常暴发东海原甲藻赤潮（2021年与2023年记录均在4月下旬至6月上旬）\cite{zhao2025distinguishing}，表层藻华斑块随潮汐发生往复漂移\cite{lou2014diurnal}。赤潮暴发时，应急指挥中心派出自主水下航行器（AUV）进入目标海域开展24小时巡测，要求航行器尽早找到叶绿素浓度最高的水体，并随时响应指挥中心对最浓处位置的查询\cite{fossum2019, remus100}。由于AUV在水下作业期间几乎无法与母船或岸站实时通信，航行途中的航线重规划必须全部由机载计算机独立完成。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_overview}
  \caption{海洋大数据驱动的AUV赤潮应急巡测与用时策略选择总览。中央为东海一次测试任务（2025年4月4日）的三维海洋窗口，顶面颜色表示航行器遇到的真实叶绿素浓度；图中标示了AUV及其航迹（浅蓝色为走并由低功耗处理器后台规划，橙色为开启GPU深想）以及赤潮最浓处的浅色圆环；海面块体上方为一叠想象中的海洋，最上方两个橙色边框样本留出用于评判，其余深蓝色边框样本用于规划航线。（A）海洋大数据：2018至2026年共3197天逐日2千米卫星叶绿素数据，航行器遇到的真实海洋不同于3天前的卫星图，从中切出422个赤潮季任务窗口，小尺度信息需靠现场观测获取；（B）航行器的想象：由旧图和数据标定的误差生成48个想象中的海洋，32个用来规划航线，16个留出来评判，并在出发前对五种用时策略各跑一遍预演；（C）每20分钟的选择：走、深想、停下，应急中心可随时询问最浓处位置。}
  \label{fig:overview}
\end{figure}

卫星水色遥感提供了大尺度背景场，但时间滞后与空间平滑使其无法替代AUV的现场观测\cite{beckers2003dineof, ye2021cocts}。东海春夏多云雨，业务化叶绿素产品通常利用经验正交函数插值方法填补云区盲区，生成空间连续的2千米逐日融合底图\cite{beckers2003dineof}。如图\ref{fig:overview}所示，受遥感产品处理合成与调查船奔赴作业海域航渡时间的限制，AUV出发前装入的往往是1至3天前的旧卫星图，在此期间赤潮斑块已随水体演变；此外，缺测插值平滑了小尺度结构，卫星反演与现场海水之间也存在固有偏差\cite{ye2021cocts}。因此，AUV必须把旧卫星图及历史误差统计转化为概率化的内部记忆，一边用机载荧光计沿途采样修正地图，一边合理分配计算与机动资源。

\subsection{现有控制方法的不足与本文方法}

面对计算与采样的分配问题，固定分配规则、经典单步元推理以及基于历史任务结果的学习器均存在明显局限。第一种直接做法是采用固定的用时规则（如一直走或按固定比例开启GPU深想），但固定规则无法兼顾不同的机载计算机速度与功耗：在慢计算机上一直走会因搜索不足而走弯路，在算力已够用的计算机上频繁开启高功耗GPU则会多耗电却不改善航线。第二种做法是采用人工智能中的经典单步元推理\cite{horvitz1987reasoning, russell1991right, lin2015metareasoning, sung2021quit}，在每个周期在线评估额外规划的计算收益与原位复测的信息收益；但该方法直接用规划器在搜索样本上的内部得分增量来估计计算收益，当搜索预算较大时，规划器会迎合有限样本中的随机正涨落而虚报收益，并且单步评估无法反映当前耗电对24小时全程续航的影响\cite{cuadron2025overthinking}。第三种做法是从历史巡测任务的最终表现中直接学习策略选择器\cite{magnino2026metareasoning}；但在本场景中，不同任务窗口之间的遗憾标准差约为0.13，而几种较好策略之间的平均差距不超过0.01，单次任务结果包含很大的环境背景波动。

针对上述问题，本文提出利用多年卫星数据标定底图不确定性、将航线搜索与价值评判分离，并在出发前通过完整任务预演选择用时策略的方法。全文工作包括三个部分：第一，利用2018至2026年东海3197天卫星叶绿素数据标定滞后底图误差，围绕旧图生成48个想象中的海洋并随现场观测同化更新，同时验证了深度时空预测模型无法在测试年份上改善1至3天的底图外推；第二，将48个想象中的海洋分为32个规划用样本与16个留出评判样本，消除航线搜索对有限样本的过拟合偏差；第三，在AUV下水前由母船或岸上计算机以4个留出海洋为假想真值，按机载计算机速度与电池功耗将五种用时策略各完整预演一遍，选出平均遗憾最低的策略投入实海执行，并进一步在单步元推理中检验了留出评判消除过度规划的作用机制。

\section{东海叶绿素遥感数据与底图不确定性}

\subsection{八年卫星数据集与赤潮任务窗口}

本文使用2018至2026年东海多源卫星融合叶绿素a数据集构建赤潮巡测任务窗口与先验误差统计。该数据集下载自美国国家海洋和大气管理局海岸观测网的ERDDAP服务器，融合了多颗极轨卫星水色传感器的观测，并采用经验正交函数缺失数据插值算法填补云层遮挡区\cite{beckers2003dineof}。数据空间分辨率为2千米，时间分辨率为逐日，覆盖2018年1月1日至2026年10月23日共3197天；研究区域取东海北纬$25^\circ\text{--}33^\circ$、东经$119.5^\circ\text{--}127^\circ$，每日包含$385\times 361$个网格像素。同时，为检验海表温度对叶绿素演变的辅助预测作用，本文还从美国国家海洋和大气管理局海岸观测网的ERDDAP服务器下载了美国国家航空航天局喷气推进实验室制作的多尺度超分辨率海表温度逐日无云产品（版本4.1）\cite{chin2017mur}，将其从$0.01^\circ$重采样至$0.04^\circ$。文中除特别注明外，所有叶绿素浓度、误差与遗憾均以$\log_{10}(\text{叶绿素a浓度}/\text{mg m}^{-3})$为单位。

为聚焦离岸赤潮高发场景，本文按统一条件从每年4月至6月的卫星序列中切出正方形巡测任务窗口。具体做法是在浙江外海陆架区（北纬$26.5^\circ\text{--}31.5^\circ$，东经$121.5^\circ\text{--}125^\circ$）寻找离岸至少30千米、经空间平滑后局部峰值超过$5\text{ mg/m}^3$的藻华中心，将该中心随机平移至多16千米后，截取$80\text{ km}\times 80\text{ km}$（$40\times 40$个2千米网格）的窗口；距离陆地或岛屿15千米以内的网格设为禁航区，仅保留可航行水域不少于80\%且窗内对数叶绿素极差不低于0.3的窗口。按此标准共切出422个赤潮任务窗口，其中2018至2022年的274个窗口作为开发集（用于标定误差统计和选择调好的基线策略），2023至2026年的148个窗口作为测试集。每次任务开始时，AUV从窗口边缘随机选取的一个可航行网格出发。

\subsection{底图滞后误差图谱与小尺度偏差}

航行器携带的旧卫星底图与现场真实海洋之间的差异，来自底图滞后数日内的海洋演变以及同日卫星图对小尺度结构的平滑。利用全部3197天数据计算相隔3天的对数叶绿素变化标准差，可得到四季分布图谱（图\ref{fig:atlas}）。全海域3天变化标准差的中位数在春季最高（0.127），夏季为0.107，秋季为0.103，冬季降至0.081；夏季空间差异显著，全海域90\%分位数达0.204，在浙闽沿岸与长江冲淡水锋面一带形成3天变化标准差达0.25至0.3的条带。在274个开发集任务窗口内，任务当日卫星图减去$k$天前旧图的误差统计显示：当滞后天数$k=1, 2, 3$天时，误差标准差分别为$s_1=0.125$、$s_2=0.176$与$s_3=0.210$，空间相关尺度约为$\ell=5$个网格（10千米），均值偏差分别为$+0.016$、$+0.032$与$+0.045$。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_atlas}
  \caption{东海海域（北纬$25^\circ\text{--}33^\circ$，东经$119.5^\circ\text{--}127^\circ$）全部3197天对数叶绿素3天变化标准差的四季分布图。陆地标为灰色；春季子图中的圆点为切出的赤潮任务窗口位置，蓝色为2018至2022年开发集（274个），绿色为2023至2026年测试集（148个）。}
  \label{fig:atlas}
\end{figure}

即便是任务当天的缺测填补卫星图，也与现场海水存在小尺度差异\cite{beckers2003dineof, ye2021cocts}。针对海洋一号丙星水色传感器在东海与南海的现场验证表明，卫星反演叶绿素与实测值之间的无偏相对百分比差异约为39\%（折合对数空间约0.15）\cite{ye2021cocts}。因此，仿真环境在任务当日卫星图上叠加一个标准差为$s_{\text{sat}}=0.15$、空间相关尺度为3个网格（6千米）的高斯随机场来生成航行器遇到的真实海洋，并在参数扫描实验中将$s_{\text{sat}}$在0.05至0.3之间变化。

\subsection{时空预测模型的检验}

为检验能否用深度学习模型在出发前将旧卫星图向前推演以减小滞后误差，本文训练了一个含550万参数的联合嵌入预测架构模型\cite{assran2025vjepa2}。该模型以过去3天的叶绿素a和海表温度异常场为输入，使用2018至2021年3月至6月数据训练并在2022年数据上验证（验证集均方根误差仅比直接沿用最新底图低1.4\%）；但在2023至2026年测试集上，模型提前1、2、3天预报缺测填补叶绿素图的均方根误差分别为0.1229、0.1439与0.1487（集合离散度与误差之比为0.70至0.93），并未优于直接将最新可用卫星图作为预报值的基线（0.1226、0.1439与0.1474），说明无法靠日均卫星图的时间外推恢复小尺度信息，必须依靠AUV现场观测。

\section{随水漂移参考系下的采样与决策模型}

\subsection{随水漂移参考系与评价指标}

本文假设斑块随表层水体一同移动，并将AUV运动、叶绿素场与数据同化全部建立在随表层水体漂移的参考系中。这一假设的依据在于，静止轨道卫星对2011年5月东海一次赤潮的逐时连续追踪表明，表层藻华斑块主要随潮汐与表层水体发生往复漂移\cite{lou2014diurnal}。在随表层水体漂移的参考系下，赤潮斑块相对于水体不移动，AUV无需逆流追赶斑块，而海流的作用则体现在卫星图滞后期间的演变统计中。

在由$40\times 40$个2千米网格组成的任务窗口内，记网格$\mathbf{x}$处的真实对数叶绿素浓度为$c(\mathbf{x})$。在$T=24\text{ h}$的任务窗口内，应急指挥中心可随时询问最浓处在哪里；AUV从截至时刻$t$已实际造访的网格集合$\mathcal{V}(t)$中，选出内部集合均值$\bar{c}_t(\mathbf{x})$最高的位置作为回答：
\begin{equation}
  \hat{\mathbf{x}}(t) = \arg\max_{\mathbf{x}\in\mathcal{V}(t)} \bar{c}_t(\mathbf{x})
  \label{eq:answer}
\end{equation}
任务在满24小时或电池耗尽时结束，结束后的回答保持不变。定义24小时时间平均遗憾$R$为评价指标（越低越好）：
\begin{equation}
  R = \frac{1}{T}\int_0^T \left[\max_{\mathbf{x}} c(\mathbf{x}) - c\big(\hat{\mathbf{x}}(t)\big)\right] dt
  \label{eq:regret}
\end{equation}

\subsection{航行器功耗模型与二十分钟决策周期}

航行器机电参数参照百米级轻型AUV\cite{remus100}与嵌入式边缘GPU模块\cite{jetsonorinnx}设定。AUV对水巡航速度为$1.5\text{ m/s}$（约3节），携带$1\text{ kWh}$电池，在3节航速下续航约22小时，对应巡航总功率$45\text{ W}$，其中基础航电功率$15\text{ W}$（含导航、传感器及常驻后台运行的低功耗处理器），推进功率$30\text{ W}$。机载嵌入式GPU模块（功率范围$10\text{--}25\text{ W}$，基准设定取$+20\text{ W}$，省电加速器设定取$+5\text{ W}$）用于深度航线规划，其推演速度为低功耗处理器的50倍。由于本文的折线规划器与二维表层场是对真实水下三维路径评估（需计入海流、深度与安全约束）的简化替代，决定规划质量的是计算机相对于规划问题的速度；因此实验以“每分钟想象推演次数”度量低功耗处理器速度，并在5至200次/分的范围内变化。

整个24小时任务按每段20分钟划分为连续的决策周期。在每个20分钟周期内，AUV的机体与大脑并行动作\cite{xiao2020thinking, elboher2023formal}：
\begin{itemize}
  \item \textbf{机体动作：}选择“走”时，开启推进器（$30\text{ W}$）沿当前航线以$1.5\text{ m/s}$航行，20分钟走过$1.8\text{ km}$（不足一个2千米网格），机载荧光计每走$1\text{ km}$采样1次，每周期获得约2个样本；在电池允许时，24小时可航行约$120\text{--}130\text{ km}$，约能横穿80千米窗口1.5次。选择“停下”时，关停推进器（推进功率$0\text{ W}$，仅耗电$15\text{ W}$）随水漂流，荧光计每4分钟对同一水体采样1次，每周期获得5个样本。每次独立采样的观测模型为：
  \begin{equation}
    y = c(\mathbf{x}) + \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, 0.1^2)
    \label{eq:obs}
  \end{equation}
  \item \textbf{大脑规划：}维持低功耗处理器后台规划（额外功耗$0\text{ W}$），或开启GPU“深想”（额外功耗$+20\text{ W}$或$+5\text{ W}$，推演速度提高至50倍）。新航线以AUV在当前20分钟周期结束时的预计位置为起点进行计算（时延补偿），并在周期结束时替换旧航线。
\end{itemize}

\section{想象中的海洋与出发前预演方法}

\subsection{想象中的海洋与现场观测同化}

航行器在内部维护48个“想象中的海洋”来表达对叶绿素分布的先验认识与当前记忆。出发前，围绕滞后$k$天的卫星图$c_{\text{map}}(\mathbf{x})$生成48个样本：
\begin{equation}
  c^{(i)}(\mathbf{x}) = c_{\text{map}}(\mathbf{x}) + \sigma_k\, z^{(i)}(\mathbf{x}), \quad i = 1, \dots, 48
  \label{eq:prior}
\end{equation}
其中$\sigma_k = \sqrt{s_k^2 + s_{\text{sat}}^2}$为合成先验标准差（当$k=3$天、$s_3=0.210$、$s_{\text{sat}}=0.15$时，$\sigma_3 \approx 0.26$），$z^{(i)}(\mathbf{x})$为具有平方指数空间相关结构（相关长度$\ell = 5$个网格，即10千米）的独立标准高斯随机场。

巡测过程中，每当荧光计获得一个样本$y$，AUV采用序列集合调整卡尔曼滤波\cite{anderson2001eakf}更新全部48个想象中的海洋。为消除小集合在远距离网格间产生的伪相关，更新时乘以半宽为$2\ell$（10个网格，20千米）的五阶分段有理局地化函数\cite{gaspari1999correlation}，使单点观测仅修正周围空间相关范围内的水体估计。

\subsection{规划搜索与留出评判分离}

在每个20分钟周期内，规划器通过想象推演寻找连接当前周期终点与两个中间航路点的折线航线。将一条候选航线在单个想象海洋$c^{(i)}$上模拟航行一次称为一次想象推演：记沿该航线航行至剩余任务时刻$\tau \in [0, T_{\text{left}}]$时所遇最高叶绿素浓度为$m_i(\tau)$（以当前已访最佳估计为初值，当可用巡航电池时间耗尽后保持冻结），则该航线在样本$i$上的价值定义为剩余窗口内的时间均值：
\begin{equation}
  V_i = \frac{1}{T_{\text{left}}}\int_0^{T_{\text{left}}} m_i(\tau)\, d\tau
  \label{eq:route_value}
\end{equation}
这一定义直接对应式\eqref{eq:regret}的时间平均遗憾目标：越早到达浓水区，$V_i$越高。规划器采用周期之间热启动的交叉熵方法\cite{deboer2005cem}搜索航路点。

当规划器在有限个想象海洋上搜索航线时，若同时用这批样本的平均得分来评判航线好坏，就会受到“优化器诅咒”的影响\cite{smith2006curse, vanhasselt2010double}。其原因在于，当推演次数大幅增加时，优化器能够精细调整航路点位置，使折线恰好穿过这批特定样本中偶然重合的随机高值点；此时规划器看到的内部自评得分会随推演次数增加而持续上升，但在未参与搜索的真实海洋中，这种针对样本随机涨落的微调并不提高实际收益。为此，本文将48个想象中的海洋固定分为两组（图\ref{fig:overview}B）：32个作为规划用海洋，供交叉熵规划器搜索并选出均值最高的航线；其余16个作为留出海洋，它们同样随现场观测同化更新，但从不参与航线搜索。当先验底图不确定性经数据如实标定时，留出海洋能够对选出的航线给出近乎无偏的价值评判。

\subsection{出发前预演控制器与对比基线}

为在全任务周期尺度上权衡走、深想与停下，本文定义了五种候选时间分配策略：（1）一直走：全程巡航采样，仅用低功耗处理器后台规划；（2）一直深想：全程巡航采样，同时每周期开启GPU深想；（3）三段深想一段：全程巡航采样，每3个周期中开启1个周期GPU深想；（4）三段停下深想一段：每3个周期中有1个周期停下漂流并开启GPU深想，其余2个周期走并用后台规划；（5）三段停下复测一段：每3个周期中有1个周期停下漂流原位复测且仅用后台规划，其余2个周期走并用后台规划。

在AUV下水前，当航行器仍位于母船甲板或岸站并保持有线连接时，母船或岸上计算机运行“出发前预演”来选定本次任务的策略。预演程序从16个留出海洋中取出4个样本$\{c^{(j)}\}_{j=1}^4$作为假想的“真实海洋”；对每个假想真值$c^{(j)}$和五种策略中的每一种策略$s$，按AUV自身的规划器、机载计算机速度与$1\text{ kWh}$电池模型完整模拟一遍24小时巡测任务，得到假想遗憾$R_{s,j}$。五种策略在同一个假想真值上使用相同的初始集合与观测噪声序列，最后选出4个假想真值上平均遗憾最低的策略执行：
\begin{equation}
  s^* = \arg\min_{s} \frac{1}{4}\sum_{j=1}^4 R_{s,j}
  \label{eq:rehearsal}
\end{equation}
预演本身运行在母船或岸上计算机上：慢计算机配置单次任务需约190万次推演，在机载GPU上需约125小时，而在普通台式机单核上每次任务仅需数秒。

实验将出发前预演与四类基线对比：（1）上述五种固定策略；（2）调好的固定策略，即针对每一种硬件配置，先在2018至2022年120个开发集窗口上找出平均遗憾最低的固定策略，再用于测试集（该基线需要该型航行器的历史任务数据，而出发前预演不需要）；（3）单步元推理\cite{russell1991right}，在每个周期根据规划器在规划用海洋上的搜索改进轨迹估计计算价值，并通过想象海洋上的预后验分析估计采样信息价值；（4）规划用海洋上的出发前预演对照，其流程与式\eqref{eq:rehearsal}相同，但4个假想真值取自32个规划用海洋。

\section{实验结果与分析}

\subsection{规划预算与留出海洋评判的准确性}

在80个开发集窗口（每窗口3个随机种子，3天前卫星图，任务前8小时）上的预算扩展实验表明，留出的想象海洋能够消除规划器的自评高估并准确反映航线价值的饱和过程（图\ref{fig:curse}）。当每次决策的想象推演次数从64次增至2000次再增至200,000次（跨度约三个半数量级）时，所选航线在真实海洋中的价值从0.749升至0.793，随后平缓收敛至0.803；规划器在32个规划用海洋上的搜索自评得分则从0.762升至0.833并继续攀升至0.917，在最高预算下比真实值高出0.114。相比之下，同一批航线在16个留出海洋上的评判均值分别为0.745、0.794与0.802，当底图不确定性经数据标定时，在所有预算下与真实价值之差均在0.005以内（图\ref{fig:curse}b蓝色虚线）。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_curse}
  \caption{每次决策的想象推演次数从64次增至200,000次时的航线价值与评判偏差（80个开发集窗口$\times 3$个种子，3天前卫星图）。（a）航线的时间平均最佳浓度（折算为$\text{mg/m}^3$）：规划器搜索时的自评（红线）随推演次数持续上升，留出的想象海洋上的评价（蓝色虚线）与真实海洋中的结果（黑线）在约2000次后一同趋于平缓，阴影带表示任务间的离散度；（b）估计减去真实的对数浓度偏差：不确定性如实标定时留出评价保持在0附近（蓝色虚线），不确定性设大到1.5倍（橙色点线）或设小一半（浅蓝色点线）时分别产生约$+0.07$与$-0.06$的平移。}
  \label{fig:curse}
\end{figure}

即便先验不确定性幅值标定存在偏差，留出海洋对增加算力所获相对提升的判断依然稳健（图\ref{fig:curse}b）。当人为将先验标准差设小一半或设大到1.5倍时，留出评价虽分别产生$-0.06$（浅蓝色点线）与$+0.07$（橙色点线）的整体偏移，但推演次数从64次增至200,000次时留出评价估计的增益（$+0.059$与$+0.054$）仍与真实海洋中的实际增益（$+0.054$与$+0.047$）接近。

\subsection{算力与底图误差相图及典型任务分析}

在低功耗处理器速度（每分钟5至200次推演）与真实海洋偏离卫星图程度（0.05、0.15、0.30）构成的18格二维网格（每格60个开发集任务）上，五种固定策略的表现呈现出清晰的相图分界（图\ref{fig:phase}）。首先，开启GPU深想仅在基础算力相对于规划问题过慢时才显著优于“一直走”（图\ref{fig:phase}a）：在最慢的计算机（5次/分）上，后台每20分钟仅完成100次推演，远低于图\ref{fig:curse}a中约2000次的饱和区，此时“三段深想一段”（单次深想推演5000次）显著优于“一直走”，且底图越不准，深想收益越大，当偏离程度为0.05、0.15与0.30时配对遗憾差值分别为$-0.086$、$-0.109$与$-0.138$；在10次/分且偏离0.15的格点上仅存在微弱优势（差值$-0.017$，95\%置信区间$[-0.035, -0.001]$）；从20次/分起（后台每20分钟推演400次以上），所有格点中均无任何固定策略显著优于“一直走”（图\ref{fig:phase}a灰色“$\approx$”区域），而“一直走”自身的绝对遗憾则随底图偏离程度增大而上升（在20次/分下，偏离0.05、0.15与0.30时的平均遗憾分别为0.273、0.342与0.495）。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_phase}
  \caption{低功耗计算机速度（5、10、20、50、100、200次推演/分钟）与真实海洋偏离卫星图程度（0.05、0.15、0.30）网格上的固定策略相图（每格60个开发集任务）。（a）最好的固定策略相对“一直走”的时间平均遗憾差值：仅在配对差值的95\%置信区间低于0时标出显著优于“一直走”的策略颜色（橙色为“三段深想一段”）及差值，灰色“$\approx$”表示无策略显著优于“一直走”；（b）两个停下类策略中较好者比不停的最好策略多出的遗憾（正值表示停下带来损失）。}
  \label{fig:phase}
\end{figure}

其次，在全部18个格点的算力与底图误差组合下，两个停下类策略中较好者的表现均显著劣于不停的最好策略，多出的遗憾达$+0.063$至$+0.118$，所有格点的95\%置信区间均高于0（图\ref{fig:phase}b）。从采样几何与不确定性尺度可以解释这一现象：AUV以$1.5\text{ m/s}$航行20分钟走过$1.8\text{ km}$并采集约2个样本，而停下漂流20分钟对同一水体采集5个样本；在原地重复采样5次虽能将该点处的测量误差从单次$0.1$压低至约$0.1/\sqrt{5}\approx 0.045$，但决定回答质量的瓶颈是尚未造访水域的高先验不确定性（标准差约$0.26$），且将三分之一的时间用于停下会使航行器更晚到达浓水区，从而受到时间平均遗憾的惩罚。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_example}
  \caption{一次测试集任务（2023年4月15日，慢计算机5次/分）中两种策略的对比。（a）航行器携带的3天前卫星图，东侧边缘白色三角形为起点；（b）真实海洋及“一直走”（蓝线）与“三段深想一段”（橙线）的航迹，西南角五角星为真实最浓处；（c）24小时内应急中心随时得到的答案误差，“一直走”停留在0.4附近（平均0.43），“三段深想一段”在约19小时后到达真实最浓处（误差降至0，平均0.31）。}
  \label{fig:example}
\end{figure}

图\ref{fig:example}展示了按日期顺序第一个策略差距超过0.1的测试集任务实例（2023年4月15日，慢计算机）。AUV从东侧边缘（白色三角形）出发；3天前的卫星图在东北部浓度较低，向西和西南方向浓度较高（图\ref{fig:example}a），而真实最浓处位于西南角（图\ref{fig:example}b五角星）。在慢计算机上，“一直走”（蓝线）向西南航行至窗口中部后便在中部来回移动，其回答误差一直停留在0.4左右，24小时平均遗憾为0.43（图\ref{fig:example}c）；“三段深想一段”（橙线）则直接横穿窗口驶向西南角，在约19小时后到达真实最浓处（回答误差降至0），24小时平均遗憾降至0.31。

\subsection{不同硬件平台上的控制器对比}

在2023至2026年全部148个测试任务窗口上，表\ref{tab:main}对比了四种硬件配置下各控制方式的表现。按120个开发集窗口选出的“调好的”固定策略随硬件而异：慢计算机（5次/分，$+20\text{ W}$）与中等计算机（20次/分，$+20\text{ W}$）上均为“三段深想一段”（测试集遗憾0.270与0.269），快计算机（100次/分，$+20\text{ W}$）上为“一直走”（0.267），省电加速器（20次/分，$+5\text{ W}$）上则为“一直深想”（0.267）。测试集上，除慢计算机上“一直走”遗憾达0.374（比调好策略高$+0.104$）外，其余三种硬件下三种持续航行策略之间的平均遗憾差距均不超过0.004（中等0.003、快0.004、省电0.001），处于统计噪声范围内（如中等计算机上“一直走”减调好策略为$-0.002$，95\%置信区间$[-0.010, +0.005]$）；而两种停下类策略在四种硬件上均比调好策略差$+0.059$至$+0.138$。

\begin{table}[htbp]
  \centering
  \caption{2023至2026年148个测试集任务（3天前卫星图，真实海洋偏离0.15，传感器误差0.1）上各控制方式的时间平均遗憾（越低越好）。“调好的”指在该型航行器的120个开发集任务上表现最好的固定策略；括号内为相对于“调好的”策略的差值，方括号内为按赤潮周自助重采样得到的95\%置信区间。}
  \label{tab:main}
  \input{tables/main_table.tex}
\end{table}

经典单步元推理在慢、中、快计算机与省电加速器上的时间平均遗憾分别为0.287、0.287、0.282与0.278，比各硬件调好的策略分别高出$+0.017$、$+0.018$、$+0.015$与$+0.011$（表\ref{tab:main}）。单步元推理利用规划器在搜索样本上的内部改进轨迹评估计算价值，并通过想象海洋上的预后验分析评估原位复测价值；在四种硬件上，它分别在80\%、93\%（其中63\%边走边想，30\%停下深想）、97\%与94\%的周期内开启GPU深想，并分别有34\%、33\%、33\%与33\%的周期处于停下漂流状态，损耗了巡航时间与电池能量。

本文提出的留出海洋出发前预演在四种硬件上分别取得0.276、0.265、0.268与0.266的时间平均遗憾，相对于各硬件调好策略的差值分别为$+0.007$（$[-0.001, +0.014]$）、$-0.003$（$[-0.009, +0.003]$）、$+0.002$（$[-0.005, +0.008]$）与$-0.001$（$[-0.006, +0.005]$），95\%置信区间均包含0；与单步元推理作配对比较，出发前预演减去单步元推理的遗憾差值分别为$-0.011$（$[-0.019, -0.002]$）、$-0.022$（$[-0.030, -0.013]$）、$-0.013$（$[-0.020, -0.007]$）与$-0.012$（$[-0.019, -0.004]$），置信区间全部位于0以下。对慢计算机全部148个测试任务重新运行预演，所得每次任务的遗憾与首次运行完全一致，验证了实验的精确可重复性。从选出的策略比例看，出发前预演能够随硬件特征自适应调整：在“一直走”代价高昂的慢计算机上，预演选出“三段深想一段”占55\%、“一直深想”占39\%、“一直走”仅占1\%、停下类策略占4\%；随着基础算力提高，“一直走”的入选比例从慢计算机的1\%升至中等计算机的30\%（“三段深想一段”43\%、“一直深想”25\%、停下类1\%）和快计算机的47\%（“三段深想一段”28\%、“一直深想”22\%、停下类3\%）；而在GPU功耗降至$+5\text{ W}$的省电加速器上，预演最常选择“一直深想”（43\%，“三段深想一段”35\%、“一直走”20\%、停下类1\%）。

对比表\ref{tab:main}最后两行可见，规划用海洋预演对照的平均遗憾与留出海洋预演接近，两者选出各策略的总体比例也相近，但在单个任务上选出同一策略的比例仅为37\%至41\%，与按总体比例独立抽取两次相当。这表明预演的作用在于避开劣质选项（各硬件上的停下策略及慢计算机上的“一直走”），其相对于随机选取的优势正源于此（如慢计算机上三种不停策略随机选取的平均遗憾为0.306，预演降至0.276）；而在真实平均差距不超过0.01（除慢计算机外不超过0.004）的三种不停策略之间，预演的单任务选择并不优于随机抽取，距离事后逐任务最优选择（中等计算机上为0.243，预演为0.265）仍有提升空间。此外，预演内部假想遗憾比真实海洋高出0.05至0.07，但该偏移对各策略大致相同，不影响剔除劣质策略的排序。

\subsection{留出评判消除过度规划的机制检验}

为直接检验第5.1节的规划自评偏差是否是导致第5.3节单步元推理过度规划的主要原因，本文在慢计算机与中等计算机的148个测试任务（保持相同随机种子）上测试了改用留出评判的单步元推理：保持单步元推理其余流程不变，仅将“多想一步的计算收益”和“原位复测的信息收益”改为在16个留出想象海洋上评判（即在32个规划用海洋上搜索选出航线、在16个留出海洋上评估其价值，对应双估计思想\cite{vanhasselt2010double}）。

实验结果显示，改用留出评判后，单步元推理开启GPU深想的周期比例在慢计算机上从80\%大幅降至30\%，在中等计算机上从93\%降至38\%；处于停下漂流状态的周期比例分别从34\%降至17\%和从33\%降至17\%（均减少一半）。相应地，其时间平均遗憾在慢计算机上从0.287降至0.278（配对差值$-0.009$，95\%置信区间$[-0.018, +0.000]$），在中等计算机上从0.287降至0.270（配对差值$-0.017$，95\%置信区间$[-0.025, -0.009]$）；与出发前预演相比，修正后的单步元推理在慢、中计算机上的配对差值分别为$+0.002$（$[-0.007, +0.010]$）与$+0.005$（$[-0.003, +0.011]$），置信区间均包含0。这表明经典单步元推理的过度规划主要源于在同一批规划用海洋上既搜索选出航线又评估计算与采样价值；将计算收益与原位复测收益改在留出海洋上评判即可消除大部分过度规划（剩余17\%的停下周期仍带来少量损失）。由此可见，本文两种有效控制器共享同一核心机制——在未参与搜索的留出想象海洋上做价值评判：出发前预演在任务下水前将这一准则用于完整任务尺度，而修正后的单步元推理则在航行途中将其用于每个20分钟控制周期。

\section{结论}

本文依托八年东海多源融合卫星叶绿素数据与春季赤潮任务窗口，研究了携带滞后卫星图的AUV在巡测中如何权衡走、深想与停下复测的时间与能量。主要结论如下：
\begin{enumerate}
  \item 深度时空预测模型在测试年份上对数日缺测填补叶绿素图的预报精度未超过直接沿用最新卫星图，小尺度藻华结构必须依靠AUV现场采样获取。
  \item 将内部集合划分为规划用海洋与留出海洋可有效消除优化器诅咒：随单次决策推演预算增加，规划用海洋上的搜索自评得分因迎合样本噪声而持续攀升，而在先验不确定性经数据标定时，留出海洋上的评判均值在所有预算下均紧密跟踪真实航线价值。
  \item 在未参与搜索的留出想象海洋上做价值评判，是抑制过度计算的核心机制。开启高功耗GPU深想仅在基础算力过慢时显著优于“一直走”，中途停下复测在所有算力与底图误差下均得不偿失。出发前预演在任务尺度上应用留出评判，能够避开停下策略并在慢计算机上避开“一直走”，从而在无需历史任务调参的条件下适配四种硬件配置，达到与各硬件调好策略相当且显著优于经典单步元推理的表现；将留出评判按周期引入单步元推理同样能将深想比例从80\%—93\%压低至30\%—38\%，达到与出发前预演相当的水平。
\end{enumerate}

本研究仍存在以下局限：（1）随表层水体漂移的参考系忽略了窗口内的水平流剪切与藻华昼夜垂直迁移；（2）仿真中的“真实海洋”是在任务当日卫星图上叠加按发表文献标定的空间相关随机场生成的，并非现场实测真值；（3）二维表层场上的双航路点折线规划器是对真实水下三维路径规划的简化替代，因此机载算力需按相对于规划问题的推演速度来表征；（4）出发前预演需在AUV下水前依赖母船或岸基计算机运行，且仅在出发前执行一次而未在任务中途重选策略；（5）4个假想真值的预演仅能实现针对硬件平台的策略适配，尚无法在真实差距微小的几种持续航行策略间做出优于随机的单任务选择。后续工作将结合三维海流预报集合与实海观测数据，进一步探讨多台航行器协同巡测中的在线计算与采样分配问题。

===== FILE: sections/appendix.tex =====
\section{代码与数据说明}

本研究的数据处理、集合同化、航线规划器、时空预测模型、出发前预演与论文图表的完整代码、原始实验结果数据，以及学生与Claude的研究讨论对话记录（已隐去涉及学生其他未发表工作的内容）均开源于：\TBD{GitHub 仓库地址}。

实验使用的两套卫星遥感数据集均下载自美国国家海洋和大气管理局海岸观测网（NOAA CoastWatch）的ERDDAP服务器：
\begin{enumerate}
  \item \textbf{东海多源融合叶绿素a逐日数据集（2018—2026年）：} 融合了S-NPP与NOAA-20卫星上的VIIRS传感器以及Sentinel-3A卫星上的OLCI传感器观测，并经DINEOF方法填补云区盲区，空间分辨率2千米，时间分辨率逐日，遵循CC0开放许可，数据集标识为\texttt{noaacwNPPN20S3ASCIDINEOF2kmDaily}。
  \item \textbf{多尺度超分辨率海表温度数据集（2018—2026年）：} 由美国国家航空航天局喷气推进实验室（NASA JPL）制作（MUR v4.1），原始空间分辨率$0.01^\circ$，时间分辨率逐日，数据集标识为\texttt{jplMURSST41}。
\end{enumerate}

\section{人工智能工具使用说明}

在本课程论文的研究与写作过程中，人工智能工具的使用情况与各环节分工如下：
\begin{enumerate}
  \item 学生提出了本文的研究问题（海洋航行器在巡测过程中何时应当继续计算、何时应当继续观测），设定了研究方向与各项要求，并对提交的论文承担全部责任。
  \item Claude（Anthropic）完成了文献调研，与学生讨论细化了选题，编写了实验代码，运行了全部数值实验并绘制了论文图表。
  \item Gemini（Google）根据Claude整理的实验事实清单撰写了论文初稿与修改稿的文字。
  \item Claude对照实验结果与原始文献逐一核查了文中的全部数值与文献引用。
\end{enumerate}
```

</details>
