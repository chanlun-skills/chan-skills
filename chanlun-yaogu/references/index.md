# 数据地图（chanlun-yaogu / references）

## data/ — 结构化数据

| 文件 | 大小 | 内容 |
|---|---|---|
| yearbook.json | 447KB | **核心库**：`meta`（来源/口径/免责）+ `kpis`（6 项）+ `themes`（4 类题材）+ `items`（444 条 × 30 字段）+ `yearCards`（37 张）+ `fixTop`（40 条修正榜）+ `uncovered`（24 条） |
| kline.json | 2.1MB | 420 组日线序列：`cal/gain/lowDay/lowPrice/highDay/highPrice/prec/base/bars`，bars 内每根为 `[日序号, 开, 高, 低, 收]`（价格 ×10^prec 复权处理） |
| database_v4.json | 683KB | 37 年原始库（`years[37]` 每年 12 只 + 6 类题材 + 完整 `caliber_note` v5 口径 + `data_quality` 10 项） |
| calc_v4.json | 420KB | 原始测算结果：`results`（420 条，key = 年\|代码）+ `fails`（24 条）+ `meta`（复权校准） |

### yearbook.json → items 关键字段

`key`（年\|代码）· `year` · `name` · `code` · `now`（现名）· `gain`/`gainText`（实算涨幅）·
`gainMode` · `annualGain`/`crossGain`/`closeGain`（三种口径对照）· `caliber` · `calTag`（跨年/年内/无）·
`lowDay`/`highDay`/`days`（谷峰与天数）· `deviation`/`deviationText`（与原始记载偏差）·
`fixLevel` · `verified`（双源一致）· `theme`（题材）· `boards`（连板）· `driver`（驱动因素）·
`note`（来源备注）· `hasKline` · `pf`/`pi`/`latin`/`search`（检索索引）

## archive/ — 素材库

| 文件 | 大小 | 内容 |
|---|---|---|
| 妖股年鉴素材库.md | 102KB | 700 行、5 章：〇口径与合规说明（发布前必读）· 一各年最强妖股速览（实算归类）· 二年度妖股总表（每年 12 只降序）· 三发布前必须核对的条目 · 四视频拆解模板（缠论 × 江恩） |

## viewer/ — 离线查看器

| 文件 | 大小 | 说明 |
|---|---|---|
| 妖股年鉴_1990-2026.html | 2.8MB | 单文件自包含，六大板块：题材分布 / 各年最强妖股 / 444 条明细 / 37 年份卡 / 修正榜 TOP40 / 未覆盖 24 条 |

## 检索路径建议（AI 引用指南）

1. **某年妖股** → `--year Y`（年份卡 + Top12 + 12 条明细）
2. **某只个股** → `--code` 或 `--keyword`（返回全部相关年份记录）
3. **题材脉络** → `--theme`（4 类：题材叙事/重组借壳/业绩驱动/制度红利）
4. **数字对不上网上说法** → `--fix` 修正榜（口径差异解释）+ `--caliber`（口径全文）
5. **某年某股缺失** → `--uncovered`（24 条原因）
6. **K 线谷峰 + 天数** → `--kline "年|代码"`
7. **完整浏览** → 引导打开 `references/viewer/妖股年鉴_1990-2026.html`

## 一致性提示

- `yearbook.json` 的 `themes` 是 4 分类（服务统计展示）；`database_v4.json` 的 `themes` 是 6 分类
  （含"周期行情""次新股"）。两者不冲突：前者为聚合口径，后者为原始标签集
- `database_v4.json` 的 `version` 为 `v5-max-drawup`（口径说明更新），`yearbook.json` 的
  `sourceVersion` 为 `v4 实算口径`（数据快照版本）。**数值以 yearbook.json 为准**，差异属版本迭代
- 年份卡 Top12 中含 `calTag = "无谷→峰"` 的条目为未测算（如 1990 年全体、2015 海天精工），
  与 `uncovered` 24 条部分重合——引用时必须标注"仅有原始记载值"
