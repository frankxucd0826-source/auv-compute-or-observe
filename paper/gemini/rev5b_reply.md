===== FILE: sections/title.tex =====
合理反例检验：粗分辨率海流图下自主水下航行器何时计算、何时观测

===== FILE: sections/abstract.tex =====
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

===== FILE: sections/intro.tex =====
\section{引言}

海洋大数据的计算引擎正从岸基超算中心向移动观测平台边缘延伸，使“继续计算、补充观测还是立即行动”成为自主水下航行器必须面对的在线决策问题。传统流程依赖岸基中心汇集卫星与模式产品并下发指令\cite{chassignet2007hycom,chin2017mur}，但水下声学通信带宽极窄且上浮卫星通信耗时耗能，长航程航行器必须依靠低功耗机载计算模块独立完成环境推演与重规划\cite{remus100,jetsonorinnx}。由于机载算力与电池能量受限，航行器既不能无限制地进行高分辨率搜索，也不能频繁中断航行去原位测流或上浮通信\cite{horvitz1987reasoning,russell1991right}。如何在计算、观测与行动之间分配资源，构成了海洋边缘智能的核心挑战\cite{sung2021quit,magnino2026metareasoning}。

在台湾以东至东海的黑潮强流区，当航行器携带数天前下发的粗分辨率海流图执行绕障航行时，选错绕行方向将导致数小时的航时损失。长航程航行器对水巡航速度约为1.0米/秒，与黑潮主轴及邻近涡旋流速相当。在相距百余千米的起终点之间绕越禁航区时，从左侧或右侧绕行是不可逆的二元拓扑决策：一旦驶入逆流一侧，不仅航时大增，还可能因顶流过强而无法通行。本文考虑航行器只携带3天前制作的1°粗分辨率海流图（简称粗图）的情形：该图既丢失了中尺度锋面与涡旋切变，又包含数天内流轴摆动的时效误差，极易误导左右选边。

面对粗图上的航路决策，常规做法是在当前海流图上投入更多算力以加密网格与航向离散度\cite{lolla2014levelset}，但当环境信息本身缺失时，这种确定性等价做法难以奏效。若左右两侧在粗网格上的预计航时接近，规划器会自然地细分网格以分辨快慢。然而，这混淆了求解器粗糙与海洋环境不确定性：加密网格只能减少同一张粗图上的离散误差，却不能提供任何关于真实涡旋位置的新信息\cite{jiang2015horizon,cuadron2025overthinking}。正如第3节前期赤潮巡测研究所示，当背景场陈旧时，成百上千倍地增加机载推演只会使规划器在想象模型上的自评不断虚高，而航线在真实海洋中的价值早已饱和\cite{smith2006curse}。

第二种常见路径是利用集合预报开展风险感知航路规划，但现有方法不仅无法回答何时应停止计算或去观测，还容易因有限抽样漏掉翻转决策的流场\cite{wang2016path,subramani2018stochastic,kularatne2018forecast}。集合规划通过在数十个扰动流场中评估平均航时或翻转比例来折中选路，但将不确定性视为静态输入，缺乏在计算与观测之间切换的元推理机制\cite{lin2015metareasoning,elboher2023formal}。进一步而言，随机抽取的几十个集合成员往往集中于高概率平庸状态，难以覆盖合理误差球内那些物理相容却使所选航路急剧恶化的不利流场，从而低估了选错一侧的尾部风险\cite{benhaim2006infogap,marx2020predictive}。

第三种路径是基于信息价值的自适应采样，即主动前往不确定性最高的海区测量，但对整个海流场有价值的信息并不等同于对左右选边有价值的信息\cite{fossum2019,hollinger2014sampling}。传统自适应采样以降低全场估计方差或最大化互信息为目标\cite{srinivas2012gpucb}；然而在绕障任务中，若禁航区外某处的误差对左右航时影响相同，测量它便徒耗航时；反之，顺路在起点附近测流虽代价低廉，若决定两侧快慢的关键切变远在数十千米之外，近处测量也无法改变决策。序贯实验设计与模型判别理论指出，真正决定是否需要新信息的，是在现有证据下能否找到与当前观测同样相容、却要求采取相反行动的竞争模型\cite{chernoff1959sequential,box1967discrimination,garivier2016optimal,attia2018goal}。

为此，本文提出“合理反例检验”：机载计算与现场观测消除的是两类不同性质的不确定性；当两侧难分伯仲是因为求解网格粗糙（数值歧义）时，多算即可做对决定；而当存在与粗图同样相容、却使另一侧明显更快的合理海流（环境歧义）时，继续计算无法分辨真伪，唯有引入新观测才能消解，且在观测过贵时应直接选择最坏后悔更小的一侧。我们将这一判别转化为操作问题：针对粗图推荐的一侧，能否在多年海洋大数据标定的合理集合内搜出使另一侧更快、且让当前选择付出沉重代价的合理反例？在图\ref{fig:overview}所示的2022年1月18日测试任务示例中，粗图上两侧只差约0.3小时且地图推荐左侧，继续加密网格只会把这一账面差值算得更细，而合理反例检验在合理集合内搜出了使左侧明显变慢、右侧更快的物理相容流场，准确预警了真实海洋中右侧快11.7小时的逆流风险，并指导航行器执行门控决策。

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{fig_route_overview}
\caption{粗分辨率海流图下的航路决策与合理反例检验（2022年1月18日任务示例）。(a) 航行器携带的3天前1°粗图，左侧航时37.7小时、右侧38.0小时，地图选左侧；(b) 在大数据标定的合理集合内搜出的合理反例海流，左侧55.7小时、右侧44.1小时；(c) 当天1/12°真实海流，左侧53.4小时、右侧41.7小时，右侧实际快11.7小时；(d) 本文决策流程：先校验粗图两侧时间差是否小于数值误差容限以决定是否按需精算，再通过反例检验计算最坏后悔，最坏后悔小则照地图走，大则在观测便宜时上浮取新图、观测昂贵时改选最坏后悔更小的保守一侧。再多的机载计算也只能把粗图上的0.3小时差值算准，唯有合理反例检验能显式找出(b)(c)这类同样合理却翻转决策的海洋状态。}
\label{fig:overview}
\end{figure}

本文的主要贡献如下：
\begin{itemize}
    \item \textbf{概念与判别准则创新：}在航路决策中分离了可由计算消除的“数值歧义”与需靠新信息或保守决策应对的“环境歧义”，提出以最坏合理后悔为核心判据的合理反例检验框架，明确了边缘计算与海洋观测的功能边界。
    \item \textbf{大数据标定与高效反例搜索：}利用多年再分析海流标定旧粗图的无散流函数误差模态及覆盖90\%以上真实时间差的合理集合半径，结合包络定理梯度与球面投影搜索，以约71次标准网格求解直接定位最坏后悔流场。
    \item \textbf{黑潮强流区系统实证：}在六年黑潮再分析海流共1333个任务上证实，64倍算力仅修复28\%的粗算错误，而99.7\%的任务存在合理反例；最坏后悔前20\%的任务集中了67\%的损失，门控后取保守将平均航时损失降低28\%，并给出了原位测流与上浮取图的收益边界。
\end{itemize}

本文其余部分组织如下：第2节回顾相关工作；第3节简述前期赤潮巡测研究；第4节建立绕障航路决策模型；第5节详述合理反例检验与门控方法；第6节给出实验结果与适用范围；第7节拆解创新点与研究脉络；第8节总结全文。

===== FILE: sections/related.tex =====
\section{相关工作}

\subsection{受限理性元推理与智能体过度思考}
机载算力分配源于受限理性与元推理理论，核心是评估“计算的价值”是否超过其时间与能量代价\cite{horvitz1987reasoning,russell1991right}。在机器人运动规划中，研究者通过学习停止规则或自适应计算预算来决定何时终止搜索并执行动作，或使规划与移动并行交织\cite{xiao2020thinking,sung2021quit,elboher2023formal,magnino2026metareasoning}。然而，当内部环境模型存在偏差时，延长规划视野或增加搜索深度反而会放大模型误差，诱发决策分析中的“优化器诅咒”，使规划器陷入无益的过度思考\cite{smith2006curse,jiang2015horizon,cuadron2025overthinking}。近期在智能体推理与任务消歧中也发现了相似规律：当外部环境状态未知或指令存在多重解释时，增加测试时计算无法替代与环境交互或主动寻求澄清\cite{hunt2021formalizing,shen2025thinking,kobalczyk2025active}。与仅关注何时停止搜索的元推理不同，本文将模糊性拆解为求解器粗糙引起的数值歧义与地图失真引起的环境歧义，从而在计算、观测与保守行动之间建立切换准则。

\subsection{面向决策的信息获取与多解性判别}
并非所有减少环境不确定性的观测都能改善特定决策，唯有能区分竞争假设的信息才具决策价值\cite{chernoff1959sequential,box1967discrimination}。在统计实验设计与多臂赌博机中，最优臂识别与信息导向采样专门收集能尽快排除次优选项的样本，而非均匀降低全局方差\cite{garivier2016optimal,russo2018thompson,russo2018ids}；目标导向实验设计同样强调只针对目标泛函优化传感器布放\cite{attia2018goal}。与之呼应，信息间隙决策理论与预测多解性研究指出，当多个与数据同样相容的模型给出相反预测时，单靠点估计无法保证安全，必须考察不确定性半径内的最坏表现\cite{benhaim2006infogap,marx2020predictive}。不同于在离散假设空间或线性反问题中计算期望信息增益，本文利用包络定理直接在连续无散海流场上沿梯度搜寻翻转二元航路选择的物理反例，以最坏后悔度量环境歧义的严重程度。

\subsection{不确定海洋流场中的航路规划与自适应采样}
强海流下的自主水下航行器路径规划常利用图搜索或水平集方程在确定性流场中求取时间最优轨迹\cite{dijkstra1959note,lolla2014levelset}。为应对海洋预报不确定性，研究者提出了集合期望与风险折中规划、动态正交随机时间最优控制以及纳入误差协方差的鲁棒路径搜索\cite{wang2016path,subramani2018stochastic,kularatne2018forecast}；海洋自适应采样则利用高斯过程或集合卡尔曼滤波在线更新叶绿素或流场估计，引导航行器前往高信息增益区\cite{anderson2001eakf,srinivas2012gpucb,hollinger2014sampling,fossum2019}。然而，现有不确定流场规划大多将集合样本作为固定输入来寻找单一路径，既不评估有限集合是否漏掉了翻转拓扑走向的流场，也不回答是否值得付出时间代价去换取新海流图；本文则将多年海洋再分析大数据转化为合理流场集合的物理边界，专门解决粗图下“算、测、走”的闭环元决策问题。

===== FILE: sections/prior.tex =====
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

这一前期探索促使作者把问题收紧：既然当多个可能世界都与旧图相容、却要求采取不同行动时，继续计算无法将它们区分开来，那么在强海流绕障这种选错一侧就会付出数小时代价的二元拓扑决策中，能否直接检验“是否存在另一个同样合理却让当前选择吃亏的流场”，并以此决定何时该算、何时该测、何时该保守绕行？这正是本文接下来要解决的问题。

===== FILE: sections/problem.tex =====
\section{问题建模}

\subsection{任务场景与海洋再分析数据}
本文研究自主水下航行器在强流海区携带陈旧粗分辨率海流图执行绕障航行的二元路径决策问题，参数汇总于表\ref{tab:settings}。研究海区取台湾以东至东海的黑潮区（23°--31°N、121°--129°E），采用HYCOM全球再分析（GLBy0.08，实验93.0\cite{chassignet2007hycom}）10米水深处的1/12°水平流速场，2019年1月1日至2024年8月29日每3天一张快照共689张；其中2019--2021年作为开发年份（710个任务），2022--2024年作为独立测试年份（623个任务）。每张快照生成2个任务，起终点相距100--140千米、离岸不少于20千米，中点设半径15千米的圆形禁航区，只保留粗图上任务区平均流速不低于0.3米/秒的强流任务。航行器下水时携带3天前生成的1°粗图（格内平均），当天1/12°场作为真实海流。

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
航行器面对粗图 $\boldsymbol{u}_0$ 可在五类动作中选择：（1）同一张粗图上加算：用粗算、标准或照地图走（精算）选更快一侧出发；（2）改变决策准则：在32个合理海流上按期望时间选边，或采取保守（最坏后悔最小）准则；（3）就地取新信息：原地停留测（2小时测12次）、沿途测30千米、沿途测60千米后再决定是否换边，或绕行定点测（去前方40千米内反例与地图差别最大处测量；测流噪声0.05米/秒，同化时取0.15米/秒\cite{anderson2001eakf}）；（4）上浮取新图：每次耗时1小时接收当天1°图或0.5°图；（5）本文反例检验门控：仅在最坏后悔超阈值时触发门控后取保守或门控后上浮取图。定义任务航时“损失”为实际总耗时 $T_{\text{total}}$ 减去真实更快一侧的航时：
\begin{equation}
\mathcal{L} = T_{\text{total}} - \min\left\{ T_{\text{L}}(\boldsymbol{u}_{\text{true}}),\, T_{\text{R}}(\boldsymbol{u}_{\text{true}}) \right\}.
\label{eq:loss}
\end{equation}

\subsection{问题剖析：为何常规计算与盲目观测难以奏效}
选对绕行一侧依赖禁航区两侧数十千米尺度的海流切变，而3天前1°粗图抹平了这一信息；机载计算只能锐化粗图自身的几何推论，却无法创造缺失的物理信息。这带来两个结构性性质：

第一，粗图上的时间差模糊性源于“数值歧义”与“环境歧义”两类不同机制。当 $|\Delta T(\boldsymbol{u}_0)|$ 很小时，若仅因8千米粗算网格折线失真，换成2千米精算即可看清粗图倾向；但若精算选出某侧 $s_0$ 后，合理集合 $\mathcal{U}(r)$ 内仍存在使另一侧明显更快的流场 $\boldsymbol{u}^*$，继续加密网格也无法判断真实海洋接近 $\boldsymbol{u}_0$ 还是 $\boldsymbol{u}^*$。

第二，是否值得去观测，不取决于是否存在合理反例，而取决于该反例成真会让当前决策多损失多少小时（最坏后悔）以及观测能否触及关键切变区。由于旧粗图误差相关长度达数十千米，几乎任何任务都能找到某个让另一侧略快的合理流场；唯有直接求出所选一侧的最大可能航时劣势并与观测代价比较，才能避免过度反应。

===== FILE: sections/method.tex =====
\section{方法}

本文提出如图\ref{fig:overview}(d)所示的四步决策方法：先通过按需精算消除数值歧义，再在多年海洋大数据标定的合理集合内用投影梯度上升搜索最坏合理反例，最后依据最坏后悔执行门控分流。

\subsection{按需精算：数值歧义的快速识别与消除}
区分求解器误差与环境不确定性的首要原则，是仅当粗算时间差落在数值离散误差容限之内时才动用精算。常规确定性规划要么一律使用粗算而在两侧航时接近时受网格锯齿误导，要么对所有任务一律执行耗时64倍的精算，在粗图上两侧本就相差十几个小时的任务上浪费算力。

我们在开发年份任务上离线对比同一张粗图 $\boldsymbol{u}_0$ 的粗算时间差 $\Delta T_{\text{coarse}}(\boldsymbol{u}_0)$ 与精算时间差 $\Delta T_{\text{fine}}(\boldsymbol{u}_0)$，取绝对偏差 $|\Delta T_{\text{coarse}}(\boldsymbol{u}_0) - \Delta T_{\text{fine}}(\boldsymbol{u}_0)|$ 的95\%分位数作为数值误差容限 $\tau_{\text{num}} = 3.2$ 小时。在线执行时，航行器先用粗算求 $\Delta T_{\text{coarse}}(\boldsymbol{u}_0)$；若 $|\Delta T_{\text{coarse}}(\boldsymbol{u}_0)| \ge \tau_{\text{num}}$，直接采纳粗算结果；仅当 $|\Delta T_{\text{coarse}}(\boldsymbol{u}_0)| < \tau_{\text{num}}$ 时才判定存在数值歧义并触发精算，以很小的平均算力确保地图基准选择 $s_0$ 不受求解器粗糙度误导。

\subsection{反例检验：基于包络定理的合理集合投影梯度搜索}
判断粗图所选一侧 $s_0$ 是否面临严重环境歧义，最直接的准则是主动在合理集合 $\mathcal{U}(r)$ 内寻找使 $s_0$ 相比另一侧 $\bar{s}_0$ 尽可能变慢的最坏合理反例，而非在少数随机样本上求平均。现有集合规划通常随机抽取32个流场样本统计航时均值或翻转比例\cite{wang2016path}；然而，翻转比例只反映有多少样本翻转了决定，不反映翻转后损失有多大；而两侧时间差只对少数扰动方向敏感，随机样本未必落在这些方向上。

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
\Require 粗分辨率海流图 $\boldsymbol{u}_0$，标定误差幅度图 $\sigma(\boldsymbol{x})$ 与无散流函数基 $\{\phi_k\}_{k=1}^{K}$，标定半径 $r=1.5$，数值误差容限 $\tau_{\text{num}}=3.2$ 小时，门控阈值 $\theta=8.0$ 小时，上浮取图代价 $c_{\text{surf}}$ 及代价平衡点 $c^* \approx 1.0$ 小时。
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

===== FILE: sections/experiments.tex =====
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
在同一张3天前1°粗图上大幅增加计算量只能消除少部分数值歧义，而在包住真实海洋的合理集合内，几乎每个任务都存在翻转决策的合理反例。在测试年份中，将求解算力从粗算增加64倍至精算，选错一侧的任务比例仅从21.7\%降至19.7\%，即只修好了粗算错误的28\%，对应的平均损失变化在统计上也不显著；相反，若不加计算而换成当天0.5°图，选错率立即降至10.4\%（图\ref{fig:ambiguity}(a)）。多算无效的原因在于环境本身的多解性：在开发年份覆盖93\%真实时间差、测试年份覆盖94\%的标定半径 $r=1.5$ 处，99.7\%的测试任务都存在至少一个使另一侧更快的合理反例（图\ref{fig:ambiguity}(b)）。因此，在旧粗图下环境歧义是常态，仅问“是否存在反例”没有区分度，真正决定行动的是反例造成的最坏后悔有多大。

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

各类观测手段的成败则取决于观测视野与时间代价的权衡。就地原位测流均未能带来显著净收益（与精算地图之差的置信区间或显著为正、或包含0）：原地停留测耗去2小时却只测到起点一处；绕行定点测平均要先花15.4小时才能顶流赶到前方测点，得不偿失；沿途测30千米后换边的任务仅占3.4\%（其中81\%换对），因为此时尚未进入禁航区两侧的核心切变区，而沿途测60千米后换边的任务虽增至18.8\%，但由于已深入半程、折返代价过大，换边只有15\%是划算的。对于能更新全局流场的上浮取当天0.5°图（图\ref{fig:risk}(b)），当单次上浮代价为0.5小时时，门控后上浮取图的平均损失为0.55小时，优于门控后取保守的0.70小时；而当上浮代价升至1.0小时时，门控后上浮取图升至0.78小时，交点出现在0.5至1小时之间（近1小时），此后无需观测的门控后取保守成为更优选择。

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

===== FILE: sections/innovation.tex =====
\section{原创创新点拆解}

本研究从《海洋大数据技术原理与应用》课程核心议题出发，经历了问题提出、实证证伪与问题锐化的完整演进。课上讲授的“海洋大数据的计算引擎”使作者联想到：自主水下航行器端侧的算力与能量十分有限，计算、测量与运动之间必须权衡。作者最初提出的问题是：当航行器带着几天前的旧卫星图下水时，应把时间花在继续机载推演上，还是停下来重新观测？在东海赤潮巡测前期研究（第3节）中，我们发现增加推演计算只会让规划器在想象模型里自评虚高，真实收益早已饱和，且平滑标量场中用时分配的改进空间仅约0.02，远小于下水位置与地图新鲜度的影响。针对前期方法增益小、新意不足的缺陷，作者将问题锐化并转向强海流绕障这一选错一侧就损失数小时的二元决策：当存在多个与旧图同样相容、却要求采取相反行动的海洋状态时，再多计算也无法区分；能否在历史大数据界定的合理流场范围内，专门搜出一个让另一侧更好、且让当前选择吃亏的合理反例？这一追问直接催生了本文的合理反例检验框架（表\ref{tab:innovation}）。

\begin{table}[htbp]
\centering
\caption{本文核心原创创新点、已有做法对比、实验证据与局限拆解。}
\label{tab:innovation}
\small
\begin{tabular}{@{}p{0.15\linewidth}p{0.21\linewidth}p{0.23\linewidth}p{0.19\linewidth}p{0.14\linewidth}@{}}
\toprule
创新点 & 已有做法及其不足 & 本文做法 & 证据（图表） & 局限 \\
\midrule
1. 分离数值歧义与环境歧义的决策判据 & 确定性规划在粗图上盲目加密网格（误以为多算能消除一切模糊）；传统元推理只管何时停止搜索，不区分误差源于求解器还是环境模型失真。 & 提出数值歧义（小于粗精网格容限 $\tau_{\text{num}}$，靠按需精算消除）与环境歧义（合理集合内存在翻转决策的反例，只能靠新信息或保守应对）的二分准则。 & 图\ref{fig:overview}、图\ref{fig:curse}、图\ref{fig:ambiguity}(a)：64倍精算仅将选错率从21.7\%降至19.7\%，当天0.5°图则降至10.4\%。 & 仅在左右绕障的二元拓扑决策上验证，尚未扩展至多分支同伦路径。 \\
\addlinespace
2. 基于包络定理梯度的合理反例主动搜索 & 集合规划随机抽取数十个流场算均值或翻转比例；翻转比例只反映多少样本翻转了决定，不反映翻转后损失多大。 & 利用包络定理沿当前最快航线累加流速导数，一次梯度仅需2次最短路求解；先沿初始梯度跳至球面再投影细化，直接求最坏后悔。 & 图\ref{fig:main}、图\ref{fig:risk}(a)：最坏后悔前20\%任务捕获67\%损失，显著优于32成员集合翻转率（49\%）与地图差值（34\%）。 & 流场过大扰动下最短路拓扑可能跳变，使目标函数非凸、局部梯度近似产生折耗。 \\
\addlinespace
3. 海洋大数据驱动的合理集合与半径标定 & 鲁棒优化与信息间隙方法常假设空间均匀白噪声并主观设定不确定性半径，脱离海洋物理结构，易过度保守或漏报黑潮切变。 & 用三年历史再分析误差标定非均匀幅度图 $\sigma(\boldsymbol{x})$ 与76千米相关长度的无散流函数模态；以覆盖90\%以上真实两侧时间差标定最小半径 $r=1.5$。 & 图\ref{fig:data}、图\ref{fig:ambiguity}(b)、表\ref{tab:scope}：$r=1.5$在测试年份覆盖94\%真实差值；消融替换为历史相似日差值后保守增益消失（0.99 vs 0.95小时）。 & 依赖多年历史再分析数据标定平稳统计量，对台风过境等非平稳极端天气适应受限。 \\
\addlinespace
4. 权衡最坏后悔与观测代价的门控响应 & 自适应采样面向全场降方差去测流，或不论代价一律保守/一律上浮，忽视了原位测流看不见远方切变及上浮通信本身耗时。 & 以最坏后悔超阈值 $\theta=8$小时作为门控：超标且上浮代价低（$<1$小时）时上浮取新图，代价高或仅有原位测流时改选最坏后悔更小一侧。 & 图\ref{fig:main}、图\ref{fig:risk}(b)、表\ref{tab:scope}：门控保守将平均损失从0.98降至0.70小时（降28\%），并给出约1小时的上浮代价切换点。 & 不观测时门控保守（0.70小时）比一律保守（0.72小时）的额外边际增益较小，主收益源于最坏后悔准则本身。 \\
\bottomrule
\end{tabular}
\end{table}

在人机协同完成本研究的过程中，作者与人工智能工具的分工如下（详见附录B，完整对话记录见代码仓库）。作者提出了最初关于机载计算与观测如何权衡的问题；在第一版结果出来后要求改用真实卫星数据检验、补充对照与消融实验；在前期研究结果出来后指出用时分配增益过小、方法新意不足，并提出了“两条航路、一张粗图、能否找到让另一条路更好的合理海流反例”这一新问题，决定转向本文的研究。人工智能助手Claude（Anthropic）完成了文献检索、代码、实验与作图，并核对了正文中的数字与引用；Gemini（Google）根据Claude整理的事实清单与提纲撰写了论文文字。

===== FILE: sections/conclusion.tex =====
\section{结论}

本文针对自主水下航行器在粗分辨率海流图下执行强流绕障时的在线元决策问题，提出了基于海洋大数据标定的合理反例检验方法，阐明了一条基本原理：机载计算的职责是消除求解器近似带来的数值歧义，从而读出已有海流图的本来倾向；而当多年海洋大数据界定的合理集合内存在翻转航路优劣并造成严重航时损失的合理反例时，环境处于算力无法消解的环境歧义状态，航行器唯有通过低代价的大尺度观测引入新信息，或在观测昂贵时改选最坏后悔更小的保守航路，才能有效降低逆流风险。在台湾以东至东海黑潮区域六年再分析海流的系统实验表明，将航线求解算力提高64倍仅能修复28\%的粗算错误，而合理反例的最坏后悔将67\%的地图总损失锁定在排名前20\%的高危任务中，使门控后取保守在不消耗观测时间的条件下将平均航时损失降低28\%，并清晰给出了原位测流的局限与上浮取图的代价阈值。未来工作将把该方法扩展至随时间连续演变的四维流场，并结合实艇开展海上试验。

===== FILE: sections/appendix.tex =====
\section*{附录}

\subsection*{附录 A：代码与数据开源说明}
本研究的全部源代码、数据处理脚本、实验配置、统计汇总程序以及论文图表生成脚本均已开源于代码仓库：\url{https://github.com/frankxucd0826-source/auv-compute-or-observe}。

\begin{enumerate}
    \item \textbf{数据集来源：}主实验海流数据取自HYCOM全球海洋再分析公开服务（产品GLBy0.08，实验93.0，10米水深水平流速，区域23°--31°N、121°--129°E，2019--2024年）；第3节前期赤潮巡测研究的数据取自美国国家海洋和大气管理局海岸观测网公开的多星融合叶绿素产品与喷气推进实验室多尺度融合海表温度产品。
    \item \textbf{主要程序结构：}数据下载与预处理由 \texttt{scripts/download\_hycom.py} 完成；核心航路规划与反例检验软件包位于 \texttt{src/oceanroute/} 目录下，包含多精度网格最短路与包络定理梯度求解器（\texttt{solver.py}）、海流快照读取与粗图生成（\texttt{fields.py}）、旧粗图误差的多年数据标定与无散误差模态（\texttt{errormodel.py}）以及任务生成、反例搜索与测量更新（\texttt{mission.py}）；批量评估、统计重抽样汇总、事实清单生成与典型任务提取分别由 \texttt{experiments/route\_eval.py}、\texttt{experiments/route\_summary.py}、\texttt{experiments/route\_facts.py} 与 \texttt{experiments/route\_example.py} 执行；正文全部插图由 \texttt{paper/figures/fig\_route\_*.py} 系列脚本一键复现；前期赤潮巡测研究的对应脚本清单详见代码仓库根目录下的 \texttt{README} 文档。
\end{enumerate}

\subsection*{附录 B：人工智能工具使用说明}
根据课程论文规范，现将本论文研究与撰写过程中人工智能工具的使用情况如实说明如下：
\begin{enumerate}
    \item \textbf{作者：}提出了机载计算与现场观测如何权衡的初始问题；对第一版结果提出用真实卫星数据检验、补充对照与消融、按学术论文格式写作等要求；在前期研究结果出来后指出其提升小、新意不足，并提出“粗分辨率海流图下两条航路的合理反例”这一新问题，决定转向本文研究；对全文负责。
    \item \textbf{Claude（Anthropic）：}在作者授权下完成文献检索与核对、数据下载与全部代码、实验与统计、论文插图，整理写作提纲与由实验程序生成的事实清单，并逐项核对正文中的数字与引用。
    \item \textbf{Gemini（Google）：}根据Claude整理的提纲、术语表与事实清单撰写论文文字，再由Claude核对与修改。
    \item \textbf{可追溯性记录：}整个研究过程中作者与人工智能工具交互的完整对话记录、问题演进记录与多轮修改日志均保存在上述开源代码仓库中备查。
\end{enumerate}
