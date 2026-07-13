#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base64 编码/解码工具
支持文本、文件、URL 安全模式等多种类型的 Base64 处理
"""

import base64
import os
import sys


# ─── ANSI 颜色 ──────────────────────────────────────────────────────────────

class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE    = "\033[94m"
    DIM     = "\033[2m"

def c(text: str, color: str) -> str:
    """给文本着色"""
    return f"{color}{text}{Color.RESET}"


# ─── 公共工具 ────────────────────────────────────────────────────────────────

def print_banner():
    banner = r"""
  ____                 __   _  _     _____           _
 | __ )  __ _ ___  ___|\ \ | || |   |_   _|__   ___ | |
 |  _ \ / _` / __|/ _ \ \ \| || |_    | |/ _ \ / _ \| |
 | |_) | (_| \__ \  __/  > |__   _|   | | (_) | (_) | |
 |____/ \__,_|___/\___| /_/    |_|     |_|\___/ \___/|_|
    """
    print(c(banner, Color.CYAN))
    print(c("  Base64 编码 / 解码工具  v1.0", Color.BOLD + Color.MAGENTA))
    print(c("  " + "─" * 44, Color.DIM))
    print()


def print_menu():
    print(c("  ┌─────────────────────────────────────────┐", Color.BLUE))
    print(c("  │            ", Color.BLUE) + c("请选择操作", Color.BOLD + Color.YELLOW) + c("                    │", Color.BLUE))
    print(c("  ├─────────────────────────────────────────┤", Color.BLUE))
    print(c("  │  ", Color.BLUE) + c("1", Color.GREEN + Color.BOLD) + c("  →  文本编码（Base64）           │", Color.BLUE))
    print(c("  │  ", Color.BLUE) + c("2", Color.GREEN + Color.BOLD) + c("  →  文本解码（Base64）           │", Color.BLUE))
    print(c("  │  ", Color.BLUE) + c("3", Color.GREEN + Color.BOLD) + c("  →  文件编码（Base64）           │", Color.BLUE))
    print(c("  │  ", Color.BLUE) + c("4", Color.GREEN + Color.BOLD) + c("  →  文件解码（Base64）           │", Color.BLUE))
    print(c("  │  ", Color.BLUE) + c("5", Color.GREEN + Color.BOLD) + c("  →  URL 安全编码（Base64url）    │", Color.BLUE))
    print(c("  │  ", Color.BLUE) + c("6", Color.GREEN + Color.BOLD) + c("  →  URL 安全解码（Base64url）    │", Color.BLUE))
    print(c("  │  ", Color.BLUE) + c("0", Color.RED   + Color.BOLD) + c("  →  退出                        │", Color.BLUE))
    print(c("  └─────────────────────────────────────────┘", Color.BLUE))
    print()


def prompt(msg: str) -> str:
    return input(c(f"  » {msg}: ", Color.YELLOW)).strip()


def success(label: str, value: str):
    print()
    print(c("  ✔  " + label, Color.GREEN + Color.BOLD))
    print(c("  ┌" + "─" * 50, Color.DIM))
    # 每 76 个字符换行以便阅读
    for i in range(0, len(value), 76):
        print(c("  │ ", Color.DIM) + c(value[i:i+76], Color.CYAN))
    print(c("  └" + "─" * 50, Color.DIM))
    print()


def error(msg: str):
    print(c(f"\n  ✘  错误：{msg}\n", Color.RED + Color.BOLD))


def separator():
    print(c("  " + "─" * 46, Color.DIM))


# ─── 编码 / 解码 逻辑 ────────────────────────────────────────────────────────

def encode_text():
    """将用户输入的文本编码为 Base64"""
    text = prompt("请输入要编码的文本")
    if not text:
        error("输入内容不能为空")
        return
    encoding = prompt("字符编码（默认 UTF-8，直接回车跳过）") or "utf-8"
    try:
        raw = text.encode(encoding)
        result = base64.b64encode(raw).decode("ascii")
        success("Base64 编码结果", result)
    except LookupError:
        error(f"不支持的字符编码：{encoding}")
    except Exception as e:
        error(str(e))


def decode_text():
    """将 Base64 字符串解码为原始文本"""
    b64 = prompt("请输入要解码的 Base64 字符串")
    if not b64:
        error("输入内容不能为空")
        return
    encoding = prompt("输出字符编码（默认 UTF-8，直接回车跳过）") or "utf-8"
    try:
        # 自动补全缺失的 '=' 填充
        padding = (4 - len(b64) % 4) % 4
        raw = base64.b64decode(b64 + "=" * padding)
        result = raw.decode(encoding)
        success("解码结果（文本）", result)
    except Exception as e:
        error(f"解码失败，请确认输入为合法 Base64 字符串。详情：{e}")


def encode_file():
    """将文件内容编码为 Base64 并可选保存"""
    path = prompt("请输入文件路径")
    if not os.path.isfile(path):
        error(f"文件不存在：{path}")
        return
    try:
        with open(path, "rb") as f:
            raw = f.read()
        result = base64.b64encode(raw).decode("ascii")
        preview = result[:200] + ("..." if len(result) > 200 else "")
        success(f"文件 [{os.path.basename(path)}] 编码结果（前 200 字符预览）", preview)
        save = prompt("是否保存完整结果到文件？（输入目标路径，直接回车跳过）")
        if save:
            with open(save, "w", encoding="ascii") as out:
                out.write(result)
            print(c(f"  ✔  已保存到 {save}\n", Color.GREEN))
    except Exception as e:
        error(str(e))


def decode_file():
    """将包含 Base64 内容的文件解码并保存"""
    path = prompt("请输入 Base64 文件路径")
    if not os.path.isfile(path):
        error(f"文件不存在：{path}")
        return
    out_path = prompt("请输入解码后的输出文件路径")
    if not out_path:
        error("输出路径不能为空")
        return
    try:
        with open(path, "r", encoding="ascii") as f:
            b64 = f.read().strip()
        padding = (4 - len(b64) % 4) % 4
        raw = base64.b64decode(b64 + "=" * padding)
        with open(out_path, "wb") as out:
            out.write(raw)
        print(c(f"\n  ✔  解码完成，已保存到 {out_path}（{len(raw):,} 字节）\n", Color.GREEN + Color.BOLD))
    except Exception as e:
        error(str(e))


def encode_url_safe():
    """URL 安全 Base64 编码（Base64url，去除填充 =）"""
    text = prompt("请输入要编码的文本")
    if not text:
        error("输入内容不能为空")
        return
    try:
        raw = text.encode("utf-8")
        result = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
        success("Base64url 编码结果（已去除填充 =）", result)
    except Exception as e:
        error(str(e))


def decode_url_safe():
    """URL 安全 Base64 解码（Base64url）"""
    b64 = prompt("请输入 Base64url 字符串")
    if not b64:
        error("输入内容不能为空")
        return
    try:
        padding = (4 - len(b64) % 4) % 4
        raw = base64.urlsafe_b64decode(b64 + "=" * padding)
        result = raw.decode("utf-8")
        success("Base64url 解码结果", result)
    except Exception as e:
        error(f"解码失败：{e}")


# ─── 主循环 ──────────────────────────────────────────────────────────────────

ACTIONS = {
    "1": encode_text,
    "2": decode_text,
    "3": encode_file,
    "4": decode_file,
    "5": encode_url_safe,
    "6": decode_url_safe,
}


def main():
    print_banner()
    while True:
        print_menu()
        choice = prompt("请输入选项编号")
        print()

        if choice == "0":
            print(c("  再见！\n", Color.MAGENTA + Color.BOLD))
            break
        elif choice in ACTIONS:
            separator()
            ACTIONS[choice]()
            separator()
            input(c("  按 Enter 返回主菜单…", Color.DIM))
            print()
        else:
            error("无效选项，请输入 0–6 之间的数字")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(c("\n\n  已中断，再见！\n", Color.MAGENTA))
        sys.exit(0)
