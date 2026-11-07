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
