# Revision 6c: the vehicle carries a real satellite current map (a test written down before its data were downloaded)

The attached section files are the current, checked paper. One more result must go in (facts_v4.md, last
section 航行器改带真实卫星海流图). Until now the vehicle's coarse map was made from the same reanalysis as
the "real ocean" (block means of HYCOM, 3 days old) — the largest threat to validity, stated in the
limitations. In this test the vehicle instead carries the NOAA CoastWatch near-real-time blended altimetry
surface geostrophic currents (0.25°, from 3 days before), the kind of product a vehicle can actually get;
the real ocean is still the HYCOM field; surfacing fetches today's altimetry map (1 hour), and today's 0.5°
model map is kept as an idealised reference. The error model, radius and thresholds were calibrated on the
development years with "altimetry map minus HYCOM"; the test years were scored once. The plan and its five
checks were written into the research notebook before the satellite data were downloaded and not changed.
Report the five checks in the plan's own terms (the facts file states each verdict), finding first.

## Pieces to write (output each after its marker line, nothing else)

===== T1 =====
experiments.tex, Section 6.7: a new paragraph starting "第六，" placed after the paragraph that starts
"第五，" (Agulhas) and before the table. About 300-400 characters, at most eight numbers. Say what the
map is, that the plan was written down before the data were downloaded, give the five outcomes compactly,
and say in one sentence what this means for the main results (do they depend on the map being made from
the same model as the truth?). Do not repeat numbers of other settings.

===== T2 =====
experiments.tex, the limitations paragraph (starts "本研究存在五方面局限"): rewrite point 2 only so that
it says the main experiments use a map made from the same reanalysis, that Section 6.7 repeats the test
with a real satellite altimetry map, and that the "real ocean" is still a reanalysis field; output the whole
paragraph with points 1, 3, 4, 5 word for word.

===== T3 =====
abstract.tex: the Chinese abstract's last sentence and the English abstract's last sentence only, each
extended by one short clause on the satellite-map test (output the two sentences, each after its own line
"===== T3-zh =====" / "===== T3-en ====="). Chinese abstract total at most 600 characters, English at most
305 words.

===== T4 =====
conclusion.tex: the sentence that starts "湾流区与阿古拉斯回流区的重复实验表明", extended by one short clause
on the satellite-map test (output just that sentence).

## Rules (as before)
- Every number must appear in facts_v4.md or facts_v3.md. Terms as in terms_v5.md; 卫星测高地转流图 for
  the altimetry map; 当天 0.5° 模式图 for the idealised reference.
- No English abbreviations in Chinese text; no emotive or inflated words; no "显著" unless a confidence
  interval excludes 0; first sentence of each paragraph states its conclusion; write "\%" for percent.
- Keep every \label, \ref, \cite as given.
