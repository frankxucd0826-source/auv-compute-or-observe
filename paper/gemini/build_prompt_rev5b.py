"""Assemble the revision-5b request (tighten and correct draft 5): the brief, the facts, the terms and the
current section files.
    python -E -X utf8 paper/gemini/build_prompt_rev5b.py   -> paper/gemini/prompt_rev5b.txt
"""
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
FILES = ["title", "abstract", "intro", "related", "prior", "problem", "method", "experiments", "innovation",
         "conclusion", "appendix"]


def main():
    parts = [("brief_rev5b.md", (PAPER / "gemini/brief_rev5b.md").read_text(encoding="utf-8")),
             ("facts_v3.md", (PAPER / "gemini/facts_v3.md").read_text(encoding="utf-8")),
             ("terms_v5.md", (PAPER / "gemini/terms_v5.md").read_text(encoding="utf-8"))]
    for f in FILES:
        parts.append((f"sections/{f}.tex (draft 5 after Claude's corrections, to be edited)",
                      (PAPER / f"sections/{f}.tex").read_text(encoding="utf-8")))
    text = "".join(f"\n\n########## ATTACHED FILE: {name} ##########\n\n{body}" for name, body in parts)
    out = PAPER / "gemini/prompt_rev5b.txt"
    out.write_text(text, encoding="utf-8")
    print(out, len(text), "chars")


if __name__ == "__main__":
    main()
