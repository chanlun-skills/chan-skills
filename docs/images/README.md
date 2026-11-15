# docs/images 素材清单

本目录存放 README、加群页、个人主页引用的图片。

## ✅ 已就绪

| 文件名 | 尺寸 | 说明 |
|---|---|---|
| `banner.png` | 1500×500 | README 顶部横幅。深紫渐变底 + 缠论「日线中枢→第三类买点」结构示意 + 安装命令 + 合规声明条 |
| `banner-logo.svg` | 512×512 | Logo 矢量源文件（可无损改色改形） |
| `banner-logo.png` | 1024×1024 | Logo 位图，GitHub 个人主页头像用这个 |
| `donate-wechat.png` | 800×853 | **微信收款码**（已裁掉微信推广页头页脚，保留二维码 + 韭菜 Logo + 昵称「韭菜之路」） |
| `donate-alipay.png` | 800×858 | **支付宝收款码**（已裁掉支付宝页头页脚，保留二维码 + 昵称「**风」） |
| `qq-qrcode.png` | 700×927 | **QQ 群二维码**（已裁到完整三个定位圆点，含 Logo + 群名「缠论Skills」+ 群号 1132948221） |

---

## ⬜ 待你放入

### 可选 · 6 张演示动图

| 文件名 | 建议尺寸 | 演示内容 |
|---|---|---|
| `demo-case-library.gif` | 480p，≤10MB | AI 检索缠论案例库并输出结构拆解 |
| `demo-sanmai.gif` | 480p，≤10MB | AI 走五步判定链输出三买分析 |
| `demo-jiexpan.gif` | 480p，≤10MB | AI 检索历史解盘并给出当时语境 |
| `demo-chan-zen.gif` | 480p，≤10MB | AI 检索佛学概念并注明出处 |
| `demo-music.gif` | 480p，≤10MB | AI 查询某期音乐会节目单与乐评 |
| `demo-yaogu.gif` | 480p，≤10MB | AI 复算某年妖股日线谷峰涨幅 |

**制作**：ScreenToGif（Windows 免费）录屏 → 裁剪 15~30 秒 → 导出 GIF 控制在 10MB 内。

### 可选 · 微信群二维码

| 文件名 | 尺寸 | 说明 |
|---|---|---|
| `qun-qrcode.png` | 800×800 | 微信群二维码（**7 天过期**）。过期时覆盖同名文件并 push 即可 |

> **过期怎么办？** 只需覆盖同名图片并推送，README 和 `docs/join.html` 里的链接永远不用改。
> 详见 `docs/join.html` 顶部注释。

---

## ❌ 不要放入（.gitignore 已拦截）

- ❌ 案例大全配图包 427MB → 走 GitHub Release / 网盘
- ❌ 缠师音乐会音频母版、视频工程 → 你的商业生产资产
- ❌ 长版口播文稿、选题分期、抖音文稿 → 商业资产，留作 Pro 版

> ⚠️ `.gitignore` 按扩展名拦截，中文名目录不一定命中规则。提交前用 `git status` 看一眼。

---

## 命名规范

`demo-<skill目录名>.gif`，与 `chan-skills/<skill目录名>/` 一一对应，方便后续批量补图。
