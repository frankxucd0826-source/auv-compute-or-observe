# Revision 4b: tighten draft 4 to journal length and correct it (EDIT, do not rewrite)

Draft 4 (attached as the current sections/*.tex) has the right structure, but it compiles to 26
pages and the body text is about 15,900 Chinese characters; the course asks for a paper of a dozen
or so pages. Please EDIT draft 4: keep every section and subsection, every equation, the algorithm,
all figures and tables with their labels, and all citations; shorten the prose and apply the
corrections below. Do not turn paragraphs into lists; do not drop any finding.

## Length targets (Chinese characters of running text, without captions, tables, algorithm)
Total body 9,000-10,000 (lower bound 8,500). Per section, at most: 引言 1,500; 相关工作 800;
问题建模 1,500; 方法 2,000; 实验 3,800; 结论 400. Abstract at most 450 characters; English
abstract at most 230 words. Shorten subsection titles to at most 12 characters, plain words
(e.g. 实验设置, 卫星大数据的作用与局限, 规划自评的偏差, 主要结果, 机理分析, 消融实验, 适用范围, 局限性).

## How to cut (in this order)
1. Numbers: keep in the text only the numbers that carry a claim (the paired differences of the
   main comparison, the key rates); move the rest to the figures and tables they already appear in
   (do not repeat a caption's numbers in the text; do not list every interval).
2. Implementer detail already in Table 1 (data product, grid sizes, power split, sample rates,
   window criteria) appears once, in Table 1 or one sentence of 3.1, not in several places.
3. The EAKF exposition in 4.1: keep the prior equations and one compact sentence on the
   localised serial ensemble adjustment Kalman filter with its two equations; cut the surrounding
   prose by half.
4. The strategy list in 4.3: one line per strategy, no battery-life arithmetic.
5. 5.5 (choices of rehearsal): one paragraph; the shares are in Fig. 5c.
6. 5.6: one paragraph per group of ablations, about 3 sentences each.
7. Remove every sentence that only announces what a figure shows.

## Corrections (all required)
1. Abstract last sentence: "证实" -> "表明". Intro: "绝不能" -> "不应"; delete "而且在未知测试年份上的
   泛化表现依然无法超越简单的固定策略" (an own result does not belong in the introduction).
2. Related work 2.3: "本文首次将……" -> "尚未见将……的研究；本文……".
3. 3.4 (问题剖析): delete "\cite{assran2025vjepa2}" from the sentence on forecasting (that paper
   does not show it; refer to Section 5.2 instead); replace "全程开启高功耗芯片只会白白透支推进电池并
   缩短总航程" by a neutral statement that on a fast computer the extra energy buys little; replace
   "唯有在下水前……才能……" by a statement that does not exclude the online variant.
4. 4.4 must describe the held-out variant exactly: it differs from classic one-step metareasoning
   in TWO places - (i) the value of more planning and of resampling is judged on the 16 held-out
   oceans (routes still chosen on the 32 searched ones), and (ii) it leaves "go" only when another
   use of the interval is better by more than two standard errors of the paired difference over
   the imagined truths, whereas the classic one takes the plain maximum. Never write "其余流程完全
   不变" or "仅将……改为".
5. 5.2: delete the untested explanation "由于云区插补产品平滑了日内潮汐混合与亚中尺度梯度，数值外推无法
   凭空恢复小尺度峰值"; keep the finding.
6. 5.3: "这证实……能够彻底切断……" -> "表明……" without "彻底".
7. 5.4: the first sentence must say rehearsal beats all survey rules except greedy on the slow
   computer under the main truth model (tie); delete "在统计上高度显著"; delete "这直接解释了为何
   按历史任务学习的选择器……无法……超越" (not tested); keep the reproducibility sentence in 5.1 as
   one clause.
8. 5.5 mechanism paragraph: held-out one-step regrets are 0.278 / 0.270 / 0.270 / 0.267 (not
   0.269 on the fast computer), i.e. 0.009 / 0.017 / 0.012 / 0.010 below classic one-step
   metareasoning (not 0.013 / 0.011). Replace "这一对照实验直接证明……正是由……引起的" and "唯一残余
   损失来源" by what the one-change diagnostic shows: [DIAGNOSTIC RESULTS - see below].
9. Example mission (5.5): keep it factual - delete "果断", "远端高梯度潜力", "及时识别出"; say that
   with 5000 rollouts in a thinking interval the plan crossed the window to the south-west corner.
10. 5.7: fill the two \TBD with the numbers below; replace "严重推迟……沉重惩罚" by plain wording.
11. Every "直接证明/证实/彻底/根除/完全/唯一/盲目" that is not literally true: soften to a factual
    verb or delete.

12. 结论: "实验证实" -> "实验表明"; say rehearsal beats the survey rules except greedy on the slow
    computer; keep the future-work sentence short.
13. 附录 A: the scripts that reproduce the paper are experiments/main_eval.sh and phase.sh (main
    comparison, development tuning, phase diagram), experiments/anytime_curse.py (planning budget),
    experiments/rev2.sh and rev2_diag.sh (second round: survey rules, satellite-map truth,
    ablations, fresher map, one-change diagnostic), with the summaries experiments/main_extra.py,
    rev2_summary.py and rev2_tables.py; the exact commands are in README.md. Do not claim that one
    script reproduces everything.
14. 附录 B must state the division of work exactly as follows (rephrase lightly, keep the facts):
    the author proposed the research question, set the direction and the requirements (including the
    second-round requirements: real satellite data, more baselines and ablations, journal format,
    figure quality) and is responsible for the paper; Claude (Anthropic) did the literature search
    and checks, refined the topic, wrote the code, ran all experiments, drew the figures and checked
    every number and citation in the text against the experiment records; Gemini (Google) wrote the
    text from Claude's facts sheet and briefs. Do NOT say that the author checked the numbers.

## Numbers for the \TBD and the diagnostic
- Phase diagram, fourth row (the satellite map of the day itself as truth): on the 5-per-minute
  computer thinking beats always going by 0.080 (interval -0.119 to -0.043); from 10 per minute up no
  clear gain; stopping is worse in every cell of this row (0.061-0.076). Over all 24 cells the better
  stopping strategy is 0.061-0.118 worse than the best moving one (update the Fig. 8 caption: it now
  says +0.063 to +0.118).
- Fresher map, moderate computer: the tuned fixed strategy is 一直走 (0.250); rehearsal 0.243, lower
  than the tuned strategy by 0.007 (interval -0.014 to -0.002) and than one-step metareasoning (0.260)
  by 0.017 (-0.022 to -0.013); on the test years 三段深想一段 (0.239) is the best fixed strategy
  although 一直走 was best on the development years.
- One-change diagnostic (new, 5.5; slow and moderate computers, same 148 missions and seeds): the
  held-out variant changes two things, so each was also run alone: (a) held-out valuation only
  (plain maximum); (b) the two-standard-error rule only (valuation on the searched oceans).
  Pattern (write the paragraph with \TBD{...} for each number; I will fill them in): held-out
  valuation alone brings the share of intervals with the high-performance computer on down from about
  80% to about 30% on the slow computer while the stopped share stays about one third; the
  two-standard-error rule alone leaves thinking unchanged (about 80%) and lowers the stopped share;
  both together give the lowest regret. Reading: over-thinking comes from valuing computation on the
  searched oceans (the planner's own fit), excess stopping from reacting to small noisy differences;
  the held-out variant fixes both. Write this as the mechanism, replacing the sentences named in
  correction 8; mention it in one clause in the abstract and the conclusion only if it fits the
  length.


## Output
The same nine files, each preceded by a line "===== FILE: sections/<name>.tex =====".
