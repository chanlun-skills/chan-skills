# 缠论大盘解盘 · Skill

> **chanlun-jiexpan** — 缠师 2006-2008 年大盘解盘历史库，做成 AI 可直接调用的 Agent Skill。
> 时间线解盘 **515** 篇 | 大盘解读主题帖 **946** 条 | 关键时段 **6** 个 / 49 篇精选 | 文库目录 ≈1,100 条

## 这是什么

把缠师在博客时间线与论坛中对**大盘（指数）**的解盘原文做成可按日期、关键词、时段检索的 Agent Skill：

- **按日期查解盘**：2007-05-30（530 印花税）、2007-10-16（6124 前后）、2008-09-18 等任一历史交易日的缠师原话
- **六个关键时段主线**：体系成型与 1000 点筑底 → 牛市主升与比例线推演 → 震荡筑平台 → 6124 见顶与全年展望 → 熊市两阶段 → 2284 筑底反弹定级
- **标志性表述溯源**："小康跌幅"（1000/1500/2000/2500/3000 点命名体系）、"两个翅膀"、"扬抑大扬大抑"、比例线、区间套
- **文库目录**：≈1,100 篇文档按"大盘相关度"（高度相关 328 / 相关 181 / 一般 591）分级检索
- **离线查看器**：report.html（关键解盘图表）/ lib_reader.html（文库阅读器），浏览器直接打开

## 目录结构

```
chanlun-jiexpan/
├── SKILL.md                     # 技能入口：6 时段主线、标志性表述、检索流程、合规红线
├── README.md                    # 本文件
├── 合规与版权说明.md
├── references/
│   ├── index.md                 # 数据地图与检索指南
│   ├── data/
│   │   ├── timeline.json        # ★ 515 篇时间线解盘正文
│   │   ├── market_posts.json    # 946 条大盘解读主题帖
│   │   ├── docs_index.json      # 1,679 条文档索引
│   │   ├── key_periods.json     # 6 关键时段 × 49 篇关键文章
│   │   └── library_catalog/     # 11 批文库目录记录（含相关度评级）
│   └── viewer/
│       ├── report.html          # 关键解盘报告图表查看器
│       ├── index.html           # 查看器导航
│       ├── lib_reader.html      # 文库阅读器
│       └── data/                # key_snapshot.js + echarts.min.js
└── scripts/
    └── search_jiexpan.py        # 命令行检索工具（无第三方依赖）
```

## 安装

```bash
npx skills add chanlun-skills/chan-skills
```

## 命令行检索工具（独立于 AI 也能用）

```bash
python scripts/search_jiexpan.py --stats                    # 库统计
python scripts/search_jiexpan.py --date 2007-05-30          # 某日解盘
python scripts/search_jiexpan.py --from 2007-10-01 --to 2007-10-31
python scripts/search_jiexpan.py --keyword 小康跌幅         # 全文检索
python scripts/search_jiexpan.py --key-periods              # 六个关键时段
python scripts/search_jiexpan.py --catalog --relevance 高度相关
```

## 效果演示

<!-- TODO: 录制 ScreenToGif 演示（15~30 秒，<10MB）
![演示](docs/images/demo-jiexpan.gif)
-->

## 交流与支持

<!-- TODO: 二维码过期请看置顶 Issue
| 微信群 | 请作者喝杯茶 |
|---|---|
| ![群](docs/images/qun-qrcode.png) | ![打赏](docs/images/donate-wechat.png) |
-->

- 🐛 问题反馈：[Issues](../../issues)（问题反馈 / 内容纠错模板）
- 💬 讨论交流：[Discussions](../../discussions)

## ⚠️ 免责声明

本仓库所有内容仅为**缠论技术理论学习与 2006-2008 年 A 股历史行情复盘**，不构成任何投资建议，不提供当前或未来市场走势判断。市场有风险，决策需独立判断，风险自担。

## License

数据整理部分：[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh)
缠师原文版权归原权利人所有，本库仅作教学研究之引用与索引。
