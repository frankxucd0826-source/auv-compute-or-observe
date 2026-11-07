"""Export this project's Claude Code conversation(s) as readable Markdown for the course
repository: the user's messages in full, the assistant's replies in full, each tool call as one
line, tool results shortened. Parts the author chose not to publish are left out: a user message
matching a line of private/skip_turns.txt (one regular expression per line) starts an omitted
stretch, which lasts until a user message containing a marker from private/cut_markers.txt;
of that message only the text after the marker is published.

Omitted: tool calls and results that touch other projects (their memory or files may contain an
unpublished paper), the text of the research skill that was loaded, and the automatic summaries
written when the conversation was compacted. Timed reminders and background-task notices are
labelled as such, so they are not mistaken for the user's words.

Other projects are recognised from the folder names under ~/.claude/projects (all except this
project's own) plus the patterns below; extra private patterns, one regular expression per line,
can be put in private/redact_extra.txt (not published).

    python -E -X utf8 scripts/export_chat.py <session.jsonl> [...] -> chat/对话记录_<n>.md
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "chat"
HERE = Path(sys.argv[1]).parent.name if len(sys.argv) > 1 else ""
MAX_RESULT = 1200


def build_rename():
    """Names of other projects in the assistant's replies are replaced by a neutral phrase; the
    patterns (one per line: regular expression, a tab, the replacement) are kept in
    private/rename_extra.txt, which is not published."""
    f = ROOT / "private" / "rename_extra.txt"
    out = []
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if "\t" in line:
                pat, rep = line.split("\t", 1)
                out.append((re.compile(pat), rep))
    return out


def build_redact():
    pats = [r"C--Users-xcd-AppData"]     # further patterns: private/redact_extra.txt
    projects = Path.home() / ".claude" / "projects"
    for d in projects.iterdir() if projects.exists() else []:
        if d.is_dir() and d.name != HERE:
            pats.append(r"(?<![\w-])" + re.escape(d.name) + r"(?![\w-])")
    extra = ROOT / "private" / "redact_extra.txt"
    if extra.exists():
        pats += [l.strip() for l in extra.read_text(encoding="utf-8").splitlines() if l.strip()]
    return re.compile("|".join(pats), re.I)


def build_skip():
    f = ROOT / "private" / "skip_turns.txt"
    if not f.exists():
        return []
    return [re.compile(l.strip()) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]


def build_cut():
    """Markers (one per line in private/cut_markers.txt): of a user message containing one, only
    the text after it is published."""
    f = ROOT / "private" / "cut_markers.txt"
    if not f.exists():
        return []
    return [l.strip() for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]


def build_omit():
    """Tool calls whose input or output matches a line of private/omit_calls.txt (one regular
    expression per line) are published only as an omission note: they displayed text from the parts
    of the conversation the author chose not to publish."""
    f = ROOT / "private" / "omit_calls.txt"
    if not f.exists():
        return None
    pats = [l.strip() for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    return re.compile("|".join(pats)) if pats else None


REDACT = None
OMIT = None
RENAME = []
SKIP = []
CUT = []


def rename(txt):
    for pat, rep in RENAME:
        txt = pat.sub(rep, txt)
    return txt


def text_of(content):
    if isinstance(content, str):
        return content
    return "\n".join(c["text"] for c in content or [] if c.get("type") == "text")


def tool_line(c):
    name = c.get("name", "")
    inp = c.get("input", {})
    if OMIT is not None and OMIT.search(json.dumps(inp, ensure_ascii=False)):
        return f"**{name}**：[已省略]"
    if REDACT.search(json.dumps(inp, ensure_ascii=False)):
        desc = rename(inp.get("description", ""))
        return f"**{name}**（{desc}）：[涉及其他项目，已省略]" if desc else f"**{name}**：[涉及其他项目，已省略]"
    if name in ("Bash", "PowerShell"):
        desc = inp.get("description", "")
        cmd = inp.get("command", "").strip().splitlines()[0][:160] if inp.get("command") else ""
        return f"**{name}**（{desc}）：`{cmd}`"
    if name in ("Read", "Write", "Edit"):
        return f"**{name}** `{inp.get('file_path', '')}`"
    if name == "WebSearch":
        return f"**WebSearch** {inp.get('query', '')}"
    if name == "WebFetch":
        return f"**WebFetch** {inp.get('url', '')}"
    keys = ", ".join(f"{k}" for k in list(inp)[:4])
    return f"**{name}**（{keys}）"


def result_text(c):
    content = c.get("content")
    if isinstance(content, list):
        return "\n".join(x.get("text", "") for x in content if isinstance(x, dict) and x.get("type") == "text")
    return str(content or "")


def user_block(s, stamp):
    """Heading and text for a user-role message that is not a tool result."""
    if s.startswith("This session is being continued from a previous conversation"):
        return f"## 上下文压缩（{stamp} UTC）", "[对话过长，系统自动把前文压缩成摘要后继续；摘要是前文的重复，已省略]"
    if s.startswith("Base directory for this skill:"):
        return f"## 载入研究技能（{stamp} UTC）", "[载入本机的研究流程说明（ocean-autoresearch），全文省略]"
    if s.startswith("（自动续跑提醒"):
        return f"## 定时提醒（{stamp} UTC，助手自己设的定时任务，不是用户输入）", rename(s)
    if s.startswith("[Request interrupted by user"):
        return f"## 中断（{stamp} UTC）", "[用户中断了助手当时的输出]"
    if s.startswith("[Image:"):
        return f"## 图片（{stamp} UTC，助手查看渲染图时的工具输出，不是用户输入）", "[图片省略]"
    if s.startswith("<task-notification>"):
        m = re.search(r"<summary>(.*?)</summary>", s, re.S)
        return f"## 后台任务通知（{stamp} UTC，自动）", (m.group(1).strip() if m else "[后台任务结束]")
    return f"## 用户（{stamp} UTC）", s


def export(path, k, state):
    """state carries over between the session files of one conversation (given in time order):
    rows a resumed session copied from an earlier file are written only once, and an omitted
    turn that spans two files stays omitted."""
    lines = [f"# 对话记录 {k}", "", f"来源：`{Path(path).name}`（Claude Code 桌面版会话）。收录的用户消息与助手回复均为原文"
             "（助手回复中提到的其他项目名称改写为“另一研究会话/项目”）；工具调用只列一行，工具输出截短；"
             "涉及其他项目（含未发表论文）的工具调用与输出已省略。"
             + ("会话中断后续接时，新会话文件开头复制了上一份记录的内容，复制部分不重复收录。" if k > 1 else ""), ""]
    pending = {}
    skipping = state["skipping"]
    for raw in open(path, encoding="utf-8"):
        d = json.loads(raw)
        u = d.get("uuid")
        if u:
            if u in state["seen"]:
                continue
            state["seen"].add(u)
        t = d.get("type")
        stamp = d.get("timestamp", "")[:16].replace("T", " ")
        if t == "user":
            content = d.get("message", {}).get("content")
            if isinstance(content, list) and any(c.get("type") == "tool_result" for c in content):
                if skipping:
                    continue
                for c in content:
                    if c.get("type") != "tool_result":
                        continue
                    call = pending.pop(c.get("tool_use_id"), "")
                    s = result_text(c)
                    if REDACT.search(call) or REDACT.search(s):
                        s = "[已省略：涉及其他项目的记忆或文件]"
                    elif OMIT is not None and (OMIT.search(call) or OMIT.search(s)):
                        s = "[已省略]"
                    s = s.strip()
                    if len(s) > MAX_RESULT:
                        s = s[:MAX_RESULT] + f"\n…（截短，原文 {len(s)} 字符）"
                    if s:
                        lines += ["", "<details><summary>工具输出</summary>", "", "```", s, "```", "", "</details>"]
                continue
            s = text_of(content).strip()
            if "<system-reminder>" in s:
                s = re.sub(r"<system-reminder>.*?</system-reminder>", "", s, flags=re.S).strip()
            resume = False
            if d.get("isCompactSummary") or s.startswith("This session is being continued from a previous conversation"):
                if not skipping:        # the summary repeats earlier text (and may quote a marker): never cut or publish it
                    lines += ["", "---", "", *user_block("This session is being continued from a previous conversation", stamp)[:1], "",
                              user_block("This session is being continued from a previous conversation", stamp)[1]]
                continue
            for mk in CUT:
                if mk in s:
                    s, resume = s.split(mk, 1)[1].strip(), True
            if not s:
                continue
            head, body = user_block(s, stamp)
            if head.startswith("## 用户"):
                if resume:
                    skipping = False
                elif any(p.match(s) for p in SKIP):
                    skipping = True
            if skipping:
                continue
            lines += ["", "---", "", head, "", body]
        elif t == "assistant" and not skipping:
            for c in d.get("message", {}).get("content", []) or []:
                if c.get("type") == "text" and c.get("text", "").strip():
                    lines += ["", f"**助手**：{rename(c['text'].strip())}"]
                elif c.get("type") == "tool_use":
                    pending[c.get("id")] = json.dumps(c.get("input", {}), ensure_ascii=False)
                    lines += ["", "- " + tool_line(c)]
    state["skipping"] = skipping
    OUT.mkdir(exist_ok=True)
    dst = OUT / f"对话记录_{k}.md"
    dst.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", dst, len(lines), "lines")


if __name__ == "__main__":
    REDACT = build_redact()
    OMIT = build_omit()
    RENAME = build_rename()
    SKIP = build_skip()
    CUT = build_cut()
    state = dict(seen=set(), skipping=False)
    for k, p in enumerate(sys.argv[1:], 1):
        export(p, k, state)
