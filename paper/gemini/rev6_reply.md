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
