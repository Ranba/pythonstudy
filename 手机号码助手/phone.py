import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

class PhoneAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("手机号码助手")
        # ... 其他初始化代码 ...

    def import_phone_segments(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not file_path:
            return
            
        try:
            df = pd.read_excel(file_path, sheet_name=0)
            total_rows = len(df)
            
            # 创建进度条窗口
            progress_window = tk.Toplevel(self.root)
            progress_window.title("导入进度")
            progress = ttk.Progressbar(progress_window, length=300, mode='determinate')
            progress.pack(padx=10, pady=10)
            
            cursor = self.conn.cursor()
            for index, row in df.iterrows():
                cursor.execute('''
                    INSERT OR REPLACE INTO phone_segments (segment, area_code, city, operator)
                    VALUES (?, ?, ?, ?)
                ''', (str(row[0]), str(row[1]), str(row[2]), str(row[3])))
                
                progress['value'] = (index + 1) / total_rows * 100
                progress_window.update()
                
            self.conn.commit()
            progress_window.destroy()
            messagebox.showinfo("成功", "号段表导入完成！")
            
        except Exception as e:
            messagebox.showerror("错误", f"导入失败：{str(e)}")

    def import_city_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not file_path:
            return
            
        try:
            df = pd.read_excel(file_path, sheet_name=0)
            cursor = self.conn.cursor()
            
            for _, row in df.iterrows():
                cursor.execute('''
                    INSERT OR REPLACE INTO city_codes (area_code, province, city)
                    VALUES (?, ?, ?)
                ''', (str(row[0]), str(row[1]), str(row[2])))
                
            self.conn.commit()
            self.update_province_list()
            messagebox.showinfo("成功", "城市表导入完成！")
            
        except Exception as e:
            messagebox.showerror("错误", f"导入失败：{str(e)}")

    def upload_phone_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if not file_path:
            return
            
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_csv(file_path, header=None)
                
            numbers = df.iloc[:, 0].astype(str).tolist()
            if not str(numbers[0]).isdigit():
                numbers = numbers[1:]
                
            self.phone_text.delete('1.0', tk.END)
            self.phone_text.insert('1.0', '\n'.join(numbers))
            
        except Exception as e:
            messagebox.showerror("错误", f"文件读取失败：{str(e)}")

    def query_phones(self):
        # 清除之前的结果
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
            
        # 获取输入的号码
        numbers = self.phone_text.get('1.0', tk.END).strip().split('\n')
        cursor = self.conn.cursor()
        
        for number in numbers:
            if not number.strip():
                continue
                
            # 提取后11位
            number = number[-11:] if len(number) >= 11 else number
            segment = number[:7]
            
            # 查询号码信息
            cursor.execute('''
                SELECT ps.area_code, cc.province, ps.city, ps.operator
                FROM phone_segments ps
                LEFT JOIN city_codes cc ON ps.area_code = cc.area_code
                WHERE ps.segment = ?
            ''', (segment,))
            
            result = cursor.fetchone()
            if result:
                self.result_tree.insert('', 'end', values=(number,) + result)

    # 城市区号查询相关方法
    def update_province_list(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT DISTINCT province FROM city_codes ORDER BY province')
        provinces = cursor.fetchall()
        
        self.province_listbox.delete(0, tk.END)
        for province in provinces:
            self.province_listbox.insert(tk.END, province[0])

    def on_province_select(self, event):
        selection = self.province_listbox.curselection()
        if not selection:
            return
            
        province = self.province_listbox.get(selection[0])
        cursor = self.conn.cursor()
        cursor.execute('SELECT city FROM city_codes WHERE province = ? ORDER BY city', (province,))
        cities = cursor.fetchall()
        
        self.city_listbox.delete(0, tk.END)
        for city in cities:
            self.city_listbox.insert(tk.END, city[0])

    def add_city(self, event):
        selection = self.city_listbox.curselection()
        if not selection:
            return
            
        city = self.city_listbox.get(selection[0])
        if city not in self.selected_listbox.get(0, tk.END):
            self.selected_listbox.insert(tk.END, city)

    def add_province_cities(self, event):
        selection = self.province_listbox.curselection()
        if not selection:
            return
            
        province = self.province_listbox.get(selection[0])
        cursor = self.conn.cursor()
        cursor.execute('SELECT city FROM city_codes WHERE province = ?', (province,))
        cities = cursor.fetchall()
        
        for city in cities:
            if city[0] not in self.selected_listbox.get(0, tk.END):
                self.selected_listbox.insert(tk.END, city[0])

    def show_area_codes(self):
        selected_cities = self.selected_listbox.get(0, tk.END)
        if not selected_cities:
            return
            
        cursor = self.conn.cursor()
        area_codes = []
        
        for city in selected_cities:
            cursor.execute('SELECT area_code FROM city_codes WHERE city = ?', (city,))
            result = cursor.fetchone()
            if result:
                area_codes.append(result[0])
                
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', ', '.join(area_codes))

    def clear_selected_cities(self):
        self.selected_listbox.delete(0, tk.END)

    def clear_query_results(self):
        self.result_text.delete('1.0', tk.END)

# 主程序入口
if __name__ == '__main__':
    root = tk.Tk()
    app = PhoneAssistant(root)
    root.mainloop()