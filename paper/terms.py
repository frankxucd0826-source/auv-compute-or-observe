"""Names used in the paper's figures and tables, in one place: change a name here and rerun the
figure and table scripts. Keys are the controller names in results/*.jsonl."""
STRATEGY = {"fixed-0": "一直走", "fixed-1": "一直深想", "periodic-100": "三段深想一段",
            "periodic-300": "三段停下深想一段", "periodic-200": "三段停下复测一段"}
CONTROLLER = {**STRATEGY, "rational": "单步元推理", "double": "单步元推理（留出估值）",
              "rehearsal": "出发前预演（本文）", "rehearsal-self": "预演（以搜索过的海洋为真值）",
              "tuned": "调好的固定策略", "learned": "按历史任务学习的选择器",
              "lawnmower": "割草机式全覆盖", "greedy": "贪心：驶向估计最浓处", "ucb": "上置信界采样",
              "thompson": "汤普森采样", "random5": "五种策略随机选", "random3": "三种不停策略随机选",
              "oracle": "每次任务事后最优（参考）"}
TUNED = "调好的"          # marks the fixed strategy tuned on the development years
VEHICLE = {"weak": "慢计算机", "moderate": "中等计算机", "strong": "快计算机", "efficient": "省电加速器"}
VEHICLE_SUB = {"weak": "5 次/分，+20 W", "moderate": "20 次/分，+20 W", "strong": "100 次/分，+20 W",
               "efficient": "20 次/分，+5 W"}
TRUTH = {"sat+": "当天卫星图 + 小尺度变化", "sat": "当天卫星图"}
