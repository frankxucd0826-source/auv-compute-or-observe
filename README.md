# 合理反例检验：粗分辨率海流图下自主水下航行器何时计算、何时观测

浙江大学《海洋大数据技术原理与应用》课程大作业（2026–2027 学年秋学期，任课教师张帆研究员）。作者：徐陈栋（3240100538，24 级海洋工程与技术）。

**直达**
- 论文：[paper/main.pdf](paper/main.pdf)
- 与 Claude 的对话记录：[chat/对话记录_1.md](chat/对话记录_1.md)（11-04 至 11-06）、[chat/对话记录_2.md](chat/对话记录_2.md)（11-06 起）
- 与 Gemini（写作）的每一轮往来：[chat/](chat/) 下的 `Gemini对话记录_*.md`
- 研究笔记（含失败的尝试）：[NOTEBOOK.md](NOTEBOOK.md)；作者每次的原话：[THEME.md](THEME.md)

## 切入点与问题
- **切入点**：课上讲的“海洋大数据的计算引擎”。海洋大数据的计算正从岸基延伸到航行器端侧，而航行器端侧算力有限，自然引出“继续计算、去测量、还是移动”的权衡。
- **作者最初的问题**（11-04）：海洋智能体何时应该继续计算、何时应该重新观测？前期研究（东海赤潮巡测）发现：多算只让规划器的自评越来越高，真实收益早已不涨；计算与观测怎么分配，对结果影响很小。
- **作者把问题收紧后的版本**（11-06）：航行器面前有左右两条航路，只有一张粗分辨率海流图。在海流场 A 中走左边好，在 B 中走右边好。多推理几轮、换更大的模型、加密求解网格，只会把答案算得更“精致”，却得不到区分两个世界的新信息。**对当前推荐的路线，能否找到另一个同样符合现有观测、却使这条路线变差的合理海流场？** 能找到，就该测量（或在测量太贵时保守）；找不到而只是数值不够准，才该继续算。

## 对话记录导读：作者的每条消息（时间为 UTC）
| 时间 | 所在记录 | 要点 |
|---|---|---|
| 11-04 13:56 | 对话记录_1 | 提出最初的问题：海洋智能体何时继续计算、何时重新观测；要求调研创新性与一周可行性 |
| 11-04 14:44 | 对话记录_1 | 定篇幅与期限、仓库公开；建议可试世界模型类方法；授权自主推进 12 小时 |
| 11-05 00:09 | 对话记录_1 | 要求用中文讲清项目、结果与结论 |
| 11-05 00:44 | 对话记录_1 | 质疑“真实海洋是模拟的”，要求用真实卫星数据；批评图表与封面；要求补对照与消融、按学术论文格式重写 |
| 11-05 03:15、03:22 | 对话记录_1 | 建公开仓库并推送 |
| 11-06 15:57（中断后重发）、16:03 | 对话记录_1、_2 | 质疑第一种方法提升小、预演不新；提出利用物理规律与运动约束，要求从根本上重新考虑 |
| 11-06 16:46 | 对话记录_2 | 提出新问题：两条航路与粗分辨率海流图——能否找到同样符合观测、却使推荐路线变差的合理海流场 |
| 11-06 17:07、17:09 | 对话记录_2 | 决定全面转向，授权自主推进 12 小时 |

## 主要结论（四种设置：黑潮主设置、湾流、阿古拉斯回流区、黑潮区改带卫星测高地转流图）
- **多算消除不了环境歧义**：求解计算量增加 64 倍，选错一侧的比例几乎不变（黑潮 21.7%→19.7%，其余三种设置同样如此）；换成当天 0.5° 图，黑潮选错率降到 10.4%。
- **最大后悔值找得出额外航时在哪**：按它排在前 20% 的任务集中了 53%–71% 的额外航时，高于按“集合中改变选边的成员比例”（36%–52%）或粗图左右航时差排序。在黑潮主设置中，约 71 次航线求解就达到集合平均选边用 1024 个集合成员（2048 次求解）的效果。
- **判定粗图不可信后，取新信息最划算**：超阈值时上浮取当天 0.5° 图，湾流的平均额外航时从 3.56 小时降到 1.31 小时，阿古拉斯回流区从 6.87 小时降到 2.20 小时；黑潮主设置中单次上浮代价低于约 0.8 小时时同样划算。
- **适用范围**：不观测时改选最大后悔值较小的一侧，只在黑潮主设置显著有效（0.98→0.70 小时）。湾流与阿古拉斯回流区有一部分任务两侧都可能被强流堵死，这一做法失效；航行器改带真实卫星测高地转流图时，各类响应都不显著。阿古拉斯与卫星图两项检验的计划都在下载数据之前写进 NOTEBOOK。
- **“合理”的定义是关键**：用历史相似日的小尺度差代替标定的误差模型构造合理集合，保守改选不再有效。
- 术语（与论文一致）：**粗图** = 3 天前的 1° 粗分辨率海流图；**最大后悔值** = 在与粗图相容的合理流场集合中，所选一侧比另一侧最多多花的航时；**阈值判据** = 最大后悔值超过阈值即判定粗图不可信；**额外航时** = 实际航时减去真实更快一侧的航时。

## 目录
| 路径 | 内容 |
|---|---|
| `paper/` | 论文（`main.tex`、`sections/`、`refs.bib`、`tables/`、`figures/` 及作图代码 `route*_*.py`，`rstyle.py` 统一字体与配色，`rmaps.py` 画深色海图；图 1 中心的三维示意由 `figures/blender/render_route.py` 渲染）；`check_paper.py` 逐项核对正文数字与引用；`paper/gemini/` 为此前交给 Gemini 写作的简报、事实清单（`facts_v3.md`、`facts_v4.md` 由脚本从结果生成）与它的原始回复 |
| `src/oceanroute/` | 航路决策研究：最快航线求解器（`solver.py`，左右两侧、梯度）、海流数据与粗图（`fields.py`）、旧粗图误差模型（`errormodel.py`）、任务与反例搜索（`mission.py`） |
| `experiments/route_*.py` | 主实验（`route_eval.py`）、汇总与阈值标定（`route_summary.py`）、适用范围（`route_scope.py`）、事实清单（`route_facts.py`、`route_facts_rev6.py`）、示例任务（`route_example.py`）、设定扫描（`route_scan.py`）、随机合理场数量对照（`route_ensemble_size.py` 计算、`route_ensemble_analysis.py` 汇总） |
| `scripts/download_hycom.py` | 下载 HYCOM 海流（免账号） |
| `src/oceanmeta/`、`experiments/` 其余脚本 | 前期研究（东海赤潮巡测）的仿真、方法与实验，见 `NOTEBOOK.md` |
| `results/` | 实验原始输出（每行一个任务）与汇总；`route_main_*` 为主实验，`route_fresh05_*`、`route_slow_*`、`route_analog_*` 为适用范围与消融，`route_ens1024_*` 为每个任务 1024 个随机合理场（压缩存储），`route_gulf_*`、`route_agulhas_*` 为湾流与阿古拉斯回流区的重复实验，`route_altimetry_*` 为改带卫星测高图的检验 |
| `chat/` | 对话记录（见上） |
| `notes/` | 文献调研（`prior-决策歧义.md` 为新问题的文献对照） |

## 复现
```bash
python -E -X utf8 scripts/download_hycom.py
python -E -X utf8 tests/test_route_solver.py
python -E -X utf8 experiments/route_eval.py --split dev  --tag main --deg 1.0 --lag 1 --sigma 0.15
python -E -X utf8 experiments/route_eval.py --split test --tag main --deg 1.0 --lag 1 --sigma 0.15
python -E -X utf8 experiments/route_summary.py main
bash results/route_settings_queue.sh        # 适用范围与消融（当天 0.5° 图、慢速航行器、相似日合理集合）
python -E -X utf8 experiments/route_scope.py
python -E -X utf8 experiments/route_example.py
python -E -X utf8 experiments/route_facts.py
python -E -X utf8 experiments/route_ensemble_size.py --split test --M 1024   # 每个任务 1024 个随机合理场
python -E -X utf8 experiments/route_ensemble_size.py --split dev --M 1024
python -E -X utf8 experiments/route_ensemble_analysis.py
python -E -X utf8 scripts/download_hycom.py --region gulfstream              # 湾流重复实验
bash results/route_gulf_queue.sh                                             # 设 OCEANROUTE_REGION=gulfstream 后跑主流程
python -E -X utf8 scripts/download_hycom.py --region agulhas                 # 第三海区（检验计划见 NOTEBOOK）
bash results/route_agulhas_queue.sh
python -E -X utf8 scripts/download_altimetry.py                              # 卫星测高地转流图（检验计划见 NOTEBOOK）
bash results/route_altimetry_queue.sh                                        # 设 OCEANROUTE_MAP=altimetry 后跑主流程
python -E -X utf8 experiments/route_facts_rev6.py
bash paper/build.sh
```
作图（在 `paper/figures/` 下运行）：`route1_overview.py`（总体框架；先运行 `blender/make_route_textures.py` 生成海面与流场纹理，再用 Blender 4.5 运行 `blender -b -P blender/render_route.py -- --samples 160` 渲染中心三维示意）、`route2_example.py`（示例任务）、`route3_data.py`（研究海区与粗图误差）、`route4_compute.py`（加算与取新信息）、`route5_rank.py`（风险排序）、`route6_budget.py`（集合成员数量）、`route7_respond.py`（判定不可信后的回应）。前期探索的图（`fig_*.py`）保留在同一目录。随机种子按任务固定，同一命令重跑结果逐条一致。

## 人机协作说明
- 研究问题由作者提出，并由作者两次收紧（11-04 最初的问题；11-06 质疑第一种方法提升小、创新不足，并提出“两条航路 + 合理反例”的新问题，决定全面转向）；作者把关方向与要求，对论文负责。
- Claude（Anthropic）完成文献检索与核对、全部代码、实验、作图，并逐条核对正文数字与引用；论文此前各稿由 Gemini（Google）依据 Claude 生成的事实清单与写作提纲撰写，终稿由 Claude 按作者要求重构重写。
- `chat/` 中的对话记录由 `scripts/export_chat.py`（与 Claude）和 `scripts/export_gemini.py`（与 Gemini）导出：收录的作者消息与助手回复均为原文；工具调用只列一行、输出截短；涉及作者其他项目（含未发表论文）的工具调用与输出已省略；定时提醒与后台通知已标明不是作者输入。

## 数据来源
- 海流：HYCOM 全球海洋再分析 GLBy0.08（实验 93.0），1/12°，经 HYCOM 公开数据服务器读取；主实验区 23–31°N、121–129°E（黑潮），重复实验区 33–41°N、75–67°W（湾流）与 35–43°S、14–22°E（阿古拉斯回流区）。
- 卫星海流图：NOAA CoastWatch 近实时融合测高地转流（`noaacwBLENDEDNRTcurrentsDaily`，0.25°，逐日），经 NOAA CoastWatch ERDDAP 下载（免账号）。
- 前期研究：NOAA CoastWatch 多星融合叶绿素 a（`noaacwNPPN20S3ASCIDINEOF2kmDaily`）与 NASA JPL MUR 海表温度（`jplMURSST41`），经 NOAA CoastWatch ERDDAP 下载。
