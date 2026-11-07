# Revision 6b: add the third region (Agulhas), a test written down before its data were downloaded

The attached section files are the current, checked paper. One more result must go in: an independent test
in a third region, the Agulhas retroflection south of Africa (facts_v4.md, last section 第三海区独立检验).
The plan was written into the research notebook before the data were downloaded and was not changed; the
radius and thresholds were calibrated on the region's own development years; the test years were scored
once. It tested the refined rule proposed after the Gulf Stream results (switch only when the two sides'
worst regrets differ by more than the numerical tolerance; no new parameter). Results, in the plan's own
terms (use the facts' numbers exactly):
1. refined rule: −0.16 h, interval contains 0, point estimate below 0 → harmless, no significant gain;
2. original conservative rule: not significant either (16.2% of missions have one side impassable);
3. gated surfacing for today's 0.5° map: 6.87 → 2.20 h, interval excludes 0 → holds;
4. extra computation: wrong-side share 27.7% → 27.7% (32 choices changed, 16 right, 16 wrong) → holds;
5. ranking: worst regret's top 20% hold 53% of the loss, flip share 36% → holds.
Also: probing the first 30 km helps significantly here (4.48 h, −2.39), unlike in the other two regions.
Reading across the three regions (say it plainly): consistent are "computation does not remove the
ambiguity; plausible counterexamples are almost everywhere; the worst regret finds where the losses are;
once flagged, observing pays". The observation-free conservative choice is significant only in the
Kuroshio; the refined rule makes it harmless elsewhere but brings no significant gain. So the gate's value
is deciding *when to observe*; the observation-free conservative choice is a region-dependent fallback.

## Pieces to write (output each after its marker line, nothing else)

===== S1 =====
experiments.tex, Section 6.7: a new paragraph starting "第五，" placed after the paragraph that starts
"然而，不观测直接改选保守一侧在湾流未能复现" and before the table. About 300-400 characters, at most
eight numbers. Say that the test was written down before the data were downloaded, give the five
outcomes compactly (finding first), and end with the cross-region reading above. Do not repeat the
Gulf Stream numbers.

===== S2 =====
abstract.tex: the whole file. Replace the last Chinese sentence (湾流区…) by one sentence on both
replication regions (Gulf Stream and Agulhas): computation useless, ranking and gated surfacing hold
(3.56 → 1.31 h and 6.87 → 2.20 h), the observation-free conservative choice brings no significant gain
there. Do the same in the English abstract (last sentence). Keep everything else word for word. Chinese at
most 570 characters, English at most 285 words.

===== S3 =====
intro.tex, item 3 of the contributions itemize (starts "\item \textbf{黑潮与湾流两个强流区的系统实证：}"):
rewrite for three regions (黑潮、湾流与阿古拉斯回流区); keep the Kuroshio sentence as it is; one sentence
for the two replication regions, including that the refined rule was tested in the third region on a plan
fixed before its data were downloaded.

===== S4 =====
innovation.tex, table row 4 (starts "4. 权衡最坏后悔与观测代价的门控响应"): rewrite cells 4 and 5 only
(output just these two cells separated by " & " and ending with " \\"), adding the Agulhas numbers
(gated surfacing 6.87 → 2.20 h; conservative choice not significant in either replication region).

===== S5 =====
experiments.tex, the limitations paragraph (starts "本研究存在五方面局限"): rewrite point 5 only for
three regions (output the whole paragraph; points 1-4 word for word).

===== S6 =====
conclusion.tex: the whole file; replace the sentence on the Gulf Stream replication by one on both
replication regions. At most 480 characters of running text.

## Rules (as before)
- Every number must appear in facts_v4.md or facts_v3.md. At most about 6-8 numbers per paragraph.
- Terms as in terms_v5.md; 阿古拉斯回流区 for the third region; 改进规则 for the refined rule (describe it
  once in words: 仅当两侧最坏后悔之差超过数值误差容限时才改选).
- No English abbreviations in Chinese text; no emotive or inflated words; no "显著" unless a confidence
  interval excludes 0; first sentence of each paragraph states its conclusion.
- Keep every \label, \ref, \cite as given.
