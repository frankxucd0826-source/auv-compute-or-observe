# Figures (file names without extension; width = \linewidth unless noted)

PNG copies of the finished figures are attached; describe only what is in them.

- fig_overview (Figure 1). Centre: a 3D block of the East China Sea window of one test mission
  (2025-04-04), its top surface coloured by the real chlorophyll the vehicle meets; a REMUS-class
  AUV with its track (light blue = going with low-power planning, orange = planning on the GPU);
  a pale ring at the true densest water ("赤潮最浓处"); above the block a small stack of imagined
  oceans, the top two framed orange (held out), the others framed dark blue (searched).
  (A, blue) ocean big data: 2018-2026 daily 2-km satellite chlorophyll, 3197 days; the real
  ocean the vehicle meets is not the 3-day-old satellite map (two thumbnails, "≠"); how wrong an
  old map is (1/2/3 days: 0.13/0.18/0.21; coastal fronts in summer up to 0.3 in 3 days); 422
  bloom-season missions cut from the data (development 2018-2022: 274; test 2023-2026: 148);
  "small-scale information has to be observed on site". An arrow labelled "出发前装入" goes from
  the old map to the stack. (B, green) the vehicle's imagination: 48 imagined oceans generated
  from the old map and the data-calibrated error; 32 used to plan routes, 16 held out to judge;
  "出发前预演": the five time-allocation strategies are each run once in imagination, one is
  chosen by the result on held-out oceans. (C, sand) every 20 minutes: 走 (follow the plan,
  sampling on the way), 深想 (plan on the high-performance computer, +20 W), 停下 (drift with
  the water, resample in place); the operations centre may ask at any time where the densest
  water is. No satellite is drawn.
- fig_atlas: four seasonal maps of the East China Sea box (25-33 N, 119.5-127 E): spread of the
  3-day change of log10 chlorophyll from all 3197 days; land grey; dots in the spring panel are
  mission windows (blue development 2018-2022, green test 2023-2026).
- fig_curse: (a) value of the planned route (y axis converted to mg/m3, time-averaged best
  concentration along the route) against imagined rollouts per decision (64 to 200,000, log
  axis): the planner's own score during search (red, keeps rising), the same route judged on
  the held-out imagined oceans (blue dashed), and its real value (black); shaded bands = spread
  over missions; real and held-out flatten after about 2000. (b) estimate minus reality in log
  units: search score (red) grows to about +0.11; held-out with calibrated uncertainty (blue
  dashed) stays at zero; held-out with the uncertainty stated 1.5 times too large (orange dotted)
  is about +0.07 at every budget, with it stated half as large (light blue dotted) about -0.06.
- fig_phase (attached PNG): a grid of low-power computer speed (5, 10, 20, 50, 100, 200 rollouts
  per minute) x how far the real ocean departs from the satellite map (0.05, 0.15, 0.3); 60
  development missions per cell, the five fixed strategies on the same missions. (a) a cell is
  coloured by the strategy with the lowest time-averaged regret only where it beats always going
  clearly (95% interval of the paired difference below zero), and the number is its regret minus
  that of always going; grey "≈" = no strategy clearly better than always going. (b) how much
  worse the better of the two stopping strategies is than the best strategy that never stops
  (positive = stopping costs).
- fig_example: one test mission (2023-04-15, slow computer): (a) the 3-day-old map the vehicle
  carries (start = white triangle on the east edge); (b) the real ocean, the track of always going
  (blue) and of thinking one interval in three (orange), the true densest water (star, south-west
  corner); (c) the error of the answer the operations centre gets, over 24 h (always going stays
  near 0.4, average 0.43; thinking one in three reaches 0 after about 19 h, average 0.31).
- No fig_main: the main comparison is the table paper/tables/main_table.tex.
