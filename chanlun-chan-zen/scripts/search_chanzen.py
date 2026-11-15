# -*- coding: utf-8 -*-
"""缠论佛学与禅宗检索工具（零依赖，Python 3.8+）

用法示例:
  python search_chanzen.py --stats
  python search_chanzen.py --cat "博客·禅宗专栏" --sub "教你打坐" --top 10
  python search_chanzen.py --keyword 打坐 --top 5
  python search_chanzen.py --date 2006-02-01
  python search_chanzen.py --from 2006-02-01 --to 2006-03-01 --top 10
  python search_chanzen.py --topics
  python search_chanzen.py --index --keyword 缘起 --top 5
"""
import argparse
import json
import os
import sys
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "references", "data")

DISCLAIMER = "\n[本内容为缠中说禅文字的历史资料整理，仅作哲学文化学习研究之用，不构成任何投资建议或宗教指导]"


def load_corpus():
    p = os.path.join(DATA, "corpus.json")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def load_index():
    p = os.path.join(DATA, "buddhist_index.json")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def norm_date(s):
    """'2006/2/1 10:16:25' -> (2006,2,1)"""
    m = re.match(r"(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})", s or "")
    if not m:
        return None
    return tuple(int(x) for x in m.groups())


def parse_arg_date(s):
    m = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})$", s or "")
    if not m:
        sys.exit(f"日期格式应为 YYYY-MM-DD: {s}")
    return tuple(int(x) for x in m.groups())


def fmt_date(s):
    m = re.match(r"(\d{4}/\d{1,2}/\d{1,2})", s or "")
    return m.group(1).replace("/", "-") if m else (s or "")[:10]


def print_item(it, max_len=400):
    print(f"◆ [{it['id']}] {it['title']}")
    print(f"  分类: {it['cat']} / {it['sub']}   日期: {fmt_date(it.get('date'))}")
    url = it.get("url") or ""
    if url:
        print(f"  原文: {url}")
    text = (it.get("text") or "").strip().replace("\n", " ")
    print(f"  摘要: {text[:max_len]}{'……' if len(text) > max_len else ''}")
    print()


def main():
    ap = argparse.ArgumentParser(description="缠论佛学与禅宗检索")
    ap.add_argument("--stats", action="store_true", help="语料总览统计")
    ap.add_argument("--cat", help="按一级分类过滤")
    ap.add_argument("--sub", help="按子系列过滤")
    ap.add_argument("--keyword", help="关键词（标题+正文模糊匹配）")
    ap.add_argument("--date", help="按日期检索 YYYY-MM-DD")
    ap.add_argument("--from", dest="dfrom", help="起始日期 YYYY-MM-DD")
    ap.add_argument("--to", dest="dto", help="结束日期 YYYY-MM-DD")
    ap.add_argument("--topics", action="store_true", help="列出佛学概念索引的词组大类")
    ap.add_argument("--index", action="store_true", help="在佛学概念索引中检索")
    ap.add_argument("--head", action="store_true", help="仅看系列首篇")
    ap.add_argument("--top", type=int, default=5, help="显示条数")
    args = ap.parse_args()

    corpus = load_corpus()

    if args.stats:
        import collections
        cats = collections.Counter(x["cat"] for x in corpus)
        subs = collections.Counter((x["cat"], x["sub"]) for x in corpus)
        chars = sum(len(x.get("text") or "") for x in corpus)
        dates = sorted(d for d in (norm_date(x.get("date")) for x in corpus) if d)
        print(f"总条数: {len(corpus)}   总字数: {chars:,}")
        print(f"时间范围: {dates[0]} ~ {dates[-1]}")
        print("\n== 一级分类 ==")
        for k, v in cats.most_common():
            c = sum(len(x.get("text") or "") for x in corpus if x["cat"] == k)
            print(f"  {k}: {v} 条 / {c:,} 字")
        print("\n== 子系列 ==")
        for (cat, sub), v in subs.most_common():
            print(f"  {cat} / {sub}: {v}")
        return

    if args.topics:
        idx = load_index()
        groups = {}
        for it in idx:
            for g, gv in (it.get("groups") or {}).items():
                if g not in groups:
                    groups[g] = {"n": 0, "words": set()}
                groups[g]["n"] += gv.get("n", 0)
                for w in (gv.get("words") or {}):
                    groups[g]["words"].add(w)
        print("== 佛学概念索引词组大类 ==")
        for g, gv in sorted(groups.items(), key=lambda kv: -kv[1]["n"]):
            ws = "、".join(sorted(gv["words"])[:12])
            print(f"  {g}: 覆盖 {gv['n']} 处   示例词: {ws}")
        return

    if args.index:
        kw = args.keyword
        idx = load_index()
        hits = {}
        for it in idx:
            for g, gv in (it.get("groups") or {}).items():
                for w, n in (gv.get("words") or {}).items():
                    if kw in w:
                        title = it.get("title") or it.get("path")
                        prev = hits.get(title)
                        # 同标题多路径（镜像副本）只保留最短规范路径，词频取最大
                        if prev is None or n > prev[3] or (
                            n == prev[3] and len(it.get("path") or "") < len(prev[0].get("path") or "")
                        ):
                            hits[title] = (it, g, w, n)
        merged = sorted(hits.values(), key=lambda x: -x[3])
        print(f"概念'{kw}' 命中 {len(merged)} 篇文档（显示前 {args.top}）:\n")
        for it, g, w, n in merged[: args.top]:
            print(f"◆ {it.get('title', it.get('path'))}")
            print(f"  文档: {it.get('path', '')}   命中词组: {g}/{w} ×{n}")
            print()
        return

    # 语料过滤
    rows = corpus
    if args.cat:
        rows = [x for x in rows if args.cat in x["cat"]]
    if args.sub:
        rows = [x for x in rows if args.sub in x["sub"]]
    if args.head:
        rows = [x for x in rows if x.get("is_head")]
    if args.date:
        d = parse_arg_date(args.date)
        rows = [x for x in rows if norm_date(x.get("date")) == d]
    if args.dfrom:
        d = parse_arg_date(args.dfrom)
        rows = [x for x in rows if (norm_date(x.get("date")) or (0,)) >= d]
    if args.dto:
        d = parse_arg_date(args.dto)
        rows = [x for x in rows if (norm_date(x.get("date")) or (9999,)) <= d]
    if args.keyword:
        kw = args.keyword
        rows = [x for x in rows if kw in (x.get("title") or "") or kw in (x.get("text") or "")]

    rows.sort(key=lambda x: (x.get("date") or "", x.get("id", 0)))
    print(f"命中 {len(rows)} 条（显示前 {args.top}）:\n")
    for it in rows[: args.top]:
        print_item(it)
    print(DISCLAIMER)


if __name__ == "__main__":
    main()
