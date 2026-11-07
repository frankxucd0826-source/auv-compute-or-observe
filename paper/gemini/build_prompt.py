"""Assemble one Gemini request: the brief first, then the facts, figure notes, terms, the generated
table, the references, the template and the current section files, each marked as an attached file.
    python -E -X utf8 paper/gemini/build_prompt.py gemini/brief_rev2.md gemini/prompt_rev2.txt
(paths relative to paper/)
"""
import sys
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]


def main():
    brief, out = sys.argv[1], sys.argv[2]
    parts = [(Path(brief).name, PAPER / brief), ("facts.md", PAPER / "facts.md"), ("figures.md", PAPER / "gemini/figures.md"),
             ("terms.md", PAPER / "terms.md"), ("tables/main_table.tex (generated)", PAPER / "tables/main_table.tex"),
             ("refs.bib", PAPER / "refs.bib"), ("main.tex (template)", PAPER / "main.tex")]
    for f in ["title", "subtitle", "abstract", "body", "appendix"]:
        parts.append((f"sections/{f}.tex (current draft)", PAPER / f"sections/{f}.tex"))
    text = "".join(f"\n\n########## ATTACHED FILE: {name} ##########\n\n" + p.read_text(encoding="utf-8") for name, p in parts)
    (PAPER / out).write_text(text, encoding="utf-8")
    print(out, len(text), "chars")


if __name__ == "__main__":
    main()
