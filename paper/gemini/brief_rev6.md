# Revision 6: add two results to the finished paper (write only the pieces listed; do not touch anything else)

The attached section files are the current, checked paper (19 pages). Two new results must go in:

1. **What the counterexample search buys against random plausible fields.** The paper said the
   expected-time rule (32 random plausible fields) fails because "averaging symmetric random perturbations
   cannot single out the adverse field". That explanation is wrong and must go. The new experiment
   (facts_v4.md, section 随机合理场的数量与反例搜索) shows: the expected-time rule improves as the number of
   random plausible fields grows; with 32 fields it is significantly worse than the conservative choice
   after the search, and only from several hundred fields on is the difference no longer significant
   (test years: 1024 fields 0.71 h against 0.72 h; development years 0.88 h against 0.76 h), while the
   search uses about 71 route solves against 2048. With 32 fields the sampling error of the mean (2.4 h)
   is larger than the correction it tries to estimate (1.7 h), so its switches are mostly noise. For
   ranking risky missions the key is to measure how much could be lost: the expected regret over random
   fields holds about two thirds of the loss in its top 20% once there are enough fields (test 65% with
   32, 67% with 1024), close to the worst regret (67%), while the flip share stays at 44% even with 1024
   fields. So the search's advantage on a vehicle with little computation is that it reaches the right
   side with about 1/29 of the route solves; the regret criterion (size of the loss, not frequency of a
   flip) is what makes the ranking work. Report test-year numbers; mention the development years once. Also the finding about extra computation: on the test years it changed the
   choice on 64 missions, 38 for the better and 26 for the worse (this sentence is already in 6.3; keep it).
2. **Replication in a second region, the Gulf Stream** (facts_v4.md, section 换海区重复：湾流). Same
   product, depth, years and procedure; radius and thresholds calibrated on the Gulf Stream development
   years. The result is mixed and must be reported as it is:
   - replicates: more computation does not reduce wrong choices (18.5% cheap, 19.4% expensive; it changed
     22 choices, 8 for the better, 14 for the worse); almost every mission has a plausible counterexample
     (98.8%); the worst regret again ranks the risky missions (top 20% hold 71% of the loss; flip share
     49%); and the gate is the right trigger to observe: surfacing for today's 0.5-degree map only on
     flagged missions cuts the mean loss from 3.56 to 1.31 hours (interval excludes 0), better than
     always surfacing (1.53).
   - does not replicate: the conservative choice without observing (门控后取保守) does not help there
     (4.00 against 3.56 hours, interval contains 0). Reason (facts): in 8.7% of Gulf Stream missions one
     side is impassable in reality (1.0% in the Kuroshio); on such missions the plausible set contains a
     field that blocks either side, both worst regrets sit near the cap (e.g. 138.6 against 138.0 hours),
     and choosing the smaller one is close to a coin toss; 5 switches went into the side that was really
     impassable. A post-hoc check (state that it was done after seeing the test results, not specified in
     advance): switching only when the two worst regrets differ by more than the numerical tolerance gives
     3.45 hours (interval contains 0) in the Gulf Stream and keeps most of the gain in the Kuroshio (0.77).
   - meaning: the counterexample test tells reliably *when* the map cannot be trusted; observing is then
     the robust response; the observation-free conservative choice works only where the two sides' worst
     cases differ clearly. Say this plainly; it narrows the paper's claim about 门控后取保守.

## Pieces to write (output each one after its marker line, nothing else)

===== R1 =====
experiments.tex, Section 6.1, the first paragraph (it lists the questions the section answers). Add the
new question (what the search buys against random plausible fields) before the scope question, and say
the scope part now includes a second region. Keep the paragraph's style.

===== R2 =====
experiments.tex, Section 6.4, replace exactly this sentence (it is wrong):
"改用32个合理场的按期望时间准则或门控后按期望时间，与精算地图的配对差置信区间均包含0，说明对对称随机扰动求平均并不能挑出翻转决策的不利流场。"
with one sentence that keeps the first half (both expected-time variants are not significantly different
from the map) and points to the new subsection for the reason (too few random fields; see 6.6).

===== R3 =====
A new subsection to be placed after Section 6.5 (it becomes 6.6; the scope subsection becomes 6.7):
"\subsection{反例搜索省下了什么：与随机合理场的比较}" followed by two paragraphs (decision; ranking)
and a figure environment for fig_route_budget (\label{fig:budget}; width \linewidth). Paragraph rules
below apply. In the first paragraph also explain in one sentence why the conservative choice equals
choosing by the midpoint of the plausible range of the two-side time difference, so it only departs from
the map where one side's worst case is much worse than the other's (facts_v4.md, 推导与核对). The figure
caption: (a) mean loss against route solves per mission for the expected-time rule over n random plausible
fields (2n solves), the search as one point, the map as a reference line; (b) share of the map's loss held
by the top 20% of missions for the expected regret and the flip share over the same random fields, the
search's worst regret as one point, the map margin as a reference line; end with one sentence of takeaway.
No error bars are drawn; do not say there are.

===== R4 =====
experiments.tex, the scope subsection (now 6.7): its first sentence, plus a new paragraph on the Gulf
Stream placed after the existing paragraph and before the table (about 250-350 characters, at most six
numbers): what replicates, what does not, the reason, the post-hoc check (labelled as such), and the
meaning (point 2 above). The table (表\ref{tab:scope}) now has the Gulf Stream row and a new column
门控后上浮取图; the table file is attached.

===== R9 =====
innovation.tex, table row 4 (the line starting "4. 权衡最坏后悔与观测代价的门控响应"): rewrite cells 4
(证据) and 5 (局限) so that they include the Gulf Stream result (gated surfacing 3.56 → 1.31 hours there;
the conservative choice without observing fails there when both sides can be blocked). Keep cells 1-3.

===== R10 =====
experiments.tex, the limitations subsection (局限性讨论): the whole paragraph, adding a fifth point: the
observation-free conservative choice relies on the two sides' worst cases being clearly different; where
strong currents can block either side (Gulf Stream) it fails and the vehicle should observe instead.
Keep the four existing points.

===== R5 =====
abstract.tex: the whole file (Chinese abstract, keywords line, English title block, English abstract,
English keywords) with two additions: the efficiency result (the search reaches with about 71 route
solves what the expected-time rule needs about a thousand random plausible fields, about 2048 solves, to
reach) and the Gulf Stream replication stated honestly in one clause (the gate-then-surface response
replicates, 3.56 → 1.31 hours; the conservative choice without observing does not, because strong
currents can block either side). Chinese abstract at most 560 characters, English at most 270 words.
Keep the order already used (background, problem, gap, method, results, meaning).

===== R6 =====
intro.tex, the "本文的主要贡献如下" itemize (three items): add the efficiency number to item 2 and the
Gulf Stream replication to item 3, honestly (the gate and gated surfacing hold there; the
observation-free conservative choice does not). Keep "据我们所知，本文首次" in item 1 unchanged. Also the
last paragraph of intro.tex (the section road map) must now read: ...第6节给出实验结果、与随机合理场的比较、
适用范围与湾流重复实验... (rewrite that one paragraph too, after a line "===== R6b =====").

===== R7 =====
innovation.tex, table row 2 (the line starting "2. 基于包络定理梯度的合理反例主动搜索"): rewrite its
cells 2 (已有做法及其不足), 4 (证据) and 5 (局限) to reflect the new finding (the ensemble mean needs about
a thousand fields; the expected regret already ranks well, so the search's gain is in the side choice per
route solve). Keep cell 1 and cell 3 unchanged, keep the column count (5 cells, & separated, ending with \\).

===== R8 =====
conclusion.tex: the whole paragraph with one added clause for each new result (efficiency; Gulf Stream:
the gate and the gated surfacing hold, the observation-free conservative choice needs clearly different
worst cases). At most 470 characters.

## Rules (as in all earlier rounds)
- Every number must appear in facts_v4.md or facts_v3.md (attached). No number may be invented or rounded
  differently. At most about 6 numbers per paragraph; finding first, then the numbers that carry it.
- Terms exactly as in terms_v5.md. New terms: 随机合理场 (random plausible fields drawn from the same error
  model), 期望后悔 (the mean, over random plausible fields, of how much longer the map's side takes than the
  other side, counting 0 when it is faster), 翻转比例, 求解次数 (route solves).
- No English abbreviations in Chinese text; no emotive or inflated words (揪出、彻底、灾难、飙升、竟然、高达、
  仅仅、一眼、白白、毫无、有力证明); the first sentence of each paragraph states its conclusion; no "如图X所示"
  at the start of a paragraph.
- Do not claim more than the facts: the search does not beat a large ensemble on loss, it matches it with
  far fewer solves; the Gulf Stream result must be reported as it is.
- Keep every \label, \ref, \cite, equation and figure name as given. Refer to the new figure as
  图\ref{fig:budget} and to the scope table as 表\ref{tab:scope}.
