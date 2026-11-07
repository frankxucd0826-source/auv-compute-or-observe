"""Assemble the revision-4 request: the brief, the facts, the figure notes, the names, both tables,
the references, the LaTeX template and the previous draft (as a source of wording only).
    python -E -X utf8 paper/gemini/build_prompt_rev4.py   -> paper/gemini/prompt_rev4.txt
"""
import sys
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PAPER))
from terms import CONTROLLER, STRATEGY, TRUTH, VEHICLE, VEHICLE_SUB  # noqa: E402


def terms_md():
    out = ["# Names to use exactly (strategies, controllers, vehicles, truth models)", ""]
    out += [f"- strategy {k}: {v}" for k, v in STRATEGY.items()]
    out += [f"- controller {k}: {v}" for k, v in CONTROLLER.items() if k not in STRATEGY]
    out += [f"- vehicle {k}: {VEHICLE[k]} ({VEHICLE_SUB[k]})" for k in VEHICLE]
    out += [f"- truth model {k}: {v}" for k, v in TRUTH.items()]
    out += ["- 留出海洋 = the 16 imagined oceans never used by the search; 搜索用海洋 = the 32 searched ones",
            "- 想象海洋 = one member of the vehicle's ensemble; 推演 = one route scored on one imagined ocean",
            "- 时间平均遗憾 = the score; 高功耗芯片 = the high-performance computer; 低功耗处理器 = the background one"]
    return "\n".join(out)


def main():
    parts = [("brief_rev4.md", (PAPER / "gemini/brief_rev4.md").read_text(encoding="utf-8")),
             ("facts_v2.md", (PAPER / "gemini/facts_v2.md").read_text(encoding="utf-8")),
             ("figures_rev4.md", (PAPER / "gemini/figures_rev4.md").read_text(encoding="utf-8")),
             ("terms.md", terms_md()),
             ("tables/settings.tex (Table 1)", (PAPER / "tables/settings.tex").read_text(encoding="utf-8")),
             ("tables/main_table.tex (Table 2, generated)", (PAPER / "tables/main_table.tex").read_text(encoding="utf-8")),
             ("refs.bib", (PAPER / "refs.bib").read_text(encoding="utf-8")),
             ("main.tex (template; do not change)", (PAPER / "main.tex").read_text(encoding="utf-8"))]
    for f in ["title", "abstract", "body", "appendix"]:
        parts.append((f"previous draft sections/{f}.tex (wording source only; superseded)",
                      (PAPER / f"sections/{f}.tex").read_text(encoding="utf-8")))
    text = "".join(f"\n\n########## ATTACHED FILE: {name} ##########\n\n{body}" for name, body in parts)
    out = PAPER / "gemini/prompt_rev4.txt"
    out.write_text(text, encoding="utf-8")
    print(out, len(text), "chars")


if __name__ == "__main__":
    main()
