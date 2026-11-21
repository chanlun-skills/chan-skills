#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成六个 Skill 的演示动图（真实脚本输出 → 终端风格帧 → GIF）
"""
import os, sys, subprocess, shutil, tempfile
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "docs", "images")
PY = sys.executable

W, H = 820, 400
PAD = 16
TITLEBAR = 32
LH = 21
MAXROWS = 15

BG = (22, 24, 34)
TITLEBG = (38, 41, 56)
FG = (222, 226, 240)
CYAN = (118, 200, 226)
YELLOW = (232, 193, 112)
DIM = (110, 116, 138)
PROMPT = (126, 214, 154)

_fcache = {}


def font(path, size=14):
    key = (path, size)
    if key not in _fcache:
        _fcache[key] = ImageFont.truetype(path, size)
    return _fcache[key]


def _pick(*cands):
    for c in cands:
        if os.path.exists(c):
            return c
    return None


MONO = _pick(
    r"C:\Windows\Fonts\consola.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/System/Library/Fonts/Menlo.ttc",
) or r"C:\Windows\Fonts\consola.ttf"
CJK = _pick(
    r"C:\Windows\Fonts\msyh.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/PingFang.ttc",
) or r"C:\Windows\Fonts\msyh.ttc"


def render_frame(lines, title):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, TITLEBAR], fill=TITLEBG)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([13 + i * 19, 11, 23 + i * 19, 21], fill=c)
    tf = font(CJK, 13)
    d.text((W // 2 - 70, 9), title, font=tf, fill=(198, 204, 226))

    fm = font(MONO)
    fc = font(CJK)
    y = TITLEBAR + PAD
    for line in lines[:MAXROWS]:
        if y > H - 10:
            break
        if line.startswith("$"):
            col, f = PROMPT, fc
        elif "====" in line or line.startswith("--"):
            col, f = DIM, fm
        elif "免责" in line or "不构成" in line:
            col, f = YELLOW, fc
        elif line.strip().startswith("["):
            col, f = CYAN, fc
        else:
            col, f = FG, fc
        d.text((PAD, y), line, font=f, fill=col)
        y += LH
    return img


def wrap_lines(raw_lines, maxpx):
    """按像素宽度折行"""
    probe = Image.new("RGB", (10, 10))
    pd = ImageDraw.Draw(probe)
    fm = font(MONO)
    fc = font(CJK)
    out = []
    for raw in raw_lines:
        if not raw.strip():
            continue
        f = fc if any("\u4e00" <= ch <= "\u9fff" for ch in raw) else fm
        if pd.textlength(raw, font=f) <= maxpx:
            out.append(raw)
            continue
        indent = len(raw) - len(raw.lstrip())
        cur = ""
        for ch in raw:
            trial = cur + ch
            if pd.textlength(trial, font=f) > maxpx and cur:
                out.append(cur)
                cur = " " * indent + ch
            else:
                cur = trial
        if cur:
            out.append(cur)
    return out


def typed_frames(raw_lines, title, cols_per_step=3, hold=26):
    """逐字打字动画：生成帧列表"""
    maxpx = W - PAD * 2
    full = wrap_lines(raw_lines, maxpx)
    frames = []
    # 阶段1：命令行出现
    cmd = raw_lines[0] if raw_lines else ""
    frames.append(render_frame([cmd], title))
    # 阶段2：内容逐行出现（每行分几帧，模拟打字）
    shown = [cmd]
    for line in full[1:]:
        n = len(line)
        steps = max(1, min(4, n // cols_per_step + 1))
        for k in range(1, steps + 1):
            part = line[:max(1, int(n * k / steps))]
            frames.append(render_frame(shown + [part], title))
        shown.append(line)
    frames.extend([frames[-1]] * hold)
    return frames


def build_gif(title, raw_lines, out_name, fps=7, hold=26):
    frames = typed_frames(raw_lines, title, hold=hold)
    out_path = os.path.join(OUT, out_name)
    tmp = tempfile.mkdtemp()
    paths = []
    for i, fr in enumerate(frames):
        p = os.path.join(tmp, "f%04d.png" % i)
        fr.save(p, "PNG")
        paths.append(p)
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-framerate", str(fps), "-i", os.path.join(tmp, "f%04d.png"),
           "-vf", "scale=%d:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3" % W,
           "-loop", "0", out_path]
    r = subprocess.run(cmd, capture_output=True)
    shutil.rmtree(tmp, ignore_errors=True)
    return os.path.exists(out_path), r.stderr.decode("utf-8", "ignore"), len(frames)


def run(skill, args):
    p = subprocess.run([PY] + args, cwd=os.path.join(REPO, skill),
                       capture_output=True, timeout=180)
    return (p.stdout or b"").decode("utf-8", "ignore") + (p.stderr or b"").decode("utf-8", "ignore")


def clip(lines, n):
    return [l for l in lines.splitlines() if l.strip()][:n]


def mk(skill, title, cmdline, raw, out_name):
    body = ["$ " + cmdline] + clip(raw, 12)
    ok, err, nf = build_gif(title, body, out_name)
    p = os.path.join(OUT, out_name)
    mb = os.path.getsize(p) / 1024 / 1024 if os.path.exists(p) else 0
    print("[%s] %-18s frames=%-4d %5.2f MB %s" % ("OK" if ok else "FAIL",
          out_name.replace("demo-", "").replace(".gif", ""), nf, mb, "" if ok else err[:120]))
    return ok


def main():
    os.makedirs(OUT, exist_ok=True)

    s = run("chanlun-case-library", ["scripts/search_cases.py", "--stats"])
    k = run("chanlun-case-library", ["scripts/search_cases.py", "--keyword", "中国联通"])
    mk("chanlun-case-library", "chanlun-case-library · 缠论案例大全",
       "python scripts/search_cases.py --stats", s, "demo-case-library.gif")

    s = run("chanlun-sanmai", ["scripts/search_sanmai.py", "--stats"])
    q = run("chanlun-sanmai", ["scripts/search_sanmai.py", "--quotes"])
    mk("chanlun-sanmai", "chanlun-sanmai · 缠论三买汇集",
       "python scripts/search_sanmai.py --quotes", q, "demo-sanmai.gif")

    s = run("chanlun-jiexpan", ["scripts/search_jiexpan.py", "--stats"])
    mk("chanlun-jiexpan", "chanlun-jiexpan · 缠论大盘解盘",
       "python scripts/search_jiexpan.py --stats", s, "demo-jiexpan.gif")

    s = run("chanlun-chan-zen", ["scripts/search_chanzen.py", "--stats"])
    mk("chanlun-chan-zen", "chanlun-chan-zen · 缠论佛学与禅宗",
       "python scripts/search_chanzen.py --stats", s, "demo-chan-zen.gif")

    s = run("chanlun-music", ["scripts/search_music.py", "--stats"])
    mk("chanlun-music", "chanlun-music · 缠师周末音乐会",
       "python scripts/search_music.py --stats", s, "demo-music.gif")

    s = run("chanlun-yaogu", ["scripts/search_yaogu.py", "--stats"])
    y = run("chanlun-yaogu", ["scripts/search_yaogu.py", "--year", "2015"])
    mk("chanlun-yaogu", "chanlun-yaogu · 妖股年鉴",
       "python scripts/search_yaogu.py --year 2015", y, "demo-yaogu.gif")


if __name__ == "__main__":
    main()
