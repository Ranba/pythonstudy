#!/usr/bin/env python3
"""Base64 编码/解码工具 — 支持标准 Base64、URL-safe Base64 及命令行管道调用。"""

import argparse
import base64
import binascii
import sys


def encode(text: str, urlsafe: bool = False) -> str:
    """将文本编码为 Base64 字符串。

    Args:
        text:   待编码的明文字符串。
        urlsafe: 是否使用 URL-safe Base64（将 +/ 替换为 -_，并去除 = 填充）。

    Returns:
        Base64 编码后的字符串。
    """
    data = text.encode("utf-8")
    encoded = base64.urlsafe_b64encode(data) if urlsafe else base64.b64encode(data)
    result: str = encoded.decode("ascii")
    if urlsafe:
        result = result.rstrip("=")
    return result


def decode(text: str, urlsafe: bool = False) -> str:
    """将 Base64 字符串解码为明文。

    Args:
        text:   Base64 编码的字符串。
        urlsafe: 输入是否为 URL-safe Base64（会自动补齐缺失的 = 填充）。

    Returns:
        解码后的明文字符串。

    Raises:
        ValueError: 输入不是合法的 Base64 字符串或解码后非 UTF-8 文本。
    """
    if urlsafe:
        # URL-safe Base64 可能缺少 = 填充，补齐到 4 的倍数
        missing_padding = len(text) % 4
        if missing_padding:
            text += "=" * (4 - missing_padding)
        raw = base64.urlsafe_b64decode(text)
    else:
        raw = base64.b64decode(text, validate=True)

    return raw.decode("utf-8")


def run_cli() -> None:
    """命令行模式：通过参数直接编码/解码，适合脚本和管道使用。"""
    parser = argparse.ArgumentParser(
        description="Base64 编码/解码工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  python base64script.py -e 'hello'         # 编码\n"
            "  python base64script.py -d 'aGVsbG8='      # 解码\n"
            "  echo hello | python base64script.py -e     # 管道编码\n"
            "  python base64script.py -d -u 'aGVsbG8'    # URL-safe 解码"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    _ = group.add_argument("-e", "--encode", action="store_true", help="编码模式")
    _ = group.add_argument("-d", "--decode", action="store_true", help="解码模式")
    _ = parser.add_argument("-u", "--urlsafe", action="store_true", help="使用 URL-safe Base64")
    _ = parser.add_argument("text", nargs="?", default=None, help="要处理的文本（不提供则从 stdin 读取）")

    args = parser.parse_args()

    # 获取输入文本：优先命令行参数，其次标准输入
    if args.text is not None:
        input_text = args.text
    else:
        input_text = sys.stdin.read().rstrip("\n")

    if not input_text:
        print("错误：没有输入内容", file=sys.stderr)
        sys.exit(1)

    try:
        if args.encode:
            print(encode(input_text, urlsafe=args.urlsafe))
        else:
            print(decode(input_text, urlsafe=args.urlsafe))
    except (binascii.Error, ValueError, UnicodeDecodeError) as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)


def menu() -> None:
    """交互式菜单模式。"""
    while True:
        print("\n=== Base64 编码/解码工具 ===")
        print("1. 编码 (Encode)")
        print("2. 解码 (Decode)")
        print("3. 编码 (URL-safe)")
        print("4. 解码 (URL-safe)")
        print("0. 退出")
        choice = input("请选择: ").strip()

        if choice == "0":
            print("再见！")
            break

        if choice not in ("1", "2", "3", "4"):
            print("无效选择，请重新输入")
            continue

        content = input("请输入内容: ").strip()
        if not content:
            print("输入内容不能为空")
            continue

        try:
            if choice == "1":
                result = encode(content)
            elif choice == "2":
                result = decode(content)
            elif choice == "3":
                result = encode(content, urlsafe=True)
            else:
                result = decode(content, urlsafe=True)
            print(f"结果:\n\n {result}")
        except (binascii.Error, ValueError, UnicodeDecodeError) as e:
            print(f"处理失败: {e}")


if __name__ == "__main__":
    # 如果传入了命令行参数（非交互运行），走 CLI 模式；否则走交互菜单
    if len(sys.argv) > 1:
        run_cli()
    else:
        menu()
