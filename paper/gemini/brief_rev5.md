# Revision 5: a new paper on route decisions under a coarse current map (in Chinese)

## Why a new paper
This is a Zhejiang University course paper for 《海洋大数据技术原理与应用》. The student's entry
point is the course topic "海洋大数据的计算引擎": ocean big data is computed not only in data
centres but more and more on the vehicle itself, and an autonomous underwater vehicle's onboard
computing is limited, which naturally raises the trade-off between computing, measuring and moving.
The student first asked when an ocean vehicle should keep computing and when it should observe
again, and we studied it on harmful-algal-bloom surveys (the earlier study, facts_v3.md section 前期研究).
That study found that computing more made the planner's answer more "refined" without giving it
new information: its own score kept rising while the real value had stopped improving, and the
choice of how to split time between computing and observing could change the outcome only a
little. The student then sharpened the question and moved it to where it matters, the route
choice under a coarse current map: two routes, a coarse map, and possibly several current fields
that agree with what is known yet call for different routes. The new experiments answer it.
Write a NEW paper; the earlier study is a short motivating section, not the subject.

## The central idea (the one thing the reader must carry away)
Computation and observation remove different kinds of uncertainty. When the two routes are close
only because the solver is imprecise (numerical ambiguity), computing more decides correctly. When
there exist current fields that agree with the available information as well as the real ocean
does, yet make the other route better (environmental ambiguity), no amount of computation can
decide; only new information can, and if information is too expensive the vehicle should choose
the route whose worst plausible loss is smallest. The operational test is the student's question:
for the recommended route, can we find a plausible current field that makes the other route
better, and by how much? "Plausible" is defined with ocean big data: the error of stale coarse
maps, calibrated on six years of reanalysis currents, sets the plausible set and its radius.
Say this idea in the introduction where the approach is introduced, as contribution 1, and once
more in the conclusion, each time from a different angle; do not repeat the same sentence.

## What the evidence says (use these claims, with numbers only from facts_v3.md)
- More computation fixes little: 64 times more computation lowers the wrong-side rate only from
  21.7% to 19.7% (it fixes 28% of the cheap solver's errors), whereas today's 0.5° map would halve
  it (10.4%).
- Environmental ambiguity is the rule for a 3-day-old 1° map in the Kuroshio region: with the
  plausible set just large enough to contain the real ocean (93% on development years, 94% on test
  years), a plausible counterexample exists for 99.7% of decisions. So existence alone is not
  informative; the size of the worst plausible loss is.
- The worst plausible regret finds where the losses are: the 20% of missions it ranks highest hold
  67% of the map's loss (32-member ensemble flip share 49%, map margin 34%).
- Responses: the conservative choice on flagged missions cuts the mean loss from 0.98 to 0.70 h
  (28%, interval excludes 0); measuring on the way (30 or 60 km) does not help because the decisive
  currents lie farther ahead; detouring to measure costs 12.4 h; hovering costs 2 h and only
  resolves noise at one point; surfacing for today's 0.5° map pays when it costs less than about
  1 h, and the conservative choice is better when it costs more. The expected-time (Bayesian)
  choice does not help on the test years.
- State honestly that the gate's gain over always choosing conservatively is small (0.70 vs 0.72):
  the value comes from the counterexample's worst regret itself.

## Structure (sections and what each must do)
- Title (sections/title.tex): concrete, says what was done. Suggested direction: “合理反例检验：粗分辨率
  海流图下自主水下航行器何时计算、何时观测” (you may improve it; no English, no colon-less slogan).
- 摘要 (about 450 Chinese characters) in Ma Dongfang's eight steps: background; need; what existing
  methods lack; what this paper proposes; its key points; the experiment; the main numbers;
  significance. 关键词 4-6. Then the English title, Abstract (same content) and Keywords, in
  sections/abstract.tex formatted as in the current file ({\heiti 摘要：} ... and {\bfseries Abstract:} ...).
- 1 引言 (no subsections, about 1500-1800 characters): (1) paradigm: the computing engine of ocean big
  data extends to the vehicle's edge; limited onboard computing makes "compute, measure or move" a
  real decision; (2) the case and why it is hard: routing an underwater vehicle through strong
  currents (the Kuroshio east of Taiwan and the East China Sea) with a coarse, days-old current map,
  where currents are comparable to the vehicle's speed and a wrong side costs hours; (3)-(5) the
  existing paths, one per paragraph, each "the obvious way -> why it fails here": plan on the best
  estimate and spend more computation (certainty equivalence: answers sharpen, information does
  not grow; the earlier study and Fig. 1); risk-aware planning over ensembles of forecasts (chooses
  a safe route but does not say whether to compute or observe, and a finite ensemble can miss the
  field that flips the decision); value-of-information sampling (values information about the
  whole field rather than about the decision; sequential design and best-arm identification give
  the right principle: look for the closest alternative that changes the decision); no own numbers
  in these paragraphs; (6) this paper's idea and approach, ending with Fig. 1; (7) three
  contributions as bullets, each opening with a bold label and a claim of what is new (idea /
  method / evidence), contribution 1 with "据我们所知，首次" on separating numerical and
  environmental ambiguity for ocean-vehicle route decisions and testing the latter by a plausible
  counterexample; (8) one organization paragraph.
- 2 相关工作 (three short subsections, 900-1200 characters in total): metareasoning, value of
  computation versus value of information, and over-thinking in agents, with clarification-seeking
  for ambiguous tasks as the language-model counterpart; decision-relevant information (sequential
  design, model discrimination, best-arm identification, information-directed sampling,
  goal-oriented experimental design, info-gap robustness, predictive multiplicity); path planning
  in uncertain ocean currents (level-set time-optimal planning, ensemble paths, stochastic and
  risk-optimal paths, forecast-uncertainty planning, adaptive sampling). Each ends with one sentence
  on how this paper differs.
- 3 前期研究：多算为何收效甚微 (about 600-800 characters, Fig. curse): the bloom survey in one paragraph
  (stale satellite chlorophyll map, compute/measure/stop), then the two findings: the planner's own
  score inflates with computation while the real value saturates (numbers in facts), and the time
  allocation has little room compared with information and launch position. End with the question
  this raises, in the student's words: when several worlds fit what is known and call for different
  decisions, computing more cannot tell them apart.
- 4 问题建模 (about 1300-1600 characters): 4.1 scenario and data (Table 1; Fig. data may be cited
  here or in Section 6); 4.2 route time and solver budgets (equation for the edge time: ground speed
  along an edge = along-edge current + sqrt(V^2 - cross-edge current^2); the two sides via the
  no-go zone); 4.3 plausible current fields: map + error modes from a stream function (divergence
  free), scaled by the calibrated error map, coefficients standard normal, radius r; 4.4 actions
  and costs (commit; compute; observe: hover, measure on the way, detour, surface for a newer map;
  hedge) and the loss; 4.5 问题剖析: the root conflict (the decision needs information the map lacks,
  while computation only sharpens what the map says) and two properties that make it hard, from
  which the method follows: (a) ambiguity has two sources that call for different actions;
  (b) whether new information is worth its cost depends on how much the decision could lose.
- 5 方法 (about 1800-2200 characters, about 28-32% of the body): opening sentence with Fig. overview.
  5.1 numerical check (cheap solve; refine when the margin is within the numerical tolerance);
  5.2 counterexample search: maximize the margin against the chosen side over the plausible ball by
  projected gradient ascent; the gradient of a route's optimal time with respect to the currents is
  the sum along that route (envelope theorem), so each step costs two route solves; first jump to
  the ball's edge along the gradient (exact if the margin were linear), then refine; output the
  worst regret and the counterexample field; 5.3 calibrating "plausible" with ocean big data: the
  radius is the smallest one whose range covers the real margin in at least 90% of development
  missions; 5.4 gated response: worst regret below the threshold -> commit; above it -> observe if
  an observation is cheap (surface for a newer map), otherwise choose the side with the smaller
  worst regret; thresholds set on development years only. Algorithm 1 (algorithm + algpseudocode:
  \Require, \Ensure, \State, \If, \Else, \EndIf, \Return) for the whole check. Each subsection opens
  with its principle, then the choice existing methods would make and the cost it ignores.
- 6 实验 (about 35-40% of the body): opening paragraph stating the questions answered, in order.
  6.1 设置 (Table 1; baselines defined once with the names of terms_v5.md, grouped as in Fig. main;
  development/test split; statistics). 6.2 旧粗图错在哪里 (Fig. data). 6.3 计算消除不了环境歧义
  (Fig. ambiguity). 6.4 主对比 (Fig. main). 6.5 损失集中在哪里、何时值得观测 (Fig. risk; include the
  probe numbers in words: switching after 30 km happens in 3.4% of missions and is right in 81%,
  after 60 km in 18.8% and right in 15%; detours start with a 15.4-hour transit). 6.6 适用范围
  (Table 2, tables/route_scope.tex; if the table file is not attached, write the subsection from the
  facts' 适用范围 section). 6.7 局限 (one short paragraph: steady snapshots rather than evolving
  currents; reanalysis as the real ocean; a two-sided decision; the within-side execution
  assumption). Each subsection: first sentence = its finding; then purpose -> finding -> interpretation.
- 7 原创创新点拆解 (required by the course; about 900-1200 characters plus one table): open with the
  path of thinking in plain academic Chinese (the course topic -> limited edge computing -> the
  first question -> the earlier study's small gains -> the sharper question about indistinguishable
  worlds -> the counterexample test). Then a table (\begin{table}[htbp] ... tabular with p-columns,
  \toprule/\midrule/\bottomrule) with four rows: (1) separating numerical from environmental
  ambiguity; (2) the counterexample test with the gradient search; (3) calibrating "plausible" with
  big data (coverage of the real margin); (4) the gated response (observe or hedge by cost). Columns:
  创新点 | 已有做法及其不足 | 本文做法 | 证据（图表） | 局限. Then one paragraph on what the student
  contributed and what the AI tools did (consistent with Appendix B): the student proposed the
  original question, insisted on real data, criticized the small gains and limited novelty of the
  first method, and proposed the two-route counterexample question that this paper tests; the
  AI assistant did the literature search, code, experiments and figures; Gemini wrote the text.
- 8 结论: formal; the idea restated from a new angle; the main evidence in two sentences without
  repeating every number; one sentence of future work (evolving forecasts and field trials with an
  onboard current profiler).
- 附录 (sections/appendix.tex): A 代码与数据 — the repository (keep the \url{...} address exactly:
  https://github.com/frankxucd0826-source/auv-compute-or-observe), the data (HYCOM reanalysis via the
  public server; NOAA satellite chlorophyll for the earlier study), and the scripts:
  scripts/download_hycom.py, src/oceanroute/ (solver.py, fields.py, errormodel.py, mission.py),
  experiments/route_eval.py, experiments/route_summary.py, experiments/route_facts.py,
  experiments/route_example.py, paper/figures/fig_route_*.py; the earlier study's scripts are listed
  in the repository README. B 人工智能工具使用说明 — a numbered list, factual: the student (作者) proposed
  the research question and its later sharpening, set the requirements and judged every turn,
  and is responsible for the paper; Claude (Anthropic) did literature search, coding, experiments,
  figures and checked every number and citation; Gemini (Google) wrote the text from Claude's facts
  and outline; the full conversation records are in the repository.

## Style (the student's standing requirements)
1. The first sentence of every paragraph states its conclusion; reading only first sentences must
   tell the whole story. Never open a paragraph with "如图X所示" or with a setting.
2. Introduction and method follow "常规做法 -> 为何在这里失效 -> 因此这样做"; principle first, the
   replaced choice second.
3. No hedging, no defensive asides, no replies to imagined reviewers, no "值得注意的是/需要指出".
   Limitations only in 6.7, once. Do not oversell: write what the evidence shows (e.g., measuring on
   the way did not help here) plainly, as findings.
4. No coined terms beyond terms_v5.md and NO English abbreviations in the Chinese text (write
   自主水下航行器/航行器, 再分析, 流函数; not AUV, HYCOM is a product name and may appear once in 4.1
   and Table 1 only). Units: 千米、米/秒、小时.
5. Numbers: reason first, numbers after; at most about 6 numbers per paragraph; quote 95% intervals
   only where they carry a claim (the 28% reduction; the non-significant ones may be summarized in
   words); never invent a number - every number must come from facts_v3.md.
6. Formal academic Chinese with proper connectives (然而、因此、相反、进一步); no slogans, no
   rhetorical questions, no semicolon chains of facts, no list-style paragraphs in the body (lists
   only for contributions).
7. Figures are part of the argument: cite each figure where its claim is made; each caption = what
   is shown (panels) + the takeaway in one sentence; do not repeat captions in the text. Figure
   order of first mention: overview, curse, data, ambiguity, main, risk.
8. Cite only keys in the attached list; each citation must support its sentence.
9. Length: body (sections 1-8, without captions, tables, algorithm and references) 10,000-12,000
   Chinese characters.

## LaTeX
- Files: sections/title.tex (title text only), abstract.tex, intro.tex, related.tex, prior.tex
  (Section 3), problem.tex, method.tex, experiments.tex, innovation.tex (Section 7),
  conclusion.tex, appendix.tex.
- \section{...} is numbered by ctex as "1 引言". Figures: \begin{figure}[htbp]\centering
  \includegraphics[width=\linewidth]{fig_<name>}\caption{...}\label{fig:<name>}\end{figure}, placed
  right after the paragraph that first cites it; labels: fig:overview, fig:curse, fig:data,
  fig:ambiguity, fig:main, fig:risk. Tables: Table 1 = \begin{table}[htbp]\centering\caption{...}
  \label{tab:settings}\small\input{tables/route_settings.tex}\end{table}; Table 2 = the same with
  tables/route_scope.tex and tab:scope; Table 3 = the innovation table in innovation.tex (tab:innovation).
- Escape every % as \%. Use math mode for symbols ($V$, $r$, $\Delta T$). Use \cite{key}.

## Output
The eleven files, each preceded by a line "===== FILE: sections/<name>.tex =====".
