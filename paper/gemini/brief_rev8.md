# Revision 8: polish the whole paper — clear main line, positive results, standard terms, shorter

The student's instruction for this round, verbatim:
"提醒一下gemini润色一下逻辑性和可读性，不要写自己编造的黑话，呈现正面结果，应当主线清晰篇幅不要太长"

So: rewrite every attached section file for logic and readability; use standard terms or plain words
(terms_v6.md: every label in its last column is home-made jargon and must not appear); lead with the
positive results; keep one clear main line from the abstract to the conclusion; and cut the length by
about 30% (caps below). Every fact must stay exact (facts_v3.md, facts_v4.md, the tables); do not add any
claim that the facts do not support.

## The main line (the same in abstract, introduction, experiments and conclusion)
Problem: a vehicle with a 3-day-old 1° coarse current map must pass a no-go zone on the left or the right;
a wrong side costs hours. Should it compute more, observe, or play safe?
Idea: two kinds of ambiguity. Numerical ambiguity (the solver is too coarse) is removed by computing more.
Environmental ambiguity (the map is consistent with currents that favour either side) is not; it needs new
information. The plausible counterexample test asks: within the set of currents consistent with the map
(sized from years of reanalysis errors), is there one that makes the other side faster, and how much time
could the current choice lose at most (the maximum regret)? A threshold on the maximum regret says when the
map cannot be trusted.
Positive findings, holding in all four settings (黑潮主设置、湾流、阿古拉斯回流区、黑潮区改带卫星测高地转流图):
  1. Computing more does not fix wrong choices: 64 times more computation leaves the wrong-side share almost
     unchanged (黑潮 21.7% → 19.7%; similar in the other three settings).
  2. The maximum regret finds where the extra time is: the 20% of missions it ranks riskiest hold 53%-71% of
     the extra time, more than ranking by the share of ensemble members that change the choice (36%-52%)
     or by the closeness of the two sides on the map. And it is cheap: about 71 route solves reach the side
     choice that averaging over random ensemble members needs about 2048 solves (1024 members) to reach.
  3. Once the map is flagged as untrustworthy, new information pays most: surfacing for today's 0.5° map
     only on flagged missions cuts the mean extra time from 3.56 to 1.31 hours in the Gulf Stream and from
     6.87 to 2.20 hours in the Agulhas; in the Kuroshio main setting it pays when one surfacing costs less
     than about 1 hour.
Scope (state briefly and plainly in the experiments' scope subsection, the limitations and once in the
abstract/conclusion; do not let it dominate): choosing the side with the smaller maximum regret without
observing helps significantly only in the Kuroshio main setting (0.98 → 0.70 hours); it is not significant
in the other three settings; with the satellite map, plausible counterexamples exist for 81.0% of missions
and no response is significant.
Meaning: the plausible counterexample test tells reliably when the map cannot be trusted and where the
extra time lies; the answer is then to get new information, not to compute more.

## Structure (keep every \label, \ref, \cite, equation, \includegraphics name, \input line and the URL)
1 引言 (cap 1400): background; the left/right decision and why it matters (one example from Fig. 1, two
  numbers); why computing more, ensembles and adaptive sampling fall short (one short paragraph); the idea;
  the three positive findings (one sentence each); contributions (three short items; keep the phrase
  "据我们所知，本文首次" in item 1); one-sentence road map.
2 相关工作 (cap 650): three short paragraphs; end each with how this paper differs.
3 前期研究 (cap 550): what the earlier bloom-survey study showed (computing more inflates the planner's
  own score while the real value stops improving; how time is split matters little) and why this led to the
  present question. Use the new prior-study words from terms_v6.md.
4 问题建模 (cap 1000): data and missions (Table 1); route solver (equations as they are); the plausible set
  (equations as they are); options and the extra-time measure. Drop the separate "问题剖析" subsection
  (fold its two key points into one sentence in 4.4 or in the method's opening).
5 方法 (cap 1200): 5.1 numerical ambiguity check; 5.2 searching the maximum regret (envelope-theorem
  gradient, equations as they are, about 71 solves); 5.3 calibrating the set from data (76 km, radius 1.5,
  93%/94% coverage); 5.4 threshold rule and responses. Rewrite the algorithm box in the new terms, same
  steps.
6 实验 (cap 3600), subsections in this order:
  6.1 实验设置与对比方法 (the four settings in one paragraph; development 2019-2021, test 2022-2024; the
      policies compared, in the new terms; statistics);
  6.2 粗图误差具有可标定的空间结构 (Fig. data; short);
  6.3 发现一：多算消除不了环境歧义 (Fig. ambiguity; Kuroshio numbers plus one sentence on the other three
      settings);
  6.4 发现二：最大后悔值找得出额外航时所在，而且算得快 — keep \label{sec:budget} on this subsection
      (ranking across settings with Fig. risk (a); the efficiency result with Fig. budget; the reason the
      ensemble average needs so many members: with 32 members its sampling error (2.4 h) exceeds the
      correction it estimates (1.7 h));
  6.5 发现三：判定不可信时，取新信息最划算 (Fig. main and Fig. risk (b): surfacing results and the 1-hour
      crossover in the Kuroshio; Gulf Stream and Agulhas surfacing; probing helps in the Agulhas only;
      waiting or detouring to measure does not pay);
  6.6 适用范围 — keep \label{sec:scope} on this subsection (Table 2; better map, slower vehicle, ablation of the
      plausible set; the conservative choice without observing: significant only in the main setting, why
      it fails where either side can be blocked (Gulf Stream 8.7% of missions), the revised rule tested on a
      plan written before the Agulhas data were downloaded (harmless, no significant gain), the satellite
      map test (planned before download; 81.0% of missions with a counterexample; no response
      significant)). One paragraph per topic, finding first.
  6.7 局限 (short list).
7 原创创新点拆解 (cap 450 plus the table; table cells short, at most about 45 characters each).
8 结论 (cap 330): principle; the three findings; scope in one clause; future work.
Appendix: keep content and roles exactly; only replace old terms.

## Writing rules
- Plain, logical Chinese; one idea per paragraph; the first sentence states the paragraph's conclusion;
  connectives that show the logic (因此、然而、相反、进一步).
- At most about 5 numbers per paragraph; leave the rest to the figures and tables. Intervals: give the main
  one (0.98 → 0.70, −0.28 [−0.51, −0.07]) once; elsewhere say in words whether a result is significant.
- No English abbreviations in Chinese text; no emotive or inflated words (揪出、彻底、灾难、飙升、竟然、高达、
  仅仅、一眼、白白、毫无、有力证明); "显著" only where a confidence interval excludes 0.
- Captions: at most about 120 characters each; describe the panels in the new terms; no numbers that the
  figure already shows unless needed for the takeaway; no error bars are drawn.
- Abstract: Chinese at most 480 characters; English at most 250 words with the same content and the same
  standard terms (maximum regret, threshold, ensemble average, extra time).

## Output
All eleven section files and Table 1, each preceded by its line:
"===== FILE: sections/<name>.tex =====" for title, abstract, intro, related, prior, problem, method,
experiments, innovation, conclusion, appendix; and "===== FILE: tables/route_settings.tex =====" (Table 1
rewritten in the new terms, same rows and facts).
