# 数据地图与检索指南

> 本目录是 chanlun-jiexpan 的全部数据层。AI 使用前请先读本文件。

## 一、库的构成

| 项 | 数量 | 说明 |
|---|---|---|
| 时间线解盘正文 | 515 条 | 缠师博客时间线栏目的大盘解盘（2006: 95 / 2007: 259 / 2008: 161） |
| 大盘解读主题帖 | 946 条 | mirror 镜像 431 + official 515，含 market_hits 相关度 |
| 文档索引 | 1,679 条 | 全部文档的标题/日期/主题/来源/字数（无正文） |
| 关键时段 | 6 个 | 每段 8-9 篇关键文章，共 49 篇 |
| 文库目录 | 11 批 ≈1,100 条 | 含大盘相关度评级：高度相关 328 / 相关 181 / 一般 591 |

## 二、文件清单

| 文件 | 关键字段 | 用途 |
|---|---|---|
| `data/timeline.json` | title, dt, main, url | ★ 按日期/关键词检索解盘正文（主力数据） |
| `data/market_posts.json` | src(official/mirror), tid, title, dt, year, text, topics, market_hits, url | 同日多来源交叉印证；market_hits 为大盘相关命中计数 |
| `data/docs_index.json` | id, title, dt, year, topics, src, url, hits, nseg, len | 全库文档总索引 |
| `data/key_periods.json` | span, name, lo, hi, count, docs[] | 六个关键时段及各段关键文章 |
| `data/library_catalog/batch_*.json` | 标题, 发布时间, 主题, 大盘相关度, 原文链接, 来源站点, 原文摘录, 正文字数, 年份 | Notion 导出风格（字段值为嵌套 dict），文库分级目录 |
| `viewer/report.html` | 依赖 `viewer/data/key_snapshot.js` + `viewer/data/echarts.min.js` | 关键解盘报告图表查看器（浏览器打开） |
| `viewer/lib_reader.html` | 自包含 | 文库阅读器 |
| `viewer/index.html` | 三个查看器的导航页 | 入口 |

## 三、检索配方

1. **"530 那天缠师说了什么"** → `--date 2007-05-30`（会同时返回时间线 + mirror + official 三个来源）
2. **"6124 见顶前后"** → `--from 2007-10-01 --to 2007-11-30`，或 `--key-periods` 看第四时段
3. **"小康跌幅是什么"** → `--keyword 小康跌幅`（原始出处 2007-11-12 时间线）
4. **"比例线怎么用"** → `--keyword 比例线 --year 2007`
5. **"只看官方来源"** → `--src official`
6. **"找高度相关的大盘文章"** → `--catalog --relevance 高度相关`
7. **"熊市阶段复盘"** → `--key-periods` 第五、六时段 → 再按 `--frm/--to` 细读

## 四、日期口径

- `dt` 字段为发布时间（含时分秒），检索时截取日期部分比较
- 时间线与市场帖存在**同文多源**（official + mirror 收录同一篇），计数时注意去重（title + date 相同即同文）
- 年份分布：2006: 95 / 2007: 259 / 2008: 161（时间线）

## 五、数据局限

- 部分记录 text 含 `attach://xxxx.mp3` 等附件占位符，引用时忽略
- mirror 来源的帖子正文可能有少量 OCR/排版噪音
- corpus.json（106MB 全量语料）、segments.json（52MB 分段）、search_index.json（18MB 搜索索引）未入库，留在源目录 `D:\传统文化构建\缠论大盘解读\chanlun\data\`，如需深度检索可另行打包
- threads/*.html 为原始爬取网页（约 400+ 个），仅作溯源备份
