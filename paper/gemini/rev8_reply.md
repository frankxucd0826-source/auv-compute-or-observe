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
