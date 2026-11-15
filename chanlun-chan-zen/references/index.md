# 数据地图（chanlun-chan-zen / references）

## data/ — 结构化数据

| 文件 | 大小 | 内容 |
|---|---|---|
| corpus.json | 5.6MB | **主语料** 7,131 条（id / cat / sub / title / date / source / url / text / is_head / seq），约 134 万字，时间跨度 2006-01 ~ 2014-02（论坛跟帖较晚） |
| tree.json | <1KB | 分类树计数（博客专栏四系列 + 兜率天 + 论语详解 + 回复区 + 论坛跟帖） |
| corpus_meta.json | 19KB | 禅宗专栏 83 篇篇目清单（title / date / slug / path / series） |
| buddhist_index.json | 0.9MB | 2,355 篇文档的佛学概念词频索引，六大词组大类 |
| stats.json | <1KB | 构建统计 |

## report/ — 研究报告

| 文件 | 大小 | 内容 |
|---|---|---|
| 佛学禅宗内容汇总.md | 293KB | 四层材料总览表 + 十大主题综述与核心原文摘引（首选入口：按主题查原文） |
| 论坛佛学争鸣速览.md | 131KB | 77,725 楼层中 1,471 条佛学楼层，按 12 议题组织（儒释道关系 580 / 生死与灵魂 273 / …），每条带发言人、日期、原帖链接 |

## series/ — 人工整理系列汇编

| 文件 | 大小 | 内容 |
|---|---|---|
| A_禅宗专栏全文.md | 361KB | 禅宗专栏 83 篇全文（缠非缠禅非禅 / 禅宗辨微 / 禅余随笔 / 教你打坐） |
| B_教你打坐全集.md | 161KB | 《教你打坐》30 篇全集 |
| C_禅宗辨微_上中下.md | 68KB | 对陈建民《禅宗辨微》的三篇辨析（汉传 vs 藏密） |
| D_兜率天连载.md | 202KB | 《兜率天》21 节连载 |
| E_经文类文本.md | 14KB | 经文类相关文本 |
| F_论语详解佛学段落.md | 1,006KB | 《论语》详解 114 篇中的佛学段落摘编 |
| H_缠师回复与网友讨论_佛学篇.md | 197KB | 博文回复区佛学问答摘编 |

> 未入库（留在源目录，走 Release/私域分发）：G_博客佛学段落汇编（5.6MB）、
> I_文史哲系列PDF_佛学篇章（1.4MB）、J_论坛佛学讨论（4.4MB）、reply_index.json（3.4MB）、
> pdf_fulltext.txt、缠中说禅文集 PDF（4.7MB）、chzhshch-src 完整源站（含 283MB 图片）。

## site/ — 离线检索站点

浏览器直接打开 `index.html` 即可使用，无需服务器：

- **index.html** — 主界面：全文搜索（分片加载 shard_0~7.js，共约 5.3MB 索引）、分类树（tree.js）、搜索建议（suggest.js）
- **relations.html** — 人物/概念关系图谱
- **about.html** — 关于页（数据来源与统计说明）

## 检索路径建议（AI 引用指南）

1. **主题类问题** → `report/佛学禅宗内容汇总.md` 主题综述 → 按 path 定位 corpus 条目
2. **篇目类问题** → `scripts/search_chanzen.py --cat/--sub/--keyword`
3. **论坛争论类** → `report/论坛佛学争鸣速览.md` 议题目录
4. **概念定位** → `scripts/search_chanzen.py --index --keyword <词>`
5. **完整浏览** → 引导用户打开 `site/index.html`
