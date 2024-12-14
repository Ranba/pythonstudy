import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import pandas as pd
from datetime import datetime

class CityCodeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("城市区号管理程序")
        
        self.conn = sqlite3.connect('city_codes.db')
        self.create_table()
        
        self.province_listbox = tk.Listbox(master)
        self.city_listbox = tk.Listbox(master, selectmode=tk.MULTIPLE)
        self.export_button = tk.Button(master, text="导出", command=self.export_data)
        
        self.province_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.city_listbox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.export_button.pack(side=tk.BOTTOM)
        
        self.load_provinces()
        
        self.province_listbox.bind('<<ListboxSelect>>', self.load_cities)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS city_codes (
                id INTEGER PRIMARY KEY,
                area_code TEXT,
                province TEXT,
                city TEXT
            )
        ''')
        self.conn.commit()

    def load_provinces(self):
        # 通过文件对话框上传Excel文件
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if not file_path:
            return  # 如果没有选择文件，则返回
        
        df = pd.read_excel(file_path)  # 从选择的Excel文件导入数据
        provinces = df['省份'].tolist()  # 假设Excel中有一列名为'省份'
        self.province_listbox.delete(0, tk.END)  # 清空现有的省份列表
        for province in provinces:
            self.province_listbox.insert(tk.END, province)

    def load_cities(self, event):
        selected_province = self.province_listbox.get(self.province_listbox.curselection())
        # 这里可以根据省份加载城市数据
        cities = ['城市1', '城市2', '城市3']  # 示例城市
        self.city_listbox.delete(0, tk.END)
        for city in cities:
            self.city_listbox.insert(tk.END, city)

    def export_data(self):
        selected_cities = [self.city_listbox.get(i) for i in self.city_listbox.curselection()]
        if not selected_cities:
            messagebox.showwarning("警告", "请至少选择一个城市")
            return
        
        area_codes = ['区号1', '区号2', '区号3']  # 示例区号
        output = ','.join(area_codes)
        
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
        with open(filename, 'w') as f:
            f.write(output)
        
        messagebox.showinfo("导出成功", f"数据已导出到 {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CityCodeApp(root)
    root.mainloop()
