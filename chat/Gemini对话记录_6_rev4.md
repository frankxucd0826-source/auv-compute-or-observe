# 与 Gemini 的对话记录 6：第 4 次修改（期刊论文格式）

时间（回复保存时间）：2026-11-05 02:38 UTC。调用方式：Claude 用命令行工具 ask-gemini 把下面“发送内容”作为附件发给 Gemini，并附一句简短指令（按附件中的写作要求完成各节）；回复原样存档后再由 Claude 核对数字与引用、拆分进论文各节。下面两部分都是原文，未作删改。

调用记录：

```
回答已存到 D:\海洋大数据\paper\gemini\rev4_reply.md
[gemini-4-argon-high · gemini 格式 · 输入 30457 / 输出 23152 / 思考 16252 token · 452.0 秒]
```

本轮的写作要求见下方发送内容里的附件 `brief_rev4.md`。

## 发送内容

<details><summary>展开（共 72739 字符）</summary>

```
########## ATTACHED FILE: brief_rev4.md ##########

# Revision 4: rewrite as a journal research paper (in Chinese), with the new experiments

## Why this rewrite
The student's verdict on the previous draft: it reads like a running log and a lab report
("流水账和实验报告"); the experiments are far too few compared with a real journal paper; the
structure copies the literature-review course template. The course is 《海洋大数据技术原理与应用》
(Zhejiang University). Apart from the cover (handled outside these files) and the Chinese
language, the paper must follow the format and standards of an SCI journal research paper:
a clear central idea, sections that each serve it, logical links between them, figures woven
into the argument. Please write a NEW paper from the attached facts, figures and tables; the
previous draft (attached) is only a source of wording you may reuse.

## The central idea (the one thing the reader must carry away)
A vehicle should not decide whether to compute more by trusting its planner's own score: that
score is fitted to the very imagined oceans it was searched on and rises with computation even
when the real benefit has stopped (the optimizer's curse). Imagined oceans built from eight years
of satellite data, with their error calibrated from the same data, give an independent yardstick:
judge computation by outcomes on imagined oceans the search did not fit. Applied before launch as
a whole-mission rehearsal of a few time-allocation strategies (on the support ship's or shore
computer), it lets each vehicle choose how to split its time between computing and observing
without any historical missions; applied online (held-out valuation each interval) it removes the
over-planning of classic metareasoning. Say this idea in the introduction where the approach is
introduced, as contribution 1, and once more in the conclusion, from a different angle each time.

## Structure (sections and what each must do)
- Title: concrete, says what was done (the course paper is single-author; no subtitle needed).
- 摘要 (about 450 Chinese characters) in Ma Dongfang's eight steps: background; need; what
  existing methods lack; what this paper proposes; its key points; the experiment; the main
  numbers; significance. 关键词 4-6. Then the English title, Abstract and Keywords (same content).
  Put both in sections/abstract.tex; use \section*{} is NOT wanted here: format them as
  {\heiti 摘要：} paragraph and {\bfseries Abstract:} paragraph (see the current main.tex: the
  title block is printed before \input{sections/abstract}).
- 1 引言 (no subsections). Paragraph order: (1) the paradigm: satellite ocean big data plus
  autonomous vehicles that must split onboard time and energy between computing and observing;
  (2) the case and why it is hard: East China Sea harmful algal bloom emergency survey, stale and
  smoothed satellite maps, no communication underwater; (3)-(5) the existing paths, one per
  paragraph, each "the obvious way -> why it fails here" (fixed rules tuned per vehicle need past
  missions; adaptive-sampling rules treat planning computation as free or fixed; classic
  metareasoning values computation with the planner's own score, which the optimizer's curse
  inflates; learning a selector from past missions needs data and the mission-to-mission noise is
  large) - no own numbers here; (6) this paper's idea and approach; (7) three contributions as
  bullets, each opening with a bold label and a claim of what is new (idea / method / evidence),
  not a list of work done; (8) one organization paragraph.
- 2 相关工作: three short subsections (metareasoning and anytime planning incl. "thinking vs
  doing" in agents; ocean adaptive sampling and information gathering incl. coverage surveys,
  upper-confidence-bound and Thompson sampling; the optimizer's curse / double estimation and
  ensemble data assimilation with satellite products). Each ends with one sentence on how this
  paper differs. About 900-1200 characters in total.
- 3 问题建模: 3.1 scenario and data (state plainly that the true ocean is built from the real
  satellite map of the mission day, with or without the small-scale variability a satellite
  misses, and that the vehicle carries the real map of 3 days earlier); 3.2 vehicle, actions and
  energy; 3.3 objective (time-averaged regret, equation); 3.4 问题剖析: the root conflict
  (computing and observing share the same time and battery) and three properties that make it
  hard, from which the method's decisions follow: (a) the value of more computation can only be
  estimated in imagination, and the planner's own score is biased upward; (b) the value of
  observing depends on how wrong the stale map is, which ocean big data can measure but cannot
  remove; (c) the best allocation depends on the onboard computer and battery, while single
  missions are too noisy to tune it per vehicle.
- 4 方法: an opening sentence with Fig. 1. 4.1 imagined oceans calibrated from data and updated
  by assimilation; 4.2 separating search from judgement (32 searched / 16 held out); 4.3 pre-launch
  rehearsal, with Algorithm 1 (algorithm + algpseudocode: \Require, \Ensure, \For, \EndFor,
  \State, \Return) and its cost; 4.4 the same principle online (held-out valuation inside one-step
  metareasoning), briefly. Each subsection opens with the principle, then the choice existing
  methods would make and the cost it ignores. Method about 28-32% of the body.
- 5 实验: opening paragraph that states the questions the experiments answer, in the order of the
  subsections. 5.1 设置 (Table 1; baselines defined once, named exactly as in terms.md, grouped:
  fixed strategies; methods that need past missions; online metareasoning; survey rules; the
  per-mission best in hindsight as a reference only; the two truth models; the statistics).
  5.2 what ocean big data tells the vehicle and what it cannot (Fig. 2). 5.3 the planner's
  self-score inflates, held-out judgement does not (Fig. 3). 5.4 main comparison (Fig. 4 and
  Table 2, both truth models). 5.5 mechanism: why one-step metareasoning loses and what rehearsal
  chooses (Fig. 5), with the example mission (Fig. 6). 5.6 ablation (Fig. 7). 5.7 scope: when
  thinking and stopping pay (Fig. 8), a fresher map. 5.8 局限 (one short paragraph). Each
  subsection: its first sentence is its finding; then purpose -> finding -> interpretation.
  Experiments about 35-40% of the body.
- 6 结论: formal; the idea restated from a new angle; the main evidence in a sentence or two
  without repeating every number; one sentence of future work.
- 附录 (sections/appendix.tex): keep the attached appendix (A code/data/reproduction with
  \TBD{GitHub 仓库地址}; B AI-use statement) but tighten wording; update A to mention
  experiments/rev2.sh, experiments/rev2_summary.py and experiments/rev2_tables.py.

## Style (the student's standing requirements)
1. The first sentence of every paragraph states its conclusion; reading only first sentences
   must tell the whole story. Never open a paragraph with "如图X所示" or a setting.
2. Introduction and method follow "常规做法 -> 为何在这里失效 -> 因此这样做"; put the principle
   first and the replaced choice second.
3. No hedging, no defensive asides, no replies to imagined reviewers, no "值得注意的是/需要指出".
   Limitations only in 5.8, once.
4. No coined terms and NO English abbreviations in the Chinese text (write 自主水下航行器 /
   航行器, 高功耗芯片 or 图形处理器, 集合调整卡尔曼滤波, 交叉熵方法, 联合嵌入预测架构, etc.;
   do not write AUV, GPU, EAKF, CEM, JEPA, RMSE, VOC). Use the names in terms.md exactly for
   strategies, controllers, vehicles and truth models; define a term once, then keep it.
5. Numbers: give the reason first, numbers after; keep most numbers in figures and tables; quote
   95% intervals only where they carry a claim; never invent a number - every number must come
   from facts_v2.md. Units: log10 chlorophyll, stated once.
6. Formal academic Chinese with proper connectives (然而、因此、相反、进一步); no slogans, no
   rhetorical questions, no semicolon chains of facts, no list-style paragraphs in the body
   (lists only for contributions and the five strategies).
7. Figures are part of the argument: refer to each figure where its claim is made; each caption
   = what is shown (panels) + the takeaway in one sentence; do not repeat captions in the text.
   Figure order of first mention: Fig. 1 (method overview) ... Fig. 8 as listed in figures.md.
8. Cite only keys in refs.bib; each citation must support the sentence it is attached to.
9. Length: body (sections 1-6, without captions, tables, algorithm and references) 8,500-10,000
   Chinese characters.

## LaTeX
- Files: sections/title.tex (title text only), abstract.tex, intro.tex, related.tex,
  problem.tex, method.tex, experiments.tex, conclusion.tex, appendix.tex.
- \section{...} numbered by ctex as "1 引言". Figures: \begin{figure}[htbp]\centering
  \includegraphics[width=\linewidth]{fig_<name>}\caption{...}\label{fig:<name>}\end{figure}, placed
  right after the paragraph that first cites it. Tables: \begin{table}[htbp]\centering
  \caption{...}\label{tab:...}\small\resizebox{\linewidth}{!}{\input{tables/main_table.tex}}
  \end{table} (Table 2; add the footnote line given in facts_v2.md under the table with
  \par\footnotesize ...) and \input{tables/settings.tex} for Table 1 (no resizebox needed).
- Escape every % as \%. Use $\cdot$ etc. only inside math. Use \cite{key}.

## Output
The nine files, each preceded by a line "===== FILE: sections/<name>.tex =====".


########## ATTACHED FILE: facts_v2.md ##########

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
  0.270 / 0.269 / 0.267; greedy 0.285; upper confidence bound 0.299; Thompson 0.332; lawnmower
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
  -0.025 to -0.009), and 0.013 / 0.011 on the fast / efficient vehicles (rational 0.282 -> 0.269,
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
  best moving one in every cell, by 0.063 to 0.118 (all intervals above 0). A fourth row (departure 0,
  the satellite map itself as truth) is still being computed: write one sentence on it with
  \TBD{...} where its numbers go; I will fill them in.
- Why stopping does not pay: resampling one place five times lowers its measurement error from
  0.1 to about 0.045, but the bottleneck is the unvisited water (prior uncertainty about 0.26), and
  stopping a third of the time delays reaching the dense water, which the time-averaged score
  penalises.
- Fresher map (1 day old, main truth model): slow computer: tuned = 一直深想 0.250, rehearsal 0.251
  (+0.001, -0.005 to +0.011), one-step metareasoning 0.260 (rehearsal minus -0.009, -0.018 to
  +0.001); the moderate computer is still being computed: write its clause with \TBD{...} where the
  numbers go.

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


########## ATTACHED FILE: figures_rev4.md ##########

# Figures and tables (files exist; write captions and refer to them in the text)

Order of first mention = numbering. Every number below is also in facts_v2.md.

Fig. 1 `fig_overview` - overview of the approach (vector diagram around a 3-D render).
  (A) ocean big data: 3197 days of daily 2-km satellite chlorophyll and SST; the 3-day-old map vs
  the map of the mission day; stale-map error 0.125/0.176/0.210 for 1/2/3 days; seasonal atlas of
  3-day change; 422 bloom windows (274 development, 148 test); a 5.5-million-parameter deep
  forecaster is no better than keeping the latest map -> small scales must be observed.
  (B) before launch: 48 imagined oceans c^(i) = c_map + sigma_k z^(i) (sigma_k calibrated from the
  data), 32 searched / 16 held out; rehearsal: 4 held-out oceans as imagined truths x 5 strategies,
  the bars are the imagined regrets of one real test mission (2025-04-04, moderate computer;
  always go 0.715 chosen, think one in three 0.720, always think 0.734, the stopping strategies
  0.881 and 0.921); the strategy s* with the lowest imagined regret goes to sea.
  (C) during the mission: every 20 minutes go / think / stop; inset: the planner's search score
  keeps rising with the planning budget while real value and held-out judgement level off; the
  operations centre asks at any time where the densest water is; score = time-averaged regret.
  Message: data-calibrated imagined oceans are the yardstick for the value of computation.

Fig. 2 `fig_data` - what eight years of satellite chlorophyll tell the vehicle and what not.
  (a)-(d) spread of the 3-day change of log10 chlorophyll per season over all 3197 days (medians
  0.127 spring, 0.107 summer, 0.103 autumn, 0.081 winter; a band along the Zhejiang-Fujian coast
  and the Changjiang plume front in summer), spring panel with the 274 development and 148 test
  windows; (e) stale-map error 0.125/0.176/0.210 for maps 1/2/3 days old (development windows),
  next to the about 0.15 difference between a same-day satellite map and in-situ chlorophyll;
  (f) a deep spatio-temporal forecaster vs keeping the latest map on the test years (errors
  0.1229 vs 0.1226, 0.1439 vs 0.1439, 0.1487 vs 0.1474 for 1/2/3-day leads).
  Message: the data calibrate how wrong a stale map is, but cannot replace observing.

Fig. 3 `fig_curse` - thinking longer makes the planner believe more, not achieve more.
  (a) value of the chosen route (log10 chlorophyll) vs rollouts per decision (64 to 200,000): the
  search score 0.762 -> 0.917, real value 0.749 -> 0.803 (flat after about 2000), held-out judgement
  0.745 -> 0.802; gap of 0.114 at the largest budget; (b) estimate minus reality: search score bias
  grows; held-out judgement stays within 0.005 with calibrated uncertainty, shifts by -0.06 / +0.07
  with half / 1.5 times the uncertainty but keeps the right gain.
  Message: valuing computation with the planner's own score is biased; held-out oceans are not.

Fig. 4 `fig_main` - every compared controller minus rehearsal (paired, 95% intervals), four
  vehicles (columns), both truth models (filled: same-day satellite map plus small-scale
  variability, main setting; hollow: same-day satellite map itself). Rows grouped: needs past
  missions (tuned fixed strategy, learned selector); online metareasoning (one-step, one-step with
  held-out valuation); survey rules without route planning (greedy, upper confidence bound,
  Thompson, lawnmower); reference (per-mission best in hindsight).
  Message: rehearsal matches the methods that need past missions, beats one-step metareasoning and
  all survey rules (greedy only ties on the slow computer), on every vehicle and both truth models.

Table 1 `tables/settings.tex` - experimental settings.
Table 2 `tables/main_table.tex` - time-averaged regret of every controller, 148 test missions,
  four vehicles x two truth models; bold = best runnable controller in each column; rehearsal row
  shaded. Footnote: which fixed strategy was tuned per vehicle (see facts_v2.md).

Fig. 5 `fig_mech` - why one-step metareasoning loses and what rehearsal chooses (main truth model).
  (a) share of intervals with the high-performance computer on, (b) share spent stopped, for
  one-step metareasoning, the same with held-out valuation, and rehearsal; (c) which strategy
  rehearsal picks per vehicle.
  Message: trusting the search score makes the online controller think in 80-97% of intervals and
  stop in a third; held-out valuation and rehearsal think only as much as the computer needs and
  rarely stop; rehearsal's picks follow the hardware.

Fig. 6 `fig_example` - one test mission (2023-04-15, slow computer; first test mission in date
  order where the two strategies differ by more than 0.1): (a) the 3-day-old map and the start;
  (b) the real ocean with the tracks of always go (blue) and think one interval in three (orange,
  thick where the high-performance computer ran) and the true densest water (star); (c) how far
  the reported location is from the densest water over 24 h (always go stays near 0.4, mean 0.43;
  think one in three reaches the densest water after about 19 h, mean 0.31).
  Message: on a slow computer, background planning alone leaves the vehicle circling mid-window.

Fig. 7 `fig_ablation` - rehearsal with one design choice changed at a time (slow and moderate
  computers, main truth model), change of regret vs the full method with 95% intervals.
  Message: see facts_v2.md "Ablation".

Fig. 8 `fig_phase` - when thinking and stopping pay: grid of low-power computer speed (5-200
  rollouts per minute) x departure of the real ocean from the satellite map (0 = the satellite map
  itself, 0.05, 0.15, 0.30), 60 development missions per cell. (a) best thinking strategy minus
  always go (framed = significantly better); (b) the better stopping strategy minus the best
  strategy that never stops (all significantly positive).


########## ATTACHED FILE: terms.md ##########

# Names to use exactly (strategies, controllers, vehicles, truth models)

- strategy fixed-0: 一直走
- strategy fixed-1: 一直深想
- strategy periodic-100: 三段深想一段
- strategy periodic-300: 三段停下深想一段
- strategy periodic-200: 三段停下复测一段
- controller rational: 单步元推理
- controller double: 单步元推理（留出估值）
- controller rehearsal: 出发前预演（本文）
- controller rehearsal-self: 预演（以搜索过的海洋为真值）
- controller tuned: 调好的固定策略
- controller learned: 按历史任务学习的选择器
- controller lawnmower: 割草机式全覆盖
- controller greedy: 贪心：驶向估计最浓处
- controller ucb: 上置信界采样
- controller thompson: 汤普森采样
- controller random5: 五种策略随机选
- controller random3: 三种不停策略随机选
- controller oracle: 每次任务事后最优（参考）
- vehicle weak: 慢计算机 (5 次/分，+20 W)
- vehicle moderate: 中等计算机 (20 次/分，+20 W)
- vehicle strong: 快计算机 (100 次/分，+20 W)
- vehicle efficient: 省电加速器 (20 次/分，+5 W)
- truth model sat+: 当天卫星图 + 小尺度变化
- truth model sat: 当天卫星图
- 留出海洋 = the 16 imagined oceans never used by the search; 搜索用海洋 = the 32 searched ones
- 想象海洋 = one member of the vehicle's ensemble; 推演 = one route scored on one imagined ocean
- 时间平均遗憾 = the score; 高功耗芯片 = the high-performance computer; 低功耗处理器 = the background one

########## ATTACHED FILE: tables/settings.tex (Table 1) ##########

\begin{tabular}{@{}p{0.17\linewidth}p{0.79\linewidth}@{}}
\toprule
项目 & 设置 \
\midrule
卫星数据 & 美国国家海洋和大气管理局海岸观测网多星融合叶绿素 a 产品（经验正交函数插补去云），2 km、逐日，2018-01-01 至 2026-10-23 共 3197 天；喷气推进实验室多尺度融合海表温度，0.01° \
任务窗口 & 每年 4--6 月浙江外海陆架（26.5°--31.5°N，121.5°--125°E）局部峰值超过 5 mg/m$^3$ 处，80 km $\times$ 80 km（40 $\times$ 40 个 2 km 网格）；开发 274 个（2018--2022 年），测试 148 个（2023--2026 年） \
真实海洋 & 任务当天卫星图叠加卫星分辨不出的小尺度变化（标准差 0.15，相关尺度 6 km，主设置）；或任务当天卫星图本身 \
航行器 & 航速 1.5 m/s，电池 1 kWh；平台 15 W，推进 30 W，高功耗芯片 +20 W（省电加速器 +5 W）；任务 24 h，耗尽电量即停 \
决策周期 & 20 min；走一段约 1.8 km、采样约 2 次；停下漂流采样 5 次；荧光计单次误差 0.1 \
想象海洋 & 48 个（32 个用于搜索航线，16 个留出），由 3 天前卫星图与数据标定的误差生成，空间相关长度 10 km，随每个样本同化更新 \
规划器 & 交叉熵搜索经两个航路点的折线航线，跨周期热启动；低功耗处理器每分钟 5、20 或 100 次推演（条件扫描 5--200 次），高功耗芯片为其 50 倍 \
出发前预演 & 4 个留出海洋作假想真值 $\times$ 5 种用时策略，各完整模拟 24 h，选平均假想遗憾最小者 \
评价 & 时间平均遗憾（对数浓度，越低越好）；配对差值的 95\% 置信区间由按赤潮周整组的自助重抽样得到 \
\bottomrule
\end{tabular}


########## ATTACHED FILE: tables/main_table.tex (Table 2, generated) ##########

\begin{tabular}{@{}llcccccccc@{}}
\toprule
 & & \multicolumn{4}{c}{真值：当天卫星图 + 小尺度变化} & \multicolumn{4}{c}{真值：当天卫星图} \\
\cmidrule(lr){3-6}\cmidrule(l){7-10}
类别 & 控制方式 & 慢计算机 & 中等计算机 & 快计算机 & 省电加速器 & 慢计算机 & 中等计算机 & 快计算机 & 省电加速器 \\
\midrule
固定策略 & 一直走 & 0.374 & 0.267 & 0.267 & 0.267 & 0.281 & 0.196 & 0.194 & 0.195 \\
 & 一直深想 & 0.273 & 0.269 & 0.269 & 0.267 & 0.195 & 0.194 & 0.193 & \textbf{0.190} \\
 & 三段深想一段 & \textbf{0.270} & 0.269 & \textbf{0.265} & 0.266 & \textbf{0.194} & \textbf{0.190} & \textbf{0.191} & 0.191 \\
 & 三段停下深想一段 & 0.331 & 0.328 & 0.327 & 0.327 & 0.252 & 0.248 & 0.245 & 0.249 \\
 & 三段停下复测一段 & 0.408 & 0.335 & 0.331 & 0.335 & 0.319 & 0.251 & 0.248 & 0.251 \\
\midrule
需要历史任务 & 调好的固定策略$^{a}$ & \textbf{0.270} & 0.269 & 0.267 & 0.267 & \textbf{0.194} & 0.196 & \textbf{0.191} & 0.191 \\
 & 按历史任务学习的选择器 & 0.278 & 0.269 & 0.273 & \textbf{0.266} & 0.200 & 0.197 & \textbf{0.191} & \textbf{0.189} \\
\midrule
在线元推理 & 单步元推理 & 0.287 & 0.287 & 0.282 & 0.278 & 0.202 & 0.202 & 0.204 & 0.199 \\
 & 单步元推理（留出估值） & 0.278 & 0.270 & -- & -- & -- & -- & -- & -- \\
\midrule
巡测规则 & 割草机式全覆盖 & 0.424 & 0.424 & 0.424 & 0.424 & 0.328 & 0.328 & 0.328 & 0.328 \\
 & 贪心：驶向估计最浓处 & 0.285 & 0.285 & 0.285 & 0.285 & 0.206 & 0.206 & 0.206 & 0.206 \\
 & 上置信界采样 & 0.299 & 0.299 & 0.299 & 0.299 & 0.224 & 0.224 & 0.224 & 0.224 \\
 & 汤普森采样 & 0.332 & 0.332 & 0.332 & 0.332 & 0.256 & 0.256 & 0.256 & 0.256 \\
\midrule
\rowcolor{violet!8}本文 & 出发前预演（本文） & 0.276 & \textbf{0.265} & 0.268 & \textbf{0.266} & 0.197 & 0.191 & 0.195 & 0.191 \\
\midrule
参考 & 每次任务事后最优（参考） & 0.250 & 0.243 & 0.243 & 0.242 & 0.183 & 0.179 & 0.180 & 0.180 \\
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

@article{galceran2013coverage,
  author  = {Galceran, Enric and Carreras, Marc},
  title   = {A survey on coverage path planning for robotics},
  journal = {Robotics and Autonomous Systems},
  year    = {2013},
  volume  = {61},
  number  = {12},
  pages   = {1258--1276},
  doi     = {10.1016/j.robot.2013.09.004}
}

@article{srinivas2012gpucb,
  author  = {Srinivas, Niranjan and Krause, Andreas and Kakade, Sham M. and Seeger, Matthias W.},
  title   = {Information-theoretic regret bounds for {Gaussian} process optimization in the bandit setting},
  journal = {IEEE Transactions on Information Theory},
  year    = {2012},
  volume  = {58},
  number  = {5},
  pages   = {3250--3265},
  doi     = {10.1109/TIT.2011.2182033}
}

@article{russo2018thompson,
  author  = {Russo, Daniel J. and Van Roy, Benjamin and Kazerouni, Abbas and Osband, Ian and Wen, Zheng},
  title   = {A tutorial on {Thompson} sampling},
  journal = {Foundations and Trends in Machine Learning},
  year    = {2018},
  volume  = {11},
  number  = {1},
  pages   = {1--96},
  doi     = {10.1561/2200000070}
}

@article{hollinger2014sampling,
  author  = {Hollinger, Geoffrey A. and Sukhatme, Gaurav S.},
  title   = {Sampling-based robotic information gathering algorithms},
  journal = {The International Journal of Robotics Research},
  year    = {2014},
  volume  = {33},
  number  = {9},
  pages   = {1271--1287},
  doi     = {10.1177/0278364914533443}
}


########## ATTACHED FILE: main.tex (template; do not change) ##########

% 浙江大学《海洋大数据技术原理与应用》课程论文。编译：bash build.sh
\documentclass[zihao=-4, a4paper, oneside]{ctexart}

% ---------- 版面 ----------
\usepackage[top=2.54cm, bottom=2.54cm, left=3.0cm, right=2.6cm, headheight=15pt]{geometry}
\usepackage{setspace}
\setstretch{1.35}
\setmainfont{Times New Roman}
\setCJKmainfont[BoldFont=SimHei, ItalicFont=KaiTi]{SimSun}
\setCJKsansfont{SimHei}
\setCJKfamilyfont{hei}{SimHei}
\setCJKfamilyfont{kai}{KaiTi}
\usepackage{amsmath, amssymb, bm}
\usepackage{graphicx, subcaption, booktabs, multirow, array}
\usepackage[table]{xcolor}
\usepackage{algorithm}
\usepackage{algpseudocode}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[sort&compress, square, comma, numbers]{natbib}
\usepackage{caption}
\usepackage{placeins}

\captionsetup{font=small, labelsep=quad, labelfont=bf}
\captionsetup[figure]{name=图}
\captionsetup[table]{name=表}
\floatname{algorithm}{算法}
\renewcommand{\algorithmicrequire}{\textbf{输入：}}
\renewcommand{\algorithmicensure}{\textbf{输出：}}
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
\fancyhead[C]{\zihao{5}\songti 海洋大数据技术原理与应用\quad 课程论文}
\fancyfoot[C]{\zihao{5}\thepage}
\renewcommand{\headrulewidth}{0.6pt}

\newcommand{\coverline}[2]{{\heiti\makebox[5.4em][s]{#1}}：\ \underline{\makebox[15em][c]{#2}}}
\newcommand{\TBD}[1]{\textcolor{red}{[待补：#1]}}

\begin{document}

% ---------- 封面（浙江大学课程论文样式：校名题字、课程名、校徽、信息栏） ----------
\begin{titlepage}
  \centering
  \singlespacing
  \vspace*{0.6cm}
  \includegraphics[width=0.40\textwidth]{logo/zjuchar}\par
  \vspace{0.8cm}
  {\zihao{-1}\heiti 《海洋大数据技术原理与应用》课程论文\par}
  \vspace{1.0cm}
  \includegraphics[width=0.27\textwidth]{logo/zju}\par
  \vspace{1.0cm}
  {\zihao{-2}\heiti \input{sections/title}\par}
  \vspace{1.1cm}
  {\zihao{4}
  \begin{tabular}{@{}l@{}}
    \coverline{学年学期}{2026--2027 学年秋学期}\\[10pt]
    \coverline{姓名与学号}{徐陈栋\quad 3240100538}\\[10pt]
    \coverline{年级与专业}{24 级海洋工程与技术}\\[10pt]
    \coverline{任课教师}{张帆\quad 研究员}\\[10pt]
    \coverline{开课学院}{海洋学院}
  \end{tabular}\par}
  \vfill
  {\zihao{4}\heiti 提交日期\quad 2026 年 11 月\quad\ \ 日\par}
  \vspace{0.8cm}
\end{titlepage}

% ---------- 题目、作者与摘要（期刊论文版式） ----------
\pagenumbering{arabic}
\begin{center}
  {\zihao{-2}\heiti \input{sections/title}\par}
  \vspace{6pt}
  {\zihao{4}\kaishu 徐陈栋\par}
  {\zihao{5}\songti （浙江大学\ 海洋学院，浙江\ 舟山\ 316021）\par}
\end{center}
\vspace{4pt}
\input{sections/abstract}

% ---------- 正文 ----------
\input{sections/intro}
\input{sections/related}
\input{sections/problem}
\input{sections/method}
\input{sections/experiments}
\input{sections/conclusion}

% ---------- 参考文献 ----------
\phantomsection
\bibliographystyle{gbt7714-numerical}
\bibliography{refs}

% ---------- 附录 ----------
\appendix
\input{sections/appendix}

\end{document}


########## ATTACHED FILE: previous draft sections/title.tex (wording source only; superseded) ##########

基于想象海洋出发前预演的自主水下航行器思考与行动权衡研究


########## ATTACHED FILE: previous draft sections/abstract.tex (wording source only; superseded) ##########

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


########## ATTACHED FILE: previous draft sections/body.tex (wording source only; superseded) ##########

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
预演本身运行在母船或岸上计算机上：慢计算机配置单次任务需约190万次推演，在机载GPU上需约125小时，而在普通台式机单核上每次任务仅需数秒至数十秒。

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


########## ATTACHED FILE: previous draft sections/appendix.tex (wording source only; superseded) ##########

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

<details><summary>展开（共 39813 字符）</summary>

```
===== FILE: sections/title.tex =====
基于留出想象海洋与出发前预演的自主水下航行器计算与观测权衡方法

===== FILE: sections/abstract.tex =====
\noindent{\heiti 摘要：}卫星海洋遥感大数据为自主水下航行器提供了大尺度先验环境场，使机动平台能够面向高动态海洋现象开展靶向观测。然而水下作业期间缺乏实时通信且机载电池与任务时间受限，面对滞后数日且缺失小尺度结构的卫星底图，航行器必须在开启高功耗芯片深入规划航线、维持低功耗处理器后台规划继续巡航采样以及关停推进器原位复测之间合理分配时间与能量。现有固定分配策略依赖同型平台的历史任务调参，而经典在线单步元推理直接用规划器在搜索样本上的内部得分增量评估计算收益，会因优化器诅咒高估计算价值并陷入过度规划。为此，本文提出以卫星大数据标定的留出想象海洋作为评判计算价值的独立标尺，构建出发前全任务预演与在线留出估值方法。该方法利用八年东海卫星叶绿素数据标定滞后底图误差，围绕3天前旧图生成48个随现场采样集合同化更新的想象海洋，并将其固定划分为32个搜索用海洋与16个留出海洋。下水前由母船或岸基计算机以4个留出海洋为假想真值，按机载算力与电池功耗完整模拟五种用时策略的24小时任务并选出时间平均遗憾最低者，或在线按周期在留出海洋上评估计算与采样收益。基于2018至2026年东海3197天数据构建的422个赤潮任务窗口、四种机载硬件及两种真值模型的实验表明，留出海洋评判在64至200,000次推演下与真实航线价值偏差不超过0.005。在148个测试任务上，出发前预演在主真值设置下的时间平均遗憾为0.265至0.276，无需历史任务即达到调好的固定策略与按历史任务学习的选择器水平，并比经典单步元推理降低0.011至0.022，同时在线引入留出估值可将单步元推理开启高功耗芯片的比例从80\%至97\%压低至30\%至44\%并达到预演水平。上述结果证实，将历史卫星遥感数据转化为独立于搜索过程的留出想象海洋可有效消除计算自评偏差，使航行器在无历史巡测记录条件下实现机载算力与观测行动的自适应权衡。

\vspace{4pt}
\noindent{\heiti 关键词：}海洋大数据；自主水下航行器；元推理；集合数据同化；赤潮巡测；优化器诅咒

\vspace{10pt}
\begin{center}
  {\zihao{4}\bfseries Balancing Computation and Observation for Autonomous Underwater Vehicles via Data-Calibrated Held-Out Imagined Oceans and Pre-Launch Rehearsal\par}
  \vspace{4pt}
  {\zihao{5} XU Chendong\par}
  {\zihao{-5}\itshape (Ocean College, Zhejiang University, Zhoushan 316021, China)\par}
\end{center}
\vspace{4pt}

\noindent{\bfseries Abstract:} Satellite ocean remote sensing big data provides large-scale prior fields for autonomous underwater vehicles, enabling targeted mobile observation of dynamic marine phenomena. Because underwater operations lack real-time communication and are constrained by onboard battery capacity and mission duration, a vehicle carrying a multi-day-old, spatially smoothed satellite map must continuously trade off activating a high-power chip for deep route planning against cruising to collect new samples under low-power background planning or stopping propulsion to resample locally. Existing fixed time-allocation rules require tuning on historical missions from the same hardware platform, whereas classic online one-step metareasoning evaluates computation using the planner's own score improvement on the searched ensemble members, which is inflated by the optimizer's curse and leads to severe over-planning. This paper proposes using uncertainty-calibrated held-out imagined oceans derived from satellite big data as an independent yardstick to judge the value of computation, instantiated both as pre-launch whole-mission rehearsal and as online held-out valuation. Using eight years of East China Sea satellite chlorophyll-a data to calibrate stale-map error, the vehicle generates 48 imagined oceans around a 3-day-old map, updates them with in-situ fluorometer measurements via a localised ensemble adjustment Kalman filter, and partitions them into 32 searched oceans and 16 held-out oceans. Before launch, a support-ship or shore computer treats 4 held-out oceans as imagined truths and simulates complete 24-hour missions for five time-allocation strategies under the vehicle's actual processor speed and battery budget to select the strategy with the lowest mean regret, while the online variant evaluates single-step computation and sampling gains on the 16 held-out oceans. Experiments across 422 bloom windows extracted from 3,197 daily maps (2018--2026), four hardware configurations, and two truth models show that held-out evaluation remains within 0.005 of true route value from 64 to 200,000 rollouts. Across 148 test missions under the main truth model, pre-launch rehearsal achieves time-averaged regrets of 0.265--0.276, matching fixed strategies tuned on historical missions and a learned strategy selector without requiring prior missions, while outperforming classic one-step metareasoning by 0.011--0.022 and heuristic survey rules. Replacing self-valuation with held-out valuation inside online one-step metareasoning similarly reduces high-power chip activation from 80\%--97\% to 30\%--44\% of intervals and matches rehearsal performance. These results demonstrate that decoupling route search from value judgement via data-calibrated held-out imagined oceans eliminates planner self-assessment bias and adapts time allocation to onboard hardware without historical mission tuning.

\vspace{4pt}
\noindent{\bfseries Keywords:} ocean big data; autonomous underwater vehicle; metareasoning; ensemble data assimilation; harmful algal bloom survey; optimizer's curse

===== FILE: sections/intro.tex =====
\section{引言}

卫星海洋遥感大数据与自主水下航行器的结合，正在将海洋环境监测从按预设航线走航转变为由先验地图引导的现场自适应巡测\cite{fossum2019}。在这一观测范式中，多年累积的卫星遥感产品提供了大尺度的海洋环境背景与演变统计，而自主水下航行器则深入云层遮挡与遥感平滑无法企及的现场水体采集高分辨率样本。然而机动观测平台受制于有限的机载电池能量、嵌入式计算速率与固定的作业时间窗口\cite{xiao2020thinking, magnino2026metareasoning}。航行器在现场获取每一条新观测后，既可以调用机载高功耗芯片开展密集的未来航线推演以优化后续探索路径，也可以维持低功耗处理器后台规划而将宝贵的电能与时间用于长距离巡航采样或原位重复测量\cite{horvitz1987reasoning, russell1991right, shen2025thinking}。由于内部航线计算与外部物理观测共同消耗同一块电池和同一个任务窗口，何时应当继续计算、何时应当继续观测，构成了大数据驱动自主海洋观测系统的核心控制问题\cite{hunt2021formalizing}。

东海有害赤潮应急巡测集中体现了先验卫星底图失真、水下通信受阻与机载资源受限带来的决策困难\cite{fossum2019, lou2014diurnal}。根据2023年中国海洋灾害公报，我国海域全年发现赤潮46次，累计面积约$1500\text{ km}^2$，其中有毒有害赤潮达29次\cite{mnr2024bulletin}。在浙江近海台州、温州与宁波外海，晚春至初夏常暴发高密度的东海原甲藻赤潮\cite{zhao2025distinguishing}，且表层藻华斑块在潮汐作用下发生剧烈的往复漂移与形态演变\cite{lou2014diurnal}。赤潮暴发时，应急指挥中心通常向$80\text{ km}\times 80\text{ km}$的目标海域派出一台百米级自主水下航行器开展24小时紧急巡测，要求航行器尽早定位叶绿素浓度最高的核心水体，并随时响应指挥中心对最浓处位置的查询\cite{remus100}。受多星遥感产品合成延迟、云区经验正交函数插补平滑\cite{beckers2003dineof}、水色反演固有偏差\cite{ye2021cocts}以及调查船航渡时间的共同影响，航行器下水前装入的往往是3天前的旧卫星图。加之航行器在水下作业期间几乎无法与母船或岸站实时通信，全部航线重规划与资源调配均须由机载计算机在航行途中独立完成\cite{jetsonorinnx}。

传统的海洋巡测规则与预设时间分配策略无法在缺乏历史任务数据的条件下适配不同的机载硬件。一方面，海洋调查中广泛采用的割草机式全覆盖\cite{galceran2013coverage}、贪心追踪以及基于高斯过程的上置信界采样\cite{srinivas2012gpucb}和汤普森采样\cite{russo2018thompson}等启发式自适应规则，均将每步决策的计算开销视为零或固定常数，忽略了多步前瞻航线规划对规避局部次优峰值的关键作用\cite{hollinger2014sampling}。另一方面，若在多步规划器之上采用固定的时间分配策略，例如全程仅靠低功耗处理器后台规划的“一直走”或周期性开启高功耗芯片的固定比例规则，其表现高度依赖于机载处理器的推演速度与芯片功耗。当航行器更换嵌入式计算模块或电池配置时，唯有依靠该型硬件在大量历史赤潮任务中的实测表现才能选出合适的固定策略，而在新平台首次投入应急巡测时并不具备这一历史任务档案。

从历史巡测任务中直接训练策略选择器同样受困于高昂的数据采集成本与剧烈的任务间环境波动。近年来机器人元推理研究尝试利用历史任务数据训练回归或分类模型，根据出发前的环境特征为每次任务自动选择计算预算或时间分配策略\cite{sung2021quit, magnino2026metareasoning}。然而海洋赤潮现场的初值格局、峰值位置与航行器入水起点千差万别，不同任务窗口之间的天然遗憾波动远远大于几种优良用时策略之间的平均性能差距。因此，基于旧卫星图静态特征训练的选择器极易被任务间的背景噪声淹没，不仅需要上百次历史巡测任务作为训练样本，而且在未知测试年份上的泛化表现依然无法超越简单的固定策略。

人工智能领域的经典在线单步元推理虽无需历史任务训练，但因轻信规划器在搜索样本上的自评得分而不可避免地陷入过度规划\cite{horvitz1987reasoning, russell1991right, cuadron2025overthinking}。经典元推理在每个控制周期通过比较“多算一步带来的航线得分增量”与“耗电及延误造成的代价”来在线决定是否开启高功耗芯片或停下复测\cite{lin2015metareasoning, elboher2023formal}。由于航行器无法预知真实海洋，规划器只能在一组由旧卫星图生成的想象海洋上搜索航线。当规划器在同一批有限的想象海洋上既搜索最优航路点又评估该航线的预期收益时，优化过程会精细迎合这批特定样本中的随机正涨落，产生决策分析中的“优化器诅咒”\cite{smith2006curse, vanhasselt2010double}。即使额外推演在真实海洋中早已不再改善航线质量，规划器看到的内部自评得分仍随推演次数增加而持续虚高，进而误导单步元推理频繁开启高功耗芯片并中途停下漂流\cite{jiang2015horizon, cuadron2025overthinking}。

针对上述症结，本文的核心思想是：航行器绝不能依据规划器自身的搜索得分来决定是否继续计算，而应利用多年卫星海洋大数据标定误差的留出想象海洋作为独立标尺，在未参与航线搜索的想象海洋上评判计算与观测的真实结果。具体而言，本文利用八年东海卫星叶绿素数据标定滞后底图的误差统计，围绕出发前旧图生成48个随现场荧光计采样经集合调整卡尔曼滤波\cite{anderson2001eakf, gaspari1999correlation}同步更新的想象海洋，并将其严格划分为32个搜索用海洋与16个留出海洋。基于这一“搜索与评判分离”准则，本文提出了两种无需历史巡测任务的控制方式：下水前，利用母船或岸基计算机以4个留出海洋为假想真值，按机载算力与功耗将五种候选策略各完整预演一遍24小时任务并择优执行；航行中，若需按周期在线决策，则在单步元推理中将计算与采样的价值改由16个留出海洋评估，从而在离线与在线两个层面根除自评乐观偏差。

本文的主要贡献归纳如下：
\begin{itemize}
  \item \textbf{提出独立于搜索过程的计算价值留出评判准则：}揭示了经典元推理在未知海洋巡测中过度计算的根源在于规划器对搜索用海洋的过拟合，提出将多年卫星遥感数据标定的想象海洋划分为搜索用海洋与留出海洋，以搜索未曾接触的留出海洋上的结果作为衡量计算收益的无偏标尺。
  \item \textbf{构建面向硬件自适应的出发前全任务预演与在线留出估值方法：}设计了结合局地化集合同化与交叉熵航线规划的五种用时策略，提出在母船或岸基计算机上以留出海洋为假想真值开展全任务出发前预演，并将同一留出评判机制嵌入在线单步元推理，无需任何历史巡测任务即可适配不同机载处理器速度与功耗。
  \item \textbf{提供基于八年东海赤潮窗口与双真值模型的系统实证及边界刻画：}在3197天卫星数据构建的422个赤潮窗口、四种机载硬件与两种真值模型上开展了配对重抽样检验，证实深度时空模型无法替代现场采样、留出评判可将跨三个半数量级推演预算的价值估计偏差控制在0.005以内、停下复测在全参数空间均得不偿失，且出发前预演与在线留出估值均达到依赖历史任务方法的同等水平。
\end{itemize}

本文其余章节安排如下：第2节回顾元推理、海洋自适应采样及优化器诅咒与集合数据同化的相关研究；第3节建立东海赤潮应急巡测的场景模型、航行器机电功耗模型与时间平均遗憾目标，并剖析问题的三重内在矛盾；第4节阐述数据标定想象海洋、搜索与评判分离、出发前预演及在线留出估值方法；第5节报告遥感数据统计、自评偏差验证、主实验对比、作用机制、消融实验与适用边界相图，并讨论研究局限性；第6节总结全文结论。

===== FILE: sections/related.tex =====
\section{相关工作}

\subsection{元推理与随时规划中的计算与行动权衡}

有限理性与元推理理论旨在回答智能体在面对计算资源约束时应如何分配内部推理时间与外部物理行动\cite{horvitz1987reasoning, russell1991right}。经典单步元推理通过估计额外一次搜索迭代对当前最优动作期望效用的提升量，并在计算期望增益低于时间延迟成本时终止搜索\cite{lin2015metareasoning}。在移动机器人运动规划与并发控制中，由于机体移动与后台计算可以并行执行，研究者提出了边移动边思考的并发控制框架与形式化元推理模型，以权衡继续规划带来的路径质量改善与推迟动作切换造成的跟踪偏差\cite{xiao2020thinking, elboher2023formal}。针对单步解析估计难以捕捉长周期代价的问题，另一类工作利用历史任务轨迹训练停止策略或计算预算选择器，根据环境特征直接预测不同算力预算的收益\cite{sung2021quit, magnino2026metareasoning}。近期在大模型智能体研究中也发现了类似的推理与交互权衡现象，过度拉长内部思考链反而会挤占环境交互机会并降低任务成功率\cite{shen2025thinking, cuadron2025overthinking, hunt2021formalizing}。然而现有元推理方法在评估额外规划收益时，普遍直接信任规划器在自身搜索空间或内部模型上的自评得分，或依赖大量历史任务数据训练预算选择器。本文则指出在不确定海洋场中规划器自评得分受优化器诅咒严重污染，并利用留出想象海洋在无需历史任务的条件下实现了计算价值的无偏评估。

\subsection{海洋自适应采样与机器人信息收集}

自主水下航行器在海洋藻华追踪与锋面观测中的应用，推动了从规则覆盖向信息驱动自适应采样的演进\cite{fossum2019}。传统海洋调查多采用割草机式全覆盖航线以均匀扫测目标海域\cite{galceran2013coverage}，但在大范围赤潮应急巡测中，受航行器巡航速度与24小时作业窗口限制，全覆盖航线仅能扫过窗口的一小部分水域。为提高热区定位效率，信息收集算法通常利用高斯过程回归维护环境场的均值与方差，并采用贪心策略、上置信界采样\cite{srinivas2012gpucb}或汤普森采样\cite{russo2018thompson}引导航行器驶向高浓度或高不确定性位置，或通过采样树搜索规划多步信息收集路径\cite{hollinger2014sampling}。与此同时，针对东海原甲藻赤潮的卫星遥感研究揭示了藻华在晚春至初夏的高发规律及随潮汐往复漂移的日内变化特征\cite{lou2014diurnal, zhao2025distinguishing}，为巡测提供了物理背景。然而现有海洋自适应采样方法均假定机载路径规划的计算开销可忽略或固定不变，未考虑高功耗芯片深想与推进电机共享机载电池及作业时间的耦合约束。本文则将机载算力速度、芯片功耗与原位复测统一纳入随水漂移参考系下的决策空间，系统揭示了多步航线规划与机动采样之间的收益边界。

\subsection{优化器诅咒与卫星数据驱动的集合数据同化}

在随机优化与强化学习中，使用同一批有限样本同时开展策略寻优与价值估计会引入系统性的正向偏差，这一现象在决策分析中被称为“优化器诅咒”\cite{smith2006curse}。当候选方案数量或搜索预算增大时，最大化算子会放大样本估计中的随机正误差，导致选出方案的事后真实表现显著低于优化器的内部预期，而双估计方法通过将动作选择与价值评估解耦至独立样本集来消除这一过估计\cite{vanhasselt2010double}，且模型误差还会进一步限制有效规划视野\cite{jiang2015horizon}。在海洋环境重构方面，业务化水色遥感利用经验正交函数缺失数据插补方法生成逐日无云叶绿素场\cite{beckers2003dineof}，结合多尺度融合海表温度产品\cite{chin2017mur}与水色传感器实测精度评估\cite{ye2021cocts}，以及自监督联合嵌入预测架构等时空模型\cite{assran2025vjepa2}，共同刻画了表层海洋的演变尺度。为融合现场观测，序列集合调整卡尔曼滤波\cite{anderson2001eakf}配合五阶分段有理局地化函数\cite{gaspari1999correlation}被广泛用于更新状态集合。然而现有研究尚未将集合同化样本集与双估计思想结合以解决元推理中的计算自评偏差。本文首次将同化更新的想象海洋划分为搜索用海洋与留出海洋，使卫星大数据标定的集合成员直接充当评判计算价值的外部标尺。

===== FILE: sections/problem.tex =====
\section{问题建模}

\subsection{巡测场景与卫星遥感数据集}

东海赤潮应急巡测场景建立在八年真实卫星遥感叶绿素与海表温度大数据之上，航行器遇到的真实海洋由任务当天的实测卫星图构建，而航行器出发时仅携带3天前的旧卫星图。本文使用的数据集源自美国国家海洋和大气管理局海岸观测网的逐日多星融合叶绿素 a 产品，该产品融合了多颗极轨卫星水色传感器的观测，并通过经验正交函数插补算法填补云层遮挡区\cite{beckers2003dineof}，空间分辨率为$2\text{ km}$，时间跨度为2018年1月1日至2026年10月23日共3197天，覆盖东海北纬$25^\circ\text{--}33^\circ$、东经$119.5^\circ\text{--}127^\circ$海域（每日$385\times 361$个网格）。辅助时空预测实验还使用了喷气推进实验室制作的多尺度融合海表温度逐日产品（原始分辨率$0.01^\circ$，重采样至$0.04^\circ$）\cite{chin2017mur}。全文除特别说明外，所有叶绿素 a 浓度、误差标准差与遗憾指标均以对数浓度$\log_{10}(\text{叶绿素 a 浓度}/\text{mg m}^{-3})$为单位。

为构建贴近实战的离岸赤潮应急任务集，本文从每年4月至6月藻华高发期的卫星序列中按统一判据切出正方形巡测窗口。具体而言，在浙江外海陆架区（北纬$26.5^\circ\text{--}31.5^\circ$，东经$121.5^\circ\text{--}125^\circ$）检索离岸至少$30\text{ km}$、经空间平滑后局部峰值超过$5\text{ mg m}^{-3}$的藻华中心，将该中心随机平移至多$16\text{ km}$后截取$80\text{ km}\times 80\text{ km}$（$40\times 40$个$2\text{ km}$网格）的任务窗口，将距陆地或岛屿$15\text{ km}$以内的网格设为禁航区，并筛选可航行水域占比不低于80\%且窗内对数浓度极差不低于0.3的窗口。按此标准共获得422个赤潮任务窗口，其中2018至2022年的274个窗口作为开发集，2023至2026年的148个窗口作为独立的测试集。每次任务开始时，航行器从窗口边缘随机选取的一个可航行网格入水出发。鉴于静止轨道水色卫星逐时观测表明东海表层赤潮斑块主要随表层水体与潮汐整体往复漂移\cite{lou2014diurnal}，本文将航行器运动、叶绿素分布与数据同化建立在随表层水体漂移的参考系中，此时斑块相对于水体保持静止，而海流平流与生消过程的作用则完整体现在3天滞后卫星图与任务当天卫星图之间的实测演变统计中。

为同时检验方法对卫星未分辨小尺度结构的适应性以及在纯实测遥感场上的表现，本文设置两种真实海洋模型。主设置称为“当天卫星图 + 小尺度变化”，在任务当天的真实卫星图上叠加一个标准差为$s_{\text{sat}}=0.15$、空间相关长度为3个网格（$6\text{ km}$）的零均值高斯随机场，用以表征2 km插补卫星图平滑掉的亚像素斑块与反演残差，其幅值依据海洋一号丙星水色传感器在东海与南海现场验证所得约39\%的无偏相对百分比差异（折合对数空间约0.15）标定\cite{ye2021cocts}。第二种设置称为“当天卫星图”，直接以任务当天的真实卫星叶绿素图本身作为真实海洋（即$s_{\text{sat}}=0$）。在两种设置下，航行器出发时携带的先验底图均为任务前3天的真实卫星图$c_{\text{map}}(\mathbf{x})$。

\subsection{航行器动作空间与能耗模型}

机载计算与机动观测的资源冲突由百米级轻型自主水下航行器的机电功耗特性与20分钟离散控制周期共同刻画。参照典型轻型航行器参数\cite{remus100}，航行器对水巡航速度为$1.5\text{ m/s}$（约3节），机载锂电池总能量为$1\text{ kWh}$，在3节巡航状态下续航约22小时，对应巡航总功率$45\text{ W}$，其中基础平台功率为$15\text{ W}$（含导航、荧光计传感器及常驻后台运行的低功耗处理器），推进电机功率为$30\text{ W}$。机载高功耗芯片参照嵌入式边缘图形处理器模块设定（典型功耗范围$10\text{--}25\text{ W}$）\cite{jetsonorinnx}，开启深想时额外消耗$+20\text{ W}$功率（在“省电加速器”硬件配置下额外消耗$+5\text{ W}$），其航线推演速度为低功耗处理器的50倍。由于本文在二维表层场上采用的双航路点折线规划器是对真实水下三维路径评估（需同时积分海流、深度剖面与地形避障约束）的简化替代，决定规划质量的关键因素是机载处理器相对于规划问题的推演速度，因此实验以低功耗处理器每分钟完成的推演次数表征基础算力（取5、20或100次/分，并在5至200次/分范围内开展参数扫描）。

在时长$T=24\text{ h}$的任务窗口内，时间按每段$\Delta t = 20\text{ min}$划分为72个连续决策周期，每个周期内航行器的机体动作与大脑规划并行执行\cite{xiao2020thinking, elboher2023formal}。在机体动作方面，若航行器选择“走”，则开启推进器（$30\text{ W}$）沿当前航线以$1.5\text{ m/s}$航行$1.8\text{ km}$，机载荧光计每航行$1\text{ km}$独立采样一次（每周期获得约2个样本），在电量充足时24小时累计航程约$120\text{--}130\text{ km}$，约为$80\text{ km}$窗口宽度的1.5倍。若航行器选择“停下”，则关停推进器（推进功率为$0\text{ W}$，仅消耗$15\text{ W}$平台功率）随水体漂流，荧光计每4分钟对同一水体采样一次，每周期共获得5个独立样本。荧光计单次测量值$y$与所在网格真实对数浓度$c(\mathbf{x})$的关系满足高斯观测模型：
\begin{equation}
  y = c(\mathbf{x}) + \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, 0.1^2)
  \label{eq:obs}
\end{equation}
在大脑规划方面，每个周期航行器可选择仅维持低功耗处理器后台规划（额外功耗$0\text{ W}$），或开启高功耗芯片“深想”（额外功耗$+20\text{ W}$或$+5\text{ W}$，本周期推演次数提升至后台的50倍）。为消除规划计算耗时带来的位置滞后，新航线常に以航行器在当前20分钟周期结束时刻的预计位置为起点进行搜索，并在周期结束瞬间无缝替换旧航线。当任务满24小时或电池电量耗尽时，航行器停止机动与采样。

\subsection{实时报告机制与时间平均遗憾目标}

应急巡测的目标是尽早找到并持续锁定窗口内叶绿素浓度最高的水体，因此评价指标必须同时奖励最终定位精度与到达高浓水体的时间效率。在$T=24\text{ h}$作业期间的任意时刻$t \in [0, T]$，应急指挥中心均可查询当前已知的最浓水体位置。为防止航行器凭借未经证实的旧图先验妄下结论，规定航行器只能从截至时刻$t$已实际造访过的网格集合$\mathcal{V}(t)$中，报告当前内部集合估计均值$\bar{c}_t(\mathbf{x})$最高的位置$\hat{\mathbf{x}}(t)$：
\begin{equation}
  \hat{\mathbf{x}}(t) = \arg\max_{\mathbf{x}\in\mathcal{V}(t)} \bar{c}_t(\mathbf{x})
  \label{eq:answer}
\end{equation}
若航行器在$24\text{ h}$前因电池耗尽而停机，则停机后的报告位置$\hat{\mathbf{x}}(t)$保持冻结直至$T=24\text{ h}$结束。定义单次任务的时间平均遗憾$R$为全窗口真实最高浓度$\max_{\mathbf{x}} c(\mathbf{x})$与航行器实时报告位置真实浓度$c\big(\hat{\mathbf{x}}(t)\big)$之差在24小时内的时间均值：
\begin{equation}
  R = \frac{1}{T}\int_0^T \left[\max_{\mathbf{x}} c(\mathbf{x}) - c\big(\hat{\mathbf{x}}(t)\big)\right] dt
  \label{eq:regret}
\end{equation}
时间平均遗憾$R$越低表示巡测表现越好，越早抵达真正的高浓度核心区并维持足够的续航时间，积分遗憾就越小。在对数叶绿素尺度下，$R=0.1$对应航行器报告位置的叶绿素浓度比窗口真实最高值低约20\%，而$R=0.3$则意味着报告浓度仅约为真实峰值的二分之一。

\subsection{问题剖析：计算与观测共享有限预算的三重矛盾}

上述巡测模型的本质困难在于内部航线计算与外部机动采样共享同一块$1\text{ kWh}$电池和同一个$24\text{ h}$窗口，而以下三重结构性矛盾直接决定了第4节方法的设计选择。第一，增加计算的真实收益只能在航行器内部的想象海洋中估算，但规划器在搜索样本上的自评得分存在系统性正向偏差。当高功耗芯片将单周期推演次数扩大50倍时，优化器能够精细调整折线航路点以穿过搜索样本集中的偶然高值网格，使内部得分持续攀升但实际航线早已不再改善\cite{smith2006curse, vanhasselt2010double}，这就要求必须将用于搜索航线的想象海洋与用于评判价值的想象海洋彻底分离。

第二，现场观测的信息收益取决于3天前旧卫星图究竟错在何处、错到何种程度，而海洋遥感大数据虽能精确标定这一误差的统计分布，却无法靠数值外推直接消除小尺度误差。由于云区插补平滑与水体亚中尺度演变，确定性或深度学习时空预测均无法从日均旧图中恢复数日后的小尺度峰值位置\cite{assran2025vjepa2}，航行器必须亲赴现场采样，并利用历史卫星大数据标定的误差方差与空间相关尺度构建先验想象海洋，再随每个现场样本通过集合数据同化动态收缩未访水域的不确定性。

第三，最优的时间分配策略随底图不确定性、机载处理器速度及高功耗芯片功耗的组合而发生相变，但单次赤潮任务的天然环境噪声过大，无法靠少量历史任务在线或离线拟合出普适规则。在算力捉襟见肘的慢计算机上，仅靠后台规划会导致航行器在窗口中部盲目绕圈，而在算力充裕的快计算机上，全程开启高功耗芯片只会白白透支推进电池并缩短总航程。由于任务间遗憾标准差远大于策略间平均差异，唯有在下水前针对当前机载硬件参数与数据标定的留出海洋开展全任务周期的完整预演，才能在不依赖任何历史巡测任务的条件下稳健剔除劣质策略。

===== FILE: sections/method.tex =====
\section{方法}

本文方法利用八年卫星数据标定的留出想象海洋作为独立标尺，将航线搜索与价值评判解耦，从而在出发前预演或在线元推理中无偏权衡计算与观测（图\ref{fig:overview}）。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_overview}
  \caption{基于数据标定留出想象海洋的自主水下航行器计算与观测权衡方法总览。（A）海洋大数据：利用2018至2026年东海3197天逐日$2\text{ km}$卫星叶绿素与海表温度数据切出422个赤潮窗口（开发集274个、测试集148个），标定1至3天滞后底图误差（0.125、0.176、0.210）与四季演变图谱，而550万参数的深度时空预测模型并不优于直接沿用最新底图，表明小尺度结构必须靠现场观测获取。（B）出发前：围绕3天前旧图生成48个经数据标定不确定性的想象海洋，划分为32个搜索用海洋与16个留出海洋；下水前以4个留出海洋为假想真值完整预演五种用时策略（柱状图为2025年4月4日测试任务在中等计算机上的假想遗憾，“一直走”以0.715入选），选出平均假想遗憾最低的策略$s^*$投入实海。（C）任务执行：每20分钟在走、深想与停下之间行动并随时响应最浓处查询，插图显示随规划预算增加规划器自评得分持续攀升，而留出海洋评判与真实航线价值一同趋于平缓。}
  \label{fig:overview}
\end{figure}

\subsection{数据标定的想象海洋与局地化集合同化}

航行器唯有使内部环境集合的先验离散度如实匹配旧卫星图与真实海洋之间的实际误差分布，才能在航行途中正确权衡先验底图指引与现场荧光计观测。常规做法通常将旧卫星图直接当作确定性背景场，或凭经验人为指定一个固定的先验方差，这不仅忽略了卫星图滞后天数与遥感小尺度平滑带来的真实误差幅值，还会导致数据同化过度轻信旧图或过度迎合单点测量噪声。为此，本文直接从2018至2022年开发集卫星序列中提取滞后$k$天底图的实测误差标准差$s_k$与空间相关长度$\ell$，结合同日卫星图相对于现场水体的未分辨小尺度标准差$s_{\text{sat}}$，构造合成先验标准差：
\begin{equation}
  \sigma_k = \sqrt{s_k^2 + s_{\text{sat}}^2}
  \label{eq:sigma_k}
\end{equation}
在$k=3$天的主设置下，由开发集标定的滞后误差为$s_3 = 0.210$，叠加小尺度偏差$s_{\text{sat}} = 0.15$后得到$\sigma_3 \approx 0.26$，而在“当天卫星图”真值模型下$s_{\text{sat}} = 0$，对应$\sigma_3 = 0.210$。航行器在下水前围绕3天前旧卫星图$c_{\text{map}}(\mathbf{x})$生成$N=48$个想象海洋：
\begin{equation}
  c^{(i)}(\mathbf{x}) = c_{\text{map}}(\mathbf{x}) + \sigma_k\, z^{(i)}(\mathbf{x}), \quad i = 1, 2, \dots, 48
  \label{eq:prior_ensemble}
\end{equation}
其中$z^{(i)}(\mathbf{x})$为相互独立的零均值单位方差高斯随机场，具有与实测滞后误差一致的平方指数空间相关函数$C(\mathbf{x}, \mathbf{x}') = \exp\!\big(-\|\mathbf{x}-\mathbf{x}'\|_2^2 / (2\ell^2)\big)$，相关长度取开发集标定值$\ell = 5$个网格（$10\text{ km}$）。

在24小时巡测过程中，每当机载荧光计在位置$\mathbf{x}_{\text{obs}}$采集到一个观测样本$y$，航行器立即对全部48个想象海洋执行同化更新，将单点观测信息传播至周围相关水域。若采用标准卡尔曼滤波或无局地化的集合滤波，48个样本的有限集合会在相距数十千米的网格间产生虚假样本相关，导致一次局部采样错误篡改远方未访水域的叶绿素估计。因此，本文采用序列集合调整卡尔曼滤波\cite{anderson2001eakf}，并在状态协方差更新中乘以半宽为$2\ell = 10$个网格（$20\text{ km}$）的五阶分段有理局地化相关函数$\rho\!\big(\|\mathbf{x}-\mathbf{x}_{\text{obs}}\|_2 / (2\ell)\big)$\cite{gaspari1999correlation}。记同化前在观测点处的集合均值为$\bar{c}(\mathbf{x}_{\text{obs}}) = \frac{1}{48}\sum_{i=1}^{48} c^{(i)}(\mathbf{x}_{\text{obs}})$，集合方差为$\sigma_{\text{ens}}^2(\mathbf{x}_{\text{obs}})$，传感器测量方差为$\sigma_{\varepsilon}^2 = 0.1^2$，则观测点处的后验集合均值$\bar{c}^a(\mathbf{x}_{\text{obs}})$与后验成员$c^{a,(i)}(\mathbf{x}_{\text{obs}})$按线性收缩关系更新：
\begin{equation}
  \bar{c}^a(\mathbf{x}_{\text{obs}}) = \frac{\sigma_{\varepsilon}^2\,\bar{c}(\mathbf{x}_{\text{obs}}) + \sigma_{\text{ens}}^2(\mathbf{x}_{\text{obs}})\,y}{\sigma_{\varepsilon}^2 + \sigma_{\text{ens}}^2(\mathbf{x}_{\text{obs}})}, \quad
  c^{a,(i)}(\mathbf{x}_{\text{obs}}) = \bar{c}^a(\mathbf{x}_{\text{obs}}) + \sqrt{\frac{\sigma_{\varepsilon}^2}{\sigma_{\varepsilon}^2 + \sigma_{\text{ens}}^2(\mathbf{x}_{\text{obs}})}}\,\Big(c^{(i)}(\mathbf{x}_{\text{obs}}) - \bar{c}(\mathbf{x}_{\text{obs}})\Big)
  \label{eq:eakf_obs}
\end{equation}
记第$i$个想象海洋在观测点处的增量为$\Delta y^{(i)} = c^{a,(i)}(\mathbf{x}_{\text{obs}}) - c^{(i)}(\mathbf{x}_{\text{obs}})$，则窗口内任意可航行网格$\mathbf{x}$处的叶绿素估计同步更新为：
\begin{equation}
  c^{a,(i)}(\mathbf{x}) = c^{(i)}(\mathbf{x}) + \rho\!\left(\frac{\|\mathbf{x}-\mathbf{x}_{\text{obs}}\|_2}{2\ell}\right)\frac{\operatorname{Cov}\!\big(c(\mathbf{x}), c(\mathbf{x}_{\text{obs}})\big)}{\sigma_{\text{ens}}^2(\mathbf{x}_{\text{obs}})}\,\Delta y^{(i)}
  \label{eq:eakf_state}
\end{equation}
通过式\eqref{eq:eakf_obs}与式\eqref{eq:eakf_state}的递推更新，已造访航迹周围$20\text{ km}$内的想象海洋迅速向实测浓度靠拢且集合离散度显著收缩，而远离航迹的水域则保持先验不确定性以待后续探索。

\subsection{航线搜索与价值评判的集合分离}

为消除航线优化过程对有限想象海洋的过拟合偏差，必须将供规划器搜索航线的样本集合与用于评判航线及计算价值的样本集合严格分离开来。现有基于集合的规划与元推理方法通常将全部48个想象海洋一并输入规划器，既用全体样本的平均得分挑选最优航线，又直接将该内部最高得分作为航线的真实预期收益\cite{russell1991right, lin2015metareasoning}。这种做法忽视了有限样本下的优化器诅咒\cite{smith2006curse}：当高功耗芯片将推演预算提升数十倍时，规划器有充足的机会微调航路点坐标，使折线恰好擦过这批特定样本中偶然重叠的随机高值斑块，从而制造出得分随算力持续上涨的假象，实则并未提升在真实海洋中的寻优表现。

为此，本文借鉴双估计思想\cite{vanhasselt2010double}，在任务开始前将48个想象海洋固定划分为两个互不相交的子集（图\ref{fig:overview}B）：前32个成员组成搜索用海洋$\mathcal{I}_{\text{search}} = \{1, 2, \dots, 32\}$，后16个成员组成留出海洋$\mathcal{I}_{\text{hold}} = \{33, 34, \dots, 48\}$。在巡测过程中，两个子集完全平等地接受式\eqref{eq:eakf_obs}与式\eqref{eq:eakf_state}的现场观测同化更新，因此它们蕴含相同的先验统计与实测信息，但交叉熵航线规划器在搜索过程中仅被允许访问32个搜索用海洋$\mathcal{I}_{\text{search}}$，而16个留出海洋$\mathcal{I}_{\text{hold}}$对搜索优化器完全不可见。

在每个20分钟周期内，规划器搜索一条以当前周期结束时刻航行器预计位置$\mathbf{x}_0$为起点、依次连接两个中间航路点$\bm{\theta} = (\mathbf{w}_1, \mathbf{w}_2)$的折线航线。将一条候选航线$\bm{\theta}$在单个想象海洋$c^{(i)}$上模拟走完剩余任务时长$T_{\text{left}}$或直至剩余可用巡航电池时间$T_{\text{batt}}$耗尽的过程称为一次推演。记模拟航行至剩余窗口时刻$\tau \in [0, T_{\text{left}}]$时，航行器沿折线已遇最高浓度与当前已访最高估计浓度$\max_{\mathbf{x}\in\mathcal{V}(t)} \bar{c}_t(\mathbf{x})$中的较大值为$m_i(\tau; \bm{\theta})$（当$\tau > T_{\text{batt}}$即电量耗尽后，$m_i(\tau; \bm{\theta})$保持耗尽时刻的值不变），则该航线在第$i$个想象海洋上的推演价值定义为：
\begin{equation}
  V_i(\bm{\theta}) = \frac{1}{T_{\text{left}}}\int_0^{T_{\text{left}}} m_i(\tau; \bm{\theta})\, d\tau
  \label{eq:route_value}
\end{equation}
式\eqref{eq:route_value}与式\eqref{eq:regret}的时间平均遗憾目标严格对应，能够同时惩罚路线绕远造成的到达延迟与电量透支造成的提前停机。规划器采用跨周期热启动的交叉熵方法\cite{deboer2005cem}在搜索用海洋$\mathcal{I}_{\text{search}}$上迭代优化航路点分布，选出搜索集平均价值最高的航线$\bm{\theta}^*$，而该航线的无偏价值评判$\hat{V}_{\text{hold}}(\bm{\theta}^*)$则由未参与搜索的16个留出海洋给出：
\begin{equation}
  \bm{\theta}^* = \arg\max_{\bm{\theta}} \frac{1}{|\mathcal{I}_{\text{search}}|}\sum_{i\in\mathcal{I}_{\text{search}}} V_i(\bm{\theta}), \quad
  \hat{V}_{\text{hold}}(\bm{\theta}^*) = \frac{1}{|\mathcal{I}_{\text{hold}}|}\sum_{j\in\mathcal{I}_{\text{hold}}} V_j(\bm{\theta}^*)
  \label{eq:split_eval}
\end{equation}
由于$\bm{\theta}^*$的选取过程从未利用$\mathcal{I}_{\text{hold}}$中的样本涨落，只要先验不确定性$\sigma_k$经历史卫星数据如实标定，$\hat{V}_{\text{hold}}(\bm{\theta}^*)$便不会随推演次数增加而产生乐观偏移。

\subsection{基于留出海洋的出发前全任务预演}

由于开启高功耗芯片导致的电量消耗以及停下复测造成的航程损失会在24小时全程内累积放大，时间分配策略的优劣必须在完整任务尺度上根据最终取得的遗憾结果来评判。常规方法要么依靠该型航行器在过往大量任务中的表现事先调好一条固定策略，要么在航行途中仅凭单步边际收益作短视切换，前者在缺乏历史任务记录时无法实施，后者则难以把握当前耗电对任务后期续航的非线性制约。为此，本文提出在下水前利用母船或岸基计算机，以留出海洋作为假想真值开展全任务出发前预演。

本文构造了五种覆盖不同计算与采样配比的候选时间分配策略（使用统一命名）：
\begin{enumerate}
  \item \textbf{一直走：}全程72个周期均开启推进器巡航采样，且仅使用低功耗处理器开展后台航线规划，不开启高功耗芯片，此时$1\text{ kWh}$电池可支撑约22.2小时连续航行。
  \item \textbf{一直深想：}全程开启推进器巡航采样，同时每个周期均开启高功耗芯片将推演次数提升至50倍，在$+20\text{ W}$芯片功耗下总功率升至$65\text{ W}$，电池续航缩短至约15.4小时（在$+5\text{ W}$省电加速器下续航约20.0小时）。
  \item \textbf{三段深想一段：}全程开启推进器巡航采样，每连续3个周期中开启1个周期高功耗芯片深想、其余2个周期仅用后台规划，兼顾周期性全局重规划与约19.4小时的巡航续航。
  \item \textbf{三段停下深想一段：}每连续3个周期中有1个周期关停推进器原位漂流复测5次并开启高功耗芯片深想，其余2个周期巡航采样并使用后台规划，试图以推进电能换取高算力与局部低噪观测。
  \item \textbf{三段停下复测一段：}每连续3个周期中有1个周期关停推进器原位漂流复测5次且仅用后台规划，其余2个周期巡航采样并使用后台规划，专门检验不增加算力时原位降噪的净效应。
\end{enumerate}

\begin{algorithm}[htbp]
  \caption{基于数据标定留出想象海洋的出发前全任务预演}
  \label{alg:rehearsal}
  \begin{algorithmic}[1]
    \Require 滞后$k$天旧卫星图$c_{\text{map}}(\mathbf{x})$，数据标定先验标准差$\sigma_k$与相关长度$\ell$，入水起点$\mathbf{x}_{\text{start}}$，机载低功耗处理器速度$v_{\text{cpu}}$、高功耗芯片倍率$50\times$与功率$P_{\text{gpu}}$，电池容量$E_{\text{batt}}=1\text{ kWh}$，候选策略集合$\mathcal{S}=\{\text{一直走}, \text{一直深想}, \text{三段深想一段}, \text{三段停下深想一段}, \text{三段停下复测一段}\}$
    \Ensure 选定的本次任务执行策略$s^*$
    \State 围绕$c_{\text{map}}(\mathbf{x})$按式\eqref{eq:prior_ensemble}生成48个想象海洋，划分为搜索用海洋$\mathcal{I}_{\text{search}}=\{1,\dots,32\}$与留出海洋$\mathcal{I}_{\text{hold}}=\{33,\dots,48\}$
    \State 从留出海洋$\mathcal{I}_{\text{hold}}$中抽取$M=4$个样本$\{c_{\text{truth}}^{(j)}\}_{j=1}^4$作为假想真值，并固定观测噪声随机数种子
    \For{每种候选策略 $s \in \mathcal{S}$}
      \For{$j = 1, 2, \dots, M$}
        \State 初始化航行器内部48个想象海洋、位置$\mathbf{x} \leftarrow \mathbf{x}_{\text{start}}$、剩余电量$E \leftarrow E_{\text{batt}}$及已访集合$\mathcal{V} \leftarrow \{\mathbf{x}_{\text{start}}\}$
        \For{决策周期 $t_{\text{step}} = 1, 2, \dots, 72$（每周期$\Delta t = 20\text{ min}$）}
          \State 若$E > 0$，按策略$s$确定本周期机体动作（走或停下）与规划模式（后台规划或开启高功耗芯片深想）
          \State 在搜索用海洋$\mathcal{I}_{\text{search}}$上按对应推演预算（$v_{\text{cpu}}\Delta t$或$50 v_{\text{cpu}}\Delta t$）运行交叉熵方法更新航线$\bm{\theta}^*$
          \State 在假想真值$c_{\text{truth}}^{(j)}$上执行机体动作并按式\eqref{eq:obs}采集荧光计样本，用式\eqref{eq:eakf_obs}与式\eqref{eq:eakf_state}更新内部海洋集合并扣除本周期耗电量
          \State 按式\eqref{eq:answer}记录已访集合$\mathcal{V}$中当前内部均值最高的位置$\hat{\mathbf{x}}(t_{\text{step}})$
        \EndFor
        \State 在假想真值$c_{\text{truth}}^{(j)}$上按式\eqref{eq:regret}计算24小时假想时间平均遗憾$R_{s,j}$
      \EndFor
      \State 计算策略$s$在4个假想真值上的平均假想遗憾$\bar{R}_s = \frac{1}{4}\sum_{j=1}^4 R_{s,j}$
    \EndFor
    \State \Return $s^* = \arg\min_{s\in\mathcal{S}} \bar{R}_s$
  \end{algorithmic}
\end{algorithm}

出发前预演的完整流程如算法\ref{alg:rehearsal}所示。当航行器在母船甲板或岸基实验室准备就绪并装入旧卫星图与入水起点后，母船或岸基计算机从16个留出海洋$\mathcal{I}_{\text{hold}}$中取出$M=4$个样本作为假想的“真实海洋”。对于每一个假想真值$c_{\text{truth}}^{(j)}$（$j=1,2,3,4$）和五种候选策略中的每一种策略$s$，预演程序严格按照该台航行器自身的交叉熵规划器、低功耗处理器推演速度、高功耗芯片功耗以及$1\text{ kWh}$电池模型，完整模拟一遍24小时（72个周期）的巡测全过程，并按式\eqref{eq:regret}记录策略$s$在假想真值$c_{\text{truth}}^{(j)}$上取得的真实时间平均遗憾$R_{s,j}$。为降低方差，五种策略在同一个假想真值上共享完全相同的初始想象海洋与荧光计观测噪声序列，最终选出4个假想真值上平均遗憾最低的策略$s^*$写入航行器下水执行：
\begin{equation}
  s^* = \arg\min_{s\in\mathcal{S}} \frac{1}{4}\sum_{j=1}^4 R_{s,j}
  \label{eq:rehearsal_select}
\end{equation}
值得强调的是，预演在比较五种策略时依据的是各策略在假想真值$c_{\text{truth}}^{(j)}$上实际达到的巡测遗憾$R_{s,j}$，而非规划器内部的自评得分，因此从根本上绕开了规划器的自评泡沫。在计算开销方面，以慢计算机配置为例，单次任务预演（4个假想真值$\times 5$种策略）共需执行约190万次航线推演，若由航行器机载高功耗芯片自算需耗时约125小时，因此预演必须也完全可以在下水前由母船或岸基计算机完成：在普通台式计算机单核上，慢计算机、中等计算机与快计算机配置完成单次任务预演的实测耗时分别仅为$4.6\text{ s}$、$7.8\text{ s}$与约$25\text{ s}$，完全满足应急出航前的快速装订需求。

\subsection{在线单步元推理中的留出估值}

当任务要求航行器不依赖出发前预演而在航行途中逐周期在线决定计算与采样动作时，将第4.2节的留出评判准则引入单步元推理即可消除经典方法的过度规划。经典单步元推理\cite{russell1991right}在每个20分钟周期先运行后台低功耗规划获得基准航线$\bm{\theta}_{\text{base}}$，再根据搜索用海洋$\mathcal{I}_{\text{search}}$上交叉熵迭代的得分爬升曲线外推开启高功耗芯片深想后的预期航线得分增量，并通过在$\mathcal{I}_{\text{search}}$上模拟原位采样5次的预后验均值变化来估计停下复测的信息价值。由于这两个价值估计均建立在已被规划器反复迎合的搜索用海洋$\mathcal{I}_{\text{search}}$之上，优化器诅咒会使控制器持续看到虚高的计算收益与复测收益，进而几乎每步都开启高功耗芯片并频繁停船。

本文提出的“单步元推理（留出估值）”保持单步元推理的全部决策逻辑与代价项不变，仅将价值评估的数据源从32个搜索用海洋$\mathcal{I}_{\text{search}}$替换为16个留出海洋$\mathcal{I}_{\text{hold}}$。具体而言，记后台规划选出的航线为$\bm{\theta}_{\text{base}}$，若开启高功耗芯片深想选出的航线为$\bm{\theta}_{\text{deep}}$，两者均在$\mathcal{I}_{\text{search}}$上由交叉熵方法搜索产生，但开启高功耗芯片的计算净收益改由留出海洋上的平均价值差$\hat{V}_{\text{hold}}(\bm{\theta}_{\text{deep}}) - \hat{V}_{\text{hold}}(\bm{\theta}_{\text{base}})$减去高功耗芯片额外耗电缩短续航造成的边际损失来度量，原位复测5次的预后验信息收益同样在16个留出海洋$\mathcal{I}_{\text{hold}}$上计算。这一改动以极小的代码与计算代价实现了在线元推理中动作搜索与价值评判的彻底分离。

===== FILE: sections/experiments.tex =====
\section{实验}

本节通过系统数值实验依次回答六个核心问题：第一，八年东海卫星遥感大数据能为航行器提供何种先验信息，深度学习时空外推能否替代现场采样（第5.2节）；第二，规划器在搜索用海洋上的自评得分随推演预算增加会产生多大的乐观偏差，留出海洋能否给出无偏评判（第5.3节）；第三，在四种机载硬件与两种真值模型下，出发前预演与需要历史任务的方法、在线元推理及启发式巡测规则相比表现如何（第5.4节）；第四，经典单步元推理为何失效，留出估值与出发前预演通过何种机制实现硬件自适应（第5.5节）；第五，预演中的假想真值数量、不确定性标定与评估尺度各起多大作用（第5.6节）；第六，在算力速度、底图偏离度与底图新鲜度构成的二维参数空间中，深想与停下复测的适用边界何在（第5.7节）。

\subsection{实验设置与对比方法}

全部实验均基于2018至2026年东海3197天卫星叶绿素与海表温度数据集构建的422个赤潮任务窗口开展，其中2018至2022年的274个开发集窗口用于统计底图误差、绘制算力相图及训练历史基线，2023至2026年的148个测试集窗口用于主实验与消融检验（表\ref{tab:settings}）。实验涵盖四种机载硬件配置：慢计算机（低功耗处理器每分钟推演5次，高功耗芯片$+20\text{ W}$）、中等计算机（20次/分，$+20\text{ W}$）、快计算机（100次/分，$+20\text{ W}$）以及省电加速器（20次/分，$+5\text{ W}$），并在“当天卫星图 + 小尺度变化”（主设置，$s_{\text{sat}}=0.15$）与“当天卫星图”（全实测数据设置，$s_{\text{sat}}=0$）两种真值模型下开展评估。为保证严格配对比较，同一任务窗口上的所有控制方式均共享完全相同的真实海洋、入水起点与荧光计随机噪声序列，且每次任务的随机数种子固定；控制器间时间平均遗憾配对差值的95\%置信区间通过按赤潮周整组重抽样的自助法计算（同一周内的任务窗口一并重抽样以计入周内空间相关性）。

\begin{table}[htbp]
  \centering
  \caption{东海赤潮应急巡测实验的核心参数与评价设置。}
  \label{tab:settings}
  \input{tables/settings.tex}
\end{table}

实验将“出发前预演（本文）”与五类控制方式进行全面对比。第一类为五种固定时间分配策略，即“一直走”、“一直深想”、“三段深想一段”、“三段停下深想一段”和“三段停下复测一段”，以及不经预演的“五种策略随机选”和“三种不停策略随机选”。第二类为需要该型航行器历史巡测任务的方法，包括“调好的固定策略”（在2018至2022年120个开发集任务上为每种硬件和真值模型选出平均遗憾最低的固定策略，再直接用于测试集，属于强基线）和“按历史任务学习的选择器”（参照学习型元推理思想\cite{magnino2026metareasoning}，在同样120个开发集任务上训练梯度提升回归模型，利用出发前已知的8项旧图特征——最大值、中位数、极差、标准差、起点至旧图峰值距离、可航行网格占比、起点处旧图浓度及接近峰值网格占比——预测五种策略的遗憾并为每次任务挑选预测遗憾最低者）。第三类为在线元推理，包括经典“单步元推理”\cite{russell1991right}与本文改进的“单步元推理（留出估值）”。第四类为不开展多步航线规划的经典海洋巡测规则（航行器全程保持巡航采样并以相同局地化集合滤波更新地图），包括“割草机式全覆盖”（从入水边缘起按间距$16\text{ km}$平行往返扫测）\cite{galceran2013coverage}、“贪心：驶向估计最浓处”（每个周期驶向集合均值最高的未访网格）、“上置信界采样”（驶向集合均值加2倍标准差最高的未访网格）\cite{srinivas2012gpucb}以及“汤普森采样”（每个周期随机抽取一个想象海洋并驶向其最浓未访网格）\cite{russo2018thompson}。第五类为仅作性能下界参考的“每次任务事后最优（参考）”，即在每次测试任务结束后事后挑出五种固定策略中实际遗憾最低者。

\subsection{海洋大数据对底图不确定性的标定作用与预测边界}

八年卫星叶绿素大数据能够精确标定滞后底图在不同季节与滞后天数下的误差分布，但即便是包含550万参数的深度时空预测模型也无法改善1至3天的底图外推精度，小尺度藻华结构必须依靠现场采样获取（图\ref{fig:data}）。在全部3197天数据上统计相隔3天的对数叶绿素变化标准差可见，东海表层叶绿素的3天演变幅度呈现出清晰的季节与空间分异：全海域中位数在赤潮高发的春季最高（0.127），夏季（0.107）与秋季（0.103）次之，冬季降至0.081，而在夏季浙闽沿岸与长江冲淡水锋面一带形成了3天变化标准差高达0.25至0.3的强变率条带（图\ref{fig:data}a至图\ref{fig:data}d）。在274个春季开发集窗口内，任务当天卫星图减去1、2、3天前旧图的误差标准差随滞后天数单调递增，依次为$0.125$、$0.176$与$0.210$（均值偏差依次为$+0.016$、$+0.032$与$+0.045$，空间相关尺度约为5个网格即$10\text{ km}$），且同日卫星图与现场海水之间还存在约0.15的对数浓度差异\cite{ye2021cocts}（图\ref{fig:data}e）。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_data}
  \caption{八年东海卫星叶绿素大数据提供的先验误差标定及其外推预测边界。（a）至（d）2018至2026年全部3197天对数叶绿素3天变化标准差的四季空间分布（中位数春季0.127、夏季0.107、秋季0.103、冬季0.081），春季子图标出了274个开发集窗口与148个测试集窗口的位置。（e）开发集窗口内滞后1、2、3天旧卫星图的误差标准差（0.125、0.176、0.210）及同日卫星图相对于现场实测水体的约0.15偏差。（f）2023至2026年测试集上深度时空预测模型与直接沿用最新卫星图在提前1、2、3天预报上的均方根误差对比（0.1229对0.1226、0.1439对0.1439、0.1487对0.1474）。数据能够可靠标定旧图的不确定性幅值，但无法替代现场观测。}
  \label{fig:data}
\end{figure}

为检验能否在航行器出发前用深度学习模型将3天前旧图向前推演以缩减滞后误差，本文训练了一个550万参数的联合嵌入预测架构模型\cite{assran2025vjepa2}，以过去3天的叶绿素和海表温度异常场为输入，使用2018至2021年3月至6月数据训练并在2022年上验证（验证集误差仅比沿用最新底图低1.4\%）。然而在2023至2026年测试年份上，该模型提前1、2、3天预报的均方根误差分别为$0.1229$、$0.1439$与$0.1487$（集合离散度与误差之比为$0.70\text{--}0.93$），与直接沿用最新可用卫星图的持久性基线（$0.1226$、$0.1439$与$0.1474$）完全持平（图\ref{fig:data}f）。这一结果从物理与数据层面确立了海洋大数据在本问题中的真正角色：由于云区插补产品平滑了日内潮汐混合与亚中尺度梯度，数值外推无法凭空恢复小尺度峰值，但多年遥感统计能够为生成想象海洋提供准确的先验不确定性标尺。

\subsection{规划器自评得分的乐观偏差与留出海洋的无偏评判}

随着单次决策推演预算的增加，规划器在搜索用海洋上的自评得分因优化器诅咒而持续虚高，而在未参与搜索的留出海洋上评判则能消除这一偏差并准确反映航线真实价值的饱和过程（图\ref{fig:curse}）。在80个开发集窗口（每窗口3个随机种子，携带3天前卫星图，评估任务前8小时，主真值模型）上，当每次决策的推演次数从64次增至2000次再扩展至200,000次（跨度达三个半数量级）时，所选航线在真实海洋中的实际价值从$0.749$升至$0.793$，随后进入平台期并平缓收敛至$0.803$（图\ref{fig:curse}a黑线）。相反，交叉熵规划器在32个搜索用海洋上的内部自评得分却从$0.762$升至$0.833$并一路攀升至$0.917$（图\ref{fig:curse}a红线），在最大预算下比真实航线价值高估达$0.114$。当把同一批搜索选出的航线放到16个留出海洋上评估时，留出评判均值依次为$0.745$、$0.794$与$0.802$（图\ref{fig:curse}a蓝虚线），在全部推演预算下与真实价值之差均不超过$0.005$（图\ref{fig:curse}b）。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_curse}
  \caption{推演预算从64次扩展至200,000次时规划器自评得分的乐观偏差与留出海洋的无偏评判（80个开发集窗口$\times 3$个种子，3天前卫星图，任务前8小时）。（a）所选航线的时间平均最佳对数叶绿素价值：搜索用海洋上的自评得分从0.762持续升至0.917，而真实航线价值（0.749升至0.803）与留出海洋评判（0.745升至0.802）在约2000次推演后一同趋于饱和。（b）估计价值减去真实价值的偏差曲线：使用数据标定不确定性时留出评判偏差保持在0.005以内，将不确定性设小一半或放大至1.5倍虽产生$-0.06$与$+0.07$的整体平移，但仍能准确捕捉增加算力的相对增益。}
  \label{fig:curse}
\end{figure}

进一步改变先验标准差幅值的实验表明，即使不确定性标定存在一定偏差，留出海洋对增加算力所获边际收益的判断依然稳健（图\ref{fig:curse}b）。当人为将先验标准差$\sigma_3$减半或放大至1.5倍时，留出评判绝对值虽分别产生约$-0.06$与$+0.07$的系统性平移，但推演预算从64次增至200,000次时留出海洋估计的价值增量（分别为$+0.059$与$+0.054$）依然与真实海洋中的实际价值增量（$+0.054$与$+0.047$）高度吻合。这证实将搜索用海洋与留出海洋分离能够彻底切断优化器对样本噪声的迎合链条，为衡量计算价值提供可靠的独立标尺。

\subsection{多硬件平台与双真值模型下的主实验对比}

在2023至2026年全部148个测试任务上，出发前预演在四种机载硬件与两种真值模型下均无需任何历史巡测任务即达到“调好的固定策略”与“按历史任务学习的选择器”的同等水平，并一致显著优于经典“单步元推理”和各类无规划巡测规则（图\ref{fig:main}，表\ref{tab:main}）。在“当天卫星图 + 小尺度变化”主设置下，慢计算机、中等计算机、快计算机与省电加速器上“出发前预演（本文）”的时间平均遗憾分别为$0.276$、$0.265$、$0.268$与$0.266$。与各硬件在120个历史开发任务上专门选出的“调好的固定策略”（依次为“三段深想一段”$0.270$、“三段深想一段”$0.269$、“一直走”$0.267$与“一直深想”$0.267$）相比，出发前预演减去调好策略的配对差值依次为$+0.007$（95\%置信区间$[-0.000, +0.014]$）、$-0.003$（$[-0.009, +0.003]$）、$+0.002$（$[-0.005, +0.008]$）与$-0.001$（$[-0.006, +0.005]$），与“按历史任务学习的选择器”（遗憾依次为$0.278$、$0.269$、$0.273$与$0.266$）的配对差值依次为$-0.001$、$-0.004$、$-0.004$与$+0.000$，全部八组对比的95\%置信区间均包含0。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_main}
  \caption{148个测试任务上各对比控制方式减去“出发前预演（本文）”的时间平均遗憾配对差值及95\%置信区间（正值表示差于本文方法）。四列对应慢计算机、中等计算机、快计算机与省电加速器，实心圆点为“当天卫星图 + 小尺度变化”主设置，空心圆点为“当天卫星图”真值设置。出发前预演在所有硬件与两种真值模型下均匹配需要历史任务的两种方法，并显著优于经典单步元推理及所有巡测规则（仅慢计算机主设置下与贪心规则持平）。}
  \label{fig:main}
\end{figure}

\begin{table}[htbp]
  \centering
  \caption{2023至2026年148个测试任务上四种机载硬件与两种真值模型下各控制方式的时间平均遗憾（越低越好，每列最优可运行控制器加粗，本文方法行加底纹）。}
  \label{tab:main}
  \small\resizebox{\linewidth}{!}{\input{tables/main_table.tex}}
  \par\vspace{2pt}\footnotesize 注：$^a$ 调好的固定策略在主设置下依次为三段深想一段、三段深想一段、一直走、一直深想，在“当天卫星图”真值下依次为三段深想一段、一直走、三段深想一段、三段深想一段。
\end{table}

与在线元推理和启发式巡测规则相比，出发前预演与多步航线规划的优势在统计上高度显著。在主设置下，经典“单步元推理”在四种硬件上的遗憾高达$0.287$、$0.287$、$0.282$与$0.278$，出发前预演相对其降低遗憾$-0.011$（$[-0.019, -0.002]$）、$-0.022$（$[-0.030, -0.013]$）、$-0.013$（$[-0.020, -0.007]$）与$-0.012$（$[-0.019, -0.004]$），95\%置信区间全部严格位于0以下。四种不含多步路线规划的巡测规则因始终只做单步或固定航线机动，在四种硬件上表现相同：“贪心：驶向估计最浓处”遗憾为$0.285$，“上置信界采样”为$0.299$，“汤普森采样”为$0.332$，“割草机式全覆盖”高达$0.424$；出发前预演除在慢计算机上与贪心规则差值为$-0.009$（$[-0.022, +0.004]$）外，在其余三种硬件上比贪心规则低$-0.017$至$-0.020$，并在所有硬件上比上置信界采样、汤普森采样和割草机式全覆盖分别低$-0.023$至$-0.034$、$-0.056$至$-0.067$以及$-0.148$至$-0.159$（置信区间全部低于0）。

在直接以任务当日实测卫星图为真值的“当天卫星图”设置下，由于不存在卫星未分辨的亚网格随机场，所有控制器的绝对遗憾均整体下降，但各方法之间的优劣排序完全不变（表\ref{tab:main}右半部）。“出发前预演（本文）”在四种硬件上取得$0.197$、$0.191$、$0.195$与$0.191$，与“调好的固定策略”（$0.194$、$0.196$、$0.191$与$0.191$）之差为$-0.004$至$+0.003$，与“按历史任务学习的选择器”之差为$-0.005$至$+0.003$（置信区间均包含0），同时比“单步元推理”（$0.202$、$0.202$、$0.204$与$0.199$）低$-0.006$至$-0.010$，比四种巡测规则低$-0.010$至$-0.139$（置信区间全部低于0）。此外，两种真值模型下148个测试任务之间的遗憾标准差分别高达约$0.13$与$0.11\text{--}0.12$，而三种不停航策略之间的平均差距（除慢计算机外）不超过$0.01$，这直接解释了为何“按历史任务学习的选择器”虽利用了8项旧图特征和120个历史训练任务，却依然无法在测试集上超越单一的调好策略。同时，对慢计算机全部148个测试任务重新独立运行预演，所得每次任务的遗憾数值与首次运行完全一致，证实了实验结果的精确可重复性。

\subsection{作用机制分析：在线过度规划的成因与预演的硬件自适应}

经典单步元推理之所以表现不佳，是因为轻信搜索集自评得分使其在80\%至97\%的周期内盲目开启高功耗芯片并在约三分之一的周期内停下复测，而改用留出估值或采用出发前预演则能大幅压低无效计算与停船，并使所选策略随硬件算力和功耗自适应调整（图\ref{fig:mech}）。在主设置下，“单步元推理”在慢、中、快计算机与省电加速器上开启高功耗芯片的周期占比分别高达80\%、93\%、97\%与94%（图\ref{fig:mech}a），处于停下漂流状态的周期占比均达33\%至34\%（图\ref{fig:mech}b）。当保持单步元推理其余流程完全不变、仅将计算收益与复测收益改在16个留出海洋上评估后，“单步元推理（留出估值）”开启高功耗芯片的比例骤降至30\%、38\%、44\%与39\%，停下比例减半至15\%至18\%，其时间平均遗憾在四种硬件上依次降至$0.278$、$0.270$、$0.269$与$0.267$（比经典单步元推理分别降低$0.009$、$0.017$、$0.013$与$0.011$），与“出发前预演（本文）”的差距缩小至$0.001$至$0.005$以内（所有95\%置信区间均包含0）。这一对照实验直接证明，经典元推理的过度规划正是由搜索样本上的自评乐观偏差引起的，而剩余15\%至18\%的停下周期则是其略逊于预演（预演停下比例仅$0.5\%\text{--}1.8\%$）的唯一残余损失来源。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_mech}
  \caption{在线元推理过度规划的成因与出发前预演的硬件自适应机制（主真值设置，148个测试任务）。（a）高功耗芯片开启周期占比与（b）停下复测周期占比：经典单步元推理在80\%至97\%的周期内开启高功耗芯片并在33\%至34\%的周期内停下，而单步元推理（留出估值）与出发前预演大幅削减了无效深想与停船。（c）出发前预演在四种硬件上选出各候选策略的任务占比：随基础算力提升，“一直走”占比从1\%升至30\%再升至47\%，而在省电加速器上“一直深想”占比从25\%升至43\%。}
  \label{fig:mech}
\end{figure}

从出发前预演在148个测试任务上选出的策略分布（图\ref{fig:mech}c）可以清晰看出其适配不同硬件的物理机制。在后台算力极慢（5次/分）、“一直走”遗憾高达$0.374$（比调好策略差$+0.104$）的慢计算机上，预演选出“三段深想一段”占55\%、“一直深想”占39\%，“一直走”仅占1\%，停下类策略仅占4\%。随着低功耗处理器速度提升至中等计算机（20次/分）和快计算机（100次/分），后台规划已接近航线价值饱和区，预演选出“一直走”的比例随之从1\%跃升至30\%（“三段深想一段”43\%、“一直深想”25\%、停下类1\%）并进一步升至快计算机上的47\%（“三段深想一段”28\%、“一直深想”22\%、停下类3\%）。而在算力与中等计算机相同（20次/分）、但高功耗芯片功耗从$+20\text{ W}$降至$+5\text{ W}$的省电加速器上，由于开启深想对续航的惩罚大幅减轻，预演选出“一直深想”的比例从中等计算机的25\%上升至43\%（“三段深想一段”35\%、“一直走”20\%、停下类1\%）。由此可见，预演的核心收益在于准确识别并剔除当前硬件下的劣质选项（所有硬件上的两种停下策略以及慢计算机上的“一直走”），从而显著优于“五种策略随机选”（遗憾$0.331$、$0.293$、$0.292$与$0.292$）和慢计算机上的“三种不停策略随机选”（$0.306$）。而在真实平均差距不超过$0.004$的其余三种硬件的不停策略之间，预演的单任务区分能力接近随机抽取：“出发前预演（本文）”与“预演（以搜索过的海洋为真值）”在单个任务上选出同一策略的比例仅为37\%至41\%，且两者平均遗憾仅相差$-0.004$至$+0.004$（置信区间均包含0），这是因为预演依据假想真值上的最终任务遗憾而非规划器自评得分来比较策略，本身已对规划器自评泡沫免疫。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_example}
  \caption{一次典型测试任务（2023年4月15日，慢计算机）中“一直走”与“三段深想一段”的航迹及实时遗憾对比。（a）航行器出发时携带的3天前卫星图及东侧边缘入水起点（白色三角形）。（b）真实海洋叶绿素分布（西南角五角星为真实最浓处）以及“一直走”（蓝线）与“三段深想一段”（橙线，加粗段为开启高功耗芯片深想）的24小时航迹。（c）24小时内报告位置的实时遗憾曲线：“一直走”因搜索不足在窗口中部绕圈，遗憾停留在0.4附近（均值0.43），“三段深想一段”横穿窗口并在约19小时后抵达真实最浓处（均值降至0.31）。}
  \label{fig:example}
\end{figure}

一次具体测试任务（2023年4月15日，慢计算机，按日期顺序首个两种策略差距超过0.1的任务）直观展示了慢速处理器上开启高功耗芯片深想如何改变航行轨迹（图\ref{fig:example}）。该任务中航行器从窗口东侧边缘入水，3天前旧图显示西侧与西南侧浓度较高（图\ref{fig:example}a），而真实海洋的最浓核心区位于西南角（图\ref{fig:example}b五角星）。在慢计算机上，“一直走”每20分钟仅能完成100次后台推演，粗糙的航路点搜索使其航行至窗口中部次高值区后便陷入局部徘徊（图\ref{fig:example}b蓝线），24小时内报告误差始终停留在0.4左右，时间平均遗憾达$0.43$（图\ref{fig:example}c）。相比之下，“三段深想一段”每3个周期开启一次高功耗芯片完成5000次推演（图\ref{fig:example}b橙色加粗段），充裕的搜索预算使其及时识别出西南方向的远端高梯度潜力并果断横穿整个窗口，在约19小时后准确抵达西南角真实最浓处，将24小时时间平均遗憾压低至$0.31$。

\subsection{消融实验：假想真值数量、不确定性标定与评估尺度}

在慢计算机与中等计算机上开展的单因素消融实验表明，充足的假想真值数量、由卫星大数据标定的先验不确定性幅值以及全任务预演或留出估值机制，均是保障方法稳健性的必要环节（图\ref{fig:ablation}）。首先，当把预演使用的留出假想真值数量从默认的4个缩减为1个或2个时，慢计算机与中等计算机上的时间平均遗憾分别劣化$+0.013$（$[-0.000, +0.027]$）与$+0.010$（$[-0.001, +0.020]$），以及$+0.010$（$[-0.001, +0.022]$）与$+0.006$（$[-0.002, +0.013]$），说明单个假想真值的空间涨落较大，容易误选次优策略；而将假想真值增至8个时，慢计算机遗憾虽进一步微降$-0.007$（$[-0.012, -0.001]$），但中等计算机变化为$+0.003$（$[-0.004, +0.009]$）且计算耗时翻倍，因此4个假想真值是兼顾精度与岸基计算效率的合理选择。其次，将4个假想真值改为从32个搜索用海洋中抽取的“预演（以搜索过的海洋为真值）”，其遗憾与完整方法仅相差$-0.004$与$+0.003$（置信区间均包含0），再次印证只要以假想真值上的最终任务结果而非规划器自评得分作为评判标准，即可规避自评过拟合。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_ablation}
  \caption{慢计算机与中等计算机（主真值设置，148个测试任务）上的消融实验结果（各变体减去完整“出发前预演（本文）”的时间平均遗憾配对差值及95\%置信区间）。减少假想真值数量、将先验不确定性错误放大至2倍或取消预演改为随机选择均导致性能劣化，而在任务尺度预演、在线周期级留出估值与需要历史任务的方法之间表现相当。}
  \label{fig:ablation}
\end{figure}

先验不确定性的遥感数据标定对同化与预演质量具有决定性影响。当不依赖数据标定而人为将先验标准差$\sigma_3$减半时，慢、中计算机遗憾变化为$+0.002$与$+0.004$（置信区间包含0），但当将先验标准差放大至标定值的2倍时，慢计算机与中等计算机的遗憾分别显著恶化$+0.011$（$[+0.001, +0.020]$）与$+0.020$（$[+0.011, +0.030]$）。在2倍不确定性下，過大的先验噪声淹没了旧卫星图的大尺度梯度信息，不仅使所有固定策略本身的表现全面退化（中等计算机上三种不停策略的遗憾从$0.267\text{--}0.269$恶化至$0.275\text{--}0.283$），而且使预演选出的策略（$0.286$）落后于最佳固定策略（$0.275$）。最后，将全任务出发前预演替换为在线逐周期的“单步元推理（留出估值）”时，慢、中计算机差值仅为$+0.002$与$+0.005$（置信区间包含0），与需要历史任务的“调好的固定策略”（$-0.007$与$+0.003$）和“按历史任务学习的选择器”（$+0.001$与$+0.004$）同样处于统计等价区间，而完全取消预演改为“五种策略随机选”则会带来$+0.055$与$+0.028$的显著损失（“三种不停策略随机选”在慢计算机上亦损失$+0.029$）。

\subsection{适用边界：算力、底图偏离度与底图新鲜度的影响}

在低功耗处理器速度与真实海洋偏离卫星图程度构成的二维参数空间中，开启高功耗芯片深想仅在基础算力低于航线价值饱和阈值时产生显著收益且底图越不准收益越大，而中途停下原位复测在所有参数组合下均造成显著损失（图\ref{fig:phase}）。在由低功耗处理器推演速度（5、10、20、50、100、200次/分）与真实海洋偏离同日卫星图程度（$s_{\text{sat}}$取0、0.05、0.15、0.30，每格60个开发集任务）组成的网格相图上，比较较好的深想策略（“一直深想”与“三段深想一段”中较优者）与“一直走”可见（图\ref{fig:phase}a）：唯有在最慢的5次/分处理器上（后台每20分钟仅推演100次，远低于图\ref{fig:curse}a中约2000次推演的饱和点），开启高功耗芯片深想才稳定显著优于“一直走”，且当偏离程度从0.05增至0.15再增至0.30时，深想降低的时间平均遗憾从$-0.086$扩大至$-0.109$再扩大至$-0.138$，表明底图越不可信，越需要充足的算力结合现场同化重塑航线。在10次/分处理器上，仅偏离0.15一格存在微弱收益（$-0.017$，$[-0.035, -0.001]$），而从20次/分（每周期后台推演400次）起直至200次/分，所有偏离程度下深想均不再带来显著收益。当真实海洋偏离程度为0（即“当天卫星图”本身作为真值）时，相图第四行的结果与上述规律一致：\TBD{待补偏离度为0行的具体数值}。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_phase}
  \caption{低功耗处理器速度（每分钟5至200次推演）与真实海洋偏离卫星图程度（0、0.05、0.15、0.30）二维网格上的策略收益相图（每格60个开发集任务）。（a）最佳深想策略减去“一直走”的时间平均遗憾差值（加框格点表示95\%置信区间低于0，即深想显著有益）：深想仅在基础算力过慢（5次/分）时显著获益，且底图偏离越大收益越强。（b）较好停下策略减去最佳不停策略的遗憾差值：所有格点差值均为显著正值（$+0.063$至$+0.118$），表明停下原位复测在任何算力与底图误差下均得不偿失。}
  \label{fig:phase}
\end{figure}

相图右半部（图\ref{fig:phase}b）揭示了另一条普适规律：在全部算力速度与底图偏离度格点上，两种停下策略中较好者均比最佳不停策略高出$+0.063$至$+0.118$的时间平均遗憾，所有格点的95\%置信区间均严格大于0。这一现象可由不确定性空间尺度与时间积分目标共同解释：在原地停下漂流20分钟连续采样5次，虽能将该单点处的荧光计测量标准差从$0.1$压低至$0.1/\sqrt{5}\approx 0.045$，但制约航行器找到全窗最浓水体的瓶颈并非已访点的传感器噪声，而是广阔未访水域高达约$0.26$的先验不确定性，且将三分之一的作业时间用于原地漂流会严重推迟抵达核心浓水区的时刻，直接招致时间平均遗憾的沉重惩罚。此外，当航行器装入的是滞后仅1天的新鲜卫星图（$k=1$，$s_1=0.125$，主真值设置）时，在148个测试任务上各控制器绝对遗憾整体下降：在慢计算机上，“调好的固定策略”为“一直深想”（$0.250$），“出发前预演（本文）”取得$0.251$（与调好策略差值$+0.001$，$[-0.005, +0.011]$），依然优于“单步元推理”的$0.260$（差值$-0.009$，$[-0.018, +0.001]$），而在中等计算机上，\TBD{待补1天前卫星图在中等计算机上的具体数值}。

\subsection{局限性}

本研究在海洋环境表征、运动规划维度与预演执行机制上仍存在若干简化，界定了当前结论的适用范围。首先，实验中的真实海洋是由任务当天的真实卫星叶绿素图（叠加或不叠加按实测文献标定的小尺度随机场）构成的，并非现场走航实测剖面，且二维表层场与随表层水体漂移的参考系忽略了窗口内的水平流剪切以及东海原甲藻的昼夜垂直迁移行为，双航路点折线规划器也是对水下三维流场路径规划的简化替代。其次，出发前预演仅在下水前由母船或岸基计算机执行一次，未在24小时巡测中途根据同化更新后的地图重新切换策略，且4个假想真值的预演主要实现了针对机载硬件平台特性的策略适配，尚不足以在平均差距微小的几种不停策略之间针对单次任务做出优于随机的精细区分（主设置下距离“每次任务事后最优（参考）”仍有$0.022\text{--}0.027$的差距）。最后，预演内部的假想遗憾绝对值比真实海洋中的实际遗憾系统性偏高约$0.05\text{--}0.07$，但由于这一偏移对所有候选策略均等发生，并未改变各策略之间的相对优劣排序。

===== FILE: sections/conclusion.tex =====
\section{结论}

多年累积的卫星海洋遥感大数据对于自主水下航行器的意义，不仅在于提供一张指引大方向的先验底图，更在于能够生成一套经真实误差标定且独立于机载规划器搜索过程的留出想象海洋，使航行器拥有衡量自身计算价值的客观标尺而不被规划器的内部自评泡沫所误导。本文围绕东海赤潮应急巡测中走、深想与停下复测的时间与能量分配问题，将48个随现场采样局地化集合同化更新的想象海洋划分为32个搜索用海洋与16个留出海洋，分别提出了下水前在母船或岸基计算机上运行的出发前全任务预演方法以及航行途中逐周期运行的在线留出估值单步元推理方法。在2018至2026年东海3197天卫星数据构建的422个赤潮窗口、四种机载硬件及两种真值模型上的实验证实，留出海洋评判在横跨三个半数量级的推演预算下始终与真实航线价值保持在0.005以内，开启高功耗芯片深想仅在基础算力过慢时有益而停下复测始终得不偿失，且出发前预演与在线留出估值在无需任何历史巡测任务的条件下均取得了与依赖历史任务方法一致、并显著优于经典单步元推理和启发式巡测规则的表现。未来工作将把基于留出想象海洋的计算价值评判框架拓展至三维斜压海流预报集合与多台自主水下航行器协同赤潮追踪的海试研究中。

===== FILE: sections/appendix.tex =====
\section{代码与数据说明}

本研究的数据预处理、局地化集合调整卡尔曼滤波、交叉熵航线规划器、联合嵌入预测架构时空模型、出发前预演与在线留出估值控制器、论文全部图表的生成脚本、原始实验结果数据，以及作者与人工智能助手的研究讨论记录（已隐去涉及作者其他未发表工作的讨论内容）均开源于：\TBD{GitHub 仓库地址}。在代码仓库中，运行 \texttt{experiments/rev2.sh} 即可按固定随机种子完整重现正文与附录的全部数值实验，运行 \texttt{experiments/rev2\_summary.py} 与 \texttt{experiments/rev2\_tables.py} 可由原始输出日志直接汇总生成文中的全部统计置信区间与表格文件。

实验使用的两套卫星遥感数据集均下载自美国国家海洋和大气管理局海岸观测网的公开数据服务器：
\begin{enumerate}
  \item \textbf{东海多星融合叶绿素 a 逐日数据集（2018—2026年）：}融合了极轨卫星水色传感器观测并经经验正交函数缺失数据插补算法填补云区盲区，空间分辨率为$2\text{ km}$，时间分辨率为逐日，遵循公共领域开放许可，数据集标识为 \texttt{noaacwNPPN20S3ASCIDINEOF2kmDaily}。
  \item \textbf{多尺度超分辨率海表温度逐日数据集（2018—2026年）：}由美国国家航空航天局喷气推进实验室制作（版本4.1），原始空间分辨率为$0.01^\circ$，时间分辨率为逐日，数据集标识为 \texttt{jplMURSST41}。
\end{enumerate}

\section{人工智能工具使用说明}

在本课程论文的研究与写作过程中，人工智能工具的使用情况与各环节具体分工如下：
\begin{enumerate}
  \item 作者本人提出了本文的核心研究问题（自主水下航行器在现场巡测中何时应当继续计算、何时应当继续观测），确立了研究思路、实验设计与写作规范，并对论文的全部内容与学术诚信承担完全责任。
  \item Claude（Anthropic）协助完成了相关文献检索与核查，与作者讨论细化了技术方案，编写了仿真与实验代码，运行了全部数值实验并绘制了论文图表。
  \item Gemini（Google）根据实验事实清单与结构大纲协助撰写了论文初稿与修改稿的正文文字。
  \item 作者与 Claude 对照原始实验日志与出版文献逐一核查了文中的全部数值结果、置信区间与参考文献引用。
\end{enumerate}
```

</details>
