# -*- coding: utf-8 -*-
"""妖股年鉴检索工具（零依赖，Python 3.8+）

用法示例:
  python search_yaogu.py --stats
  python search_yaogu.py --years
  python search_yaogu.py --year 2015
  python search_yaogu.py --top 20 [--from 2010 --to 2026]
  python search_yaogu.py --theme 重组借壳
  python search_yaogu.py --code 300431 | --keyword 暴风
  python search_yaogu.py --caliber | --fix | --uncovered
  python search_yaogu.py --kline 2015|300431
"""
import argparse
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "references", "data")

DISCLAIMER = "\n[历史走势事后复盘素材，涨幅为日线谷→峰实算值，不可复制；不构成任何投资建议，禁止据此交易]"


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def fmt_item(it):
    cal = it.get("calTag") or ""
    cal = f"  [{cal}谷→峰]" if cal and cal != "无" else ""
    gain = it.get("gainText") or "—"
    now = f"（今名 {it['now']}）" if it.get("now") and it["now"] != it.get("name") else ""
    ver = " ✓双源" if it.get("verified") else ""
    kl = " ·有K线" if it.get("hasKline") else ""
    return (f"  {it['year']}  {it['name']}{now} {it['code']}  {gain}{cal}"
            f"  题材:{it.get('theme','')}  连板:{it.get('boards','')}{ver}{kl}")


def main():
    ap = argparse.ArgumentParser(description="妖股年鉴检索")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--years", action="store_true", help="37 年一览")
    ap.add_argument("--year", type=int, help="某年详情")
    ap.add_argument("--top", type=int, default=20, help="涨幅排行条数")
    ap.add_argument("--from", dest="yfrom", type=int, help="起始年份")
    ap.add_argument("--to", dest="yto", type=int, help="结束年份")
    ap.add_argument("--theme", help="按题材过滤")
    ap.add_argument("--code", help="按股票代码查询")
    ap.add_argument("--keyword", help="按名称/驱动因素模糊查询")
    ap.add_argument("--caliber", action="store_true", help="口径说明")
    ap.add_argument("--fix", action="store_true", help="修正幅度榜")
    ap.add_argument("--uncovered", action="store_true", help="行情源未覆盖明细")
    ap.add_argument("--kline", help="日线谷峰指标，格式 年|代码，如 2015|300431")
    args = ap.parse_args()

    yb = load("yearbook.json")
    items = yb["items"]

    if args.stats:
        m, k = yb["meta"], yb["kpis"]
        print(f"{m['title']}  {m['range']}  ({m['sourceVersion']})")
        print(f"数据更新: {m.get('dataUpdated')}")
        print(f"\n明细 {k['entries']} 条 / {k['years']} 年 | 已实算 {k['computed']} | 未覆盖 {k['uncovered']}")
        print(f"跨年口径 {k['crossYear']} 条 | 双源交叉验证 {k['dualChecked']}")
        print("\n== 题材分布 ==")
        for t in sorted(yb["themes"], key=lambda x: -x["count"]):
            print(f"  {t['name']}: {t['count']} 条 ({t['pct']}%)")
        print("\n== 各年条数 ==")
        from collections import Counter
        c = Counter(i["year"] for i in items)
        line = "  " + "  ".join(f"{y}:{n}" for y, n in sorted(c.items()))
        print(line)
        print(f"\n数据源: {m.get('sourceNote','')}")
        print(f"口径: {m.get('caliberNote','')}")
        print(DISCLAIMER)
        return

    if args.years:
        print(f"{'年':<6}{'年度标题':<14}{'市场特征':<22}最強妖股")
        for c in yb["yearCards"]:
            print(f"{c['year']:<6}{c['title']:<14}{c['market'][:20]:<22}{c['heroName']} {c['heroGain']}（{c['heroCaliber']}）")
        print(DISCLAIMER)
        return

    if args.year:
        card = next((c for c in yb["yearCards"] if c["year"] == args.year), None)
        if not card:
            sys.exit(f"无 {args.year} 年数据（范围 1990~2026）")
        print(f"== {card['year']} · {card['title']} ==")
        print(f"市场特征: {card['market']}")
        print(f"年度综述: {card['summary']}")
        print(f"\n最强妖股 Top{len(card['top'])}（实算口径）:")
        for t in card["top"]:
            print(f"  {t['rank']:>2}. {t['name']}  {t['gain']}  [{t.get('calTag','')}谷→峰]")
        rows = [i for i in items if i["year"] == args.year]
        print(f"\n明细 {len(rows)} 条:")
        for it in sorted(rows, key=lambda x: -(x.get("gain") or 0)):
            print(fmt_item(it))
        print(DISCLAIMER)
        return

    if args.caliber:
        m = yb["meta"]
        db = load("database_v4.json")
        print("== 涨幅口径（v5 · max draw-up）==")
        print(db.get("caliber_note", "").strip())
        print("\n== 数据质量 ==")
        for k, v in (db.get("data_quality") or {}).items():
            print(f"  {k}: {v}")
        print(f"\n数据源: {m.get('sourceNote','')}")
        print(f"\n{m.get('disclaimer','')}")
        return

    if args.fix:
        print(f"修正幅度 TOP{min(args.top, len(yb['fixTop']))}（原值 → 实算值）:\n")
        for r in yb["fixTop"][: args.top]:
            print(f"  {r['year']}  {r['name']} {r['code']}")
            print(f"      {r['orig']}  →  {r['new']}   {r['deviation']}")
            print(f"      口径变化: {r['caliberChange']}\n")
        print(DISCLAIMER)
        return

    if args.uncovered:
        rows = yb["uncovered"]
        print(f"行情源未覆盖 {len(rows)} 条（仅有原始记载值，无实算涨幅）:\n")
        for r in rows:
            print(f"  {r['year']}  {r['name']} {r['code']}  {r['orig']}")
            print(f"      原因: {r['reason']}")
        print(DISCLAIMER)
        return

    if args.kline:
        kl = load("kline.json")
        key = args.kline.strip()
        if key not in kl:
            cands = [k for k in kl if key in k][:10]
            if not cands:
                sys.exit(f"无 K 线组: {key}（共 {len(kl)} 组）")
            print("未精确匹配，候选:", ", ".join(cands), "\n")
            key = cands[0]
        d = kl[key]
        print(f"== 日线谷→峰指标  {key} ==")
        for k, v in d.items():
            if k == "bars":
                print(f"  K线根数: {len(v)}（每根为 [日序号, 开, 高, 低, 收]，价格已 ×10^prec 复权处理）")
            else:
                print(f"  {k}: {v}")
        print(DISCLAIMER)
        return

    # 明细筛选
    rows = items
    if args.yfrom:
        rows = [i for i in rows if i["year"] >= args.yfrom]
    if args.yto:
        rows = [i for i in rows if i["year"] <= args.yto]
    if args.theme:
        rows = [i for i in rows if args.theme in (i.get("theme") or "")]
    if args.code:
        rows = [i for i in rows if i.get("code") == args.code or args.code in (i.get("key") or "")]
    if args.keyword:
        kw = args.keyword
        rows = [i for i in rows if kw in (i.get("search") or "")]

    rows = sorted(rows, key=lambda x: -(x.get("gain") or -1))
    if not rows:
        sys.exit("无匹配记录（可试 --stats / --years 看数据范围）")
    # --top 未显式给出且是查单股时，显示全部
    n = args.top if len(rows) > args.top else len(rows)
    print(f"命中 {len(rows)} 条（显示 {n}，按实算涨幅降序）:\n")
    for it in rows[:n]:
        print(fmt_item(it))
    print(DISCLAIMER)


if __name__ == "__main__":
    main()
