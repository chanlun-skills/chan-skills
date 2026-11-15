#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chanlun-jiexpan 检索工具

对缠论大盘解盘历史库的 JSON 数据做本地检索，无第三方依赖。

用法示例:
    python search_jiexpan.py --stats                          # 库统计
    python search_jiexpan.py --date 2007-05-30                # 某日解盘
    python search_jiexpan.py --from 2007-10-01 --to 2007-10-31
    python search_jiexpan.py --year 2008 --top 15             # 按年份
    python search_jiexpan.py --keyword 小康跌幅               # 全文检索
    python search_jiexpan.py --keyword 比例线 --year 2007     # 组合过滤
    python search_jiexpan.py --key-periods                    # 六个关键时段
    python search_jiexpan.py --catalog --relevance 高         # 文库目录
"""
import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, os.pardir, "references", "data")

TIMELINE = os.path.join(DATA, "timeline.json")
POSTS = os.path.join(DATA, "market_posts.json")
KEY = os.path.join(DATA, "key_periods.json")
CATALOG_GLOB = os.path.join(DATA, "library_catalog", "batch_*.json")

DISCLAIMER = (
    "\n[免责声明] 本工具仅检索 2006-2008 年历史解盘内容，用于缠论技术理论学习与历史复盘，"
    "不构成任何投资建议，不提供当前或未来市场走势判断。市场有风险，决策需独立判断，风险自担。"
)


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def norm_date(s):
    """统一为 YYYY-MM-DD（容忍 2007/05/30、2007-05-30 15:28 等写法）。"""
    s = str(s or "").strip().replace("/", "-")
    return s[:10]


def excerpt(text, limit=140):
    text = " ".join(str(text or "").split())
    return text[:limit] + ("……" if len(text) > limit else "")


def print_doc(idx, title, dt, src, text):
    print("-" * 72)
    print(f"[{idx}] {title}")
    print(f"    日期: {dt}  来源: {src}")
    print(f"    {excerpt(text)}")


def in_range(d, args):
    if args.date and d != norm_date(args.date):
        return False
    if args.year and not d.startswith(str(args.year)):
        return False
    if args.frm and d < norm_date(args.frm):
        return False
    if args.to and d > norm_date(args.to):
        return False
    return True


def catalog_val(rec, key):
    """文库目录记录为 Notion 导出风格，字段值是嵌套 dict，安全取文本。"""
    v = rec.get(key, "")
    if isinstance(v, dict):
        if "text" in v:
            return str(v["text"])
        if "date" in v:
            return str(v["date"])
        if "select" in v:
            return str(v["select"])
        if "multi_select" in v:
            return " / ".join(map(str, v["multi_select"]))
        if "number" in v:
            return str(v["number"])
        if "url" in v and isinstance(v["url"], dict):
            return str(v["url"].get("link", ""))
    return str(v)


def main():
    ap = argparse.ArgumentParser(description="缠论大盘解盘检索")
    ap.add_argument("--stats", action="store_true", help="库统计")
    ap.add_argument("--date", help="精确日期（YYYY-MM-DD）")
    ap.add_argument("--frm", dest="frm", help="起始日期（含）")
    ap.add_argument("--to", help="结束日期（含）")
    ap.add_argument("--year", type=int, help="按年份过滤")
    ap.add_argument("--keyword", help="标题+正文关键词检索")
    ap.add_argument("--title", help="仅标题关键词检索")
    ap.add_argument("--src", choices=["official", "mirror"], help="按来源渠道过滤（市场帖）")
    ap.add_argument("--key-periods", action="store_true", help="显示六个关键时段")
    ap.add_argument("--catalog", action="store_true", help="检索文库目录记录")
    ap.add_argument("--relevance", choices=["高度相关", "相关", "一般"], help="按大盘相关度过滤（文库目录）")
    ap.add_argument("--top", type=int, default=15, help="最多显示条数（默认 15）")
    args = ap.parse_args()

    has_filter = any([args.date, args.frm, args.to, args.year, args.keyword,
                      args.title, args.src, args.key_periods, args.catalog, args.stats])

    # --stats
    if args.stats:
        tl = load(TIMELINE)
        posts = load(POSTS)
        print("缠论大盘解盘 · 库统计")
        print(f"  时间线解盘正文: {len(tl)} 条")
        years = {}
        for r in tl:
            y = norm_date(r.get("dt"))[:4]
            years[y] = years.get(y, 0) + 1
        print(f"    年份分布: {dict(sorted(years.items()))}")
        print(f"  大盘解读主题帖: {len(posts)} 条")
        srcs = {}
        for r in posts:
            s = r.get("src", "?")
            srcs[s] = srcs.get(s, 0) + 1
        print(f"    来源分布: {srcs}")
        kp = load(KEY)
        print(f"  关键时段: {len(kp)} 个，共 {sum(x['count'] for x in kp)} 篇关键文章")
        print(DISCLAIMER)
        return

    # --key-periods
    if args.key_periods:
        kp = load(KEY)
        for seg in kp:
            print("=" * 72)
            print(f"◆ {seg['span']}  {seg['name']}  （{seg['count']} 篇）")
            for doc in seg.get("docs", []):
                t = doc.get("title", "")
                dt = doc.get("dt", "")
                print(f"    - {dt}  {t}")
        print(DISCLAIMER)
        return

    # --catalog 文库目录
    if args.catalog:
        rows = []
        for fp in sorted(glob.glob(CATALOG_GLOB)):
            rows.extend(load(fp))
        if args.keyword:
            rows = [r for r in rows if args.keyword in catalog_val(r, "标题")]
        if args.year:
            rows = [r for r in rows if catalog_val(r, "年份").startswith(str(args.year))]
        if args.relevance:
            rows = [r for r in rows if args.relevance == catalog_val(r, "大盘相关度")]
        for i, r in enumerate(rows[: args.top], 1):
            print("-" * 72)
            print(f"[{i}] {catalog_val(r, '标题')}")
            print(f"    发布: {catalog_val(r, '发布时间')}  相关度: {catalog_val(r, '大盘相关度')}  "
                  f"字数: {catalog_val(r, '正文字数')}  年份: {catalog_val(r, '年份')}")
            ex = catalog_val(r, "原文 摘录")
            if ex:
                print(f"    摘录: {excerpt(ex, 100)}")
        print("-" * 72)
        print(f"共 {len(rows)} 条（显示前 {min(len(rows), args.top)} 条）")
        print(DISCLAIMER)
        return

    if not has_filter:
        ap.print_help()
        print("\n提示：至少指定一个检索条件（--date/--year/--keyword/--key-periods/--catalog 等）")
        print(DISCLAIMER)
        return

    # 时间线 + 市场帖联合检索
    results = []
    if not args.src:  # 时间线始终参与
        for r in load(TIMELINE):
            d = norm_date(r.get("dt"))
            if not in_range(d, args):
                continue
            blob = (r.get("title", "") or "") + "\n" + (r.get("main", "") or "")
            if args.keyword and args.keyword not in blob:
                continue
            if args.title and args.title not in (r.get("title", "") or ""):
                continue
            results.append(("时间线", r.get("title", ""), d, "官方博客时间线", r.get("main", "")))
    for r in load(POSTS):
        d = norm_date(r.get("dt"))
        if not in_range(d, args):
            continue
        if args.src and r.get("src") != args.src:
            continue
        blob = (r.get("title", "") or "") + "\n" + (r.get("text", "") or "")
        if args.keyword and args.keyword not in blob:
            continue
        if args.title and args.title not in (r.get("title", "") or ""):
            continue
        results.append(("市场帖", r.get("title", ""), d,
                        f"{r.get('src', '')} tid-{r.get('tid', '')}", r.get("text", "")))

    results.sort(key=lambda x: x[2])
    for i, (kind, title, d, src, text) in enumerate(results[: args.top], 1):
        print_doc(i, title, d, f"{kind} · {src}", text)
    print("-" * 72)
    print(f"共 {len(results)} 条（显示前 {min(len(results), args.top)} 条，按日期排序）")
    print(DISCLAIMER)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
