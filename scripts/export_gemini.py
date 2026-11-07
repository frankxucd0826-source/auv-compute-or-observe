"""Export every exchange with Gemini (the writing model) as Markdown in chat/: for each round, what was
sent (the instruction line and every attached file, verbatim) and Gemini's reply, verbatim.

The prompts were assembled by paper/gemini/build_prompt*.py into prompt_*.txt; the replies were saved
as *_reply.md; rounds without a saved call log are dated by the reply file's time.

    python -E -X utf8 scripts/export_gemini.py  -> chat/Gemini对话记录_<k>_<round>.md
"""
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G = ROOT / "paper" / "gemini"
OUT = ROOT / "chat"
ROUNDS = [("draft1", "初稿"), ("rev1", "第 1 次修改"), ("rev2", "第 2 次修改"), ("rev3", "第 3 次修改"),
          ("rev3b", "第 3b 次修改"), ("rev4", "第 4 次修改（期刊论文格式）"), ("rev4b", "第 4b 次修改（压缩与改正）"),
          ("rev5", "第 5 轮：转向航路决策后的新论文"), ("rev5b", "第 5b 轮：新论文的修改"),
          ("rev6", "第 6 轮：补入随机合理场对照与湾流重复实验"),
          ("rev6b", "第 6b 轮：补入第三海区（阿古拉斯回流区）的预先写定检验"),
          ("rev6c", "第 6c 轮：补入改带真实卫星海流图的预先写定检验"),
          ("rev7", "第 7 轮：按各设置下都成立的结论改写摘要、引言与结论（被第 8 轮取代）"),
          ("rev8", "第 8 轮：全文润色——主线清晰、正面结果、标准术语、压缩篇幅")]


def fence(text):
    n = 3
    while "`" * n in text:
        n += 1
    return "`" * n


def main():
    OUT.mkdir(exist_ok=True)
    k = 0
    for tag, name in ROUNDS:
        prompt = G / f"prompt_{tag}.txt"
        reply = G / f"{tag}_reply.md"
        if not prompt.exists() or not reply.exists():
            continue
        k += 1
        log = G / f"{tag}_call.log"
        when = dt.datetime.fromtimestamp(reply.stat().st_mtime, dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        p, r = prompt.read_text(encoding="utf-8"), reply.read_text(encoding="utf-8")
        brief = G / f"brief_{tag}.md"
        lines = [f"# 与 Gemini 的对话记录 {k}：{name}", "",
                 f"时间（回复保存时间）：{when}。调用方式：Claude 用命令行工具 ask-gemini 把下面“发送内容”作为附件发给 Gemini，"
                 "并附一句简短指令（按附件中的写作要求完成各节）；回复原样存档后再由 Claude 核对数字与引用、拆分进论文各节。"
                 "下面两部分都是原文，未作删改。", ""]
        if log.exists():
            lines += ["调用记录：", "", "```", log.read_text(encoding="utf-8").strip(), "```", ""]
        if brief.exists():
            lines += [f"本轮的写作要求见下方发送内容里的附件 `brief_{tag}.md`。", ""]
        f1, f2 = fence(p), fence(r)
        lines += ["## 发送内容", "", "<details><summary>展开（共 %d 字符）</summary>" % len(p), "", f1, p.strip(), f1, "", "</details>", "",
                  "## Gemini 的回复", "", "<details><summary>展开（共 %d 字符）</summary>" % len(r), "", f2, r.strip(), f2, "", "</details>", ""]
        dst = OUT / f"Gemini对话记录_{k}_{tag}.md"
        dst.write_text("\n".join(lines), encoding="utf-8")
        print("wrote", dst.name, len("\n".join(lines)), "chars")


if __name__ == "__main__":
    main()
