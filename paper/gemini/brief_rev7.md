# Revision 7: reorganise the paper's headline around the findings that hold in all four settings

The attached section files are the current, checked paper. Its experiments now cover four settings: the
Kuroshio main setting, the Gulf Stream, the Agulhas retroflection, and the Kuroshio with a real satellite
altimetry map (facts_v3.md, facts_v4.md). The abstract, the contributions and the conclusion still lead
with the main setting's best number (门控后取保守 0.98 → 0.70 小时, −28%), which did not hold in the other
three settings. The student has decided that the paper's main line is the findings that hold everywhere.
Rewrite only the pieces below around this main line; keep the method description and every fact exact.

## The main line (use these facts exactly; all are in the fact files)
A. Holds in all four settings:
   1. 64 times more computation barely changes the share of wrong-side choices
      (黑潮 21.7% → 19.7%，湾流 18.5% → 19.4%，阿古拉斯 27.7% → 27.7%，卫星图 19.9% → 19.6%).
   2. The worst regret finds where the losses are: the 20% of missions it ranks riskiest hold more of the
      map's loss than when ranked by the flip share (67% 对 49%，71% 对 49%，53% 对 36%，67% 对 52%).
   3. (Kuroshio) the counterexample search reaches with about 71 route solves the side choice that the
      expected-time rule over random plausible fields needs about 2048 solves (1024 fields) to reach.
   Plausible counterexamples exist for 98.8%-99.7% of missions with the model-derived maps and for 81.0%
   with the satellite map: common, but less so with a real map.
B. Depends on the setting:
   4. Surfacing for today's 0.5° map only when flagged: strong where the coarse map is poor (湾流
      3.56 → 1.31 小时，阿古拉斯 6.87 → 2.20 小时); in the Kuroshio main setting it pays only when one surfacing
      costs less than about 1 hour; not significant with the satellite map.
   5. Choosing the side with the smaller worst regret without observing: significant only in the Kuroshio
      main setting (0.98 → 0.70 小时); not significant in the other three settings.
C. Meaning: the plausible counterexample test reliably tells when the map cannot be trusted and where the
   losses are; computing more is not the answer; what to do then depends on the observation available.

## Pieces to write (output each after its marker line, nothing else)

===== V1 =====
abstract.tex: the whole file. Keep the background, gap and method sentences (you may shorten them a
little); rewrite the results so that A comes first, then B, then C in one sentence. Name the four settings
once. Chinese abstract at most 600 characters; English abstract at most 300 words, same content; keywords
unchanged.

===== V2 =====
intro.tex: the paragraph that starts "为此，本文提出“合理反例检验”". Change only its first sentence's end
("且在观测过贵时应直接选择最坏后悔更小的一侧"), so that choosing the smaller worst regret is a fallback
whose value depends on the setting; keep the rest of the paragraph (the example) word for word. Output the
whole paragraph.

===== V3 =====
intro.tex: the whole "\begin{itemize} ... \end{itemize}" block of contributions. Keep item 1 word for word
(it must keep "据我们所知，本文首次"). Item 2 may stay as it is. Rewrite item 3 as "四种设置下的系统实证" along
the main line (A, then B, at most eight numbers).

===== V4 =====
conclusion.tex: the whole file, along the main line (principle; A; B; future work). At most 480 characters
of running text.

===== V5 =====
experiments.tex, Section 6.4: only its first sentence (starts "在五类响应策略的对比中"): keep its finding and
add that this gain belongs to the main setting and was not reproduced in the other settings (see 第\ref{sec:scope}节).

===== V6 =====
innovation.tex, table row 4 (starts "4. 权衡最坏后悔与观测代价的门控响应"): cell 4 only (证据), leading with
the surfacing results in the two poor-map regions, then the main setting's conservative result as
setting-specific. Output just the cell text.

## Rules (as before)
- Every number must appear in facts_v4.md or facts_v3.md. Terms as in terms_v5.md (卫星测高地转流图 for the
  satellite map). No English abbreviations in Chinese text; no emotive or inflated words; "显著" only where a
  confidence interval excludes 0; first sentence of each paragraph states its conclusion; write "\%".
- Keep every \label, \ref, \cite as given.
