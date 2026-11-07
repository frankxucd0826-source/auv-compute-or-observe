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
