# 缠论案例大全 · Skill

> **chanlun-case-library** — 缠中说禅（缠师）2002-2008 年 A 股个股案例系统汇编，做成 AI 可直接调用的 Agent Skill。
> 案例条目 **3,026** 条 | 覆盖个股 **347** 只 | 六大经典案例深度剖析 | 配图索引 1,385 张

## 这是什么

一个让 AI 掌握"缠论历史案例复盘"能力的 Agent Skill（SKILL.md 开放标准）：

- 按个股检索缠师当年的原话与判断（600050 中国联通 236 条、601857 中国石油 128 条、600737 北方导航 86 条……）
- 按关键词全文检索案例原文（如"底分型""背驰""中枢""三买"）
- 深度阅读六大经典案例：贵州茅台周线买卖点推演、紫光股份阻击建仓、宁波海运认沽底分型示范、中国联通全周期样本、北方导航中字头样本、华闻传媒低位提示
- 按行业、按年度浏览案例分布，查看重点个股操作时间线

## 目录结构

```
chanlun-case-library/
├── SKILL.md                  # 技能入口：触发场景、工作流程、数据地图、合规红线
├── README.md                 # 本文件
├── 合规与版权说明.md          # 版权归属与证券合规边界
├── references/               # 数据层
│   ├── index.md              # 数据地图与检索指南
│   ├── 汇编总览.md            # 全库总纲（9 章）
│   ├── 六大经典案例.md        # 六大经典案例深度剖析
│   ├── data/
│   │   ├── 个股清单.csv       # 347 只个股总表
│   │   ├── 案例明细.csv       # 3,026 条案例明细
│   │   ├── 个股案例档案.csv   # 按个股归档
│   │   └── 重点个股时间线.csv # 操作类型时间线
│   └── images/
│       ├── 配图索引.json      # 1,385 张配图的索引
│       └── 配图索引.md
└── scripts/
    └── search_cases.py       # 命令行检索工具（无第三方依赖）
```

## 安装

```bash
# skills.sh（支持 Claude Code / Codex / Cursor 等 20+ Agent）
npx skills add chanlun-skills/chan-skills

# 或手动克隆
git clone https://github.com/chanlun-skills/chan-skills.git
cp -r chan-skills/chanlun-case-library ~/.claude/skills/
```

## 命令行检索工具（独立于 AI 也能用）

```bash
python scripts/search_cases.py --list --top 10          # 案例最多的个股
python scripts/search_cases.py --code 600050            # 某股全部案例
python scripts/search_cases.py --keyword 底分型         # 全文关键词
python scripts/search_cases.py --timeline 600737        # 操作时间线
```

## 配图包

原始配图共 427MB（1,385 张，缠师博客走势图截图），不随仓库分发：

- GitHub Release 下载（推荐）
- 本仓库置顶 Issue 内的网盘链接

下载后解压到 `references/images/配图/` 即可被配图索引引用。

## 效果演示

<!-- TODO: 录制 ScreenToGif 演示（15~30 秒，<10MB）
![演示](docs/images/demo-case-library.gif)
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

本仓库所有内容仅为**缠论技术理论学习与 2002-2008 年 A 股历史行情复盘**，不构成任何投资建议。
历史案例中的个股其后多经历退市、重组、ST 等重大变化。市场有风险，决策需独立判断，风险自担。

## License

数据整理部分：[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh)
缠师原文版权归原权利人所有，本库仅作教学研究之引用与索引。
