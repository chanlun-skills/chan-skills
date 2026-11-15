# -*- coding: utf-8 -*-
"""缠师周末音乐会检索工具（零依赖，Python 3.8+）

用法示例:
  python search_music.py --stats
  python search_music.py --list
  python search_music.py --ep 5 [--full]
  python search_music.py --keyword 冬之旅 [--top 10]
  python search_music.py --replies --ep 12
  python search_music.py --replies --chan --top 20
  python search_music.py --replies --keyword 卡拉扬
  python search_music.py --topics
"""
import argparse
import csv
import os
import re
import sys

# 保证中文输出稳定
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "references")

DISCLAIMER = "\n[本内容为缠中说禅「网上周末音乐会」历史资料整理，仅作音乐文化学习研究之用，不构成任何投资建议]"


def read_csv(name):
    p = os.path.join(REF, "data", name)
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def episode_files():
    d = os.path.join(REF, "episodes")
    return sorted(os.listdir(d))


def ep_num(fname):
    m = re.match(r"(\d+)_", fname)
    return int(m.group(1)) if m else 0


def load_episodes():
    """{期号: (文件名, 正文)}"""
    eps = {}
    for f in episode_files():
        n = ep_num(f)
        with open(os.path.join(REF, "episodes", f), encoding="utf-8") as fh:
            eps[n] = (f, fh.read())
    return eps


def load_topics():
    d = os.path.join(REF, "topics")
    out = []
    for f in sorted(os.listdir(d)):
        with open(os.path.join(d, f), encoding="utf-8") as fh:
            out.append((f, fh.read()))
    return out


def print_ep_body(text, full=False):
    if full:
        print(text)
        return
    # 正文在 "## 原文" 与 "## 回复与交流" 标记之间
    m_start = re.search(r"\n## 原文\s*\n", text)
    m_end = re.search(r"\n## 回复", text)
    if m_start:
        body = text[m_start.end(): m_end.start() if m_end else m_start.end() + 1200]
        body = body.strip()
        print(body)
        if not m_end:
            print("\n……（本文件无回复段）")
    else:
        print(text[:1200])


def main():
    ap = argparse.ArgumentParser(description="缠师周末音乐会检索")
    ap.add_argument("--stats", action="store_true", help="总览统计")
    ap.add_argument("--list", action="store_true", help="42 期节目单列表")
    ap.add_argument("--ep", type=int, help="查看某期原文")
    ap.add_argument("--full", action="store_true", help="配合 --ep 输出完整原文（含回复）")
    ap.add_argument("--keyword", help="关键词检索（原文/专题/回复）")
    ap.add_argument("--replies", action="store_true", help="检索回复库")
    ap.add_argument("--chan", action="store_true", help="配合 --replies 只看缠师本人回复")
    ap.add_argument("--topics", action="store_true", help="音乐专题清单")
    ap.add_argument("--top", type=int, default=5, help="显示条数")
    args = ap.parse_args()

    idx = read_csv("索引.csv")

    if args.stats:
        total_rep = sum(int(x["回复数"] or 0) for x in idx)
        chan_rep = sum(int(x["缠师回复数"] or 0) for x in idx)
        people = sum(int(x["参与人数"] or 0) for x in idx)
        chars = sum(int(x["正文字数"] or 0) for x in idx)
        print(f"期数: {len(idx)} 期   正文合计: {chars:,} 字")
        print(f"时间范围: {idx[0]['发布日期']} ~ {idx[-1]['发布日期']}")
        print(f"回复合计: {total_rep:,} 条（索引统计），缠师回复 {chan_rep} 条，参与人次 {people:,}")
        replies = read_csv("全部回复.csv")
        chan_rows = [r for r in replies if r.get("是否缠师") == "是"]
        print(f"回复库实际条数: {len(replies):,}，其中缠师 {len(chan_rows)} 条")
        return

    if args.list:
        print(f"{'期号':>4}  {'日期':<10}  {'回复':>4}  标题")
        for x in idx:
            print(f"{x['期号']:>4}  {x['发布日期'][:10]:<10}  {x['回复数']:>4}  {x['标题']}")
        return

    if args.topics:
        meta = read_csv("音乐专题清单.csv")
        print(f"专题文章 {len(meta)} 篇:\n")
        for x in meta:
            print(f"◆ [{x['分类']}] {x['标题']}  ({x['日期']}, {x['正文字数']}字)")
        print("\n专题汇编文件: references/topics/ (compose/concert/cross/popular/prelude/vocal)")
        return

    eps = load_episodes()

    if args.ep:
        if args.ep not in eps:
            sys.exit(f"没有第 {args.ep} 期（范围 1~{max(eps)}）")
        row = next((x for x in idx if int(x["期号"]) == args.ep), None)
        if row:
            print(f"第 {args.ep} 期 | {row['发布日期']} | 回复 {row['回复数']} 条（缠师 {row['缠师回复数']}）")
            print(f"原帖: {row['原帖链接']}\n")
        fname, text = eps[args.ep]
        print_ep_body(text, full=args.full)
        print(DISCLAIMER)
        return

    if args.replies:
        replies = read_csv("全部回复.csv")
        rows = replies
        if args.ep:
            rows = [r for r in rows if r.get("期号", "").lstrip("0") == str(args.ep)]
        if args.chan:
            rows = [r for r in rows if r.get("是否缠师") == "是"]
        if args.keyword:
            kw = args.keyword
            rows = [r for r in rows if kw in (r.get("内容") or "") or kw in (r.get("期标题") or "")]
        rows.sort(key=lambda r: (int(r.get("期号") or 0), int(r.get("楼层") or 0)))
        print(f"命中 {len(rows)} 条回复（显示前 {args.top}）:\n")
        for r in rows[: args.top]:
            tag = "★缠师" if r.get("是否缠师") == "是" else "  "
            content = (r.get("内容") or "").strip().replace("\n", " ")
            print(f"{tag} 第{r.get('期号')}期 楼{r.get('楼层')} [{r.get('昵称')}] {r.get('时间')}")
            print(f"    {content[:200]}{'……' if len(content) > 200 else ''}\n")
        print(DISCLAIMER)
        return

    if args.keyword:
        kw = args.keyword
        hits = []
        for n, (fname, text) in eps.items():
            if kw in text:
                pos = text.find(kw)
                snippet = text[max(0, pos - 60): pos + 140].replace("\n", " ")
                hits.append((f"第{n}期", fname, snippet))
        for fname, text in load_topics():
            if kw in text:
                pos = text.find(kw)
                snippet = text[max(0, pos - 60): pos + 140].replace("\n", " ")
                hits.append(("专题", fname, snippet))
        arch = os.path.join(REF, "archive", "音乐与唱歌专题档案.md")
        if os.path.exists(arch):
            text = open(arch, encoding="utf-8").read()
            c = text.count(kw)
            if c:
                pos = text.find(kw)
                snippet = text[max(0, pos - 60): pos + 140].replace("\n", " ")
                hits.append(("唱歌专题", "音乐与唱歌专题档案.md", snippet + f"  [全库出现 {c} 次]"))
        print(f"关键词'{kw}' 命中 {len(hits)} 处（显示前 {args.top}）:\n")
        for src, fname, snippet in hits[: args.top]:
            print(f"◆ [{src}] {fname}")
            print(f"    …{snippet}…\n")
        print(DISCLAIMER)
        return

    # 无参数：默认输出 stats
    sys.argv.append("--stats")
    main()


if __name__ == "__main__":
    main()
