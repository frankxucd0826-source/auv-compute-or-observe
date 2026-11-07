# Revision 2

Draft 2 (attached as the current sections/*.tex) is much better: the length, tone and almost all
numbers are right. All experiments have now finished. Please produce the final text: fill every
\TBD{} except the repository address, and make the corrections below. Keep the length about the
same (body at most about 8,500 Chinese characters, Chinese abstract at most 500 characters);
keep the structure unless a change below needs it. Wording and structure remain your decision.

## 1. New results (all in the updated facts.md; the table file is regenerated)
1. Fast computer and efficient accelerator: both columns of the table are filled. Per-vehicle
   tuned strategy: slow - think one in three; moderate - think one in three; fast - always go;
   efficient accelerator - always think. Apart from the slow computer, the three strategies that
   keep moving are within 0.003 of each other on the test years; the stopping strategies are
   0.06-0.14 worse on every vehicle.
2. Rehearsal versus the tuned strategy: +0.007, -0.003, +0.002, -0.001 (all intervals include
   zero). Rehearsal minus one-step metareasoning: -0.011, -0.022, -0.013, -0.012 (all intervals
   below zero). One-step metareasoning thinks in 80/93/97/94% of intervals and stands still in
   about a third of them on every vehicle.
3. What rehearsal picks: always go in 1% of missions on the slow computer (where always going
   costs +0.104), 30% on the moderate and 47% on the fast computer; with the cheap accelerator it
   picks always think most often (43%). So it adapts to the vehicle. Within a vehicle, held-out
   and searched rehearsal agree on only 37-41% of individual missions (see correction 1).
4. Runs are exactly reproducible: rerunning rehearsal on the 148 slow-computer missions gave
   identical regrets.
5. New check of the mechanism (facts.md, "Check of the mechanism"): one-step metareasoning that
   values more planning and more looking on the held-out imagined oceans instead of the searched
   ones thinks much less (80% to 30%, 93% to 38% of intervals), stands still half as often, and
   reaches rehearsal's level (moderate: -0.017 versus the usual one-step metareasoning, interval
   below zero; slow: -0.009, interval touching zero). This links the planning-budget experiment
   (5.1) to the controller comparison (5.3): the over-planning is mostly the self-assessment
   bias. Add it as a short subsection or paragraph in section 5 (text only, no new figure), and
   let it shape the conclusion: the shared idea of the paper is to judge computation on imagined
   oceans that were not used to search; rehearsal applies it to whole missions before departure,
   the corrected one-step controller applies it interval by interval. Keep rehearsal as the main
   method (the title can stay), and do not claim the corrected one-step controller is better or
   worse than rehearsal - they are within each other's intervals.
6. Phase diagram (attached fig_phase.png; facts.md "Phase diagram"): thinking one interval in
   three clearly beats always going only on the slowest computer (5 rollouts/min), and there more
   so the worse the map (-0.086, -0.109, -0.138); one marginal cell at 10/min; from 20/min up
   nothing is clearly better than always going; stopping costs 0.063-0.118 in all 18 cells.
   Replace the \TBD in 5.2 with this, and make the caption match the attached figure (its
   design changed: grey "≈" cells mean no strategy is clearly better than always going).

## 2. Corrections to draft 2
0. The bootstrap intervals were recomputed with all four vehicles, so a few differ in the third
   decimal from draft 2 (e.g. slow-computer rehearsal versus tuned is now -0.001 to +0.014, not
   +0.015). The text must quote exactly the numbers in the regenerated table and facts.md.
1. Held-out versus searched rehearsal (last paragraph of 5.3): they do NOT pick "nearly the
   same strategies". Overall they pick each strategy about equally often, but on individual
   missions they agree only about 38% of the time - about what two independent picks with
   those shares would give. The facts sheet now explains what rehearsal does and does not
   achieve: it avoids the bad options (stopping everywhere; always going on the slow computer),
   and so adapts to the vehicle; among strategies whose real difference is 0.01 or less, its
   per-mission pick is no better than chance. Say this plainly; it is a finding, not a defect
   to hide. It belongs in the results and, briefly, in the conclusion and limitations (picking
   the best strategy per mission would give 0.243 on the moderate computer versus 0.265 - room
   that four imagined missions cannot reach).
2. One-step metareasoning (5.3): describe what it does without attributing all of it to one
   cause. It values more planning by the planner's own improvement on the searched oceans and
   values resampling by preposterior analysis over the imagined oceans; it ends up thinking in
   80-97% of intervals and standing still in about a third of them. Do not write "由于……自评
   改进量……" as the reason for the stopping.
3. "无偏的价值评判" for the held-out oceans (4.2): add the condition - nearly unbiased when the
   map uncertainty is calibrated (fig_curse shows the offsets when it is not).
4. 1.1, first paragraph: jiang2015horizon is about planning horizons with inaccurate models; do
   not cite it for "maps lag behind and miss small-scale structure".
5. 1.2, last paragraph: the old map is 1-3 days old because of product processing and the time
   needed to get to sea, not "在等待下水期间".
6. 1.2: delete "高浓度斑块的叶绿素a浓度通常超过6 mg/m3" (its source could not be re-checked);
   cite zhao2025distinguishing (new in refs.bib) for the late-spring/early-summer season of
   Prorocentrum donghaiense blooms; lou2014diurnal for the drifting with the tides.
7. 2.1: the two datasets come from NOAA CoastWatch ERDDAP servers (not literally "the same
   server").
8. 3.1: the drifting frame is a modelling assumption - write "本文假设斑块随表层水体一同移动",
   then why it is reasonable (Lou & Hu), rather than stating it as a fact.
9. 3.1: delete the sentence about also recording the end regret and the share of end answers
   within 0.1 - the paper does not report them.
10. Wording in 5.3: "降低遗憾−0.011" is a double negative (write "低0.011" or "差值为−0.011");
    "均在置信区间之内" should say that the intervals include zero.
11. Limitations (conclusion): besides the two given, state briefly (a) the "real ocean" in the
    simulation is the satellite map plus correlated noise calibrated from published validation,
    not in-situ truth; (b) the two-waypoint planner on a 2-D surface field is a simplified stand-
    in, which is why computer speed is expressed relative to the planning problem; (c) rehearsal
    needs a ship or shore computer before launch; (d) per-mission choice is not achieved (item 1).
12. Appendix A: add that the repository also holds the conversation logs between the student
    and Claude (with content about the student's other, unpublished work removed), the figure
    code and the raw results.
13. The figures now say 航行器 instead of 艇 ("(B) 航行器的想象", "航行器遇到的真实海洋",
    "(a) 航行器携带的 3 天前卫星图"); captions should follow.
14. Both abstracts end on numbers; the eighth step (what the result means for ocean big data
    and for vehicles that must decide between computing and observing) is missing - add one
    sentence, at the strength of the evidence.

## Output
As before: sections/title.tex, sections/subtitle.tex, sections/abstract.tex, sections/body.tex,
sections/appendix.tex (no terms.md needed unless you change a name).
