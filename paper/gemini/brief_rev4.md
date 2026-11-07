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
