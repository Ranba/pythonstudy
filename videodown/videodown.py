#!/usr/bin/env python3
"""
videodown.py — YouTube / Bilibili 视频下载工具
依赖：yt-dlp >= 2023.x，ffmpeg
用法：python3 videodown.py

Cookie 认证（用于下载 YouTube 需登录验证的内容）：
  优先级 1 — 脚本同目录下放置 cookies.txt（Netscape 格式）
  优先级 2 — 自动检测本机 / WSL Windows 侧浏览器
  优先级 3 — 匿名下载（部分视频可能被拒绝）
"""

import subprocess
import sys
import shutil
import re
from pathlib import Path


# ─── ANSI 颜色 ───────────────────────────────────────────────────────────────

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    DIM     = "\033[2m"
    MAGENTA = "\033[95m"


def banner():
    print(f"""
{C.CYAN}{C.BOLD}╔══════════════════════════════════════════╗
║        VideoDown  🎬  v1.0               ║
║  YouTube & Bilibili 高清视频下载工具      ║
╚══════════════════════════════════════════╝{C.RESET}
""")


def info(msg: str):
    print(f"{C.CYAN}[•]{C.RESET} {msg}")


def ok(msg: str):
    print(f"{C.GREEN}[✓]{C.RESET} {msg}")


def warn(msg: str):
    print(f"{C.YELLOW}[!]{C.RESET} {msg}")


def err(msg: str):
    print(f"{C.RED}[✗]{C.RESET} {msg}", file=sys.stderr)


def section(title: str):
    print(f"\n{C.MAGENTA}{C.BOLD}── {title} ──{C.RESET}")


# ─── 依赖检查 ─────────────────────────────────────────────────────────────────

def check_dependencies() -> bool:
    section("依赖检查")
    all_ok = True

    for tool, install_hint in [
        ("yt-dlp", "pip install yt-dlp  或  pipx install yt-dlp"),
        ("ffmpeg",  "sudo apt install ffmpeg  (Ubuntu/Debian)"),
    ]:
        if shutil.which(tool):
            ok(f"{tool} 已找到：{shutil.which(tool)}")
        else:
            err(f"{tool} 未安装。安装方法：{install_hint}")
            all_ok = False

    return all_ok


# ─── 链接验证 ─────────────────────────────────────────────────────────────────

SUPPORTED_PATTERNS = [
    r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/",
    r"(https?://)?(www\.)?bilibili\.com/",
    r"(https?://)?b23\.tv/",
]


def is_supported_url(url: str) -> bool:
    return any(re.search(p, url) for p in SUPPORTED_PATTERNS)


# ─── Cookie 检测 ──────────────────────────────────────────────────────────────

# WSL 下 Windows 侧浏览器候选（按优先级排列）
_WIN_BROWSERS: list[tuple[str, str]] = [
    ("chrome",   r"Google\Chrome"),
    ("edge",     r"Microsoft\Edge"),
    ("brave",    r"BraveSoftware\Brave-Browser"),
    ("chromium", r"Chromium"),
    ("firefox",  r"Mozilla\Firefox"),
]

# 本机 Linux 浏览器候选
_LINUX_BROWSERS: list[str] = ["chrome", "chromium", "firefox", "edge", "brave"]


def _win_user_dirs() -> list[Path]:
    """返回 /mnt/c/Users/* 下所有真实用户目录。"""
    base = Path("/mnt/c/Users")
    if not base.exists():
        return []
    skip = {"All Users", "Default", "Default User", "Public"}
    return [d for d in base.iterdir() if d.is_dir() and d.name not in skip]


def detect_cookie_source() -> tuple[str, str] | None:
    """
    按优先级检测可用的 Cookie 来源，返回 (类型, 值) 或 None：
      ("file",    "/path/to/cookies.txt")   — cookies.txt 文件
      ("browser", "chrome")                  — 本机 Linux 浏览器
    注意：WSL 下 Windows 浏览器 Cookie 因 DPAPI 加密无法被 yt-dlp 解密，已跳过。
    """
    # 1. 优先：同目录或当前目录下的 cookies.txt
    for candidate in [
        Path(__file__).parent / "cookies.txt",
        Path.cwd() / "cookies.txt",
    ]:
        if candidate.exists() and candidate.stat().st_size > 0:
            return ("file", str(candidate))

    # 2. 本机 Linux 浏览器（非 WSL 场景）
    if not Path("/mnt/c").exists():
        for browser in _LINUX_BROWSERS:
            if shutil.which(browser):
                return ("browser", browser)

    return None


# ─── 下载逻辑 ─────────────────────────────────────────────────────────────────

def build_yt_dlp_cmd(url: str, output_dir: Path,
                     cookie_source: tuple[str, str] | None = None) -> list[str]:
    """
    构建 yt-dlp 命令：
    - 最高画质 + 最佳音质，由 ffmpeg 合并为 mp4
    - 下载所有字幕（含自动生成），统一转为 srt
    - 嵌入元数据和封面缩略图
    - 支持 cookies.txt 文件或浏览器 Cookie
    """
    output_tmpl = str(output_dir / "%(title)s" / "%(title)s.%(ext)s")

    cmd = [
        "yt-dlp",
        # ── 画质 / 音质（多级回退，兼容地区限制/特殊格式视频）──────
        "--format", (
            "bestvideo[ext=mp4]+bestaudio[ext=m4a]"
            "/bestvideo+bestaudio"
            "/best[ext=mp4]"
            "/best"
        ),
        "--merge-output-format", "mp4",
        # ── 字符清洗（Windows/Linux 文件系统非法字符替换为空格）───────
        "--replace-in-metadata", "title", r"[\\/:*?\"<>|]", " ",
        "--replace-in-metadata", "title", r"\s+", " ",
        "--replace-in-metadata", "title", r"^\s+|\s+$", "",
        # ── 字幕 ───────────────────────────────────────────────────
        "--write-subs",           # 下载手动字幕
        "--write-auto-subs",      # 下载自动生成字幕
        "--sub-langs", "zh-Hans,en",  # 仅简体中文、英文
        "--convert-subs", "srt",  # 统一转为 srt
        # ── 容错 ───────────────────────────────────────────────────
        "--ignore-errors",        # 单个字幕/分片失败不中断整体
        "--sleep-interval", "1",  # 请求间隔 1s，避免 429 限流
        # ── 元数据 / 封面 ──────────────────────────────────────────
        "--embed-metadata",       # 写入元数据
        "--embed-thumbnail",      # 嵌入封面（如容器支持）
        # ── 输出路径 ───────────────────────────────────────────────
        "--output", output_tmpl,
        # ── 进度 ───────────────────────────────────────────────────
        "--progress",
        "--no-warnings",
    ]

    # ── Cookie ────────────────────────────────────────────────────
    if cookie_source:
        kind, value = cookie_source
        if kind == "file":
            cmd += ["--cookies", value]
        elif kind == "browser":
            cmd += ["--cookies-from-browser", value]

    cmd.append(url)
    return cmd


def download(url: str, cookie_source: tuple[str, str] | None = None) -> bool:
    output_dir = Path.cwd()
    cmd = build_yt_dlp_cmd(url, output_dir, cookie_source)

    section("开始下载")
    info(f"链接：{C.DIM}{url}{C.RESET}")
    info(f"保存到：{C.DIM}{output_dir}{C.RESET}")
    print()

    try:
        result = subprocess.run(cmd, check=False)
        if result.returncode == 0:
            ok("下载完成！")
            return True
        else:
            err(f"yt-dlp 退出码：{result.returncode}")
            return False
    except FileNotFoundError:
        err("找不到 yt-dlp，请确认已正确安装。")
        return False
    except KeyboardInterrupt:
        warn("用户中断下载。")
        return False


# ─── 主流程 ───────────────────────────────────────────────────────────────────

def get_url() -> str:
    """交互式获取并验证视频链接。"""
    section("输入链接")
    print(f"{C.DIM}支持：YouTube、YouTube 播放列表、Bilibili 视频/合集{C.RESET}\n")

    while True:
        try:
            url = input(f"{C.BOLD}请输入视频链接（q 退出）：{C.RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)

        if url.lower() in ("q", "quit", "exit", ""):
            print(f"\n{C.CYAN}再见！{C.RESET}")
            sys.exit(0)

        if is_supported_url(url):
            return url
        else:
            warn("不支持的链接，请输入 YouTube 或 Bilibili 的视频/播放列表链接。")


def main():
    banner()

    # 1. 检查依赖
    if not check_dependencies():
        sys.exit(1)

    # 2. 检测 Cookie 来源
    section("Cookie 检测")
    cookie_source = detect_cookie_source()

    if cookie_source is None:
        warn("未找到 Cookie，将以匿名方式下载。")
        warn(f"若 YouTube 报错，请在脚本目录放置 {C.BOLD}cookies.txt{C.RESET}{C.YELLOW} 文件。")
        warn("导出方法：Chrome/Edge 安装扩展 'Get cookies.txt LOCALLY'，")
        warn("          访问 youtube.com 后点击导出，保存为 cookies.txt。")
    elif cookie_source[0] == "file":
        ok(f"使用 Cookie 文件：{C.DIM}{cookie_source[1]}{C.RESET}")
    else:
        ok(f"使用浏览器 Cookie：{C.BOLD}{cookie_source[1]}{C.RESET}")

    # 3. 循环下载
    while True:
        url = get_url()
        download(url, cookie_source)

        # 是否继续
        print()
        try:
            again = input(f"{C.BOLD}是否继续下载其他视频？[Y/n]：{C.RESET} ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if again in ("n", "no", "否"):
            break

    print(f"\n{C.GREEN}{C.BOLD}全部任务完成，感谢使用 VideoDown 🎬{C.RESET}\n")


if __name__ == "__main__":
    main()
