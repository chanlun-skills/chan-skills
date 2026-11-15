# chanlun-music · 缠师周末音乐会

> 缠中说禅「网上周末音乐会」档案库：42 期古典音乐连载 · 7,149 条回复 · 声乐与作曲专题 · 离线查看器

收录禅师（缠中说禅）2006-07-21 至 2007-08-25 在博客创办的「网上周末音乐会」全部档案——
中文互联网最早的系统性古典音乐网络专栏之一，每期一个主题（舒伯特、莫扎特、勃拉姆斯、
萧斯塔科维奇、柴可夫斯基、马勒、贝多芬……），42 期全程存档。

## 内容构成

| 内容 | 数量 | 说明 |
|---|---|---|
| 音乐会期数 | 42 期 | 逐期原文（节目单 + 缠师乐评 + 当年回复） |
| 博客回复 | 7,149 条 | 有实质内容 6,292 条；缠师本人 141 条仅存签名（正文源存档缺失） |
| 音乐与唱歌专题 | 77 篇 | 声乐技术 7 / 流行音乐评论 9 / 缠师作曲录音 7 / 跨界 4 / 前奏说明 6 / 主系列 42 |
| 专题汇编 | 6 类 md | compose / concert / cross / popular / prelude / vocal |
| 期数索引 | CSV | 期号、标题、日期、回复数、缠师回复数、论坛原帖链接 |
| 离线查看器 | 4 个 HTML | 主界面 / 音乐页 / 专题页 / 长稿页，全部自包含 |

## 安装

```bash
# skills.sh 一键安装
npx skills add <你的用户名>/chan-skills --skill chanlun-music

# 或手动克隆
git clone https://github.com/<你的用户名>/chan-skills.git
cp -r chan-skills/chanlun-music ~/.claude/skills/
```

## 使用示例

**对话式（装到支持 Agent Skills 的客户端后）：**

- "缠师的《冬之旅》那期讲了什么？" → 第 5 期原文与乐评
- "42 期音乐会里有哪些专场？" → 按期数索引梳理作曲家分布
- "缠师怎么看流行音乐？" → popular 专题（老鼠爱大米、张靓颖等评论）
- "缠师自己写过什么曲子？" → compose 专题（中学钢琴小回旋曲到 18 岁无调性《寂》）
- "教我怎么练声？" → vocal 专题文献呈现（歌唱技术系列，不作实修指导）

**命令行：**

```bash
python scripts/search_music.py --stats                     # 总览
python scripts/search_music.py --list                      # 42 期节目单
python scripts/search_music.py --ep 5                      # 某期原文（加 --full 看全文）
python scripts/search_music.py --keyword 冬之旅             # 关键词检索
python scripts/search_music.py --replies --ep 12           # 某期回复
python scripts/search_music.py --replies --keyword 卡拉扬    # 回复库关键词
python scripts/search_music.py --topics                    # 77 篇专题清单
```

**离线查看器**：浏览器直接打开 `references/viewer/index.html`（另附 music.html / topics.html / longscripts.html），无需联网。

## 使用边界

- 仅作音乐文化史料学习之用；引用缠师乐评保留期号与日期
- **已知局限**：缠师 141 条回复在源存档中仅存签名与时间，正文缺失——引用时不得编造，观点以 42 期原文为准
- 缠师对具体歌手/指挥的批判性乐评仅作史料，标注后不扩散
- 本库不含任何音频文件；曲目均为公版古典乐曲，现代录音请通过正规音乐平台聆听
- 详细说明见 [合规与版权说明.md](./合规与版权说明.md)
