# 与 Gemini 的对话记录 14：第 8 轮：全文润色——主线清晰、正面结果、标准术语、压缩篇幅

时间（回复保存时间）：2026-11-07 02:46 UTC。调用方式：Claude 用命令行工具 ask-gemini 把下面“发送内容”作为附件发给 Gemini，并附一句简短指令（按附件中的写作要求完成各节）；回复原样存档后再由 Claude 核对数字与引用、拆分进论文各节。下面两部分都是原文，未作删改。

调用记录：

```
回答已存到 D:\海洋大数据\paper\gemini\rev8_reply.md
[gemini-4-argon-medium · gemini 格式 · 输入 31781 / 输出 14845 token · 175.2 秒]
```

本轮的写作要求见下方发送内容里的附件 `brief_rev8.md`。

## 发送内容

<details><summary>展开（共 55578 字符）</summary>

```
########## ATTACHED FILE: brief_rev8.md ##########

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


########## ATTACHED FILE: terms_v6.md ##########

# 术语表（v6）——用标准术语或一看就懂的说法；下表“不再使用”一列的自造标签一律不用

| 统一写法 | 含义（首次出现时用一句话说明） | 不再使用 |
|---|---|---|
| 自主水下航行器（下称航行器） | 研究对象 | AUV |
| 粗图 | 首次写全称“3天前的1°粗分辨率海流图（下称粗图）” | 粗分辨率地图、地图（作专名时） |
| 真实海流 | 当天1/12°再分析海流场（实验中作为真实海洋） | 知道真相 |
| 左右航时差 | 左侧最快航时减右侧最快航时（小时），为负则左侧快 | 两侧时间差 |
| 粗网格、中网格、细网格求解 | 8千米网格8个方向、4千米16个方向、2千米32个方向的最短路求解，计算量之比1:8:64 | 粗算、标准、精算 |
| 基线：按粗图选边 | 在粗图上用细网格求解，选航时更短的一侧 | 照地图走（精算）、地图+精算 |
| 数值歧义 | 左右航时差小于求解误差，加密网格即可分辨 | |
| 环境歧义 | 粗图同时容许“左侧更快”和“右侧更快”的真实海流，加密网格无法分辨 | |
| 合理流场集合（简称合理集合） | 以粗图为中心、按多年误差统计划定大小的流场集合，即鲁棒优化中的不确定集 | 合理海流、合理场 |
| 合理反例 | 合理集合中使另一侧更快的流场 | |
| 后悔值；最大后悔值 | 选某一侧后比另一侧多花的航时称后悔值；合理集合内后悔值的最大值称最大后悔值（决策理论中的标准概念） | 最坏后悔 |
| 合理反例检验 | 本文方法：在合理集合中搜索最大后悔值及对应的合理反例 | 反例检验（可作简称） |
| 阈值判据 | 最大后悔值超过阈值，即判定粗图对本次决定不可信 | 门控 |
| 超阈值时上浮取图 | 判定不可信时上浮获取当天海流图（每次计1小时） | 门控后上浮取图 |
| 超阈值时保守改选 | 判定不可信时改选最大后悔值较小的一侧 | 门控后取保守、保守（最坏后悔最小） |
| 修正规则 | 仅当两侧最大后悔值之差超过数值误差容限时才改选 | 改进规则、规则C |
| 集合平均选边 | 从误差模型随机抽取若干流场（集合成员），选平均航时更短的一侧 | 按期望时间、集合期望（贝叶斯） |
| 集合成员 | 从误差模型随机抽取的流场 | 随机合理场、合理场 |
| 改变选边的成员比例 | 集合中选择与粗图不同的成员所占比例 | 翻转比例 |
| 后悔值的集合平均 | 坚持粗图一侧时，后悔值在集合成员上的平均 | 期望后悔 |
| 额外航时 | 实际航时减去真实更快一侧的航时（小时），越低越好 | 损失 |
| 理想上限 | 已知真实海流时直接选更快一侧 | 知道真相 |
| 原地停留测流、沿途测流30千米、沿途测流60千米、绕行定点测流、上浮取当天1°图、上浮取当天0.5°图 | 各种观测方式（见表1） | 原地停留测、沿途测30千米 |
| 卫星测高地转流图 | 美国国家海洋和大气管理局近实时融合测高地转流（0.25°） | |
| 黑潮主设置、湾流、阿古拉斯回流区、黑潮区改带卫星测高地转流图 | 四种实验设置 | 同源粗图 |
| 前期研究的词：模拟海洋、检验用模拟海洋、规划器对自身航线的估值、出发前模拟 | 由误差模型生成的海洋样本；未参与搜索、只用于检验的样本；规划器在搜索过的样本上给航线的分数；出发前在模拟海洋上比较各种用时策略 | 想象海洋、留出海洋、自评、出发前预演 |
| 单位 | 千米、米/秒、小时 | |


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

## 第三海区独立检验：阿古拉斯回流区（35–43°S、14–22°E，全为开阔海洋；检验计划在下载数据之前写进 NOTEBOOK.md，写定后未改；流程同上，半径与阈值用该区自己的开发年份标定，测试年份只评价一次）
- 任务：开发年份 697 个（364 天），测试年份 618 个（323 天）；更快一侧平均航时 40.9 小时。
- 3 天前 1° 粗图的误差：典型误差中位数 0.39 米/秒，相关长度 43 千米。
- 标定：半径 r = 2.0（开发年份覆盖 92%，测试年份 94%）；数值误差容限 11.2 小时；保守门控阈值 0 小时，上浮取 0.5° 图门控阈值 12 小时。
- 选错一侧：粗算 27.7%，精算 27.7%（加算改变 32 个任务的选择：16 个改对、16 个改错）；换成当天 0.5° 图 7.0%。
- 真实海流中有一侧过不去的任务：16.2%。存在合理反例的任务：99.2%。
- 地图+粗算：平均损失 6.62 小时；与精算地图之差 -0.25 [-1.14, 0.54]
- 地图+精算：平均损失 6.87 小时；与精算地图之差 +0.00 [0.00, 0.00]
- 集合期望（贝叶斯）：平均损失 7.00 小时；与精算地图之差 +0.13 [-1.46, 1.71]
- 保守（最坏后悔最小）：平均损失 6.24 小时；与精算地图之差 -0.63 [-1.99, 0.57]
- 反例门控→保守：平均损失 6.49 小时；与精算地图之差 -0.38 [-1.50, 0.76]
- 反例门控→保守（差距超过容限才改选）：平均损失 6.72 小时；与精算地图之差 -0.16 [-0.82, 0.39]
- 总是沿途测30km：平均损失 4.48 小时；与精算地图之差 -2.39 [-4.43, -0.63]
- 总是上浮取当天0.5°图：平均损失 1.98 小时；与精算地图之差 -4.89 [-6.82, -3.04]
- 反例门控→上浮取0.5°图：平均损失 2.20 小时；与精算地图之差 -4.67 [-6.47, -2.86]
- 风险排序（排前 20% 的任务所占的地图损失）：反例的最坏后悔 53%，32 个合理场的翻转比例 36%，地图上两侧时间差 23%。
- 预先写定的判定：
  1. 改进规则 C（只在两侧最坏后悔之差超过容限时改选）：与精算地图之差 -0.16 [-0.82, 0.39] → 无害、无显著收益。
  2. 原规则 A（门控后取保守）：-0.38 [-1.50, 0.76]；一侧过不去的任务 16.2%（只报告）。
  3. 门控后上浮取 0.5° 图：-4.67 [-6.47, -2.86] → 成立。
  4. 加算 64 倍选错率变化 0.0 个百分点（预期不超过 3）→ 成立。
  5. 最坏后悔排前 20% 的损失 53% 对翻转比例 36% → 成立。

## 航行器改带真实卫星海流图（黑潮区；检验计划在下载卫星数据之前写进 NOTEBOOK.md，写定后未改）
- 设置：真实海流仍为 HYCOM 1/12°、10 米；航行器的图换成 NOAA CoastWatch 近实时融合测高地转流（0.25°，逐日，绝对表层地转流），取 3 天前那一天；上浮取图 = 取当天的测高图（每次 1 小时），另保留“上浮取当天 0.5° 模式图”作理想参照；误差模型、半径与阈值在开发年份用“测高图减 HYCOM”标定。
- 任务：开发年份 616 个（308 天），测试年份 648 个（324 天）；更快一侧平均航时 38.7 小时。
- 测高图（3 天前）的误差：典型误差中位数 0.19 米/秒，相关长度 80 千米。
- 标定：半径 r = 1.75（开发年份覆盖 92%，测试年份 92%）；数值误差容限 7.4 小时；保守门控阈值 6 小时，上浮取测高图门控阈值 1000000000 小时，上浮取 0.5° 模式图门控阈值 12 小时。
- 选错一侧：粗算 19.9%，精算 19.6%（加算改变 22 个任务的选择：12 个改对、10 个改错）；换成当天测高图 18.5%，当天 0.5° 模式图 8.6%。
- 存在合理反例的任务 81.0%；真实海流中有一侧过不去的任务 0.8%。
- 地图+粗算：平均损失 0.89 小时；与精算地图之差 +0.09 [-0.01, 0.24]
- 地图+精算：平均损失 0.79 小时；与精算地图之差 +0.00 [0.00, 0.00]
- 集合期望（贝叶斯）：平均损失 0.83 小时；与精算地图之差 +0.04 [-0.22, 0.27]
- 保守（最坏后悔最小）：平均损失 0.71 小时；与精算地图之差 -0.09 [-0.38, 0.19]
- 反例门控→保守：平均损失 0.71 小时；与精算地图之差 -0.08 [-0.37, 0.20]
- 反例门控→保守（差距超过容限才改选）：平均损失 0.70 小时；与精算地图之差 -0.09 [-0.38, 0.19]
- 总是沿途测30km：平均损失 0.85 小时；与精算地图之差 +0.06 [-0.16, 0.25]
- 总是上浮取当天测高图：平均损失 1.97 小时；与精算地图之差 +1.18 [0.73, 1.77]
- 反例门控→上浮取测高图：平均损失 0.79 小时；与精算地图之差 +0.00 [0.00, 0.00]
- 总是上浮取当天0.5°图：平均损失 1.18 小时；与精算地图之差 +0.39 [0.08, 0.66]
- 反例门控→上浮取0.5°图：平均损失 0.64 小时；与精算地图之差 -0.15 [-0.45, 0.10]
- 风险排序（排前 20% 的任务所占的地图损失）：反例的最坏后悔 67%，32 个合理场的翻转比例 52%，地图上两侧时间差 28%。
- 预先写定的判定：
  1. 加算 64 倍选错率变化 0.3 个百分点（预期不超过 3）→ 成立。
  2. 存在合理反例 81.0%（预期不少于 90%）→ 不成立。
  3. 最坏后悔排前 20% 的损失 67% 对翻转比例 52% → 成立。
  4. 门控后上浮取当天测高图：+0.00 [0.00, 0.00]（只报告）；门控后上浮取当天 0.5° 模式图：-0.15 [-0.45, 0.10] → 不成立。
  5. 门控后取保守（规则 A）-0.08 [-0.37, 0.20]；改进规则 C -0.09 [-0.38, 0.19]（预期 C 的点估计不高于照地图走 → 成立）。



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



########## ATTACHED FILE: tables/route_settings.tex (Table 1, to be rewritten in the new terms) ##########

\begin{tabular}{@{}p{0.16\linewidth}p{0.80\linewidth}@{}}
\toprule
项目 & 设置 \\
\midrule
海流数据 & HYCOM 全球海洋再分析（GLBy0.08，实验 93.0），水平分辨率 1/12°，取 10 米深度；23°--31°N、121°--129°E（台湾以东至东海，含黑潮）；2019-01-01 至 2024-08-29 每 3 天 12:00 时一张，共 689 张 \\
任务 & 每张快照抽 2 个：起终点相距 100--140 千米、离岸不少于 20 千米，两点中间设半径 15 千米的禁航区，可从左侧或右侧绕过；只取粗图上任务区平均流速不低于 0.3 米/秒的强流任务；开发 710 个（2019--2021 年），测试 623 个（2022--2024 年） \\
地图与真实海流 & 航行器带 3 天前的 1° 粗分辨率海流图（格内平均）；真实海流为当天 1/12° 场 \\
航行器 & 对水速度 1.0 米/秒；选定一侧后，按真实海流在该侧以最快方式航行 \\
航线求解 & 网格最短路：粗算 8 千米网格、8 个方向；标准 4 千米、16 个方向；精算 2 千米、32 个方向（计算量之比 1 : 8 : 64）；顶流过强的边不可通行 \\
合理海流 & 粗图加上由流函数生成的无散误差模态的组合，各点误差大小与相关长度（76 千米）由开发年份标定，组合系数服从标准正态；半径 $r=1.5$（开发年份中包住真实两侧时间差的任务占 93\%） \\
反例检验 & 在半径 $r$ 的球内对两侧时间差做投影梯度上升（梯度沿最快航线累加）；两个方向、半径 1 与 2 各搜一次，其他半径线性插值，每个任务约 71 次标准网格求解 \\
观测方式 & 出发前原地停留 2 小时测 12 次；沿所选一侧航行 30 或 60 千米并连续测流后可换边；绕到反例与地图差别最大处（前方 40 千米内）去测；上浮取当天 1° 或 0.5° 海流图（每次 1 小时）；测流噪声 0.05 米/秒 \\
门控 & 最坏后悔超过 8 小时（开发年份选定）时取保守一侧或上浮取图，否则照地图走 \\
评价 & 损失 = 实际航时 $-$ 更快一侧的航时（小时）；配对差值的 95\% 置信区间按天整组自助重抽样 2000 次 \\
\bottomrule
\end{tabular}


########## ATTACHED FILE: tables/route_scope.tex (Table 2, generated by a script; Claude renames its headers to the new terms) ##########

\begin{tabular}{@{}p{0.21\linewidth}>{\centering\arraybackslash}p{0.080\linewidth}>{\centering\arraybackslash}p{0.080\linewidth}>{\centering\arraybackslash}p{0.080\linewidth}>{\centering\arraybackslash}p{0.080\linewidth}>{\centering\arraybackslash}p{0.080\linewidth}>{\centering\arraybackslash}p{0.080\linewidth}>{\centering\arraybackslash}p{0.080\linewidth}@{}}
\toprule
设置 & 测试任务 & 存在合理反例 & 精算地图选错 & 精算地图损失（小时） & 门控后取保守（小时） & 门控后上浮取图（小时） & 反例排前 20\% 的任务所占损失 \\
\midrule
主设置：3 天前 1° 粗图，对水 1.0 米/秒 & 623 & 99.7\% & 19.7\% & 0.98 & 0.70 & 0.78 & 67\% \\
地图较好：当天 0.5° 图 & 349 & 64.5\% & 8.0\% & 0.17 & 0.17 & 0.16 & 60\% \\
慢速航行器：对水 0.75 米/秒 & 347 & 99.1\% & 18.4\% & 2.43 & 1.80 & 1.32 & 74\% \\
消融：合理集合改用历史相似日的小尺度差 & 349 & 99.4\% & 19.5\% & 0.99 & 0.95 & 0.77 & 64\% \\
换海区：湾流（33°–41°N、75°–67°W），其余同主设置 & 643 & 98.8\% & 19.4\% & 3.56 & 4.00 & 1.31 & 71\% \\
换海区：阿古拉斯回流区（35°–43°S、14°–22°E），其余同主设置 & 618 & 99.2\% & 27.7\% & 6.87 & 6.49 & 2.20 & 53\% \\
换地图：带 3 天前的卫星测高地转流图（0.25°），其余同主设置 & 648 & 81.0\% & 19.6\% & 0.79 & 0.71 & 0.64 & 67\% \\
\bottomrule
\end{tabular}


########## ATTACHED FILE: sections/title.tex (current text, to be rewritten) ##########

合理反例检验：粗分辨率海流图下自主水下航行器何时计算、何时观测


########## ATTACHED FILE: sections/abstract.tex (current text, to be rewritten) ##########

{\heiti 摘要：}
随着海洋大数据的计算引擎延伸至移动观测平台边缘，自主水下航行器在受限算力与能量下必须在继续计算、补充观测与立即行动之间做出在线权衡。在强流区携带3天前的粗分辨率海流图绕越禁航区时，选错绕行一侧将导致数小时航时损失。现有确定性规划通过加密网格增加计算，只能提升求解精度而无法补充缺失的海洋信息；集合规划与自适应采样或需大量样本才能估准不利流场，或将观测耗费在与二元选边无关的全场重构上。为此，本文提出基于海洋大数据标定的合理反例检验方法，分离数值歧义与环境歧义以决定何时计算、何时观测、何时保守绕行。该方法先按需精算以消除数值歧义，再用多年再分析海流标定旧粗图的无散误差模态与合理集合半径，利用包络定理投影梯度上升搜索使所选一侧变差、另一侧变好的合理反例及最坏后悔，据此门控触发上浮取图或选最坏后悔更小的一侧。台湾以东至东海黑潮区六年再分析数据实验表明：计算量增加64倍仅将选错率从21.7\%降至19.7\%，而在覆盖94\%真实时间差的合理集合内99.7\%的任务存在合理反例；最坏后悔前20\%的任务集中了67\%的损失；反例搜索仅用约71次航线求解，即达到按期望时间选边使用约1024个随机合理场时的效果；门控后取保守将平均损失从0.98小时降至0.70小时。在湾流区与阿古拉斯回流区的重复实验中，单纯增加计算同样无效，最坏后悔风险排序与门控后上浮取图均成立（平均损失分别由3.56降至1.31小时、由6.87降至2.20小时），而不观测的保守改选在这两个海区均无显著收益；航行器改带真实卫星测高地转流图后，加算无效与风险排序仍成立，但各种响应的收益不再显著。

{\heiti 关键词：}海洋大数据；自主水下航行器；航路规划；合理反例检验；元推理；不确定性量化

\vspace{1em}
\begin{center}
{\large\bfseries Plausible Counterexample Test: When an Autonomous Underwater Vehicle Should Compute and When It Should Observe Under a Coarse Current Map}
\end{center}
\vspace{0.5em}

{\bfseries Abstract:}
As ocean big-data computing moves onto mobile platforms, an autonomous underwater vehicle with limited onboard computation and energy must trade off computing, observing and moving. Rounding a no-go zone in strong currents with a three-day-old coarse current map, a vehicle that picks the wrong side loses hours. A finer solver grid sharpens precision but adds no oceanographic information; ensemble planning needs many samples, and adaptive sampling spends observations on the whole field rather than on the binary route choice. We propose a plausible counterexample test, calibrated by ocean big data, that separates numerical from environmental ambiguity to decide when to compute, observe or hedge. The method resolves numerical ambiguity with an on-demand fine solve, calibrates divergence-free error modes and a plausible-set radius from multi-year reanalysis currents, finds the worst counterexample and its worst regret by envelope-theorem gradient ascent, and gates between surfacing for a new map and taking the side with smaller worst regret. Across six years of Kuroshio reanalysis data, 64-fold more computation cuts wrong-side choices only from 21.7\% to 19.7\%, whereas 99.7\% of missions admit a plausible counterexample inside a set covering 94\% of real time differences; the top 20\% of missions by worst regret hold 67\% of total loss; the search reaches with about 71 route solves what the expected-time rule needs about 1024 random plausible fields to reach; and gated conservative routing lowers mean loss from 0.98 to 0.70 hours. In replications in the Gulf Stream and the Agulhas retroflection, extra computation remains ineffective, while risk ranking and gated surfacing hold (mean loss from 3.56 to 1.31 hours and from 6.87 to 2.20 hours); observation-free conservative routing brings no significant gain in either region. With a real satellite altimetry map, computation stays ineffective and ranking holds, but no response gains significantly.

{\bfseries Keywords:} ocean big data; autonomous underwater vehicle; path planning; plausible counterexample test; metareasoning; uncertainty quantification


########## ATTACHED FILE: sections/intro.tex (current text, to be rewritten) ##########

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
    \item \textbf{大数据标定与高效反例搜索：}利用多年再分析海流标定旧粗图的无散流函数误差模态及覆盖90\%以上真实时间差的合理集合半径，结合包络定理梯度与球面投影搜索，以约71次标准网格求解直接定位最坏后悔流场，其选边效果与按期望时间准则使用约1024个随机合理场（2048次求解，约为其29倍）相当。
    \item \textbf{黑潮、湾流与阿古拉斯回流区三个强流区的系统实证：}在六年黑潮再分析海流共1333个任务上的实验表明，64倍算力仅使选错率从21.7\%降至19.7\%，而99.7\%的任务存在合理反例；最坏后悔前20\%的任务集中了67\%的损失，门控后取保守将平均航时损失降低28\%。在湾流区以及在下载数据前即写定检验计划的阿古拉斯回流区，门控识别高危任务与门控后上浮取图（平均损失分别从3.56小时降至1.31小时、从6.87小时降至2.20小时）同样成立，而不观测的保守改选及其改进规则均无显著收益，从而表明门控的核心价值在于决定何时去观测；黑潮区改带真实卫星测高图时，加算无效与风险排序仍成立，而各种响应的收益不再显著。
\end{itemize}

本文其余部分组织如下：第2节回顾相关工作；第3节简述前期赤潮巡测研究；第4节建立绕障航路决策模型；第5节详述合理反例检验与门控方法；第6节给出实验结果、与随机合理场的比较、适用范围与两个海区的重复实验；第7节拆解创新点与研究脉络；第8节总结全文。


########## ATTACHED FILE: sections/related.tex (current text, to be rewritten) ##########

\section{相关工作}

\subsection{受限理性元推理与智能体过度思考}
机载算力分配源于受限理性与元推理理论，核心是评估“计算的价值”是否超过其时间与能量代价\cite{horvitz1987reasoning,russell1991right}。在机器人运动规划中，研究者通过学习停止规则或自适应计算预算来决定何时终止搜索并执行动作，或使规划与移动并行交织\cite{xiao2020thinking,sung2021quit,elboher2023formal,magnino2026metareasoning}。然而，当内部环境模型存在偏差时，延长规划视野或增加搜索深度反而会放大模型误差，诱发决策分析中的“优化器诅咒”，使规划器陷入无益的过度思考\cite{smith2006curse,jiang2015horizon,cuadron2025overthinking}。近期在智能体推理与任务消歧中也发现了相似规律：当外部环境状态未知或指令存在多重解释时，增加测试时计算无法替代与环境交互或主动寻求澄清\cite{hunt2021formalizing,shen2025thinking,kobalczyk2025active}。与仅关注何时停止搜索的元推理不同，本文将模糊性拆解为求解器粗糙引起的数值歧义与地图失真引起的环境歧义，从而在计算、观测与保守行动之间建立切换准则。

\subsection{面向决策的信息获取与多解性判别}
并非所有减少环境不确定性的观测都能改善特定决策，唯有能区分竞争假设的信息才具决策价值\cite{chernoff1959sequential,box1967discrimination}。在统计实验设计与多臂赌博机中，最优臂识别与信息导向采样专门收集能尽快排除次优选项的样本，而非均匀降低全局方差\cite{garivier2016optimal,russo2018thompson,russo2018ids}；目标导向实验设计同样强调只针对目标泛函优化传感器布放\cite{attia2018goal}。与之呼应，信息间隙决策理论与预测多解性研究指出，当多个与数据同样相容的模型给出相反预测时，单靠点估计无法保证安全，必须考察不确定性半径内的最坏表现\cite{benhaim2006infogap,marx2020predictive}。不同于在离散假设空间或线性反问题中计算期望信息增益，本文利用包络定理直接在连续无散海流场上沿梯度搜寻翻转二元航路选择的物理反例，以最坏后悔度量环境歧义的严重程度。

\subsection{不确定海洋流场中的航路规划与自适应采样}
强海流下的自主水下航行器路径规划常利用图搜索或水平集方程在确定性流场中求取时间最优轨迹\cite{dijkstra1959note,lolla2014levelset}。为应对海洋预报不确定性，研究者提出了集合期望与风险折中规划、动态正交随机时间最优控制以及纳入误差协方差的鲁棒路径搜索\cite{wang2016path,subramani2018stochastic,kularatne2018forecast}；海洋自适应采样则利用高斯过程或集合卡尔曼滤波在线更新叶绿素或流场估计，引导航行器前往高信息增益区\cite{anderson2001eakf,srinivas2012gpucb,hollinger2014sampling,fossum2019}。然而，现有不确定流场规划大多将集合样本作为固定输入来寻找单一路径，既不评估有限集合是否漏掉了翻转拓扑走向的流场，也不回答是否值得付出时间代价去换取新海流图；本文则将多年海洋再分析大数据转化为合理流场集合的物理边界，专门解决粗图下“算、测、走”的闭环元决策问题。


########## ATTACHED FILE: sections/prior.tex (current text, to be rewritten) ##########

\section{前期研究：多算为何收效甚微}

本研究始于作者在东海赤潮巡测场景下对机载算力分配的初步探索：当航行器携带3天前的卫星叶绿素浓度图下水，在“继续计算”“边走边测”与“停下复测”之间分配有限作业时间时，多算能否带来更好的观测收益\cite{lou2014diurnal,mnr2024bulletin}？我们用多年卫星叶绿素数据标定旧图误差并构造48个想象海洋（32个用于搜索、16个留出不参与搜索）\cite{beckers2003dineof,gaspari1999correlation}，采用交叉熵方法搜索巡测航线\cite{deboer2005cem}，以航行器报告的最浓位置与真实最浓处之间对数叶绿素浓度差的时间平均（遗憾）为指标，考察了推演次数与用时策略的作用。

前期研究的第一个发现是，在陈旧背景图上大幅增加推演计算，只会使规划器在自身搜索过的想象海洋上给出的自评持续虚高，而航线在真实海洋中的价值早已饱和\cite{smith2006curse,vanhasselt2010double}。当每次决策的推演次数从64次增至2000次与20万次时，规划器自评从0.762升至0.833和0.917；但所选航线在真实海洋中的价值仅从0.749升至0.793和0.803，在约2000次推演后便饱和，且在不参与搜索的留出海洋上的评判始终紧贴真实价值（图\ref{fig:curse}）。这表明过多算力并未帮航行器看清真实赤潮位置，而是被用来迎合有限想象样本中的偶然高值噪声。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_curse}
\caption{前期东海赤潮巡测研究揭示的机载过度计算现象。(a) 所选航线价值（对数叶绿素浓度）随每次决策想象推演次数（64至20万次）的变化：规划器搜索时的自评从0.762持续升至0.917，而真实价值从0.749升至0.793后在约2000次推演处饱和（20万次时为0.803），留出海洋上的独立评判紧贴真实价值；(b) 估计价值减真实价值的偏差：搜索自评的高估偏差随计算量单调膨胀，留出评判保持无偏，不确定性幅度设错仅引起整体平移。多算只让规划器的答案在旧信息上越来越“精致”，却不能提供区分真实环境的新信息。}
\label{fig:curse}
\end{figure}

前期研究的第二个发现是，在连续平滑的标量场巡测中，计算与观测的时间分配所能改变的结局空间十分有限。出发前预演选出的用时策略平均遗憾为0.265，而事后为每个任务挑最好的用时策略也只能降到0.243，用时分配本身的空间仅约0.022。对遗憾来源的拆解进一步显示，下水位置决定了约0.13的差距，信息新鲜度决定了约0.03，而用时分配仅占约0.02；尝试用前一天光流外推3天反而比直接用旧图误差增大0.018，说明逐日卫星图里没有可外推的整体移动。

这一前期探索促使作者把问题收紧：既然当多个可能世界都与旧图相容、却要求采取不同行动时，继续计算无法将它们区分开来，那么在强海流绕障这种选错一侧就会付出数小时代价的二元拓扑决策中，能否直接检验“是否存在另一个同样合理、却使当前选择明显受损的流场”，并以此决定何时该算、何时该测、何时该保守绕行？这正是本文接下来要解决的问题。


########## ATTACHED FILE: sections/problem.tex (current text, to be rewritten) ##########

\section{问题建模}

\subsection{任务场景与海洋再分析数据}
本文研究自主水下航行器在强流海区携带陈旧粗分辨率海流图执行绕障航行的二元路径决策问题，参数汇总于表\ref{tab:settings}。研究海区取台湾以东至东海的黑潮区（23°--31°N、121°--129°E；第\ref{sec:scope}节另在湾流区与阿古拉斯回流区重复，并改带卫星测高地转流图重复），采用HYCOM全球再分析（GLBy0.08，实验93.0\cite{chassignet2007hycom}）10米水深处的1/12°水平流速场，2019年1月1日至2024年8月29日每3天一张快照共689张；其中2019--2021年作为开发年份（710个任务），2022--2024年作为独立测试年份（623个任务）。每张快照生成2个任务，起终点相距100--140千米、离岸不少于20千米，中点设半径15千米的圆形禁航区，只保留粗图上任务区平均流速不低于0.3米/秒的强流任务。航行器下水时携带3天前生成的1°粗图（格内平均），当天1/12°场作为真实海流。

\begin{table}[htbp]
\centering
\caption{粗分辨率海流图下自主水下航行器航路决策问题的实验设置与参数。}
\label{tab:settings}
\small
\input{tables/route_settings.tex}
\end{table}

\subsection{航线求解与计算预算}
给定水平海流场 $\boldsymbol{u}(\boldsymbol{x})$ 与航行器恒定对水速度 $V = 1.0$ 米/秒，选定绕行一侧 $s \in \{\text{L}, \text{R}\}$（左侧或右侧）后的最快航线由有向图最短路算法求取\cite{dijkstra1959note}。对长度为 $\ell_e$、单位方向为 $\boldsymbol{d}_e$ 的有向边 $e$，以边两端节点海流的平均作为该边的海流，记沿边分量为 $u_{\parallel} = \boldsymbol{u} \cdot \boldsymbol{d}_e$、垂直边分量为 $u_{\perp} = \|\boldsymbol{u} - u_{\parallel}\boldsymbol{d}_e\|$。航行器抵消横流后的对地速度 $v_{\text{g}}(e)$ 与通行时间 $t(e)$ 为：
\begin{equation}
v_{\text{g}}(e) = u_{\parallel} + \sqrt{V^2 - u_{\perp}^2}, \qquad t(e) = \frac{\ell_e}{v_{\text{g}}(e)}.
\label{eq:edge_time}
\end{equation}
当 $|u_{\perp}| \ge V$ 或 $v_{\text{g}}(e) \le 0$ 时该边不可通行。在严格位于禁航区左侧或右侧的子图上求最短路，得两侧最优航时 $T_{\text{L}}(\boldsymbol{u})$ 与 $T_{\text{R}}(\boldsymbol{u})$ 及两侧时间差：
\begin{equation}
\Delta T(\boldsymbol{u}) = T_{\text{L}}(\boldsymbol{u}) - T_{\text{R}}(\boldsymbol{u}),
\label{eq:delta_t}
\end{equation}
其中 $\Delta T(\boldsymbol{u}) < 0$ 表示左侧快。本文设三档求解计算量：粗算（8千米8向）、标准（4千米16向）与精算（2千米32向），按边数计相对计算量为 $1:8:64$。选定一侧后，假设航行器按真实海流 $\boldsymbol{u}_{\text{true}}$ 在该侧以最优方式航行（测试年份更快一侧平均航时39.2小时），从而聚焦于选左侧还是右侧这一二元决策。

\subsection{合理海流集合的参数化建模}
由于3天前的1°粗图 $\boldsymbol{u}_0(\boldsymbol{x})$ 缺失了中尺度切变与流轴演变，我们用流函数生成无散的误差模态，并按多年数据标定的误差大小逐点缩放，构造叠加在粗图之上的合理海流 $\boldsymbol{u}(\boldsymbol{x}; \boldsymbol{z})$：
\begin{equation}
\boldsymbol{u}(\boldsymbol{x}; \boldsymbol{z}) = \boldsymbol{u}_0(\boldsymbol{x}) + \sum_{k=1}^{K} z_k \boldsymbol{m}_k(\boldsymbol{x}), \qquad \boldsymbol{m}_k(\boldsymbol{x}) = \mathbf{S}(\boldsymbol{x})\, \nabla^{\perp}\phi_k(\boldsymbol{x}),
\label{eq:plausible_field}
\end{equation}
其中 $\nabla^{\perp} = (-\partial_y, \partial_x)$，$\{\phi_k\}_{k=1}^{K}$ 为相关长度 $L_{\text{corr}}$ 的高斯相关流函数的前 $K$ 个主模态（保留95\%方差），因而 $\nabla^{\perp}\phi_k$ 处处无散；$\mathbf{S}(\boldsymbol{x})$ 为对角缩放矩阵，使两个流速分量在各点的方差等于开发数据标定的误差方差（缩放后近似无散）；$\boldsymbol{z} = (z_1, \dots, z_K)^{\top}$ 为先验服从标准正态分布的组合系数。给定半径 $r > 0$，合理集合定义为
\begin{equation}
\mathcal{U}(r) = \left\{ \boldsymbol{u}(\boldsymbol{x}; \boldsymbol{z}) \;\middle|\; \|\boldsymbol{z}\|_2 \le r \right\}.
\label{eq:plausible_set}
\end{equation}
半径 $r$ 由开发年份标定（第5.3节），使 $\mathcal{U}(r)$ 恰好包住大多数真实海洋的两侧时间差。

\subsection{可选动作、观测代价与评价指标}
航行器面对粗图 $\boldsymbol{u}_0$ 可在五类动作中选择：（1）同一张粗图上加算：用粗算、标准或照地图走（精算）选更快一侧出发；（2）改变决策准则：在32个合理海流上按期望时间选边，或采取保守（最坏后悔最小）准则；（3）就地取新信息：原地停留测（2小时测12次）、沿途测30千米、沿途测60千米后再决定是否换边，或绕行定点测（去前方40千米内反例与地图差别最大处测量；测流噪声0.05米/秒；测得的海流按线性高斯更新修正模态系数，观测误差在开发年份比较0.08、0.15、0.3米/秒后取0.15米/秒）；（4）上浮取新图：每次耗时1小时接收当天1°图或0.5°图；（5）本文反例检验门控：仅在最坏后悔超阈值时触发门控后取保守或门控后上浮取图。定义任务航时“损失”为实际总耗时 $T_{\text{total}}$ 减去真实更快一侧的航时：
\begin{equation}
\mathcal{L} = T_{\text{total}} - \min\left\{ T_{\text{L}}(\boldsymbol{u}_{\text{true}}),\, T_{\text{R}}(\boldsymbol{u}_{\text{true}}) \right\}.
\label{eq:loss}
\end{equation}

\subsection{问题剖析：为何常规计算与盲目观测难以奏效}
选对绕行一侧依赖禁航区两侧数十千米尺度的海流切变，而3天前1°粗图抹平了这一信息；机载计算只能锐化粗图自身的几何推论，却无法创造缺失的物理信息。这带来两个结构性性质：

第一，粗图上的时间差模糊性源于“数值歧义”与“环境歧义”两类不同机制。当 $|\Delta T(\boldsymbol{u}_0)|$ 很小时，若仅因8千米粗算网格折线失真，换成2千米精算即可看清粗图倾向；但若精算选出某侧 $s_0$ 后，合理集合 $\mathcal{U}(r)$ 内仍存在使另一侧明显更快的流场 $\boldsymbol{u}^*$，继续加密网格也无法判断真实海洋接近 $\boldsymbol{u}_0$ 还是 $\boldsymbol{u}^*$。

第二，是否值得去观测，不取决于是否存在合理反例，而取决于该反例成真会让当前决策多损失多少小时（最坏后悔）以及观测能否触及关键切变区。由于旧粗图误差相关长度达数十千米，几乎任何任务都能找到某个让另一侧略快的合理流场；唯有直接求出所选一侧的最大可能航时劣势并与观测代价比较，才能避免过度反应。


########## ATTACHED FILE: sections/method.tex (current text, to be rewritten) ##########

\section{方法}

本文提出如图\ref{fig:overview}(d)所示的四步决策方法：先通过按需精算消除数值歧义，再在多年海洋大数据标定的合理集合内用投影梯度上升搜索最坏合理反例，最后依据最坏后悔执行门控分流。

\subsection{按需精算：数值歧义的快速识别与消除}
区分求解器误差与环境不确定性的首要原则，是仅当粗算时间差落在数值离散误差容限之内时才动用精算。常规确定性规划要么一律使用粗算而在两侧航时接近时受网格锯齿误导，要么对所有任务一律执行耗时64倍的精算，在粗图上两侧本就相差十几个小时的任务上浪费算力。

我们在开发年份任务上离线对比同一张粗图 $\boldsymbol{u}_0$ 的粗算时间差 $\Delta T_{\text{coarse}}(\boldsymbol{u}_0)$ 与精算时间差 $\Delta T_{\text{fine}}(\boldsymbol{u}_0)$，取绝对偏差 $|\Delta T_{\text{coarse}}(\boldsymbol{u}_0) - \Delta T_{\text{fine}}(\boldsymbol{u}_0)|$ 的95\%分位数作为数值误差容限 $\tau_{\text{num}} = 3.2$ 小时。在线执行时，航行器先用粗算求 $\Delta T_{\text{coarse}}(\boldsymbol{u}_0)$；若 $|\Delta T_{\text{coarse}}(\boldsymbol{u}_0)| \ge \tau_{\text{num}}$，直接采纳粗算结果；仅当 $|\Delta T_{\text{coarse}}(\boldsymbol{u}_0)| < \tau_{\text{num}}$ 时才判定存在数值歧义并触发精算，以很小的平均算力确保地图基准选择 $s_0$ 不受求解器粗糙度误导。

\subsection{反例检验：基于包络定理的合理集合投影梯度搜索}
判断粗图所选一侧 $s_0$ 是否面临严重环境歧义，最直接的准则是主动在合理集合 $\mathcal{U}(r)$ 内寻找使 $s_0$ 相比另一侧 $\bar{s}_0$ 尽可能变慢的最坏合理反例，而非在少数随机样本上求平均。现有集合规划通常随机抽取32个流场样本统计航时均值或翻转比例\cite{wang2016path}；然而，翻转比例只反映有多少样本翻转了决定，不反映翻转后损失有多大；而两侧时间差只对少数扰动方向敏感，随机样本要很多才能把这些方向上的效应估准（第\ref{sec:budget}节）。

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


########## ATTACHED FILE: sections/experiments.tex (current text, to be rewritten) ##########

\section{实验}

本节利用黑潮区域六年的高分辨率再分析数据（第\ref{sec:scope}节另加湾流区与阿古拉斯回流区），依次回答六个问题：（1）3天前的1°粗图错在哪里，其误差是否具备可由大数据标定的物理结构？（2）单纯增加计算量能否消除选边错误，环境歧义有多普遍？（3）五类策略中哪种能真正降低航时损失？（4）损失集中在哪些任务上，最坏后悔为何优于集合翻转比例，何时值得去观测？（5）与随机合理场相比，反例搜索在算力上省下了什么？（6）当海流图变好、航行器变慢、更换误差模型、换至其他强流海区或改带真实卫星海流图时，方法的适用范围如何？

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
在五类响应策略的对比中，唯有基于合理集合控制尾部风险的保守准则与本文的门控后取保守策略显著降低了平均航时损失，而单纯加算、按期望时间选边与就地测流均未能显著改善结果（图\ref{fig:main}）。在测试年份上，照地图走（精算）的平均损失为0.98小时；改用32个合理场的按期望时间准则或门控后按期望时间，与精算地图的配对差置信区间均包含0，原因在于32个随机合理场数量太少、均值的抽样误差过大（见第\ref{sec:budget}节）。相反，门控后取保守将测试年份平均损失降至0.70小时，与照精算地图走的配对差为$-0.28$小时，95\%置信区间为$[-0.51, -0.07]$（不含0），相对损失降低28\%。门控后取保守之所以奏效，是因为在保守规则实际改选另一侧的41个任务中，有23个改对且平均每次省下10.1小时，18个改错但平均每次仅多花3.3小时——被避开的一侧往往具有很大的下行风险，改对的收益远大于改错的代价。同时，一律取保守的平均损失为0.72小时（与精算地图之差的置信区间亦不含0），门控后取保守与之相近：这表明不观测时的核心收益来自反例搜索给出的最坏后悔准则本身，而门控的作用在于锁定高风险任务，在调用有代价的上浮观测时将平均损失从总是上浮取0.5°图的1.22小时降至门控后上浮取图的0.78小时。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_main}
\caption{测试年份623个强流任务上五类响应策略的平均航时损失（竖直虚线为照精算地图走的0.98小时，各策略的数值标在点旁）。五组从上至下依次为：同一张粗图上加算、不取新信息而改变决策准则、就地取新信息、总是上浮取新图（每次计1小时）、本文的反例检验门控分流。只有基于合理反例最坏后悔的保守与门控策略显著降低了损失，单纯加算与就地测流均难以奏效。}
\label{fig:main}
\end{figure}

\subsection{损失集中在哪里、何时值得观测}
航路决策的航时损失高度集中在少数尾部任务上，反例最坏后悔之所以有效，是因为它比集合翻转比例和地图时间差更能把大损失任务排在前面。若只论能否区分“是否选错且多花1小时以上”而不论多花多少，三种排序指标的区分能力其实相近；但考察排在前20\%的任务所捕获的地图总损失比例时，按反例最坏后悔达67\%，明显高于32个合理场翻转比例的49\%与地图两侧时间差的34\%（图\ref{fig:risk}(a)）。在门控阈值8小时下，被标记的47\%任务囊括了82\%的地图总损失，因为最坏后悔直接度量了不利流场造成的航时差，而非将小损失翻转与十几个小时的大损失翻转同等看待。

各类观测手段的成败则取决于观测视野与时间代价的权衡。就地原位测流均未能带来显著净收益（与精算地图之差的置信区间或显著为正、或包含0）：原地停留测耗去2小时却只测到起点一处；绕行定点测平均要先花15.4小时才能赶到前方测点，得不偿失；沿途测30千米后换边的任务仅占3.4\%（其中81\%换对），说明出发后前30千米测到的海流很少足以改变对两侧的判断，而沿途测60千米后换边的任务虽增至18.8\%，但由于已深入半程、折返代价过大，换边只有15\%是划算的。对于能更新全局流场的上浮取当天0.5°图（图\ref{fig:risk}(b)），当单次上浮代价为0.5小时时，门控后上浮取图的平均损失为0.55小时，优于门控后取保守的0.70小时；而当上浮代价升至1.0小时时，门控后上浮取图升至0.78小时，交点出现在0.5至1小时之间（近1小时），此后无需观测的门控后取保守成为更优选择。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_risk}
\caption{黑潮测试年份的风险排序与上浮观测代价。(a) 按不同风险指标从高到低排序时，排在前面的任务累计占地图总损失的比例：排名前20\%的任务中，反例最坏后悔占67\%，明显高于32个合理场的翻转比例（49\%）与地图两侧时间差（34\%）；(b) 平均损失随单次上浮取当天0.5°图的时间代价（0--4小时）的变化：总是上浮随代价线性变差，门控后上浮在代价低于约1小时时最优，代价更高时门控后取保守最优。}
\label{fig:risk}
\end{figure}

\subsection{反例搜索省下了什么：与随机合理场的比较}
\label{sec:budget}
在决定选哪一侧时，反例搜索的优势在于以约1/29的求解次数达到与上千个随机合理场平均同等的降损效果。理论推导与逐任务核对表明，选最坏后悔更小的一侧等价于按合理集合给出的两侧时间差范围的中点选边；若两侧时间差随海流线性变化，中点即等于地图值，只有当一侧的最不利情形比另一侧严重得多时保守选择才会改选。测试年份实验（图\ref{fig:budget}(a)）显示，按期望时间选边随随机合理场数量增加而改善：用32个合理场时，其平均损失显著高于反例搜索后取保守（配对差的置信区间不含0），因为均值的抽样误差（中位数2.4小时）大于它要估计的修正量（中位数1.7小时），改选多由抽样噪声驱动；直到数百个合理场以上两者差异才不再显著，1024个合理场（2048次求解）的平均损失为0.71小时，与仅需约71次求解的反例搜索后取保守（0.72小时）相当，开发年份两者之差亦不显著。

在识别高风险任务时，排序有效的关键在于度量损失大小，而非翻转频率。测试年份中（图\ref{fig:budget}(b)），按随机合理场算出的期望后悔排在前20\%的任务，在32个场时已占地图总损失的65\%，接近反例搜索最坏后悔的67\%；翻转比例则即使用1024个随机合理场也只有44\%。因此，只要度量的是坚持地图一侧会多花多少航时，数十个随机合理场的期望后悔已能较好地排出危险任务；反例搜索为算力受限的航行器省下的，是做出正确选边所需的上千次航线求解。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_budget}
\caption{随机合理场数量与反例搜索在选边决策和风险排序上的对比（测试年份）。(a) 平均航时损失随每个任务求解次数的变化：曲线为在 $n$ 个随机合理场上按期望时间选边（每次需 $2n$ 次求解），单点为反例搜索后取保守（约71次求解），水平虚线为照精算地图走（0.98小时）；(b) 按不同风险指标排名前20\%的任务所占地图总损失比例随求解次数的变化：两条曲线分别为同样随机合理场上的期望后悔与翻转比例，单点为反例搜索的最坏后悔（67\%），水平虚线为地图两侧时间差（34\%）。反例搜索以约1/29的求解次数达到了上千个随机合理场平均的选边效果，而风险排序的优劣取决于是否度量损失大小，而非样本数量。}
\label{fig:budget}
\end{figure}

\subsection{适用范围与消融分析}
\label{sec:scope}
表\ref{tab:scope}进一步检验了不同先验地图、航速、误差模型以及另外两个强流海区下的适用边界。第一，当航行器直接携带当天0.5°图时，存在合理反例的任务降至64.5\%，精算地图平均损失仅0.17小时，门控后取保守自动退化为绝大多数时候照地图走（损失同为0.17小时，配对差置信区间含0），不产生负向干扰。第二，当航行器对水速度降至0.75米/秒时，选错一侧的代价被显著放大，精算地图平均损失升至2.43小时；门控后取保守将损失降至1.80小时（但配对差置信区间包含0，统计上不显著），而由于选错代价变大、上浮相对更划算，门控后上浮取图将损失进一步降至1.32小时。第三，在消融实验中，若改用历史相似日的小尺度差构造合理集合，门控后取保守的平均损失为0.95小时，相比精算地图的0.99小时几乎失去纠错能力（配对差置信区间含0）。两组的反例搜索方法完全相同，差别只在“合理”如何定义：由多年数据标定误差大小与相关长度的合理集合，能够指出真正危险的一侧，而拼装历史相似日的小尺度差则不能。

第四，在北大西洋湾流海区（33°--41°N、75°--67°W）的重复实验中，“计算消除不了环境歧义”“最坏后悔能找出损失所在”与“门控后去观测”三条结论均得到复现。该实验采用同一再分析产品、深度、年份划分与流程，半径与阈值由湾流开发年份重新标定。湾流的旧粗图误差更大，照精算地图走的平均损失达3.56小时；加算64倍改变了22个任务的选择，其中8个改对、14个改错；门控后上浮取当天0.5°图将平均损失降至1.31小时（与精算地图之差的置信区间不含0），也优于总是上浮取图。

然而，不观测直接改选保守一侧在湾流未能复现：门控后取保守的平均损失为4.00小时，与精算地图之差的置信区间包含0。原因在于湾流测试任务中有8.7\%在真实海流下有一侧因顶流过强而不可通行（黑潮为1.0\%）；这类任务的合理集合内既有堵死左侧、也有堵死右侧的流场，两侧最坏后悔同时接近上限，选较小的一侧近于随机，共有5次改选误入真实不可通行的一侧。看过测试结果后所做的事后检验（非预先设定）表明，若仅在两侧最坏后悔之差超过数值误差容限时才改选，湾流的损失回到3.45小时，与照地图走无显著差别，而黑潮仍保留大部分收益。这提示：合理反例检验能可靠地判断粗图何时不可信，此时去观测是稳健的回应；不观测的保守改选可能只在两侧最坏情形差别分明时有效，下面在第三海区检验这一点。

第五，在阿古拉斯回流区（35°--43°S、14°--22°E）的第三海区独立检验中，加算无效、风险排序与门控后观测三条结论再次成立，而改进规则无害但无显著收益。该检验的计划在下载数据之前写定且未作改动，专门检验湾流实验后提出的改进规则（仅当两侧最坏后悔之差超过数值误差容限时才改选，不引入新参数）；半径与阈值由该区开发年份标定，测试年份只评价一次。预先写定的五项判定结果为：改进规则与精算地图之差为$-0.16$小时，置信区间含0；原门控后取保守同样不显著（该区16.2\%的任务有一侧不可通行）；门控后上浮取当天0.5°图将平均损失从6.87小时降至2.20小时，置信区间不含0；加算64倍后选错率不变（16个选择改对、16个改错）；最坏后悔排前20\%的任务占地图损失的53\%，高于翻转比例的36\%。此外，沿途测30千米在该区也显著降低了损失。纵观三个海区，一致成立的是：计算消除不了环境歧义，合理反例几乎处处存在，最坏后悔能找出损失所在，被门控标记后去观测有回报；不观测的保守改选只在黑潮显著有效，改进规则使它在其他海区无害，但没有带来显著收益。因此，门控的核心价值在于决定何时去观测，不观测时的保守改选是因海区而异的后备手段。

第六，航行器改带真实卫星海流图时，加算无效与最坏后悔风险排序两条结论依然成立，而各种响应的收益缩小且不再显著。该检验在黑潮区进行：航行器带3天前的0.25°近实时融合卫星测高地转流图，上浮取当天的同一产品，另以当天0.5°模式图作理想参照；“真实海洋”仍为再分析场；误差模型、半径与阈值在开发年份由“测高图减再分析场”标定（该产品有一次长时间中断，地图比预定日期老1天以上的快照在看到结果前即被排除）；检验计划在下载卫星数据之前写定。五项预设判定中三项成立：加算后选错率只降0.3个百分点；最坏后悔排前20\%的任务占地图损失的67\%，高于翻转比例的52\%；改进规则的点估计不高于照地图走（置信区间含0）。两项不成立：存在合理反例的任务为81.0\%，低于预设的90\%；门控后上浮取当天0.5°模式图的置信区间含0。照精算地图走的选错率为19.6\%，换成当天的测高图仍有18.5\%，换成当天0.5°模式图则降至8.6\%，说明测高图与再分析场之差主要是两种产品之间的系统差，而非时效。由此，加算无效与风险排序不依赖“粗图与真实海洋同源”的设置；主设置中门控后取保守的显著收益，则未能在真实卫星图下复现。

\begin{table}[htbp]
\centering
\caption{不同海流图、航行器速度、合理集合构造方法与海区下的适用范围与消融实验结果（测试年份；损失单位：小时；门控后上浮取图指取当天0.5°图）。}
\label{tab:scope}
\small
\input{tables/route_scope.tex}
\end{table}

\subsection{局限性讨论}
本研究存在五方面局限：第一，单次任务求解将海流快照视为定常二维场，尚未耦合约40小时航行中的流场时变；第二，主实验的旧粗图由同一再分析场平均与滞后得到，尽管第\ref{sec:scope}节改用真实的卫星测高地转流图重复了检验，但“真实海洋”仍取当天1/12°再分析场，且再分析场仍平滑了亚中尺度过程与内波扰动；第三，将绕障简化为单个圆形禁航区的左右二元决策，未扩展至多岛礁群的多分支同伦类；第四，假设选定一侧后航行器能按真实海流以最优轨迹航行，以剥离底层轨迹跟踪误差、专门评估顶层选边决策；第五，不观测的门控后取保守只在黑潮主设置下显著降低损失，在另两个海区与真实卫星图下均不显著（第\ref{sec:scope}节），此时应依靠门控触发观测来消解环境歧义。


########## ATTACHED FILE: sections/innovation.tex (current text, to be rewritten) ##########

\section{原创创新点拆解}

本研究从《海洋大数据技术原理与应用》课程核心议题出发，经历了问题提出、实证证伪与问题锐化的完整演进。课上讲授的“海洋大数据的计算引擎”使作者联想到：自主水下航行器端侧的算力与能量十分有限，计算、测量与运动之间必须权衡。作者最初提出的问题是：当航行器带着几天前的旧卫星图下水时，应把时间花在继续机载推演上，还是停下来重新观测？在东海赤潮巡测前期研究（第3节）中，我们发现增加推演计算只会让规划器在想象模型里自评虚高，真实收益早已饱和，且平滑标量场中用时分配的改进空间仅约0.02，远小于下水位置与地图新鲜度的影响。针对前期方法增益小、新意不足的缺陷，作者将问题锐化并转向强海流绕障这一选错一侧就损失数小时的二元决策：当存在多个与旧图同样相容、却要求采取相反行动的海洋状态时，再多计算也无法区分；能否在历史大数据界定的合理流场范围内，专门搜出一个让另一侧更好、且使当前选择明显受损的合理反例？这一追问直接催生了本文的合理反例检验框架（表\ref{tab:innovation}）。

\begin{table}[htbp]
\centering
\caption{本文核心原创创新点、已有做法对比、实验证据与局限拆解。}
\label{tab:innovation}
\footnotesize
\begin{tabular}{@{}p{0.13\linewidth}p{0.20\linewidth}p{0.22\linewidth}p{0.19\linewidth}p{0.14\linewidth}@{}}
\toprule
创新点 & 已有做法及其不足 & 本文做法 & 证据（图表） & 局限 \\
\midrule
1. 分离数值歧义与环境歧义的决策判据 & 确定性规划在粗图上盲目加密网格（误以为多算能消除一切模糊）；传统元推理只管何时停止搜索，不区分误差源于求解器还是环境模型失真。 & 提出数值歧义（小于粗精网格容限 $\tau_{\text{num}}$，靠按需精算消除）与环境歧义（合理集合内存在翻转决策的反例，只能靠新信息或保守应对）的二分准则。 & 图\ref{fig:overview}、图\ref{fig:curse}、图\ref{fig:ambiguity}(a)：64倍精算仅将选错率从21.7\%降至19.7\%，当天0.5°图则降至10.4\%。 & 仅在左右绕障的二元拓扑决策上验证，尚未扩展至多分支同伦路径。 \\
\addlinespace
2. 基于包络定理梯度的合理反例主动搜索 & 随机合理场按期望时间选边需上千个样本（约2048次求解）才能压住抽样噪声，32个样本时改选多为噪声；翻转比例只计翻转多少而不计损失多大。 & 利用包络定理沿当前最快航线累加流速导数，一次梯度仅需2次最短路求解；先沿初始梯度跳至球面再投影细化，直接求最坏后悔。 & 图\ref{fig:risk}(a)、图\ref{fig:budget}：约71次求解即达到1024个随机合理场（2048次求解）的选边效果；最坏后悔与期望后悔排前20\%的任务均捕获约三分之二的损失，明显高于翻转比例（44\%--49\%）。 & 随机合理场的期望后悔已能较好地排序风险任务，故反例搜索的优势集中在减少选边所需的求解次数；大扰动下最短路拓扑可能跳变，局部梯度近似会产生折耗。 \\
\addlinespace
3. 海洋大数据驱动的合理集合与半径标定 & 若凭经验设定不确定性集合的形状与半径，会脱离海洋物理结构，易过度保守或漏报黑潮切变。 & 用三年历史再分析误差标定各点误差大小（缩放矩阵 $\mathbf{S}(\boldsymbol{x})$）与76千米相关长度的无散流函数模态；以覆盖90\%以上真实两侧时间差标定最小半径 $r=1.5$。 & 图\ref{fig:data}、图\ref{fig:ambiguity}(b)、表\ref{tab:scope}：$r=1.5$在测试年份覆盖94\%真实差值；消融替换为历史相似日差值后保守增益消失（0.99 vs 0.95小时）。 & 依赖多年历史再分析数据标定平稳统计量，对台风过境等非平稳极端天气适应受限。 \\
\addlinespace
4. 权衡最坏后悔与观测代价的门控响应 & 自适应采样面向全场降方差去测流，或不论代价一律保守/一律上浮，忽视了原位测流看不见远方切变及上浮通信本身耗时。 & 以最坏后悔超阈值 $\theta=8$小时作为门控：超标且上浮代价低（$<1$小时）时上浮取新图，代价高或仅有原位测流时改选最坏后悔更小一侧。 & 图\ref{fig:main}、图\ref{fig:risk}(b)、表\ref{tab:scope}：黑潮区门控后取保守将平均损失从0.98降至0.70小时，上浮代价切换点约1小时；湾流区与阿古拉斯回流区门控后上浮取图分别将损失从3.56降至1.31小时、从6.87降至2.20小时。 & 不观测的保守改选在湾流与阿古拉斯回流区这类两侧都可能被强流堵死的海区均无显著收益，此时须靠门控触发观测；黑潮区改带真实卫星图后其收益也不再显著。 \\
\bottomrule
\end{tabular}
\end{table}

在人机协同完成本研究的过程中，作者与人工智能工具的分工如下（详见附录B，对话记录见代码仓库）。作者提出了最初关于机载计算与观测如何权衡的问题；在第一版结果出来后要求改用真实卫星数据检验、补充对照与消融实验；在前期研究结果出来后指出用时分配增益过小、方法新意不足，并提出了“两条航路、一张粗图、能否找到让另一条路更好的合理海流反例”这一新问题，决定转向本文的研究。人工智能助手Claude（Anthropic）完成了文献检索、代码、实验与作图，并核对了正文中的数字与引用；Gemini（Google）根据Claude整理的事实清单与提纲撰写了论文文字。


########## ATTACHED FILE: sections/conclusion.tex (current text, to be rewritten) ##########

\section{结论}

本文针对自主水下航行器在粗分辨率海流图下执行强流绕障时的在线元决策问题，提出了基于海洋大数据标定的合理反例检验方法，阐明了一条基本原理：机载计算的职责是消除求解器近似带来的数值歧义，从而读出已有海流图的本来倾向；而当多年海洋大数据界定的合理集合内存在翻转航路优劣并造成严重航时损失的合理反例时，环境处于算力无法消解的环境歧义状态，航行器应通过门控引入大尺度观测，不观测时改选最坏后悔更小的一侧只是因海区而异的后备手段。在黑潮区域六年再分析海流的系统实验表明，将航线求解算力提高64倍仅使选错率从21.7\%降至19.7\%；反例搜索以约71次求解达到按期望时间选边使用约1024个随机合理场（2048次求解）时的效果，其最坏后悔将67\%的地图总损失集中在排名前20\%的任务中，门控后取保守将平均航时损失从0.98小时降至0.70小时。湾流区与阿古拉斯回流区的重复实验表明，加算无效、最坏后悔风险排序以及门控后上浮取图（平均损失分别从3.56小时降至1.31小时、从6.87小时降至2.20小时）跨海区成立，而不观测的保守改选在这两个海区均无显著收益；黑潮区改带真实卫星测高地转流图的检验表明，加算无效与风险排序不依赖“粗图与真实海洋同源”的设置，而门控后取保守的收益在真实卫星图下不再显著。未来工作将把该方法扩展至随时间演变的流场，并结合实艇开展海上试验。


########## ATTACHED FILE: sections/appendix.tex (current text, to be rewritten) ##########

\section*{附录}

\subsection*{附录 A：代码与数据开源说明}
本研究的全部源代码、数据处理脚本、实验配置、统计汇总程序以及论文图表生成脚本均已开源于代码仓库：\url{https://github.com/frankxucd0826-source/auv-compute-or-observe}。

\begin{enumerate}
    \item \textbf{数据集来源：}主实验海流数据取自HYCOM全球海洋再分析公开服务（产品GLBy0.08，实验93.0，10米水深水平流速，区域23°--31°N、121°--129°E，2019--2024年；重复实验区为湾流33°--41°N、75°--67°W与阿古拉斯回流区35°--43°S、14°--22°E，产品与时间范围相同；卫星地图检验所用的近实时融合测高地转流取自美国国家海洋和大气管理局海岸观测网数据服务）；第3节前期研究的叶绿素与海表温度数据取自美国国家海洋和大气管理局海岸观测网数据服务的公开卫星产品。
    \item \textbf{主要程序结构：}核心软件包 \texttt{src/oceanroute/} 包含网格最短路与包络定理梯度求解器（\texttt{solver.py}）、海流快照与粗图（\texttt{fields.py}，海区由环境变量 \texttt{OCEANROUTE\_REGION} 选择）、旧粗图误差的多年数据标定与无散误差模态（\texttt{errormodel.py}）以及任务生成、反例搜索与测量更新（\texttt{mission.py}）；数据下载、批量评估、统计汇总、随机合理场对照与湾流实验分别由 \texttt{scripts/download\_hycom.py} 与 \texttt{experiments/route\_*.py} 完成，正文插图由 \texttt{paper/figures/fig\_route\_*.py} 生成；逐条复现命令与前期研究的脚本见仓库根目录的 \texttt{README}。
\end{enumerate}

\subsection*{附录 B：人工智能工具使用说明}
本研究与论文撰写中人工智能工具的使用情况如下：
\begin{enumerate}
    \item \textbf{作者：}提出了机载计算与现场观测如何权衡的初始问题；对第一版结果提出用真实卫星数据检验、补充对照与消融、按学术论文格式写作等要求；在前期研究结果出来后指出其提升小、新意不足，并提出“粗分辨率海流图下两条航路的合理反例”这一新问题，决定转向本文研究；对全文负责。
    \item \textbf{Claude（Anthropic）：}在作者授权下完成文献检索与核对、数据下载与全部代码、实验与统计、论文插图，整理写作提纲与由实验程序生成的事实清单，并逐项核对正文中的数字与引用。
    \item \textbf{Gemini（Google）：}根据Claude整理的提纲、术语表与事实清单撰写论文文字，再由Claude核对与修改。
    \item \textbf{可追溯性记录：}作者与人工智能工具的对话记录、与Gemini的每轮写作往来以及研究笔记均保存在上述代码仓库中（涉及作者其他未发表工作的内容已隐去）。
\end{enumerate}
```

</details>

## Gemini 的回复

<details><summary>展开（共 26629 字符）</summary>

```
===== FILE: sections/title.tex =====
合理反例检验：粗分辨率海流图下自主水下航行器何时计算、何时观测

===== FILE: sections/abstract.tex =====
{\heiti 摘要：}
自主水下航行器携带3天前的1°粗分辨率海流图（下称粗图）绕越禁航区时，必须从左侧或右侧通行；选错一侧将付出数小时的额外航时。为此，本文提出基于多年再分析数据标定的合理反例检验，区分两类不确定性：求解网格过粗造成的数值歧义可通过增加计算消除；而粗图同时容许左侧更快与右侧更快流场的环境歧义则无法靠计算消解，必须补充新信息。该方法在多年误差统计划定的合理流场集合内，利用包络定理梯度搜索使另一侧更快的合理反例及当前选择的最大后悔值，并以阈值判据识别粗图何时不可信。在黑潮主设置、湾流、阿古拉斯回流区及黑潮区改带卫星测高地转流图四种设置下的实验一致表明：（1）增加计算无法纠正选边错误，64倍计算量仅使黑潮选错率从21.7\%变为19.7\%；（2）最大后悔值排名前20\%的任务集中了53\%--71\%的额外航时，优于改变选边的成员比例（36\%--52\%）与粗图左右航时差，且仅需约71次航线求解即达到集合平均选边使用1024个集合成员（2048次求解）的效果；（3）判定粗图不可信时获取新信息收益最大，超阈值时上浮取图将湾流和阿古拉斯回流区的平均额外航时分别从3.56降至1.31小时、从6.87降至2.20小时，在黑潮主设置中单次上浮代价低于约1小时时同样划算。不观测而仅在超阈值时保守改选仅在黑潮主设置显著有效（额外航时从0.98降至0.70小时），在改带卫星测高地转流图时各类响应均不显著。

{\heiti 关键词：}海洋大数据；自主水下航行器；航路规划；合理反例检验；最大后悔值；不确定性量化

\vspace{1em}
\begin{center}
{\large\bfseries Plausible Counterexample Test: When an Autonomous Underwater Vehicle Should Compute and When It Should Observe Under a Coarse Current Map}
\end{center}
\vspace{0.5em}

{\bfseries Abstract:}
An autonomous underwater vehicle carrying a three-day-old 1° coarse current map must pass a no-go zone on the left or the right; choosing the wrong side adds hours of extra time. We propose a plausible counterexample test calibrated from multi-year reanalysis errors to separate two kinds of ambiguity: numerical ambiguity from a coarse solver is removed by computing more, whereas environmental ambiguity—where the map is consistent with currents favouring either side—requires new information. Within the plausible set of currents consistent with the map, our method uses envelope-theorem gradients to search for a counterexample that makes the other side faster and to compute the maximum regret of the current choice; a threshold on maximum regret then flags when the map cannot be trusted. Experiments across four settings (Kuroshio main setting, Gulf Stream, Agulhas retroflection, and Kuroshio with a satellite altimetry geostrophic map) show three consistent findings: (1) computing 64 times more barely changes the wrong-side share (21.7\% to 19.7\% in the Kuroshio); (2) the top 20\% of missions ranked by maximum regret contain 53\%--71\% of all extra time, outperforming the share of ensemble members changing the choice (36\%--52\%) and the map time difference, while needing about 71 route solves to match the side choice of an ensemble average over 1024 members (2048 solves); (3) once a mission is flagged, new information pays most: surfacing for today's 0.5° map cuts mean extra time from 3.56 to 1.31 hours in the Gulf Stream and from 6.87 to 2.20 hours in the Agulhas, and pays in the Kuroshio when surfacing costs under about 1 hour. Choosing the smaller-regret side without observing helps significantly only in the Kuroshio main setting (0.98 to 0.70 hours), and no response is significant under the satellite map.

{\bfseries Keywords:} ocean big data; autonomous underwater vehicle; path planning; plausible counterexample test; maximum regret; uncertainty quantification

===== FILE: sections/intro.tex =====
\section{引言}

自主水下航行器（下称航行器）在强流区执行长航程任务时，受限于水下声学通信带宽与机载电池能量，必须在继续机载计算、补充现场观测与立即行动之间做出权衡\cite{chassignet2007hycom,chin2017mur,remus100,jetsonorinnx}。传统方法将计算资源分配与信息收集分开处理\cite{horvitz1987reasoning,russell1991right,sung2021quit,magnino2026metareasoning}，但在海洋环境中，何时停止计算、何时获取新信息，取决于航行器所面临的不确定性究竟源于算法求解粗糙，还是源于环境信息缺失。

当航行器携带3天前的1°粗分辨率海流图（下称粗图）绕越禁航区时，从左侧或右侧通行是不可逆的二元决策，选错一侧将导致数小时的额外航时（实际航时减去真实更快一侧的航时）。长航程航行器对水速度约为1.0米/秒，与强流区流速相当；粗图既抹平了中尺度涡旋切变，又存在3天的时效滞后。如图\ref{fig:overview}所示的2022年1月18日任务，粗图上左侧与右侧航时仅差约0.3小时且左侧略快，但在当天1/12°再分析海流场（下称真实海流）中，右侧实际比左侧快11.7小时。

面对此类决策，现有三类常规策略均存在不足。首先，确定性规划通过加密求解网格来增加计算\cite{lolla2014levelset}，但这只能减小粗图上的离散误差，无法补充缺失的涡旋信息\cite{smith2006curse,jiang2015horizon,cuadron2025overthinking}。其次，集合规划在数十个随机扰动流场（下称集合成员）上通过集合平均选边或统计改变选边的成员比例\cite{wang2016path,subramani2018stochastic,kularatne2018forecast}；然而有限抽样的均值噪声较大，且改变选边的成员比例只统计有多少成员改选，不度量改选背后的航时差大小，难以识别高代价任务\cite{lin2015metareasoning,elboher2023formal,benhaim2006infogap,marx2020predictive}。最后，自适应采样致力于降低全场估计方差\cite{srinivas2012gpucb,hollinger2014sampling,fossum2019}，但对全场重构有用的测量未必能区分左右两侧的快慢\cite{chernoff1959sequential,box1967discrimination,garivier2016optimal,attia2018goal}。

为此，本文区分两类歧义并提出“合理反例检验”。第一类是数值歧义，即粗图上左右航时差（左侧最快航时减右侧最快航时）小于求解误差，此时加密网格计算即可看清粗图本意；第二类是环境歧义，即粗图同时容许“左侧更快”和“右侧更快”的真实海流，此时继续计算无济于事，必须补充新信息或做保守决策。本文利用多年历史再分析误差标定以粗图为中心的不确定集——合理流场集合（简称合理集合），在其中主动搜索使另一侧更快的流场（合理反例），并计算坚持当前选择可能多付出的最大航时（最大后悔值）。一旦最大后悔值超过阈值判据，即判定粗图对本次决定不可信，进而触发上浮获取新图或保守改选。

在黑潮主设置、湾流、阿古拉斯回流区以及黑潮区改带卫星测高地转流图四种实验设置下，本文得到三项一致的正面发现：
\begin{enumerate}
    \item 单纯增加计算无法消除选边错误：将求解计算量增加64倍后，选错一侧的任务比例几乎不变（黑潮主设置仅从21.7\%变为19.7\%，其余三种设置同样如此）。
    \item 最大后悔值能准确锁定高风险任务且计算高效：按最大后悔值排名前20\%的任务集中了53\%--71\%的额外航时，高于按改变选边的成员比例（36\%--52\%）或按粗图左右航时差排序；同时，合理反例检验仅需约71次航线求解，即可达到集合平均选边使用1024个集合成员（2048次求解）的选边效果。
    \item 阈值判据判定粗图不可信时，获取新信息回报最高：超阈值时上浮取图将湾流和阿古拉斯回流区的平均额外航时分别从3.56小时降至1.31小时、从6.87小时降至2.20小时；在黑潮主设置中，当单次上浮代价低于约1小时时，超阈值时上浮取图同样优于不观测策略。
\end{enumerate}

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_overview}
\caption{粗图下的航路决策与合理反例检验（2022年1月18日任务）。(a) 3天前1°粗图，左侧37.7小时、右侧38.0小时，按粗图选左侧；(b) 合理集合内搜出的合理反例，左侧55.7小时、右侧44.1小时；(c) 当天1/12°真实海流，右侧实际快11.7小时；(d) 决策流程：先消除数值歧义，再算最大后悔值并按阈值判据触发上浮取图或保守改选。}
\label{fig:overview}
\end{figure}

本文的主要贡献如下：
\begin{itemize}
    \item 据我们所知，本文首次在自主水下航行器航路决策中分离了可由计算消除的数值歧义与需靠新信息应对的环境歧义，提出了以最大后悔值为核心的合理反例检验与阈值判据。
    \item 提出基于多年再分析数据标定无散误差模态与合理集合半径的方法，结合包络定理梯度搜索，以约71次航线求解达到了集合平均选边2048次求解的选边效果。
    \item 在四个实验设置、逾两千个测试任务上系统验证了方法，证实增加计算无效、最大后悔值排序与超阈值时上浮取图跨海区成立，并界定了不观测时超阈值保守改选的适用范围。
\end{itemize}

本文其余部分安排如下：第2节回顾相关工作，第3节简述前期研究，第4节建立问题模型，第5节详述合理反例检验方法，第6节报告实验结果与适用范围，第7节拆解创新点，第8节总结全文。

===== FILE: sections/related.tex =====
\section{相关工作}

受限理性与元推理研究旨在评估计算的价值是否超过其时间与能量代价，以此决定何时停止搜索并执行动作\cite{horvitz1987reasoning,russell1991right,xiao2020thinking,sung2021quit,elboher2023formal,magnino2026metareasoning}。然而，当内部环境模型本身存在偏差时，增加搜索深度反而会放大模型误差，诱发决策分析中的“优化器诅咒”或过度思考\cite{smith2006curse,jiang2015horizon,cuadron2025overthinking}；近期智能体推理研究也指出，当外部状态未知时，增加测试时计算无法替代与环境交互\cite{hunt2021formalizing,shen2025thinking,kobalczyk2025active}。不同于仅决定何时停止搜索的元推理，本文将决策模糊性拆解为求解器粗糙引起的数值歧义与粗图失真引起的环境歧义，从而明确何时应加密求解、何时应获取新信息。

序贯实验设计与模型判别理论指出，只有能够区分竞争假设并改变行动的观测才具有决策价值\cite{chernoff1959sequential,box1967discrimination}。最优臂识别、信息导向采样与目标导向实验设计均强调针对具体决策目标收集样本，而非均匀降低全局方差\cite{garivier2016optimal,russo2018thompson,russo2018ids,attia2018goal}；信息间隙决策理论与预测多解性研究进一步表明，当多个与观测相容的模型给出相反结论时，应考察不确定集内的最坏表现\cite{benhaim2006infogap,marx2020predictive}。与离散假设检验或线性反问题不同，本文利用包络定理直接在连续无散海流场上搜索翻转二元选边的合理反例，并以最大后悔值量化环境歧义。

在不确定海洋流场规划中，研究者提出了确定性最短路与水平集方法\cite{dijkstra1959note,lolla2014levelset}、集合规划与随机时间最优控制\cite{wang2016path,subramani2018stochastic,kularatne2018forecast}，以及利用集合卡尔曼滤波或高斯过程在线更新场估计的自适应采样\cite{anderson2001eakf,srinivas2012gpucb,hollinger2014sampling,fossum2019}。然而，现有方法大多在固定集合成员上求平均，或面向全场重构去测量，未回答现有海流图何时不可信以及何时值得付出代价获取新图；本文用多年再分析数据标定合理集合，直接解决“继续计算、上浮观测还是保守选边”的权衡问题。

===== FILE: sections/prior.tex =====
\section{前期研究：多算为何收效甚微}

本文的问题源于作者前期在东海赤潮巡测场景下对机载计算与观测时间分配的探索\cite{lou2014diurnal,mnr2024bulletin}。在该研究中，航行器携带3天前的卫星叶绿素图下水，利用多年数据标定误差并生成48个模拟海洋（32个用于搜索航线，16个作为不参与搜索的检验用模拟海洋）\cite{beckers2003dineof,gaspari1999correlation,deboer2005cem}，以寻找叶绿素高值区。

前期研究首先发现，在陈旧背景图上大幅增加推演次数，只会抬高规划器对自身航线的估值，而航线在真实海洋中的价值早已停止改善\cite{smith2006curse,vanhasselt2010double}。当每次决策的推演从64次增至2000次和20万次时，规划器对自身航线的估值从0.762持续升至0.833和0.917；但真实价值仅从0.749升至0.793和0.803，在约2000次后即不再提高，且在检验用模拟海洋上的得分（0.745、0.794、0.802）始终紧贴真实价值（图\ref{fig:curse}）。这说明过多计算只是在迎合有限模拟海洋中的偶然噪声，无法弥补旧图缺失的信息。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_curse}
\caption{前期东海赤潮巡测研究中的过度计算现象。(a) 航线价值随推演次数的变化：规划器对自身航线的估值持续上升，而真实价值与检验用模拟海洋上的估值在约2000次后饱和；(b) 估计价值减真实价值的偏差：规划器自身估值的高估偏差随计算量单调增大，检验用模拟海洋保持无偏。}
\label{fig:curse}
\end{figure}

前期研究还发现，在平滑标量场巡测中，如何分配计算与测量时间对结果的改变很小。通过出发前模拟选出的时间分配策略平均遗憾为0.265，而事后为每个任务挑选最优策略也只能降至0.243（差距仅0.022，远小于下水位置带来的0.13和信息新鲜度带来的0.03）；用前一天光流外推3天反而使误差增大0.018。

这两点认识促使我们将研究转向强海流绕障这一二元决策：既然面对陈旧粗图时多算无益，那么在选错一侧就会付出数小时额外航时的场景下，能否直接检验“是否存在与粗图相容、却使另一侧更快的合理反例”，并以此决定何时计算、何时观测？

===== FILE: sections/problem.tex =====
\section{问题建模}

\subsection{任务场景与海洋再分析数据}
本文研究航行器携带粗图绕越禁航区时的左右二元选边问题，黑潮主设置的参数汇总于表\ref{tab:settings}。主设置取台湾以东至东海的黑潮区（23°--31°N、121°--129°E），使用HYCOM全球再分析10米水深处的1/12°水平流速场\cite{chassignet2007hycom}，2019年1月1日至2024年8月29日每3天取一张快照共689张；其中2019--2021年为开发年份（710个任务），2022--2024年为测试年份（623个任务）。每张快照生成2个起终点相距100--140千米、中点设半径15千米圆形禁航区的强流任务。航行器携带3天前的1°粗图，当天1/12°场作为真实海流。此外，我们在湾流、阿古拉斯回流区以及黑潮区改带卫星测高地转流图（美国国家海洋和大气管理局近实时融合测高地转流，0.25°）三种设置下开展了同流程检验。

\begin{table}[htbp]
\centering
\caption{黑潮主设置下自主水下航行器航路决策问题的实验设置与参数。}
\label{tab:settings}
\small
\input{tables/route_settings.tex}
\end{table}

\subsection{航线求解与网格精度}
给定水平海流场 $\boldsymbol{u}(\boldsymbol{x})$ 与航行器恒定对水速度 $V = 1.0$ 米/秒，选定绕行一侧 $s \in \{\text{L}, \text{R}\}$（左侧或右侧）后的最快航线由有向图最短路算法求取\cite{dijkstra1959note}。对长度为 $\ell_e$、单位方向为 $\boldsymbol{d}_e$ 的有向边 $e$，记沿边流速分量为 $u_{\parallel} = \boldsymbol{u} \cdot \boldsymbol{d}_e$、垂直边分量为 $u_{\perp} = \|\boldsymbol{u} - u_{\parallel}\boldsymbol{d}_e\|$，则航行器对地速度 $v_{\text{g}}(e)$ 与通行时间 $t(e)$ 为：
\begin{equation}
v_{\text{g}}(e) = u_{\parallel} + \sqrt{V^2 - u_{\perp}^2}, \qquad t(e) = \frac{\ell_e}{v_{\text{g}}(e)}.
\label{eq:edge_time}
\end{equation}
当 $|u_{\perp}| \ge V$ 或 $v_{\text{g}}(e) \le 0$ 时该边不可通行。在禁航区左侧或右侧子图上分别求最短路，得两侧最快航时 $T_{\text{L}}(\boldsymbol{u})$、$T_{\text{R}}(\boldsymbol{u})$ 及左右航时差：
\begin{equation}
\Delta T(\boldsymbol{u}) = T_{\text{L}}(\boldsymbol{u}) - T_{\text{R}}(\boldsymbol{u}),
\label{eq:delta_t}
\end{equation}
其中 $\Delta T(\boldsymbol{u}) < 0$ 表示左侧更快。本文设粗网格求解（8千米8个方向）、中网格求解（4千米16个方向）与细网格求解（2千米32个方向）三档，计算量之比为 $1:8:64$。选定一侧后，航行器按真实海流 $\boldsymbol{u}_{\text{true}}$ 在该侧以最快方式航行。

\subsection{合理流场集合的参数化建模}
为刻画粗图 $\boldsymbol{u}_0(\boldsymbol{x})$ 缺失的中尺度涡旋与流轴摆动，我们用流函数生成无散误差模态，并按历史误差统计逐点缩放，构造合理集合中的流场 $\boldsymbol{u}(\boldsymbol{x}; \boldsymbol{z})$：
\begin{equation}
\boldsymbol{u}(\boldsymbol{x}; \boldsymbol{z}) = \boldsymbol{u}_0(\boldsymbol{x}) + \sum_{k=1}^{K} z_k \boldsymbol{m}_k(\boldsymbol{x}), \qquad \boldsymbol{m}_k(\boldsymbol{x}) = \mathbf{S}(\boldsymbol{x})\, \nabla^{\perp}\phi_k(\boldsymbol{x}),
\label{eq:plausible_field}
\end{equation}
其中 $\nabla^{\perp} = (-\partial_y, \partial_x)$，$\{\phi_k\}_{k=1}^{K}$ 为相关长度 $L_{\text{corr}}$ 的高斯相关流函数前 $K$ 个主模态（保留95\%方差），$\mathbf{S}(\boldsymbol{x})$ 为由开发年份标定的逐点误差标准差对角矩阵，$\boldsymbol{z} = (z_1, \dots, z_K)^{\top}$ 为先验服从标准正态分布的系数向量。给定半径 $r > 0$，合理集合定义为以粗图为中心的不确定集：
\begin{equation}
\mathcal{U}(r) = \left\{ \boldsymbol{u}(\boldsymbol{x}; \boldsymbol{z}) \;\middle|\; \|\boldsymbol{z}\|_2 \le r \right\}.
\label{eq:plausible_set}
\end{equation}

\subsection{可选策略与额外航时指标}
航行器可在五类策略中选择：（1）同一张粗图上改变求解网格，其中在粗图上用细网格求解并选更快一侧作为“基线：按粗图选边”；（2）不观测而改变选边准则，包括集合平均选边（从误差模型抽取集合成员，选平均航时更短的一侧）或直接选最大后悔值较小的一侧；（3）就地测流（原地停留测流、沿途测流30千米、沿途测流60千米、绕行定点测流，测得流速后按线性高斯更新修正模态系数）；（4）总是上浮取当天1°图或上浮取当天0.5°图（每次计1小时）；（5）本文基于合理反例检验的阈值判据响应（超阈值时上浮取图、超阈值时保守改选）。粗图上的选边模糊性源于求解粗糙的数值歧义与流场多解的环境歧义，而是否值得采取行动取决于合理反例造成的最大后悔值是否超过代价。为此，以实际总航时 $T_{\text{total}}$ 减去真实更快一侧航时的“额外航时”作为评价指标（越低越好，已知真实海流时直接选更快一侧的理想上限为0）：
\begin{equation}
\mathcal{L} = T_{\text{total}} - \min\left\{ T_{\text{L}}(\boldsymbol{u}_{\text{true}}),\, T_{\text{R}}(\boldsymbol{u}_{\text{true}}) \right\}.
\label{eq:loss}
\end{equation}

===== FILE: sections/method.tex =====
\section{方法}

本文方法分为四步（图\ref{fig:overview}(d)）：先按需用细网格求解消除数值歧义，再在多年数据标定的合理集合内用包络定理梯度搜索最大后悔值，最后按阈值判据决定是否上浮取图或保守改选。

\subsection{数值歧义的识别与按需细网格求解}
当粗图上的左右航时差很小时，首先要排除粗网格求解带来的折线离散误差。我们在开发年份对比同一张粗图 $\boldsymbol{u}_0$ 上粗网格求解的 $\Delta T_{\text{coarse}}(\boldsymbol{u}_0)$ 与细网格求解的 $\Delta T_{\text{fine}}(\boldsymbol{u}_0)$，取两者绝对差值的95\%分位数作为数值误差容限 $\tau_{\text{num}}$（黑潮主设置为3.2小时）。在线决策时，航行器先做粗网格求解；仅当 $|\Delta T_{\text{coarse}}(\boldsymbol{u}_0)| < \tau_{\text{num}}$ 时才判定存在数值歧义并调用细网格求解，从而以很小的平均计算量确定粗图选边 $s_0$。

\subsection{合理反例检验：基于包络定理梯度的最大后悔值搜索}
为判断粗图所选一侧 $s_0$ 是否面临严重的环境歧义，我们在合理集合 $\mathcal{U}(r)$ 内主动搜索使另一侧 $\bar{s}_0$ 更快、且让选 $s_0$ 多花最多航时的合理反例。在流场 $\boldsymbol{u}(\boldsymbol{z}) \in \mathcal{U}(r)$ 下，选一侧 $s$ 相比另一侧 $\bar{s}$ 多花的航时称为后悔值；合理集合内后悔值的最大值即为决策理论中的最大后悔值 $R_s(r)$：
\begin{equation}
R_s(r) = \max_{\|\boldsymbol{z}\|_2 \le r} J_s(\boldsymbol{z}), \qquad J_s(\boldsymbol{z}) = \max\left\{ 0,\, T_s(\boldsymbol{u}(\boldsymbol{z})) - T_{\bar{s}}(\boldsymbol{u}(\boldsymbol{z})) \right\}.
\label{eq:worst_regret}
\end{equation}
当 $R_{s_0}(r) > 0$ 时，即存在使另一侧更快的合理反例，$R_{s_0}(r)$ 度量了坚持选 $s_0$ 的最大潜在航时劣势。

若用有限差分求航时差对 $K$ 个模态系数的导数，每步迭代需 $2K$ 次最短路求解。本文利用最优化中的包络定理消除了这一开销：当流场微小扰动时，最快航线 $P_s^*(\boldsymbol{z})$ 的节点序列在一阶近似下不变，因此 $T_s(\boldsymbol{u}(\boldsymbol{z}))$ 对系数 $z_k$ 的偏导数等于沿当前最快航线累加各边通行时间对局部流速的导数：
\begin{equation}
\frac{\partial T_s}{\partial z_k} = \sum_{e \in P_s^*(\boldsymbol{z})} \left( \frac{\partial t(e)}{\partial u_{\parallel}} \boldsymbol{d}_e + \frac{\partial t(e)}{\partial u_{\perp}} \boldsymbol{n}_e \right) \cdot \frac{\boldsymbol{m}_k(\boldsymbol{x}_e^{-}) + \boldsymbol{m}_k(\boldsymbol{x}_e^{+})}{2},
\label{eq:envelope_grad}
\end{equation}
其中 $\boldsymbol{x}_e^{-}$、$\boldsymbol{x}_e^{+}$ 为边 $e$ 的两端节点，$\boldsymbol{n}_e$ 为垂直边方向的单位向量，标量偏导数由式(\ref{eq:edge_time})直接给出：
\begin{equation}
\frac{\partial t(e)}{\partial u_{\parallel}} = -\frac{\ell_e}{v_{\text{g}}(e)^2}, \qquad \frac{\partial t(e)}{\partial u_{\perp}} = \frac{\ell_e u_{\perp}}{v_{\text{g}}(e)^2 \sqrt{V^2 - u_{\perp}^2}}.
\label{eq:edge_deriv}
\end{equation}
由此，每步只需在中网格上求左、右最快航线各一次（共2次求解），即可同时得到对全部 $K$ 个模态系数的梯度 $\boldsymbol{g}(\boldsymbol{z}) = \nabla_{\boldsymbol{z}} \Delta T(\boldsymbol{u}(\boldsymbol{z}))$。算法从粗图中心 $\boldsymbol{z}=\boldsymbol{0}$ 出发，先沿初始梯度正负方向一步跳至球面 $\boldsymbol{z}^{(1)} = \pm r\, \boldsymbol{g}(\boldsymbol{0}) / \|\boldsymbol{g}(\boldsymbol{0})\|_2$，再做步长减半的投影梯度上升；在半径1与2上各搜一次后线性插值到标定半径 $r$，每个任务平均仅需约71次中网格求解。

\subsection{利用多年再分析数据标定合理集合}
合理集合的物理结构与大小完全由开发年份的历史误差数据标定。第一步，统计粗图减真实海流的逐点误差标准差以确定式(\ref{eq:plausible_field})中的 $\mathbf{S}(\boldsymbol{x})$（黑潮主设置全区中位数为0.17米/秒），并由空间相关衰减曲线定出相关长度 $L_{\text{corr}} = 76$ 千米（当天0.5°图为0.07米/秒、18千米）。第二步，在开发年份任务上求使合理集合的左右航时差范围包住真实海流左右航时差 $\Delta T(\boldsymbol{u}_{\text{true}})$ 的任务比例不低于90\%的最小半径，在黑潮主设置下得 $r = 1.5$（开发年份实际覆盖93\%，测试年份覆盖94\%）。

\subsection{阈值判据与响应策略}
求得两侧最大后悔值 $R_{\text{L}}(r)$ 与 $R_{\text{R}}(r)$ 后，以阈值判据 $R_{s_0}(r) > \theta$（$\theta$ 在开发年份按平均额外航时最小选定，黑潮主设置为8小时）判定粗图是否可信：
\begin{enumerate}
    \item 若 $R_{s_0}(r) \le \theta$，判定粗图可信，直接按粗图选边 $s_0$。
    \item 若 $R_{s_0}(r) > \theta$，判定粗图不可信：当存在代价低于平衡点 $c^*$ 的大尺度观测手段时，执行“超阈值时上浮取图”（获取当天0.5°图后按新图选边）；当无法上浮或上浮过贵时，执行“超阈值时保守改选”，选最大后悔值较小的一侧：
    \begin{equation}
    s_{\text{cons}} = \arg\min_{s \in \{\text{L}, \text{R}\}} R_s(r).
    \label{eq:conservative_choice}
    \end{equation}
\end{enumerate}
此外，为避免在两侧都可能被强流堵死的海区盲目改选，第\ref{sec:scope}节进一步考察了“修正规则”：仅当 $|R_{\text{L}}(r) - R_{\text{R}}(r)| > \tau_{\text{num}}$ 时才在超阈值后改选。完整流程见算法\ref{alg:counterexample_gate}。

\begin{algorithm}[htbp]
\caption{基于合理反例检验的自主水下航行器航路决策算法}
\label{alg:counterexample_gate}
\begin{algorithmic}[1]
\Require 粗图 $\boldsymbol{u}_0$，标定的误差模态 $\{\boldsymbol{m}_k\}_{k=1}^{K}$，标定半径 $r$，数值误差容限 $\tau_{\text{num}}$，阈值 $\theta$，单次上浮代价 $c_{\text{surf}}$ 及平衡点 $c^*$。
\Ensure 选定绕行一侧 $s^*$ 或触发上浮取图。
\State 在粗图 $\boldsymbol{u}_0$ 上用粗网格求解得左右航时差 $\Delta T_{\text{coarse}}(\boldsymbol{u}_0)$。
\If{$|\Delta T_{\text{coarse}}(\boldsymbol{u}_0)| < \tau_{\text{num}}$}
    \State 用细网格求解重算得 $\Delta T_{\text{fine}}(\boldsymbol{u}_0)$，定粗图选边 $s_0 \gets \arg\min_{s \in \{\text{L},\text{R}\}} T_s^{\text{fine}}(\boldsymbol{u}_0)$。
\Else
    \State 直接定粗图选边 $s_0 \gets \arg\min_{s \in \{\text{L},\text{R}\}} T_s^{\text{coarse}}(\boldsymbol{u}_0)$。
\EndIf
\State 在中心 $\boldsymbol{z}=\boldsymbol{0}$ 处用中网格求解左右最快航线，按包络定理式(\ref{eq:envelope_grad})求初始梯度 $\boldsymbol{g}(\boldsymbol{0})$。
\State 沿 $\pm\boldsymbol{g}(\boldsymbol{0})$ 跳至 $r_1=1$ 与 $r_2=2$ 球面并做投影梯度上升，插值得标定半径 $r$ 下的最大后悔值 $R_{\text{L}}(r)$ 与 $R_{\text{R}}(r)$。
\If{$R_{s_0}(r) \le \theta$}
    \State \Return 按粗图选边：$s^* \gets s_0$。
\Else
    \If{允许上浮通信且 $c_{\text{surf}} < c^*$}
        \State \Return 超阈值时上浮取图：付出代价 $c_{\text{surf}}$ 获取当天0.5°图 $\boldsymbol{u}_{\text{new}}$，选 $s^* \gets \arg\min_{s \in \{\text{L},\text{R}\}} T_s(\boldsymbol{u}_{\text{new}})$。
    \Else
        \State \Return 超阈值时保守改选：选最大后悔值较小的一侧 $s^* \gets \arg\min_{s \in \{\text{L},\text{R}\}} R_s(r)$。
    \EndIf
\EndIf
\end{algorithmic}
\end{algorithm}

===== FILE: sections/experiments.tex =====
\section{实验}

\subsection{实验设置与对比方法}
我们在四种强流设置下验证本文方法：（1）黑潮主设置（23°--31°N、121°--129°E，开发年份710个任务，测试年份623个任务）；（2）湾流（33°--41°N、75°--67°W，开发724个、测试643个任务）；（3）阿古拉斯回流区（35°--43°S、14°--22°E，开发697个、测试618个任务，检验计划在下载数据前写定）；（4）黑潮区改带卫星测高地转流图（航行器带3天前的0.25°卫星测高地转流图，开发616个、测试648个任务，检验计划同样在下载数据前写定）。所有设置均以2019--2021年为开发年份标定误差模态、半径 $r$、数值误差容限 $\tau_{\text{num}}$ 与阈值 $\theta$，在2022--2024年测试年份上原样评价一次。

对比方法涵盖五组（图\ref{fig:main}）：（1）同一张粗图上改变网格：粗网格求解、中网格求解、基线：按粗图选边（细网格求解）；（2）改变选边准则：集合平均选边、直接选最大后悔值较小的一侧；（3）就地测流：原地停留测流、沿途测流30千米、沿途测流60千米、绕行定点测流；（4）总是上浮取当天1°图或上浮取当天0.5°图（每次计1小时）；（5）本文阈值判据响应：超阈值时保守改选、超阈值时上浮取图、超阈值时用集合平均选边。统计显著性由与“基线：按粗图选边”配对差值的按天整组重抽样（2000次）95\%置信区间判定，仅当区间不含0时称为显著。

\subsection{粗图误差具有可标定的空间结构}
3天前1°粗图的误差并非均匀白噪声，而是沿强流主轴形成长相关尺度的结构，可由多年再分析数据稳定标定（图\ref{fig:data}）。在黑潮开发年份中，粗图误差高值带紧密贴合黑潮主轴，全区误差中位数为0.17米/秒，空间相关长度达76千米；而在当天0.5°图上，误差中位数降至0.07米/秒，相关长度缩短至18千米。由于76千米的相关尺度与禁航区绕行跨度相当，单个中尺度误差模态即可使整条左侧或右侧通道同时顺流或逆流，这为用流函数模态构造合理集合提供了物理依据。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_data}
\caption{黑潮研究海区的流场特征与粗图误差标定。(a) 开发年份10米平均海流场与测试任务禁航区中心（橙色圆点）；(b) 3天前1°粗图的误差幅度分布（米/秒）；(c) 误差空间相关衰减曲线，3天前1°粗图相关长度为76千米，当天0.5°图为18千米。}
\label{fig:data}
\end{figure}

\subsection{发现一：多算消除不了环境歧义}
在四种实验设置下，将同一张粗图上的求解计算量增加64倍（从粗网格求解到细网格求解），均无法消除选边错误。在黑潮主设置测试年份中（图\ref{fig:ambiguity}(a)），加密网格仅改变了64个任务的选择（38个改对、26个改错），选错一侧的比例仅从21.7\%变为19.7\%，平均额外航时从1.16小时变为0.98小时，差异不显著；相反，若换成当天0.5°图，选错率即降至10.4\%。在湾流、阿古拉斯回流区和黑潮区改带卫星测高地转流图下，计算量增加64倍后的选错率分别仅从18.5\%变为19.4\%、保持27.7\%不变、以及从19.9\%变为19.6\%。多算无效的根源在于环境歧义普遍存在：在覆盖94\%真实左右航时差的标定半径 $r=1.5$ 下，黑潮测试年份99.7\%的任务都存在合理反例（图\ref{fig:ambiguity}(b)），湾流与阿古拉斯回流区也分别达98.8\%和99.2\%。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_ambiguity}
\caption{求解计算量与环境信息对选边错误的不同作用（黑潮测试年份）。(a) 选错一侧的任务比例：粗图上计算量增加64倍仅从21.7\%变为19.7\%，而换成当天0.5°图则降至10.4\%（理想上限为0\%）；(b) 合理集合覆盖真实左右航时差的比例与存在合理反例的比例随半径 $r$ 的变化。}
\label{fig:ambiguity}
\end{figure}

\subsection{发现二：最大后悔值找得出额外航时所在，而且算得快}
\label{sec:budget}
按最大后悔值对任务排序，能够将绝大部分额外航时集中在排名前列的少数任务中，且在全部四种设置下均优于按改变选边的成员比例或按粗图左右航时差排序。黑潮测试年份中，额外航时最大的10\%任务占了全部额外航时的92\%；按最大后悔值排名前20\%的任务集中了67\%的额外航时，高于32个集合成员中改变选边的成员比例（49\%）和粗图左右航时差（34\%，图\ref{fig:risk}(a)）。在湾流、阿古拉斯回流区和黑潮区改带卫星测高地转流图下，最大后悔值排名前20\%的任务分别集中了71\%、53\%和67\%的额外航时，同样一致高于改变选边的成员比例（分别为49\%、36\%和52\%）。这是因为改变选边的成员比例将多花半小时与多花十几个小时的改选同等看待，而最大后悔值（以及在集合成员上计算的后悔值的集合平均）直接度量了选错后的航时劣势大小（图\ref{fig:budget}(b)）。

在决定选哪一侧时，合理反例检验仅用约71次航线求解，就达到了集合平均选边使用1024个集合成员（2048次求解，约为其29倍）才能达到的效果（图\ref{fig:budget}(a)）。数学上，选最大后悔值较小的一侧等价于按合理集合给出的左右航时差范围的中点选边，只有当一侧的最不利情形比另一侧严重得多时才会改选。相比之下，集合平均选边在仅有32个集合成员时（平均额外航时0.99小时）显著劣于反例搜索后的保守选边（0.72小时），原因是32个成员均值的抽样误差（中位数2.4小时）大于它要估计的真实修正量（中位数1.7小时），导致改选多由抽样噪声驱动；直到集合成员增至1024个（2048次求解，平均额外航时0.71小时），两者才无显著差异。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_risk}
\caption{黑潮测试年份的风险排序与上浮代价权衡。(a) 按不同指标排序时前序任务累计占总额外航时的比例：排名前20\%时，最大后悔值占67\%，高于改变选边的成员比例（49\%）与粗图左右航时差（34\%）；(b) 平均额外航时随单次上浮取当天0.5°图时间代价的变化。}
\label{fig:risk}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_budget}
\caption{集合成员数量与合理反例检验在选边和风险排序上的对比（黑潮测试年份）。(a) 平均额外航时随求解次数的变化：曲线为集合平均选边，单点为反例检验后选最大后悔值较小的一侧（约71次求解）；(b) 排名前20\%任务所占额外航时比例随求解次数的变化：对比后悔值的集合平均、改变选边的成员比例与最大后悔值。}
\label{fig:budget}
\end{figure}

\subsection{发现三：判定不可信时，取新信息最划算}
当阈值判据标记粗图不可信时，获取新信息是跨海区最稳健的响应策略（图\ref{fig:main}、表\ref{tab:scope}）。在湾流和阿古拉斯回流区中，粗图误差大且常有一侧因强逆流难以通行，“基线：按粗图选边”的平均额外航时分别达3.56小时和6.87小时；即使计入每次1小时的上浮耗时，超阈值时上浮取图（当天0.5°图）仍将两海区的平均额外航时分别显著降至1.31小时和2.20小时，同时优于不论风险高低总是上浮取当天0.5°图（1.53小时和1.98小时在湾流略差或相近，但省去了约三分之一无谓上浮）。在黑潮主设置中，阈值判据（$\theta=8$小时）标记了47\%的任务，囊括了82\%的额外航时；当单次上浮代价低于约1小时时，超阈值时上浮取图带来的净收益最优（例如上浮代价0.5小时时平均额外航时仅0.55小时，图\ref{fig:risk}(b)）。

相比之下，局部就地测流受限于观测范围与时间代价，在多数情况下不划算（图\ref{fig:main}）。在黑潮主设置中，原地停留测流耗费2小时却只测起点一处（平均额外航时升至2.91小时）；绕行定点测流平均需先花15.4小时赶往测点（额外航时12.43小时）；沿途测流30千米或60千米与按粗图选边的差异均不显著，因为前30千米测流很少足以改变判断（仅3.4\%换边），而走完60千米再折返已得不偿失。唯有在额外航时基数很大的阿古拉斯回流区，沿途测流30千米才显著降低了额外航时（从6.87降至4.48小时），但仍远不如超阈值时上浮取图（2.20小时）。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_main}
\caption{黑潮测试年份623个任务上五组策略的平均额外航时（竖直虚线为基线：按粗图选边的0.98小时）。五组从上至下依次为：同一张粗图改变求解网格、改变选边准则、就地测流、总是上浮取图、本文阈值判据响应。}
\label{fig:main}
\end{figure}

\subsection{适用范围}
\label{sec:scope}
表\ref{tab:scope}汇总了不同地图质量、航速、合理集合构造方式以及全部四种设置下的结果。当航行器直接携带当天0.5°图时，按粗图选边的平均额外航时仅0.17小时，超阈值时保守改选与上浮取图均自动退化为照图航行（0.17与0.16小时），不产生负向干扰。当航行器对水速度降至0.75米/秒时，选错代价放大，按粗图选边的额外航时升至2.43小时，超阈值时上浮取图将其降至1.32小时。在消融实验中，若不用标定的无散流函数模态、而改用历史相似日的小尺度差构造合理集合，超阈值时保守改选的额外航时为0.95小时，与按粗图选边（0.99小时）无显著差异，说明准确标定误差空间结构是合理反例检验生效的前提。

在不允许观测、只能靠超阈值时保守改选的场景下，其收益显著与否取决于海区是否存在两侧同时可能被强流堵死的情形。在黑潮主设置中，超阈值时保守改选将平均额外航时从0.98小时显著降至0.70小时（配对差$-0.28$小时，95\%置信区间$[-0.51, -0.07]$，降低28\%）：在改选的41个任务中，23个改对（平均省10.1小时）、18个改错（平均多花3.3小时），避开高风险一侧的收益远大于改错代价。然而在湾流和阿古拉斯回流区，真实海流中有一侧过不去的任务分别占8.7\%和16.2\%（黑潮仅1.0\%）；此时合理集合内既有堵死左侧、也有堵死右侧的流场，两侧最大后悔值同时接近上限，选较小一侧近于随机，导致超阈值时保守改选在两海区均无显著收益（4.00小时与6.49小时）。在下载阿古拉斯数据前写定的计划中，我们预先检验了“修正规则”（仅当两侧最大后悔值之差超过数值误差容限时才改选）：它在湾流（事后检验，3.45小时）和阿古拉斯回流区（预先设定检验，6.72小时）均消除了盲目改选的负作用，但与按粗图选边的差异仍不显著。

在黑潮区改带卫星测高地转流图的预先设定检验中，增加计算无效（选错率19.9\%变为19.6\%）与最大后悔值排序（前20\%任务占67\%额外航时）依然成立，但各类响应策略的收益均不显著。在该设置下，存在合理反例的任务占81.0\%；按粗图选边的平均额外航时为0.79小时，超阈值时保守改选（0.71小时）、修正规则（0.70小时）与超阈值时上浮取当天0.5°图（0.64小时）与基线的置信区间均包含0。原因在于卫星测高地转流图只含地转分量，即使换成当天的卫星测高地转流图，选错率仍达18.5\%（当天0.5°模式图为8.6\%），说明误差主要来自两种流场产品之间的系统差异而非3天时效。

\begin{table}[htbp]
\centering
\caption{不同实验设置与消融条件下的测试年份结果汇总（额外航时单位：小时；超阈值时上浮取图指取当天0.5°图）。}
\label{tab:scope}
\small
\input{tables/route_scope.tex}
\end{table}

\subsection{局限}
本研究的局限包括：（1）单次任务将海流视为定常二维场，未耦合航行过程中的流场时变；（2）真实海流采用当天1/12°再分析场，仍平滑了亚中尺度过程与内波；（3）仅考虑单个圆形禁航区的左右二元选边，未扩展至多障碍物的多同伦类路径；（4）假设选定一侧后航行器在该侧按理想轨迹航行，以隔离底层控制误差；（5）不观测时的超阈值保守改选仅在黑潮主设置下显著有效，在其他海区与卫星测高地转流图下必须依赖阈值判据触发大尺度观测。

===== FILE: sections/innovation.tex =====
\section{原创创新点拆解}

本研究源于《海洋大数据技术原理与应用》课程核心议题，经历了从探索、证伪到问题聚焦的完整过程。作者最初提问：航行器携带几天前的旧卫星图下水时，应继续机载计算还是停下观测？第3节的前期赤潮巡测研究表明，增加推演只会抬高规划器对自身航线的估值，真实价值很快停止提升，且时间分配策略的改进空间仅约0.022。针对前期研究增益小的不足，作者将问题聚焦到选错一侧即多花数小时的强海流绕障二元决策：当粗图同时容许左侧更快与右侧更快的真实海流时，多算无法分辨真伪；能否在历史大数据标定的合理集合内，主动搜出使另一侧更快的合理反例及最大后悔值，以此决定何时计算、何时观测？这一思路形成了本文的四个创新点（表\ref{tab:innovation}）。

\begin{table}[htbp]
\centering
\caption{本文核心原创创新点、已有做法对比、实验证据与局限拆解。}
\label{tab:innovation}
\footnotesize
\begin{tabular}{@{}p{0.13\linewidth}p{0.20\linewidth}p{0.22\linewidth}p{0.19\linewidth}p{0.14\linewidth}@{}}
\toprule
创新点 & 已有做法及其不足 & 本文做法 & 证据（图表） & 局限 \\
\midrule
1. 分离数值歧义与环境歧义的判据 & 确定性规划在粗图上加密网格，混淆求解误差与环境信息缺失。 & 区分粗细网格容限内的数值歧义与合理集合内存在反例的环境歧义。 & 图\ref{fig:overview}、\ref{fig:ambiguity}(a)：64倍计算选错率仅21.7\%变19.7\%，当天0.5°图降至10.4\%。 & 仅在单禁航区二元选边验证，未扩展至多分支路径。 \\
\addlinespace
2. 包络定理梯度搜索最大后悔值 & 集合平均选边需上千成员压低噪声；改变选边的成员比例不计航时差大小。 & 用包络定理沿最快航线求导，一次梯度仅2次求解，在球面搜索最大后悔值。 & 图\ref{fig:risk}(a)、\ref{fig:budget}：约71次求解达到1024个成员效果；前20\%任务占53\%--71\%额外航时。 & 大扰动下最短路拓扑跳变时，一阶梯度近似有折耗。 \\
\addlinespace
3. 多年再分析数据标定合理集合 & 凭经验设不确定集形状与半径，脱离海洋误差空间结构。 & 用三年误差标定逐点标准差与76千米无散流函数模态，按90\%覆盖率标定半径。 & 图\ref{fig:data}、\ref{fig:ambiguity}(b)、表\ref{tab:scope}：测试覆盖94\%；改用历史相似日差值后失去增益。 & 依赖历史平稳统计，对台风等极端天气适应受限。 \\
\addlinespace
4. 基于最大后悔值的阈值判据响应 & 自适应采样面向全场降方差，或不论风险高低一律上浮/保守。 & 最大后悔值超阈值时判定粗图不可信，按观测代价选择上浮取图或保守改选。 & 图\ref{fig:main}、\ref{fig:risk}(b)、表\ref{tab:scope}：湾流与阿古拉斯上浮将额外航时降至1.31与2.20小时。 & 不观测的保守改选仅在黑潮主设置显著有效。 \\
\bottomrule
\end{tabular}
\end{table}

在人机协同方面（详见附录B），作者提出了初始问题，要求补充真实卫星数据、对照与消融实验，并在前期研究后提出“粗图下两条航路的合理反例”这一核心问题；Claude（Anthropic）完成了文献检索、代码实验、作图与数据核对；Gemini（Google）根据事实清单与提纲撰写了论文初稿。

===== FILE: sections/conclusion.tex =====
\section{结论}

本文针对自主水下航行器在3天前1°粗图下绕越禁航区的左右选边问题，提出了基于多年再分析数据标定的合理反例检验方法。核心结论是：加密网格计算只能消除求解粗糙带来的数值歧义；当合理集合内存在使另一侧更快且造成较大最大后悔值的合理反例时，任务处于计算无法消解的环境歧义，此时应依靠阈值判据触发大尺度观测。在黑潮主设置、湾流、阿古拉斯回流区及黑潮区改带卫星测高地转流图四种设置下的实验一致证实：（1）将求解计算量增加64倍几乎不改变选错率（黑潮仅从21.7\%变为19.7\%）；（2）最大后悔值排名前20\%的任务集中了53\%--71\%的额外航时，且仅用约71次航线求解即达到集合平均选边使用1024个集合成员（2048次求解）的选边效果；（3）超阈值时上浮取图将湾流和阿古拉斯回流区的平均额外航时分别从3.56降至1.31小时、从6.87降至2.20小时，在黑潮主设置中上浮代价低于约1小时时同样划算；而不观测的超阈值保守改选仅在黑潮主设置下显著降低额外航时（0.98降至0.70小时），在卫星测高地转流图下各类响应均不显著。未来工作将把该方法推广至时变三维流场并开展实艇海试。

===== FILE: sections/appendix.tex =====
\section*{附录}

\subsection*{附录 A：代码与数据开源说明}
本研究的全部源代码、数据处理脚本、实验配置、统计汇总程序以及论文图表生成脚本均已开源于代码仓库：\url{https://github.com/frankxucd0826-source/auv-compute-or-observe}。

\begin{enumerate}
    \item \textbf{数据集来源：}主实验海流数据取自HYCOM全球海洋再分析公开服务（产品GLBy0.08，实验93.0，10米水深水平流速，黑潮主设置区域23°--31°N、121°--129°E，2019--2024年；重复实验区为湾流33°--41°N、75°--67°W与阿古拉斯回流区35°--43°S、14°--22°E，产品与时间范围相同；黑潮区改带卫星测高地转流图检验所用的近实时融合测高地转流取自美国国家海洋和大气管理局海岸观测网数据服务）；第3节前期研究的叶绿素与海表温度数据取自美国国家海洋和大气管理局海岸观测网数据服务的公开卫星产品。
    \item \textbf{主要程序结构：}核心软件包 \texttt{src/oceanroute/} 包含网格最短路与包络定理梯度求解器（\texttt{solver.py}）、海流快照与粗图（\texttt{fields.py}，海区由环境变量 \texttt{OCEANROUTE\_REGION} 选择）、粗图误差的多年数据标定与无散误差模态（\texttt{errormodel.py}）以及任务生成、合理反例检验与测量更新（\texttt{mission.py}）；数据下载、批量评估、统计汇总、集合成员对照与各海区实验分别由 \texttt{scripts/download\_hycom.py} 与 \texttt{experiments/route\_*.py} 完成，正文插图由 \texttt{paper/figures/fig\_route\_*.py} 生成；逐条复现命令与前期研究的脚本见仓库根目录的 \texttt{README}。
\end{enumerate}

\subsection*{附录 B：人工智能工具使用说明}
本研究与论文撰写中人工智能工具的使用情况如下：
\begin{enumerate}
    \item \textbf{作者：}提出了机载计算与现场观测如何权衡的初始问题；对第一版结果提出用真实卫星数据检验、补充对照与消融、按学术论文格式写作等要求；在前期研究结果出来后指出其提升小、新意不足，并提出“粗分辨率海流图下两条航路的合理反例”这一新问题，决定转向本文研究；对全文负责。
    \item \textbf{Claude（Anthropic）：}在作者授权下完成文献检索与核对、数据下载与全部代码、实验与统计、论文插图，整理写作提纲与由实验程序生成的事实清单，并逐项核对正文中的数字与引用。
    \item \textbf{Gemini（Google）：}根据Claude整理的提纲、术语表与事实清单撰写论文文字，再由Claude核对与修改。
    \item \textbf{可追溯性记录：}作者与人工智能工具的对话记录、与Gemini的每轮写作往来以及研究笔记均保存在上述代码仓库中（涉及作者其他未发表工作的内容已隐去）。
\end{enumerate}

===== FILE: tables/route_settings.tex =====
\begin{tabular}{@{}p{0.16\linewidth}p{0.80\linewidth}@{}}
\toprule
项目 & 设置 \\
\midrule
海流数据 & HYCOM 全球海洋再分析（GLBy0.08，实验 93.0），水平分辨率 1/12°，取 10 米深度；23°--31°N、121°--129°E（台湾以东至东海，含黑潮）；2019-01-01 至 2024-08-29 每 3 天 12:00 时一张，共 689 张 \\
任务 & 每张快照抽 2 个：起终点相距 100--140 千米、离岸不少于 20 千米，两点中间设半径 15 千米的禁航区，可从左侧或右侧绕过；只取粗图上任务区平均流速不低于 0.3 米/秒的强流任务；开发 710 个（2019--2021 年），测试 623 个（2022--2024 年） \\
粗图与真实海流 & 航行器带 3 天前的 1° 粗分辨率海流图（下称粗图，格内平均）；真实海流为当天 1/12° 再分析海流场 \\
航行器 & 对水速度 1.0 米/秒；选定一侧后，按真实海流在该侧以最快方式航行 \\
航线求解 & 网格最短路：粗网格求解 8 千米网格、8 个方向；中网格求解 4 千米、16 个方向；细网格求解 2 千米、32 个方向（计算量之比 1 : 8 : 64）；顶流过强的边不可通行 \\
合理流场集合 & 粗图加上由流函数生成的无散误差模态的组合，各点误差大小与相关长度（76 千米）由开发年份标定，组合系数服从标准正态；半径 $r=1.5$（开发年份中包住真实左右航时差的任务占 93\%） \\
合理反例检验 & 在半径 $r$ 的球内对左右航时差做投影梯度上升（梯度沿最快航线累加）；两个方向、半径 1 与 2 各搜一次，其他半径线性插值，每个任务约 71 次中网格求解 \\
观测方式 & 原地停留测流（出发前 2 小时测 12 次）；沿途测流 30 千米或沿途测流 60 千米后可换边；绕行定点测流（去前方 40 千米内反例与粗图差别最大处测量）；上浮取当天 1° 图或上浮取当天 0.5° 图（每次 1 小时）；测流噪声 0.05 米/秒 \\
阈值判据 & 最大后悔值超过 8 小时（开发年份选定）时判定粗图不可信，触发超阈值时保守改选或超阈值时上浮取图，否则按粗图选边 \\
评价指标 & 额外航时 = 实际航时 $-$ 真实更快一侧的航时（小时）；配对差值的 95\% 置信区间按天整组自助重抽样 2000 次 \\
\bottomrule
\end{tabular}
```

</details>
