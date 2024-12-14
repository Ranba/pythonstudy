import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd


class PhoneCityApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("手机号码处理与城市区号查询")
        width = 800
        height = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(False, False)

        # Database connection
        self.conn = sqlite3.connect("phone_city.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Menu bar
        self.create_menu()

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.place(x=10, y=10, width=780, height=480)

        self.phone_frame = ttk.Frame(self.notebook)
        self.city_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.phone_frame, text="手机号码处理")
        self.notebook.add(self.city_frame, text="城市区号查询")

        # Build Phone Processing UI
        self.build_phone_processing_ui()

        # Build City Query UI
        self.build_city_query_ui()

    def create_tables(self):
        # Create segment and city tables
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS segments (
                segment TEXT PRIMARY KEY,
                area_code TEXT,
                city TEXT,
                operator TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                area_code TEXT PRIMARY KEY,
                province TEXT,
                city TEXT
            )
        """)
        self.conn.commit()

    def create_menu(self):
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="导入号码段", command=self.import_segments)
        file_menu.add_command(label="导入城市表", command=self.import_cities)
        menu_bar.add_cascade(label="文件", menu=file_menu)
        self.config(menu=menu_bar)

    def import_segments(self):
        file_path = filedialog.askopenfilename(
            title="选择号码段Excel文件",
            filetypes=[("Excel 文件", "*.xls;*.xlsx")]
        )
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path, usecols=[0, 1, 2, 3])  # Only load the first 4 columns
            df.columns = ["segment", "area_code", "city", "operator"]  # Set column names explicitly

            # Insert into database
            df.to_sql("segments", self.conn, if_exists="append", index=False)

            messagebox.showinfo("成功", "号码段数据导入成功！")
        except Exception as e:
            messagebox.showerror("错误", f"号码段导入失败: {str(e)}")

    def import_cities(self):
        file_path = filedialog.askopenfilename(
            title="选择城市表Excel文件",
            filetypes=[("Excel 文件", "*.xls;*.xlsx")]
        )
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path, usecols=[0, 1, 2])  # Only load the first 3 columns
            df.columns = ["area_code", "province", "city"]  # Set column names explicitly

            # Insert into database
            df.to_sql("cities", self.conn, if_exists="append", index=False)

            messagebox.showinfo("成功", "城市表数据导入成功！")
        except Exception as e:
            messagebox.showerror("错误", f"城市表导入失败: {str(e)}")

    def build_phone_processing_ui(self):
        tk.Label(self.phone_frame, text="输入号码或上传文件：").place(x=10, y=10)
        self.phone_input = tk.Text(self.phone_frame, height=10, width=50)
        self.phone_input.place(x=10, y=50, width=200, height=320)

        upload_btn = tk.Button(self.phone_frame, text="上传文件", command=self.upload_file)
        upload_btn.place(x=10, y=380)

        query_btn = tk.Button(self.phone_frame, text="查询", command=self.query_phone_numbers)
        query_btn.place(x=220, y=180)

        export_btn = tk.Button(self.phone_frame, text="导出查询结果", command=self.export_results)
        export_btn.place(x=470, y=380)

        tk.Label(self.phone_frame, text="查询结果：").place(x=290, y=10)
        self.phone_table = ttk.Treeview(self.phone_frame, columns=("号码", "区号", "省份", "城市", "运营商"), show="headings")
        col_width = 500 // 5  # Divide total width evenly among 5 columns
        for col in ("号码", "区号", "省份", "城市", "运营商"):
            self.phone_table.heading(col, text=col)
            self.phone_table.column(col, width=col_width, anchor="center")
        self.phone_table.place(x=280, y=50, width=500, height=320)

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[("文本文件", "*.txt"), ("CSV 文件", "*.csv")]
        )
        if not file_path:
            return

        try:
            if file_path.endswith(".csv"):
                data = pd.read_csv(file_path, header=None)
            elif file_path.endswith(".txt"):
                data = pd.read_csv(file_path, header=None, delimiter="\t")

            numbers = data.iloc[:, 0].astype(str).tolist()
            self.phone_input.delete("1.0", tk.END)
            self.phone_input.insert(tk.END, "\n".join(numbers))
        except Exception as e:
            messagebox.showerror("错误", f"文件读取失败: {str(e)}")

    def query_phone_numbers(self):
        numbers = self.phone_input.get("1.0", tk.END).strip().split("\n")
        self.phone_table.delete(*self.phone_table.get_children())

        for num in numbers:
            if len(num) >= 11:
                phone_number = num[-11:]  # Extract last 11 digits as phone number
                segment = phone_number[:7]  # Extract first 7 digits for query
                self.cursor.execute("SELECT area_code, city, operator FROM segments WHERE segment = ?", (segment,))
                result = self.cursor.fetchone()
                if result:
                    area_code, city, operator = result
                    self.cursor.execute("SELECT province FROM cities WHERE area_code = ?", (area_code,))
                    province = self.cursor.fetchone()
                    province = province[0] if province else "未知"
                    self.phone_table.insert("", tk.END, values=(phone_number, area_code, province, city, operator))

    def export_results(self):
        file_path = filedialog.asksaveasfilename(
            title="导出查询结果",
            defaultextension=".csv",
            filetypes=[("CSV 文件", "*.csv")]
        )
        if not file_path:
            return

        try:
            rows = [self.phone_table.item(item, "values") for item in self.phone_table.get_children()]
            df = pd.DataFrame(rows, columns=["号码", "区号", "省份", "城市", "运营商"])
            df.to_csv(file_path, index=False, encoding="utf-8-sig")
            messagebox.showinfo("成功", "查询结果已导出！")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")

    def build_city_query_ui(self):
        tk.Label(self.city_frame, text="省份列表：").place(x=10, y=10)
        tk.Label(self.city_frame, text="城市列表：").place(x=175, y=10)
        tk.Label(self.city_frame, text="选中城市：").place(x=340, y=10)
        tk.Label(self.city_frame, text="区号查询结果：").place(x=595, y=10)

        self.province_list = tk.Listbox(self.city_frame)
        self.province_list.place(x=10, y=50, width=150, height=300)
        self.province_list.bind("<ButtonRelease-1>", self.update_city_list)
        self.province_list.bind("<Double-Button-1>", self.add_all_cities_from_province)

        self.city_list = tk.Listbox(self.city_frame)
        self.city_list.place(x=175, y=50, width=150, height=300)
        self.city_list.bind("<Double-Button-1>", self.add_city_to_selected)

        self.selected_cities = tk.Listbox(self.city_frame)
        self.selected_cities.place(x=340, y=50, width=150, height=300)

        self.result_text = tk.Text(self.city_frame)
        self.result_text.place(x=595, y=50, height=300, width=185)

        show_code_btn = tk.Button(self.city_frame, text="查询区号", command=self.display_area_codes)
        show_code_btn.place(x=505, y=190, width=60, height=30)

        clear_btn = tk.Button(self.city_frame, text="清空查询结果", command=self.clear_city_query)
        clear_btn.place(x=595, y=370, width=100, height=30)

        clear_selection_btn = tk.Button(self.city_frame, text="清空选中城市", command=self.clear_selected_cities)
        clear_selection_btn.place(x=340, y=370, width=100, height=30)

        self.populate_province_list()

    def populate_province_list(self):
        self.province_list.delete(0, tk.END)
        self.cursor.execute("SELECT DISTINCT province FROM cities")
        provinces = self.cursor.fetchall()
        for province in provinces:
            self.province_list.insert(tk.END, province[0])

    def update_city_list(self, event):
        selected_province = self.province_list.get(self.province_list.curselection())
        self.city_list.delete(0, tk.END)
        self.cursor.execute("SELECT city FROM cities WHERE province = ?", (selected_province,))
        cities = self.cursor.fetchall()
        for city in cities:
            self.city_list.insert(tk.END, city[0])

    def add_all_cities_from_province(self, event):
        selected_province = self.province_list.get(tk.ACTIVE)
        self.cursor.execute("SELECT city FROM cities WHERE province = ?", (selected_province,))
        cities = self.cursor.fetchall()
        for city in cities:
            if city[0] not in self.selected_cities.get(0, tk.END):
                self.selected_cities.insert(tk.END, city[0])

    def add_city_to_selected(self, event):
        selected_city = self.city_list.get(tk.ACTIVE)
        if selected_city not in self.selected_cities.get(0, tk.END):
            self.selected_cities.insert(tk.END, selected_city)

    def display_area_codes(self):
        selected_cities = self.selected_cities.get(0, tk.END)
        codes = []
        for city in selected_cities:
            self.cursor.execute("SELECT area_code FROM cities WHERE city = ?", (city,))
            result = self.cursor.fetchone()
            if result:
                codes.append(result[0])
        codes_str = ", ".join(codes)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, codes_str)

    def clear_city_query(self):
        self.result_text.delete("1.0", tk.END)

    def clear_selected_cities(self):
        self.selected_cities.delete(0, tk.END)


if __name__ == "__main__":
    app = PhoneCityApp()
    app.mainloop()
