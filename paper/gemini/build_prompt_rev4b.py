"""Assemble the revision-4b request (tighten and correct draft 4): the brief, the facts, the figure
notes, the names, both tables, the reference keys and the current draft-4 section files.
    python -E -X utf8 paper/gemini/build_prompt_rev4b.py   -> paper/gemini/prompt_rev4b.txt
"""
import re
import sys
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PAPER / "gemini"))
from build_prompt_rev4 import terms_md  # noqa: E402


def main():
    bib = (PAPER / "refs.bib").read_text(encoding="utf-8")
    keys = "\n".join(re.findall(r"@\w+\{([^,]+),", bib))
    parts = [("brief_rev4b.md", (PAPER / "gemini/brief_rev4b.md").read_text(encoding="utf-8")),
             ("facts_v2.md", (PAPER / "gemini/facts_v2.md").read_text(encoding="utf-8")),
             ("figures_rev4.md", (PAPER / "gemini/figures_rev4.md").read_text(encoding="utf-8")),
             ("terms.md", terms_md()),
             ("tables/settings.tex (Table 1)", (PAPER / "tables/settings.tex").read_text(encoding="utf-8")),
             ("tables/main_table.tex (Table 2)", (PAPER / "tables/main_table.tex").read_text(encoding="utf-8")),
             ("citation keys in refs.bib", keys)]
    for f in ["title", "abstract", "intro", "related", "problem", "method", "experiments", "conclusion", "appendix"]:
        parts.append((f"sections/{f}.tex (draft 4, to be edited)", (PAPER / f"sections/{f}.tex").read_text(encoding="utf-8")))
    text = "".join(f"\n\n########## ATTACHED FILE: {name} ##########\n\n{body}" for name, body in parts)
    out = PAPER / "gemini/prompt_rev4b.txt"
    out.write_text(text, encoding="utf-8")
    print(out, len(text), "chars")


if __name__ == "__main__":
    main()
