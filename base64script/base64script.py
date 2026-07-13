import base64

def encode(text):
    return base64.b64encode(text.encode()).decode()

def decode(text):
    try:
        return base64.b64decode(text).decode()
    except Exception as e:
        return f"解码失败: {e}"

def menu():
    while True:
        print("\n=== Base64 编码/解码工具 ===")
        print("1. 编码 (Encode)")
        print("2. 解码 (Decode)")
        print("0. 退出")
        choice = input("请选择: ").strip()

        if choice == "0":
            print("再见！")
            break
        elif choice in ("1", "2"):
            content = input("请输入内容: ")
            result = encode(content) if choice == "1" else decode(content)
            print(f"结果: {result}")
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    menu()
