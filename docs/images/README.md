# docs/images 素材清单

本目录存放 README 与各 Skill 文档引用的图片。**下表中带 ⬜ 的素材需要你手动放入**，其余已就位。

## 必须放入（README 会引用，缺失会显示裂图）

| 文件名 | 建议尺寸 | 用途 | 制作方式 |
|---|---|---|---|
| ⬜ `banner.png` | 1500×500 | README 顶部横幅 | Canva 搜"科技横幅"模板，文字填「缠论 Skills 系列」+ 一句话定位 |
| ⬜ `donate-wechat.png` | 800×800 | 微信收款码 | 微信 → 服务 → 收款码，**中间打上 LOGO**，注明"请作者喝杯茶" |
| ⬜ `donate-alipay.png` | 800×800 | 支付宝收款码 | 支付宝 → 收款码，同样加 LOGO |
| ⬜ `qun-qrcode.png` | 800×800 | 微信群二维码 | 群二维码 **7 天过期**，README 里写明"过期请看置顶 Issue"，这个文件放当期即可 |

## 建议放入（提升转化，但不是必需）

| 文件名 | 建议尺寸 | 用途 |
|---|---|---|
| ⬜ `demo-case-library.gif` | 480p，≤10MB | 演示：AI 检索缠论案例库并输出结构拆解 |
| ⬜ `demo-sanmai.gif` | 480p，≤10MB | 演示：AI 走五步判定链输出三买分析 |
| ⬜ `demo-jiexpan.gif` | 480p，≤10MB | 演示：AI 检索历史解盘并给出当时语境 |
| ⬜ `demo-chan-zen.gif` | 480p，≤10MB | 演示：AI 检索佛学概念并注明出处 |
| ⬜ `demo-music.gif` | 480p，≤10MB | 演示：AI 查询某期音乐会节目单与乐评 |
| ⬜ `demo-yaogu.gif` | 480p，≤10MB | 演示：AI 复算某年妖股日线谷峰涨幅 |

**动图制作**：Windows 用 ScreenToGif（免费）录屏 → 裁剪 15~30 秒 → 导出 GIF 控制在 10MB 内（GitHub 单文件上限 100MB，但 README 里塞大文件会拖慢加载）。录完压缩可再用 ezgif.com。

## 不要放入（已由 .gitignore 拦截）

- ❌ 案例大全配图包 427MB → 走 GitHub Release / 网盘
- ❌ 缠师音乐会音频母版、视频工程 → 你的商业生产资产
- ❌ 长版口播文稿、选题分期、抖音文稿 → 商业资产，留作 Pro 版

## 命名规范

`demo-<skill目录名>.gif`，与 `chan-skills/<skill目录名>/` 一一对应，方便后续批量补图。
