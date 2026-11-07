"""Mechanical checks of a revision-6 draft before reading it: numbers that do not occur in
facts_v3.md / facts_v4.md / figures_v5.md / the tables, figures/tables/citations that are missing, English
abbreviations in the Chinese text, stray Japanese or traditional characters, the first sentence of
every paragraph, and the Chinese character count of the body.
    python -E -X utf8 paper/gemini/check_draft6.py
"""
import re
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
BODY = ["intro", "related", "prior", "problem", "method", "experiments", "innovation", "conclusion"]
FILES = ["title", "abstract"] + BODY + ["appendix"]
ABBR = r"\b(AUV|GPU|EAKF|CEM|JEPA|RMSE|VOC|VOI|UCB|SST|CPU|LLM|ADCP|DVL|PINN|EVSI|EVPI|ROC|AUC|km|h)\b"


def numbers_in(text):
    return set(re.findall(r"(?<![\w.])\d+(?:\.\d+)?", text))


def main():
    bib = (PAPER / "refs.bib").read_text(encoding="utf-8")
    keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    figs = {p.stem for p in (PAPER / "figures").glob("fig_*.p*")}
    facts = "".join((PAPER / p).read_text(encoding="utf-8") for p in
                    ("gemini/facts_v3.md", "gemini/facts_v4.md", "gemini/figures_v5.md", "tables/route_settings.tex", "tables/route_scope.tex"))
    known = numbers_in(facts) | {str(k) for k in range(0, 13)} | {"2026", "2025", "2024", "2023", "2022", "2021", "2020",
                                                                    "2019", "1959", "1967", "2016", "2018", "90", "95", "20", "100"}
    total = 0
    for f in FILES:
        p = PAPER / "sections" / f"{f}.tex"
        if not p.exists():
            print("MISSING", f)
            continue
        t = p.read_text(encoding="utf-8")
        plain = re.sub(r"\\(cite|ref|label|includegraphics|input|url)(\[[^\]]*\])?\{[^}]*\}", "", t)
        body = re.sub(r"\\caption\{.*?\}\s*\\label", "", plain, flags=re.S)
        body = re.sub(r"\\begin\{(table|algorithm)\}.*?\\end\{\1\}", "", body, flags=re.S)
        cjk = len(re.findall(r"[\u4e00-\u9fff]", body))
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
        for m in re.finditer(r"[\u3040-\u30ff]+|[過這個們說來對時會後還與為當開發點應實際體驗於並從無則經設計]", t):
            a = max(0, m.start() - 15)
            print("  !! stray Japanese/traditional character:", m.group(0), "|", t[a:m.end() + 10].replace("\n", " "))
        for m in re.finditer(ABBR, re.sub(r"\\cite\{[^}]*\}|\$[^$]*\$|\\url\{[^}]*\}", "", t)):
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
    print(f"\nbody Chinese characters (sections 1-8, without captions, tables, algorithm): {total}")


if __name__ == "__main__":
    main()
