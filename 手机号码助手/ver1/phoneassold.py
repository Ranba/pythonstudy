import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd


class PhoneCityApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("手机号码处理与城市区号查询")
        self.geometry("800x600")
        self.resizable(False, False)

        # Database connection
        self.conn = sqlite3.connect("phone_city.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Menu bar
        self.create_menu()

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

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
        ttk.Label(self.phone_frame, text="输入号码或上传文件：").pack(pady=5)
        self.phone_input = tk.Text(self.phone_frame, height=10, width=50)
        self.phone_input.pack()

        upload_btn = ttk.Button(self.phone_frame, text="上传文件", command=self.upload_file)
        upload_btn.pack(pady=5)

        query_btn = ttk.Button(self.phone_frame, text="查询", command=self.query_phone_numbers)
        query_btn.pack(pady=5)

        export_btn = ttk.Button(self.phone_frame, text="导出查询结果", command=self.export_results)
        export_btn.pack(pady=5)

        self.phone_table = ttk.Treeview(self.phone_frame, columns=("号码", "区号", "省份", "城市", "运营商"),
                                        show="headings")
        for col in ("号码", "区号", "省份", "城市", "运营商"):
            self.phone_table.heading(col, text=col)
        self.phone_table.pack(fill="both", expand=True)

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
                    self.cursor.execute("SELECT province FROM cities WHERE city = ?", (city,))
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
        ttk.Label(self.city_frame, text="省份列表：").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.city_frame, text="城市列表：").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.city_frame, text="选中城市：").grid(row=0, column=2, padx=5, pady=5)

        self.province_list = tk.Listbox(self.city_frame)
        self.province_list.grid(row=1, column=0, padx=5, pady=5)

        self.city_list = tk.Listbox(self.city_frame)
        self.city_list.grid(row=1, column=1, padx=5, pady=5)

        self.selected_cities = tk.Listbox(self.city_frame)
        self.selected_cities.grid(row=1, column=2, padx=5, pady=5)

        show_code_btn = ttk.Button(self.city_frame, text="显示区号", command=self.display_area_codes)
        show_code_btn.grid(row=2, column=0, pady=10)

        clear_btn = ttk.Button(self.city_frame, text="清空查询结果", command=self.clear_city_query)
        clear_btn.grid(row=2, column=1, pady=10)

        clear_selection_btn = ttk.Button(self.city_frame, text="清空选中城市", command=self.clear_selected_cities)
        clear_selection_btn.grid(row=2, column=2, pady=10)

    def display_area_codes(self):
        selected_cities = self.selected_cities.get(0, tk.END)
        codes = []
        for city in selected_cities:
            self.cursor.execute("SELECT area_code FROM cities WHERE city = ?", (city,))
            result = self.cursor.fetchone()
            if result:
                codes.append(result[0])
        codes_str = ", ".join(codes)
        messagebox.showinfo("查询结果", f"区号: {codes_str}")

    def clear_city_query(self):
        self.selected_cities.delete(0, tk.END)

    def clear_selected_cities(self):
        self.selected_cities.delete(0, tk.END)


if __name__ == "__main__":
    app = PhoneCityApp()
    app.mainloop()
