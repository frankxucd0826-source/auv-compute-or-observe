"""Assemble the revision-5 request (a new paper on route decisions under a coarse current map): the
brief, the facts, the figure notes, the terms, both tables and the citation keys.
    python -E -X utf8 paper/gemini/build_prompt_rev5.py   -> paper/gemini/prompt_rev5.txt
"""
import re
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]


def main():
    bib = (PAPER / "refs.bib").read_text(encoding="utf-8")
    keys = []
    for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", bib, re.S):
        title = re.search(r"title\s*=\s*\{(.+?)\},?\n", m.group(2), re.S)
        keys.append(f"{m.group(1)}: {re.sub(r'[{}]', '', title.group(1)) if title else ''}")
    parts = [("brief_rev5.md", (PAPER / "gemini/brief_rev5.md").read_text(encoding="utf-8")),
             ("facts_v3.md", (PAPER / "gemini/facts_v3.md").read_text(encoding="utf-8")),
             ("figures_v5.md", (PAPER / "gemini/figures_v5.md").read_text(encoding="utf-8")),
             ("terms_v5.md", (PAPER / "gemini/terms_v5.md").read_text(encoding="utf-8")),
             ("tables/route_settings.tex (Table 1)", (PAPER / "tables/route_settings.tex").read_text(encoding="utf-8")),
             ("tables/route_scope.tex (Table 2)", (PAPER / "tables/route_scope.tex").read_text(encoding="utf-8")),
             ("citation keys in refs.bib (key: title)", "\n".join(keys))]
    text = "".join(f"\n\n########## ATTACHED FILE: {name} ##########\n\n{body}" for name, body in parts)
    out = PAPER / "gemini/prompt_rev5.txt"
    out.write_text(text, encoding="utf-8")
    print(out, len(text), "chars")


if __name__ == "__main__":
    main()
