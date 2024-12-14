"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
# 示例下载 https://www.pytk.net/blog/1702564569.html
from tkinter import filedialog, messagebox
import pandas as pd
import sqlite3

class Controller:
    # 导入UI类后，替换以下的 object 类型，将获得 IDE 属性提示功能
    ui: object
    def __init__(self):
        pass
    def init(self, ui):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui
        # TODO 组件初始化 赋值操作
    def upload_file_to_input(self,evt):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    number = line.strip()
                    if number.isdigit():
                        self.ui.tk_text_m4m4l3ks.insert('end', number + '\n')
        except Exception as e:
            messagebox.showerror("错误", f"文件读取失败：{str(e)}")
    def process_numbers(self,evt):
        numbers = self.ui.tk_text_m4m4l3ks.get("1.0", 'end').strip().split('\n')
        cursor = self.ui.db.conn.cursor()
        self.ui.tk_table_m4m4l9xt.delete(*self.ui.tk_table_m4m4l9xt.get_children())
        for number in numbers:
            if len(number) >= 11:
                segment = number[:7]
                cursor.execute('''
                    SELECT segment, area_code, city, operator FROM phone_segments WHERE segment=?
                ''', (segment,))
                result = cursor.fetchone()
                if result:
                    self.ui.tk_table_m4m4l9xt.insert('', 'end', values=(number, *result[1:]))
    def export_results(self,evt):
        print("<Button-1>事件未处理:",evt)
    def clear_selected_cities(self,evt):
        self.ui.tk_list_box_m4m4lrja.delete(0, 'end')
    def clear_results(self,evt):
        self.ui.tk_table_m4m4l9xt.delete(*self.ui.tk_table_m4m4l9xt.get_children())
    def display_area_codes(self,evt):
        selected_cities = self.ui.tk_list_box_m4m4lrja.get(0, 'end')
        cursor = self.ui.db.conn.cursor()
        area_codes = []
        for city in selected_cities:
            cursor.execute('SELECT area_code FROM cities WHERE city_name=?', (city,))
            result = cursor.fetchone()
            if result:
                area_codes.append(result[0])
        self.ui.tk_text_m4m54np9.delete("1.0", 'end')
        self.ui.tk_text_m4m54np9.insert('end', ', '.join(area_codes))
    def import_segments(self, evt):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not file_path:
            return
        
        try:
            df = pd.read_excel(file_path, sheet_name=0)
            cursor = self.ui.db.conn.cursor()  # 确保使用 ui.db.conn
            for index, row in df.iterrows():
                cursor.execute('''
                    INSERT OR REPLACE INTO phone_segments (segment, area_code, city, operator)
                    VALUES (?, ?, ?, ?)
                ''', (str(row[0]), str(row[1]), str(row[2]), str(row[3])))
            self.ui.db.conn.commit()  # 确保使用 ui.db.conn
            messagebox.showinfo("成功", "号段表导入完成！")
        except Exception as e:
            messagebox.showerror("错误", f"导入失败：{str(e)}")

    def import_cities(self, evt):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not file_path:
            return
        
        try:
            df = pd.read_excel(file_path, sheet_name=0)
            cursor = self.ui.db.conn.cursor()  # 确保使用 ui.db.conn
            for index, row in df.iterrows():
                cursor.execute('''
                    INSERT OR REPLACE INTO cities (city_name, area_code)
                    VALUES (?, ?)
                ''', (str(row[0]), str(row[1])))
            
            self.ui.db.conn.commit()  # 确保使用 ui.db.conn
            messagebox.showinfo("成功", "城市表导入完成！")
            
            # 加载省份到省份列表框
            provinces = df['省份'].unique()  # 假设省份在 DataFrame 的 '省份' 列中
            self.ui.province_listbox.delete(0, END)  # 清空现有列表
            for province in provinces:
                self.ui.province_listbox.insert(END, province)  # 添加省份到列表框

        except Exception as e:
            messagebox.showerror("错误", f"导入失败：{str(e)}")

    