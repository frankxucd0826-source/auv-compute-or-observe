===== FILE: sections/title.tex =====
基于留出想象海洋与出发前预演的自主水下航行器计算与观测权衡方法

===== FILE: sections/abstract.tex =====
\noindent{\heiti 摘要：}自主水下航行器开展赤潮巡测时受通信、电池与时间约束，面对滞后卫星底图，需在开启高功耗芯片深想、维持后台规划巡航与停船复测间权衡。固定策略依赖历史任务调参，而经典单步元推理用搜索样本自评得分评估计算，会因优化器诅咒过度规划。本文利用八年东海卫星叶绿素数据标定底图误差，围绕3天前旧图生成48个随采样同化更新的想象海洋，划分为32个搜索用海洋与16个留出海洋。下水前以4个留出海洋为假想真值，按机载算力与功耗模拟五种策略的24小时任务并择优执行；或在线用留出海洋评估单步收益并配以两倍标准误判据。在422个赤潮窗口、四种硬件与两种真值模型上的实验表明：留出评判在64至200,000次推演下与真实价值偏差不超过0.005；在148个测试任务上，出发前预演无需历史任务即匹配调好策略与学习型选择器，主设置下比单步元推理降低遗憾0.011至0.022，在线留出估值亦将深想占比从80\%--97\%降至30\%--44\%并达预演水平。上述结果表明，以数据标定的留出想象海洋解耦搜索与评判可消除自评偏差，实现算力与观测的自适应权衡。

\vspace{4pt}
\noindent{\heiti 关键词：}海洋大数据；自主水下航行器；元推理；集合数据同化；赤潮巡测；优化器诅咒

\vspace{10pt}
\begin{center}
  {\zihao{4}\bfseries Balancing Computation and Observation for Autonomous Underwater Vehicles via Data-Calibrated Held-Out Imagined Oceans and Pre-Launch Rehearsal\par}
  \vspace{4pt}
  {\zihao{5} XU Chendong\par}
  {\zihao{-5}\itshape (Ocean College, Zhejiang University, Zhoushan 316021, China)\par}
\end{center}
\vspace{4pt}

\noindent{\bfseries Abstract:} During harmful algal bloom surveys without underwater communication, an autonomous underwater vehicle guided by a multi-day-old satellite map must trade off activating a high-power chip for deep route planning against cruising under low-power background planning or stopping to resample. Fixed time-allocation rules require tuning on past missions from the same hardware, whereas classic online one-step metareasoning evaluates computation using the planner's score on the searched ensemble members, which is inflated by the optimizer's curse and causes over-planning. We propose using uncertainty-calibrated held-out imagined oceans derived from satellite big data as an independent yardstick for the value of computation, via pre-launch rehearsal or online held-out valuation. Using eight years of East China Sea satellite chlorophyll-a data to calibrate stale-map error, the vehicle generates 48 imagined oceans around a 3-day-old map, updates them via a localised ensemble adjustment Kalman filter, and splits them into 32 searched and 16 held-out oceans. Before launch, a support computer treats 4 held-out oceans as imagined truths and simulates 24-hour missions for five strategies under the vehicle's processor speed and battery budget; the online variant evaluates single-step gains on the 16 held-out oceans with a two-standard-error switching threshold. Across 422 bloom windows, four hardware configurations, and two truth models, held-out evaluation stays within 0.005 of true route value up to 200,000 rollouts. Across 148 test missions, rehearsal matches historically tuned and learned selectors without prior missions, lowers regret by 0.011--0.022 over classic one-step metareasoning under the main truth model, and online held-out valuation cuts high-power chip usage from 80\%--97\% to 30\%--44\% while matching rehearsal.

\vspace{4pt}
\noindent{\bfseries Keywords:} ocean big data; autonomous underwater vehicle; metareasoning; ensemble data assimilation; harmful algal bloom survey; optimizer's curse

===== FILE: sections/intro.tex =====
\section{引言}

卫星海洋遥感大数据与自主水下航行器的结合，正在将海洋监测从预设航线走航转变为先验地图引导的现场自适应巡测\cite{fossum2019}。多年累积的遥感产品提供了大尺度环境背景与演变统计，航行器则深入云层遮挡与遥感平滑难以企及的水体采集高分辨率样本。然而机动平台受制于有限的机载电池能量、嵌入式计算速率与固定作业时间窗口\cite{xiao2020thinking, magnino2026metareasoning}。航行器获取新观测后，既可调用机载高功耗芯片开展密集航线推演以优化后续路径，也可维持低功耗处理器后台规划而将电能与时间用于巡航采样或原位复测\cite{horvitz1987reasoning, russell1991right, shen2025thinking}。由于内部计算与外部观测共享同一块电池和同一任务窗口，何时继续计算、何时继续观测，是大数据驱动自主海洋观测的核心控制问题\cite{hunt2021formalizing}。

东海有害赤潮应急巡测集中体现了先验底图失真、水下通信受阻与机载资源受限带来的决策困难\cite{fossum2019, lou2014diurnal}。2023年中国海洋灾害公报记录全年赤潮46次、累计面积约$1500\text{ km}^2$，其中有毒有害赤潮29次\cite{mnr2024bulletin}。浙江台州、温州与宁波外海晚春至初夏常暴发东海原甲藻赤潮\cite{zhao2025distinguishing}，表层斑块在潮汐作用下往复漂移演变\cite{lou2014diurnal}。应急指挥中心通常向$80\text{ km}\times 80\text{ km}$海域派出一台百米级航行器开展24小时巡测，要求尽早定位叶绿素最浓水体并随时响应位置查询\cite{remus100}。受多星产品合成延迟、云区经验正交函数插补平滑\cite{beckers2003dineof}、水色反演偏差\cite{ye2021cocts}及船只航渡影响，航行器下水前装入的常是3天前旧图；加之水下几乎无法实时通信，航线重规划与资源调配均须由机载计算机独立完成\cite{jetsonorinnx}。

传统海洋巡测规则与预设时间分配策略难以在缺乏历史任务数据时适配不同机载硬件。一方面，割草机式全覆盖\cite{galceran2013coverage}、贪心追踪、上置信界采样\cite{srinivas2012gpucb}与汤普森采样\cite{russo2018thompson}等启发式规则将每步计算开销视为常数，忽略了多步前瞻规划对规避局部次优峰值的作用\cite{hollinger2014sampling}。另一方面，在多步规划器上采用固定时间分配策略（如仅靠后台规划的“一直走”或周期性开启高功耗芯片的规则），其表现高度依赖处理器速度与芯片功耗。当更换计算模块或电池配置时，需依靠该型硬件在大量历史赤潮任务中的实测表现才能选出合适策略，而新平台首次投入应急巡测时并无历史档案。

从历史任务中训练策略选择器同样受制于高昂采集成本与剧烈的任务间环境波动。近期机器人元推理研究尝试由历史任务训练回归或分类模型，根据出发前环境特征选择计算预算或用时策略\cite{sung2021quit, magnino2026metareasoning}。然而赤潮现场的初值格局、峰值位置与入水起点千差万别，任务窗口间的天然遗憾波动远大于优良策略间的平均性能差距，基于旧图静态特征训练的选择器极易被背景噪声淹没，且需要上百次历史任务作为训练样本。

经典在线单步元推理虽无需历史任务训练，但因轻信规划器在搜索样本上的自评得分而易陷入过度规划\cite{horvitz1987reasoning, russell1991right, cuadron2025overthinking}。该方法在每个周期比较“多算一步的得分增量”与“耗电及延误代价”来决定是否开启高功耗芯片或停下复测\cite{lin2015metareasoning, elboher2023formal}。由于航行器只能在一组由旧图生成的想象海洋上搜索航线，当规划器在同一批有限样本上既搜索航路点又评估预期收益时，优化过程会迎合特定样本中的随机正涨落，产生“优化器诅咒”\cite{smith2006curse, vanhasselt2010double}。即便额外推演在真实海洋中已不再改善航线，内部自评得分仍随推演次数持续虚高，误导控制器频繁开启高功耗芯片并中途停船\cite{jiang2015horizon, cuadron2025overthinking}。

针对上述问题，本文的核心思想是：航行器不应依据规划器自身的搜索得分决定是否继续计算，而应利用多年卫星大数据标定误差的留出想象海洋作为独立标尺，在未参与搜索的想象海洋上评判计算与观测结果。本文用八年东海卫星叶绿素数据标定滞后底图误差，围绕旧图生成48个随现场采样经集合调整卡尔曼滤波\cite{anderson2001eakf, gaspari1999correlation}同步更新的想象海洋，划分为32个搜索用海洋与16个留出海洋。基于“搜索与评判分离”准则，本文提出两种无需历史任务的控制方式：下水前，由母船或岸基计算机以4个留出海洋为假想真值，按机载算力与功耗将五种策略各完整预演一遍24小时任务并择优执行；航行中，在单步元推理中改由16个留出海洋评估计算与采样收益并配合两倍标准误切换判据，在离线与在线两个层面消除自评乐观偏差。

本文主要贡献如下：
\begin{itemize}
  \item \textbf{提出独立于搜索过程的计算价值留出评判准则：}揭示了未知海洋巡测中过度计算的根源在于规划器对搜索用海洋的过拟合，提出将卫星数据标定的想象海洋划分为搜索用海洋与留出海洋，以留出海洋上的结果作为衡量计算收益的无偏标尺。
  \item \textbf{构建硬件自适应的出发前预演与在线留出估值方法：}设计了结合局地化集合同化与交叉熵规划的五种用时策略，提出在母船或岸基计算机上以留出海洋为假想真值开展全任务预演，并将留出评判嵌入在线单步元推理，无需历史任务即可适配不同算力与功耗。
  \item \textbf{提供基于八年东海赤潮窗口与双真值模型的实证及边界刻画：}在422个赤潮窗口、四种硬件与两种真值模型上开展配对检验，表明深度时空模型无法替代现场采样、留出评判将跨三个半数量级推演预算的价值偏差控制在0.005以内、停下复测在全参数空间均得不偿失，且出发前预演与在线留出估值均达到依赖历史任务方法的水平。
\end{itemize}

本文其余章节安排如下：第2节回顾相关工作；第3节建立巡测模型并剖析问题矛盾；第4节阐述留出想象海洋、出发前预演与在线留出估值方法；第5节报告实验结果与机理分析；第6节总结全文。

===== FILE: sections/related.tex =====
\section{相关工作}

\subsection{元推理与计算行动权衡}

有限理性与元推理研究智能体在计算受限时如何分配内部推理与外部行动\cite{horvitz1987reasoning, russell1991right}。经典单步元推理估计额外一次搜索对动作期望效用的提升，并在增益低于延迟代价时终止搜索\cite{lin2015metareasoning}。在机器人并发控制中，边移动边思考框架权衡继续规划的路径改善与推迟动作切换的跟踪偏差\cite{xiao2020thinking, elboher2023formal}；另一类工作利用历史任务轨迹训练停止策略或预算选择器，由环境特征预测不同算力预算的收益\cite{sung2021quit, magnino2026metareasoning}。近期大模型智能体研究也发现过度思考会挤占交互机会并降低成功率\cite{shen2025thinking, cuadron2025overthinking, hunt2021formalizing}。然而现有方法评估规划收益时普遍直接信任规划器在搜索空间上的自评得分，或依赖大量历史任务训练选择器；本文指出不确定海洋场中自评得分受优化器诅咒污染，并利用留出想象海洋在无历史任务条件下无偏评估计算价值。

\subsection{海洋自适应采样与信息收集}

自主水下航行器在藻华追踪中的应用推动了从规则覆盖向自适应采样的演进\cite{fossum2019}。割草机式全覆盖航线均匀扫测海域\cite{galceran2013coverage}，但在24小时大范围赤潮巡测中仅能覆盖局部水域。信息收集算法常利用高斯过程维护环境均值与方差，采用贪心策略、上置信界采样\cite{srinivas2012gpucb}或汤普森采样\cite{russo2018thompson}驶向高浓度或高不确定性位置，或通过采样树搜索规划多步路径\cite{hollinger2014sampling}。东海原甲藻赤潮遥感研究揭示了其晚春至初夏高发及随潮汐往复漂移的特征\cite{lou2014diurnal, zhao2025distinguishing}。然而现有自适应采样方法均假定机载规划的计算开销可忽略或固定不变，未考虑高功耗芯片与推进电机共享电池及时间的耦合约束；本文将机载算力、芯片功耗与原位复测纳入统一决策空间，刻画了多步规划与机动采样的收益边界。

\subsection{优化器诅咒与集合数据同化}

在随机优化与强化学习中，用同一批有限样本寻优并估计价值会放大随机正误差，即“优化器诅咒”\cite{smith2006curse}；双估计方法通过将动作选择与价值评估解耦至独立样本集来消除过估计\cite{vanhasselt2010double}，而模型误差也会限制有效规划视野\cite{jiang2015horizon}。海洋环境重构方面，业务化水色遥感利用经验正交函数插补生成逐日无云叶绿素场\cite{beckers2003dineof}，结合多尺度融合海表温度\cite{chin2017mur}、水色实测精度评估\cite{ye2021cocts}及联合嵌入预测架构等时空模型\cite{assran2025vjepa2}刻画表层演变，并以序列集合调整卡尔曼滤波\cite{anderson2001eakf}配合五阶分段有理局地化函数\cite{gaspari1999correlation}同化现场观测。目前尚未见将集合同化样本集与双估计思想结合以消除元推理自评偏差的研究；本文将同化更新的想象海洋划分为搜索用海洋与留出海洋，使卫星大数据标定的集合成员充当评判计算价值的独立标尺。

===== FILE: sections/problem.tex =====
\section{问题建模}

\subsection{巡测场景与卫星遥感数据}

东海赤潮应急巡测场景建立在八年真实卫星遥感数据之上，真实海洋由任务当天卫星图构建，而航行器出发时仅携带3天前旧图。数据集采用美国国家海洋和大气管理局海岸观测网2018年1月1日至2026年10月23日共3197天的$2\text{ km}$逐日多星融合叶绿素a产品（经经验正交函数插补去云\cite{beckers2003dineof}，覆盖$25^\circ\text{--}33^\circ\text{N}$、$119.5^\circ\text{--}127^\circ\text{E}$，每日$385\times 361$格）及喷气推进实验室多尺度融合海表温度产品（重采样至$0.04^\circ$）\cite{chin2017mur}。全文除特别说明外，叶绿素a浓度、误差与遗憾均以$\log_{10}(\text{浓度}/\text{mg m}^{-3})$为单位。

我们在每年4至6月浙江外海陆架检索离岸至少$30\text{ km}$、平滑峰值超$5\text{ mg m}^{-3}$的藻华中心，随机平移至多$16\text{ km}$后截取$80\text{ km}\times 80\text{ km}$窗口（距岸$15\text{ km}$内禁航，可航行占比不低于80\%，窗内极差不低于0.3），共得2018至2022年开发集窗口274个、2023至2026年测试集窗口148个，航行器从窗口边缘随机可航行格入水（表\ref{tab:settings}）。鉴于东海表层赤潮斑块主要随水体与潮汐整体往复漂移\cite{lou2014diurnal}，本文在随表层水体漂移的参考系中建模，斑块相对水体静止，平流与生消作用体现在3天旧图与当天卫星图的实测演变统计中。

实验设置两种真值模型：主设置“当天卫星图 + 小尺度变化”在当天卫星图上叠加标准差$s_{\text{sat}}=0.15$、相关长度3格（$6\text{ km}$）的零均值高斯随机场，表征遥感平滑的亚像素斑块与反演残差（幅值按海洋一号丙星水色传感器在东海与南海实测验证约39\%的无偏相对差异即对数空间约0.15标定\cite{ye2021cocts}）；“当天卫星图”设置直接以当天卫星图本身为真值（$s_{\text{sat}}=0$）。两种设置下先验底图均为3天前卫星图$c_{\text{map}}(\mathbf{x})$。

\subsection{航行器动作空间与能耗模型}

参照百米级轻型航行器参数\cite{remus100}，航行器巡航速度$1.5\text{ m/s}$，电池容量$1\text{ kWh}$，巡航总功率$45\text{ W}$（含导航、传感器与低功耗处理器的平台功率$15\text{ W}$，推进功率$30\text{ W}$）。高功耗芯片参照嵌入式边缘图形处理器设定\cite{jetsonorinnx}，开启深想额外消耗$+20\text{ W}$（“省电加速器”为$+5\text{ W}$），推演速度为低功耗处理器的50倍。因二维双航路点规划器是对三维流场与避障路径评估的简化替代，实验以低功耗处理器每分钟推演次数表征基础算力（5、20或100次/分，扫描5至200次/分）。

在$T=24\text{ h}$内按$\Delta t = 20\text{ min}$划分为72个周期，机体动作与大脑规划并行执行\cite{xiao2020thinking, elboher2023formal}。机体选择“走”时沿当前航线航行$1.8\text{ km}$、每千米采样一次（24小时航程约$120\text{--}130\text{ km}$）；选择“停下”时关停推进器随水漂流，每4分钟对同一水体采样一次（每周期5次）。荧光计观测$y$与所在网格真实浓度$c(\mathbf{x})$满足：
\begin{equation}
  y = c(\mathbf{x}) + \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, 0.1^2)
  \label{eq:obs}
\end{equation}
大脑规划可维持低功耗处理器后台规划，或开启高功耗芯片“深想”（推演次数扩至50倍）。新航线以当前周期结束时刻的预计位置为起点搜索，并在周期末替换旧航线；满24小时或电量耗尽即停止机动与采样。

\subsection{实时报告与时间平均遗憾}

在$T=24\text{ h}$内任意时刻$t \in [0, T]$，航行器从已访网格集合$\mathcal{V}(t)$中报告当前内部集合均值$\bar{c}_t(\mathbf{x})$最高的位置$\hat{\mathbf{x}}(t)$（若提前耗尽电量则冻结至$T$）：
\begin{equation}
  \hat{\mathbf{x}}(t) = \arg\max_{\mathbf{x}\in\mathcal{V}(t)} \bar{c}_t(\mathbf{x})
  \label{eq:answer}
\end{equation}
单次任务的时间平均遗憾$R$定义为全窗口真实最高浓度与实时报告位置真实浓度之差的时间均值：
\begin{equation}
  R = \frac{1}{T}\int_0^T \left[\max_{\mathbf{x}} c(\mathbf{x}) - c\big(\hat{\mathbf{x}}(t)\big)\right] dt
  \label{eq:regret}
\end{equation}
$R$越低表明越早锁定高浓核心区并保持足够续航；对数尺度下$R=0.1$和$0.3$分别对应报告浓度比真实峰值低约20\%和约一半。

\subsection{问题剖析}

内部计算与外部采样共享有限电池与时间窗口，存在三重矛盾。第一，增加计算的收益只能在内部想象海洋中估算，但规划器在搜索样本上的自评得分存在正向偏差：当推演次数扩大50倍时，优化器会微调航路点以穿过搜索样本中的偶然高值格，使内部得分虚高而实际航线不再改善\cite{smith2006curse, vanhasselt2010double}，因此需要将搜索航线与评判价值的想象海洋分离。

第二，观测的信息收益取决于3天前旧图的误差分布，遥感大数据虽能标定这一统计规律，却难以靠数值外推直接消除小尺度误差。正如第5.2节所示，深度学习时空预测无法从旧图中恢复数日后的小尺度峰值，航行器必须现场采样，并利用历史数据标定的误差方差与相关尺度构建先验想象海洋，随采样同化收缩不确定性。

第三，最优用时策略随底图不确定性、处理器速度与芯片功耗而变化，但任务间天然环境波动远大于策略间平均差异。在慢计算机上仅靠后台规划易使航行器在窗口中部局部绕圈，而在快计算机上开启高功耗芯片的额外能耗换取的航线改善十分有限。因此，无论是在下水前利用留出海洋开展全任务预演，还是在航行中利用留出海洋评估单步收益，核心均在于不依赖历史巡测任务而稳健剔除劣质策略。

===== FILE: sections/method.tex =====
\section{方法}

本文利用八年卫星数据标定的留出想象海洋作为独立标尺，将航线搜索与价值评判解耦，在出发前预演或在线元推理中权衡计算与观测（图\ref{fig:overview}）。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_overview}
  \caption{基于数据标定留出想象海洋的自主水下航行器计算与观测权衡方法总览。（A）海洋大数据：利用2018至2026年东海3197天逐日$2\text{ km}$卫星叶绿素与海表温度数据切出422个赤潮窗口（开发集274个、测试集148个），标定1至3天滞后底图误差（0.125、0.176、0.210）与四季演变图谱，而550万参数的深度时空预测模型并不优于直接沿用最新底图，表明小尺度结构必须靠现场观测获取。（B）出发前：围绕3天前旧图生成48个经数据标定不确定性的想象海洋，划分为32个搜索用海洋与16个留出海洋；下水前以4个留出海洋为假想真值完整预演五种用时策略（柱状图为2025年4月4日测试任务在中等计算机上的假想遗憾，“一直走”以0.715入选），选出平均假想遗憾最低的策略$s^*$投入实海。（C）任务执行：每20分钟在走、深想与停下之间行动并随时响应最浓处查询，插图显示随规划预算增加规划器自评得分持续攀升，而留出海洋评判与真实航线价值一同趋于平缓。}
  \label{fig:overview}
\end{figure}

\subsection{想象海洋与局地化集合同化}

为使内部环境集合的先验离散度匹配旧图与真实海洋的误差分布，本文从2018至2022年开发集序列中提取滞后$k$天底图的实测误差标准差$s_k$与空间相关长度$\ell$，结合同日卫星图未分辨小尺度标准差$s_{\text{sat}}$，构造合成先验标准差：
\begin{equation}
  \sigma_k = \sqrt{s_k^2 + s_{\text{sat}}^2}
  \label{eq:sigma_k}
\end{equation}
在$k=3$天主设置下，$s_3 = 0.210$、$s_{\text{sat}} = 0.15$，故$\sigma_3 \approx 0.26$；在“当天卫星图”真值下$s_{\text{sat}} = 0$、$\sigma_3 = 0.210$。航行器下水前围绕3天前旧图$c_{\text{map}}(\mathbf{x})$生成$N=48$个想象海洋：
\begin{equation}
  c^{(i)}(\mathbf{x}) = c_{\text{map}}(\mathbf{x}) + \sigma_k\, z^{(i)}(\mathbf{x}), \quad i = 1, 2, \dots, 48
  \label{eq:prior_ensemble}
\end{equation}
其中$z^{(i)}(\mathbf{x})$为相互独立的零均值单位方差高斯随机场，采用平方指数相关函数$C(\mathbf{x}, \mathbf{x}') = \exp\!\big(-\|\mathbf{x}-\mathbf{x}'\|_2^2 / (2\ell^2)\big)$，相关长度取开发集标定值$\ell = 5$格（$10\text{ km}$）。

每当荧光计在$\mathbf{x}_{\text{obs}}$采集样本$y$（观测方差$\sigma_{\varepsilon}^2 = 0.1^2$），航行器采用乘以半宽$2\ell = 10$格（$20\text{ km}$）五阶分段有理局地化函数$\rho\!\big(\|\mathbf{x}-\mathbf{x}_{\text{obs}}\|_2 / (2\ell)\big)$\cite{gaspari1999correlation}的序列集合调整卡尔曼滤波\cite{anderson2001eakf}，由同化前观测点集合均值$\bar{c}(\mathbf{x}_{\text{obs}})$与方差$\sigma_{\text{ens}}^2(\mathbf{x}_{\text{obs}})$计算后验均值$\bar{c}^a(\mathbf{x}_{\text{obs}})$、成员$c^{a,(i)}(\mathbf{x}_{\text{obs}})$及增量$\Delta y^{(i)} = c^{a,(i)}(\mathbf{x}_{\text{obs}}) - c^{(i)}(\mathbf{x}_{\text{obs}})$，并同步更新全窗可航行网格$\mathbf{x}$：
\begin{equation}
  \bar{c}^a(\mathbf{x}_{\text{obs}}) = \frac{\sigma_{\varepsilon}^2\,\bar{c}(\mathbf{x}_{\text{obs}}) + \sigma_{\text{ens}}^2(\mathbf{x}_{\text{obs}})\,y}{\sigma_{\varepsilon}^2 + \sigma_{\text{ens}}^2(\mathbf{x}_{\text{obs}})}, \quad
  c^{a,(i)}(\mathbf{x}_{\text{obs}}) = \bar{c}^a(\mathbf{x}_{\text{obs}}) + \sqrt{\frac{\sigma_{\varepsilon}^2}{\sigma_{\varepsilon}^2 + \sigma_{\text{ens}}^2(\mathbf{x}_{\text{obs}})}}\,\Big(c^{(i)}(\mathbf{x}_{\text{obs}}) - \bar{c}(\mathbf{x}_{\text{obs}})\Big)
  \label{eq:eakf_obs}
\end{equation}
\begin{equation}
  c^{a,(i)}(\mathbf{x}) = c^{(i)}(\mathbf{x}) + \rho\!\left(\frac{\|\mathbf{x}-\mathbf{x}_{\text{obs}}\|_2}{2\ell}\right)\frac{\operatorname{Cov}\!\big(c(\mathbf{x}), c(\mathbf{x}_{\text{obs}})\big)}{\sigma_{\text{ens}}^2(\mathbf{x}_{\text{obs}})}\,\Delta y^{(i)}
  \label{eq:eakf_state}
\end{equation}

\subsection{航线搜索与价值评判分离}

为消除航线优化对有限想象海洋的过拟合偏差，需要将供规划器搜索航线的样本集合与用于评判价值的样本集合分离开来。若将全部48个想象海洋一并输入规划器并直接以搜索最高分代表预期收益\cite{russell1991right, lin2015metareasoning}，在推演预算扩大数十倍时，规划器会微调航路点以迎合这批样本中偶然重叠的随机高值斑块，产生优化器诅咒\cite{smith2006curse}。为此，本文借鉴双估计思想\cite{vanhasselt2010double}，在出发前将48个想象海洋固定划分为互不相交的搜索用海洋$\mathcal{I}_{\text{search}} = \{1, \dots, 32\}$与留出海洋$\mathcal{I}_{\text{hold}} = \{33, \dots, 48\}$（图\ref{fig:overview}B）。两个子集在航行中按式\eqref{eq:eakf_obs}与式\eqref{eq:eakf_state}同步同化更新，蕴含相同的先验统计与观测信息，但规划器仅在$\mathcal{I}_{\text{search}}$上搜索航线，而$\mathcal{I}_{\text{hold}}$对搜索过程不可见。

每个20分钟周期内，规划器搜索以周期末预计位置$\mathbf{x}_0$为起点、依次连接两个航路点$\bm{\theta} = (\mathbf{w}_1, \mathbf{w}_2)$的折线航线。将候选航线$\bm{\theta}$在单个想象海洋$c^{(i)}$上模拟走完剩余时长$T_{\text{left}}$（或直至可用巡航电池时间$T_{\text{batt}}$耗尽）称为一次推演。记剩余时刻$\tau \in [0, T_{\text{left}}]$沿折线已遇最高浓度与当前已访最高估计浓度$\max_{\mathbf{x}\in\mathcal{V}(t)} \bar{c}_t(\mathbf{x})$中的较大值为$m_i(\tau; \bm{\theta})$（$\tau > T_{\text{batt}}$后保持耗尽时刻值不变），则航线在第$i$个想象海洋上的推演价值定义为：
\begin{equation}
  V_i(\bm{\theta}) = \frac{1}{T_{\text{left}}}\int_0^{T_{\text{left}}} m_i(\tau; \bm{\theta})\, d\tau
  \label{eq:route_value}
\end{equation}
式\eqref{eq:route_value}与式\eqref{eq:regret}的时间平均遗憾目标对应，可同时惩罚路线绕远造成的到达延迟与电量透支造成的提前停机。规划器采用跨周期热启动的交叉熵方法\cite{deboer2005cem}在$\mathcal{I}_{\text{search}}$上迭代优化航路点分布，选出搜索集平均价值最高的航线$\bm{\theta}^*$，其无偏价值评判$\hat{V}_{\text{hold}}(\bm{\theta}^*)$则在未参与搜索的16个留出海洋$\mathcal{I}_{\text{hold}}$上计算：
\begin{equation}
  \bm{\theta}^* = \arg\max_{\bm{\theta}} \frac{1}{|\mathcal{I}_{\text{search}}|}\sum_{i\in\mathcal{I}_{\text{search}}} V_i(\bm{\theta}), \quad
  \hat{V}_{\text{hold}}(\bm{\theta}^*) = \frac{1}{|\mathcal{I}_{\text{hold}}|}\sum_{j\in\mathcal{I}_{\text{hold}}} V_j(\bm{\theta}^*)
  \label{eq:split_eval}
\end{equation}

\subsection{出发前全任务预演}

由于开启高功耗芯片的电量消耗与停下复测的航程损失会在24小时内累积作用，本文构造五种候选时间分配策略，并在下水前以留出海洋为假想真值开展全任务预演：
\begin{enumerate}
  \item \textbf{一直走：}全程巡航采样，仅用低功耗处理器后台规划。
  \item \textbf{一直深想：}全程巡航采样，每周期均开启高功耗芯片将推演次数提升至50倍。
  \item \textbf{三段深想一段：}全程巡航采样，每3个周期中开启1个周期高功耗芯片深想、其余2个周期后台规划。
  \item \textbf{三段停下深想一段：}每3个周期中有1个周期关停推进器原位复测5次并开启高功耗芯片深想，其余2个周期巡航并后台规划。
  \item \textbf{三段停下复测一段：}每3个周期中有1个周期关停推进器原位复测5次且仅用后台规划，其余2个周期巡航并后台规划。
\end{enumerate}

\begin{algorithm}[htbp]
  \caption{基于数据标定留出想象海洋的出发前全任务预演}
  \label{alg:rehearsal}
  \begin{algorithmic}[1]
    \Require 滞后$k$天旧卫星图$c_{\text{map}}(\mathbf{x})$，数据标定先验标准差$\sigma_k$与相关长度$\ell$，入水起点$\mathbf{x}_{\text{start}}$，机载低功耗处理器速度$v_{\text{cpu}}$、高功耗芯片倍率$50\times$与功率$P_{\text{gpu}}$，电池容量$E_{\text{batt}}=1\text{ kWh}$，候选策略集合$\mathcal{S}=\{\text{一直走}, \text{一直深想}, \text{三段深想一段}, \text{三段停下深想一段}, \text{三段停下复测一段}\}$
    \Ensure 选定的本次任务执行策略$s^*$
    \State 围绕$c_{\text{map}}(\mathbf{x})$按式\eqref{eq:prior_ensemble}生成48个想象海洋，划分为搜索用海洋$\mathcal{I}_{\text{search}}=\{1,\dots,32\}$与留出海洋$\mathcal{I}_{\text{hold}}=\{33,\dots,48\}$
    \State 从留出海洋$\mathcal{I}_{\text{hold}}$中抽取$M=4$个样本$\{c_{\text{truth}}^{(j)}\}_{j=1}^4$作为假想真值，并固定观测噪声随机数种子
    \For{每种候选策略 $s \in \mathcal{S}$}
      \For{$j = 1, 2, \dots, M$}
        \State 初始化航行器内部48个想象海洋、位置$\mathbf{x} \leftarrow \mathbf{x}_{\text{start}}$、剩余电量$E \leftarrow E_{\text{batt}}$及已访集合$\mathcal{V} \leftarrow \{\mathbf{x}_{\text{start}}\}$
        \For{决策周期 $t_{\text{step}} = 1, 2, \dots, 72$（每周期$\Delta t = 20\text{ min}$）}
          \State 若$E > 0$，按策略$s$确定本周期机体动作（走或停下）与规划模式（后台规划或开启高功耗芯片深想）
          \State 在搜索用海洋$\mathcal{I}_{\text{search}}$上按对应推演预算（$v_{\text{cpu}}\Delta t$或$50 v_{\text{cpu}}\Delta t$）运行交叉熵方法更新航线$\bm{\theta}^*$
          \State 在假想真值$c_{\text{truth}}^{(j)}$上执行机体动作并按式\eqref{eq:obs}采集荧光计样本，用式\eqref{eq:eakf_obs}与式\eqref{eq:eakf_state}更新内部海洋集合并扣除本周期耗电量
          \State 按式\eqref{eq:answer}记录已访集合$\mathcal{V}$中当前内部均值最高的位置$\hat{\mathbf{x}}(t_{\text{step}})$
        \EndFor
        \State 在假想真值$c_{\text{truth}}^{(j)}$上按式\eqref{eq:regret}计算24小时假想时间平均遗憾$R_{s,j}$
      \EndFor
      \State 计算策略$s$在4个假想真值上的平均假想遗憾$\bar{R}_s = \frac{1}{4}\sum_{j=1}^4 R_{s,j}$
    \EndFor
    \State \Return $s^* = \arg\min_{s\in\mathcal{S}} \bar{R}_s$
  \end{algorithmic}
\end{algorithm}

下水前（算法\ref{alg:rehearsal}），母船或岸基计算机从$\mathcal{I}_{\text{hold}}$中取$M=4$个样本作为假想真值$c_{\text{truth}}^{(j)}$，对每种候选策略$s$按该航行器自身的交叉熵规划器、处理器速度、芯片功耗与电池模型完整模拟24小时巡测过程（五种策略在同一假想真值上共享相同的初始想象海洋与荧光计观测噪声序列），按式\eqref{eq:regret}记录假想遗憾$R_{s,j}$并选出均值最低者写入航行器执行：
\begin{equation}
  s^* = \arg\min_{s\in\mathcal{S}} \frac{1}{4}\sum_{j=1}^4 R_{s,j}
  \label{eq:rehearsal_select}
\end{equation}
预演以假想真值上的结果$R_{s,j}$而非规划器内部自评得分比较策略，故绕开了规划器自评泡沫。慢计算机配置下单次任务预演共约190万次推演（机载高功耗芯片自算需约125小时），而在普通台式计算机单核上，慢、中、快计算机配置的预演耗时分别为$4.6\text{ s}$、$7.8\text{ s}$与约$25\text{ s}$，满足出航前装订需求。

\subsection{在线单步元推理的留出估值}

若不采用出发前预演而在航行途中逐周期在线决策，经典“单步元推理”\cite{russell1991right}在每周期先运行后台规划得基准航线$\bm{\theta}_{\text{base}}$，再直接在搜索用海洋$\mathcal{I}_{\text{search}}$上估计开启高功耗芯片深想（航线$\bm{\theta}_{\text{deep}}$，扣除额外耗电缩短续航的边际代价）的收益以及原位采样5次的预后验信息收益，并直接取估计价值最高者。由于搜索与估值共用$\mathcal{I}_{\text{search}}$且对微弱样本涨落敏感，控制器极易过度深想并频繁停船。

本文提出的“单步元推理（留出估值）”与经典单步元推理有两处明确区别：第一，候选航线$\bm{\theta}_{\text{base}}$与$\bm{\theta}_{\text{deep}}$虽仍由交叉熵规划器在32个搜索用海洋$\mathcal{I}_{\text{search}}$上搜索产生，但开启高功耗芯片的计算净收益与原位复测5次的预后验信息收益均改在16个留出海洋$\mathcal{I}_{\text{hold}}$上评判；第二，经典方法直接选取估计价值的普通最大值，而留出估值变体以“走且后台规划”为默认动作，仅当另一周期用时方式在留出海洋上的配对差值均值超出其两倍标准误时才离开默认动作切换为深想或停下，从而同时抑制搜索过拟合与有限样本噪声引起的误切换。

===== FILE: sections/experiments.tex =====
\section{实验}

\subsection{实验设置}

实验基于东海274个开发集窗口（2018至2022年，用于标定底图误差、绘制相图及训练历史基线）与148个测试集窗口（2023至2026年，用于主实验与消融检验）开展，参数汇总于表\ref{tab:settings}。测试涵盖慢计算机（5次/分，$+20\text{ W}$）、中等计算机（20次/分，$+20\text{ W}$）、快计算机（100次/分，$+20\text{ W}$）与省电加速器（20次/分，$+5\text{ W}$）四种硬件，以及“当天卫星图 + 小尺度变化”（主设置，$s_{\text{sat}}=0.15$）和“当天卫星图”（$s_{\text{sat}}=0$）两种真值模型。同一任务上所有控制器共享相同的真实海洋、起点与传感器噪声序列，且随机种子按任务固定（慢计算机独立重跑全部148个测试任务预演所得遗憾与首次运行逐任务一致）；配对差值的95\%置信区间由按赤潮周整组重抽样的自助法给出。

\begin{table}[htbp]
  \centering
  \caption{东海赤潮应急巡测实验的核心参数与评价设置。}
  \label{tab:settings}
  \input{tables/settings.tex}
\end{table}

我们将“出发前预演（本文）”与五类控制方式对比：（1）五种固定策略及“五种策略随机选”、“三种不停策略随机选”；（2）需要历史任务的方法，包括“调好的固定策略”（在120个开发集任务上为每种硬件和真值模型选出平均遗憾最低的固定策略）与“按历史任务学习的选择器”（参照学习型元推理\cite{magnino2026metareasoning}，在同批开发集任务上用旧图最大值、中位数、极差、标准差、起点至旧图峰值距离、可航行占比、起点旧图浓度及近峰值网格占比共8项特征训练梯度提升回归预测各策略遗憾并择优）；（3）在线元推理，包括经典“单步元推理”\cite{russell1991right}与“单步元推理（留出估值）”；（4）不含多步航线规划的巡测规则（全程巡航并用相同局地化集合滤波更新地图），包括间距$16\text{ km}$平行扫测的“割草机式全覆盖”\cite{galceran2013coverage}、“贪心：驶向估计最浓处”（驶向集合均值最高未访格）、“上置信界采样”（均值加2倍标准差最高未访格）\cite{srinivas2012gpucb}与“汤普森采样”（每周期随机抽取一个想象海洋并驶向其最浓未访格）\cite{russo2018thompson}；（5）事后挑出最佳固定策略的“每次任务事后最优（参考）”。

\subsection{卫星大数据的作用与局限}

八年卫星叶绿素大数据能够标定滞后底图在不同季节与滞后天数下的误差分布，但深度时空预测模型无法改善1至3天的底图外推精度，小尺度结构必须依靠现场采样获取（图\ref{fig:data}）。全海域3197天数据上相隔3天的对数叶绿素变化标准差在春季赤潮高发期最高（中位数0.127），夏秋季次之，冬季最低（0.081），夏季浙闽沿岸与长江冲淡水锋面形成0.25至0.3的强变率带（图\ref{fig:data}a至图\ref{fig:data}d）。在274个开发集窗口内，滞后1、2、3天旧图的误差标准差依次增至$0.125$、$0.176$与$0.210$（均值偏差$+0.016$、$+0.032$、$+0.045$，相关尺度约5格即$10\text{ km}$），而同日卫星图与现场海水还存在约0.15的对数差异\cite{ye2021cocts}（图\ref{fig:data}e）。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_data}
  \caption{八年东海卫星叶绿素大数据提供的先验误差标定及其外推预测边界。（a）至（d）2018至2026年全部3197天对数叶绿素3天变化标准差的四季空间分布（中位数春季0.127、夏季0.107、秋季0.103、冬季0.081），春季子图标出了274个开发集窗口与148个测试集窗口的位置。（e）开发集窗口内滞后1、2、3天旧卫星图的误差标准差（0.125、0.176、0.210）及同日卫星图相对于现场实测水体的约0.15偏差。（f）2023至2026年测试集上深度时空预测模型与直接沿用最新卫星图在提前1、2、3天预报上的均方根误差对比（0.1229对0.1226、0.1439对0.1439、0.1487对0.1474）。数据能够可靠标定旧图的不确定性幅值，但无法替代现场观测。}
  \label{fig:data}
\end{figure}

为检验出发前能否用深度学习外推旧图以减小滞后误差，我们训练了550万参数的联合嵌入预测架构模型\cite{assran2025vjepa2}，以过去3天叶绿素和海表温度异常场为输入（2018至2021年3至6月训练，2022年验证集误差仅比沿用最新底图低1.4\%）。在2023至2026年测试集上，该模型提前1、2、3天预报的均方根误差（集合离散度与误差之比$0.70\text{--}0.93$）与直接沿用最新可用卫星图的持久性基线持平（图\ref{fig:data}f）。这确立了海洋大数据在本问题中的角色：数值外推无法替代现场采样，但多年遥感统计能够为生成想象海洋提供准确的先验不确定性标尺。

\subsection{规划自评的偏差}

随着单次决策推演预算增加，规划器在搜索用海洋上的自评得分因优化器诅咒持续虚高，而在留出海洋上评判则能准确反映真实航线价值的饱和过程（图\ref{fig:curse}）。在80个开发集窗口（每窗口3个种子，3天前旧图，任务前8小时，主真值设置）上，当推演次数从64次增至2000次再扩至200,000次时，真实航线价值在2000次后即进入平台期并收敛至$0.803$，而32个搜索用海洋上的自评得分却一路升至$0.917$，在最大预算下高估达$0.114$；同一批航线在16个留出海洋上的评判均值在全部预算下与真实价值之差均不超过$0.005$（图\ref{fig:curse}a、图\ref{fig:curse}b）。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_curse}
  \caption{推演预算从64次扩展至200,000次时规划器自评得分的乐观偏差与留出海洋的无偏评判（80个开发集窗口$\times 3$个种子，3天前卫星图，任务前8小时）。（a）所选航线的时间平均最佳对数叶绿素价值：搜索用海洋上的自评得分从0.762持续升至0.917，而真实航线价值（0.749升至0.803）与留出海洋评判（0.745升至0.802）在约2000次推演后一同趋于饱和。（b）估计价值减去真实价值的偏差曲线：使用数据标定不确定性时留出评判偏差保持在0.005以内，将不确定性设小一半或放大至1.5倍虽产生$-0.06$与$+0.07$的整体平移，但仍能准确捕捉增加算力的相对增益。}
  \label{fig:curse}
\end{figure}

当人为将先验标准差$\sigma_3$减半或放大至1.5倍时，留出评判虽产生整体平移，但推演预算从64次增至200,000次时留出海洋估计的价值增量（$+0.059$与$+0.054$）仍与真实价值增量（$+0.054$与$+0.047$）吻合（图\ref{fig:curse}b）。这表明将搜索用海洋与留出海洋分离能够切断优化器对样本噪声的迎合，为衡量计算价值提供可靠的独立标尺。

\subsection{主要结果}

在148个测试任务上，出发前预演在四种硬件与两种真值模型下无需历史任务即达到“调好的固定策略”与“按历史任务学习的选择器”水平，并优于经典“单步元推理”以及除慢计算机主设置下贪心规则（持平）外的全部无规划巡测规则（图\ref{fig:main}，表\ref{tab:main}）。在主设置下，预演在四种硬件上的时间平均遗憾为$0.265\text{--}0.276$，与“调好的固定策略”的配对差值为$-0.003$至$+0.007$（慢计算机$[-0.000, +0.014]$、中等计算机$[-0.009, +0.003]$），与“按历史任务学习的选择器”差值为$-0.004$至$+0.000$，全部95\%置信区间均包含0。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_main}
  \caption{148个测试任务上各对比控制方式减去“出发前预演（本文）”的时间平均遗憾配对差值及95\%置信区间（正值表示差于本文方法）。四列对应慢计算机、中等计算机、快计算机与省电加速器，实心圆点为“当天卫星图 + 小尺度变化”主设置，空心圆点为“当天卫星图”真值设置。出发前预演在所有硬件与两种真值模型下均匹配需要历史任务的两种方法，并显著优于经典单步元推理及所有巡测规则（仅慢计算机主设置下与贪心规则持平）。}
  \label{fig:main}
\end{figure}

\begin{table}[htbp]
  \centering
  \caption{2023至2026年148个测试任务上四种机载硬件与两种真值模型下各控制方式的时间平均遗憾（越低越好，每列最优可运行控制器加粗，本文方法行加底纹）。}
  \label{tab:main}
  \small\resizebox{\linewidth}{!}{\input{tables/main_table.tex}}
  \par\vspace{2pt}\footnotesize 注：$^a$ 调好的固定策略在主设置下依次为三段深想一段、三段深想一段、一直走、一直深想，在“当天卫星图”真值下依次为三段深想一段、一直走、三段深想一段、三段深想一段。
\end{table}

相比之下，主设置下预演比经典“单步元推理”降低遗憾$0.011$（$[-0.019, -0.002]$）、$0.022$（$[-0.030, -0.013]$）、$0.013$（$[-0.020, -0.007]$）与$0.012$（$[-0.019, -0.004]$），置信区间全部低于0。对四种无规划巡测规则，预演除在慢计算机上与贪心规则差值为$-0.009$（$[-0.022, +0.004]$）外，在其余三种硬件上比贪心规则低$0.017\text{--}0.020$，并在所有硬件上比上置信界采样、汤普森采样和割草机式全覆盖分别低$0.023\text{--}0.034$、$0.056\text{--}0.067$和$0.148\text{--}0.159$（区间全部低于0）。

在“当天卫星图”真值下，因无亚网格随机场，各控制器绝对遗憾整体下降，但相对格局一致（表\ref{tab:main}右半部）：预演（$0.191\text{--}0.197$）与调好策略及学习型选择器的差值在$-0.005$至$+0.003$之间（区间均含0），比单步元推理低$0.006\text{--}0.010$，比全部四种巡测规则低$0.010\text{--}0.139$（区间全部低于0）；较优停下策略在两种真值下均比最佳不停策略差$0.054\text{--}0.062$。此外，两种真值下148个测试任务间的遗憾标准差达约$0.13$与$0.11\text{--}0.12$，而三种不停策略间的平均差距（除慢计算机外）不超过$0.01$。

\subsection{机理分析}

经典单步元推理失利源于在80\%至97\%的周期内开启高功耗芯片并在33\%至34\%的周期内停下复测，而“单步元推理（留出估值）”将深想比例压低至30\%至44\%、停下比例降至15\%至18\%（预演深想占26\%至54\%、停下仅$0.5\%\text{--}1.8\%$，图\ref{fig:mech}a、图\ref{fig:mech}b），使四种硬件上的遗憾降至$0.278$、$0.270$、$0.270$与$0.267$（比经典单步元推理低$0.009$、$0.017$、$0.012$与$0.010$，与预演之差在$0.005$以内且区间含0）。为分离留出估值变体中两项改动各自的作用，我们在慢计算机与中等计算机（相同148个任务与种子）上分别单独运行“仅留出估值（直接取最大）”与“仅两倍标准误规则（仍在搜索用海洋上估值）”：仅采用留出估值时，慢、中计算机深想占比即从\TBD{经典单步深想占比}降至\TBD{仅留出估值深想占比}（慢计算机从约80\%降至约30\%），但停下占比仍维持在\TBD{仅留出估值停下占比}（约三分之一），遗憾为\TBD{仅留出估值遗憾}；仅采用两倍标准误规则时，深想占比仍居高不下（\TBD{仅两倍标准误深想占比}，慢计算机约80\%），而停下占比降至\TBD{仅两倍标准误停下占比}，遗憾为\TBD{仅两倍标准误遗憾}；两项改动结合方才取得最低遗憾（$0.278$与$0.270$）。这说明过度深想源于在搜索用海洋上评估计算收益（规划器自身拟合偏差），而过多停船源于对微小噪声差值的直接响应，留出估值变体同时消除了这两项偏差。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_mech}
  \caption{在线元推理过度规划的成因与出发前预演的硬件自适应机制（主真值设置，148个测试任务）。（a）高功耗芯片开启周期占比与（b）停下复测周期占比：经典单步元推理在80\%至97\%的周期内开启高功耗芯片并在33\%至34\%的周期内停下，而单步元推理（留出估值）与出发前预演大幅削减了无效深想与停船。（c）出发前预演在四种硬件上选出各候选策略的任务占比：随基础算力提升，“一直走”占比从1\%升至30\%再升至47\%，而在省电加速器上“一直深想”占比从25\%升至43\%。}
  \label{fig:mech}
\end{figure}

出发前预演选出的策略比例随硬件算力与功耗自适应调整（图\ref{fig:mech}c）：在“一直走”比调好策略差$+0.104$的慢计算机上，预演极少选“一直走”，随基础算力升至中等和快计算机，“一直走”占比阶梯式上升，而在同为20次/分但芯片仅$+5\text{ W}$的省电加速器上，“一直深想”占比显著增加。预演的优势来自剔除当前硬件下的劣质选项（各硬件上的停下策略及慢计算机上的“一直走”），故显著优于“五种策略随机选”（$0.292\text{--}0.331$）和慢计算机上的“三种不停策略随机选”（$0.306$）；而在真实差距不超过$0.004$的其余三种硬件不停策略间，其单任务选择接近随机，与“预演（以搜索过的海洋为真值）”选出同一策略的比例为37\%至41\%，但两者平均遗憾仅差$-0.004$至$+0.004$（区间含0），因为预演以假想真值上的最终任务遗憾而非规划器自评得分比较策略。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_example}
  \caption{一次典型测试任务（2023年4月15日，慢计算机）中“一直走”与“三段深想一段”的航迹及实时遗憾对比。（a）航行器出发时携带的3天前卫星图及东侧边缘入水起点（白色三角形）。（b）真实海洋叶绿素分布（西南角五角星为真实最浓处）以及“一直走”（蓝线）与“三段深想一段”（橙线，加粗段为开启高功耗芯片深想）的24小时航迹。（c）24小时内报告位置的实时遗憾曲线：“一直走”因搜索不足在窗口中部绕圈，遗憾停留在0.4附近（均值0.43），“三段深想一段”横穿窗口并在约19小时后抵达真实最浓处（均值降至0.31）。}
  \label{fig:example}
\end{figure}

在2023年4月15日测试任务（慢计算机，按日期顺序首个两策略差距超0.1的任务，图\ref{fig:example}）中，航行器从东侧入水，真实最浓处位于西南角。慢计算机上“一直走”每周期仅后台推演100次，航行至窗口中部次高值区后局部徘徊，时间平均遗憾为$0.43$；而“三段深想一段”在深想周期内执行5000次推演，规划出的航线横穿窗口指向西南角，于约19小时后抵达真实最浓处，将平均遗憾降至$0.31$。

\subsection{消融实验}

在慢计算机与中等计算机上的消融实验（图\ref{fig:ablation}）首先检验了假想真值的数量与来源。将假想真值从4个减为1个或2个时，两台计算机上的遗憾恶化$+0.006$至$+0.013$；增至8个仅在慢计算机上微降$-0.007$（$[-0.012, -0.001]$）而中等计算机变化$+0.003$，故4个真值是兼顾精度与耗时的合理配置。将假想真值改从搜索用海洋中抽取时，遗憾变化仅为$-0.004$与$+0.003$（区间含0），印证以假想真值上的任务结果评判策略可规避自评过拟合。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_ablation}
  \caption{慢计算机与中等计算机（主真值设置，148个测试任务）上的消融实验结果（各变体减去完整“出发前预演（本文）”的时间平均遗憾配对差值及95\%置信区间）。减少假想真值数量、将先验不确定性错误放大至2倍或取消预演改为随机选择均导致性能劣化，而在任务尺度预演、在线周期级留出估值与需要历史任务的方法之间表现相当。}
  \label{fig:ablation}
\end{figure}

第二组消融检验先验不确定性标定与评估尺度。将先验标准差减半时遗憾变化不大（$+0.002$与$+0.004$），但放大至标定值的2倍时，慢、中计算机遗憾恶化$+0.011$（$[+0.001, +0.020]$）与$+0.020$（$[+0.011, +0.030]$），此时过大噪声使所有固定策略退化（中等计算机不停策略恶化至$0.275\text{--}0.283$），预演（$0.286$）亦不再匹配最佳固定策略（$0.275$）。将全任务预演替换为在线“单步元推理（留出估值）”时差值仅为$+0.002$与$+0.005$（区间含0），说明留出评判准则在离线任务级与在线周期级均有效，而取消预演改为五种策略随机选则损失$+0.055$与$+0.028$。

\subsection{适用范围}

在低功耗处理器速度与真实海洋偏离卫星图程度构成的二维相图（图\ref{fig:phase}）上，深想仅在基础算力低于航线价值饱和阈值时明显获益，而停下复测在全部格点均造成损失。在5次/分处理器上（后台每周期仅推演100次，远低于约2000次的饱和点），当底图偏离度为0.05、0.15与0.30时，较优深想策略比“一直走”分别降低遗憾$0.086$、$0.109$与$0.138$，底图越不准深想收益越大；10次/分上仅偏离0.15一格有微弱收益（$-0.017$），从20次/分起均无明显收益。在偏离度为0的第四行（当天卫星图本身为真值），5次/分计算机上深想比“一直走”降低遗憾$0.080$（$[-0.119, -0.043]$），10次/分及以上无明显收益，而该行每一格中较优停下策略均比最佳不停策略差$0.061\text{--}0.076$。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_phase}
  \caption{低功耗处理器速度（每分钟5至200次推演）与真实海洋偏离卫星图程度（0、0.05、0.15、0.30）二维网格上的策略收益相图（每格60个开发集任务）。（a）最佳深想策略减去“一直走”的时间平均遗憾差值（加框格点表示95\%置信区间低于0，即深想显著有益）：深想仅在基础算力过慢（5次/分）时显著获益，且底图偏离越大收益越强。（b）较好停下策略减去最佳不停策略的遗憾差值：所有格点差值均为显著正值（$+0.061$至$+0.118$），表明停下原位复测在任何算力与底图误差下均得不偿失。}
  \label{fig:phase}
\end{figure}

跨越全部24个相图格点，较优停下策略始终比最佳不停策略高出$0.061\text{--}0.118$的遗憾（图\ref{fig:phase}b）：原位复测5次虽将单点测量误差从$0.1$降至约$0.045$，但巡测瓶颈在于未访水域约$0.26$的先验不确定性，且停船三分之一时间推迟了到达高浓水体的时刻，增大了时间平均遗憾。此外，当改用滞后1天的较新卫星图（$s_1=0.125$，主设置）时，慢计算机上调好策略为“一直深想”（$0.250$），预演取得$0.251$（差值$+0.001$，$[-0.005, +0.011]$），优于单步元推理（$0.260$，差值$-0.009$，$[-0.018, +0.001]$）；中等计算机上调好策略为“一直走”（$0.250$），预演取得$0.243$，比调好策略低$0.007$（$[-0.014, -0.002]$）且比单步元推理（$0.260$）低$0.017$（$[-0.022, -0.013]$），这是因为“一直走”在开发年份最优，而在测试年份上“三段深想一段”（$0.239$）反而是最佳固定策略。

\subsection{局限性}

本研究仍存在若干简化。首先，实验以任务当天卫星叶绿素图（叠加或不叠加标定小尺度场）作为真实海洋而非现场走航剖面，二维随水漂移参考系忽略了水平流剪切与藻类昼夜垂直迁移，双航路点规划器也是对三维流场路径规划的简化替代。其次，预演仅在下水前执行一次而未在任务中途重跑，且4个假想真值主要使策略适配机载硬件特性，尚不足以在平均差距微小的几种不停策略间针对单次任务做出精细区分（主设置下距“每次任务事后最优（参考）”仍差$0.022\text{--}0.027$）。最后，预演中的假想遗憾比真实海洋遗憾整体偏高约$0.05\text{--}0.07$，但该偏移对各策略一致，不改变相对排序。

===== FILE: sections/conclusion.tex =====
\section{结论}

多年累积的卫星海洋遥感大数据不仅能为自主水下航行器提供先验底图，更能生成一套经误差标定且独立于搜索过程的留出想象海洋，作为衡量机载计算价值的客观标尺。本文围绕东海赤潮应急巡测中走、深想与停下复测的资源分配问题，将48个随采样局地化集合同化更新的想象海洋划分为32个搜索用海洋与16个留出海洋，提出了出发前全任务预演方法及结合留出估值与两倍标准误判据的在线单步元推理方法。在3197天东海卫星数据构建的422个赤潮窗口、四种机载硬件及两种真值模型上的实验表明：留出评判在跨三个半数量级的推演预算下与真实航线价值偏差不超过0.005；开启高功耗芯片深想仅在基础算力过慢时有益，而停下复测始终得不偿失；出发前预演与在线留出估值无需历史任务即达到依赖历史任务方法的水平，并优于经典单步元推理以及除慢计算机主设置下贪心规则外的全部巡测规则。未来工作将把该方法拓展至三维斜压海流场与多航行器协同赤潮巡测研究。

===== FILE: sections/appendix.tex =====
\section{代码与数据说明}

本研究的数据预处理、局地化集合调整卡尔曼滤波、交叉熵航线规划器、联合嵌入预测架构时空模型、出发前预演与在线留出估值控制器、图表生成脚本、原始实验数据，以及作者与人工智能助手的研究讨论记录（已隐去涉及作者其他未发表工作的讨论内容）均开源于：\TBD{GitHub 仓库地址}。代码仓库中复现实验的脚本包括：用于主实验对比、开发集调参与算力相图的 \texttt{experiments/main\_eval.sh} 和 \texttt{experiments/phase.sh}，用于规划预算自评偏差实验的 \texttt{experiments/anytime\_curse.py}，用于巡测规则对比、当天卫星图真值、消融实验、1天滞后底图及单因素改动诊断的 \texttt{experiments/rev2.sh} 和 \texttt{experiments/rev2\_diag.sh}，以及用于由原始日志汇总统计置信区间与生成表格的 \texttt{experiments/main\_extra.py}、\texttt{experiments/rev2\_summary.py} 和 \texttt{experiments/rev2\_tables.py}；各脚本的具体运行命令见仓库中的 \texttt{README.md}。

实验使用的两套卫星遥感数据集均下载自美国国家海洋和大气管理局海岸观测网的公开数据服务器：
\begin{enumerate}
  \item \textbf{东海多星融合叶绿素 a 逐日数据集（2018—2026年）：}融合极轨卫星水色传感器观测并经经验正交函数缺失数据插补算法填补云区，空间分辨率为$2\text{ km}$，时间分辨率为逐日，遵循公共领域开放许可，数据集标识为 \texttt{noaacwNPPN20S3ASCIDINEOF2kmDaily}。
  \item \textbf{多尺度超分辨率海表温度逐日数据集（2018—2026年）：}由美国国家航空航天局喷气推进实验室制作（版本4.1），原始空间分辨率为$0.01^\circ$，时间分辨率为逐日，数据集标识为 \texttt{jplMURSST41}。
\end{enumerate}

\section{人工智能工具使用说明}

在本课程论文的研究与写作过程中，作者与人工智能工具的具体分工如下：
\begin{enumerate}
  \item 作者本人提出了核心研究问题，确立了研究方向与各项要求（包括第二轮修改要求：引入真实卫星遥感数据、补充基线与消融实验、采用学术期刊排版格式及提升图表质量），并对论文承担全部责任。
  \item Claude（Anthropic）完成了文献检索与核查，细化了研究选题，编写了全部代码，运行了所有数值实验，绘制了论文全部图表，并对照实验记录逐一核查了正文中的全部数值与文献引用。
  \item Gemini（Google）依据 Claude 整理的实验事实清单与写作提纲撰写了论文正文。
\end{enumerate}
