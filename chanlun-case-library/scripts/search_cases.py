#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chanlun-case-library 检索工具

对缠论案例库的 CSV 数据做本地检索，无第三方依赖。

用法示例:
    python search_cases.py --list --top 10            # 案例数最多的个股
    python search_cases.py --code 600050              # 某股全部案例
    python search_cases.py --name 茅台                # 按名称模糊检索
    python search_cases.py --type 论坛回复与图解例析   # 按内容类型过滤
    python search_cases.py --keyword 底分型 --top 15  # 全文关键词检索
    python search_cases.py --timeline 600737          # 某股操作时间线
"""
import argparse
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, os.pardir, "references", "data")

DETAIL = os.path.join(DATA, "案例明细.csv")
STOCKS = os.path.join(DATA, "个股清单.csv")
TIMELINE = os.path.join(DATA, "重点个股时间线.csv")

DISCLAIMER = (
    "\n[免责声明] 本工具仅检索 2002-2008 年历史案例，用于缠论技术理论学习与历史复盘，"
    "不构成任何投资建议。市场有风险，决策需独立判断，风险自担。"
)


def read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def norm_code(code):
    """统一代码为 6 位字符串，容忍 600050 / 600050.0 / 600050SH 等写法。"""
    code = str(code).strip().split(".")[0]
    return "".join(ch for ch in code if ch.isdigit()).zfill(6)[-6:]


def print_rows(rows, cols, width=60):
    if not rows:
        print("（无匹配结果）")
        return
    for i, r in enumerate(rows, 1):
        print("-" * 72)
        print(f"[{i}] {r.get('股票名称', r.get('名称', ''))} "
              f"({r.get('股票代码', r.get('代码', ''))})  "
              f"日期: {r.get('日期', '') or '（未标注）'}")
        print(f"    类型: {r.get('内容类型', '')} | 来源: {r.get('来源渠道', '')} "
              f"| 出处: {r.get('来源标题', '')}")
        excerpt = (r.get("原文摘录", "") or "").strip()
        if len(excerpt) > width:
            excerpt = excerpt[:width] + "……"
        print(f"    摘录: {excerpt}")
    print("-" * 72)
    print(f"共 {len(rows)} 条")


def main():
    ap = argparse.ArgumentParser(description="缠论案例库检索")
    ap.add_argument("--list", action="store_true", help="列出个股清单（按案例数排序）")
    ap.add_argument("--code", help="按股票代码检索")
    ap.add_argument("--name", help="按股票名称模糊检索")
    ap.add_argument("--type", dest="ctype", help="按内容类型过滤")
    ap.add_argument("--channel", help="按来源渠道过滤")
    ap.add_argument("--keyword", help="在原文摘录中全文检索")
    ap.add_argument("--timeline", metavar="CODE", help="查看某股操作时间线")
    ap.add_argument("--top", type=int, default=20, help="最多显示条数（默认 20）")
    args = ap.parse_args()

    # --list: 个股清单
    if args.list:
        rows = read_csv(STOCKS)
        rows.sort(key=lambda r: -int(r.get("案例数", 0) or 0))
        print(f"{'排名':<4}{'代码':<10}{'名称':<14}{'行业':<8}{'案例数':>6}  跨度")
        for r in rows[: args.top]:
            print(f"{r['排名']:<5}{r['代码']:<10}{r['名称']:<14}{r['行业']:<8}"
                  f"{r['案例数']:>6}  {r['起始日期']} ~ {r['结束日期']}")
        print(DISCLAIMER)
        return

    # --timeline: 操作时间线
    if args.timeline:
        code = norm_code(args.timeline)
        rows = [r for r in read_csv(TIMELINE) if norm_code(r["代码"]) == code]
        rows.sort(key=lambda r: r.get("日期", "") or "")
        for r in rows[: args.top]:
            print("-" * 72)
            print(f"{r.get('日期', '') or '（未标注）'}  [{r.get('操作类型', '')}]")
            print(f"    {r.get('来源栏目', '')} | {r.get('来源标题', '')}")
            excerpt = (r.get("原文摘录", "") or "").strip()
            print(f"    {excerpt[:120]}{'……' if len(excerpt) > 120 else ''}")
        print("-" * 72)
        print(f"共 {len(rows)} 条时间线条目（显示前 {min(len(rows), args.top)} 条）")
        print(DISCLAIMER)
        return

    # 案例明细检索
    detail = read_csv(DETAIL)
    rows = detail
    if args.code:
        code = norm_code(args.code)
        rows = [r for r in rows if norm_code(r["股票代码"]) == code]
    if args.name:
        rows = [r for r in rows if args.name in (r["股票名称"] or "")]
    if args.ctype:
        rows = [r for r in rows if args.ctype in (r["内容类型"] or "")]
    if args.channel:
        rows = [r for r in rows if args.channel in (r["来源渠道"] or "")]
    if args.keyword:
        rows = [r for r in rows if args.keyword in (r["原文摘录"] or "")]

    if not any([args.code, args.name, args.ctype, args.channel, args.keyword]):
        ap.print_help()
        print("\n提示：至少指定 --code / --name / --keyword 之一，或使用 --list / --timeline")
        print(DISCLAIMER)
        return

    print_rows(rows[: args.top], None)
    if len(rows) > args.top:
        print(f"（共 {len(rows)} 条匹配，仅显示前 {args.top} 条，可用 --top 调整）")
    print(DISCLAIMER)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
