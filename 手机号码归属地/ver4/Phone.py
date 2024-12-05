import os
import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import logging
import csv

# 设置日志记录
logging.basicConfig(
    filename="phone_data_tool.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 初始化数据库
def create_database():
    conn = sqlite3.connect("phone_data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS number_segments (
        segment TEXT, 
        area_code TEXT, 
        city TEXT, 
        carrier TEXT
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cities (
        area_code TEXT, 
        province TEXT, 
        city TEXT
    )""")
    conn.commit()
    conn.close()

# 导入数据到数据库
def import_excel_to_db(file_path, table_name):
    try:
        df = pd.read_excel(file_path)
        conn = sqlite3.connect("phone_data.db")
        cursor = conn.cursor()
        if table_name == "number_segments":
            data = df.iloc[:, :4].values.tolist()
            cursor.executemany("INSERT INTO number_segments VALUES (?, ?, ?, ?)", data)
        elif table_name == "cities":
            data = df.iloc[:, :3].values.tolist()
            cursor.executemany("INSERT INTO cities VALUES (?, ?, ?)", data)
        conn.commit()
        conn.close()
        messagebox.showinfo("成功", f"{table_name} 数据导入成功！")
        logging.info(f"导入数据到 {table_name} 表，文件路径: {file_path}")
    except Exception as e:
        messagebox.showerror("错误", f"导入数据时发生错误：{e}")
        logging.error(f"导入数据时发生错误: {e}")

# 查询数据库
def query_database(numbers):
    conn = sqlite3.connect("phone_data.db")
    cursor = conn.cursor()
    results = []
    for number in numbers:
        standard_number = number[-11:] if len(number) >= 11 else number
        segment = standard_number[:7]
        cursor.execute("""
        SELECT ns.area_code, c.province, c.city, ns.carrier
        FROM number_segments ns
        LEFT JOIN cities c ON ns.area_code = c.area_code
        WHERE ns.segment = ?
        """, (segment,))
        result = cursor.fetchone()
        if result:
            results.append((standard_number, *result))
        else:
            results.append((standard_number, "未知", "未知", "未知", "未知"))
    conn.close()
    return results

# 文件处理
def process_file(file_path):
    try:
        output_path = os.path.splitext(file_path)[0] + "_output.csv"
        with open(file_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            headers = next(reader)
            if not headers[0].isdigit():
                writer.writerow(headers + ["标准号码", "区号", "省份", "城市", "运营商"])
            else:
                infile.seek(0)
            numbers = [row[0] for row in reader if row]
            results = query_database(numbers)
            writer.writerows(results)
        messagebox.showinfo("成功", f"处理完成，输出文件：{output_path}")
        logging.info(f"处理文件完成，输入文件: {file_path}, 输出文件: {output_path}")
    except Exception as e:
        messagebox.showerror("错误", f"处理文件时发生错误：{e}")
        logging.error(f"处理文件时发生错误: {e}")

# 主界面布局
def main():
    create_database()
    root = tk.Tk()
    root.title("号码查询工具")
    root.geometry("930x390")

    # 功能函数
    def open_file_dialog(table_name):
        file_path = filedialog.askopenfilename(filetypes=[("Excel 文件", "*.xlsx")])
        if file_path:
            import_excel_to_db(file_path, table_name)

    def process_numbers():
        for row in tree.get_children():
            tree.delete(row)  # 清除表格数据
        numbers = number_input.get("1.0", tk.END).strip().split("\n")
        results = query_database(numbers)
        for row in results:
            tree.insert("", tk.END, values=row)
        logging.info(f"查询号码完成，数量: {len(numbers)}")

    def process_file_dialog():
        file_path = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt"), ("CSV 文件", "*.csv")])
        if file_path:
            process_file(file_path)

    # 菜单栏
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="导入号段表", command=lambda: open_file_dialog("number_segments"))
    file_menu.add_command(label="导入城市表", command=lambda: open_file_dialog("cities"))
    file_menu.add_separator()
    file_menu.add_command(label="退出", command=root.quit)
    menu_bar.add_cascade(label="文件", menu=file_menu)
    root.config(menu=menu_bar)

    # 左侧布局 - 输入框
    tk.Label(root, text="手动输入号码").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    number_input = tk.Text(root, height=20, width=40)
    number_input.grid(row=1, column=0, padx=10, pady=5)
    tk.Button(root, text="查询", command=process_numbers).grid(row=2, column=0, padx=10, pady=5, sticky="w")

    # 文件上传按钮
    tk.Button(root, text="上传文件", command=process_file_dialog).grid(row=5, column=0, padx=10, pady=5, sticky="w")

    # 右侧布局 - 查询结果表格
    columns = ("手机号码", "区号", "省份", "城市", "运营商")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
    tree.grid(row=0, column=1, rowspan=4, padx=10, pady=5)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    root.mainloop()

if __name__ == "__main__":
    main()
