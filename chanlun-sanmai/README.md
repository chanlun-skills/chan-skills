# 缠论三买汇集 · Skill

> **chanlun-sanmai** — 缠师确认过的日线第三类买点专项库，做成 AI 可直接调用的 Agent Skill。
> 核心案例 **20** 条（确认 13 / 否认 3 / 讨论 4）| 三买原话库 **81** 条 | 涨停名单 **9** 只 | 五步判定链 | 三处流传资料纠错

## 这是什么

把缠中说禅（缠师）博客中确认过的日线三买，做成可检索、可核对、可教学的 Agent Skill：

- **五步判定链条**：日线中枢 → 30 分钟离开 → 30 分钟回试 → 5 分钟背驰确认 → 不破 ZG（三级共振）
- **20 条核心案例**按五维分类：缠师态度 / 构成形态 / 中枢命运 / 涨幅档位 / 级别
- **否认类案例单独成类**——"一天不可能完成三买""有重叠不是三买"等缠师亲手纠错的反例，教学价值最高
- **原话库 81 条**按六类主题归置：定义 7 / 判定 25 / 形态 10 / 操作 15 / 风险 8 / 教学 16
- **三买"形式之争"专章**：课程 20/21/36/37/92 表述差异及缠师最终结论（q100-q111）
- **三处流传资料纠错**：北辰实业代码（600832→601588）、000803 三卖年份（2007→2006）、涨停名单首行（600608→600068 葛洲坝）
- **历史复测数据**：12 条确认案例买点后 120 日涨幅全部 ≥20%（最低 +59.0%，最高 +266.7%，东方财富不复权日线）

## 目录结构

```
chanlun-sanmai/
├── SKILL.md                     # 技能入口：判定链条、形式之争、检索流程、合规红线
├── README.md                    # 本文件
├── 合规与版权说明.md
├── references/
│   ├── index.md                 # 数据地图与检索指南
│   ├── 归类汇编说明.md           # 汇编方法论（五维分类/纠错/涨幅实证/出处登记）
│   ├── 案例核实报告.md           # 426 行核实报告（原文佐证+逐案复盘+OCR校正）
│   ├── 归类汇编.html            # 单文件离线查阅器（浏览器打开可筛选）
│   ├── 案例目录.html            # 单文件离线案例目录（可搜索）
│   ├── 原始PDF-当年缠师确认的日线3买.pdf
│   └── data/
│       ├── library.json         # ★ 主数据底稿（20案例+81原话+判定链+出处）
│       └── cases.json           # 精简案例数据（含行情复测）
└── scripts/
    └── search_sanmai.py         # 命令行检索工具（无第三方依赖）
```

## 安装

```bash
npx skills add 你的用户名/chan-skills
```

## 命令行检索工具（独立于 AI 也能用）

```bash
python scripts/search_sanmai.py --stats              # 库统计
python scripts/search_sanmai.py --chain              # 五步判定链条
python scripts/search_sanmai.py --cat 确认           # 缠师确认的三买
python scripts/search_sanmai.py --cat 否认           # 缠师否认的反例（教学价值高）
python scripts/search_sanmai.py --fate 新生          # 中枢新生的案例
python scripts/search_sanmai.py --quotes --theme 判定 # 三买原话库
```

## 效果演示

<!-- TODO: 录制 ScreenToGif 演示（15~30 秒，<10MB）
![演示](docs/images/demo-sanmai.gif)
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

本仓库所有内容仅为**缠论技术理论学习与 2006-2008 年 A 股历史行情复盘**，不构成任何投资建议。
所有涨幅均为历史回测，不代表未来表现。缠论"必然赢利"是理论命题，不是收益承诺。市场有风险，决策需独立判断，风险自担。

## License

数据整理部分：[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh)
缠师原文版权归原权利人所有，本库仅作教学研究之引用与索引。
