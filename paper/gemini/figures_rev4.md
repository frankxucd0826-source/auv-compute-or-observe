# Figures and tables (files exist; write captions and refer to them in the text)

Order of first mention = numbering. Every number below is also in facts_v2.md.

Fig. 1 `fig_overview` - overview of the approach (vector diagram around a 3-D render).
  (A) ocean big data: 3197 days of daily 2-km satellite chlorophyll and SST; the 3-day-old map vs
  the map of the mission day; stale-map error 0.125/0.176/0.210 for 1/2/3 days; seasonal atlas of
  3-day change; 422 bloom windows (274 development, 148 test); a 5.5-million-parameter deep
  forecaster is no better than keeping the latest map -> small scales must be observed.
  (B) before launch: 48 imagined oceans c^(i) = c_map + sigma_k z^(i) (sigma_k calibrated from the
  data), 32 searched / 16 held out; rehearsal: 4 held-out oceans as imagined truths x 5 strategies,
  the bars are the imagined regrets of one real test mission (2025-04-04, moderate computer;
  always go 0.715 chosen, think one in three 0.720, always think 0.734, the stopping strategies
  0.881 and 0.921); the strategy s* with the lowest imagined regret goes to sea.
  (C) during the mission: every 20 minutes go / think / stop; inset: the planner's search score
  keeps rising with the planning budget while real value and held-out judgement level off; the
  operations centre asks at any time where the densest water is; score = time-averaged regret.
  Message: data-calibrated imagined oceans are the yardstick for the value of computation.

Fig. 2 `fig_data` - what eight years of satellite chlorophyll tell the vehicle and what not.
  (a)-(d) spread of the 3-day change of log10 chlorophyll per season over all 3197 days (medians
  0.127 spring, 0.107 summer, 0.103 autumn, 0.081 winter; a band along the Zhejiang-Fujian coast
  and the Changjiang plume front in summer), spring panel with the 274 development and 148 test
  windows; (e) stale-map error 0.125/0.176/0.210 for maps 1/2/3 days old (development windows),
  next to the about 0.15 difference between a same-day satellite map and in-situ chlorophyll;
  (f) a deep spatio-temporal forecaster vs keeping the latest map on the test years (errors
  0.1229 vs 0.1226, 0.1439 vs 0.1439, 0.1487 vs 0.1474 for 1/2/3-day leads).
  Message: the data calibrate how wrong a stale map is, but cannot replace observing.

Fig. 3 `fig_curse` - thinking longer makes the planner believe more, not achieve more.
  (a) value of the chosen route (log10 chlorophyll) vs rollouts per decision (64 to 200,000): the
  search score 0.762 -> 0.917, real value 0.749 -> 0.803 (flat after about 2000), held-out judgement
  0.745 -> 0.802; gap of 0.114 at the largest budget; (b) estimate minus reality: search score bias
  grows; held-out judgement stays within 0.005 with calibrated uncertainty, shifts by -0.06 / +0.07
  with half / 1.5 times the uncertainty but keeps the right gain.
  Message: valuing computation with the planner's own score is biased; held-out oceans are not.

Fig. 4 `fig_main` - every compared controller minus rehearsal (paired, 95% intervals), four
  vehicles (columns), both truth models (filled: same-day satellite map plus small-scale
  variability, main setting; hollow: same-day satellite map itself). Rows grouped: needs past
  missions (tuned fixed strategy, learned selector); online metareasoning (one-step, one-step with
  held-out valuation); survey rules without route planning (greedy, upper confidence bound,
  Thompson, lawnmower); reference (per-mission best in hindsight).
  Message: rehearsal matches the methods that need past missions, beats one-step metareasoning and
  all survey rules (greedy only ties on the slow computer), on every vehicle and both truth models.

Table 1 `tables/settings.tex` - experimental settings.
Table 2 `tables/main_table.tex` - time-averaged regret of every controller, 148 test missions,
  four vehicles x two truth models; bold = best runnable controller in each column; rehearsal row
  shaded. Footnote: which fixed strategy was tuned per vehicle (see facts_v2.md).

Fig. 5 `fig_mech` - why one-step metareasoning loses and what rehearsal chooses (main truth model).
  (a) share of intervals with the high-performance computer on, (b) share spent stopped, for
  one-step metareasoning, the same with held-out valuation, and rehearsal; (c) which strategy
  rehearsal picks per vehicle.
  Message: trusting the search score makes the online controller think in 80-97% of intervals and
  stop in a third; held-out valuation and rehearsal think only as much as the computer needs and
  rarely stop; rehearsal's picks follow the hardware.

Fig. 6 `fig_example` - one test mission (2023-04-15, slow computer; first test mission in date
  order where the two strategies differ by more than 0.1): (a) the 3-day-old map and the start;
  (b) the real ocean with the tracks of always go (blue) and think one interval in three (orange,
  thick where the high-performance computer ran) and the true densest water (star); (c) how far
  the reported location is from the densest water over 24 h (always go stays near 0.4, mean 0.43;
  think one in three reaches the densest water after about 19 h, mean 0.31).
  Message: on a slow computer, background planning alone leaves the vehicle circling mid-window.

Fig. 7 `fig_ablation` - rehearsal with one design choice changed at a time (slow and moderate
  computers, main truth model), change of regret vs the full method with 95% intervals.
  Message: see facts_v2.md "Ablation".

Fig. 8 `fig_phase` - when thinking and stopping pay: grid of low-power computer speed (5-200
  rollouts per minute) x departure of the real ocean from the satellite map (0 = the satellite map
  itself, 0.05, 0.15, 0.30), 60 development missions per cell. (a) best thinking strategy minus
  always go (framed = significantly better); (b) the better stopping strategy minus the best
  strategy that never stops (all significantly positive).
