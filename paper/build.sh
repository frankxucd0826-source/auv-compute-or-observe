#!/usr/bin/env bash
# Build main.pdf: xelatex, bibtex, xelatex twice (latexmk's perl crashes on this machine).
cd "$(dirname "$0")" || exit 1
B=/c/texlive/2025/bin/windows
"$B/xelatex.exe" -interaction=nonstopmode -halt-on-error main.tex > build.log 2>&1 || { tail -30 build.log; exit 1; }
"$B/bibtex.exe" main >> build.log 2>&1
"$B/xelatex.exe" -interaction=nonstopmode -halt-on-error main.tex >> build.log 2>&1
"$B/xelatex.exe" -interaction=nonstopmode -halt-on-error main.tex >> build.log 2>&1 || { tail -30 build.log; exit 1; }
grep -E "Warning.*(undefined|multiply)" main.log | head
echo "built $(python -X utf8 -c "import fitz;print(fitz.open('main.pdf').page_count)") pages"
