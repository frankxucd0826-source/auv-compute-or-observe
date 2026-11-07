# 与 Gemini 的对话记录 10：第 6 轮：补入随机合理场对照与湾流重复实验

时间（回复保存时间）：2026-11-06 19:40 UTC。调用方式：Claude 用命令行工具 ask-gemini 把下面“发送内容”作为附件发给 Gemini，并附一句简短指令（按附件中的写作要求完成各节）；回复原样存档后再由 Claude 核对数字与引用、拆分进论文各节。下面两部分都是原文，未作删改。

调用记录：

```
回答已存到 D:\海洋大数据\paper\gemini\rev6_reply.md
[gemini-4-argon-medium · gemini 格式 · 输入 21593 / 输出 3824 token · 40.9 秒]
```

本轮的写作要求见下方发送内容里的附件 `brief_rev6.md`。

## 发送内容

<details><summary>展开（共 40674 字符）</summary>

```
########## ATTACHED FILE: brief_rev6.md ##########

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


########## ATTACHED FILE: facts_v4.md ##########

# 事实清单 v4（第 6 轮新增；由 experiments/route_facts_rev6.py 从结果文件生成，新增文字中的数字只能取自这里或 facts_v3.md）

## 加算改变了哪些决定（黑潮主设置）
- 测试年份：把求解计算量从粗算增加 64 倍到精算，改变了 64 个任务的选择，其中 38 个改对、26 个改错。
- 开发年份：把求解计算量从粗算增加 64 倍到精算，改变了 75 个任务的选择，其中 51 个改对、24 个改错。

## 随机合理场的数量与反例搜索（黑潮主设置）
- 做法：每个任务另取 1024 个合理海流（与主实验同一误差模型、独立随机数），在标准网格上求两侧时间差；“按期望时间选边”用其中前 n 个的平均（每个合理场要求解左右两次，共 2n 次求解）。反例搜索后取保守（最坏后悔更小的一侧）用的是主实验的结果。
- 推导与核对：最坏后悔更小的一侧，等于按“合理集合给出的两侧时间差范围的中点”选边；若两侧时间差随海流线性变化，中点就是地图上的值，保守选择与照地图走相同，只有当一侧的最不利情形比另一侧严重得多时才改选。逐任务核对，二者完全一致。
- 测试年份（623 个任务）：照精算地图走 0.98 小时；反例搜索后取保守 0.72 小时（平均 71 次求解）；按期望时间选边，8 个合理场 1.71，16 个合理场 1.26，32 个合理场 0.99，64 个合理场 0.91，128 个合理场 0.82，256 个合理场 0.77，512 个合理场 0.79，1024 个合理场 0.71 小时。
  - 与反例搜索后取保守的配对差：32 个合理场 +0.26 [0.03, 0.52]；1024 个合理场 -0.02 [-0.11, 0.07]；从 128 个合理场起（及更多），区间都包含 0。
  - 1024 个合理场（2048 次求解）与精算地图之差 -0.27 [-0.51, -0.08]；反例搜索约 71 次求解，约为其 1/29。
  - 抽样噪声：32 个合理场平均值的抽样误差（中位数）2.4 小时，大于它要估计的修正量（1024 个合理场平均相对地图的修正，中位数）1.7 小时。
  - 风险排序（排前 20% 的任务所占的地图损失）：反例的最坏后悔 67%；同样的随机合理场算“坚持地图一侧的期望后悔”：32 个 65%，1024 个 67%；翻转比例：32 个 44%，1024 个 44%（主实验那 32 个 49%）；地图上两侧时间差 34%。
- 开发年份（710 个任务）：照精算地图走 1.13 小时；反例搜索后取保守 0.76 小时（平均 70 次求解）；按期望时间选边，8 个合理场 1.95，16 个合理场 1.44，32 个合理场 1.06，64 个合理场 0.92，128 个合理场 0.87，256 个合理场 0.94，512 个合理场 0.81，1024 个合理场 0.88 小时。
  - 与反例搜索后取保守的配对差：32 个合理场 +0.30 [0.13, 0.50]；1024 个合理场 +0.12 [-0.02, 0.31]；从 512 个合理场起（及更多），区间都包含 0。
  - 1024 个合理场（2048 次求解）与精算地图之差 -0.26 [-0.46, -0.08]；反例搜索约 70 次求解，约为其 1/29。
  - 抽样噪声：32 个合理场平均值的抽样误差（中位数）2.3 小时，大于它要估计的修正量（1024 个合理场平均相对地图的修正，中位数）1.6 小时。
  - 风险排序（排前 20% 的任务所占的地图损失）：反例的最坏后悔 65%；同样的随机合理场算“坚持地图一侧的期望后悔”：32 个 58%，1024 个 65%；翻转比例：32 个 50%，1024 个 47%（主实验那 32 个 50%）；地图上两侧时间差 48%。
- 读法：选哪一侧时，随机合理场的平均要上千个才估得准，反例搜索以约 1/29 的求解次数达到同样效果；判断哪些任务危险时，关键是度量“会损失多少”而不是“有多少合理场翻转”，期望后悔（合理场足够多时）与最坏后悔都能抓住约三分之二的损失，翻转比例即使用 1024 个合理场也只有四成多。

## 换海区重复：湾流（33–41°N、75–67°W；同一 HYCOM 产品与深度，同一时间范围与年份划分，同一流程；半径与阈值用湾流自己的开发年份标定）
- 任务：开发年份 724 个（364 天），测试年份 643 个（324 天）；更快一侧平均航时 39.9 小时。
- 3 天前 1° 粗图的误差：典型误差中位数 0.27 米/秒，相关长度 76 千米。
- 标定：半径 r = 1.75（开发年份覆盖 93%，测试年份 91%）；数值误差容限 6.6 小时；保守门控阈值 12 小时，上浮取 0.5° 图门控阈值 12 小时。
- 选错一侧：粗算 18.5%，精算 19.4%（加算改变 22 个任务的选择：8 个改对、14 个改错）；换成当天 0.5° 图 8.4%。
- 存在合理反例的任务：98.8%。
- 地图+粗算：平均损失 3.64 小时；与精算地图之差 +0.08 [-0.36, 0.68]
- 地图+精算：平均损失 3.56 小时；与精算地图之差 +0.00 [0.00, 0.00]
- 集合期望（贝叶斯）：平均损失 4.36 小时；与精算地图之差 +0.80 [-0.38, 2.04]
- 保守（最坏后悔最小）：平均损失 4.10 小时；与精算地图之差 +0.54 [-0.75, 1.88]
- 反例门控→保守：平均损失 4.00 小时；与精算地图之差 +0.45 [-0.83, 1.77]
- 总是沿途测30km：平均损失 3.63 小时；与精算地图之差 +0.07 [-1.47, 1.46]
- 总是沿途测60km：平均损失 3.85 小时；与精算地图之差 +0.29 [-1.21, 1.77]
- 总是上浮取当天0.5°图：平均损失 1.53 小时；与精算地图之差 -2.03 [-3.35, -0.81]
- 反例门控→上浮取0.5°图：平均损失 1.31 小时；与精算地图之差 -2.25 [-3.58, -1.04]
- 门控后取保守比精算地图多损失 13%（3.56 → 4.00 小时）。
- 风险排序（排前 20% 的任务所占的地图损失）：反例的最坏后悔 71%，32 个合理场的期望后悔 68%，32 个合理场的翻转比例 49%，地图上两侧时间差 47%。
- 门控标记 66% 的任务，占地图损失的 95%。
- 真实海流中有一侧过不去（顶流过强）的任务：湾流测试年份 8.7%，黑潮测试年份 1.0%。
- 门控后取保守改选的 55 个任务中 25 个改对（平均省 30.7 小时），30 个改错（平均多花 35.1 小时），其中 5 次改到了真实海流中过不去的一侧。这类任务里两侧的最坏后悔都因“合理集合中存在把该侧堵死的海流”而接近上限（代价最大的一次：地图一侧 138.6、另一侧 138.0 小时，改选后多花 170.9 小时），选“最坏后悔更小的一侧”近于随机。
- 事后检验（看过测试结果后才做，非预先设定）：若只在两侧最坏后悔之差超过数值误差容限（3.2 小时）时才改选，黑潮测试年份损失 0.77 小时，与精算地图之差 -0.21 [-0.39, -0.05]。
- 事后检验（看过测试结果后才做，非预先设定）：若只在两侧最坏后悔之差超过数值误差容限（6.6 小时）时才改选，湾流测试年份损失 3.45 小时，与精算地图之差 -0.11 [-0.43, 0.20]。



########## ATTACHED FILE: facts_v3.md ##########

# 事实清单 v3（航路决策研究；由 experiments/route_facts.py 从结果文件生成，正文所有数字只能取自这里）

## 数据与设置
- 海流数据：HYCOM 全球海洋再分析（GLBy0.08，实验 93.0），水平分辨率 1/12°，取 10 米深度的海流，区域 23–31°N、121–129°E（台湾以东至东海，含黑潮），2019-01-01 至 2024-08-29 每 3 天一张（12:00 UTC），共 689 张；开发年份 2019–2021 共 365 张，测试年份 2022–2024 共 324 张。
- 任务：每张快照抽 2 个任务；起终点相距 100–140 千米，中点有半径 15 千米的禁航区，左右两侧各求最快航线；起终点离岸至少 20 千米；只取粗图上任务区平均流速不低于 0.3 米/秒的强流任务。开发年份 710 个任务（357 天），测试年份 623 个任务（313 天）。
- 航行器：对水速度 1.0 米/秒（长航程自主水下航行器量级）；更快一侧的平均航时 39.2 小时（测试年份）。
- 航行器带的地图：1° 粗分辨率（格内平均），3 天前制作（主设置）。真实海流：当天 1/12° 场。
- 航线求解（三档计算量）：粗算 8 千米网格、8 个方向；标准 4 千米、16 个方向；精算 2 千米、32 个方向（相对计算量 1 : 8 : 64，按边数）。最快航线用图上的最短路（Dijkstra）求，过一条边的时间 = 边长 / 对地速度，对地速度 = 沿边流速 + sqrt(V² − 垂直边流速²)；顶流过强则该边不可通行。
- 执行假设：选定一侧后，航行器按真实海流在该侧以最优方式航行（贴近实际的边走边测、边调整）；本文研究的是选哪一侧这个二元决策。
- 误差模型（大数据标定，开发年份）：旧粗图减真实海流的误差，3 天前 1° 粗图：典型误差中位数 0.17 米/秒，相关长度 76 千米；当天 0.5° 图：0.07 米/秒，18 千米。合理海流 = 粗图 + 由流函数生成的无散误差模态的组合（各点方差按标定的误差图缩放），系数服从标准正态。
- 合理集合的半径在开发年份标定：使合理集合给出的两侧时间差范围包住真实差值的任务比例不低于 90% 的最小半径，得 r = 1.5；该半径下开发年份覆盖 93%，测试年份覆盖 94%。
- 反例搜索：在半径 r 的球内对“两侧时间差”做投影梯度上升（梯度由最快航线上各段时间对海流的导数给出，即包络定理），先沿梯度跳到球面，再步长减半细化；分别朝两个方向、在半径 1 与 2 上各搜一次，其他半径按两者线性插值；每个任务共约 71 次标准网格航线求解，与 32 个成员的集合（64 次）相近。
- 数值误差容限（开发年份）：粗算与精算两侧时间差之差的 95% 分位 3.2 小时；粗算差值小于它时改用精算（按需精算）。
- 门控阈值（开发年份按平均损失最小选定，测试年份原样使用）：最坏后悔超过 8 小时时取保守一侧；最坏后悔超过 8 小时时上浮取当天 0.5° 图（上浮一次计 1 小时）。
- 观测方式：原地停留 2 小时测 12 次；沿所选一侧航行 30 或 60 千米并连续测流后再决定是否换边；绕到反例与地图差别最大处（前方 40 千米内）去测；上浮取当天 1° 或 0.5° 图（每次 1 小时）。测流噪声 0.05 米/秒，同化时取 0.15 米/秒（含模型误差）。
- 统计：损失 = 实际航时 − 更快一侧的航时（小时）；95% 区间按天整组重抽样 2000 次。

## 主要结果（测试年份，括号内为 95% 区间；与“照精算地图走”的配对差）
- 地图+粗算：平均损失 1.16 小时 [0.80, 1.60]；与精算地图之差 +0.18 [-0.14, 0.58]
- 地图+标准：平均损失 1.03 小时 [0.73, 1.38]；与精算地图之差 +0.05 [-0.05, 0.18]
- 地图+精算：平均损失 0.98 小时 [0.69, 1.33]；与精算地图之差 +0.00 [0.00, 0.00]
- 集合期望（贝叶斯）：平均损失 1.04 小时 [0.76, 1.37]；与精算地图之差 +0.06 [-0.22, 0.34]
- 保守（最坏后悔最小）：平均损失 0.72 小时 [0.50, 0.99]；与精算地图之差 -0.26 [-0.49, -0.05]
- 原地停留测：平均损失 2.91 小时 [2.67, 3.19]；与精算地图之差 +1.94 [1.55, 2.31]
- 总是沿途测30km：平均损失 0.93 小时 [0.69, 1.21]；与精算地图之差 -0.05 [-0.30, 0.18]
- 总是沿途测60km：平均损失 0.91 小时 [0.66, 1.22]；与精算地图之差 -0.07 [-0.27, 0.05]
- 总是绕行定点测：平均损失 12.43 小时 [11.50, 13.45]；与精算地图之差 +11.45 [10.49, 12.46]
- 总是上浮取当天1°图：平均损失 1.67 小时 [1.49, 1.89]；与精算地图之差 +0.69 [0.40, 0.96]
- 总是上浮取当天0.5°图：平均损失 1.22 小时 [1.14, 1.31]；与精算地图之差 +0.24 [-0.11, 0.53]
- 反例门控→保守：平均损失 0.70 小时 [0.48, 0.97]；与精算地图之差 -0.28 [-0.51, -0.07]
- 反例门控→上浮取0.5°图：平均损失 0.78 小时 [0.69, 0.89]；与精算地图之差 -0.20 [-0.54, 0.08]
- 反例门控→贝叶斯：平均损失 0.96 小时 [0.68, 1.29]；与精算地图之差 -0.01 [-0.29, 0.25]
- 开发年份对应：精算地图 1.13，保守 0.76，门控后取保守 0.70，门控后上浮取 0.5° 图 0.76，集合期望 0.96。
- 门控后取保守比精算地图少损失 28%（0.98 → 0.70 小时）。

## 歧义的性质（测试年份；开发年份在括号内）
- 选错一侧的比例：粗算 21.7%（25.1%），精算 19.7%（21.3%）；换成当天 0.5° 图 10.4%；计算量增加 64 倍只修好粗算错误的 28%。
- 平均损失：粗算 1.16，精算 0.98 小时（差异不显著，见上）。
- 能找到合理反例（存在使地图所选一侧变差、且让另一侧更好的合理海流）的任务比例，按半径：r=0.25：41.6%，r=0.5：64.8%，r=1.0：94.1%，r=1.5：99.7%，r=2.0：100.0%。
- 损失高度集中：精算地图损失最大的 10% 任务占全部损失的 92%（开发年份 88%）。
- 按风险排序，排在前 20% 的任务所占的地图损失：反例的最坏后悔 67%，32 个合理场中翻转的比例 49%，地图上两侧时间差越小越危险 34%，随机 20%，按真实损失（上限）100%。
- 门控（最坏后悔 > 8 小时）标记 47% 的任务，这些任务占地图损失的 82%；其中保守规则改选另一侧的有 41 个任务。
- 门控后取保守为何有效：改选的 41 个任务中 23 个改对，改对时平均省 10.1 小时；18 个改错，改错时平均多花 3.3 小时——被避开的一侧往往有很大的下行风险，改对的收益远大于改错的代价。
- 只论“是否选错且多花 1 小时以上”（测试年份 79 个）而不论多花多少时，三种排序的区分能力相近（曲线下面积：反例 0.65，32 成员集合 0.67，地图差值 0.67）；反例的优势在于把损失大的任务排在前面（见上一条）。

## 观测的代价（测试年份）
- 上浮一次 0.0 小时：总是上浮取 0.5° 图 0.22，门控后上浮 0.22，门控后取保守 0.70，精算地图 0.98（小时）。
- 上浮一次 0.5 小时：总是上浮取 0.5° 图 0.72，门控后上浮 0.55，门控后取保守 0.70，精算地图 0.98（小时）。
- 上浮一次 1.0 小时：总是上浮取 0.5° 图 1.22，门控后上浮 0.78，门控后取保守 0.70，精算地图 0.98（小时）。
- 上浮一次 2.0 小时：总是上浮取 0.5° 图 2.22，门控后上浮 1.06，门控后取保守 0.70，精算地图 0.98（小时）。
- 上浮一次 3.0 小时：总是上浮取 0.5° 图 3.22，门控后上浮 0.98，门控后取保守 0.70，精算地图 0.98（小时）。
- 沿途测 30 千米后换边的任务 3.4%，换对 81%；测 60 千米后换边 18.8%，换对 15%。
- 绕行定点测平均先花 15.4 小时到测点。

## 示例任务（图 1；按规则选出：测试年份按日期第一个满足“精算地图选错且多花 3 小时以上、存在合理反例、门控后保守选对”的任务）
- 日期 2022-01-18；粗图上左侧 37.71 小时、右侧 38.02 小时（地图选左）；合理反例中左侧 55.69、右侧 44.07；真实海洋左侧 53.44、右侧 41.72（右侧快 11.7 小时）。

## 前期研究（东海赤潮巡测：航行器带 3 天前的卫星叶绿素图，在“继续计算”“边走边测”“停下复测”之间分配时间；损失为对数叶绿素浓度）
- 规划器在自己搜索过的想象海洋上给航线打分，随推演次数增加而虚高：64、2000、20 万次推演时自评 0.762、0.833、0.917，真实价值 0.749、0.793、0.803，在不参与搜索的留出海洋上评判 0.745、0.794、0.802。
- 出发前预演选用时策略的遗憾 0.265，每个任务事后挑最好的策略 0.243（用时分配本身的空间约 0.022），经典单步元推理 0.287。
- 遗憾拆解：从窗口边缘下水（离最浓处中位数 48 千米）时，知道真相直奔最浓处 0.206，换成当天卫星图 0.235；改在旧图最浓处下水后，五种用时策略 0.126–0.145，换成当天卫星图 0.098。即下水点约 0.13、信息新鲜度约 0.03、用时分配约 0.02。
- 用前一天的移动（光流）把旧图外推 3 天，比直接用旧图误差大 0.018（95% 区间 0.012–0.025）：逐日卫星图里没有可外推的整体移动。

## 适用范围（每组测试年份约 350 个任务；阈值各自在开发年份标定）
- 主设置：3 天前 1° 粗图，对水 1.0 米/秒：测试任务 623，标定半径 1.5，精算地图选错 19.7%，粗算选错 21.7%，精算地图损失 0.98，门控后取保守 0.70，门控后取保守与地图之差 -0.28 [-0.51, -0.07]，门控后上浮取图 0.78，存在合理反例 99.7%，反例前20%所占损失 67%，平均最快航时 39.2
- 地图较好：当天 0.5° 图：测试任务 349，标定半径 1.75，精算地图选错 8.0%，粗算选错 8.9%，精算地图损失 0.17，门控后取保守 0.17，门控后取保守与地图之差 +0.00 [-0.04, 0.05]，门控后上浮取图 0.16，存在合理反例 64.5%，反例前20%所占损失 60%，平均最快航时 38.7
- 慢速航行器：对水 0.75 米/秒：测试任务 347，标定半径 1.5，精算地图选错 18.4%，粗算选错 22.2%，精算地图损失 2.43，门控后取保守 1.80，门控后取保守与地图之差 -0.63 [-1.67, 0.30]，门控后上浮取图 1.32，存在合理反例 99.1%，反例前20%所占损失 74%，平均最快航时 59.8
- 消融：合理集合改用历史相似日的小尺度差：测试任务 349，标定半径 1.5，精算地图选错 19.5%，粗算选错 22.3%，精算地图损失 0.99，门控后取保守 0.95，门控后取保守与地图之差 -0.04 [-0.43, 0.36]，门控后上浮取图 0.77，存在合理反例 99.4%，反例前20%所占损失 64%，平均最快航时 39.8



########## ATTACHED FILE: terms_v5.md ##########

# 术语表（v5，航路决策研究）——正文、图注、表格必须与此一致；中文里不出现英文缩写

| 写法 | 含义 |
|---|---|
| 自主水下航行器（首次出现后可称“航行器”） | 研究对象；不写 AUV |
| 粗图 | 航行器所带的 3 天前 1° 粗分辨率海流图（格内平均） |
| 真实海流 / 真实海洋 | 当天 1/12° 再分析海流场 |
| 禁航区；左侧、右侧 | 起终点中间半径 15 千米的圆形禁航区；从它的左边或右边绕过 |
| 两侧时间差 | 左侧航时减右侧航时（小时）；为负则左侧快 |
| 粗算、标准、精算 | 三档航线求解计算量（8 千米 8 向、4 千米 16 向、2 千米 32 向） |
| 数值歧义 | 两侧时间差小于求解误差，加大计算量可以消除 |
| 环境歧义 | 存在与现有信息同样相容、却要求选另一侧的海流场，计算消除不了 |
| 合理海流、合理集合、半径 | 粗图加上按多年数据标定的误差模态组合；组合系数范数不超过半径 r 的全部海流场 |
| 合理反例 | 合理集合中让地图所选一侧变差、另一侧更好的海流场 |
| 反例检验 | 在合理集合中搜索最坏的合理反例的过程 |
| 最坏后悔 | 合理集合中，所选一侧比另一侧多花时间的最大值（小时） |
| 门控 | 以最坏后悔是否超过阈值决定是否采取观测或保守动作 |
| 照地图走（精算） | 基线：在粗图上用精算选更快一侧 |
| 按需精算 | 粗算差值小于数值误差容限时改用精算 |
| 按期望时间 | 选 32 个合理海流中平均航时更短的一侧 |
| 保守（最坏后悔最小） | 选合理集合中最坏后悔更小的一侧 |
| 原地停留测、沿途测 30 千米、沿途测 60 千米、绕行定点测、上浮取当天 1° 图、上浮取当天 0.5° 图 | 各种观测方式（见表 1） |
| 门控后取保守、门控后上浮取图 | 本文的两种响应 |
| 知道真相 | 仅作参考的上限：直接选真实更快的一侧 |
| 损失 | 实际航时减去更快一侧的航时（小时），越低越好 |
| 前期研究里的词 | 想象海洋、留出海洋、自评、出发前预演、遗憾（对数叶绿素浓度） |
| 单位 | 千米、米/秒、小时（与图一致） |


########## ATTACHED FILE: tables/route_scope.tex (generated by the script; includes the Gulf Stream row) ##########

\begin{tabular}{@{}p{0.21\linewidth}>{\centering\arraybackslash}p{0.080\linewidth}>{\centering\arraybackslash}p{0.080\linewidth}>{\centering\arraybackslash}p{0.080\linewidth}>{\centering\arraybackslash}p{0.080\linewidth}>{\centering\arraybackslash}p{0.080\linewidth}>{\centering\arraybackslash}p{0.080\linewidth}>{\centering\arraybackslash}p{0.080\linewidth}@{}}
\toprule
设置 & 测试任务 & 存在合理反例 & 精算地图选错 & 精算地图损失（小时） & 门控后取保守（小时） & 门控后上浮取图（小时） & 反例排前 20\% 的任务所占损失 \\
\midrule
主设置：3 天前 1° 粗图，对水 1.0 米/秒 & 623 & 99.7\% & 19.7\% & 0.98 & 0.70 & 0.78 & 67\% \\
地图较好：当天 0.5° 图 & 349 & 64.5\% & 8.0\% & 0.17 & 0.17 & 0.16 & 60\% \\
慢速航行器：对水 0.75 米/秒 & 347 & 99.1\% & 18.4\% & 2.43 & 1.80 & 1.32 & 74\% \\
消融：合理集合改用历史相似日的小尺度差 & 349 & 99.4\% & 19.5\% & 0.99 & 0.95 & 0.77 & 64\% \\
换海区：湾流（33°–41°N、75°–67°W），其余同主设置 & 643 & 98.8\% & 19.4\% & 3.56 & 4.00 & 1.31 & 71\% \\
\bottomrule
\end{tabular}


########## ATTACHED FILE: sections/abstract.tex (current, checked text) ##########

{\heiti 摘要：}
随着海洋大数据的计算引擎延伸至移动观测平台边缘，自主水下航行器在受限算力与能量下必须在继续计算、补充观测与立即行动之间做出在线权衡。在台湾以东至东海的黑潮强流区，当航行器携带3天前的粗分辨率海流图绕越禁航区时，选错绕行一侧将导致数小时航时损失。现有确定性规划通过加密网格增加计算，只能提升求解精度而无法补充缺失的海洋信息；集合规划与自适应采样或因样本有限漏掉翻转决策的流场，或将观测耗费在与二元选边无关的全场重构上。为此，本文提出基于海洋大数据标定的合理反例检验方法，分离数值歧义与环境歧义以决定何时计算、何时观测、何时保守绕行。该方法先通过粗精网格容限按需精算以消除数值歧义，再用多年再分析海流标定旧粗图的无散误差模态与合理集合半径，利用包络定理投影梯度上升搜索使所选一侧变差、另一侧变好的合理反例及最坏后悔，据此门控触发上浮取图或选最坏后悔更小的一侧。六年黑潮再分析数据实验表明：计算量增加64倍仅将选错率从21.7\%降至19.7\%，而在覆盖94\%真实时间差的合理集合内99.7\%的任务存在合理反例；最坏后悔前20\%的任务集中了67\%的损失，门控后取保守将平均损失从0.98小时降至0.70小时（降低28\%），并在上浮代价低于约1小时时触发上浮取新图。

{\heiti 关键词：}海洋大数据；自主水下航行器；航路规划；合理反例检验；元推理；不确定性量化

\vspace{1em}
\begin{center}
{\large\bfseries Plausible Counterexample Test: When an Autonomous Underwater Vehicle Should Compute and When It Should Observe Under a Coarse Current Map}
\end{center}
\vspace{0.5em}

{\bfseries Abstract:}
As the computing engine of ocean big data extends to the edge of mobile platforms, an autonomous underwater vehicle under limited onboard computation and energy must trade off online among continued computation, additional observation, and immediate movement. In the Kuroshio region east of Taiwan and the East China Sea, when a vehicle navigates around a no-go zone carrying a three-day-old coarse current map, choosing the wrong side costs hours of transit time. Deterministic planning refines the search grid on the best-estimate map, sharpening numerical precision without supplying missing oceanographic information, while ensemble planning and adaptive sampling either miss decision-flipping flows due to finite samples or spend observations reconstructing the whole field rather than resolving the binary route choice. We propose a plausible counterexample test calibrated by ocean big data that separates numerical ambiguity from environmental ambiguity to decide when to compute, observe, or hedge conservatively. The method resolves numerical ambiguity via an on-demand fine solve, calibrates divergence-free error modes and a plausible-set radius from multi-year reanalysis currents, and uses envelope-theorem projected gradient ascent within the plausible ball to find the worst counterexample and its worst regret, gating between surfacing for a new map and choosing the side with smaller worst regret. Across six years of Kuroshio reanalysis data, 64-fold more computation cuts wrong-side choices only from 21.7\% to 19.7\%, whereas 99.7\% of missions admit a plausible counterexample inside the calibrated set covering 94\% of real time differences; the top 20\% of missions by worst regret hold 67\% of total loss, and gated conservative routing lowers mean loss by 28\% from 0.98 to 0.70 hours while triggering surfacing when communication costs under about 1 hour.

{\bfseries Keywords:} ocean big data; autonomous underwater vehicle; path planning; plausible counterexample test; metareasoning; uncertainty quantification


########## ATTACHED FILE: sections/intro.tex (current, checked text) ##########

\section{引言}

海洋大数据的计算引擎正从岸基超算中心向移动观测平台边缘延伸，使“继续计算、补充观测还是立即行动”成为自主水下航行器必须面对的在线决策问题。传统流程依赖岸基中心汇集卫星与模式产品并下发指令\cite{chassignet2007hycom,chin2017mur}，但水下声学通信带宽极窄且上浮卫星通信耗时耗能，长航程航行器必须依靠低功耗机载计算模块独立完成环境推演与重规划\cite{remus100,jetsonorinnx}。由于机载算力与电池能量受限，航行器既不能无限制地进行高分辨率搜索，也不能频繁中断航行去原位测流或上浮通信\cite{horvitz1987reasoning,russell1991right}。如何在计算、观测与行动之间分配资源，构成了海洋边缘智能的核心挑战\cite{sung2021quit,magnino2026metareasoning}。

在台湾以东至东海的黑潮强流区，当航行器携带数天前下发的粗分辨率海流图执行绕障航行时，选错绕行方向将导致数小时的航时损失。长航程航行器对水巡航速度约为1.0米/秒，与黑潮主轴及邻近涡旋流速相当。在相距百余千米的起终点之间绕越禁航区时，从左侧或右侧绕行是不可逆的二元拓扑决策：一旦驶入逆流一侧，不仅航时大增，还可能因顶流过强而无法通行。本文考虑航行器只携带3天前制作的1°粗分辨率海流图（简称粗图）的情形：该图既丢失了中尺度锋面与涡旋切变，又包含数天内流轴摆动的时效误差，极易误导左右选边。

面对粗图上的航路决策，常规做法是在当前海流图上投入更多算力以加密网格与航向离散度\cite{lolla2014levelset}，但当环境信息本身缺失时，这种确定性等价做法难以奏效。若左右两侧在粗网格上的预计航时接近，规划器会自然地细分网格以分辨快慢。然而，这混淆了求解器粗糙与海洋环境不确定性：加密网格只能减少同一张粗图上的离散误差，却不能提供任何关于真实涡旋位置的新信息\cite{jiang2015horizon,cuadron2025overthinking}。正如第3节前期赤潮巡测研究所示，当背景场陈旧时，成百上千倍地增加机载推演只会使规划器在想象模型上的自评不断虚高，而航线在真实海洋中的价值早已饱和\cite{smith2006curse}。

第二种常见路径是利用集合预报开展风险感知航路规划，但现有方法不仅无法回答何时应停止计算或去观测，还容易因有限抽样漏掉翻转决策的流场\cite{wang2016path,subramani2018stochastic,kularatne2018forecast}。集合规划通过在数十个扰动流场中评估平均航时或翻转比例来折中选路，但将不确定性视为静态输入，缺乏在计算与观测之间切换的元推理机制\cite{lin2015metareasoning,elboher2023formal}。进一步而言，集合给出的翻转比例只反映有多少成员翻转了决定，而不反映翻转后损失有多大，因而难以区分“翻转后多花半小时”与“翻转后多花十几个小时”的任务，容易低估选错一侧的尾部风险\cite{benhaim2006infogap,marx2020predictive}。

第三种路径是基于信息价值的自适应采样，即主动前往不确定性最高的海区测量，但对整个海流场有价值的信息并不等同于对左右选边有价值的信息\cite{fossum2019,hollinger2014sampling}。传统自适应采样以降低全场估计方差或最大化互信息为目标\cite{srinivas2012gpucb}；然而在绕障任务中，若禁航区外某处的误差对左右航时影响相同，测量它便徒耗航时；反之，顺路在起点附近测流虽代价低廉，若决定两侧快慢的关键切变远在数十千米之外，近处测量也无法改变决策。序贯实验设计与模型判别理论指出，真正决定是否需要新信息的，是在现有证据下能否找到与当前观测同样相容、却要求采取相反行动的竞争模型\cite{chernoff1959sequential,box1967discrimination,garivier2016optimal,attia2018goal}。

为此，本文提出“合理反例检验”：机载计算与现场观测消除的是两类不同性质的不确定性；当两侧难分伯仲是因为求解网格粗糙（数值歧义）时，多算即可做对决定；而当存在与粗图同样相容、却使另一侧明显更快的合理海流（环境歧义）时，继续计算无法分辨真伪，唯有引入新观测才能消解，且在观测过贵时应直接选择最坏后悔更小的一侧。我们将这一判别转化为操作问题：针对粗图推荐的一侧，能否在多年海洋大数据标定的合理集合内搜出使另一侧更快、且让当前选择付出沉重代价的合理反例？在图\ref{fig:overview}所示的2022年1月18日测试任务示例中，粗图上两侧只差约0.3小时且地图推荐左侧，继续加密网格只会把这一账面差值算得更细，而合理反例检验在合理集合内搜出了使左侧明显变慢、右侧更快的物理相容流场，预示了真实海洋中右侧快11.7小时的结果，并据此触发门控决策。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_overview}
\caption{粗分辨率海流图下的航路决策与合理反例检验（2022年1月18日任务示例）。(a) 航行器携带的3天前1°粗图，左侧航时37.7小时、右侧38.0小时，地图选左侧；(b) 在大数据标定的合理集合内搜出的合理反例海流，左侧55.7小时、右侧44.1小时；(c) 当天1/12°真实海流，左侧53.4小时、右侧41.7小时，右侧实际快11.7小时；(d) 本文决策流程：先校验粗图两侧时间差是否小于数值误差容限以决定是否按需精算，再通过反例检验计算最坏后悔，最坏后悔小则照地图走，大则在观测便宜时上浮取新图、观测昂贵时改选最坏后悔更小的保守一侧。再多的机载计算也只能把粗图上的0.3小时差值算准，唯有合理反例检验能显式找出(b)(c)这类同样合理却翻转决策的海洋状态。}
\label{fig:overview}
\end{figure}

本文的主要贡献如下：
\begin{itemize}
    \item \textbf{概念与判别准则创新：}据我们所知，本文首次在自主水下航行器航路决策中分离了可由计算消除的“数值歧义”与需靠新信息或保守决策应对的“环境歧义”，提出以最坏合理后悔为核心判据的合理反例检验框架，明确了边缘计算与海洋观测的功能边界。
    \item \textbf{大数据标定与高效反例搜索：}利用多年再分析海流标定旧粗图的无散流函数误差模态及覆盖90\%以上真实时间差的合理集合半径，结合包络定理梯度与球面投影搜索，以约71次标准网格求解直接定位最坏后悔流场。
    \item \textbf{黑潮强流区系统实证：}在六年黑潮再分析海流共1333个任务上的实验表明，64倍算力仅修复28\%的粗算错误，而99.7\%的任务存在合理反例；最坏后悔前20\%的任务集中了67\%的损失，门控后取保守将平均航时损失降低28\%，并给出了原位测流与上浮取图的收益边界。
\end{itemize}

本文其余部分组织如下：第2节回顾相关工作；第3节简述前期赤潮巡测研究；第4节建立绕障航路决策模型；第5节详述合理反例检验与门控方法；第6节给出实验结果与适用范围；第7节拆解创新点与研究脉络；第8节总结全文。


########## ATTACHED FILE: sections/method.tex (current, checked text) ##########

\section{方法}

本文提出如图\ref{fig:overview}(d)所示的四步决策方法：先通过按需精算消除数值歧义，再在多年海洋大数据标定的合理集合内用投影梯度上升搜索最坏合理反例，最后依据最坏后悔执行门控分流。

\subsection{按需精算：数值歧义的快速识别与消除}
区分求解器误差与环境不确定性的首要原则，是仅当粗算时间差落在数值离散误差容限之内时才动用精算。常规确定性规划要么一律使用粗算而在两侧航时接近时受网格锯齿误导，要么对所有任务一律执行耗时64倍的精算，在粗图上两侧本就相差十几个小时的任务上浪费算力。

我们在开发年份任务上离线对比同一张粗图 $\boldsymbol{u}_0$ 的粗算时间差 $\Delta T_{\text{coarse}}(\boldsymbol{u}_0)$ 与精算时间差 $\Delta T_{\text{fine}}(\boldsymbol{u}_0)$，取绝对偏差 $|\Delta T_{\text{coarse}}(\boldsymbol{u}_0) - \Delta T_{\text{fine}}(\boldsymbol{u}_0)|$ 的95\%分位数作为数值误差容限 $\tau_{\text{num}} = 3.2$ 小时。在线执行时，航行器先用粗算求 $\Delta T_{\text{coarse}}(\boldsymbol{u}_0)$；若 $|\Delta T_{\text{coarse}}(\boldsymbol{u}_0)| \ge \tau_{\text{num}}$，直接采纳粗算结果；仅当 $|\Delta T_{\text{coarse}}(\boldsymbol{u}_0)| < \tau_{\text{num}}$ 时才判定存在数值歧义并触发精算，以很小的平均算力确保地图基准选择 $s_0$ 不受求解器粗糙度误导。

\subsection{反例检验：基于包络定理的合理集合投影梯度搜索}
判断粗图所选一侧 $s_0$ 是否面临严重环境歧义，最直接的准则是主动在合理集合 $\mathcal{U}(r)$ 内寻找使 $s_0$ 相比另一侧 $\bar{s}_0$ 尽可能变慢的最坏合理反例，而非在少数随机样本上求平均。现有集合规划通常随机抽取32个流场样本统计航时均值或翻转比例\cite{wang2016path}；然而，翻转比例只反映有多少样本翻转了决定，不反映翻转后损失有多大；而两侧时间差只对少数扰动方向敏感，随机样本要很多才能把这些方向上的效应估准（第6.6节）。

我们将反例检验构建为合理球域上的约束最大化问题。定义流场 $\boldsymbol{u}(\boldsymbol{z}) \in \mathcal{U}(r)$ 下选用一侧 $s$ 的“最坏后悔”为该侧航时超出另一侧 $\bar{s}$ 的最大值 $R_s(r)$：
\begin{equation}
R_s(r) = \max_{\|\boldsymbol{z}\|_2 \le r} J_s(\boldsymbol{z}), \qquad J_s(\boldsymbol{z}) = \max\left\{ 0,\, T_s(\boldsymbol{u}(\boldsymbol{z})) - T_{\bar{s}}(\boldsymbol{u}(\boldsymbol{z})) \right\}.
\label{eq:worst_regret}
\end{equation}
当 $R_{s_0}(r) > 0$ 时，即存在使另一侧 $\bar{s}_0$ 更快的合理反例，且 $R_{s_0}(r)$ 给出了坚持选 $s_0$ 可能多付出的最大航时。

由于 $T_{\text{L}}(\boldsymbol{u}(\boldsymbol{z})) - T_{\text{R}}(\boldsymbol{u}(\boldsymbol{z}))$ 嵌套了图最短路算子，对每个系数 $z_k$ 做有限差分每次迭代需 $2K$ 次最短路求解。本文利用最优化中的包络定理（Danskin定理）避免了这一开销：当流场微小扰动时，最短路径 $P_s^*(\boldsymbol{z})$ 的节点序列在一阶近似下不变，因此最优航时 $T_s(\boldsymbol{u}(\boldsymbol{z}))$ 对系数 $\boldsymbol{z}$ 的梯度，等于沿当前最快航线 $P_s^*(\boldsymbol{z})$ 将各边通行时间 $t(e)$ 对局部流速的偏导数直接累加：
\begin{equation}
\frac{\partial T_s}{\partial z_k} = \sum_{e \in P_s^*(\boldsymbol{z})} \left( \frac{\partial t(e)}{\partial u_{\parallel}} \boldsymbol{d}_e + \frac{\partial t(e)}{\partial u_{\perp}} \boldsymbol{n}_e \right) \cdot \frac{\boldsymbol{m}_k(\boldsymbol{x}_e^{-}) + \boldsymbol{m}_k(\boldsymbol{x}_e^{+})}{2},
\label{eq:envelope_grad}
\end{equation}
其中 $\boldsymbol{x}_e^{-}$、$\boldsymbol{x}_e^{+}$ 为有向边 $e$ 的两端节点，$\boldsymbol{n}_e$ 为垂直边方向的单位向量，$\boldsymbol{m}_k$ 为式(\ref{eq:plausible_field})中的误差模态，标量导数由式(\ref{eq:edge_time})解析给出：
\begin{equation}
\frac{\partial t(e)}{\partial u_{\parallel}} = -\frac{\ell_e}{v_{\text{g}}(e)^2}, \qquad \frac{\partial t(e)}{\partial u_{\perp}} = \frac{\ell_e u_{\perp}}{v_{\text{g}}(e)^2 \sqrt{V^2 - u_{\perp}^2}}.
\label{eq:edge_deriv}
\end{equation}
由此，每步梯度计算只需在标准网格上对左、右两侧各求一次最短路（共2次求解），即可同时获得对全部 $K$ 个模态系数的梯度 $\boldsymbol{g}(\boldsymbol{z}) = \nabla_{\boldsymbol{z}} \Delta T(\boldsymbol{u}(\boldsymbol{z}))$。

搜索时，算法先在粗图中心 $\boldsymbol{z}=\boldsymbol{0}$ 计算初始梯度，一步跳至球面边界 $\boldsymbol{z}^{(1)} = \pm r\, \boldsymbol{g}(\boldsymbol{0}) / \|\boldsymbol{g}(\boldsymbol{0})\|_2$，再在球内执行步长减半的投影梯度上升。算法分别朝使左侧变慢与使右侧变慢两个方向、在半径 $r=1$ 与 $r=2$ 上各搜一次，其他半径 $r$ 下的最坏后悔按两者线性插值得到。每个任务共消耗约71次标准网格航线求解，与评估32个集合成员的计算量（64次求解）相近。

\subsection{海洋大数据标定：合理集合的物理结构与覆盖半径}
“合理反例”具有实际决策意义的关键，在于“合理”二字由多年历史海洋大数据标定而非主观设定\cite{benhaim2006infogap}。我们利用开发年份中旧粗图减真实海流的历史误差分两步标定：第一步统计各网格点误差流速大小以定出式(\ref{eq:plausible_field})中的缩放矩阵 $\mathbf{S}(\boldsymbol{x})$（3天前1°粗图全区典型误差中位数为0.17米/秒），并由空间相关衰减曲线定出误差相关长度 $L_{\text{corr}} = 76$ 千米（当天0.5°图为0.07米/秒、18千米），据此生成流函数模态 $\{\phi_k\}$。

第二步标定合理集合的半径 $r$：我们在开发年份任务上考察合理集合给出的两侧时间差范围包住真实时间差 $\Delta T(\boldsymbol{u}_{\text{true}})$ 的任务比例，将覆盖比例不低于90\%的最小半径选定为标定半径，得 $r = 1.5$（开发年份实际覆盖93\%，测试年份覆盖94\%）。这一准则以决策关心的时间差为尺度，使合理集合恰好包住大多数真实海洋。

\subsection{门控响应：依据最坏后悔与观测代价权衡行动}
获得两侧最坏后悔 $R_{s_0}(r)$ 与 $R_{\bar{s}_0}(r)$ 后，最后一步是根据最坏后悔是否超过门控阈值 $\theta$（开发年份按平均损失最小选定 $\theta = 8$ 小时）以及观测代价高低做出响应：
\begin{enumerate}
    \item 若 $R_{s_0}(r) \le \theta$，说明即使最不利的合理流场成真，坚持选 $s_0$ 的劣势也不超过 $\theta$，航行器直接照地图走（选 $s_0$）。
    \item 若 $R_{s_0}(r) > \theta$，说明当前选择面临较大尾部风险：当存在低代价且能消解大尺度歧义的观测手段（如单次上浮代价 $c_{\text{surf}}$ 较低时上浮取当天0.5°图）时，触发“门控后上浮取图”；当上浮代价高昂或仅有看不清远方切变的原位测流可用时，触发“门控后取保守”，直接改选最坏后悔更小的一侧：
    \begin{equation}
    s_{\text{cons}} = \arg\min_{s \in \{\text{L}, \text{R}\}} R_s(r).
    \label{eq:conservative_choice}
    \end{equation}
\end{enumerate}
完整流程见算法\ref{alg:counterexample_gate}。

\begin{algorithm}[htbp]
\caption{基于合理反例检验的自主水下航行器航路门控决策算法}
\label{alg:counterexample_gate}
\begin{algorithmic}[1]
\Require 粗分辨率海流图 $\boldsymbol{u}_0$，标定的误差模态 $\{\boldsymbol{m}_k\}_{k=1}^{K}$（式(\ref{eq:plausible_field})），标定半径 $r=1.5$，数值误差容限 $\tau_{\text{num}}=3.2$ 小时，门控阈值 $\theta=8.0$ 小时，上浮取图代价 $c_{\text{surf}}$ 及代价平衡点 $c^* \approx 1.0$ 小时。
\Ensure 最终执行的航路决策动作（选定绕行一侧 $s^*$ 或触发上浮取新图）。
\State 在粗图 $\boldsymbol{u}_0$ 上用粗算（8千米网格、8方向）求解两侧航时，得时间差 $\Delta T_{\text{coarse}}(\boldsymbol{u}_0)$。
\If{$|\Delta T_{\text{coarse}}(\boldsymbol{u}_0)| < \tau_{\text{num}}$}
    \State 触发按需精算：在 $\boldsymbol{u}_0$ 上用精算（2千米网格、32方向）重算得 $\Delta T_{\text{fine}}(\boldsymbol{u}_0)$，定地图倾向侧 $s_0 \gets \arg\min_{s \in \{\text{L},\text{R}\}} T_s^{\text{fine}}(\boldsymbol{u}_0)$。
\Else
    \State 直接采纳粗算结果：$s_0 \gets \arg\min_{s \in \{\text{L},\text{R}\}} T_s^{\text{coarse}}(\boldsymbol{u}_0)$。
\EndIf
\State 在中心 $\boldsymbol{z}=\boldsymbol{0}$ 处用标准网格（4千米、16方向）求左、右最快航线，按包络定理式(\ref{eq:envelope_grad})计算初始梯度 $\boldsymbol{g}(\boldsymbol{0})$。
\State 分别沿 $+\boldsymbol{g}(\boldsymbol{0})$ 与 $-\boldsymbol{g}(\boldsymbol{0})$ 方向跳至 $r_1=1$ 与 $r_2=2$ 的球面边界，执行步长减半的投影梯度上升，并在标定半径 $r$ 处线性插值得两侧最坏后悔 $R_{\text{L}}(r)$ 与 $R_{\text{R}}(r)$。
\If{$R_{s_0}(r) \le \theta$}
    \State \Return 直接照地图走：选择绕行一侧 $s^* \gets s_0$。
\Else
    \If{允许上浮通信且 $c_{\text{surf}} < c^*$}
        \State \Return 门控后上浮取图：付出代价 $c_{\text{surf}}$ 获取当天0.5°海流图 $\boldsymbol{u}_{\text{new}}$，选 $s^* \gets \arg\min_{s \in \{\text{L},\text{R}\}} T_s(\boldsymbol{u}_{\text{new}})$。
    \Else
        \State \Return 门控后取保守：选择最坏后悔更小的一侧 $s^* \gets \arg\min_{s \in \{\text{L},\text{R}\}} R_s(r)$。
    \EndIf
\EndIf
\end{algorithmic}
\end{algorithm}


########## ATTACHED FILE: sections/experiments.tex (current, checked text) ##########

\section{实验}

本节利用黑潮区域六年的高分辨率再分析数据，依次回答五个问题：（1）3天前的1°粗图错在哪里，其误差是否具备可由大数据标定的物理结构？（2）单纯增加计算量能否消除选边错误，环境歧义有多普遍？（3）五类策略中哪种能真正降低航时损失？（4）损失集中在哪些任务上，最坏后悔为何优于集合翻转比例，何时值得去观测？（5）当海流图变好、航行器变慢或更换误差模型时，方法的适用范围如何？

\subsection{实验设置与对比基线}
所有误差模态、标定半径（$r=1.5$）、数值误差容限（$\tau_{\text{num}}=3.2$小时）及门控阈值（$\theta=8$小时）均在2019--2021年开发年份（710个任务）上标定，原样用于2022--2024年测试年份（623个任务）评价。我们将14种对比方法分为五组（见图\ref{fig:main}）：（1）同一张粗图上加算（地图+粗算、地图+标准、照地图走（精算））；（2）不取新信息而改变决策准则（按期望时间、保守（最坏后悔最小））；（3）就地取新信息（原地停留测、沿途测30千米、沿途测60千米、绕行定点测）；（4）上浮取新图（总是上浮取当天1°图、总是上浮取当天0.5°图，每次计1小时）；（5）反例检验分流（门控后取保守、门控后上浮取图、门控后按期望时间）。显著性通过与照地图走（精算）配对差值的按天整组重抽样（2000次）95\%置信区间检验。

\subsection{旧粗图错在哪里：黑潮误差的空间结构与尺度}
3天前的1°粗图频繁误导决策，根本原因在于丢失了黑潮主轴及伴生涡旋的高幅值、长相关尺度切变，而这一结构可由多年历史数据稳定标定。开发年份的误差统计（图\ref{fig:data}）表明，黑潮强流带自台湾东北蜿蜒贯穿东海陆架坡折，3天前1°粗图的误差并非均匀白噪声，而是沿黑潮主轴形成高误差带，全区典型误差中位数为0.17米/秒，误差空间相关长度达76千米；相比之下，当天0.5°图的典型误差中位数降至0.07米/秒，相关长度缩短至18千米。76千米的误差相关长度意味着，在跨度百余千米的绕障任务中，一个未被粗图解析的中尺度误差模态足以笼罩整个左侧或右侧通道，使整条备选航线同时遭受逆流或顺流偏置，这构成了用低维流函数模态构造合理集合的物理依据。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_data}
\caption{台湾以东至东海研究海区的流场特征与粗图误差标定。(a) 研究海区（23°--31°N、121°--129°E）在2019--2021年开发年份的10米平均海流场，黑潮主轴清晰可见，橙色圆点标示测试任务禁航区中心位置；(b) 3天前1°粗图的典型误差幅度分布（米/秒），最大误差带紧密贴合黑潮强流轴；(c) 海流误差相关系数随两点空间距离的衰减曲线，当天0.5°图的误差相关长度约为18千米，而3天前1°粗图达76千米。旧粗图的误差具有鲜明的空间结构与中尺度相关长度，可由多年海洋大数据可靠标定，构成了构造“合理海流”的物理依据。}
\label{fig:data}
\end{figure}

\subsection{计算消除不了环境歧义：算力与合理反例的实证分析}
在同一张3天前1°粗图上大幅增加计算量只能消除少部分数值歧义，而在包住真实海洋的合理集合内，几乎每个任务都存在翻转决策的合理反例。在测试年份中，将求解算力从粗算增加64倍至精算，改变了64个任务的选择，其中38个改对、26个改错，选错一侧的任务比例因此仅从21.7\%降至19.7\%，平均损失的变化在统计上也不显著；相反，若不加计算而换成当天0.5°图，选错率立即降至10.4\%（图\ref{fig:ambiguity}(a)）。多算无效的原因在于环境本身的多解性：在开发年份覆盖93\%真实时间差、测试年份覆盖94\%的标定半径 $r=1.5$ 处，99.7\%的测试任务都存在至少一个使另一侧更快的合理反例（图\ref{fig:ambiguity}(b)）。因此，在旧粗图下环境歧义是常态，仅问“是否存在反例”没有区分度，真正决定行动的是反例造成的最坏后悔有多大。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_ambiguity}
\caption{机载计算量与环境信息对航路决策歧义的不同作用。(a) 测试年份选错绕行一侧的任务比例：在同一张3天前1°粗图上将计算量从粗算（21.7\%）增加至标准（20.5\%）与64倍精算（19.7\%），错误率仅下降约2个百分点，而换成当天0.5°图则直接减半至10.4\%（知道真相为0\%）；(b) 开发年份合理集合包住真实两侧时间差的任务比例与测试年份存在合理反例的任务比例随半径 $r$ 的变化，在标定半径 $r=1.5$ 处两者分别达93\%与99.7\%。机载计算只能消除少量的数值歧义；在足以包住真实海洋的合理集合里，几乎每个决定都存在合理反例，因此必须进一步度量反例导致的最坏损失大小。}
\label{fig:ambiguity}
\end{figure}

\subsection{主对比：五类响应策略的平均航时损失}
在五类响应策略的对比中，唯有基于合理集合控制尾部风险的保守准则与本文的门控后取保守策略显著降低了平均航时损失，而单纯加算、按期望时间选边与就地测流均未能显著改善结果（图\ref{fig:main}）。在测试年份上，照地图走（精算）的平均损失为0.98小时；改用32个合理场的按期望时间准则或门控后按期望时间，与精算地图的配对差置信区间均包含0，说明对对称随机扰动求平均并不能挑出翻转决策的不利流场。相反，门控后取保守将测试年份平均损失降至0.70小时，与照精算地图走的配对差为$-0.28$小时，95\%置信区间为$[-0.51, -0.07]$（不含0），相对损失降低28\%。门控后取保守之所以奏效，是因为在保守规则实际改选另一侧的41个任务中，有23个改对且平均每次省下10.1小时，18个改错但平均每次仅多花3.3小时——被避开的一侧往往具有很大的下行风险，改对的收益远大于改错的代价。同时，一律取保守的平均损失为0.72小时（与精算地图之差的置信区间亦不含0），门控后取保守与之相近：这表明不观测时的核心收益来自反例搜索给出的最坏后悔准则本身，而门控的作用在于锁定高风险任务，在调用有代价的上浮观测时将平均损失从总是上浮取0.5°图的1.22小时降至门控后上浮取图的0.78小时。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_main}
\caption{测试年份623个强流任务上五类响应策略的平均航时损失对比（竖直虚线为照精算地图走的平均损失0.98小时）。各组从上至下依次为：同一张粗图上加算（粗算1.16、标准1.03、精算0.98小时）；不取新信息而改变决策准则（按期望时间1.04、最坏后悔最小的保守准则0.72小时）；就地取新信息（原地停留测2.91、沿途测30千米0.93、沿途测60千米0.91、绕行定点测12.43小时）；总是上浮取新图（每次计1小时：当天1°图1.67、当天0.5°图1.22小时）；以及本文反例检验门控分流（门控后取保守0.70、门控后上浮取0.5°图0.78小时）。只有基于合理反例最坏后悔的保守与门控策略显著降低了损失，单纯加算与就地测流均难以奏效。}
\label{fig:main}
\end{figure}

\subsection{损失集中在哪里、何时值得观测}
航路决策的航时损失高度集中在少数尾部任务上，反例最坏后悔之所以有效，是因为它比集合翻转比例和地图时间差更能把大损失任务排在前面。若只论能否区分“是否选错且多花1小时以上”而不论多花多少，三种排序指标的区分能力其实相近；但考察排在前20\%的任务所捕获的地图总损失比例时，按反例最坏后悔达67\%，明显高于32个合理场翻转比例的49\%与地图两侧时间差的34\%（图\ref{fig:risk}(a)）。在门控阈值8小时下，被标记的47\%任务囊括了82\%的地图总损失，因为梯度搜索的最坏后悔直接度量了不利流场造成的航时差，而非将小损失翻转与十几个小时的大损失翻转同等看待。

各类观测手段的成败则取决于观测视野与时间代价的权衡。就地原位测流均未能带来显著净收益（与精算地图之差的置信区间或显著为正、或包含0）：原地停留测耗去2小时却只测到起点一处；绕行定点测平均要先花15.4小时才能赶到前方测点，得不偿失；沿途测30千米后换边的任务仅占3.4\%（其中81\%换对），说明出发后前30千米测到的海流很少足以改变对两侧的判断，而沿途测60千米后换边的任务虽增至18.8\%，但由于已深入半程、折返代价过大，换边只有15\%是划算的。对于能更新全局流场的上浮取当天0.5°图（图\ref{fig:risk}(b)），当单次上浮代价为0.5小时时，门控后上浮取图的平均损失为0.55小时，优于门控后取保守的0.70小时；而当上浮代价升至1.0小时时，门控后上浮取图升至0.78小时，交点出现在0.5至1小时之间（近1小时），此后无需观测的门控后取保守成为更优选择。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_risk}
\caption{航时损失的风险集中度排序与上浮观测代价平衡分析。(a) 按不同风险指标从高到低排序时，前一定比例任务累计捕获的地图总损失占比：排名前20\%的任务中，反例最坏后悔捕获了67\%的损失，显著高于32个合理场翻转比例（49\%）与地图两侧时间差（34\%）；(b) 测试年份平均损失随单次上浮取当天0.5°图时间代价（0--4小时）的变化曲线：总是上浮随代价线性恶化，门控后上浮在代价低于约1小时时最优，代价高于约1小时后门控后取保守（0.70小时）最优。反例最坏后悔能够准确识别大损失任务，从而实现“观测便宜时门控去测、观测昂贵时门控保守”的自适应切换。}
\label{fig:risk}
\end{figure}

\subsection{适用范围与消融分析}
表\ref{tab:scope}进一步检验了不同先验地图、航速与误差模型下的适用边界。第一，当航行器直接携带当天0.5°图时，存在合理反例的任务降至64.5\%，精算地图平均损失仅0.17小时，门控后取保守自动退化为绝大多数时候照地图走（损失同为0.17小时，配对差置信区间含0），不产生负向干扰。第二，当航行器对水速度降至0.75米/秒时，选错一侧的代价被显著放大，精算地图平均损失升至2.43小时；门控后取保守将损失降至1.80小时（但配对差置信区间包含0，统计上不显著），而由于选错代价变大、上浮相对更划算，门控后上浮取图将损失进一步降至1.32小时。第三，在消融实验中，若改用历史相似日的小尺度差构造合理集合，门控后取保守的平均损失为0.95小时，相比精算地图的0.99小时几乎失去纠错能力（配对差置信区间含0）。两组的反例搜索方法完全相同，差别只在“合理”如何定义：由多年数据标定误差大小与相关长度的合理集合，能够指出真正危险的一侧，而拼装历史相似日的小尺度差则不能。

\begin{table}[htbp]
\centering
\caption{不同海流图质量、航行器速度及合理集合构造方法下的适用范围与消融实验结果（损失单位：小时）。}
\label{tab:scope}
\small
\input{tables/route_scope.tex}
\end{table}

\subsection{局限性讨论}
本研究存在四方面局限：第一，单次任务求解将海流快照视为定常二维场，尚未耦合约40小时航行中的流场时变；第二，以当天1/12°再分析场作为“真实海洋”，仍平滑了亚中尺度过程与内波扰动；第三，将绕障简化为单个圆形禁航区的左右二元决策，未扩展至多岛礁群的多分支同伦类；第四，假设选定一侧后航行器能按真实海流以最优轨迹航行，以剥离底层轨迹跟踪误差、专门评估顶层选边决策。


########## ATTACHED FILE: sections/innovation.tex (current, checked text) ##########

\section{原创创新点拆解}

本研究从《海洋大数据技术原理与应用》课程核心议题出发，经历了问题提出、实证证伪与问题锐化的完整演进。课上讲授的“海洋大数据的计算引擎”使作者联想到：自主水下航行器端侧的算力与能量十分有限，计算、测量与运动之间必须权衡。作者最初提出的问题是：当航行器带着几天前的旧卫星图下水时，应把时间花在继续机载推演上，还是停下来重新观测？在东海赤潮巡测前期研究（第3节）中，我们发现增加推演计算只会让规划器在想象模型里自评虚高，真实收益早已饱和，且平滑标量场中用时分配的改进空间仅约0.02，远小于下水位置与地图新鲜度的影响。针对前期方法增益小、新意不足的缺陷，作者将问题锐化并转向强海流绕障这一选错一侧就损失数小时的二元决策：当存在多个与旧图同样相容、却要求采取相反行动的海洋状态时，再多计算也无法区分；能否在历史大数据界定的合理流场范围内，专门搜出一个让另一侧更好、且使当前选择明显受损的合理反例？这一追问直接催生了本文的合理反例检验框架（表\ref{tab:innovation}）。

\begin{table}[htbp]
\centering
\caption{本文核心原创创新点、已有做法对比、实验证据与局限拆解。}
\label{tab:innovation}
\small
\begin{tabular}{@{}p{0.14\linewidth}p{0.20\linewidth}p{0.22\linewidth}p{0.18\linewidth}p{0.13\linewidth}@{}}
\toprule
创新点 & 已有做法及其不足 & 本文做法 & 证据（图表） & 局限 \\
\midrule
1. 分离数值歧义与环境歧义的决策判据 & 确定性规划在粗图上盲目加密网格（误以为多算能消除一切模糊）；传统元推理只管何时停止搜索，不区分误差源于求解器还是环境模型失真。 & 提出数值歧义（小于粗精网格容限 $\tau_{\text{num}}$，靠按需精算消除）与环境歧义（合理集合内存在翻转决策的反例，只能靠新信息或保守应对）的二分准则。 & 图\ref{fig:overview}、图\ref{fig:curse}、图\ref{fig:ambiguity}(a)：64倍精算仅将选错率从21.7\%降至19.7\%，当天0.5°图则降至10.4\%。 & 仅在左右绕障的二元拓扑决策上验证，尚未扩展至多分支同伦路径。 \\
\addlinespace
2. 基于包络定理梯度的合理反例主动搜索 & 集合规划随机抽取数十个流场算均值或翻转比例；翻转比例只反映多少样本翻转了决定，不反映翻转后损失多大。 & 利用包络定理沿当前最快航线累加流速导数，一次梯度仅需2次最短路求解；先沿初始梯度跳至球面再投影细化，直接求最坏后悔。 & 图\ref{fig:main}、图\ref{fig:risk}(a)：最坏后悔前20\%任务捕获67\%损失，显著优于32成员集合翻转率（49\%）与地图差值（34\%）。 & 流场过大扰动下最短路拓扑可能跳变，使目标函数非凸、局部梯度近似产生折耗。 \\
\addlinespace
3. 海洋大数据驱动的合理集合与半径标定 & 若凭经验设定不确定性集合的形状与半径，会脱离海洋物理结构，易过度保守或漏报黑潮切变。 & 用三年历史再分析误差标定各点误差大小（缩放矩阵 $\mathbf{S}(\boldsymbol{x})$）与76千米相关长度的无散流函数模态；以覆盖90\%以上真实两侧时间差标定最小半径 $r=1.5$。 & 图\ref{fig:data}、图\ref{fig:ambiguity}(b)、表\ref{tab:scope}：$r=1.5$在测试年份覆盖94\%真实差值；消融替换为历史相似日差值后保守增益消失（0.99 vs 0.95小时）。 & 依赖多年历史再分析数据标定平稳统计量，对台风过境等非平稳极端天气适应受限。 \\
\addlinespace
4. 权衡最坏后悔与观测代价的门控响应 & 自适应采样面向全场降方差去测流，或不论代价一律保守/一律上浮，忽视了原位测流看不见远方切变及上浮通信本身耗时。 & 以最坏后悔超阈值 $\theta=8$小时作为门控：超标且上浮代价低（$<1$小时）时上浮取新图，代价高或仅有原位测流时改选最坏后悔更小一侧。 & 图\ref{fig:main}、图\ref{fig:risk}(b)、表\ref{tab:scope}：门控保守将平均损失从0.98降至0.70小时（降28\%），并给出约1小时的上浮代价切换点。 & 不观测时门控保守（0.70小时）比一律保守（0.72小时）的额外边际增益较小，主收益源于最坏后悔准则本身。 \\
\bottomrule
\end{tabular}
\end{table}

在人机协同完成本研究的过程中，作者与人工智能工具的分工如下（详见附录B，对话记录见代码仓库）。作者提出了最初关于机载计算与观测如何权衡的问题；在第一版结果出来后要求改用真实卫星数据检验、补充对照与消融实验；在前期研究结果出来后指出用时分配增益过小、方法新意不足，并提出了“两条航路、一张粗图、能否找到让另一条路更好的合理海流反例”这一新问题，决定转向本文的研究。人工智能助手Claude（Anthropic）完成了文献检索、代码、实验与作图，并核对了正文中的数字与引用；Gemini（Google）根据Claude整理的事实清单与提纲撰写了论文文字。


########## ATTACHED FILE: sections/conclusion.tex (current, checked text) ##########

\section{结论}

本文针对自主水下航行器在粗分辨率海流图下执行强流绕障时的在线元决策问题，提出了基于海洋大数据标定的合理反例检验方法，阐明了一条基本原理：机载计算的职责是消除求解器近似带来的数值歧义，从而读出已有海流图的本来倾向；而当多年海洋大数据界定的合理集合内存在翻转航路优劣并造成严重航时损失的合理反例时，环境处于算力无法消解的环境歧义状态，航行器唯有通过低代价的大尺度观测引入新信息，或在观测昂贵时改选最坏后悔更小的保守航路，才能有效降低逆流风险。在台湾以东至东海黑潮区域六年再分析海流的系统实验表明，将航线求解算力提高64倍仅能修复28\%的粗算错误，而合理反例的最坏后悔将67\%的地图总损失锁定在排名前20\%的高危任务中，使门控后取保守在不消耗观测时间的条件下将平均航时损失降低28\%，并清晰给出了原位测流的局限与上浮取图的代价阈值。未来工作将把该方法扩展至随时间连续演变的四维流场，并结合实艇开展海上试验。
```

</details>

## Gemini 的回复

<details><summary>展开（共 7377 字符）</summary>

```
===== R1 =====
本节利用黑潮区域六年的高分辨率再分析数据，依次回答六个问题：（1）3天前的1°粗图错在哪里，其误差是否具备可由大数据标定的物理结构？（2）单纯增加计算量能否消除选边错误，环境歧义有多普遍？（3）五类策略中哪种能真正降低航时损失？（4）损失集中在哪些任务上，最坏后悔为何优于集合翻转比例，何时值得去观测？（5）与随机合理场相比，反例搜索在算力上省下了什么？（6）当海流图变好、航行器变慢、更换误差模型或换至湾流海区时，方法的适用范围如何？

===== R2 =====
在测试年份上，照地图走（精算）的平均损失为0.98小时；改用32个合理场的按期望时间准则或门控后按期望时间，与精算地图的配对差置信区间均包含0，原因在于32个随机合理场数量太少、均值抽样误差过大（详见第6.6节）。

===== R3 =====
\subsection{反例搜索省下了什么：与随机合理场的比较}
在决定选哪一侧时，反例搜索的优势在于以约1/29的求解次数达到与上千个随机合理场平均同等的降损效果。理论推导与逐任务核对表明，选最坏后悔更小的一侧等价于按合理集合给出的两侧时间差范围的中点选边；若两侧时间差随海流线性变化则中点等于地图值，只有当一侧的最不利情形比另一侧严重得多时保守选择才会改选。测试年份实验（图\ref{fig:budget}(a)）显示，按期望时间选边随随机合理场数量增加而改善：用32个合理场时平均损失高于反例搜索后取保守（配对差+0.26小时，95\%置信区间$[0.03, 0.52]$），因为其均值的抽样误差中位数（2.4小时）大于它要估计的修正量（1.7小时），改选多由抽样噪声驱动；直到数百个合理场以上两者差异才不再显著，1024个合理场（2048次求解）的平均损失为0.71小时，与仅需约71次求解的反例搜索后取保守（0.72小时）相当（开发年份分别为0.88与0.76小时）。

在识别高风险任务时，排序有效的关键在于度量损失大小的后悔准则，而非翻转频率。测试年份中（图\ref{fig:budget}(b)），排名前20\%的任务所占的地图总损失，按随机合理场算出的期望后悔在32个场时已达65\%、1024个场时达67\%，接近反例搜索的最坏后悔（67\%）；相反，翻转比例在32个与1024个随机合理场下均停留在44\%，高于地图两侧时间差的34\%但始终落后于后悔指标。因此，只要度量的是坚持地图一侧会损失多少航时，数十个随机合理场的期望后悔已能较好地排出危险任务；反例搜索为算力受限航行器省下的是做出正确选边所需的上千次航线求解。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_budget}
\caption{随机合理场数量与反例搜索在选边决策和风险排序上的对比。(a) 测试年份平均航时损失随每个任务求解次数的变化：曲线为在 $n$ 个随机合理场上按期望时间选边（每次需 $2n$ 次求解），单点为反例搜索后取保守（约71次求解），水平虚线为照精算地图走（0.98小时）；(b) 按不同风险指标排名前20\%的任务所占地图总损失比例随求解次数的变化：两条曲线分别为随机合理场上的期望后悔与翻转比例，单点为反例搜索的最坏后悔（67\%），水平虚线为地图两侧时间差（34\%）。反例搜索以约1/29的求解次数达到了上千个随机合理场平均的选边效果，而风险排序的优劣取决于是否度量损失幅度而非样本数量。}
\label{fig:budget}
\end{figure}

===== R4 =====
表\ref{tab:scope}进一步检验了不同先验地图、航速、误差模型以及另一强流海区下的适用边界。

第四，为检验方法在其他强流区的可重复性，我们在北大西洋湾流海区（33°--41°N、75°--67°W）采用同一再分析产品、深度、年份划分与流程开展独立实验，半径与阈值由湾流开发年份重新标定。结果显示，环境歧义的普遍性、风险排序与门控触发观测的结论在湾流得到复现，但不观测直接取保守未能复现：64倍精算同样不减少选边错误（粗算18.5\%、精算19.4\%，改变了22个任务的选择，其中8个改对、14个改错），98.8\%的任务存在合理反例，最坏后悔前20\%的任务捕获了71\%的损失（翻转比例为49\%），且门控后上浮取图将平均损失从3.56小时显著降至1.31小时（优于总是上浮的1.53小时）。然而，门控后取保守的平均损失为4.00小时（与精算地图之差的置信区间含0）：原因是湾流测试任务中有8.7\%在真实海流下有一侧因顶流过强而不可通行（黑潮仅1.0\%），此类任务中合理集合内往往同时存在堵死左侧或堵死右侧的流场，使两侧最坏后悔双双接近上限，选较小一侧近乎随机，导致5次改选误入真实不可通行的一侧。我们在看到测试结果后补充了非预先设定的事后检验：若规定仅当两侧最坏后悔之差超过数值误差容限时才改选，湾流损失回到3.45小时（与地图差异不显著），同时保留了黑潮的大部分收益（0.77小时）。这明确了方法的边界：合理反例检验能可靠判断地图何时不可信并触发观测，而不观测的保守改选仅在两侧最坏情形差异分明时有效。

===== R9 =====
图\ref{fig:main}、图\ref{fig:risk}(b)、表\ref{tab:scope}：黑潮区门控后取保守将损失从0.98降至0.70小时，湾流区门控后上浮取图将损失从3.56降至1.31小时。 & 不观测的保守选择依赖两侧最坏情形差异明显；在湾流等两侧均可被强流堵死的海区失效，此时须靠门控上浮观测。 \\

===== R10 =====
本研究存在五方面局限：第一，单次任务求解将海流快照视为定常二维场，尚未耦合约40小时航行中的流场时变；第二，以当天1/12°再分析场作为“真实海洋”，仍平滑了亚中尺度过程与内波扰动；第三，将绕障简化为单个圆形禁航区的左右二元决策，未扩展至多岛礁群的多分支同伦类；第四，假设选定一侧后航行器能按真实海流以最优轨迹航行，以剥离底层轨迹跟踪误差、专门评估顶层选边决策；第五，不引入观测的门控后取保守依赖左右两侧的最坏后悔存在清晰差异，在湾流这类强流常可堵死任一侧的海区会因两侧最坏后悔同时接近上限而失效，此时必须依靠门控触发上浮观测来消解歧义。

===== R5 =====
{\heiti 摘要：}
随着海洋大数据的计算引擎延伸至移动观测平台边缘，自主水下航行器在受限算力与能量下必须在继续计算、补充观测与立即行动之间做出在线权衡。在强流区携带3天前的粗分辨率海流图绕越禁航区时，选错绕行一侧将导致数小时航时损失。现有确定性规划通过加密网格增加计算，只能提升求解精度而无法补充缺失的海洋信息；集合规划与自适应采样或需大量样本才能估准不利流场，或将观测耗费在与二元选边无关的全场重构上。为此，本文提出基于海洋大数据标定的合理反例检验方法，分离数值歧义与环境歧义以决定何时计算、何时观测、何时保守绕行。该方法先通过粗精网格容限按需精算以消除数值歧义，再用多年再分析海流标定旧粗图的无散误差模态与合理集合半径，利用包络定理投影梯度上升搜索使所选一侧变差、另一侧变好的合理反例及最坏后悔，据此门控触发上浮取图或选最坏后悔更小的一侧。六年黑潮再分析数据实验表明：计算量增加64倍仅将选错率从21.7\%降至19.7\%，而在覆盖94\%真实时间差的合理集合内99.7\%的任务存在合理反例；最坏后悔前20\%的任务集中了67\%的损失，反例搜索仅用约71次航线求解即达到约1024个随机合理场（2048次求解）按期望时间选边的效果，使门控后取保守将平均损失从0.98小时降至0.70小时；湾流海区重复实验证实门控后上浮取图可将损失从3.56小时降至1.31小时，但因强流可堵死任一侧，不观测的保守改选在该区不带来收益。

{\heiti 关键词：}海洋大数据；自主水下航行器；航路规划；合理反例检验；元推理；不确定性量化

\vspace{1em}
\begin{center}
{\large\bfseries Plausible Counterexample Test: When an Autonomous Underwater Vehicle Should Compute and When It Should Observe Under a Coarse Current Map}
\end{center}
\vspace{0.5em}

{\bfseries Abstract:}
As the computing engine of ocean big data extends to the edge of mobile platforms, an autonomous underwater vehicle under limited onboard computation and energy must trade off online among continued computation, additional observation, and immediate movement. When navigating around a no-go zone in strong currents with a three-day-old coarse current map, choosing the wrong side costs hours of transit time. Deterministic planning refines the search grid on the best-estimate map, sharpening numerical precision without supplying missing oceanographic information, while ensemble planning and adaptive sampling either require large ensembles to estimate adverse flows or spend observations reconstructing the whole field rather than resolving the binary route choice. We propose a plausible counterexample test calibrated by ocean big data that separates numerical ambiguity from environmental ambiguity to decide when to compute, observe, or hedge conservatively. The method resolves numerical ambiguity via an on-demand fine solve, calibrates divergence-free error modes and a plausible-set radius from multi-year reanalysis currents, and uses envelope-theorem projected gradient ascent within the plausible ball to find the worst counterexample and its worst regret, gating between surfacing for a new map and choosing the side with smaller worst regret. Across six years of Kuroshio reanalysis data, 64-fold more computation cuts wrong-side choices only from 21.7\% to 19.7\%, whereas 99.7\% of missions admit a plausible counterexample inside the calibrated set covering 94\% of real time differences; the top 20\% of missions by worst regret hold 67\% of total loss, and the search matches the expected-time rule over 1024 random plausible fields (2048 route solves) using about 71 solves, lowering mean loss from 0.98 to 0.70 hours. Replication in the Gulf Stream confirms gated surfacing (lowering loss from 3.56 to 1.31 hours), whereas observation-free conservative routing does not help there because strong currents can block either side.

{\bfseries Keywords:} ocean big data; autonomous underwater vehicle; path planning; plausible counterexample test; metareasoning; uncertainty quantification

===== R6 =====
\begin{itemize}
    \item \textbf{概念与判别准则创新：}据我们所知，本文首次在自主水下航行器航路决策中分离了可由计算消除的“数值歧义”与需靠新信息或保守决策应对的“环境歧义”，提出以最坏合理后悔为核心判据的合理反例检验框架，明确了边缘计算与海洋观测的功能边界。
    \item \textbf{大数据标定与高效反例搜索：}利用多年再分析海流标定旧粗图的无散流函数误差模态及覆盖90\%以上真实时间差的合理集合半径，结合包络定理梯度与球面投影搜索，以约71次标准网格求解直接定位最坏后悔流场，达到按期望时间准则需约1024个随机合理场（2048次求解，约为其29倍）才能达到的选边效果。
    \item \textbf{黑潮与湾流双海区系统实证：}在六年黑潮再分析海流共1333个任务上的实验表明，64倍算力仅修复28\%的粗算错误，而99.7\%的任务存在合理反例；最坏后悔前20\%的任务集中了67\%的损失，门控后取保守将平均航时损失降低28\%。在湾流海区的独立重复实验中，门控识别高危任务与门控后上浮取图（损失由3.56降至1.31小时）同样成立，但因两侧均可能被强流堵死，不观测的保守选择不再有效，从而界定了两种响应策略各自的适用条件。
\end{itemize}

===== R6b =====
本文其余部分组织如下：第2节回顾相关工作；第3节简述前期赤潮巡测研究；第4节建立绕障航路决策模型；第5节详述合理反例检验与门控方法；第6节给出实验结果、与随机合理场的比较、适用范围与湾流重复实验；第7节拆解创新点与研究脉络；第8节总结全文。

===== R7 =====
2. 基于包络定理梯度的合理反例主动搜索 & 随机合理场按期望时间选边需上千个样本（约2048次求解）才能压低抽样噪声，32个样本误差过大；翻转比例只计翻转频率而不计损失大小。 & 利用包络定理沿当前最快航线累加流速导数，一次梯度仅需2次最短路求解；先沿初始梯度跳至球面再投影细化，直接求最坏后悔。 & 图\ref{fig:main}、图\ref{fig:risk}(a)、图\ref{fig:budget}：搜索以约71次求解达到1024个随机合理场（2048次求解）的选边效果；最坏后悔与期望后悔前20\%任务均捕获约67\%损失，显著高于翻转比例（44\%）。 & 在随机合理场的期望后悔已能较好排序风险任务，反例搜索的优势集中于减少选边所需的求解次数；大扰动下最短路拓扑跳变会带来局部梯度近似误差。 \\

===== R8 =====
\section{结论}

本文针对自主水下航行器在粗分辨率海流图下执行强流绕障时的在线元决策问题，提出了基于海洋大数据标定的合理反例检验方法，阐明了一条基本原理：机载计算的职责是消除求解器近似带来的数值歧义，从而读出已有海流图的本来倾向；而当多年海洋大数据界定的合理集合内存在翻转航路优劣并造成严重航时损失的合理反例时，环境处于算力无法消解的环境歧义状态，航行器需通过门控引入大尺度观测或在条件具备时改选最坏后悔更小的保守航路。在黑潮区域六年再分析海流的系统实验表明，将航线求解算力提高64倍仅能修复28\%的粗算错误，而反例搜索以约71次求解达到了约1024个随机合理场（2048次求解）按期望时间选边的效果，其最坏后悔将67\%的地图总损失锁定在排名前20\%的任务中，使门控后取保守将平均航时损失从0.98小时降至0.70小时；湾流海区重复实验进一步证实，反例门控与门控后上浮取图（损失从3.56降至1.31小时）跨海区稳健成立，而不观测的保守改选则仅在两侧最坏情形差异分明、不双双被强流堵死时有效。未来工作将把该方法扩展至时变四维流场并开展实艇试验。
```

</details>
