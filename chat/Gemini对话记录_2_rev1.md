# 与 Gemini 的对话记录 2：第 1 次修改

时间（回复保存时间）：2026-11-04 18:14 UTC。调用方式：Claude 用命令行工具 ask-gemini 把下面“发送内容”作为附件发给 Gemini，并附一句简短指令（按附件中的写作要求完成各节）；回复原样存档后再由 Claude 核对数字与引用、拆分进论文各节。下面两部分都是原文，未作删改。

本轮的写作要求见下方发送内容里的附件 `brief_rev1.md`。

## 发送内容

<details><summary>展开（共 71826 字符）</summary>

```
########## ATTACHED FILE: brief_rev1.md ##########

# Revision 1

Thank you for draft 1 (attached: draft1_*.tex). I checked every fact against the results. Please
rewrite the whole paper - all files - keeping what works. Structure, wording and terminology are
yours to decide; the facts (facts.md) are fixed.

## 1. Length (most important)
The compiled paper is 31 pages; the course asks for "十几页" (12-18 pages in total, cover, table
of contents, references and appendix included). Targets:
- body about 8,000-9,000 Chinese characters (draft 1: 15,400);
- Chinese abstract at most 500 characters (draft 1: 1,081); English abstract at most 250 words;
- five figures (overview, atlas, curse, phase, example) and one table; fig_main is dropped.
Where to cut: the optimizer's curse is explained four times (once is enough); numbers retold in
prose that the table already holds; acronym-by-acronym descriptions of the satellites; the long
argument for why the world model fails (two sentences suffice); repeated summaries at section
starts and ends.

## 2. Factual errors to fix
1. Moving at 1.5 m/s for 20 minutes covers 1.8 km, not 18 km: about 2 samples per interval
   while moving, 5 samples of the same water while drifting. The explanation in 5.2 of why
   stopping never pays rests on the wrong number; rewrite it. What can be said (as reasoning,
   not as a measurement): resampling one place reduces the error at that place (5 samples:
   0.1 to about 0.045), but what decides the answer is the much larger uncertainty about water
   not yet visited (prior spread about 0.26), and a vehicle that stops for a third of its time
   reaches dense water later, which the time-averaged regret penalises.
2. Moderate computer: the strategy tuned on the development years is think-one-in-three (0.269),
   not always go. Every difference in that column is relative to it (always go -0.002, always
   think +0.000, stop and think +0.059, stop and resample +0.066, one-step metareasoning +0.018,
   rehearsal -0.003, self-assessed rehearsal -0.000). Draft 1's column was wrong.
3. On the moderate computer the three good strategies differ by at most 0.003, within noise.
   Do not say always go "反超" or "成为最优", and do not explain the difference by battery use.
4. There are no p-values (delete "p < 0.01"). Rehearsal minus one-step metareasoning, paired,
   95% interval: slow -0.011 (-0.019 to -0.002); moderate -0.022 (-0.030 to -0.013).
5. One-step metareasoning, moderate computer: thinks in 93% of intervals (63% while moving, 30%
   stopped to think) and is stopped in 33%; slow computer: thinks in 80%, stopped in 34%.
   (Draft 1 had 65% / 28%.)
6. Rehearsal on the moderate computer does not "turn decisively to cruising": it picks think one
   in three in 43% of missions, always go in 30%, always think in 25%. What it picks on the slow
   and the fast computer is not available yet (placeholder).
7. The tuned strategy is chosen on the development years and then evaluated on the untouched
   test years. It is not "事后最优", not an "oracle" and not an upper limit; it is a strong
   baseline that needs past missions with that vehicle. Rehearsal needs none.
8. The rehearsal runs before launch on the support ship's or the shore computer, simulating the
   vehicle's computers; it could not run on the vehicle (facts.md gives its cost). Say so in
   the method, and mention the cost once.
9. Example mission: use the corrected description in facts.md (the old map is LOW in the north-
   east; always go reaches the middle of the window and moves back and forth there; delete the
   story about observations "falsifying a north-east patch").
10. The imagined-minus-real offset (0.05-0.07): its cause is not established - delete the
    "higher-moment difference" explanation. Likewise state only the observation for searched
    versus held-out rehearsal (they pick nearly the same strategies; a common offset leaves the
    ranking unchanged), without the mechanism draft 1 proposes.
11. Stale-map mean bias +0.016/+0.032/+0.045: give no interpretation (windows are chosen on
    bloom days; "net growth phase" is unsupported).
12. Delete unverified statements: "单次观测更新耗时仅亚毫秒级"; "严格满足贝叶斯后验均值与方差一致性";
    "藻华斑块在日尺度上主要作为被动示踪物" (Lou & Hu tracked one bloom in May 2011 drifting with
    the tides - say that); "受控于未观测的局地风应力与营养盐脉冲"; "四个数量级" (64 to 200,000 is
    about three and a half); the citations of xiao2020thinking / elboher2023formal attached to
    the 72 intervals.
13. Learning a selector from past missions (draft 1, section 1.3): the numbers 0.08 and 0.01 came
    from an earlier objective. Use the current ones (mission-to-mission spread about 0.13 versus
    differences of 0.01 or less between good strategies), and do not claim this paper showed
    that learning fails.
14. Captions must match the attached figures: no satellite in Figure 1; the ring at the densest
    water is pale, not yellow; the dotted lines in fig_curse (b) are orange and light blue, not
    grey; fig_curse (a) is in mg/m3; describe the stack of imagined oceans without counting
    layers.
15. MUR SST is produced by NASA JPL and was downloaded from a NOAA CoastWatch ERDDAP server.
16. Appendix, use of AI tools - the facts: the student proposed the question (when an ocean
    vehicle should keep computing and when it should observe again); Claude (Anthropic) surveyed
    the literature, refined the topic with the student, wrote the code, ran the experiments and
    drew the figures; Gemini (Google) wrote the text from Claude's facts sheet; Claude checked
    every number and citation against the results; the student set the direction and the
    requirements and takes responsibility for the submitted paper. Do not write that the student
    led or did work the student did not do. Repository address: \TBD{GitHub 仓库地址}.

## 3. Style (the student's standards; draft 1 breaks them)
- No hype or emotive words: 惊人、灾难性、完美、彻底、有力地、果断、扭转战局、破局之道、沙盘推演、
  泡沫、病态、深刻、全面落后、从根本上解决; no exclamation marks.
- No Markdown: **...** prints as asterisks in LaTeX.
- No English inside Chinese sentences except AUV and GPU (no "Tuned", "One-Step
  Metareasoning", "Pre-Mission Rehearsal in Imagination", "rollout").
- No coined terms or abbreviations: 海真, 过思考偏差机理, 集合解耦校正律, 自校准元控制范式,
  具身智能体 (say AUV or 航行器), 双集合解耦架构. Use plain words; define each technical term once.
- The first sentence of each paragraph states its conclusion; general question first, the bloom
  case second; "the obvious approach -> why it fails here -> therefore this".
- Claims at the strength of the evidence, e.g. "与按开发年份调好的固定策略相差在置信区间内",
  not "完全持平" or "自动逼近事后最优".

## 4. Terms - one name for each thing, consistent with the figures
The figures currently use: 想象中的海洋, 留出, 出发前预演, 走 / 深想 / 停下, and for the five
strategies 一直走, 一直深想, 三段深想一段, 三段停下深想一段, 三段停下复测一段; the table also uses
单步元推理 and 调好的 (for the tuned strategy). Use these or choose better ones, and list your
final names at the end in a block "===== FILE: terms.md =====" (one line per item: what it is, its
Chinese name); I will relabel the figures and the table to match.

## 5. Placeholders
Still running: the fast-computer and efficient-accelerator results, the phase diagram, and which
strategy rehearsal picks on the slow and the fast computer. Write every sentence that depends on
them with \TBD{...} saying what goes there, so that filling them in needs no restructuring.

## 6. Table
Use \input{tables/main_table.tex} inside a table environment with your caption (the attached file
holds the tabular). In the text, quote only the few numbers the argument needs.

## Output
As before, files separated by "===== FILE: <path> =====": sections/title.tex, sections/subtitle.tex,
sections/abstract.tex, sections/body.tex, sections/appendix.tex, terms.md.


########## ATTACHED FILE: facts.md ##########

# Facts sheet for the writer

Everything here must hold in the paper. Structure, wording, terminology and emphasis are the
writer's choice. TBD = filled from results/ when the runs finish. Numbers are log10
chlorophyll unless stated.

## Setting
- Course: Ocean Big Data, Zhejiang University, autumn 2026 (instructor Zhang Fan). Paper in
  Chinese, ZJU course paper format, about 12-16 pages.
- Scenario: harmful algal bloom (HAB) emergency survey east of Zhoushan, East China Sea.
  Prorocentrum donghaiense blooms occur in late spring and early summer off Zhejiang and the
  Changjiang estuary (Zhao et al. 2025, Front. Mar. Sci.; Lou & Hu 2014, GOCI tracking of a May
  2011 bloom drifting with tides). Bloom patches above about 6 mg m^-3 (SPIE 8175).
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
  | always go | 0.374 (+0.104) | 0.266 (-0.002) | TBD | TBD |
  | always think | 0.273 (+0.003) | 0.269 (+0.000) | TBD | TBD |
  | think 1 in 3 | 0.270 (tuned) | 0.269 (tuned) | TBD | TBD |
  | stop and think 1 in 3 | 0.331 (+0.061) | 0.328 (+0.059) | TBD | TBD |
  | stop and resample 1 in 3 | 0.408 (+0.138) | 0.335 (+0.066) | TBD | TBD |
  | one-step metareasoning | 0.287 (+0.017; 0.009 to 0.025) | 0.287 (+0.018; 0.010 to 0.027) | TBD | TBD |
  | rehearsal (held-out truths) | 0.276 (+0.007; -0.001 to 0.015) | 0.265 (-0.003; -0.009 to 0.003) | TBD | TBD |
  | rehearsal (searched truths) | 0.273 (+0.003) | 0.268 (-0.000) | TBD | TBD |
  The table for the paper is generated from the results: paper/tables/main_table.tex
  (\input it; do not retype numbers). "Tuned" is chosen on the development years 2018-2022 and
  then evaluated on the untouched test years: it is a strong baseline that needs past missions
  with that vehicle, not an oracle and not chosen after seeing the test results.
- Moderate computer: always go 0.266, always think 0.269, think 1 in 3 0.269 differ by at most
  0.003 - within noise (always go minus tuned: -0.002, interval -0.010 to +0.005). Do not
  explain this tiny difference with a mechanism.
- Rehearsal minus one-step metareasoning (paired, 95% interval, bootstrap over bloom weeks):
  slow -0.011 (-0.019 to -0.002), moderate -0.022 (-0.030 to -0.013); fast and efficient TBD.
  There are no p-values; use these intervals.
- What one-step metareasoning does with its intervals: slow computer - thinks on the GPU in 80%
  of intervals and is stopped (drifting) in 34%; moderate - thinks in 93% (63% while moving, 30%
  stopped to think) and is stopped in 33%.
- Which strategy rehearsal picks (share of test missions), moderate computer: think 1 in 3 43%,
  always go 30%, always think 25%, stop and resample 1 in 3 1%. Slow and fast: TBD (the pattern
  so far: the faster the computer, the more often it picks always go).
- Mission-to-mission spread of regret (standard deviation over test missions) is about 0.13 for
  the good strategies, while the good strategies differ from each other by 0.01 or less; one
  mission says little about which strategy is better, which is why the comparison uses 148
  missions and paired differences.
- Imagined regrets are higher than real by 0.05-0.07 for every strategy alike (the reason is not
  established; do not explain it); because the offset is common, the ranking is kept. Held-out
  and searched rehearsal pick nearly the same strategies (moderate computer: imagined "think
  minus go" -0.002 held-out vs +0.006 searched; real +0.002 - all near zero, a near tie).
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
- TBD: fast and efficient vehicles; phase diagram (which fixed strategy wins as computer speed
  and map accuracy vary).


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
- fig_phase: (to be redrawn from the final sweep; the text may describe it in general terms)
  two panels on a grid of low-power computer speed (5, 10, 20, 50, 100, 200 rollouts per minute)
  x how far the real ocean departs from the satellite map (0.05, 0.15, 0.3): (a) colour = which
  of the five fixed strategies has the lowest time-averaged regret, number = its regret minus
  that of always going ("—" where always going is best); (b) the time-averaged regret of always
  going.
- fig_example: one test mission (2023-04-15, slow computer): (a) the 3-day-old map the vehicle
  carries (start = white triangle on the east edge); (b) the real ocean, the track of always going
  (blue) and of thinking one interval in three (orange), the true densest water (star, south-west
  corner); (c) the error of the answer the operations centre gets, over 24 h (always going stays
  near 0.4, average 0.43; thinking one in three reaches 0 after about 19 h, average 0.31).
- No fig_main: the main comparison is the table paper/tables/main_table.tex.


########## ATTACHED FILE: tables/main_table.tex (generated) ##########

\begin{tabular}{lcccc}
\toprule
控制方式 & 慢计算机 & 中等计算机 & 快计算机 & 省电加速器 \\
 & {\footnotesize 5 次/分，+20 W} & {\footnotesize 20 次/分，+20 W} & {\footnotesize 100 次/分，+20 W} & {\footnotesize 20 次/分，+5 W} \\
\midrule
一直走 & 0.374（$+0.104$） & 0.266（$-0.002$） & 0.254（调好的） & \TBD{待填} \\
一直深想 & 0.273（$+0.003$） & 0.269（$+0.000$） & 0.263（$+0.009$） & \TBD{待填} \\
三取一深想 & 0.270（调好的） & 0.269（调好的） & 0.254（$-0.000$） & \TBD{待填} \\
三取一停下深想 & 0.331（$+0.061$） & 0.328（$+0.059$） & 0.325（$+0.070$） & \TBD{待填} \\
三取一停下复测 & 0.408（$+0.138$） & 0.335（$+0.066$） & 0.330（$+0.076$） & \TBD{待填} \\
\midrule
单步元推理 & 0.287（$+0.017$） & 0.287（$+0.018$） & 0.277（$+0.022$） & \TBD{待填} \\
 & {\footnotesize $[+0.009, +0.025]$} & {\footnotesize $[+0.011, +0.026]$} & {\footnotesize $[+0.011, +0.033]$} &  \\
出发前预演（留出海洋，本文） & 0.276（$+0.007$） & 0.265（$-0.003$） & 0.261（$+0.005$） & \TBD{待填} \\
 & {\footnotesize $[-0.001, +0.014]$} & {\footnotesize $[-0.009, +0.003]$} & {\footnotesize $[-0.002, +0.013]$} &  \\
出发前预演（规划用海洋，对照） & 0.273（$+0.003$） & 0.268（$-0.000$） & 0.260（$+0.003$） & \TBD{待填} \\
 & {\footnotesize $[-0.003, +0.010]$} & {\footnotesize $[-0.005, +0.004]$} & {\footnotesize $[-0.001, +0.008]$} &  \\
\bottomrule
\end{tabular}


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
  howpublished = {arXiv:2610.23662},
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
  howpublished = {arXiv:2502.08235},
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
  title = {Double Q-learning},
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
  title = {An Ensemble Adjustment Kalman Filter for Data Assimilation},
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
  howpublished = {arXiv:2506.09985},
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
  title = {{REMUS} 100 Autonomous Underwater Vehicle: product information (1 kWh lithium-ion battery; up to 22 h at 3 kn; 100 m depth rating)},
  howpublished = {\url{https://en.wikipedia.org/wiki/REMUS_(vehicle)}; \url{https://geo-matching.com/products/remus-100}},
  year = {2026}, note = {accessed 2026-11-05}
}

@misc{jetsonorinnx,
  author = {{NVIDIA}},
  title = {Jetson Orin {NX} modules: configurable module power 10--25 W (16 GB), up to 100 sparse {INT8} {TOPS}},
  howpublished = {\url{https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/}},
  year = {2026}, note = {accessed 2026-11-05}
}

Checked: the report gives 46 red tides in 2023, about 1500 km2 in total, 29 of them toxic or harmful.
@misc{mnr2024bulletin,
  author = {{自然资源部}},
  title = {2023 年中国海洋灾害公报},
  howpublished = {人民日报 2024-04-24 第 14 版报道，\url{https://paper.people.com.cn/rmrb/html/2024-04/24/nw.D110000renmrb_20240424_1-14.htm}},
  year = {2024}
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


########## ATTACHED FILE: draft1_title.tex (draft 1, sections/title.tex) ##########

基于假想海洋预演的自主水下航行器思考与行动权衡研究


########## ATTACHED FILE: draft1_subtitle.tex (draft 1, sections/subtitle.tex) ##########

——以八年卫星叶绿素大数据驱动的东海赤潮应急巡测为例


########## ATTACHED FILE: draft1_abstract.tex (draft 1, sections/abstract.tex) ##########

\section*{摘\quad 要}
\addcontentsline{toc}{section}{摘要}

携带卫星遥感大数据先验底图的自主水下航行器（AUV）在动态海洋环境中执行应急巡测时，面临机载计算能力、电池能量储备与作业时间窗口的多重物理约束。在先验底图因云层遮挡与海流平流而不可避免发生时效性退化的条件下，航行器必须在每个决策周期内反复权衡时间与能量的分配：是唤醒高功耗机载图形处理器（GPU）在内部底图上深入思考规划，还是维持低功耗巡航开展现场采样，抑或关停推进器随流漂移以开展原位重采样。既有移动观测方法多依赖经验设定的固定资源分配规则，难以适应不同机载算力速度与环境底图误差水平；而经典单步元推理方法直接利用规划器内部搜索轨迹评估计算价值，在有限样本集合上易受优化器诅咒诱导而陷入过度思考，并忽视了全任务周期内能量消耗与空间探索的非线性耦合。针对上述局限，本文提出一种基于留出假想海洋的集合同化与行前预演元控制框架，在任务出发前通过完整闭环假想任务推演实现思考与行动资源的自适应分配。该方法首先利用多年历史卫星遥感大数据校准不同滞后天数的底图误差统计特征，围绕滞后底图生成48个空间相关的假想海洋样本作为先验集合，并在随流漂移参考系下采用带局地化函数的序列集合调整卡尔曼滤波同化现场荧光计观测；其次，将假想海洋严格解耦为32个供交叉熵规划器搜索的样本与16个从未参与搜索的留出验证样本，以消除轨迹评估中的过拟合偏差；最后，在航行器出发前抽取4个留出假想海洋作为合成真实海洋，在匹配真实机载算力速度与电池功耗模型的条件下，采用共同随机数并行预演五种典型时间分配策略的24小时完整任务过程，择优执行平均随时遗憾值最低的策略。本文基于2018至2026年东海海域3197天多源融合叶绿素卫星遥感大数据，构建422个春季有害赤潮应急巡测任务窗口（含2018至2022年274个开发窗口与2023至2026年148个测试窗口），对所提方法开展系统实验验证。实验结果表明：当单步规划预算从64次推演扩展至200,000次时，真实海洋路线收益在约2,000次推演后趋于饱和（从0.749增至0.793并收敛于0.803），规划器内部搜索得分却持续攀升至0.917（虚高0.114），而16个留出假想海洋的评估均值在全预算跨度内与真实海洋收益之差始终保持在0.005以内；高功耗深度思考仅在机载基础算力相对规划问题过慢时产生显著正收益，巡航途中停航漂移重采样在所有测试工况下均呈负收益；在148个测试任务窗口上，经典单步元推理因65\%周期启动高功耗思考且28\%周期停航思考，在慢速与中速算力平台上的随时遗憾值较特定硬件事后最优调参策略分别劣化0.017与0.021，而本文提出的行前假想预演在慢速与中速算力平台上分别取得0.276与0.265的随时遗憾值，与特定硬件最优调参策略持平（差值分别为$+0.007$与$-0.001$）。本研究从机理上揭示了具身智能体轨迹规划中的过思考偏差及其集合解耦校正律，为海洋大数据赋能的实时科学计算与自主移动观测系统提供了无需历史任务调参的自校准元控制范式。

\vspace{1em}
\noindent\textbf{关键词：}海洋大数据；自主水下航行器；元推理；数据同化；赤潮巡测；计算与行动权衡

\clearpage
\section*{Abstract}
\addcontentsline{toc}{section}{Abstract}

Autonomous underwater vehicles (AUVs) equipped with prior maps derived from satellite ocean big data operate under tight physical constraints of onboard compute, battery capacity, and mission time when conducting emergency marine surveys. Because satellite prior maps inevitably degrade due to cloud gaps, retrieval uncertainties, and advective evolution, the vehicle must repeatedly decide at every control interval how to allocate its finite time and energy: whether to activate a power-hungry onboard graphics processing unit (GPU) to think more deeply on its internal map, continue cruising and sampling under low-power background planning, or shut down propulsion to drift and resample locally. Existing adaptive sampling approaches typically rely on fixed allocation heuristics that fail to generalise across varying onboard processor speeds and map error regimes, whereas classic one-step metareasoning estimates the value of computation from the planner's own internal improvement trace, succumbing to the optimizer's curse and chronic overthinking while ignoring full-mission coupling between battery depletion and spatial coverage. To overcome these limitations, this paper proposes an ensemble data assimilation and pre-mission rehearsal meta-control framework based on held-out imagined oceans, enabling self-calibrated allocation of thinking and acting resources prior to deployment. Specifically, historical satellite archives are used to calibrate stale-map error statistics and generate an ensemble of 48 spatially correlated imagined oceans around the stale satellite map, which are sequentially updated in a water-drifting reference frame using a localised Ensemble Adjustment Kalman Filter as in-situ fluorometer observations arrive; the ensemble is strictly split into 32 searched members used by a warm-started cross-entropy trajectory planner and 16 held-out members reserved exclusively for unbiased value estimation; before setting off, the vehicle treats 4 held-out imagined oceans as synthetic truths and rehearses complete 24-hour missions across five candidate time-allocation strategies under its exact hardware speed and battery model with common random numbers, executing the strategy that minimises imagined time-averaged regret. We evaluate the framework using 3,197 days of gap-filled merged satellite chlorophyll-a data over the East China Sea from 2018 to 2026 across 422 spring harmful algal bloom survey windows (274 development windows in 2018--2022 and 148 test windows in 2023--2026). Results show that as the planning budget scales from 64 to 200,000 rollouts per decision, true route value in the real ocean saturates near 2,000 rollouts (rising from 0.749 to 0.793 and plateauing at 0.803) while the planner's internal search score keeps climbing to 0.917 (overestimating reality by 0.114), whereas evaluation on the 16 held-out imagined oceans remains within 0.005 of reality across all budgets; heavy GPU thinking pays off only when the baseline processor is too slow for the planning horizon, and stopping mid-mission to resample never pays in this domain; on the 148 test windows, classic one-step metareasoning spends 65\% of intervals thinking on the GPU and 28\% stopped to think, degrading time-averaged regret by 0.017 to 0.021 relative to per-vehicle tuned strategies, whereas pre-mission rehearsal achieves time-averaged regrets of 0.276 and 0.265 on slow and moderate compute platforms respectively, matching oracle per-vehicle tuning within $+0.007$ and $-0.001$. This work elucidates the mechanism of overthinking bias in embodied trajectory planning and establishes a tuning-free, self-calibrating meta-control paradigm for ocean-big-data-driven autonomous observation.

\vspace{1em}
\noindent\textbf{Keywords: }Ocean big data; Autonomous underwater vehicle; Metareasoning; Data assimilation; Harmful algal bloom survey; Thinking-acting trade-off


########## ATTACHED FILE: draft1_body.tex (draft 1, sections/body.tex) ##########

\section{绪论}

\subsection{具身智能体在动态自然环境中的思考与行动权衡}

携带先验环境底图的具身移动智能体在未知或动态演化的自然环境中执行探索任务时，必须在“深入思考”与“立即行动”之间持续做出资源分配决策\cite{horvitz1987reasoning, russell1991right, shen2025thinking}。与运行在充裕算力服务器上的纯软件智能体不同，部署于野外的自主移动平台受制于严格的机载电池能量上限、受限的嵌入式计算速率以及不可逆的物理作业时间窗口\cite{xiao2020thinking, magnino2026metareasoning}。当智能体依托大规模历史观测构建的先验底图进入真实物理场时，先验底图虽能提供大尺度空间结构线索，却不可避免地因环境演化与观测盲区而存在时效性滞后与小尺度失真\cite{jiang2015horizon}。智能体若仅凭粗糙的瞬时规划仓促行动，极易在复杂的局部梯度中迷失方向，错失核心目标区域；反之，若频繁唤醒高功耗加速计算模块在内部底图模型上开展高强度轨迹推演，或关停推进系统在原地反复采样以压低局部感知噪声，则会直接挤占用于长距离空间机动的宝贵时间与推进电能\cite{cuadron2025overthinking, elboher2023formal}。因此，如何在算力受限、能量受限与底图失真的三重耦合约束下，科学界定内部规划推演与外部物理采样的收益边界，构成了实时科学计算与智能导航交叉领域的核心科学问题\cite{hunt2021formalizing}。

在并发控制架构下，智能体的机体机动与大脑规划虽可在同一时间步内并行执行，但两者的资源竞争关系依然通过电能消耗与决策延迟紧密交织\cite{xiao2020thinking, elboher2023formal}。一方面，维持基础巡航仅需后台低功耗处理器以较低频率更新路径，而开启嵌入式GPU进行高吞吐量轨迹搜索则会显著抬升整机功耗，直接缩短电池耗尽前的总航行里程；另一方面，若智能体选择关停推进电机以降低航行功耗并提高局部水体采样密度，虽能节约推进能量，却牺牲了在有限时间窗口内横跨大尺度空间寻找全局极值的机动能力。更为深刻的是，智能体的“思考”完全建立在其内部持有的环境概率模型之上：当内部模型存在固有的先验不确定性时，单纯增加规划器的搜索算力能否真正转化为物理世界中的采样收益，取决于规划器的搜索深度是否已触及先验底图的信息上限\cite{jiang2015horizon, smith2006curse}。

\subsection{海洋大数据驱动的东海赤潮应急巡测场景}

将上述通用决策问题置于海洋科学应用场景，卫星遥感大数据支撑下的东海有害赤潮应急机动巡测提供了一个极具代表性的真实试验场\cite{fossum2019, lou2014diurnal}。有害赤潮是海洋浮游植物在特定水文气象条件下暴发性增殖引起的水体变色与生态灾害现象；根据自然资源部发布的海洋灾害公报，我国海域仅2023年即发现赤潮46次，累计面积约1500平方千米，其中有毒有害赤潮达29次\cite{mnr2024bulletin}。在浙江近海与长江口外海域，晚春至初夏时节频繁暴发以东海原甲藻为优势种的大规模赤潮，高密度藻华斑块的叶绿素a浓度（反映水体浮游植物生物量与赤潮密度的核心光学指标）常超过$6\text{ mg m}^{-3}$，并在潮汐与表层海流驱动下发生快速的日际漂移与形态演变\cite{lou2014diurnal}。在赤潮应急响应中，岸基指挥中心亟需派遣自主水下航行器（AUV，一种无需母船实时缆控、依靠机载能源与智能算法自主航行采样的水下机器人）深入暴发海域，在24小时黄金应急窗口内尽早定位叶绿素浓度最高的核心水体，并随时响应岸基中心的位置查询\cite{fossum2019, remus100}。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_overview}
  \caption{海洋大数据驱动的AUV赤潮应急巡测与“思考—行动”资源分配框架总览。中央主视图展示东海测试任务窗口（2025年4月4日）的三维海洋叶绿素场、驶向赤潮核心区（黄色圆环）的AUV及其轨迹（蓝色为低功耗后台规划巡航段，橙色为唤醒GPU深度思考段），海面上方悬浮6个假想海洋切片（4个深蓝边框样本供规划器搜索，2个橙色边框样本留出用于无偏评估）及提供先验底图的遥感卫星。侧边子图：（A）八年卫星叶绿素遥感序列及底图随滞后天数的退化过程；（B）航行器内部48个假想海洋的搜索集（32个）与留出集（16个）解耦架构，以及出发前对五种时间分配策略的闭环预演机制；（C）每20分钟决策周期内的机体与算力选项、电池功耗分配及向岸基指挥中心实时输出的最高浓度水体位置估计。}
  \label{fig:overview}
\end{figure}

卫星海洋水色遥感大数据为AUV巡测提供了不可或缺的大尺度先验视野，但其固有的时空分辨率限制与时效性滞后决定了现场自主观测的不可替代性\cite{beckers2003dineof, ye2021cocts}。由于东海春夏季节云雨频繁，原始光学卫星影像存在大面积云层遮挡，业务化海洋大数据产品通常采用经验正交函数缺失数据插值重构算法（一种利用时空矩阵低秩特征填补云层盲区的统计重构方法）生成空间完整、分辨率为2千米的逐日融合叶绿素底图\cite{beckers2003dineof}。然而，如图\ref{fig:overview}所示，当AUV抵达现场时，受卫星过境周期、地面反演处理及插值平滑滞后的影响，机载装订的往往是1至3天前的滞后底图；加之重构算法抹平了次中尺度锋面与小尺度丝状藻华结构，且近岸浑浊水体反演存在显著本底偏差\cite{ye2021cocts}，真实海洋的赤潮核心位置与滞后卫星底图之间往往存在十余千米的空间偏移与显著的幅值涨落。因此，AUV必须将卫星大数据转化为概率化的先验认知，一边通过机载荧光计实时测量沿途水体叶绿素浓度以修正内部底图，一边动态权衡算力、电能与航时分配。

\subsection{现有元推理与自适应采样方法的局限及本文贡献}

面对机载算力与采样行动的资源分配难题，直接套用直观的启发式规则、经典单步元推理或离线强化学习策略均会因海洋环境与规划器的内在特性而失效。第一种直观做法是预设单一的固定分配规则（例如全程低功耗巡航，或按固定比例唤醒GPU思考），但固定规则无法兼顾不同硬件平台的算力差异：在算力孱弱的平台上全程巡航会因轨迹搜索不充分而陷入局部次优，而在算力充裕的平台上频繁开启高功耗GPU则会白白消耗推进电能并缩短有效航时。第二种做法是采用人工智能领域的经典单步元推理框架\cite{horvitz1987reasoning, russell1991right, lin2015metareasoning, sung2021quit}，即在每个决策步在线比较“多思考一步的计算价值”与“多采样一步的信息价值”；然而，经典方法直接利用规划器在搜索集合上的内部得分跃升来估计计算价值，忽略了连续轨迹优化在高预算下对有限样本集合的严重过拟合——即决策分析中的“优化器诅咒”\cite{smith2006curse, vanhasselt2010double}，导致规划器在真实收益早已饱和后仍误以为继续思考大有裨益，从而陷入持续消耗电能的“过度思考”陷阱\cite{cuadron2025overthinking}。第三种做法是从历史巡测任务结果中直接训练策略选择网络\cite{magnino2026metareasoning}；但在真实赤潮场景中，不同任务窗口间的自然环境复杂度差异（遗憾值标准差约0.08）远大于不同优良策略之间的平均性能差距（通常不超过0.01），极低的信噪比使得离线学习极易过拟合历史环境噪声。此外，试图单纯依靠深度学习时空预测模型外推卫星底图以消除先验滞后的做法\cite{assran2025vjepa2}，同样因日际小尺度湍流与生物生长过程的随机性而无法超越持续性基线。

为突破上述瓶颈，本文跳出“依赖内部搜索轨迹做单步短视评估”与“依赖历史任务结果做离线拟合”的传统定式，提出利用海洋大数据校准不确定性、通过搜索与评估集合解耦消除过思考偏差，并在出发前开展全任务周期假想预演的自校准元控制方法。本文的核心贡献概括如下：
\begin{enumerate}
  \item \textbf{揭示了连续轨迹规划中的过思考偏差机理并提出搜索—留出双集合解耦架构：} 将AUV内部维护的48个假想海洋严格划分为32个搜索样本与16个留出验证样本；实证发现当规划推演预算跨越四个数量级增长时，规划器在搜索集上的自评得分持续虚高，而留出集评估值与真实海洋收益之差始终稳定在0.005以内，从根本上解决了有限集合规划中的价值高估难题。
  \item \textbf{阐明了海洋移动采样中“思考—巡航—停航重采样”的硬件与环境相图规律：} 基于东海八年3197天遥感大数据与422个赤潮任务窗口，定量刻画了卫星底图时效性退化图谱，证明了深度学习时空外推无法替代现场观测，并揭示出高功耗GPU深度思考仅在基础算力不足以覆盖有效规划视野时产生净收益，而巡航途中停航漂移重采样在中尺度相关场中始终得不偿失。
  \item \textbf{提出了基于留出假想海洋的行前闭环预演元控制器：} 在任务出发前以留出假想海洋为合成真实环境，结合真实机载算力速率与电池功耗模型，采用共同随机数对候选时间分配策略开展24小时全周期闭环预演；该方法无需任何针对特定硬件的历史任务调参，即可在不同算力平台上自动逼近事后最优调参策略，并显著优于单一固定规则与经典单步元推理。
\end{enumerate}

\section{东海赤潮遥感大数据特征与先验不确定性量化}

\subsection{八年多源融合叶绿素遥感数据集与赤潮任务窗口构建}

构建高保真度的海洋自主采样仿真基准，必须依托长时序、无缝隙且具备真实地球物理统计特征的卫星遥感大数据。由于单颗极轨水色卫星受刈幅宽度与云层遮挡限制难以提供连续的每日海洋表面视图，本文选用美国国家海洋和大气管理局海岸观测网发布的每日多源融合叶绿素a浓度遥感产品作为核心海洋大数据底座（公共领域开放许可，数据集标识为\texttt{noaacwNPPN20S3ASCIDINEOF2kmDaily}）。该数据集融合了搭载于苏奥米国家极地轨道伙伴卫星与美国国家海洋和大气管理局20号卫星上的可见光红外成像辐射仪，以及搭载于哨兵三号甲星上的海洋陆地颜色仪观测数据，并采用经验正交函数缺失数据插值重构算法对云层遮挡区域进行时空一致性重构\cite{beckers2003dineof}。数据空间分辨率为2千米，时间分辨率为逐日，时间跨度覆盖2018年1月1日至2026年10月23日共3197天；研究区域截取东海核心海域（北纬$25^\circ\text{--}33^\circ$，东经$119.5^\circ\text{--}127^\circ$），每日构成$385\times 361$个空间网格像素。同时，为检验多模态海洋环境变量对赤潮演变的辅助预测能力，本文同步引入美国喷气推进实验室发布的多尺度超分辨率海表温度每日无云产品（版本4.1，数据集标识为\texttt{jplMURSST41}）\cite{chin2017mur}，将其从原始$0.01^\circ$分辨率重采样至$0.04^\circ$以匹配水色网格。因海洋叶绿素a浓度在空间上呈典型的对数正态分布，跨越数个数量级，本文所有叶绿素数值、误差统计与遗憾值指标均在以10为底的对数空间（即$\log_{10}(\text{叶绿素a浓度}/\text{mg m}^{-3})$）下定义与计算。

为确保实验评估聚焦于具有真实应急响应价值的离岸赤潮暴发事件，本文制定了严格的地球物理筛选准则，从八年春季至初夏序列中提取标准化的任务窗口。具体而言，首先在每年4月至6月的赤潮高发期内，搜索浙江近海陆架区域（北纬$26.5^\circ\text{--}31.5^\circ$，东经$121.5^\circ\text{--}125^\circ$）离岸距离至少30千米处、经空间平滑后局部极值超过$5\text{ mg m}^{-3}$的显著藻华中心；随后以该极值点为基准，施加最高达16千米的随机空间偏移以防止目标恒定处于区域几何中心，进而截取$80\text{ km}\times 80\text{ km}$（对应$40\times 40$个2千米网格单元）的正方形海域作为单次巡测任务窗口。为保障AUV航行安全并确保场内具备有意义的浓度梯度，将距离陆地或岛屿岸线15千米以内的网格标记为禁航区，仅保留可航行水域占比不低于80\%且窗内叶绿素对数浓度极差（对比度）不低于0.3的任务窗口。按此标准共筛选出422个高质量赤潮任务窗口；为严格杜绝跨年度数据泄露，按时间顺序将2018至2022年的274个窗口划分为开发集（用于先验误差统计校准与基线调参），将2023至2026年的148个窗口划分为完全独立的测试集。在每次任务开始时，AUV随机部署于任务窗口边界上的任一可航行网格点。

\subsection{卫星底图时效性退化图谱与小尺度海真偏差建模}

卫星遥感底图在AUV下水时刻的先验不确定性主要源于两个相互独立的物理过程：一是底图获取至任务执行期间（通常滞后1至3天）水体平流与生物生消引起的时效性退化，二是遥感反演与插值平滑相对于同日真实表层海水的次网格尺度表征偏差。通过对全部3197天东海叶绿素遥感序列进行滑动差分统计，本文绘制了3天滞后叶绿素对数浓度变化量的季节性空间分布图谱（图\ref{fig:atlas}）。统计结果显示，东海叶绿素场的3天变化剧烈程度具有显著的季节节律与空间非均质性：全海域中位数标准差在春季最高，达到0.127；夏季次之，中位数为0.107，但其空间分异极为强烈，全海域90\%分位数高达0.204，在浙闽沿岸流锋面与长江冲淡水羽流外缘形成了一条标准差高达0.25至0.30的强动态变化带；秋季与冬季则逐步减弱，全海域中位数分别降至0.103与0.081。在274个春季开发集赤潮任务窗口内部，真实目标日底图减去$k$天前滞后底图的时效性退化误差统计表明，当滞后天数$k=1, 2, 3$天时，误差标准差分别为$s_1=0.125$、$s_2=0.176$与$s_3=0.210$，空间自相关特征尺度约为$\ell=5$个网格单元（即10千米），且伴随$+0.016$、$+0.032$与$+0.045$的微弱正均值偏置（反映了赤潮暴发初期藻华生物量整体处于净增长阶段的统计特征）。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_atlas}
  \caption{东海海域（北纬$25^\circ\text{--}33^\circ$，东经$119.5^\circ\text{--}127^\circ$）八年3197天卫星叶绿素对数浓度3天变化幅度的四季气候态分布图谱。陆地区域以灰色标示；春季子图中叠加了全部422个赤潮巡测任务窗口的中心位置，其中蓝色圆点为2018至2022年开发集窗口（274个），绿色圆点为2023至2026年测试集窗口（148个）。浙闽沿岸与长江冲淡水锋面在春夏两季呈现出显著的高动态变化特征。}
  \label{fig:atlas}
\end{figure}

除时间滞后外，即便是目标日当天的融合卫星底图也并非真实海洋的完美写照。一方面，经验正交函数插值重构算法在填补云区时截断了高阶奇异值，使重构场在时空上呈现明显的低通平滑特性\cite{beckers2003dineof}；另一方面，针对海洋一号丙星水色水温扫描仪在东海与南海叶绿素反演产品的现场比对验证表明，卫星遥感反演值与现场实测值之间存在约39\%的无偏相对百分比差异（折算至以10为底的对数空间约为0.15的均方根偏差）\cite{ye2021cocts}。为在仿真环境中忠实复现这一遥感底图无法分辨的次中尺度斑块结构，本文将任务窗口目标日的真实海洋叶绿素场$c(\mathbf{x})$建模为目标日卫星底图叠加一个空间相关的零均值高斯随机场，其基准标准差设为$s_{\text{sat}}=0.15$，空间相关尺度设为3个网格单元（6千米）；同时在机理相图实验中，将海真相对于卫星底图的偏离程度在$0.05$至$0.30$范围内开展全参数扫描，以全面检验不同遥感精度下的决策规律。

\subsection{深度时空世界模型外推的局限性与现场观测的不可替代性}

面对滞后1至3天的卫星底图，人工智能赋能科学计算领域最直观的改进思路是利用多年历史遥感序列训练一个深度时空预测模型（即“海洋世界模型”），在AUV下水前直接将滞后底图向前推演至任务当日，从而在源头上消除底图的时效性退化。为严格检验这一技术路线在真实东海赤潮场景中的有效性，本文构建了一个参数量为550万的联合嵌入预测架构网络\cite{assran2025vjepa2}，以连续多日叶绿素a浓度场与同步海表温度场\cite{chin2017mur}作为多模态输入，利用2018至2021年每年3月至6月的历史序列进行训练，并在2022年验证集上进行超参数优选与早停控制，旨在预测未来1至3天的叶绿素场演变。

然而，在2023至2026年独立测试集上的系统评估给出了明确的否定性结论：深度时空世界模型对未来1至3天重构叶绿素场的预测精度未能超越最简单的“持续性基线”（即直接将最新可用的滞后底图作为未来预测值）。具体而言，在提前1天、2天与3天的预测任务中，深度学习模型的测试集均方根误差分别为0.1229、0.1439与0.1487，而直接沿用滞后底图的持续性基线均方根误差分别为0.1226、0.1439与0.1474；即使在2022年验证集上，深度学习模型相对于持续性基线的误差降幅也仅为微不足道的1.4\%，且其预测集合的离散度与真实误差之比仅为0.70至0.93，存在明显的方差低估倾向。这一结果具有深刻的物理与信息论根源：首先，业务化插值重构底图本身已是经时空低秩滤波后的平滑场，其中可由大尺度历史轨迹确定性外推的低频趋势分量在1至3天尺度上变化极慢，持续性假设已近似最优；其次，真正决定赤潮峰值斑块日际位移的10千米级次中尺度涡丝、潮致锋面摆动以及藻华非线性暴发增长，受控于未观测的局地风应力与营养盐脉冲，在粗分辨率日均遥感序列中属于不可预测的随机创新过程。因此，试图依靠离线神经网络外推来恢复小尺度赤潮峰值位置在物理上是不可行的；海洋大数据的正确打开方式，是从历史序列中精确校准先验误差的幅值与空间相关结构，进而指导AUV携带传感器深入现场开展自适应同化观测。

\section{随流参考系下的并发采样与能耗受限决策问题建模}

\subsection{随流漂移参考系与二十四小时随时遗憾值评价指标}

在潮汐与表层海流强劲的东海陆架区规划AUV巡测路径，若直接在固定于海底的欧拉地理参考系下建模，不仅需要高精度的实时三维海流预报场，还会使规划器耗费大量算力去处理水体整体的刚性平流运动。地球静止海洋水色成像仪对东海赤潮日内演变的高频追踪研究表明，表层浮游植物藻华斑块在日尺度上主要作为被动示踪物随表层水体同步漂移\cite{lou2014diurnal}。基于这一物理特性，本文将整个巡测运动学、环境场表征与数据同化过程完全建立在随表层水体同步漂移的拉格朗日参考系（下称随流漂移参考系）中。在该参考系下，赤潮叶绿素场相对于水体保持准静止状态，AUV以恒定的对水航速机动，无需为“追逐”随流漂移的藻华而与海流做无谓对抗；海流平流与剪切变形对先验认知的影响，则自然地内化于卫星底图从过境时刻至任务时刻的时效性退化误差统计之中。

在$40\times 40$个网格单元（分辨率2千米，总面积$80\text{ km}\times 80\text{ km}$）构成的任务窗口$\mathcal{X}$内，设真实海洋在网格点$\mathbf{x}\in\mathcal{X}$处的叶绿素a对数浓度为$c(\mathbf{x})$，全局真实最高浓度为$\max_{\mathbf{x}\in\mathcal{X}} c(\mathbf{x})$。在总时长为$T=24\text{ h}$的应急响应窗口内，岸基指挥中心可在任意时刻$t\in[0, T]$向AUV查询当前已探明的最密集赤潮水体位置。为防止AUV仅凭未经证实的先验猜测上报虚假极值，任务规程要求AUV必须从截至时刻$t$已实际造访并采样的网格集合$\mathcal{V}(t)\subseteq\mathcal{X}$中，选取当前内部同化后验均值$\bar{c}_t(\mathbf{x})$最高的网格点作为实时回报位置$\hat{\mathbf{x}}(t)$：
\begin{equation}
  \hat{\mathbf{x}}(t) = \arg\max_{\mathbf{x}\in\mathcal{V}(t)} \bar{c}_t(\mathbf{x})
  \label{eq:answer}
\end{equation}
若AUV在$24\text{ h}$结束前因电池能量耗尽而终止机动，其已访集合$\mathcal{V}(t)$与回报位置$\hat{\mathbf{x}}(t)$在剩余时间内保持冻结。为综合衡量AUV“尽早发现高浓度核心区”与“最终定位精度”的双重应急效能，本文定义24小时时间平均随时遗憾值（下称随时遗憾值）$R$作为核心评价指标：
\begin{equation}
  R = \frac{1}{T}\int_0^T \left[\max_{\mathbf{x}\in\mathcal{X}} c(\mathbf{x}) - c\big(\hat{\mathbf{x}}(t)\big)\right] dt
  \label{eq:regret}
\end{equation}
该指标度量了在整个24小时应急窗口内，真实全局最大叶绿素对数浓度与AUV实时回报位置处真实叶绿素对数浓度之差的时间积分均值（越低越好）。此外，本文同步记录任务结束时刻（$t=24\text{ h}$）的终点遗憾值，以及终点回报位置真实浓度落入全局极值$0.1$个对数单位以内（在线性浓度尺度上相当于偏差不超过26\%）的命中率。

\subsection{航行器机电功耗模型与二十分钟并发决策周期}

为真实刻画移动观测中的能量与算力耦合约束，本文依照百米级轻型AUV平台（以REMUS 100型平台技术参数为基准）\cite{remus100}与嵌入式边缘计算模块（以Jetson Orin NX级GPU模块为基准）\cite{jetsonorinnx}构建机电功耗模型。航行器搭载总容量为$E_{\max}=1\text{ kWh}$（即$1000\text{ Wh}$）的锂离子电池组，额定对水巡航速度为$v=1.5\text{ m/s}$（约3节）。在巡航状态下，整机基础功耗为$45\text{ W}$（对应约22.2小时的纯巡航续航时间），由两部分构成：一是无论航行或漂移均需持续供电的$P_{\text{hotel}}=15\text{ W}$基础航电与传感器功耗（含导航、声学通信、荧光计及低功耗后台处理器），二是驱动螺旋桨以$1.5\text{ m/s}$航行的$P_{\text{prop}}=30\text{ W}$推进功耗。在计算单元方面，低功耗后台处理器常驻运行，其功耗已包含在$15\text{ W}$基础航电中，每分钟可执行$r_{\text{base}}\in[5, 200]$次轨迹推演（取决于具体硬件配置）；当需要深度规划时，航行器可唤醒嵌入式GPU加速模块，其推演吞吐量提升至后台处理器的50倍（即$50\,r_{\text{base}}$），但在基准配置下需额外消耗$P_{\text{gpu}}=20\text{ W}$电能（在高效能专用加速器扩展配置下额外功耗为$5\text{ W}$）。

整个24小时任务被划分为72个时长$\Delta t = 20\text{ min}$（即$1/3\text{ h}$）的离散并发决策周期\cite{xiao2020thinking, elboher2023formal}。在每个20分钟周期开始时，元控制器需同时为“机体”与“大脑”下达动作指令：
\begin{itemize}
  \item \textbf{机体动作选项：}（1）\textbf{巡航采样}，即开启推进电机（$30\text{ W}$），沿当前生效的规划路径以$1.5\text{ m/s}$航行$18\text{ km}$（跨越约9个2千米网格），机载荧光计每航行$1\text{ km}$采集1个独立样本（单周期共采集18个样本，每个2千米网格内平均获得2至3次独立测量）；（2）\textbf{停航漂移重采样}，即关停推进电机（推进功耗降至$0\text{ W}$，仅保留$15\text{ W}$基础航电），在随流漂移参考系下驻留于当前网格位置，荧光计每$4\text{ min}$采集1个独立样本（单周期共采集5个原位样本），以通过多次重复测量压低局部传感器随机噪声。每个独立荧光计样本的测量方程为：
  \begin{equation}
    y = c(\mathbf{x}) + \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, \sigma_{\text{obs}}^2)
    \label{eq:obs}
  \end{equation}
  其中测量噪声标准差为$\sigma_{\text{obs}} = 0.1$。
  \item \textbf{大脑算力选项：}（1）\textbf{后台常规划}，即仅依靠低功耗处理器在20分钟内执行$20\,r_{\text{base}}$次轨迹推演（额外功耗$0\text{ W}$）；（2）\textbf{深度思考规划}，即唤醒GPU在20分钟内执行$1000\,r_{\text{base}}$次轨迹推演（额外功耗$P_{\text{gpu}}$）。
\end{itemize}
计算与机动在周期内完全并发运行：规划器在当前20分钟周期内读取最新同化后的假想海洋集合，并以航行器在当前周期结束时刻的预计到达位置作为新轨迹的起点（即精确时延补偿），搜寻最优后续路线；待当前20分钟周期结束时，新规划出的路线无缝替换旧路线并投入下一周期执行。当累计消耗电能达到$1\text{ kWh}$或任务时间满24小时时，任务立即终止。

\section{基于留出假想海洋的集合同化与行前预演元控制方法}

\subsection{数据校准的假想海洋先验集合与序列局地化同化更新}

为使AUV在缺乏确定性未来底图的条件下具备概率化的空间推理能力，本文不再让航行器维护单一的静态点估计底图，而是围绕滞后$k$天的卫星底图$c_{\text{map}}(\mathbf{x})$构建由$N=48$个“假想海洋”（即先验高斯随机场实现样本）组成的集合记忆库。基于第2.2节从八年遥感大数据中校准得到的误差统计量，第$i$个假想海洋样本$c^{(i)}(\mathbf{x})$在任务初始时刻（$t=0$）按如下公式生成：
\begin{equation}
  c^{(i)}(\mathbf{x}) = c_{\text{map}}(\mathbf{x}) + \sigma_k\, z^{(i)}(\mathbf{x}), \quad i = 1, 2, \dots, 48
  \label{eq:prior}
\end{equation}
式中，$\sigma_k = \sqrt{s_k^2 + s_{\text{sat}}^2}$为融合了$k$天底图滞后误差标准差$s_k$与海真小尺度偏离标准差$s_{\text{sat}}=0.15$的合成先验不确定性幅值（例如当底图滞后$k=3$天时，$s_3=0.210$，合成标准差$\sigma_3 \approx 0.258$）；$z^{(i)}(\mathbf{x})$为具有零均值、单位方差及平方指数空间协方差结构的独立同分布高斯随机场，其空间相关长度设为校准值$\ell = 5$个网格单元（10千米）：
\begin{equation}
  \text{Cov}\big(z^{(i)}(\mathbf{x}), z^{(i)}(\mathbf{x}')\big) = \exp\left(-\frac{\|\mathbf{x} - \mathbf{x}'\|_2^2}{2\ell^2}\right)
  \label{eq:cov}
\end{equation}
这48个假想海洋共同编码了航行器对当前海域赤潮空间分布的先验信念：每个样本本身都是一幅具有逼真次中尺度斑块结构的完整可能海洋，而48个样本之间的离散度则精确反映了先验底图的不确定性空间分布。

当AUV在巡航或漂移过程中获取到现场荧光计观测序列时，必须实时将点位测量信息传播至周围未观测网格并压缩集合不确定性。若采用标准蒙特卡洛集合卡尔曼滤波直接更新包含1600个网格点的状态向量，一方面向观测值人为注入随机扰动会引入额外的采样方差，另一方面仅用48个样本估计1600维协方差矩阵会产生严重的远距离伪相关，导致几十千米外的无关网格发生非物理跳变。因此，本文采用确定性的序列集合调整卡尔曼滤波算法\cite{anderson2001eakf}，并耦合五阶分段有理局地化函数\cite{gaspari1999correlation}对每个独立观测$y$进行逐一序列同化。具体而言，当在位置$\mathbf{x}_{\text{obs}}$获得观测$y$时，首先计算集合在该网格处的先验均值$\bar{c}_{\text{obs}}$与先验方差$\sigma_{\text{prior}}^2$，利用卡尔曼方差缩减公式精确调整该点处的集合离散度以匹配理论后验方差$\sigma_{\text{post}}^2 = (\sigma_{\text{prior}}^{-2} + \sigma_{\text{obs}}^{-2})^{-1}$，得出观测点处第$i$个样本的状态增量$\Delta c_{\text{obs}}^{(i)}$；随后，通过集合样本回归系数及以$2\ell$（10个网格单元，即20千米）为半宽尺度的局地化截断权重$\rho(\|\mathbf{x}-\mathbf{x}_{\text{obs}}\|_2 / 2\ell)$，将观测增量平滑映射至邻近网格：
\begin{equation}
  c_{\text{post}}^{(i)}(\mathbf{x}) = c_{\text{prior}}^{(i)}(\mathbf{x}) + \rho\left(\frac{\|\mathbf{x}-\mathbf{x}_{\text{obs}}\|_2}{2\ell}\right) \frac{\text{Cov}_{\text{ens}}\big(c(\mathbf{x}), c(\mathbf{x}_{\text{obs}})\big)}{\sigma_{\text{prior}}^2} \Delta c_{\text{obs}}^{(i)}, \quad i = 1, \dots, 48
  \label{eq:eakf}
\end{equation}
上述同化机制无需对高维矩阵求逆，单次观测更新耗时仅亚毫秒级，既保证了48个假想海洋在每次观测后严格满足贝叶斯后验均值与方差一致性，又将观测信息严格限制在物理合理的空间相关半径之内。

\subsection{轨迹规划中的优化器诅咒与搜索—留出双集合解耦机制}

在每个20分钟决策周期内，规划器的任务是从下一周期起点出发，在连续二维空间中搜寻一条能够在剩余任务时间$T_{\text{left}}$内最大化高浓度水体发现收益的后续航行路线。为在保持轨迹几何灵活性的同时控制搜索空间维度，本文将候选路线参数化为由当前预计终点$\mathbf{x}_0$依次连接两个中间航路点$(\mathbf{w}_1, \mathbf{w}_2)\in\mathcal{X}^2$构成的连续折线轨迹（共4个连续坐标自由度）。将一条候选路线在某一个假想海洋样本$c^{(i)}$上完整推演一次称为一次“推演”（rollout）：假设航行器沿该折线以巡航速度$v$航行，记推演时刻$\tau\in[0, T_{\text{left}}]$沿途已遇见的最高叶绿素浓度为$m_i(\tau)$（其初值$m_i(0)$设为当前已访网格集合上的最高后验均值估计，且一旦剩余可用巡航电池时间耗尽，$m_i(\tau)$即保持冻结），则该候选路线在第$i$个假想海洋上的路线价值$V_i$定义为剩余窗口内的时间积分均值：
\begin{equation}
  V_i(\mathbf{w}_1, \mathbf{w}_2) = \frac{1}{T_{\text{left}}}\int_0^{T_{\text{left}}} m_i(\tau)\, d\tau
  \label{eq:route_value}
\end{equation}
式\eqref{eq:route_value}将全局随时遗憾值目标（式\eqref{eq:regret}）直接映射至单次轨迹推演层面：越早穿过高浓度斑块，函数$m_i(\tau)$越早跃升至高位，积分均值$V_i$也就越高。在给定推演预算下，规划器采用跨周期热启动的交叉熵搜索算法\cite{deboer2005cem}迭代更新航路点$(\mathbf{w}_1, \mathbf{w}_2)$的高斯采样分布，不断向高价值轨迹区域聚焦。

然而，若让交叉熵规划器在全部48个假想海洋上评估并搜索最优路线，同时又用这48个假想海洋上的平均得分来判断“增加算力是否提升了路线质量”，系统将不可避免地陷入严重的“优化器诅咒”\cite{smith2006curse, vanhasselt2010double}。其数学机理在于：有限个假想海洋样本只是真实先验分布的有限蒙特卡洛抽样；当规划推演预算成百上千倍增加时，优化器拥有极高的自由度去精细微调折线转折点，使其恰好擦过这组特定样本中偶然重合的随机正涨落峰值。此时，规划器在内部样本集上观测到的目标函数值会随算力增加而持续虚高，但在未参与搜索的真实海洋中，这些针对样本噪声的微调根本无法带来任何实际收益。

为彻底切断搜索过程与价值评估之间的正向选择偏差，本文借鉴双Q学习中解耦动作选择与价值评估的思想\cite{vanhasselt2010double}，提出搜索—留出双集合解耦架构（图\ref{fig:overview}B）：将48个假想海洋固定划分为两个互不相交的子集——前32个样本构成**搜索集合**$\mathcal{I}_{\text{search}}=\{1,\dots,32\}$，后16个样本构成**留出验证集合**$\mathcal{I}_{\text{hold}}=\{33,\dots,48\}$。在现场同化阶段，全部48个样本均按式\eqref{eq:eakf}同步吸收真实荧光计观测，确保两个子集始终代表相同的后验知识状态；但在轨迹规划阶段，交叉熵优化器仅被允许访问32个搜索样本，通过最大化搜索集均值来选定最优航路点$(\mathbf{w}_1^*, \mathbf{w}_2^*)$：
\begin{equation}
  (\mathbf{w}_1^*, \mathbf{w}_2^*) = \arg\max_{(\mathbf{w}_1, \mathbf{w}_2)} \frac{1}{32}\sum_{i=1}^{32} V_i(\mathbf{w}_1, \mathbf{w}_2)
  \label{eq:cem_search}
\end{equation}
而对于选定的路线$(\mathbf{w}_1^*, \mathbf{w}_2^*)$，其真实的预期收益则完全交由从未参与搜索的16个留出样本进行独立无偏评估：
\begin{equation}
  \hat{V}_{\text{hold}}(\mathbf{w}_1^*, \mathbf{w}_2^*) = \frac{1}{16}\sum_{i=33}^{48} V_i(\mathbf{w}_1^*, \mathbf{w}_2^*)
  \label{eq:hold_eval}
\end{equation}
由于16个留出样本与32个搜索样本共享相同的统计分布及已同化的观测约束，但其未观测区域的随机涨落与搜索集相互独立，式\eqref{eq:hold_eval}能够在完全不接触真实海洋的前提下，精确滤除优化器过拟合样本噪声产生的虚高泡沫。

\subsection{行前假想预演元控制器与对比基线设计}

在解决了单次规划的无偏评估问题后，核心决策难题聚焦于元控制层面：面对特定的机载算力速率、电池容量与当前底图不确定性，AUV究竟应如何在72个决策周期内分配“巡航”、“深度思考”与“停航重采样”？如前所述，经典单步元推理\cite{russell1991right, lin2015metareasoning}试图在每个周期在线比较单步计算价值（由规划器内部改进轨迹外推）与单步信息价值（由假想海洋上的预后验方差缩减估计），但这种短视局部近似既受制于内部搜索轨迹的过思考偏差，又无法预见当前开启GPU消耗的$20\text{ W}$额外功率将在20小时后导致电池提前耗尽、进而丧失最后几小时空间搜索能力的全局长程后果。与此同时，直接用历史任务结果训练策略选择器的做法则因不同任务窗口间高达0.08的自然遗憾值涨落掩盖了0.01量级的策略差异而失效。

既然单步短视评估无法捕捉全周期能量耦合，而跨任务历史学习又受困于环境背景噪声，最直接且严密的破局之道便是在**同一任务窗口内部**、利用航行器自身已校准的假想海洋开展全任务周期的闭环沙盘推演。为此，本文提出**行前假想预演元控制器**（Pre-Mission Rehearsal in Imagination）。首先，提炼出覆盖“行动、思考、停航”基本组合空间的五种代表性时间分配策略构成候选策略集$\mathcal{S}=\{s_1, s_2, s_3, s_4, s_5\}$：
\begin{enumerate}
  \item \textbf{全程巡航（$s_1$）：} 所有周期均保持$1.5\text{ m/s}$巡航采样，仅使用后台低功耗处理器规划（整机功耗$45\text{ W}$）；
  \item \textbf{全程深度思考（$s_2$）：} 所有周期均在巡航采样的同时开启GPU深度思考（整机功耗$65\text{ W}$，基准配置下约15.4小时耗尽电池）；
  \item \textbf{三分之一间歇思考（$s_3$）：} 全程保持巡航采样，每3个周期中开启1个周期的GPU深度思考，其余2个周期使用后台规划（平均功耗约$51.7\text{ W}$，续航约19.3小时）；
  \item \textbf{三分之一停航思考（$s_4$）：} 每3个周期中，有1个周期关停推进器随流漂移并开启GPU深度思考（功耗$35\text{ W}$），其余2个周期巡航并使用后台规划（平均功耗约$41.7\text{ W}$，续航达24小时上限）；
  \item \textbf{三分之一停航重采样（$s_5$）：} 每3个周期中，有1个周期关停推进器随流漂移开展原位密集重采样且仅用后台规划（功耗$15\text{ W}$），其余2个周期巡航并使用后台规划（平均功耗$35\text{ W}$，续航达24小时上限）。
\end{enumerate}

在AUV正式下水出发前（$t=0$，位于母船甲板或水面待命阶段），行前假想预演按如下闭环流程自动选定当前任务的最优策略：从16个留出假想海洋$\mathcal{I}_{\text{hold}}$中抽取$M=4$个样本$\{c^{(j)}\}_{j=1}^4$，将其分别视作假想世界中的“合成真实海洋”。对于每一个合成真实海洋$c^{(j)}$和每一种候选策略$s\in\mathcal{S}$，仿真器调用AUV自身的序列集合调整卡尔曼滤波器、交叉熵规划器、真实的机载基础算力速率$r_{\text{base}}$、真实的GPU加速倍率及真实的$1\text{ kWh}$电池功耗模型，在内部完整推演一遍24小时（72个周期）的闭环巡测任务，计算得出策略$s$在合成真实海洋$c^{(j)}$上的假想随时遗憾值$R_{s,j}$。为最大限度压低4个样本间的蒙特卡洛评估方差，五种候选策略在同一个合成真实海洋$c^{(j)}$上推演时，严格共享完全相同的初始先验集合与随机数种子（即共同随机数方差缩减技术），从而彻底剥离环境背景难度的干扰，纯粹度量策略间的相对优劣。最终，AUV选择在4个留出合成真实海洋上平均假想遗憾值最低的策略$s^*$作为本次实海任务的执行策略：
\begin{equation}
  s^* = \arg\min_{s\in\mathcal{S}} \frac{1}{4}\sum_{j=1}^4 R_{s,j}
  \label{eq:rehearsal}
\end{equation}

为全面剖析本文方法的内在机理，实验部分设置四类对比基线：（1）五种单一固定策略（$s_1$至$s_5$）；（2）**特定硬件开发集最优调参策略（Tuned）**，即针对每一类硬件平台，利用2018至2022年120个开发集任务窗口事后统计出平均随时遗憾值最低的固定策略，代表需要大规模历史任务试错才能获得的先验上限；（3）**经典单步元推理（One-Step Metareasoning）**\cite{russell1991right}，在每个20分钟周期在线对比规划器内部搜索改进率与假想海洋预后验采样收益以动态决定机体与算力动作；（4）**自评预演对照（Rehearsal on Searched Truths）**，其预演流程与式\eqref{eq:rehearsal}完全一致，唯一的区别是从32个搜索集样本$\mathcal{I}_{\text{search}}$（而非留出集$\mathcal{I}_{\text{hold}}$）中抽取4个合成真实海洋，用于检验闭环全任务预演对合成真值来源的敏感性。

\section{实验结果与分析}

\subsection{规划预算扩展下的过思考偏差与留出集合的无偏性验证}

实验首先检验第4.2节提出的第一项核心论断：当单步轨迹规划的推演预算大幅扩展时，规划器自身的内部搜索得分是否会因优化器诅咒而背离真实海洋收益，以及16个留出假想海洋能否提供准确的无偏校准。为此，在开发集抽取的80个赤潮任务窗口上（每个窗口运行3组独立随机种子，共240次实验，装订滞后3天的卫星底图，考察任务前8小时的规划表现），将每次决策的交叉熵搜索推演预算从64次跨越四个数量级逐步扩展至200,000次，同步记录所选路线在32个搜索样本上的规划器内部自评得分、在16个留出假想海洋上的独立评估得分以及在真实海洋中的实际路线价值（图\ref{fig:curse}）。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_curse}
  \caption{轨迹规划推演预算从64次扩展至200,000次时的优化器诅咒与留出假想海洋无偏校准验证（80个开发集窗口$\times 3$个随机种子，3天滞后底图）。（a）规划路线价值随单次决策推演次数的变化曲线：真实海洋实际价值（黑色实线）与16个留出假想海洋评估值（蓝色虚线）在约2,000次推演后同步趋于平坦，而规划器在32个搜索样本上的内部搜索得分（红色实线）持续陡峭攀升；（b）估计值减去真实海洋价值的评估偏差曲线：内部搜索得分在高预算下产生高达$+0.114$的正向虚高偏差，而基于数据校准不确定性的留出集评估偏差在全预算跨度内始终保持在$0.005$以内；灰色点线展示先验不确定性幅值人为减半（$0.5\times$）或放大（$1.5\times$）时的留出集偏差平移特性。}
  \label{fig:curse}
\end{figure}

如图\ref{fig:curse}a所示，真实海洋中的路线价值随推演预算的增长呈现出显著的边际效益递减与饱和规律：当单次决策推演预算从64次增至2,000次时，真实路线价值从0.749显著提升至0.793（净增$+0.044$），说明在低算力区间增加轨迹搜索确实能够有效规避局部次优、找出穿透高浓度区的走廊；然而，当推演预算从2,000次再激增一百倍至200,000次时，真实海洋路线价值仅从0.793微弱增长至0.803（净增仅$+0.010$），绝大部分真实规划红利在2,000次推演处即已宣告枯竭。与之形成鲜明反差的是，规划器在32个搜索样本上的内部得分（图\ref{fig:curse}a红线）完全无视这一物理饱和边界，从64次推演时的0.762一路加速攀升至2,000次时的0.833，并在200,000次推演时达到惊人的0.917，相对于真实海洋价值产生了高达$+0.114$的虚假乐观偏差（图\ref{fig:curse}b）。这一现象直观印证了连续轨迹规划中的优化器诅咒：当搜索算力过剩时，交叉熵算法通过精巧扭曲折线航路点，专门迎合了32个搜索样本在未观测区域中偶然出现的局部随机正噪点；依赖内部得分的元推理器正是被这一不断膨胀的虚假增量所欺骗，误以为继续投入GPU算力仍在产生丰厚回报。

与之相反，将完全相同的规划路线置于从未参与搜索的16个留出假想海洋上进行评估（图\ref{fig:curse}a蓝线），其得分在64次、2,000次与200,000次推演下分别为0.745、0.794与0.802，与真实海洋价值曲线（0.749、0.793、0.803）近乎完美重合；在横跨四个数量级的全部预算范围内，留出集评估均值与真实海洋实际价值之差始终控制在$0.005$以内（图\ref{fig:curse}b）。更进一步地，当故意破坏先验不确定性校准精度，将生成假想海洋的先验标准差$\sigma_k$人为减半（$0.5\times$）或放大至1.5倍（$1.5\times$）时（图\ref{fig:curse}b灰色点线），留出集评估的绝对水平虽分别产生了$-0.06$与$+0.07$的常数基线偏移，但其对“预算从64次增至200,000次所获相对增益”的估计依然高度稳健：减半与放大不确定性下的留出集评估增益分别为$+0.059$与$+0.054$，与对应工况下的真实海洋实际增益（$+0.054$与$+0.047$）高度吻合。这证明搜索—留出双集合解耦不仅在先验准确校准时具备零偏特性，即便在先验幅值存在一定失配时，依然能够准确捕捉增加算力的边际收益拐点。

\subsection{算力与底图误差耦合相图及停航重采样失效机理分析}

在明确了单步规划的算力饱和规律后，实验进一步考察全任务周期内不同固定分配策略在机载算力速率与底图失真程度二维参数空间中的胜出规律（图\ref{fig:phase}）。通过在后台低功耗处理器速率$r_{\text{base}}\in[5, 200]\text{ 推演/min}$与海真相对于卫星底图偏离标准差$s_{\text{sat}}\in[0.05, 0.30]$构成的网格上开展系统扫描，相图清晰地揭示出具身移动采样中硬件能力与环境不确定性的交互边界\TBD{相图最终扫描完成后的具体分界数值补充}。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_phase}
  \caption{机载低功耗处理器速率（每分钟5至200次推演）与真实海洋相对于卫星底图偏离程度（0.05至0.30）二维参数空间中的最优固定策略相图。网格颜色标示五种固定时间分配策略中表现最优的策略类别，网格内数值表示该最优策略相对于“全程巡航（Always Go）”策略降低的随时遗憾值收益。}
  \label{fig:phase}
\end{figure}

从图\ref{fig:phase}及测试集定量结果可以提炼出三条清晰的物理规律。第一，**开启高功耗GPU深度思考仅在机载基础算力相对于规划问题过慢时才具有显著正收益**。当AUV搭载慢速后台处理器（$r_{\text{base}}=5\text{ 推演/min}$）时，20分钟周期内的后台常规推演仅能完成100次路线评估，远低于图\ref{fig:curse}a所示的2,000次饱和阈值，导致“全程巡航”策略规划出的路线质量低劣，在2023至2026年测试集上的平均随时遗憾值高达0.374；此时，若每3个周期唤醒1次50倍速的GPU（单周期推演跃升至5,000次，直接跨越饱和拐点），尽管多消耗了部分电能，“三分之一间歇思考”与“全程深度思考”仍将测试集随时遗憾值大幅压低至0.270与0.273，较全程巡航产生高达0.104的显著净收益！反之，当机载后台处理器升级至中速水平（$r_{\text{base}}=20\text{ 推演/min}$）时，单周期后台推演已达400次，配合跨周期热启动机制，数个周期累积的有效搜索深度已逼近饱和区；此时再开启$+20\text{ W}$的GPU不仅无法带来实质性的路线质量跃升，反而因白白消耗电池能量而缩短了总巡航里程，致使“全程巡航”以0.266的随时遗憾值反超“三分之一间歇思考”（0.269）与“全程深度思考”（0.269），成为中速平台上的最优固定策略。

第二，**在巡航途中关停推进器开展停航漂移重采样或停航思考，在所有测试算力与底图误差组合下均得不偿失**。无论是在慢速平台上（“三分之一停航思考”遗憾值0.331，“三分之一停航重采样”高达0.408），还是在中速平台上（两者遗憾值分别为0.328与0.335），包含停航动作的策略均大幅落后于持续巡航策略。这一现象可通过空间信息论与采样信噪比得到严格解释：在空间相关尺度为$\ell=10\text{ km}$（5个2千米网格）、先验合成不确定性$\sigma_3\approx 0.258$的东海赤潮场中，AUV保持$1.5\text{ m/s}$巡航时每20分钟跨越$18\text{ km}$，沿途自动采集18个独立荧光计样本（平均每个2千米网格内采集2个样本，单周期内相关半径内累积9至18个样本）；根据式\eqref{eq:eakf}的卡尔曼方差缩减关系，仅凭巡航途中的走航采样即可将沿途局部后验标准差从0.258迅速压低至$0.1/\sqrt{9}\approx 0.033$以下，局部测量噪声早已不是决策瓶颈。若此时关停推进器驻留原地重采样20分钟，虽能额外获得5个原位样本将同一点位的误差再压低几个毫对数单位，却直接付出了放弃$18\text{ km}$未知海域空间探索的惨重代价，在80千米尺度的任务窗口内严重迟滞了对真正赤潮核心区的搜寻进程。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_example}
  \caption{典型测试集赤潮巡测任务（2023年4月15日，慢速算力平台$5\text{ 推演/min}$）中“全程巡航”与“三分之一间歇思考”的轨迹与随时遗憾值对比。（a）AUV在下水前装订的3天滞后卫星叶绿素底图；（b）目标日真实海洋叶绿素场及两种策略的24小时航行轨迹，其中蓝色曲线为“全程巡航”轨迹，橙色曲线为“三分之一间歇思考”轨迹（加粗线段标示开启GPU深度思考的20分钟周期），五角星标示真实最高叶绿素浓度水体位置；（c）24小时窗口内AUV向岸基中心实时回报答案的瞬时遗憾值演化曲线，“全程巡航”长期停滞在0.40附近（24小时均值0.43），而“三分之一间歇思考”在约19小时处成功命中全局极值（瞬时遗憾值降至0，24小时均值0.31）。}
  \label{fig:example}
\end{figure}

第三，为直观展示高功耗深度思考在慢速算力平台上扭转战局的物理过程，图\ref{fig:example}剖析了按日期顺序排列的第一个策略差异超过0.1的测试集典型任务实例（2023年4月15日，慢速算力平台$r_{\text{base}}=5\text{ 推演/min}$）。对比图\ref{fig:example}a与图\ref{fig:example}b可见，3天前的滞后卫星底图在窗口东北部与中南部均显示有较高浓度斑块，但经过3天演化与小尺度修正后，真实海洋的全局最高浓度核心（五角星）实际聚集在窗口西南部。在“全程巡航”策略下（蓝色轨迹），由于每周期仅有100次推演预算，交叉熵规划器无力在连续四维航路点空间中探明横跨整个窗口的远距离高价值走廊，导致AUV长期在出发点附近的东北角次优水体中往复盘旋，其上报给岸基中心的最佳浓度估计终生停留在距离真实极值0.40个对数单位之外，24小时时间平均遗憾值高达0.43（图\ref{fig:example}c）。相反，在“三分之一间歇思考”策略下（橙色轨迹），周期性唤醒的GPU（加粗橙色线段）提供了单周期5,000次推演的充裕视野，使规划器在任务前中期成功识别出东北部先验斑块的观测证伪信号，果断规划出一条斜穿任务窗口直插西南部核心区的长距离机动航线，最终在约19小时处精确命中真实最密集赤潮水体，将瞬时遗憾值降至0，全窗口时间平均遗憾值大幅降低至0.31。

\subsection{四类硬件平台上的主实验对比与行前预演有效性分析}

最后，在2023至2026年全部148个测试集赤潮任务窗口上，对五种固定策略、特定硬件开发集最优调参策略（Tuned）、经典单步元推理以及本文提出的行前假想预演控制器（含留出集真值预演与搜索集真值自评预演）开展系统对比。实验涵盖四类典型机载计算硬件平台：（1）慢速处理器平台（$r_{\text{base}}=5\text{ 推演/min}$，GPU额外功耗$+20\text{ W}$）；（2）中速处理器平台（$r_{\text{base}}=20\text{ 推演/min}$，GPU额外功耗$+20\text{ W}$）；（3）快速处理器平台（$r_{\text{base}}=100\text{ 推演/min}$，GPU额外功耗$+20\text{ W}$）；（4）配备高效能专用加速器的中速平台（$r_{\text{base}}=20\text{ 推演/min}$，加速器额外功耗仅$+5\text{ W}$）。全部测试结果汇总于表\ref{tab:main}与图\ref{fig:main}（置信区间通过对赤潮暴发周进行分层自助重采样计算得出）。

\begin{table}[htbp]
  \centering
  \caption{2023至2026年测试集（148个赤潮任务窗口，3天滞后底图，海真偏离0.15，传感器噪声0.1）上各控制策略在四类机载硬件平台上的24小时时间平均随时遗憾值对比（数值越低越好）。括号内数值表示相对于该硬件平台在开发集（120个窗口）上事后选出的最优固定调参策略（标有“调参最优”）的遗憾值差值及基于赤潮周自助法的95\%置信区间。}
  \label{tab:main}
  \small
  \begin{tabular}{lcccc}
    \toprule
    \textbf{控制策略} & \textbf{慢速算力平台} & \textbf{中速算力平台} & \textbf{快速算力平台} & \textbf{高效加速器平台} \\
     & ($5\text{/min}, +20\text{ W}$) & ($20\text{/min}, +20\text{ W}$) & ($100\text{/min}, +20\text{ W}$) & ($20\text{/min}, +5\text{ W}$) \\
    \midrule
    全程巡航（$s_1$） & $0.374\ (+0.104)$ & $\mathbf{0.266}\ (\text{调参最优})$ & \TBD{待填} & \TBD{待填} \\
    全程深度思考（$s_2$） & $0.273\ (+0.003)$ & $0.269\ (+0.003)$ & \TBD{待填} & \TBD{待填} \\
    三分之一间歇思考（$s_3$） & $\mathbf{0.270}\ (\text{调参最优})$ & $0.269\ (+0.003)$ & \TBD{待填} & \TBD{待填} \\
    三分之一停航思考（$s_4$） & $0.331\ (+0.061)$ & $0.328\ (+0.062)$ & \TBD{待填} & \TBD{待填} \\
    三分之一停航重采样（$s_5$） & $0.408\ (+0.138)$ & $0.335\ (+0.069)$ & \TBD{待填} & \TBD{待填} \\
    \midrule
    经典单步元推理\cite{russell1991right} & $0.287\ (+0.017)$ & $0.287\ (+0.021)$ & \TBD{待填} & \TBD{待填} \\
     & {\footnotesize $[+0.009, +0.025]$} & & & \\
    \textbf{行前预演（留出集真值，本文）} & $\mathbf{0.276}\ (+0.007)$ & $\mathbf{0.265}\ (-0.001)$ & \TBD{待填} & \TBD{待填} \\
     & {\footnotesize $[-0.001, +0.015]$} & & & \\
    行前预演（搜索集真值，对照） & $0.273\ (+0.003)$ & $0.268\ (+0.002)$ & \TBD{待填} & \TBD{待填} \\
    \bottomrule
  \end{tabular}
\end{table}

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_main}
  \caption{2023至2026年测试集（148个赤潮任务窗口）上各控制器在四类硬件平台（慢速算力$5\text{/min}$、中速算力$20\text{/min}$、快速算力$100\text{/min}$及低功耗高效加速器$20\text{/min}, +5\text{ W}$）上相对于开发集特定硬件最优调参策略的随时遗憾值差值及95\%自助法置信区间（虚线0基准代表特定硬件事后调参上限，越靠左性能越优）。}
  \label{fig:main}
\end{figure}

表\ref{tab:main}与图\ref{fig:main}的实验数据有力地支撑了本文关于自适应元控制的各项核心结论。首先，**没有任何一种单一固定策略能够跨硬件平台保持最优**。若将中速平台上的最优策略“全程巡航”直接移植至慢速平台，其随时遗憾值将剧增0.104（从0.270恶化至0.374）；反之，若将慢速平台上的最优策略“三分之一间歇思考”固化至中速或更高速平台，则会因不必要的GPU能耗损失续航而落后于全程巡航\TBD{快速算力与高效加速器平台的具体对比数值补充}。这说明传统的固定启发式规则必须针对每一款特定机载处理器和功耗参数组合耗费数年历史任务数据进行事后调参，缺乏跨平台迁移能力。

其次，**经典单步元推理在真实海洋巡测中因严重的过思考偏差而全面落后于调参基线与行前预演**。在慢速与中速算力平台上，经典单步元推理的随时遗憾值均为0.287，分别比对应平台的调参最优策略劣化$+0.017$（95\%置信区间$[+0.009, +0.025]$，统计显著劣化）与$+0.021$。行为轨迹统计揭示了其失效的直接原因：在中速算力平台上，尽管400次后台推演早已足够，经典单步元推理却被规划器在32个搜索样本上持续虚高的内部改进轨迹（图\ref{fig:curse}）所误导，在高达65\%的决策周期内盲目开启GPU进行深度思考，更有28\%的周期选择关停推进电机在原地“停航思考”！这种典型的过度思考病态行为同时浪费了宝贵的推进电能与空间探索时间，证明不经集合解耦与全周期耦合校准的局部单步元推理不适用于受限具身系统。

再次，**本文提出的基于留出集真值的行前假想预演控制器，在无需任何跨任务历史调参的前提下，自动达到了与针对特定硬件事后最优调参策略完全持平的优异性能**。在慢速算力平台上，留出集行前预演自动识别出基础算力的严重不足，高频选出深度思考策略，取得0.276的随时遗憾值，较“全程巡航”大幅降低0.098，与事后调参上限（0.270）之差仅为$+0.007$（95\%置信区间$[-0.001, +0.015]$，统计上无显著差异），且显著优于经典单步元推理（$p < 0.01$）；当硬件切换至中速算力平台时，同一套行前预演算法无需修改任何一行参数，自动感知到后台算力已趋充裕而GPU额外功耗会导致提前断电，从而果断转向以巡航为主的策略，取得0.265的随时遗憾值（甚至较开发集调参最优策略0.266微弱领先$-0.001$，较单步元推理大幅领先0.022）。在全部测试任务中，行前预演几乎从不选择停航类策略（选中比例仅为1\%），准确复现了真实海洋中的策略相图规律\TBD{快速算力与高效加速器平台上行前预演的具体数值表现补充}。

最后，对比表\ref{tab:main}最后两行可以发现一个极具启发性的现象：**在闭环全任务行前预演中，即便从搜索集（而非留出集）中抽取合成真实海洋（自评预演对照），依然取得了与留出集预演高度一致的优异表现**（慢速平台0.273，中速平台0.268）。为何单步评估时搜索集会产生高达$+0.114$的灾难性过拟合（图\ref{fig:curse}），而在24小时闭环行前预演中却能保持准确的策略排序？深入剖析预演内部数据发现，在全任务闭环预演中，一旦某个假想海洋$c^{(j)}$被抽作“合成真实海洋”，它在整场24小时模拟任务中便扮演固定的外部物理环境角色，而模拟任务内部的规划器在每一步是通过同化带噪观测来搜索路径，无法直接针对未知的未来观测实现作弊；同时，由于假想海洋由高斯随机场生成，其极值尖峰分布与真实海洋存在微弱的高阶矩差异，导致预演计算出的绝对假想遗憾值在所有策略上均比真实海洋遗憾值系统性偏高0.05至0.07个对数单位。然而，由于五种策略在预演中严格共享相同的合成真实海洋与随机数序列（共同随机数技术），这一0.05至0.07的系统性加性常数偏移在五种策略上同向发生，并在按式\eqref{eq:rehearsal}做策略间作差比较时完美相互抵消！例如在中速算力平台上，留出集预演与搜索集预演估计的“思考策略减去巡航策略”相对遗憾值差值分别为$-0.002$与$+0.006$，均与真实海洋中的实际策略差值（$+0.002$）紧密吻合。这表明，全周期闭环预演结合共同随机数差分比较，天然具备对绝对评估基线偏移的免疫能力，进一步夯实了行前假想预演在实际工程部署中的鲁棒性。

\section{结论与展望}

本文围绕携带海洋大数据先验底图的自主水下航行器在动态巡测中如何权衡“深入思考”、“巡航采样”与“停航重采样”这一核心科学问题，依托2018至2026年东海3197天多源融合卫星叶绿素大数据与422个春季赤潮应急巡测任务窗口，开展了从大数据不确定性量化、集合同化建模、规划器过思考机理剖析到自适应元控制器设计的全链条研究。研究得出三项主要结论：（1）在基于有限假想海洋集合的连续轨迹规划中，随着推演算力跨越数个数量级增长，规划器内部搜索得分在真实收益早已饱和后仍因优化器诅咒而持续攀升，而将假想海洋解耦为搜索集与留出验证集可将全预算范围内的评估偏差严格控制在0.005以内；（2）深度时空神经网络无法仅凭日均平滑遥感底图确定性外推小尺度赤潮斑块的日际演变，高功耗GPU深度思考仅在机载基础算力不足以覆盖单周期有效规划深度时产生显著净收益，而在相关尺度为十千米级的中尺度场中，巡航途中关停推进器开展停航重采样始终得不偿失；（3）在出发前利用假想海洋开展24小时全周期闭环预演并结合共同随机数差分择优，能够有效克服经典单步元推理的过思考病态与离线学习的低信噪比困境，在无需特定硬件历史调参的条件下自动匹配各算力平台的事后最优调参性能。

本研究在海流运动表征与多平台协同方面仍存在一定局限：当前模型在随流漂移参考系下假设表层水体在80千米窗口内作准刚性平流，尚未显式刻画强锋面区的水平剪切变形及藻华昼夜垂直迁移引起的三维垂向分布差异，且行前预演在任务中途遭遇极端突发水文突变时缺乏在线重预演修正机制。未来的研究工作将沿着两个方向拓展：一是将三维斜压海流数值预报集合与卫星水色大数据融合，在时变剪切流场中研究AUV三维锯齿剖面机动与机载实时科学计算的联合资源分配；二是将单机行前假想预演拓展至空海潜跨域异构无人集群（如无人艇与多台AUV协同），探索通信受限条件下分布式想象推演与信息共享的最优权衡准则。


########## ATTACHED FILE: draft1_appendix.tex (draft 1, sections/appendix.tex) ##########

\section{代码与数据开源说明}

本研究坚持可重复科学研究准则，论文所涉及的全部数据处理脚本、集合调整卡尔曼滤波同化模块、交叉熵轨迹规划器、深度学习时空世界模型对比代码以及行前假想预演元控制器的完整源代码与实验配置文件，均已整理并开源于代码托管平台：\TBD{GitHub仓库地址}。

实验所使用的海洋卫星遥感大数据均取自国际公开科学数据中心，具体获取途径与数据集标识如下：
\begin{enumerate}
  \item \textbf{东海多源融合叶绿素a浓度遥感数据集（2018—2026年）：} 来源于美国国家海洋和大气管理局海岸观测网（NOAA CoastWatch）ERDDAP数据服务器，融合了可见光红外成像辐射仪（VIIRS）与哨兵三号海洋陆地颜色仪（OLCI）观测并经经验正交函数插值重构（DINEOF）生成，空间分辨率为2千米，时间分辨率为逐日，遵循CC0公共领域开放许可，数据集唯一标识符为\texttt{noaacwNPPN20S3ASCIDINEOF2kmDaily}。
  \item \textbf{全球多尺度超分辨率海表温度数据集（2018—2026年）：} 来源于美国喷气推进实验室（JPL）物理海洋学分布式活动存档中心ERDDAP服务器，版本为MUR v4.1，原始空间分辨率为$0.01^\circ$，时间分辨率为逐日，数据集唯一标识符为\texttt{jplMURSST41}。
\end{enumerate}

\section{人工智能工具使用说明}

在本课程论文的研究与撰写过程中，作者严格遵循浙江大学关于学术诚信与人工智能工具规范使用的相关规定，采用人机协同模式开展工作，各环节的具体分工与责任界定说明如下：
\begin{enumerate}
  \item \textbf{研究构思、算法设计与实验执行：} 论文的核心科学问题提出（具身采样中的思考—行动权衡与过思考偏差剖析）、东海赤潮遥感大数据清洗与422个任务窗口构建、搜索—留出双集合解耦架构设计、行前假想预演元控制器算法实现以及全部数值仿真实验与统计检验，均在作者主导下配合人工智能研究助手（Claude）共同完成；所有实验数据、统计指标与图表结果均源自真实运行日志。
  \item \textbf{文献调研与核查：} 论文引用的25篇参考文献均经过出版商原始记录或预印本库逐一核对，确保作者、题名、期刊/会议名称、年份及数字对象唯一标识符（DOI）真实准确，未引入任何未经核实的虚假文献。
  \item \textbf{论文初稿撰写与文字润色：} 在给定完整实验事实清单、数学公式定义与图表说明的严格约束下，使用大语言模型（Gemini）辅助生成中文学术初稿的LaTeX文本与中英文摘要，并由Claude与作者逐句核查文中每一项事实陈述、实验数值、公式符号及文献引用的一致性，最终由作者通读审定并对全文学术质量与事实准确性承担全部责任。
\end{enumerate}
```

</details>

## Gemini 的回复

<details><summary>展开（共 19169 字符）</summary>

```
===== FILE: sections/title.tex =====
基于想象海洋出发前预演的自主水下航行器思考与行动权衡研究

===== FILE: sections/subtitle.tex =====
——以八年卫星叶绿素数据驱动的东海赤潮应急巡测为例

===== FILE: sections/abstract.tex =====
\section*{摘\quad 要}
\addcontentsline{toc}{section}{摘要}

携带卫星遥感先验底图的自主水下航行器（AUV）在现场巡测时，受机载算力、电池容量与作业时间的制约。由于卫星底图存在数日滞后与小尺度平滑偏差，航行器需在每个控制周期权衡：是开启高功耗图形处理器（GPU）在内部地图上深想，还是靠低功耗规划继续走并沿途采样，或是停下随水漂流原位复测。固定分配规则难以适应不同机载算力，单步元推理则会因规划器在有限样本上的过拟合而高估计算价值。本文提出一种基于留出想象海洋的集合同化与出发前预演方法。该方法利用八年东海卫星数据标定底图误差，围绕旧图生成48个想象中的海洋并随现场采样实时同化更新；其中32个用于规划航线，16个留出用于评判。出发前，母船或岸上计算机以4个留出海洋为假想真值，按机载算力与电池功耗模拟五种用时策略的24小时任务，选出平均遗憾最低的策略。在2018至2026年东海3197天卫星叶绿素数据构建的422个赤潮任务窗口上的实验表明：留出海洋在64至200,000次想象推演下与真实航线价值之差均不超过0.005；深想仅在基础算力过慢时有益，停下复测始终不划算；在148个测试任务上，出发前预演在慢计算机与中等计算机上分别取得0.276与0.265的时间平均遗憾，优于单步元推理，且与按开发年份调好的固定策略相差在置信区间内。

\vspace{1em}
\noindent\textbf{关键词：}海洋大数据；自主水下航行器；元推理；数据同化；赤潮巡测；计算与行动权衡

\clearpage
\section*{Abstract}
\addcontentsline{toc}{section}{Abstract}

Autonomous underwater vehicles (AUVs) carrying satellite prior maps must trade off computation against movement under onboard processor, battery, and mission-time constraints. Because satellite maps are several days old and smooth out small-scale features, the vehicle must decide at every control interval whether to activate a high-power graphics processing unit (GPU) to plan deeply, continue cruising and sampling under low-power background planning, or stop propulsion to drift and resample locally. Fixed time-allocation rules do not generalise across processor speeds, while classic one-step metareasoning overestimates the value of computation by trusting the planner's own search trace on finite ensemble members. We propose an ensemble data assimilation and pre-mission rehearsal method using held-out imagined oceans. Using eight years of satellite chlorophyll-a data over the East China Sea to calibrate stale-map uncertainty, the vehicle generates 48 imagined oceans around the stale map and updates them with in-situ fluorometer samples via a localised ensemble adjustment Kalman filter. Thirty-two members are searched by a cross-entropy route planner and 16 are held out for unbiased evaluation. Before launch, a shipboard or shore computer treats 4 held-out members as synthetic truths and simulates complete 24-hour missions for five time-allocation strategies under the vehicle's actual compute speed and battery budget, selecting the strategy with the lowest mean regret. Across 422 spring bloom windows from 3,197 daily maps (2018--2026), held-out evaluation stays within 0.005 of true route value from 64 to 200,000 rollouts, GPU planning helps only when baseline compute is too slow, and stopping never pays. On 148 test missions, rehearsal achieves time-averaged regrets of 0.276 and 0.265 on slow and moderate computers, outperforming one-step metareasoning and matching development-tuned strategies within confidence intervals without prior missions on that vehicle.

\vspace{1em}
\noindent\textbf{Keywords: }Ocean big data; Autonomous underwater vehicle; Metareasoning; Data assimilation; Harmful algal bloom survey; Thinking-acting trade-off

===== FILE: sections/body.tex =====
\section{绪论}

\subsection{现场移动观测中的思考与行动权衡}

携带先验地图的移动观测平台在未知自然环境中作业时，需要在内部路线规划与外部现场采样之间分配有限的时间与能量\cite{horvitz1987reasoning, russell1991right, shen2025thinking}。野外自主平台受制于电池容量、嵌入式计算速率与固定的作业时间窗口\cite{xiao2020thinking, magnino2026metareasoning}。历史观测构成的先验底图能够给出大尺度空间分布，但因环境演变与观测盲区，底图往往滞后于现场实际状态且缺失小尺度结构\cite{jiang2015horizon}。若航行器仅靠低频粗糙规划维持航行，容易在复杂梯度中偏离目标核心区；反之，若频繁开启高功耗计算模块开展密集航线搜索，或关停推进器在原地重复测量以降低传感器随机误差，则会消耗本可用于推进的电能或缩减空间探索里程\cite{cuadron2025overthinking, elboher2023formal}。因此，在算力、能量与底图误差的共同约束下，何时应当继续计算、何时应当继续采样，是自主移动观测系统需要回答的基本问题\cite{hunt2021formalizing}。

当航行器边走边想时，机体机动与大脑规划虽在同一周期内并行执行，但两者仍通过电池能量消耗与先验模型不确定性紧密耦合\cite{xiao2020thinking, elboher2023formal}。维持常规巡航只需低功耗处理器在后台持续更新航线，而唤醒高功耗机载GPU开展大规模推演会抬升整机功率，缩短电池耗尽前的总巡航时间。同时，规划器的航线推演完全建立在内部环境模型之上：当底图本身存在明显的不确定性时，持续增加搜索算力能否转化为现场采样收益，取决于当前搜索深度是否已触及底图所含信息的上限\cite{jiang2015horizon, smith2006curse}。

\subsection{东海赤潮应急巡测与卫星底图的局限}

卫星遥感数据驱动的东海有害赤潮应急巡测，是检验上述思考与行动权衡的具体场景\cite{fossum2019, lou2014diurnal}。根据2023年中国海洋灾害公报，我国海域全年发现赤潮46次，累计面积约1500平方千米，其中有毒有害赤潮29次\cite{mnr2024bulletin}。在浙江近海与长江口外海域，晚春至初夏常暴发东海原甲藻赤潮，高浓度斑块的叶绿素a浓度通常超过$6\text{ mg/m}^3$，并随潮汐与海流发生日际漂移\cite{lou2014diurnal}。赤潮暴发时，应急指挥中心派出自主水下航行器（AUV）进入目标海域开展24小时巡测，要求航行器尽早找到叶绿素浓度最高的水体，并随时响应指挥中心对最浓处位置的查询\cite{fossum2019, remus100}。由于AUV在水下作业期间几乎无法与母船或岸站实时通信，航行途中的航线重规划必须全部由机载计算机独立完成。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_overview}
  \caption{海洋大数据驱动的AUV赤潮应急巡测与用时策略选择总览。中央为东海一次测试任务（2025年4月4日）的三维海洋窗口，顶面颜色表示航行器遇到的真实叶绿素浓度；图中标示了AUV及其航迹（浅蓝色为走并由低功耗处理器后台规划，橙色为开启GPU深想）以及赤潮最浓处的浅色圆环；海面块体上方为一叠想象中的海洋，最上方两个橙色边框样本留出用于评判，其余深蓝色边框样本用于规划航线。（A）海洋大数据：2018至2026年共3197天逐日2千米卫星叶绿素数据，航行器遇到的真实海洋不同于3天前的卫星图，从中切出422个赤潮季任务窗口，小尺度信息需靠现场观测获取；（B）艇的想象：由旧图和数据标定的误差生成48个想象中的海洋，32个用来规划航线，16个留出来评判，并在出发前对五种用时策略各跑一遍预演；（C）每20分钟的选择：走、深想、停下，应急中心可随时询问最浓处位置。}
  \label{fig:overview}
\end{figure}

卫星水色遥感提供了大尺度背景场，但时间滞后与空间平滑使其无法替代AUV的现场观测\cite{beckers2003dineof, ye2021cocts}。东海春夏多云雨，业务化叶绿素产品通常利用经验正交函数插值方法填补云区盲区，生成空间连续的2千米逐日融合底图\cite{beckers2003dineof}。如图\ref{fig:overview}所示，AUV出发前装入的往往是1至3天前的旧卫星图，在等待下水期间赤潮斑块已随水体演变；此外，缺测插值平滑了小尺度结构，卫星反演与现场海水之间也存在固有偏差\cite{ye2021cocts}。因此，AUV必须把旧卫星图及历史误差统计转化为概率化的内部记忆，一边用机载荧光计沿途采样修正地图，一边合理分配计算与机动资源。

\subsection{现有控制方法的不足与本文方法}

面对计算与采样的分配问题，固定分配规则、经典单步元推理以及基于历史任务结果的学习器均存在明显局限。第一种直接做法是采用固定的用时规则（如一直走或按固定比例开启GPU深想），但固定规则无法兼顾不同的机载计算机速度：在慢计算机上一直走会因搜索不足而走弯路，在算力已够用的计算机上频繁开启GPU则会多耗电却不改善航线。第二种做法是采用人工智能中的经典单步元推理\cite{horvitz1987reasoning, russell1991right, lin2015metareasoning, sung2021quit}，在每个周期在线比较“多想一步的计算收益”与“多测一步的信息收益”；但该方法直接用规划器在搜索样本上的内部得分增量来估计计算收益，当搜索预算较大时，规划器会迎合有限样本中的随机正涨落而虚报收益，并且单步评估无法反映当前耗电对24小时全程续航的影响\cite{cuadron2025overthinking}。第三种做法是从历史巡测任务的最终表现中直接学习策略选择器\cite{magnino2026metareasoning}；但在本场景中，不同任务窗口之间的遗憾标准差约为0.13，而几种较好策略之间的平均差距不超过0.01，单次任务结果包含很大的环境背景波动。

针对上述问题，本文提出利用多年卫星数据标定底图不确定性、将航线搜索与价值评判分离，并在出发前通过完整任务预演选择用时策略的方法。全文工作包括三个部分：第一，利用2018至2026年东海3197天卫星叶绿素数据标定滞后底图误差，围绕旧图生成48个想象中的海洋并随现场观测同化更新，同时验证了深度时空预测模型无法在测试年份上改善1至3天的底图外推；第二，将48个想象中的海洋分为32个规划用样本与16个留出评判样本，消除航线搜索对有限样本的过拟合偏差；第三，在AUV下水前由母船或岸上计算机以4个留出海洋为假想真值，按机载计算机速度与电池功耗将五种用时策略各完整预演一遍，选出平均遗憾最低的策略投入实海执行。

\section{东海叶绿素遥感数据与底图不确定性}

\subsection{八年卫星数据集与赤潮任务窗口}

本文使用2018至2026年东海多源卫星融合叶绿素a数据集构建赤潮巡测任务窗口与先验误差统计。该数据集下载自美国国家海洋和大气管理局海岸观测网数据服务器，融合了多颗极轨卫星水色传感器的观测，并采用经验正交函数缺失数据插值算法填补云层遮挡区\cite{beckers2003dineof}。数据空间分辨率为2千米，时间分辨率为逐日，覆盖2018年1月1日至2026年10月23日共3197天；研究区域取东海北纬$25^\circ\text{--}33^\circ$、东经$119.5^\circ\text{--}127^\circ$，每日包含$385\times 361$个网格像素。同时，为检验海表温度对叶绿素演变的辅助预测作用，本文从同一数据服务器下载了美国国家航空航天局喷气推进实验室制作的多尺度超分辨率海表温度逐日无云产品（版本4.1）\cite{chin2017mur}，将其从$0.01^\circ$重采样至$0.04^\circ$。文中除特别注明外，所有叶绿素浓度、误差与遗憾均以$\log_{10}(\text{叶绿素a浓度}/\text{mg m}^{-3})$为单位。

为聚焦离岸赤潮高发场景，本文按统一条件从每年4月至6月的卫星序列中切出正方形巡测任务窗口。具体做法是在浙江外海陆架区（北纬$26.5^\circ\text{--}31.5^\circ$，东经$121.5^\circ\text{--}125^\circ$）寻找离岸至少30千米、经空间平滑后局部峰值超过$5\text{ mg/m}^3$的藻华中心，将该中心随机平移至多16千米后，截取$80\text{ km}\times 80\text{ km}$（$40\times 40$个2千米网格）的窗口；距离陆地或岛屿15千米以内的网格设为禁航区，仅保留可航行水域不少于80\%且窗内对数叶绿素极差不低于0.3的窗口。按此标准共切出422个赤潮任务窗口，其中2018至2022年的274个窗口作为开发集（用于标定误差统计和选择调好的基线策略），2023至2026年的148个窗口作为测试集。每次任务开始时，AUV从窗口边缘随机选取的一个可航行网格出发。

\subsection{底图滞后误差图谱与小尺度偏差}

航行器携带的旧卫星底图与现场真实海洋之间的差异，来自数日等待期间的海洋演变以及同日卫星图对小尺度结构的平滑。利用全部3197天数据计算相隔3天的对数叶绿素变化标准差，可得到四季分布图谱（图\ref{fig:atlas}）。全海域3天变化标准差的中位数在春季最高（0.127），夏季为0.107，秋季为0.103，冬季降至0.081；夏季空间差异显著，全海域90\%分位数达0.204，在浙闽沿岸与长江冲淡水锋面一带形成3天变化标准差达0.25至0.3的条带。在274个开发集任务窗口内，任务当日卫星图减去$k$天前旧图的误差统计显示：当滞后天数$k=1, 2, 3$天时，误差标准差分别为$s_1=0.125$、$s_2=0.176$与$s_3=0.210$，空间相关尺度约为$\ell=5$个网格（10千米），均值偏差分别为$+0.016$、$+0.032$与$+0.045$。

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

本文将AUV运动、叶绿素场与数据同化全部建立在随表层水体一同漂移的参考系中。静止轨道卫星对2011年5月东海一次赤潮的连续追踪表明，表层藻华斑块随潮汐往复漂移\cite{lou2014diurnal}。在随表层水体漂移的参考系下，赤潮斑块相对于水体不移动，AUV无需逆流追赶斑块，而海流的作用则体现在卫星图滞后期间的演变统计中。

在由$40\times 40$个2千米网格组成的任务窗口内，记网格$\mathbf{x}$处的真实对数叶绿素浓度为$c(\mathbf{x})$。在$T=24\text{ h}$的任务窗口内，应急指挥中心可随时询问最浓处在哪里；AUV从截至时刻$t$已实际造访的网格集合$\mathcal{V}(t)$中，选出内部集合均值$\bar{c}_t(\mathbf{x})$最高的位置作为回答：
\begin{equation}
  \hat{\mathbf{x}}(t) = \arg\max_{\mathbf{x}\in\mathcal{V}(t)} \bar{c}_t(\mathbf{x})
  \label{eq:answer}
\end{equation}
任务在满24小时或电池耗尽时结束，结束后的回答保持不变。定义24小时时间平均遗憾$R$为主要评价指标（越低越好）：
\begin{equation}
  R = \frac{1}{T}\int_0^T \left[\max_{\mathbf{x}} c(\mathbf{x}) - c\big(\hat{\mathbf{x}}(t)\big)\right] dt
  \label{eq:regret}
\end{equation}
同时记录24小时结束时的终点遗憾，以及终点回答的真实浓度落在全窗最高值$0.1$个对数单位（即26\%）以内的比例。

\subsection{航行器功耗模型与二十分钟决策周期}

航行器机电参数参照百米级轻型AUV\cite{remus100}与嵌入式边缘GPU模块\cite{jetsonorinnx}设定。AUV对水巡航速度为$1.5\text{ m/s}$（约3节），携带$1\text{ kWh}$电池，在3节航速下续航约22小时，对应巡航总功率$45\text{ W}$，其中基础航电功率$15\text{ W}$（含导航、传感器及常驻后台运行的低功耗处理器），推进功率$30\text{ W}$。机载嵌入式GPU模块（功率范围$10\text{--}25\text{ W}$，基准设定取$+20\text{ W}$，省电加速器设定取$+5\text{ W}$）用于深度航线规划，其推演速度为低功耗处理器的50倍。由于本文的折线规划器与二维表层场是对真实水下三维路径评估（需计入海流、深度与安全约束）的简化替代，决定规划质量的是计算机相对于规划问题的速度；因此实验以“每分钟想象推演次数”度量低功耗处理器速度，并在5至200次/分的范围内变化。

整个24小时任务按每段20分钟划分为连续的决策周期。在每个20分钟周期内，AUV的机体与大脑并行动作\cite{xiao2020thinking, elboher2023formal}：
\begin{itemize}
  \item \textbf{机体动作：}选择“走”时，开启推进器（$30\text{ W}$）沿当前航线以$1.5\text{ m/s}$航行，20分钟走过$1.8\text{ km}$（不足一个2千米网格），机载荧光计每走$1\text{ km}$采样1次，每周期获得约2个样本；在电池允许时，24小时可航行约$120\text{--}130\text{ km}$，约能横穿80千米窗口1.5次。选择“停下”时，关停推进器（推进功率$0\text{ W}$，仅耗电$15\text{ W}$）随水漂流，荧光计每4分钟对同一水体采样1次，每周期获得5个样本。每次独立采样的观测模型为：
  \begin{equation}
    y = c(\mathbf{x}) + \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, 0.1^2)
    \label{eq:obs}
  \end{equation}
  \item \textbf{大脑规划：}维持低功耗处理器后台规划（额外功耗$0\text{ W}$），或开启GPU“深想”（额外功耗$+20\text{ W}$，推演速度提高至50倍）。新航线以AUV在当前20分钟周期结束时的预计位置为起点进行计算（时延补偿），并在周期结束时替换旧航线。
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

当规划器在有限个想象海洋上搜索航线时，若同时用这批样本的平均得分来评判航线好坏，就会受到“优化器诅咒”的影响\cite{smith2006curse, vanhasselt2010double}。其原因在于，当推演次数大幅增加时，优化器能够精细调整航路点位置，使折线恰好穿过这批特定样本中偶然重合的随机高值点；此时规划器看到的内部自评得分会随推演次数增加而持续上升，但在未参与搜索的真实海洋中，这种针对样本随机涨落的微调并不提高实际收益。为此，本文将48个想象中的海洋固定分为两组（图\ref{fig:overview}B）：32个作为规划用海洋，供交叉熵规划器搜索并选出均值最高的航线；其余16个作为留出海洋，它们同样随现场观测同化更新，但从不参与航线搜索，专门用于对选出的航线给出无偏的价值评判。

\subsection{出发前预演控制器与对比基线}

为在全任务周期尺度上权衡走、深想与停下，本文定义了五种候选时间分配策略：（1）一直走：全程巡航采样，仅用低功耗处理器后台规划；（2）一直深想：全程巡航采样，同时每周期开启GPU深想；（3）三段深想一段：全程巡航采样，每3个周期中开启1个周期GPU深想；（4）三段停下深想一段：每3个周期中有1个周期停下漂流并开启GPU深想，其余2个周期走并用后台规划；（5）三段停下复测一段：每3个周期中有1个周期停下漂流原位复测且仅用后台规划，其余2个周期走并用后台规划。

在AUV下水前，当航行器仍位于母船甲板或岸站并保持有线连接时，母船或岸上计算机运行“出发前预演”来选定本次任务的策略。预演程序从16个留出海洋中取出4个样本$\{c^{(j)}\}_{j=1}^4$作为假想的“真实海洋”；对每个假想真值$c^{(j)}$和五种策略中的每一种策略$s$，按AUV自身的规划器、机载计算机速度与$1\text{ kWh}$电池模型完整模拟一遍24小时巡测任务，得到假想遗憾$R_{s,j}$。五种策略在同一个假想真值上使用相同的初始集合与观测噪声序列，最后选出4个假想真值上平均遗憾最低的策略执行：
\begin{equation}
  s^* = \arg\min_{s} \frac{1}{4}\sum_{j=1}^4 R_{s,j}
  \label{eq:rehearsal}
\end{equation}
出发前预演模拟的是机载计算机的速度与功耗，但其本身运行在母船或岸上计算机上，无法在机载计算机上直接运行：以慢计算机配置为例，单次任务预演共需约190万次想象推演，若在AUV自身的GPU上运行需耗时约125小时，而在普通台式机单个处理器核心上，慢、中、快三种计算机配置的单次任务预演仅分别耗时4.6秒、7.8秒与约25秒。

实验将出发前预演与四类基线对比：（1）上述五种固定策略；（2）调好的固定策略，即针对每一种硬件配置，先在2018至2022年120个开发集窗口上找出平均遗憾最低的固定策略，再用于测试集（该基线需要该型航行器的历史任务数据，而出发前预演不需要）；（3）单步元推理\cite{russell1991right}，在每个周期根据规划器内部搜索改进轨迹估计计算价值，并通过想象海洋上的预后验分析估计采样信息价值；（4）规划用海洋上的出发前预演对照，其流程与式\eqref{eq:rehearsal}相同，但4个假想真值取自32个规划用海洋。

\section{实验结果与分析}

\subsection{规划预算与留出海洋评判的准确性}

在80个开发集窗口（每窗口3个随机种子，3天前卫星图，任务前8小时）上的预算扩展实验表明，留出的想象海洋能够消除规划器的自评高估并准确反映航线价值的饱和过程（图\ref{fig:curse}）。当每次决策的想象推演次数从64次增至2000次再增至200,000次（跨度约三个半数量级）时，所选航线在真实海洋中的价值从0.749升至0.793，随后平缓收敛至0.803；规划器在32个规划用海洋上的搜索自评得分则从0.762升至0.833并继续攀升至0.917，在最高预算下比真实值高出0.114。相比之下，同一批航线在16个留出海洋上的评判均值分别为0.745、0.794与0.802，在所有预算下与真实价值之差均在0.005以内（图\ref{fig:curse}b蓝色虚线）。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_curse}
  \caption{每次决策的想象推演次数从64次增至200,000次时的航线价值与评判偏差（80个开发集窗口$\times 3$个种子，3天前卫星图）。（a）航线的时间平均最佳浓度（折算为$\text{mg/m}^3$）：规划器搜索时的自评（红线）随推演次数持续上升，留出的想象海洋上的评价（蓝色虚线）与真实海洋中的结果（黑线）在约2000次后一同趋于平缓，阴影带表示任务间的离散度；（b）估计减去真实的对数浓度偏差：不确定性如实标定时留出评价保持在0附近（蓝色虚线），不确定性设大到1.5倍（橙色点线）或设小一半（浅蓝色点线）时分别产生约$+0.07$与$-0.06$的平移。}
  \label{fig:curse}
\end{figure}

即便先验不确定性幅值标定存在偏差，留出海洋对增加算力所获相对提升的判断依然稳健（图\ref{fig:curse}b）。当人为将先验标准差设小一半或设大到1.5倍时，留出评价虽分别产生$-0.06$（浅蓝色点线）与$+0.07$（橙色点线）的整体偏移，但推演次数从64次增至200,000次时留出评价估计的增益（$+0.059$与$+0.054$）仍与真实海洋中的实际增益（$+0.054$与$+0.047$）接近。

\subsection{算力与底图误差相图及典型任务分析}

在低功耗处理器速度（每分钟5至200次推演）与真实海洋偏离卫星图程度（0.05至0.3）构成的二维网格上，五种固定策略的表现呈现出清晰的分布规律（图\ref{fig:phase}）。首先，开启GPU深想仅在基础算力相对于规划问题过慢时才带来明显收益：在慢计算机（5次/分）上，后台每20分钟仅完成100次推演，远低于图\ref{fig:curse}a中约2000次的饱和区，因此“一直走”在测试集上的平均遗憾达0.374，而每三段开启一段50倍速GPU的“三段深想一段”（单次深想推演5000次）将遗憾降至0.270。\TBD{待相图扫描完成后补充快计算机与不同底图误差下的具体分界数值。}

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_phase}
  \caption{低功耗计算机速度（5、10、20、50、100、200次/分）与真实海洋偏离卫星图程度（0.05、0.15、0.3）网格上的固定策略相图。（a）颜色标示五种固定策略中时间平均遗憾最低的策略，格内数字为该策略减去“一直走”的遗憾差值（“一直走”最佳处标为“—”）；（b）“一直走”的时间平均遗憾。}
  \label{fig:phase}
\end{figure}

其次，在所有测试的算力与底图误差下，包含停下漂流动作的策略（三段停下深想一段、三段停下复测一段）表现均明显劣于持续航行的策略。从采样几何与不确定性尺度可以解释这一现象：AUV以$1.5\text{ m/s}$航行20分钟走过$1.8\text{ km}$并采集约2个样本，而停下漂流20分钟对同一水体采集5个样本；在原地重复采样5次虽能将该点处的测量误差从单次$0.1$压低至约$0.1/\sqrt{5}\approx 0.045$，但决定回答质量的瓶颈是尚未造访水域的高先验不确定性（标准差约$0.26$），且将三分之一的时间用于停下会使航行器更晚到达浓水区，从而受到时间平均遗憾的惩罚。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_example}
  \caption{一次测试集任务（2023年4月15日，慢计算机5次/分）中两种策略的对比。（a）艇携带的3天前卫星图，东侧边缘白色三角形为起点；（b）真实海洋及“一直走”（蓝线）与“三段深想一段”（橙线）的航迹，西南角五角星为真实最浓处；（c）24小时内应急中心随时得到的答案误差，“一直走”停留在0.4附近（平均0.43），“三段深想一段”在约19小时后到达真实最浓处（误差降至0，平均0.31）。}
  \label{fig:example}
\end{figure}

图\ref{fig:example}展示了按日期顺序第一个策略差距超过0.1的测试集任务实例（2023年4月15日，慢计算机）。AUV从东侧边缘（白色三角形）出发；3天前的卫星图在东北部浓度较低，向西和西南方向浓度较高（图\ref{fig:example}a），而真实最浓处位于西南角（图\ref{fig:example}b五角星）。在慢计算机上，“一直走”（蓝线）向西南航行至窗口中部后便在中部来回移动，其回答误差一直停留在0.4左右，24小时平均遗憾为0.43（图\ref{fig:example}c）；“三段深想一段”（橙线）则直接横穿窗口驶向西南角，在约19小时后到达真实最浓处（回答误差降至0），24小时平均遗憾降至0.31。

\subsection{不同硬件平台上的控制器对比}

在2023至2026年全部148个测试任务窗口上，出发前预演在无需历史任务调参的条件下，取得了与按开发年份调好的固定策略相近的表现，并优于单步元推理（表\ref{tab:main}）。在慢计算机上，开发集调好的策略是“三段深想一段”（测试集遗憾0.270），而“一直走”的遗憾达0.374；到了中等计算机（20次/分）上，开发集调好的策略同样是“三段深想一段”（0.269），此时“一直走”（0.266）、“一直深想”（0.269）与“三段深想一段”（0.269）三者相差不超过0.003，处于统计噪声范围内（“一直走”减去调好策略的差值为$-0.002$，95\%置信区间为$[-0.010, +0.005]$）。\TBD{待快计算机与省电加速器测试完成后补充这两列固定策略的对比描述。}

\begin{table}[htbp]
  \centering
  \caption{2023至2026年148个测试集任务（3天前卫星图，真实海洋偏离0.15，传感器误差0.1）上各控制方式的时间平均遗憾（越低越好）。“调好的”指在该型航行器的120个开发集任务上表现最好的固定策略；括号内为相对于“调好的”策略的差值，方括号内为按赤潮周自助重采样得到的95\%置信区间。}
  \label{tab:main}
  \input{tables/main_table.tex}
\end{table}

单步元推理在慢计算机与中等计算机上的时间平均遗憾均为0.287，分别比调好的策略高出$+0.017$与$+0.018$（\TBD{待补快计算机与省电加速器上的单步元推理表现}）。动作统计显示，由于单步元推理依据规划器在搜索样本上的自评改进量来决定是否开启GPU，它在慢计算机上有80\%的周期开启GPU深想、34\%的周期停下漂流；在中等计算机上更有93\%的周期开启GPU深想（其中63\%边走边想，30\%停下深想），且共有33\%的周期处于停下状态，过多消耗了电池能量与航行时间。

本文提出的留出海洋出发前预演在慢计算机与中等计算机上分别取得0.276与0.265的时间平均遗憾，与按开发年份调好的固定策略之差分别为$+0.007$（95\%置信区间$[-0.001, +0.015]$）与$-0.003$（$[-0.009, +0.003]$），均在置信区间之内；与单步元推理作配对比较，出发前预演在慢计算机上降低遗憾$-0.011$（95\%置信区间$[-0.019, -0.002]$），在中等计算机上降低遗憾$-0.022$（$[-0.030, -0.013]$），\TBD{待补快计算机与省电加速器上出发前预演减去单步元推理的配对差值及95\%置信区间}。在中等计算机的148个测试任务中，出发前预演选出“三段深想一段”占43\%、“一直走”占30\%、“一直深想”占25\%、“三段停下复测一段”占1\%；\TBD{待补慢计算机与快计算机上出发前预演选出各策略的比例}。

对比表\ref{tab:main}最后两行可见，用规划用海洋作为假想真值的出发前预演对照（慢计算机0.273，中等计算机0.268）与留出海洋出发前预演选出了几乎相同的策略。在预演内部，假想任务算出的遗憾比真实海洋中的遗憾普遍高出0.05至0.07；因为这一偏移对所有候选策略同样存在，所以不改变策略之间的相对排序（例如在中等计算机上，留出预演与规划用海洋预演估计的“深想减去走”差值分别为$-0.002$与$+0.006$，真实差值为$+0.002$，均接近于零）。

\section{结论}

本文依托2018至2026年东海3197天多源融合卫星叶绿素数据与422个春季赤潮任务窗口，研究了携带滞后卫星图的AUV在巡测中如何分配走、深想与停下复测的时间与能量。主要结论如下：（1）深度时空预测模型在测试年份上对1至3天缺测填补叶绿素图的预报精度未超过直接沿用最新卫星图，小尺度信息必须依靠现场观测；（2）当单次决策的想象推演次数从64次增至200,000次时，规划器在搜索样本上的自评得分因过拟合样本噪声而持续上升，而在16个留出想象海洋上的评判均值在所有预算下与真实航线价值之差均不超过0.005；（3）开启高功耗GPU深想仅在基础算力过慢时降低遗憾，中途停下复测在所有测试条件下均使结果变差，而在下水前由母船或岸上计算机运行出发前预演，无需该型航行器的历史任务调参即可取得优于单步元推理、且与按开发年份调好的固定策略相差在置信区间内的表现。

本研究仍存在两点局限：一是随表层水体漂移的参考系忽略了80千米窗口内的水平流剪切与藻华昼夜垂直迁移；二是预演仅在出发前运行一次，未在任务中途根据现场观测重选策略。后续工作将结合三维海流预报集合，进一步探讨多台航行器协同巡测中的计算与采样分配问题。

===== FILE: sections/appendix.tex =====
\section{代码与数据说明}

本研究的数据处理、集合同化、航线规划器、时空预测模型与出发前预演的完整代码及实验配置开源于：\TBD{GitHub 仓库地址}。

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

===== FILE: terms.md =====
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
```

</details>
