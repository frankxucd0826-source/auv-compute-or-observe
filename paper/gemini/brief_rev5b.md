# Revision 5b: tighten and correct the revision-5 draft (edit the attached files; do not rewrite from scratch)

The attached section files are your revision-5 draft after Claude's factual corrections. The content and
structure are right; the draft is about 35% too long (23 pages; the course wants "十几页") and several
paragraphs pile numbers. Edit the attached text: keep its argument, cut repetition and numbers, and keep
every corrected fact listed below exactly as it now stands.

## Length caps (Chinese characters of running text, excluding captions, tables and the algorithm)
abstract 480 (English abstract at most 230 words, same content) | intro 1700 | related 1000 | prior 850 |
problem 1700 | method 2200 | experiments 3200 | innovation 900 (the table stays) | conclusion 380.
Do not go below 85% of any cap.

## Numbers (the student's rule: a results paragraph must not read as a pile of numbers)
- At most about 6 numbers per paragraph; give the finding in words first, then only the numbers that carry
  it; leave the rest to the figures and tables (they already show them).
- Intervals: keep only the main one (门控后取保守 vs 照精算地图走: −0.28 小时, [−0.51, −0.07]). For the
  others say in words whether the interval contains 0.
- Introduction paragraph 6 (the example): keep only "粗图上两侧只差约0.3小时" and "真实海洋中右侧快11.7小时";
  the other example numbers are in the Fig. 1 caption.
- Section 6.3: give 21.7%, 19.7%, 10.4%, 28% of cheap-solver errors fixed, 93%/94% coverage and 99.7%;
  drop the list of shares at every radius (the figure shows it).
- Section 6.5: give 67% vs 49% vs 34%, the 47% of missions flagged holding 82% of the loss, the probe facts
  (3.4% switch / 81% right after 30 km; 18.8% / 15% after 60 km), the 15.4-hour detour, and the crossover
  of surfacing near 1 hour (between 0.5 and 1 hour) with at most two points of the cost sweep.
- Section 6.6: one or two sentences per setting, at most three numbers each, and the ablation conclusion as
  now written.
- Add one sentence in 6.4 explaining why the conservative choice pays (facts: of the 41 switched missions,
  23 were right and saved 10.1 hours on average, 18 were wrong and cost 3.3 hours on average).

## Corrected facts that must stay exactly as they are (Claude checked them against the code)
1. problem.tex: the plausible-field equation u = u0 + sum z_k m_k, m_k = S(x) grad-perp phi_k, with S(x)
   the diagonal rescaling to the calibrated error variance ("缩放后近似无散"); the set ||z||_2 <= r (no
   1/sqrt(K)); "以边两端节点海流的平均作为该边的海流".
2. method.tex: the worst-regret definition over ||z||_2 <= r; the jump z = ± r g/||g||; the envelope-gradient
   equation with the edge's two end nodes and m_k; "避免了这一开销"; the ensemble limitation as now written
   (flip share does not measure the size of the loss; the margin is sensitive to few directions);
   the radius rule as now written; the two radii 1 and 2 with linear interpolation; about 71 solves.
3. experiments.tex: the slow-vehicle sentence (interval contains 0, not significant; surfacing pays more
   because a wrong side costs more); the ablation conclusion (same search, different definition of
   "plausible"); the main-figure caption without error bars.
4. innovation.tex and appendix.tex: the course entry point as now written ("课上讲授的“海洋大数据的计算引擎”
   使作者联想到…"), the description of what the student did and what the AI tools did, the table row 2
   wording, the file descriptions in appendix A. Do not add claims about the student beyond these.
5. Keep every equation, \label, \ref, \cite, figure, table, the algorithm and the repository \url unchanged.

## Wording to remove (informal, emotive or overstated)
揪出、刀刃、彻底、本质边界、灾难性、有力证明、严格不包含、高达、仅仅、竟然、飙升、一眼看清、毫无、白白、
"Danskin" may stay once. No "如图X所示" at the start of a paragraph; the first sentence of every paragraph
states its conclusion. Keep formal connectives (然而、因此、相反、进一步).

## Output
All eleven files, each preceded by a line "===== FILE: sections/<name>.tex =====" (title, abstract, intro,
related, prior, problem, method, experiments, innovation, conclusion, appendix).
