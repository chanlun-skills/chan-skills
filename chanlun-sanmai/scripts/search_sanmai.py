#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chanlun-sanmai 检索工具

对缠论三买汇集库的 library.json 做本地检索，无第三方依赖。

用法示例:
    python search_sanmai.py --list                 # 20 条核心案例一览
    python search_sanmai.py --cat 确认             # 缠师确认的三买
    python search_sanmai.py --cat 否认             # 缠师否认/纠错
    python search_sanmai.py --code 601398          # 某股案例
    python search_sanmai.py --form 奔走式          # 按构成形态
    python search_sanmai.py --fate 新生            # 按中枢命运
    python search_sanmai.py --band "≥100%"         # 按涨幅档位
    python search_sanmai.py --quotes --theme 判定  # 三买原话库
    python search_sanmai.py --chain                # 五步判定链条
    python search_sanmai.py --stats                # 库统计
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, os.pardir, "references", "data", "library.json")

DISCLAIMER = (
    "\n[免责声明] 本工具仅检索 2006-2008 年历史案例与缠师原始论述，用于缠论技术理论学习"
    "与历史复盘，不构成任何投资建议。所有涨幅均为历史回测，不代表未来表现。"
)

THEMES = ["定义", "判定", "形态", "操作", "风险", "教学"]


def load():
    with open(LIB, "r", encoding="utf-8") as f:
        return json.load(f)


def norm_code(code):
    code = str(code).strip().split(".")[0]
    return "".join(ch for ch in code if ch.isdigit()).zfill(6)[-6:]


def fmt_perf(p):
    if not p:
        return ""
    keys = [("base_close", "基准收盘"), ("r20", "20日"), ("r120", "120日"),
            ("max_gain", "区间最大"), ("max_draw", "最大回撤")]
    parts = [f"{label} {p.get(k, '-')}%" for k, label in keys[1:]]
    base = p.get("base_close", "")
    out = f"基准收盘 {base} 元，" + "，".join(parts) if base else "，".join(parts)
    return out


def print_case(c, idx=None):
    head = f"[{idx}] " if idx else ""
    att = {"确认": "✔ 缠师确认", "否认": "✘ 缠师否认/纠错", "讨论": "◦ 讨论类"}.get(c.get("cat", ""), c.get("cat", ""))
    print("-" * 72)
    print(f"{head}{c.get('name', '')}({c.get('code', '')})  买点日: {c.get('buy', '')}  "
          f"级别: {c.get('level', '')}  {att}")
    print(f"    形态: {c.get('form', '-') or '-'} | 中枢命运: {c.get('fate', '-') or '-'} "
          f"| 涨幅档: {c.get('band', '-') or '-'} | 出处: {c.get('src', '')}")
    if c.get("title"):
        print(f"    标题: {c['title']}")
    if c.get("quote"):
        print(f"    原话: {c['quote']}")
    if c.get("detail"):
        d = c["detail"]
        print(f"    详注: {d[:150]}{'……' if len(d) > 150 else ''}")
    pn = c.get("perf_note", "")
    if pn:
        print(f"    复测: {pn}")
    elif c.get("perf"):
        print(f"    复测: {fmt_perf(c['perf'])}")
    if c.get("tags"):
        print(f"    标签: {' / '.join(c['tags'])}")


def main():
    ap = argparse.ArgumentParser(description="缠论三买汇集检索")
    ap.add_argument("--list", action="store_true", help="列出全部核心案例")
    ap.add_argument("--cat", choices=["确认", "否认", "讨论"], help="按缠师态度筛选")
    ap.add_argument("--code", help="按股票代码检索")
    ap.add_argument("--name", help="按名称模糊检索")
    ap.add_argument("--form", help="按构成形态筛选（如 标准三段回抽/奔走式/盘整背驰转化）")
    ap.add_argument("--fate", choices=["新生", "扩张", "延续"], help="按中枢命运筛选")
    ap.add_argument("--band", help="按涨幅档位筛选（≥100%% / 50%%–100%% / 不适用）")
    ap.add_argument("--level", choices=["日线", "周线", "15分钟"], help="按级别筛选")
    ap.add_argument("--quotes", action="store_true", help="检索三买原话库（81 条）")
    ap.add_argument("--theme", choices=THEMES, help="原话库按主题筛选（需 --quotes）")
    ap.add_argument("--chain", action="store_true", help="显示五步判定链条")
    ap.add_argument("--stats", action="store_true", help="显示库统计概览")
    ap.add_argument("--top", type=int, default=30, help="最多显示条数（默认 30）")
    args = ap.parse_args()

    lib = load()

    if args.stats:
        st = lib.get("meta", {}).get("stats", {})
        print("缠论三买汇集 · 库统计")
        for k, v in st.items():
            if k not in ("matrix", "bands", "bands_all"):
                print(f"  {k}: {v}")
        m = st.get("matrix", {})
        if m:
            print("  五维交叉矩阵（确认/否认/讨论 × 形态）:")
            for k, v in m.items():
                print(f"    {k}: {v}")
        print(DISCLAIMER)
        return

    if args.chain:
        for step in lib.get("chain", []):
            print("-" * 72)
            print(f"[{step.get('level', '')}] {step.get('step', '')}")
            print(f"    规则: {step.get('rule', '')}")
            if step.get("note"):
                print(f"    要点: {step['note']}")
            print(f"    出处: {step.get('src', '')}")
        print(DISCLAIMER)
        return

    if args.quotes:
        quotes = lib.get("quotes", [])
        rows = quotes
        if args.theme:
            rows = [q for q in rows if args.theme == (q.get("topic") or q.get("theme") or q.get("cat") or "")]
        for i, q in enumerate(rows[: args.top], 1):
            print("-" * 72)
            print(f"[{i}] {q.get('id', q.get('no', ''))}  主题: {q.get('topic', q.get('cat', ''))}"
                  f"{' · ' + q['theme'] if q.get('theme') else ''}  出处: {q.get('src', '')}  日期: {q.get('date', '')}")
            text = q.get("text", q.get("quote", ""))
            print(f"    {text[:160]}{'……' if len(text) > 160 else ''}")
            if q.get("note"):
                print(f"    注: {q['note'][:100]}")
        print("-" * 72)
        print(f"共 {len(rows)} 条（显示前 {min(len(rows), args.top)} 条）")
        print(DISCLAIMER)
        return

    # 案例检索
    cases = lib.get("cases", [])
    rows = cases
    if args.cat:
        rows = [c for c in rows if c.get("cat") == args.cat]
    if args.code:
        code = norm_code(args.code)
        rows = [c for c in rows if norm_code(c.get("code", "")) == code]
    if args.name:
        rows = [c for c in rows if args.name in (c.get("name", "") or "")]
    if args.form:
        rows = [c for c in rows if args.form in (c.get("form", "") or "")]
    if args.fate:
        rows = [c for c in rows if c.get("fate") == args.fate]
    if args.band:
        rows = [c for c in rows if args.band in (c.get("band", "") or "")]
    if args.level:
        rows = [c for c in rows if c.get("level") == args.level]

    if not any([args.list, args.cat, args.code, args.name, args.form,
                args.fate, args.band, args.level]):
        ap.print_help()
        print("\n提示：至少指定一个筛选条件，或使用 --list / --quotes / --chain / --stats")
        print(DISCLAIMER)
        return

    for i, c in enumerate(rows[: args.top], 1):
        print_case(c, i)
    print("-" * 72)
    print(f"共 {len(rows)} 条（显示前 {min(len(rows), args.top)} 条）")
    print(DISCLAIMER)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
