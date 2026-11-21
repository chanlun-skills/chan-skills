#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 docs/*.md 转成同风格的 HTML，供 GitHub Pages 渲染。

背景：仓库启用了 .nojekyll（跳过 Jekyll 处理，避免文件名/目录名被 Jekyll 改写），
因此 .md 文件在 Pages 上会以纯文本下载。用本脚本生成对应的 .html 页面。

用法：
    python scripts/md2html.py                # 转换 docs/ 下所有 .md
    python scripts/md2html.py docs/xxx.md   # 只转换指定文件

仅用标准库，无第三方依赖。
"""

import html
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")

# 与 docs/index.html、docs/join.html 保持同一套配色
PAGE_CSS = """
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    font-family:"Microsoft YaHei","PingFang SC",-apple-system,sans-serif;
    background:linear-gradient(160deg,#f5f6fa 0%,#eef0f7 100%);
    color:#2c2c2a; line-height:1.85; padding:34px 16px 60px;
  }
  .wrap { max-width:820px; margin:0 auto; }
  .card {
    background:#fff; border-radius:16px; padding:34px 40px;
    box-shadow:0 2px 20px rgba(38,33,92,.07); border:1px solid rgba(0,0,0,.06);
  }
  header { text-align:center; margin-bottom:26px; padding-bottom:20px; border-bottom:1px solid rgba(0,0,0,.07); }
  header .logo { width:52px; height:52px; border-radius:13px; margin:0 auto 12px; display:block; }
  h1 { font-size:22px; color:#26215c; font-weight:600; letter-spacing:.5px; }
  .sub { font-size:13px; color:#8a8a84; margin-top:6px; }
  h1, h2, h3 { color:#26215c; font-weight:600; }
  h1 { font-size:22px; margin:26px 0 14px; }
  h2 { font-size:18px; margin:30px 0 12px; padding-left:11px; border-left:4px solid #534ab7; }
  h3 { font-size:15.5px; color:#3c3489; margin:20px 0 8px; }
  p { font-size:14.5px; margin-bottom:12px; }
  ul, ol { padding-left:26px; font-size:14.5px; margin-bottom:12px; }
  li { margin-bottom:8px; }
  hr { border:none; border-top:1px solid rgba(0,0,0,.09); margin:26px 0; }
  blockquote {
    background:#e6f1fb; border-left:4px solid #185fa5; padding:12px 16px;
    border-radius:0 8px 8px 0; font-size:13.5px; color:#0c447c; margin:16px 0;
  }
  blockquote p { margin-bottom:0; font-size:13.5px; color:#0c447c; }
  table { width:100%; border-collapse:collapse; font-size:13.5px; margin:14px 0; }
  th { background:#eeedfe; color:#3c3489; text-align:left; padding:10px 12px; font-weight:600; }
  td { padding:10px 12px; border-bottom:1px solid rgba(0,0,0,.07); vertical-align:top; }
  tr:last-child td { border-bottom:none; }
  code { background:#f0effb; padding:2px 7px; border-radius:5px; font-family:Consolas,monospace; font-size:13px; color:#3c3489; }
  strong { color:#26215c; }
  em { color:#6b6b66; }
  .back { display:block; text-align:center; margin-top:26px; font-size:13px; color:#5a54a8; text-decoration:none; }
  .back:hover { text-decoration:underline; }
  footer { text-align:center; font-size:12px; color:#9a9a94; margin-top:26px; line-height:2; }
  footer a { color:#5a54a8; text-decoration:none; }
"""


def inline(text: str) -> str:
    """行内标记：**粗体**、`代码`、*斜体*、链接。"""
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
        r'<a href="\2" target="_blank" rel="noopener">\1</a>',
        text,
    )
    return text


def is_table_sep(line: str) -> bool:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells)


def split_row(line: str):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def convert(md: str, skip_first_h1: bool = False) -> str:
    lines = md.split("\n")
    out = []
    i = 0
    n = len(lines)
    dropped_h1 = False

    while i < n:
        raw = lines[i]
        line = raw.strip()

        # 空行
        if not line:
            i += 1
            continue

        # 分隔线
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", line):
            out.append("<hr>")
            i += 1
            continue

        # 标题
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lvl = len(m.group(1))
            # 页面头部已展示标题，markdown 的首个一级标题跳过，避免两个 h1
            if lvl == 1 and skip_first_h1 and not dropped_h1:
                dropped_h1 = True
                i += 1
                continue
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue

        # 引用块
        if line.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            body = " ".join(x for x in buf if x)
            out.append(f"<blockquote><p>{inline(body)}</p></blockquote>")
            continue

        # 表格
        if "|" in line and i + 1 < n and is_table_sep(lines[i + 1]):
            head = split_row(line)
            out.append("<table>")
            out.append(
                "<tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr>"
            )
            i += 2
            while i < n and "|" in lines[i] and lines[i].strip():
                cells = split_row(lines[i])
                # 补齐列数，避免错位
                while len(cells) < len(head):
                    cells.append("")
                out.append(
                    "<tr>"
                    + "".join(f"<td>{inline(c)}</td>" for c in cells[: len(head)])
                    + "</tr>"
                )
                i += 1
            out.append("</table>")
            continue

        # 有序列表
        if re.match(r"^\d+\.\s+", line):
            out.append("<ol>")
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                item = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                out.append(f"<li>{inline(item)}</li>")
                i += 1
            out.append("</ol>")
            continue

        # 无序列表
        if re.match(r"^[-*+]\s+", line):
            out.append("<ul>")
            while i < n and re.match(r"^[-*+]\s+", lines[i].strip()):
                item = re.sub(r"^[-*+]\s+", "", lines[i].strip())
                out.append(f"<li>{inline(item)}</li>")
                i += 1
            out.append("</ul>")
            continue

        # 普通段落（连续非空行合并）
        buf = [line]
        i += 1
        while i < n and lines[i].strip() and not re.match(
            r"^(#{1,6}\s|>\s|\d+\.\s|[-*+]\s|-{3,}$)", lines[i].strip()
        ) and not ("|" in lines[i] and i + 1 < n and is_table_sep(lines[i + 1])):
            buf.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(buf))}</p>")

    return "\n".join(out)


def build_page(title: str, body: str, desc: str = "") -> str:
    meta = ""
    if desc:
        meta = (
            f'\n<meta name="description" content="{html.escape(desc, quote=True)}">'
        )
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>{meta}
<link rel="icon" href="images/banner-logo.png">
<style>{PAGE_CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <header>
      <img class="logo" src="images/banner-logo.png" alt="缠论 Skills">
      <h1>{html.escape(title)}</h1>
      <p class="sub">chanlun-skills · 内容仅供学习研究，不构成投资建议</p>
    </header>
{body}
    <a class="back" href="index.html">← 返回首页</a>
  </div>
  <footer>
    <a href="https://github.com/chanlun-skills/chan-skills">GitHub 主仓库</a> ·
    <a href="https://gitee.com/chanlun-skills/chan-skills">Gitee 镜像</a> ·
    <a href="index.html">首页</a><br>
    市场有风险，决策需独立判断，风险自担
  </footer>
</div>
</body>
</html>
"""


def main(argv):
    if len(argv) > 1:
        targets = [os.path.abspath(a) for a in argv[1:]]
    else:
        if not os.path.isdir(DOCS):
            print("[md2html] 找不到 docs/ 目录")
            return 1
        targets = [
            os.path.join(DOCS, f)
            for f in sorted(os.listdir(DOCS))
            if f.endswith(".md")
        ]

    if not targets:
        print("[md2html] 没有需要转换的 .md 文件")
        return 0

    for src in targets:
        if not src.endswith(".md"):
            continue
        if not os.path.isfile(src):
            print(f"[md2html] 跳过（不存在）：{src}")
            continue
        with open(src, "r", encoding="utf-8") as f:
            md = f.read()

        # 标题：取第一个一级标题；描述：取第一个引用块
        m = re.search(r"^#\s+(.+)$", md, re.M)
        title = m.group(1).strip() if m else os.path.basename(src)[:-3]
        bq = re.search(r"^>\s*(.+)$", md, re.M)
        desc = bq.group(1).strip() if bq else ""

        body = convert(md, skip_first_h1=True)
        dst = src[:-3] + ".html"
        with open(dst, "w", encoding="utf-8", newline="\n") as f:
            f.write(build_page(title, body, desc))

        print(f"[md2html] {os.path.relpath(src, REPO)}  ->  "
              f"{os.path.relpath(dst, REPO)}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
