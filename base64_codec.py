#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base64 编解码工具
支持文本的 Base64 编码和解码
"""

import base64
import sys


def encode_base64(text: str) -> str:
    """将文本编码为 Base64"""
    try:
        encoded_bytes = base64.b64encode(text.encode('utf-8'))
        return encoded_bytes.decode('utf-8')
    except Exception as e:
        return f"编码错误: {e}"


def decode_base64(encoded_text: str) -> str:
    """将 Base64 解码为文本"""
    try:
        decoded_bytes = base64.b64decode(encoded_text)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        return f"解码错误: {e}"


def print_separator():
    """打印分隔线"""
    print("-" * 50)


def show_menu():
    """显示菜单"""
    print("\n" + "=" * 50)
    print("        Base64 编解码工具")
    print("=" * 50)
    print("1. 编码 (文本 → Base64)")
    print("2. 解码 (Base64 → 文本)")
    print("3. 退出")
    print("=" * 50)


def main():
    """主函数"""
    print("欢迎使用 Base64 编解码工具！")
    
    while True:
        show_menu()
        
        try:
            choice = input("\n请选择操作 (1/2/3): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n再见！")
            break
        
        if choice == '3' or choice.lower() in ('q', 'quit', 'exit'):
            print("\n再见！")
            break
        
        if choice == '1':
            # 编码模式
            print_separator()
            print("【编码模式】文本 → Base64")
            print_separator()
            try:
                text = input("请输入要编码的文本: ")
                if not text:
                    print("输入不能为空，请重试。")
                    continue
                result = encode_base64(text)
                print_separator()
                print(f"原始文本: {text}")
                print(f"Base64 编码: {result}")
                print_separator()
            except (KeyboardInterrupt, EOFError):
                print("\n操作已取消。")
                continue
                
        elif choice == '2':
            # 解码模式
            print_separator()
            print("【解码模式】Base64 → 文本")
            print_separator()
            try:
                encoded_text = input("请输入要解码的 Base64 字符串: ")
                if not encoded_text:
                    print("输入不能为空，请重试。")
                    continue
                result = decode_base64(encoded_text)
                print_separator()
                print(f"Base64 字符串: {encoded_text}")
                print(f"解码结果: {result}")
                print_separator()
            except (KeyboardInterrupt, EOFError):
                print("\n操作已取消。")
                continue
                
        else:
            print("无效的选择，请输入 1、2 或 3。")


if __name__ == "__main__":
    main()