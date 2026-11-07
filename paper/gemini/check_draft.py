"""Mechanical checks of a draft before reading it (revision 4 layout): numbers that do not occur in
facts_v2.md, figures/tables/citations that are missing, English abbreviations in the Chinese text,
\\TBD placeholders, the first sentence of every paragraph, and the Chinese character count.
    python -E -X utf8 paper/gemini/check_draft.py
"""
import re
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
BODY = ["intro", "related", "problem", "method", "experiments", "conclusion"]
FILES = ["title", "abstract"] + BODY + ["appendix"]
ABBR = r"\b(AUV|GPU|EAKF|CEM|JEPA|RMSE|VOC|VOI|UCB|SST|DINEOF|ERDDAP|MUR|CPU|LLM)\b"


def numbers_in(text):
    return set(re.findall(r"(?<![\w.])\d+(?:\.\d+)?", text))


def main():
    bib = (PAPER / "refs.bib").read_text(encoding="utf-8")
    keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    figs = {p.stem for p in (PAPER / "figures").glob("fig_*.p*")}
    facts = (PAPER / "gemini" / "facts_v2.md").read_text(encoding="utf-8") + \
        (PAPER / "gemini" / "figures_rev4.md").read_text(encoding="utf-8") + \
        (PAPER / "tables" / "main_table.tex").read_text(encoding="utf-8") + \
        (PAPER / "tables" / "settings.tex").read_text(encoding="utf-8")
    known = numbers_in(facts) | {str(k) for k in range(0, 13)} | {"2026", "2025", "2024", "2023", "2022", "2021",
                                                                    "2020", "2019", "2018", "2011", "1991", "100", "20",
                                                                    "24", "48", "32", "16", "50", "30", "45", "15"}
    total = 0
    for f in FILES:
        p = PAPER / "sections" / f"{f}.tex"
        if not p.exists():
            print("MISSING", f)
            continue
        t = p.read_text(encoding="utf-8")
        plain = re.sub(r"\\(cite|ref|label|includegraphics|input)(\[[^\]]*\])?\{[^}]*\}", "", t)
        cjk = len(re.findall(r"[\u4e00-\u9fff]", re.sub(r"\\caption\{.*?\}\s*\\label", "", plain, flags=re.S)))
        if f in BODY:
            total += cjk
        print(f"\n######## {f}: {cjk} Chinese characters")
        for k in re.findall(r"\\cite[pt]?\{([^}]+)\}", t):
            for key in k.split(","):
                if key.strip() not in keys:
                    print("  !! unknown citation", key.strip())
        for g in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", t):
            if Path(g).stem not in figs:
                print("  !! missing figure", g)
        for m in re.finditer(r"\\TBD\{([^}]*)\}", t):
            print("  TBD:", m.group(1))
        for m in re.finditer(r"[\u3040-\u30ff]+|[過這個們說來對時會後還與為當開發點應實際體驗於並從無則經設計]", t):
            a = max(0, m.start() - 15)
            print("  !! stray Japanese/traditional character:", m.group(0), "|", t[a:m.end() + 10].replace("\n", " "))
        for m in re.finditer(ABBR, re.sub(r"\\cite\{[^}]*\}|\$[^$]*\$", "", t)):
            a = max(0, m.start() - 20)
            print("  !! abbreviation:", m.group(0), "|", t[a:m.end() + 10].replace("\n", " "))
        for m in re.finditer(r"(?<![\w.\\{])(\d+(?:\.\d+)?)", plain):
            if m.group(1) not in known:
                a, b = max(0, m.start() - 30), min(len(plain), m.end() + 12)
                print("  ?? number not in facts:", m.group(1), "|", plain[a:b].replace("\n", " "))
        if f in BODY or f == "abstract":
            print("  -- first sentences --")
            for para in re.split(r"\n\s*\n", t):
                para = para.strip()
                if not para or (para.startswith("\\") and not para.startswith("\\textbf")):
                    continue
                print("   *", re.split(r"(?<=[。！？])", para)[0][:110])
    print(f"\nbody Chinese characters (sections 1-6, without captions): {total}")


if __name__ == "__main__":
    main()
