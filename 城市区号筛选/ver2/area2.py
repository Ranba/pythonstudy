import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import pandas as pd

# 数据库文件名
DB_FILE = "city_codes.db"

# 创建数据库连接和表
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS city_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_code TEXT,
            province TEXT,
            city TEXT
        )
    """)
    conn.commit()
    conn.close()

# 导入 Excel 文件
def import_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
    if not file_path:
        return

    try:
        df = pd.read_excel(file_path)
        if set(['区号', '省份', '城市']).issubset(df.columns):
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM city_codes")
            conn.commit()

            for _, row in df.iterrows():
                cursor.execute("INSERT INTO city_codes (area_code, province, city) VALUES (?, ?, ?)",
                               (row['区号'], row['省份'], row['城市']))
            conn.commit()
            conn.close()

            load_province_list()
            messagebox.showinfo("成功", "Excel 文件已成功导入！")
        else:
            messagebox.showerror("错误", "Excel 文件必须包含 '区号', '省份', '城市' 列！")
    except Exception as e:
        messagebox.showerror("错误", f"导入失败：{e}")

# 加载省份列表
def load_province_list():
    province_listbox.delete(0, tk.END)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT province FROM city_codes")
    provinces = cursor.fetchall()
    for province in provinces:
        province_listbox.insert(tk.END, province[0])
    conn.close()

# 双击省份列表
def add_cities_by_province(event):
    selected_province = province_listbox.get(province_listbox.curselection())
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT city FROM city_codes WHERE province = ?", (selected_province,))
    cities = cursor.fetchall()

    for city in cities:
        if city[0] not in selected_city_listbox.get(0, tk.END):
            selected_city_listbox.insert(tk.END, city[0])
    conn.close()

# 双击城市列表
def add_selected_city(event):
    selected_city = city_listbox.get(city_listbox.curselection())
    if selected_city not in selected_city_listbox.get(0, tk.END):
        selected_city_listbox.insert(tk.END, selected_city)

# 显示城市列表
def show_cities(event):
    selected_province = province_listbox.get(province_listbox.curselection())
    city_listbox.delete(0, tk.END)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT city FROM city_codes WHERE province = ?", (selected_province,))
    cities = cursor.fetchall()

    for city in cities:
        city_listbox.insert(tk.END, city[0])
    conn.close()

# 清空选中列表
def clear_selected_cities():
    selected_city_listbox.delete(0, tk.END)

# 显示区号结果
def display_area_codes():
    selected_cities = selected_city_listbox.get(0, tk.END)
    if not selected_cities:
        messagebox.showwarning("警告", "没有选择任何城市！")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    area_codes = []
    for city in selected_cities:
        cursor.execute("SELECT area_code FROM city_codes WHERE city = ?", (city,))
        code = cursor.fetchone()
        if code:
            area_codes.append(code[0])
    conn.close()

    # 将结果显示在文本框中
    result_textbox.delete("1.0", tk.END)
    result_textbox.insert(tk.END, ",".join(area_codes))

# 清空结果文本框
def clear_results():
    result_textbox.delete("1.0", tk.END)

# 初始化程序
init_db()

# 创建主窗口
root = tk.Tk()
root.title("城市区号管理系统")

# 创建菜单栏
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="导入 Excel", command=import_excel)
file_menu.add_separator()
file_menu.add_command(label="退出", command=root.quit)
menu_bar.add_cascade(label="文件", menu=file_menu)
root.config(menu=menu_bar)

# 主布局
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# 左侧省份列表
left_frame = tk.Frame(main_frame)
left_frame.grid(row=0, column=0, sticky="n")
tk.Label(left_frame, text="省份列表").pack()
province_listbox = tk.Listbox(left_frame, height=15)
province_listbox.pack()
province_listbox.bind("<Double-Button-1>", add_cities_by_province)
province_listbox.bind("<<ListboxSelect>>", show_cities)

# 中间城市列表
middle_frame = tk.Frame(main_frame)
middle_frame.grid(row=0, column=1, sticky="n", padx=10)
tk.Label(middle_frame, text="城市列表").pack()
city_listbox = tk.Listbox(middle_frame, height=15)
city_listbox.pack()
city_listbox.bind("<Double-Button-1>", add_selected_city)

# 右侧选中城市列表
right_frame = tk.Frame(main_frame)
right_frame.grid(row=0, column=2, sticky="n")
tk.Label(right_frame, text="选中城市").pack()
selected_city_listbox = tk.Listbox(right_frame, height=15)
selected_city_listbox.pack()

# 最右侧结果显示框
result_frame = tk.Frame(main_frame)
result_frame.grid(row=0, column=3, sticky="n", padx=10)
tk.Label(result_frame, text="结果区号").pack()
result_textbox = tk.Text(result_frame, height=15, width=30)
result_textbox.pack()

# 底部按钮布局
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, padx=10, pady=5)

clear_button = tk.Button(button_frame, text="清空选中", command=clear_selected_cities)
clear_button.pack(side=tk.LEFT, padx=5)

display_button = tk.Button(button_frame, text="显示区号", command=display_area_codes)
display_button.pack(side=tk.RIGHT, padx=5)

clear_result_button = tk.Button(button_frame, text="清空结果", command=clear_results)
clear_result_button.pack(side=tk.RIGHT, padx=5)

# 启动程序
load_province_list()
root.mainloop()
