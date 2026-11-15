# chanlun-chan-zen · 缠论佛学与禅宗

> 缠中说禅佛学禅宗内容库：7,131 条语料 / 约 134 万字 / 四层来源 / 离线检索站点

收录禅师（缠中说禅）2006–2008 年全部佛学禅宗相关创作与讨论，是缠论系列 skill 中唯一纯哲学文化类（不含证券内容）的技能。

## 内容构成

| 层 | 数量 | 说明 |
|---|---|---|
| 博客·禅宗专栏 | 917 条 | 缠非缠禅非禅 196 / 教你打坐 428 / 禅宗辨微 137 / 禅余随笔 156 |
| 博客·兜率天连载 | 666 条 | 禅定与瑜伽解脱理论 |
| 博客·论语详解 | 949 条 | 儒释会通主战场 |
| 博客·回复区 | 97 条 | 缠师本人回复 46 + 网友跟帖 51 |
| 论坛·跟帖 | 4,502 条 | 论坛镜像原文与讨论 |

配套研究资料：

- **主题综述报告**：十大主题（绝对否定与不立一法、儒释道关系、生死与灵魂……）+ 核心原文摘引
- **论坛争鸣速览**：77,725 条楼层中筛出 1,471 条佛学楼层，按 12 个议题组织
- **佛学概念索引**：2,355 篇文档 × 六大词组大类（生死哲学 / 禅宗术语 / 佛典经藏 / 儒道会通 / 修行实践 / 典籍人物）
- **A~H 系列汇编**：禅宗专栏全文、教你打坐全集、禅宗辨微、兜率天、经文类、论语详解佛学段落、缠师回复佛学篇

## 安装

```bash
# skills.sh 一键安装
npx skills add chanlun-skills/chan-skills --skill chanlun-chan-zen

# 或手动克隆
git clone https://github.com/chanlun-skills/chan-skills.git
cp -r chan-skills/chanlun-chan-zen ~/.claude/skills/   # Claude Code 全局
```

## 使用示例

**对话式（装到支持 Agent Skills 的客户端后）：**

- "缠师《教你打坐》系列主要讲了什么？" → 428 条打坐系列按篇目梳理
- "缠非缠、禅非禅的核心观点是什么？" → 序 + 28 篇原文引证
- "当年论坛上关于轮回有没有讨论？" → 争鸣速览 99 条楼层溯源
- "儒家和佛家在缠师那里是什么关系？" → 论语详解 + 儒道会通主题

**命令行：**

```bash
python scripts/search_chanzen.py --stats                                 # 总览
python scripts/search_chanzen.py --cat "博客·禅宗专栏" --sub "教你打坐"    # 按系列浏览
python scripts/search_chanzen.py --keyword 打坐 --top 5                   # 全文检索
python scripts/search_chanzen.py --date 2006-02-01                        # 按日期
python scripts/search_chanzen.py --topics                                 # 概念大类
python scripts/search_chanzen.py --index --keyword 缘起                   # 概念定位篇目
```

**离线站点**：浏览器直接打开 `references/site/index.html`，支持全文搜索、分类树、人物关系图谱（relations.html）。

## 使用边界

- 仅作哲学文化学习研究之用；引用缠师原文保留标题与日期
- 区分缠师原文 / 缠师回复 / 网友观点，不得混淆归属
- 宗教内容中立呈现，不作宗教宣传与修行指导
- 详细说明见 [合规与版权说明.md](./合规与版权说明.md)
