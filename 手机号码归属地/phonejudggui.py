import phonenumbers
from phonenumbers import geocoder, carrier
import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def get_phone_number_info(phone_number: str):
    try:
        # 提取后 11 位数字
        last_11_digits = phone_number.strip()[-11:]
        # 构造标准化的中国手机号码
        formatted_number = "+86" + last_11_digits
        
        # 解析电话号码
        parsed_number = phonenumbers.parse(formatted_number, "CN")
        # 获取归属地信息
        location = geocoder.description_for_number(parsed_number, "zh")  # "zh"表示中文
        # 获取运营商信息
        operator = carrier.name_for_number(parsed_number, "zh")
        
        return {
            "原始号码": phone_number,
            "标准化号码": formatted_number,
            "归属地": location or "未知",
            "运营商": operator or "未知"
        }
    except phonenumbers.NumberParseException:
        return {
            "原始号码": phone_number,
            "标准化号码": "无效号码",
            "归属地": "无效",
            "运营商": "无效"
        }

def process_file(input_file: str):
    # 确定输出文件路径
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_output.csv"
    
    # 读取输入文件内容
    results = []
    if input_file.endswith('.txt'):
        with open(input_file, 'r', encoding='utf-8') as f:
            phone_numbers = f.readlines()
    elif input_file.endswith('.csv'):
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            phone_numbers = [row[0] for row in reader]  # 假设号码在第一列
    else:
        messagebox.showerror("错误", "仅支持 .txt 或 .csv 文件！")
        return
    
    # 处理每个号码
    for phone_number in phone_numbers:
        result = get_phone_number_info(phone_number)
        results.append(result)
    
    # 将结果写入 CSV 文件
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["原始号码", "标准化号码", "归属地", "运营商"])
        writer.writeheader()
        writer.writerows(results)
    
    messagebox.showinfo("完成", f"处理完成，结果已保存至 {output_file}")

def select_file():
    # 打开文件选择对话框
    file_path = filedialog.askopenfilename(
        title="选择输入文件",
        filetypes=[("文本文件", "*.txt"), ("CSV 文件", "*.csv")]
    )
    if file_path:  # 确保用户选择了文件
        process_file(file_path)

def main():
    # 创建主窗口
    root = tk.Tk()
    root.title("手机号码归属地批量处理")
    root.geometry("400x200")

    # 添加按钮
    select_button = tk.Button(root, text="选择文件并处理", command=select_file, height=2, width=20)
    select_button.pack(pady=60)
    
    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()
