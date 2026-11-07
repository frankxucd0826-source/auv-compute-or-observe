# Brief for the first full draft

You are the writer of a Chinese course paper; I (Claude) ran the research and will check every
fact you write. Decide the structure, wording, terminology, emphasis and length yourself; keep
every fact, number, citation and figure content in the attached facts sheet exactly as given,
and do not add references that are not in refs.bib.

## The paper
- Course: 海洋大数据 (Ocean Big Data), Zhejiang University, autumn 2026; instructor 张帆 (research:
  AI for Science, millisecond-level real-time scientific computing, air-sea intelligent
  integration, polar intelligent navigation computing). He is not an oceanographer by training:
  explain ocean terms (chlorophyll as bloom indicator, gap-filled satellite products, AUV) in one
  plain clause where they first appear.
- Length: about 12-16 pages in the ZJU course-paper template, figures included. Chinese,
  academic register.
- Output: LaTeX for ctexart, in four files I will \input into the template (cover, table of
  contents and reference list are handled by the template):
    sections/title.tex      one-line title (≤ 30 characters)
    sections/subtitle.tex   one-line subtitle starting with "——"
    sections/abstract.tex   \section*{摘\quad 要} ... 关键词 ... \clearpage \section*{Abstract} ... Keywords ...
                            (each with \addcontentsline{toc}{section}{...} as in the current file)
    sections/body.tex       \section{...} etc.; cite with \cite{key}; figures with
                            \begin{figure}[htbp]\centering\includegraphics[width=\linewidth]{fig_xxx}\caption{...}\label{fig:xxx}\end{figure}
    sections/appendix.tex   \section{...} sections for: code and data availability (GitHub
                            repository, to be filled), and the use of AI tools (who did what)

## What the paper must get across (my view; you may frame it differently)
An ocean robot that carries a big-data map has to decide, again and again, how to spend its
time and energy: imagine more (plan on its map), go and look, or stop and look again. The
question is studied with eight years of satellite chlorophyll over the East China Sea and
422 bloom-season missions. Three findings: (1) the planner's own score of how much more thinking
helps keeps rising after the real benefit has stopped, while imagined oceans kept out of the
search judge it correctly; (2) heavy thinking pays only when the onboard computer is too slow
for the planning problem, stopping to resample mid-mission never pays here, and which fixed
allocation is best changes with the vehicle; (3) rehearsing the mission in imagination before
setting off picks the allocation as well as tuning each vehicle on past missions would, and
better than any single fixed rule or classic one-step metareasoning.

## Writing standards the student holds (from earlier papers)
- Abstract in eight steps: background; need; what existing approaches lack; what this paper
  proposes; its key points; the experiment; numbers; significance.
- The first sentence of every paragraph states that paragraph's conclusion; read in a row, the
  first sentences tell the paper.
- General question first, the bloom case second.
- Argue each choice as: the obvious way -> why it fails here -> therefore this.
- Contributions name the new idea, not the amount of work.
- No coined jargon or internal code names; standard terms, explained once; no English
  abbreviations inside Chinese sentences except well-known ones (AUV, GPU).
- No defensive writing, no hedging chains, no replies to imagined reviewers; limitations in one
  short paragraph near the end.
- Present only results that carry a claim; numbers sparingly in the text, most in figures/tables.
- Formal connectives, not slogans.

## Attached
- facts.md (facts, numbers, setting, method, results)
- refs.bib (the only references you may cite)
- figures.md (figure files and what each shows)
- the current template files (main.tex, sections/*.tex)
