# Revision 3 (final tightening)

Draft 3 (attached as the current sections/*.tex) is correct in substance and well organised.
This last pass is about length and a few precise points; please keep the structure, the
numbers and the citations as they are unless listed below.

## 1. Length
The compiled paper is 24 pages; it should come down to about 21-22 (the course asks for "十几页").
Bring the body from about 9,600 to at most about 8,500 Chinese characters, without dropping any
finding. Candidates:
- 5.3, first paragraph: the development-year regrets of the tuned strategies (0.298/0.299/0.310,
  0.292/0.296/0.299) - naming which strategy was tuned for each vehicle is enough; the test
  numbers are in the table.
- 5.3, fourth paragraph (held-out versus searched rehearsal): very long; keep the findings
  (similar overall shares, 37-41% per-mission agreement, avoids bad options, no better than chance
  among near-tied strategies, room shown by the per-mission best in hindsight) with fewer numbers.
- 1.1: the two paragraphs say similar things; one paragraph is enough.
- 4.3: the cost sentence can be shorter (keep: runs on the ship or shore computer; about 1.9
  million rollouts for the slow vehicle, about 125 h on its own GPU; seconds on a desktop core).
- Repeated restatements of the same numbers between 5.3, 5.4 and the conclusion.

## 2. Precise fixes
1. Apart from the slow computer, the three moving strategies differ by at most 0.004 on the test
   years (moderate 0.003, fast 0.004, efficient 0.001), not "不超过0.003". This appears twice.
2. Conclusion, item 3: "30\%—38%" - the second percent sign is not escaped and comments out the
   rest of the line in LaTeX; write 38\%. Check every % in the files.
3. 5.4: "这证实……主要源于用规划用海洋上的自评得分衡量计算价值": the change moved both valuations
   (of planning more and of looking more) to the held-out oceans, and a single check does not
   "confirm". Write "表明……主要源于在同一批规划用海洋上既选航线又评价其价值" or similar.
4. 5.3 (last paragraph) and limitation (5): "由于任务间遗憾标准差（约0.13）远大于策略间的真实差异"
   is an explanation that was not tested. State only the observation: four imagined truths do not
   tell apart strategies whose real differences are 0.01 or less; the per-mission best in
   hindsight (0.243 on the moderate computer versus 0.265) shows the room left. The 0.13 spread
   may stay in the introduction as the reason why learning from past missions is hard.
5. The imagined-minus-real offset is "大致相同" for all strategies (0.05-0.07), not identical.
6. Chinese abstract, last sentence: "无需先验任务调参" should be "无需历史任务调参".
7. 1.2: the dates late April to early June come from Zhao et al.'s 2021 and 2023 records; either
   say so or keep only "晚春至初夏".

## Output
The five files, each preceded by a line "===== FILE: sections/<name>.tex =====": title, subtitle,
abstract, body, appendix.
