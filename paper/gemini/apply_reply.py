"""Split a Gemini reply into the paper's files. Two layouts are understood:
  ===== FILE: <path> =====  followed by the file's text (optionally in a code fence), or
  a heading line naming the file in backticks (e.g. ### `sections/body.tex`) followed by a code fence.
Keeps a copy of every file it replaces under gemini/backup/<stamp>/.
    python -E -X utf8 paper/gemini/apply_reply.py paper/gemini/draft1_reply.md
"""
import re
import shutil
import sys
import time
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]


def split(text):
    parts = re.split(r"^=====\s*FILE:\s*(.+?)\s*=====\s*$", text, flags=re.M)
    if len(parts) > 1:
        out = []
        for k in range(1, len(parts), 2):
            body = parts[k + 1].strip()
            body = re.sub(r"^```[a-zA-Z]*\s*\n", "", body)
            body = re.sub(r"\n```\s*$", "", body)
            out.append((parts[k].strip().strip("`"), body))
        return out
    pat = re.compile(r"^#+\s*`([^`]+\.(?:tex|md))`\s*$\n+```[a-zA-Z]*\s*\n(.*?)\n```\s*$", re.M | re.S)
    return [(m.group(1).strip(), m.group(2).strip()) for m in pat.finditer(text)]


def main():
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    files = split(text)
    for rel, body in files:
        dst = PAPER / rel
        if dst.exists():
            bk = PAPER / "gemini" / "backup" / stamp / rel
            bk.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dst, bk)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(body + "\n", encoding="utf-8")
        print("wrote", rel, len(body), "chars")
    if not files:
        print("no file markers found")


if __name__ == "__main__":
    main()
