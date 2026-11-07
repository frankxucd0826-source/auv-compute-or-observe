基于您的审阅意见，以下是修订后的五个文件。

===== FILE: sections/title.tex =====
基于想象海洋出发前预演的自主水下航行器思考与行动权衡研究

===== FILE: sections/subtitle.tex =====
——以八年卫星叶绿素数据驱动的东海赤潮应急巡测为例

===== FILE: sections/abstract.tex =====
\section*{摘\quad 要}
\addcontentsline{toc}{section}{摘要}

携带卫星先验底图的自主水下航行器（AUV）在现场巡测时受机载算力、电池与作业时间制约。因卫星图存在滞后与小尺度偏差，航行器需在每个控制周期权衡：开启高功耗GPU深想、靠低功耗规划继续走并采样，或停下随水漂流复测。固定规则难以适应不同硬件，经典单步元推理则会因规划器在有限样本上的过拟合而高估计算价值。本文提出基于留出想象海洋的集合同化与出发前预演方法：利用八年东海卫星叶绿素数据标定底图误差，围绕旧图生成48个想象海洋并随采样同化更新，32个用于规划航线，16个留出用于评判；下水前由岸上计算机以4个留出海洋为假想真值，模拟五种用时策略的完整24小时任务并择优。在2018至2026年东海数据构建的422个任务窗口上的实验表明：留出评判在64至200,000次推演下与真实价值之差不超过0.005；深想仅在算力过慢时有益，停下始终不划算；在四种硬件、148个测试任务上，预演遗憾为0.265至0.276，与调好策略差异的95\%置信区间均包含0，且比单步元推理低0.011至0.022；改用留出评判的单步元推理同样消除了大部分过度规划。这表明将海洋遥感大数据转化为留出想象海洋可抑制计算自评偏差，使航行器无需历史任务调参即可适配机载算力与观测约束。

\vspace{1em}
\noindent\textbf{关键词：}海洋大数据；自主水下航行器；元推理；数据同化；赤潮巡测；计算与行动权衡

\clearpage
\section*{Abstract}
\addcontentsline{toc}{section}{Abstract}

Autonomous underwater vehicles (AUVs) carrying satellite prior maps must trade off computation against movement under onboard processor, battery, and mission-time constraints. Because satellite maps are滞后 and smooth out small-scale features, the vehicle must decide at every interval whether to activate a GPU to plan deeply, continue cruising under low-power planning, or stop propulsion to drift and resample. Fixed time-allocation rules do not generalize, while classic one-step metareasoning overestimates computation value by trusting the planner's search trace on finite ensemble members. We propose an ensemble data assimilation and pre-mission rehearsal method using held-out imagined oceans. Using eight years of satellite chlorophyll-a data over the East China Sea to calibrate stale-map uncertainty, the vehicle generates 48 imagined oceans, using 32 for route planning and 16 held-out for evaluation. Before launch, a shore computer treats 4 held-out members as synthetic truths and simulates complete 24-hour missions for five strategies under the vehicle's compute and battery constraints, selecting the strategy with the lowest mean regret. Across 422 spring bloom windows (2018--2026), held-out evaluation stays within 0.005 of true route value from 64 to 200,000 rollouts, GPU planning helps only when baseline compute is too slow, and stopping never pays. Across four hardware configurations on 148 test missions, rehearsal achieves regrets of 0.265--0.276, matching development-tuned strategies (all 95\% confidence intervals of differences include zero) and reducing regret by 0.011--0.022 relative to one-step metareasoning; evaluating computation on held-out oceans within one-step metareasoning similarly removes most over-planning. These findings show that converting historical satellite data into uncertainty-calibrated held-out imagined oceans curbs planner self-assessment bias, allowing autonomous vehicles to adapt computation to onboard hardware without prior mission tuning.

\vspace{1em}
\noindent\textbf{Keywords: }Ocean big data; Autonomous underwater vehicle; Metareasoning; Data assimilation; Harmful algal bloom survey; Thinking-acting trade-off

===== FILE: sections/body.tex =====
\section{绪论}

\subsection{现场移动观测中的思考与行动权衡}

携带先验地图的移动观测平台在未知自然环境中作业时，需在内部路线规划与外部现场采样之间分配有限的时间与能量\cite{horvitz1987reasoning, russell1991right, shen2025thinking}。野外自主平台受电池容量、计算速率与固定窗口限制\cite{xiao2020thinking, magnino2026metareasoning}。先验底图因环境演变与观测盲区，往往滞后且缺失小尺度结构\cite{fossum2019, beckers2003dineof}。若航行器仅靠低频后台规划维持航行，容易在复杂梯度中偏离目标；若频繁开启高功耗GPU开展搜索，或关停推进器原地复测，则会消耗电能或缩减探索里程\cite{cuadron2025overthinking, elboher2023formal}。因此，在算力、能量与底图误差约束下，如何权衡计算与采样的资源分配是自主移动观测的关键问题。

\subsection{东海赤潮应急巡测与卫星底图的局限}

卫星遥感数据驱动的东海有害赤潮应急巡测，是检验思考与行动权衡的典型场景\cite{fossum2019, lou2014diurnal}。根据2023年中国海洋灾害公报，我国海域全年发现赤潮46次，累计面积约1500平方千米\cite{mnr2024bulletin}。在浙江近海，晚春至初夏（Zhao et al. 2021, 2023记录为4月下旬至6月上旬）常暴发东海原甲藻赤潮，表层藻华斑块随潮汐往复漂移\cite{lou2014diurnal}。AUV进入目标海域后，需在24小时内尽早找到叶绿素浓度最高的水体并随时响应查询\cite{fossum2019, remus100}，由于作业期间几乎无法与岸站通信，航线重规划必须由机载计算机独立完成。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_overview}
  \caption{海洋大数据驱动的AUV赤潮应急巡测与用时策略选择总览。中央为东海一次测试任务的三维海洋窗口，顶面颜色表示真实叶绿素浓度；图中标示了AUV及其航迹（浅蓝色为走并由低功耗处理器后台规划，橙色为开启GPU深想）以及赤潮最浓处的浅色圆环；海面块体上方为一叠想象中的海洋，最上方两个橙色边框样本留出用于评判，其余深蓝色边框样本用于规划航线。（A）海洋大数据：2018至2026年3197天逐日2千米卫星叶绿素数据，航行器遇到的真实海洋不同于3天前的卫星图，从中切出422个赤潮季任务窗口；（B）航行器的想象：由旧图和数据标定的误差生成48个想象中的海洋，32个用来规划航线，16个留出来评判，并在出发前对五种用时策略各跑一遍预演；（C）每20分钟的选择：走、深想、停下，应急中心可随时询问最浓处位置。}
  \label{fig:overview}
\end{figure}

卫星水色遥感提供了大尺度背景场，但时间滞后与空间平滑使其无法替代现场观测\cite{beckers2003dineof, ye2021cocts}。如图\ref{fig:overview}所示，AUV出发前装入的往往是1至3天前的旧图，此时斑块已演变；此外，插值平滑了小尺度结构，卫星与现场间也存在固有偏差\cite{ye2021cocts}。AUV必须将旧卫星图及历史误差统计转化为概率化记忆，一边用机载荧光计沿途修正地图，一边合理分配计算与机动资源。

\subsection{现有控制方法的不足与本文方法}

固定规则无法兼顾不同的机载算力与功耗：在慢计算机上一直走会导致搜索不足，而在算力充裕的计算机上频繁开启GPU则耗电且不改善航线。经典单步元推理\cite{horvitz1987reasoning, russell1991right, lin2015metareasoning, sung2021quit}直接用规划器在搜索样本上的得分增量估计计算价值，当搜索预算较大时，规划器会迎合有限样本中的随机正涨落而虚报收益，且单步评估无法反映耗电对全程续航的影响\cite{cuadron2025overthinking}。基于历史表现学习策略选择器的方法，则因环境波动大（任务间遗憾标准差约0.13，而策略间平均差距不足0.01）而难以收敛。

针对上述问题，本文提出利用多年卫星数据标定底图不确定性、将航线搜索与价值评判分离，并在出发前通过完整任务预演选择策略的方法。全文工作包括三个部分：第一，利用2018至2026年3197天东海卫星数据标定底图误差，并验证深度预测模型无法改善短期外推；第二，将48个想象海洋分为32个规划用样本与16个留出评判样本，消除搜索过拟合偏差；第三，在下水前由岸上计算机以留出海洋为假想真值，模拟五种策略的完整任务，选出最优者投入执行，并检验了留出评判对抑制过度规划的作用。

\section{东海叶绿素遥感数据与底图不确定性}

\subsection{八年卫星数据集与赤潮任务窗口}

本文使用2018至2026年东海多源卫星融合叶绿素a数据集构建巡测任务。数据来源于NOAA CoastWatch ERDDAP服务器，空间分辨率2千米，时间分辨率逐日，共3197天。同时下载JPL MUR v4.1海表温度数据辅助分析\cite{chin2017mur}。除特别注明外，所有叶绿素浓度、误差与遗憾均以$\log_{10}(\text{叶绿素a浓度}/\text{mg m}^{-3})$为单位。

按统一条件从每年4月至6月的序列中切出正方形窗口：在浙江外海陆架区寻找离岸至少30千米、平滑后峰值超过$5\text{ mg/m}^3$的藻华中心，截取$80\text{ km}\times 80\text{ km}$窗口，要求可航行水域$\ge 80\%$且窗内对数叶绿素极差$\ge 0.3$。共切出422个任务窗口，2018至2022年的274个作为开发集，2023至2026年的148个作为测试集。

\subsection{底图滞后误差图谱与小尺度偏差}

利用3197天数据计算3天对数叶绿素变化标准差，可见夏季空间差异显著，在浙闽沿岸与长江冲淡水锋面处可达0.25至0.3（图\ref{fig:atlas}）。在开发集窗口内，滞后$k=1, 2, 3$天的底图误差标准差分别为$s_1=0.125$、$s_2=0.176$与$s_3=0.210$，空间相关尺度约10千米。仿真环境在当日卫星图上叠加标准差$s_{\text{sat}}=0.15$、空间相关尺度6千米的高斯随机场生成真实海洋\cite{ye2021cocts}。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_atlas}
  \caption{东海海域全部3197天对数叶绿素3天变化标准差的四季分布图。春季子图中的圆点为切出的赤潮任务窗口位置，蓝色为2018至2022年开发集，绿色为2023至2026年测试集。}
  \label{fig:atlas}
\end{figure}

\subsection{时空预测模型的检验}

使用联合嵌入预测架构模型\cite{assran2025vjepa2}，输入过去3天的叶绿素与温度场，在测试集上预测未来1至3天的缺测填补图，其均方根误差与直接沿用最新底图的基线（0.123, 0.144, 0.147）无显著差异，说明日均卫星图难以通过时间外推恢复小尺度信息。

\section{随水漂移参考系下的采样与决策模型}

\subsection{随水漂移参考系与评价指标}

AUV在随表层水体漂移的参考系下作业。任务期间，AUV根据已访网格集合$\mathcal{V}(t)$中的内部均值最高位置回答指挥中心查询：
\begin{equation}
  \hat{\mathbf{x}}(t) = \arg\max_{\mathbf{x}\in\mathcal{V}(t)} \bar{c}_t(\mathbf{x})
\end{equation}
评价指标为24小时时间平均遗憾$R$（越低越好）：
\begin{equation}
  R = \frac{1}{T}\int_0^T \left[\max_{\mathbf{x}} c(\mathbf{x}) - c\big(\hat{\mathbf{x}}(t)\big)\right] dt
\end{equation}

\subsection{航行器功耗模型与二十分钟决策周期}

航行器参数参照REMUS 100型AUV\cite{remus100}及Jetson Orin NX模块\cite{jetsonorinnx}。巡航总功率45 W（推进30 W，基础15 W），GPU模块深想额外耗电（+20 W或+5 W）。每20分钟决策一次，期间选择“走”（沿计划航线采样）或“停下”（关停推进器随水漂流复测）。独立采样误差为0.1。

\section{想象中的海洋与出发前预演方法}

\subsection{想象中的海洋与现场观测同化}

AUV维护48个“想象中的海洋”。出发前，围绕$k$天前的卫星图$c_{\text{map}}$生成48个样本：
\begin{equation}
  c^{(i)}(\mathbf{x}) = c_{\text{map}}(\mathbf{x}) + \sigma_k\, z^{(i)}(\mathbf{x}), \quad i = 1, \dots, 48
\end{equation}
其中$\sigma_k$为合成先验标准差，采用序列集合调整卡尔曼滤波同化现场观测，通过局地化函数抑制伪相关。

\subsection{规划搜索与留出评判分离}

规划器通过交叉熵方法\cite{deboer2005cem}搜索航路点。为消除优化器诅咒\cite{smith2006curse}，将48个海洋划分为32个规划用样本与16个留出评判样本。当先验不确定性经数据标定时，留出样本能对选出航线给出近乎无偏的价值评判。

\subsection{出发前预演控制器与对比基线}

五种时间分配策略为：一直走、一直深想、三段深想一段、三段停下深想一段、三段停下复测一段。下水前，由岸上计算机以4个留出海洋为假想真值，模拟完整任务选出平均遗憾最低的策略执行。出发前预演程序运行在岸上计算机上；以慢计算机为例，单次任务需约190万次想象推演（若在机载GPU上需约125小时），而在台式机单个核心上仅耗时数秒。对比基线包括：固定策略、开发集调好的固定策略、单步元推理以及规划用海洋上的出发前预演对照。

\section{实验结果与分析}

\subsection{规划预算与留出海洋评判的准确性}

开发集实验表明，留出海洋能消除自评高估。当推演次数增至200,000次时，规划用海洋上的搜索自评得分攀升至0.917，而留出海洋上的评判均值与真实航线价值之差始终在0.005以内（图\ref{fig:curse}）。即使标定不确定性有偏差，留出评价对于相对增益的判断依然稳健。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_curse}
  \caption{不同想象推演次数下的航线价值与评判偏差。规划器搜索自评（红线）持续上升，而留出海洋评价（蓝色虚线）与真实价值（黑线）在约2000次后趋于平缓。}
  \label{fig:curse}
\end{figure}

\subsection{算力与底图误差相图及典型任务分析}

相图（图\ref{fig:phase}）显示：深想仅在基础算力极慢时优于“一直走”；停下类策略在所有情况下均带来0.06至0.14的遗憾损失。停下采样虽能压低观测误差，但相对于航行器因停滞而错失浓水区所致的时间平均遗憾，其收益微乎其微。

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{fig_phase}
  \caption{固定策略相图。蓝色与灰色“$\approx$”区域表示无策略显著优于“一直走”。停下类策略无论在何种算力下均劣于最优移动策略。}
  \label{fig:phase}
\end{figure}

\subsection{不同硬件平台上的控制器对比}

测试集上各控制方式表现见表\ref{tab:main}。除了慢计算机配置下“一直走”遗憾较高外，其余配置下三种移动策略差异均在0.004以内，处于噪声范围内。单步元推理因在搜索海洋上自评，分别在80\%至97\%的周期内开启深想，并频繁停下，导致遗憾显著高于调好策略。

\begin{table}[htbp]
  \centering
  \caption{2023至2026年148个测试集任务上各控制方式的时间平均遗憾。}
  \label{tab:main}
  \input{tables/main_table.tex}
\end{table}

出发前预演通过完整任务模拟，自适应地规避了停下策略，并根据硬件调整移动策略组合。在慢计算机上避开了高代价的“一直走”，在省电加速器上倾向于“一直深想”。尽管预演在真实遗憾极小的几种移动策略间难以通过4个假想真值精准判优，且预演内部的遗憾值比真实海洋普遍偏高0.05-0.07（各策略偏移大致相同，不影响排序），但它成功剔除了劣质选项。

\subsection{留出评判消除过度规划的机制检验}

将单步元推理的价值评判改为在留出海洋上进行后，其开启深想的周期比例显著下降，深想比例从80\%--93\%降至30\%--38\%，遗憾水平与预演接近。表明经典单步元推理的过度计算主要源于用搜索海洋自评，改用留出评判即可消除大部分过度规划。

\section{结论}

1. 深度预测模型对1至3天缺测填补图的外推精度未超过直接沿用底图。
2. 将集合划分为规划用与留出海洋，可在所有预算下将评判偏差控制在0.005以内。
3. 在留出想象海洋上评判计算价值，是抑制过度计算的核心机制。出发前预演能够避开停下策略与低效“一直走”，在无需历史任务调参下适配四种硬件（与调好策略差异的95\%置信区间均包含0，比单步元推理低0.011至0.022）；将留出评判引入单步元推理同样能大幅压低计算频次。

局限性：(1)未考虑水平流剪切与昼夜垂直迁移；(2)仿真“真实海洋”基于统计模型生成；(3)路径规划采用简化替代模型；(4)未进行中途重选策略；(5)因任务间环境波动（标准差约0.13）远大于策略间差异，预演仅能实现针对硬件的策略适配，无法分辨最优单任务策略（事后最佳策略遗憾为0.243，预演为0.265）。

===== FILE: sections/appendix.tex =====
\section{代码与数据说明}

本研究的数据、模型与实验代码开源于：\TBD{GitHub 仓库地址}。实验使用的两套卫星遥感数据集（\texttt{noaacwNPPN20S3ASCIDINEOF2kmDaily}与\texttt{jplMURSST41}）均下载自NOAA CoastWatch ERDDAP服务器。

\section{人工智能工具使用说明}

\begin{enumerate}
  \item 学生提出了本文的研究问题，设定了研究方向与各项要求，并对论文承担全部责任。
  \item Claude（Anthropic）完成了文献调研，编写了实验代码，运行数值实验并绘制图表。
  \item Gemini（Google）根据实验事实撰写了论文初稿与修改稿。
  \item Claude对照实验结果与原始文献逐一核查了文中的全部数值与文献引用。
\end{enumerate}
