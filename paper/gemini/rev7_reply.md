===== V1 =====
{\heiti 摘要：}
随着海洋大数据的计算引擎延伸至移动观测平台边缘，自主水下航行器在受限算力与能量下必须在继续计算、补充观测与立即行动之间做出在线权衡。在强流区携带3天前的粗分辨率海流图绕越禁航区时，选错绕行一侧将导致数小时航时损失。现有确定性规划加密网格只能提升求解精度而无法补充缺失的海洋信息；集合规划与自适应采样或需大量样本才能估准不利流场，或将观测耗费在与二元选边无关的全场重构上。为此，本文提出基于海洋大数据标定的合理反例检验方法，先按需精算以消除数值歧义，再用多年再分析海流标定无散误差模态与合理集合半径，利用包络定理投影梯度上升搜索合理反例及最坏后悔，据此门控触发上浮取图或选最坏后悔更小的一侧。在黑潮主设置、湾流、阿古拉斯回流区及黑潮携带真实卫星测高地转流图四种设置下一致成立的是：算力增加64倍几乎不改变选错率（依次为21.7\%至19.7\%、18.5\%至19.4\%、27.7\%至27.7\%、19.9\%至19.6\%）；最坏后悔排前20\%的任务所占地图损失均高于翻转比例排序（67\%对49\%、71\%对49\%、53\%对36\%、67\%对52\%）；黑潮区反例搜索仅用约71次航线求解即达到按期望时间选边用约2048次求解（1024个随机合理场）的效果；同源粗图下98.8\%--99.7\%的任务存在合理反例，真实卫星图下为81.0\%。响应收益则取决于设置：门控后上浮取当天0.5°图在粗图误差大的海区显著降损（湾流3.56至1.31小时、阿古拉斯6.87至2.20小时），在黑潮主设置下仅当单次上浮代价低于约1小时时划算，在卫星图下不显著；不观测而选最坏后悔更小一侧仅在黑潮主设置显著（0.98至0.70小时），其余三种设置均不显著。这表明合理反例检验能可靠判明海流图何时不可信及损失所在，单纯加算并非出路，而后续行动则取决于可用观测。

{\heiti 关键词：}海洋大数据；自主水下航行器；航路规划；合理反例检验；元推理；不确定性量化

\vspace{1em}
\begin{center}
{\large\bfseries Plausible Counterexample Test: When an Autonomous Underwater Vehicle Should Compute and When It Should Observe Under a Coarse Current Map}
\end{center}
\vspace{0.5em}

{\bfseries Abstract:}
As ocean big-data computing moves onto mobile platforms, an autonomous underwater vehicle with limited computation and energy must trade off computing, observing and moving. Rounding a no-go zone in strong currents with a three-day-old coarse current map, picking the wrong side loses hours. Finer solver grids add no oceanographic information; ensemble planning needs many samples, and adaptive sampling spends observations on the whole field rather than the binary route choice. We propose a plausible counterexample test calibrated by ocean big data: it resolves numerical ambiguity with an on-demand fine solve, calibrates divergence-free error modes and a plausible-set radius from multi-year reanalysis currents, finds the worst counterexample and its worst regret by envelope-theorem gradient ascent, and gates between surfacing for a new map and taking the side with smaller worst regret. Across four settings---the Kuroshio main setting, the Gulf Stream, the Agulhas retroflection, and the Kuroshio with a real satellite altimetry map---three findings hold everywhere: 64-fold more computation barely changes wrong-side choices (21.7\% to 19.7\%, 18.5\% to 19.4\%, 27.7\% to 27.7\%, 19.9\% to 19.6\%); the top 20\% of missions by worst regret hold more of the map's loss than when ranked by flip share (67\% vs.\ 49\%, 71\% vs.\ 49\%, 53\% vs.\ 36\%, 67\% vs.\ 52\%); in the Kuroshio, the search reaches with about 71 route solves the side choice that the expected-time rule over random plausible fields needs about 2048 solves (1024 fields) to reach; and plausible counterexamples exist for 98.8\%--99.7\% of missions with model-derived maps and 81.0\% with the satellite map. Response gains depend on the setting: gated surfacing for today's 0.5° map works strongly where the coarse map is poor (Gulf Stream 3.56 to 1.31 hours; Agulhas 6.87 to 2.20 hours), pays in the Kuroshio main setting only when surfacing costs under about 1 hour, and is not significant with the satellite map; choosing the smaller worst regret without observing is significant only in the Kuroshio main setting (0.98 to 0.70 hours). Thus the plausible counterexample test reliably tells when the map cannot be trusted and where losses lie; computing more is not the answer, and what to do next depends on the observation available.

{\bfseries Keywords:} ocean big data; autonomous underwater vehicle; path planning; plausible counterexample test; metareasoning; uncertainty quantification

===== V2 =====
为此，本文提出“合理反例检验”：机载计算与现场观测消除的是两类不同性质的不确定性；当两侧难分伯仲是因为求解网格粗糙（数值歧义）时，多算即可做对决定；而当存在与粗图同样相容、却使另一侧明显更快的合理海流（环境歧义）时，继续计算无法分辨真伪，唯有引入新观测才能消解，而在缺乏划算观测时改选最坏后悔更小的一侧则是收益随具体设置而异的后备手段。我们将这一判别转化为操作问题：针对粗图推荐的一侧，能否在多年海洋大数据标定的合理集合内搜出使另一侧更快、且让当前选择付出沉重代价的合理反例？在图\ref{fig:overview}所示的2022年1月18日测试任务示例中，粗图上两侧只差约0.3小时且地图推荐左侧，继续加密网格只会把这一账面差值算得更细，而合理反例检验在合理集合内搜出了使左侧明显变慢、右侧更快的物理相容流场，预示了真实海洋中右侧快11.7小时的结果，并据此触发门控决策。

===== V3 =====
\begin{itemize}
    \item \textbf{概念与判别准则创新：}据我们所知，本文首次在自主水下航行器航路决策中分离了可由计算消除的“数值歧义”与需靠新信息或保守决策应对的“环境歧义”，提出以最坏合理后悔为核心判据的合理反例检验框架，明确了边缘计算与海洋观测的功能边界。
    \item \textbf{大数据标定与高效反例搜索：}利用多年再分析海流标定旧粗图的无散流函数误差模态及覆盖90\%以上真实时间差的合理集合半径，结合包络定理梯度与球面投影搜索，以约71次标准网格求解直接定位最坏后悔流场，其选边效果与按期望时间准则使用约1024个随机合理场（2048次求解，约为其29倍）相当。
    \item \textbf{四种设置下的系统实证：}在黑潮主设置、湾流、阿古拉斯回流区及黑潮携带真实卫星测高地转流图四种设置下一致证实，将求解算力增加64倍几乎不改变选错率，最坏后悔排前20\%的任务所占地图总损失在四处均明显高于按集合翻转比例排序（如黑潮主设置为67\%对49\%），且合理反例在同源粗图下几乎处处存在、在真实卫星图下见于81.0\%的任务。门控后的最优响应则取决于设置：门控后上浮取当天0.5°图在粗图误差较大的湾流与阿古拉斯回流区显著降低平均航时损失（分别从3.56小时降至1.31小时、从6.87小时降至2.20小时），在黑潮主设置下仅当单次上浮代价低于约1小时时划算，在卫星图下不显著；不观测而直接改选最坏后悔更小一侧仅在黑潮主设置下显著降低损失（从0.98小时降至0.70小时），其余三种设置下均不显著。
\end{itemize}

===== V4 =====
\section{结论}

本文针对自主水下航行器在粗分辨率海流图下绕障选边的在线元决策问题，提出了基于海洋大数据标定的合理反例检验方法：机载计算只能消除求解器粗糙导致的数值歧义，而当合理集合内存在翻转优劣并造成严重损失的合理反例时，单纯加算并非出路，合理反例检验能可靠判明海流图何时不可信及损失所在，后续如何行动则取决于可用观测。在黑潮主设置、湾流、阿古拉斯回流区与黑潮携带真实卫星测高地转流图四种设置中一致成立的是：算力增加64倍几乎不改变选错率（21.7\%至19.7\%、18.5\%至19.4\%、27.7\%至27.7\%、19.9\%至19.6\%）；最坏后悔排前20\%的任务所占地图损失均高于集合翻转比例排序（67\%对49\%、71\%对49\%、53\%对36\%、67\%对52\%）；黑潮区反例搜索以约71次求解达到按期望时间选边用约2048次求解（1024个随机合理场）的效果；同源粗图下98.8\%--99.7\%的任务存在合理反例，真实卫星图下为81.0\%。响应收益取决于设置：门控后上浮取当天0.5°图在湾流（3.56至1.31小时）与阿古拉斯（6.87至2.20小时）显著降损，在黑潮主设置下当单次上浮低于约1小时时划算，在卫星图下不显著；不观测而选最坏后悔更小一侧仅在黑潮主设置下显著（0.98至0.70小时），其余三种设置均不显著。未来工作将把该方法扩展至时变流场并开展实艇海试。

===== V5 =====
在五类响应策略的对比中，黑潮主设置下唯有基于合理集合控制尾部风险的保守准则与本文的门控后取保守策略显著降低了平均航时损失，而单纯加算、按期望时间选边与就地测流均未能显著改善结果（图\ref{fig:main}）；但这一不依赖观测的保守收益属于黑潮主设置，在其余三种设置中未能复现（见第\ref{sec:scope}节）。

===== V6 =====
图\ref{fig:main}、图\ref{fig:risk}(b)、表\ref{tab:scope}：在粗图误差大的湾流区与阿古拉斯回流区，门控后上浮取当天0.5°图分别将平均损失从3.56降至1.31小时、从6.87降至2.20小时；黑潮主设置下上浮代价低于约1小时时门控后上浮更优，不观测的门控后取保守将平均损失从0.98降至0.70小时（该保守收益仅在此设置下显著）。
