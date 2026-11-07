===== S1 =====
第五，在阿古拉斯回流区（35°--43°S、14°--22°E）的第三海区独立检验表明，门控触发观测、算力局限与风险排序均跨海区成立，而改进规则无害但无显著收益。该检验计划在下载数据前写定且未做改动，半径与阈值由该区开发年份标定，测试年份只评价一次，专门检验湾流实验后提出的改进规则（仅当两侧最坏后悔之差超过数值误差容限时才改选，不引入新参数）。五项预设判定结果为：一是改进规则与精算地图之差为$-0.16$小时（置信区间包含0），无害但无显著收益；二是原门控后取保守规则与精算地图之差同样不显著（16.2\%的任务有一侧不可通行）；三是门控后上浮取当天0.5°图将平均损失从6.87小时显著降至2.20小时；四是加算64倍的选错率保持27.7\%不变（改变32个选择，16个改对、16个改错）；五是最坏后悔前20\%的任务占地图损失的53%，高于翻转比例的36\%。此外，沿途测30千米在此区能将平均损失显著降至4.48小时。纵观三个海区，一致成立的是：计算消除不了环境歧义，合理反例几乎无处不在，最坏后悔能找出损失所在，一旦门控报警去观测就有回报；不观测的保守选择仅在黑潮显著有效，改进规则使其在其他海区无害但无显著收益。因此，门控的核心价值在于决定何时去观测，而不观测的保守改选属于依赖海区特性的备选方案。

===== S2 =====
{\heiti 摘要：}
随着海洋大数据的计算引擎延伸至移动观测平台边缘，自主水下航行器在受限算力与能量下必须在继续计算、补充观测与立即行动之间做出在线权衡。在强流区携带3天前的粗分辨率海流图绕越禁航区时，选错绕行一侧将导致数小时航时损失。现有确定性规划通过加密网格增加计算，只能提升求解精度而无法补充缺失的海洋信息；集合规划与自适应采样或需大量样本才能估准不利流场，或将观测耗费在与二元选边无关的全场重构上。为此，本文提出基于海洋大数据标定的合理反例检验方法，分离数值歧义与环境歧义以决定何时计算、何时观测、何时保守绕行。该方法先通过粗精网格容限按需精算以消除数值歧义，再用多年再分析海流标定旧粗图的无散误差模态与合理集合半径，利用包络定理投影梯度上升搜索使所选一侧变差、另一侧变好的合理反例及最坏后悔，据此门控触发上浮取图或选最坏后悔更小的一侧。台湾以东至东海黑潮区六年再分析数据实验表明：计算量增加64倍仅将选错率从21.7\%降至19.7\%，而在覆盖94\%真实时间差的合理集合内99.7\%的任务存在合理反例；最坏后悔前20\%的任务集中了67\%的损失；反例搜索仅用约71次航线求解，即达到按期望时间选边使用约1024个随机合理场（2048次求解）时的效果；门控后取保守将平均损失从0.98小时降至0.70小时。在湾流区与阿古拉斯回流区的重复实验中，单纯增加计算同样无效，最坏后悔风险排序与门控后上浮取图均成立（平均损失分别从3.56小时降至1.31小时、从6.87小时降至2.20小时），而不观测的保守选择在这两个海区均无显著收益。

{\heiti 关键词：}海洋大数据；自主水下航行器；航路规划；合理反例检验；元推理；不确定性量化

\vspace{1em}
\begin{center}
{\large\bfseries Plausible Counterexample Test: When an Autonomous Underwater Vehicle Should Compute and When It Should Observe Under a Coarse Current Map}
\end{center}
\vspace{0.5em}

{\bfseries Abstract:}
As ocean big-data computing moves onto mobile platforms, an autonomous underwater vehicle with limited onboard computation and energy must trade off computing, observing and moving. Rounding a no-go zone in strong currents with a three-day-old coarse current map, a vehicle that picks the wrong side loses hours. Refining the solver grid sharpens numerical precision but supplies no missing oceanographic information; ensemble planning needs many samples to estimate adverse flows, and adaptive sampling spends observations on the whole field rather than on the binary route choice. We propose a plausible counterexample test calibrated by ocean big data that separates numerical ambiguity from environmental ambiguity to decide when to compute, observe, or hedge conservatively. The method resolves numerical ambiguity with an on-demand fine solve, calibrates divergence-free error modes and a plausible-set radius from multi-year reanalysis currents, finds the worst counterexample and its worst regret by envelope-theorem projected gradient ascent, and gates between surfacing for a new map and taking the side with smaller worst regret. Across six years of Kuroshio reanalysis data, 64-fold more computation cuts wrong-side choices only from 21.7\% to 19.7\%, whereas 99.7\% of missions admit a plausible counterexample inside the calibrated set covering 94\% of real time differences; the top 20\% of missions by worst regret hold 67\% of total loss; the search reaches with about 71 route solves what the expected-time rule needs about 1024 random plausible fields (2048 solves) to reach; and gated conservative routing lowers mean loss from 0.98 to 0.70 hours. In replications in the Gulf Stream and the Agulhas retroflection, extra computation remains ineffective, risk ranking and gated surfacing hold (lowering mean loss from 3.56 to 1.31 hours and from 6.87 to 2.20 hours), whereas observation-free conservative choice brings no significant gain in either region.

{\bfseries Keywords:} ocean big data; autonomous underwater vehicle; path planning; plausible counterexample test; metareasoning; uncertainty quantification

===== S3 =====
    \item \textbf{黑潮、湾流与阿古拉斯回流区三个强流区的系统实证：}在六年黑潮再分析海流共1333个任务上的实验表明，64倍算力仅使选错率从21.7\%降至19.7\%，而99.7\%的任务存在合理反例；最坏后悔前20\%的任务集中了67\%的损失，门控后取保守将平均航时损失降低28\%。在湾流区与下载数据前即写定检验计划的阿古拉斯回流区独立重复实验中，门控识别高危任务与门控后上浮取图（平均损失分别从3.56小时降至1.31小时、从6.87小时降至2.20小时）均同样成立，而不观测的保守选择及预先写定的改进规则在这两个海区均无显著收益，从而明确了门控的核心价值在于决定何时去观测。

===== S4 =====
图\ref{fig:main}、图\ref{fig:risk}(b)、表\ref{tab:scope}：黑潮区门控后取保守将平均损失从0.98降至0.70小时，上浮代价切换点约1小时；湾流区与阿古拉斯回流区门控后上浮取图分别将损失从3.56降至1.31小时、从6.87降至2.20小时。 & 不观测的保守选择在湾流与阿古拉斯回流区这类两侧都可能被强流堵死的海区均无显著收益，此时须靠门控触发观测；黑潮区门控保守相对一律保守（0.72小时）的边际增益也较小。 \\

===== S5 =====
本研究存在五方面局限：第一，单次任务求解将海流快照视为定常二维场，尚未耦合约40小时航行中的流场时变；第二，以当天1/12°再分析场作为“真实海洋”，旧粗图也由同一再分析场平均与滞后得到，而非来自独立的观测系统，且再分析场仍平滑了亚中尺度过程与内波扰动；第三，将绕障简化为单个圆形禁航区的左右二元决策，未扩展至多岛礁群的多分支同伦类；第四，假设选定一侧后航行器能按真实海流以最优轨迹航行，以剥离底层轨迹跟踪误差、专门评估顶层选边决策；第五，纵观黑潮、湾流与阿古拉斯回流区三个强流区，不观测的门控后取保守仅在黑潮显著降低损失，在湾流与阿古拉斯回流区这类强流可能堵死任一侧的海区，原规则与改进规则均无显著收益，此时必须依靠门控触发观测来消解环境歧义。

===== S6 =====
\section{结论}

本文针对自主水下航行器在粗分辨率海流图下执行强流绕障时的在线元决策问题，提出了基于海洋大数据标定的合理反例检验方法，阐明了一条基本原理：机载计算的职责是消除求解器近似带来的数值歧义，从而读出已有海流图的本来倾向；而当多年海洋大数据界定的合理集合内存在翻转航路优劣并造成严重航时损失的合理反例时，环境处于算力无法消解的环境歧义状态，航行器应通过门控引入大尺度观测，或在两侧最坏情形差别分明时改选最坏后悔更小的保守航路。在黑潮区域六年再分析海流的系统实验表明，将航线求解算力提高64倍仅使选错率从21.7\%降至19.7\%；反例搜索以约71次求解达到按期望时间选边使用约1024个随机合理场（2048次求解）时的效果，其最坏后悔将67\%的地图总损失集中在排名前20\%的任务中，门控后取保守将平均航时损失从0.98小时降至0.70小时。在湾流区与阿古拉斯回流区的重复实验表明，算力局限、最坏后悔风险排序以及门控后上浮取图（平均损失分别从3.56小时降至1.31小时、从6.87小时降至2.20小时）跨海区成立，而不观测的保守选择在这两个海区均无显著收益，明确了门控的核心价值在于决定何时去观测。未来工作将把该方法扩展至随时间演变的流场，并结合实艇开展海上试验。
