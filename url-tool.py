#!/usr/bin/env python3
import urllib.parse

def url_encode(text: str) -> str:
    """将输入字符串进行 URL 编码"""
    return urllib.parse.quote(text, safe='')

def url_decode(encoded_text: str) -> str:
    """将 URL 编码后的字符串解码回原始文本"""
    return urllib.parse.unquote(encoded_text)

if __name__ == "__main__":
    # 提示用户输入
    raw_text = input("请输入要处理的 URL 或文本: ")

    # 选择操作
    mode = input("请选择操作: 输入 E 进行编码，输入 D 进行解码: ").strip().upper()

    if mode == "E":
        result = url_encode(raw_text)
        print("编码结果:", result)
    elif mode == "D":
        result = url_decode(raw_text)
        print("解码结果:", result)
    else:
        print("无效选择，请输入 E 或 D。")
