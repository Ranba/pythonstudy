import os
import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import logging

# 设置日志
logging.basicConfig(
    filename="phone_data_tool.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 创建数据库和表
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

# 导入Excel文件到数据库
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
        messagebox.showinfo("成功", f"{table_name} 数据已成功导入数据库！")
        logging.info(f"导入数据到 {table_name}，文件路径: {file_path}")
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

# 处理文件
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

# 主界面
def main():
    create_database()
    root = tk.Tk()
    root.title("号码处理程序")
    root.geometry("700x550")

    # 清除查询数据
    def clear_tree():
        for row in tree.get_children():
            tree.delete(row)

    def open_file_dialog(table_name):
        file_path = filedialog.askopenfilename(filetypes=[("Excel 文件", "*.xlsx")])
        if file_path:
            import_excel_to_db(file_path, table_name)

    def process_numbers():
        clear_tree()  # 清除之前的数据
        numbers = number_input.get("1.0", tk.END).strip().split("\n")
        results = query_database(numbers)
        for row in results:
            tree.insert("", tk.END, values=row)
        logging.info("查询号码完成，数量: %d" % len(numbers))

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

    # 输入框布局
    tk.Label(root, text="手动输入号码").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    number_input = tk.Text(root, height=10, width=80)
    number_input.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

    tk.Button(root, text="查询", command=process_numbers).grid(row=2, column=1, pady=10)

    # 查询结果表格
    columns = ("号码", "区号", "省份", "城市", "运营商")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
    tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # 文件处理
    tk.Button(root, text="上传文件", command=process_file_dialog).grid(row=4, column=0, padx=10, pady=5, sticky="w")
    root.mainloop()

if __name__ == "__main__":
    main()
