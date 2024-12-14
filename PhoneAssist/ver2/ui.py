"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
import random
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

import sqlite3

class Database:
    def __init__(self, db_name="phone_assistant.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS phone_segments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                segment TEXT NOT NULL,
                area_code TEXT NOT NULL,
                city TEXT NOT NULL,
                operator TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_name TEXT NOT NULL,
                area_code TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def close(self):
        self.conn.close()

def open_file_dialog(self):
    file_path = filedialog.askopenfilename(filetypes=[("所有文件", "*.*")])
    if file_path:
        print(f"选择的文件: {file_path}")
        return file_path
    return None


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.province_listbox = None  # 初始化省份列表框为 None
        self.__win()
        self.tk_tabs_m4m4kuj3 = self.__tk_tabs_m4m4kuj3(self)
        self.tk_label_m4m4kzsr = self.__tk_label_m4m4kzsr( self.tk_tabs_m4m4kuj3_0)
        self.tk_text_m4m4l3ks = self.__tk_text_m4m4l3ks( self.tk_tabs_m4m4kuj3_0)
        self.tk_button_m4m4l7ba = self.__tk_button_m4m4l7ba( self.tk_tabs_m4m4kuj3_0)
        self.tk_table_m4m4l9xt = self.__tk_table_m4m4l9xt( self.tk_tabs_m4m4kuj3_0)
        self.tk_button_m4m4lfqn = self.__tk_button_m4m4lfqn( self.tk_tabs_m4m4kuj3_0)
        self.tk_button_m4m4lhjh = self.__tk_button_m4m4lhjh( self.tk_tabs_m4m4kuj3_0)
        self.tk_list_box_m4m4lod9 = self.__tk_list_box_m4m4lod9( self.tk_tabs_m4m4kuj3_1)
        self.tk_list_box_m4m4lq6l = self.__tk_list_box_m4m4lq6l( self.tk_tabs_m4m4kuj3_1)
        self.tk_list_box_m4m4lrja = self.__tk_list_box_m4m4lrja( self.tk_tabs_m4m4kuj3_1)
        self.tk_label_m4m4st6h = self.__tk_label_m4m4st6h( self.tk_tabs_m4m4kuj3_0)
        self.tk_label_m4m4vy5m = self.__tk_label_m4m4vy5m( self.tk_tabs_m4m4kuj3_1)
        self.tk_label_m4m4w0ak = self.__tk_label_m4m4w0ak( self.tk_tabs_m4m4kuj3_1)
        self.tk_label_m4m4w2a1 = self.__tk_label_m4m4w2a1( self.tk_tabs_m4m4kuj3_1)
        self.tk_label_m4m4w42r = self.__tk_label_m4m4w42r( self.tk_tabs_m4m4kuj3_1)
        self.tk_button_m4m52n3t = self.__tk_button_m4m52n3t( self.tk_tabs_m4m4kuj3_1)
        self.tk_text_m4m54np9 = self.__tk_text_m4m54np9( self.tk_tabs_m4m4kuj3_1)
        self.tk_button_m4m55wky = self.__tk_button_m4m55wky( self.tk_tabs_m4m4kuj3_1)
        self.tk_button_m4m56ffb = self.__tk_button_m4m56ffb( self.tk_tabs_m4m4kuj3_1)
        self.tk_button_m4m4m82p = self.__tk_button_m4m4m82p(self)
        self.tk_button_m4m4m9qw = self.__tk_button_m4m4m9qw(self)
        self._event_bind()
        self.__style_config()
    def __win(self):
        self.title("手机号码助手")
        # 设置窗口大小、居中
        width = 800
        height = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        
        self.resizable(width=False, height=False)
        
    def scrollbar_autohide(self,vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def __tk_tabs_m4m4kuj3(self,parent):
        frame = Notebook(parent)
        self.tk_tabs_m4m4kuj3_0 = self.__tk_frame_m4m4kuj3_0(frame)
        frame.add(self.tk_tabs_m4m4kuj3_0, text="手机号码处理")
        self.tk_tabs_m4m4kuj3_1 = self.__tk_frame_m4m4kuj3_1(frame)
        frame.add(self.tk_tabs_m4m4kuj3_1, text="城市区号查询")
        frame.place(x=5, y=50, width=790, height=440)
        return frame
    def __tk_frame_m4m4kuj3_0(self,parent):
        frame = Frame(parent)
        frame.place(x=5, y=50, width=790, height=440)
        return frame
    def __tk_frame_m4m4kuj3_1(self,parent):
        frame = Frame(parent)
        frame.place(x=5, y=50, width=790, height=440)
        return frame
    def __tk_label_m4m4kzsr(self,parent):
        label = Label(parent,text="输入或上传号码",anchor="center", )
        label.place(x=10, y=10, width=100, height=30)
        return label
    def __tk_text_m4m4l3ks(self,parent):
        text = Text(parent)
        text.place(x=10, y=50, width=200, height=320)
        return text
    def __tk_button_m4m4l7ba(self,parent):
        btn = Button(parent, text="上传文件", takefocus=False,)
        btn.place(x=10, y=380, width=100, height=30)
        return btn
    def __tk_table_m4m4l9xt(self,parent):
        # 表头字段 表头宽度
        columns = {"手机号码":99,"区号":99,"省份":99,"城市":99,"运营商":99}
        tk_table = Treeview(parent, show="headings", columns=list(columns),)
        for text, width in columns.items():  # 批量设置列属性
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', width=width, stretch=False)  # stretch 不自动拉伸
        
        tk_table.place(x=290, y=50, width=500, height=320)
        return tk_table
    def __tk_button_m4m4lfqn(self,parent):
        btn = Button(parent, text="查询", takefocus=False,)
        btn.place(x=220, y=180, width=60, height=30)
        return btn
    def __tk_button_m4m4lhjh(self,parent):
        btn = Button(parent, text="导出查询结果", takefocus=False,)
        btn.place(x=470, y=380, width=150, height=30)
        return btn
    def __tk_list_box_m4m4lod9(self,parent):
        lb = Listbox(parent)
        
        lb.place(x=10, y=50, width=150, height=300)
        return lb
    def __tk_list_box_m4m4lq6l(self,parent):
        lb = Listbox(parent)
        
        lb.place(x=175, y=50, width=150, height=300)
        return lb
    def __tk_list_box_m4m4lrja(self,parent):
        lb = Listbox(parent)
        
        lb.place(x=340, y=50, width=150, height=300)
        return lb
    def __tk_label_m4m4st6h(self,parent):
        label = Label(parent,text="查询结果",anchor="center", )
        label.place(x=290, y=10, width=100, height=30)
        return label
    def __tk_label_m4m4vy5m(self,parent):
        label = Label(parent,text="省份列表",anchor="center", )
        label.place(x=10, y=10, width=100, height=30)
        self.province_listbox = Listbox(parent)  # 确保 province_listbox 被正确初始化
        self.province_listbox.place(x=10, y=50, width=150, height=300)
        return label
    def __tk_label_m4m4w0ak(self,parent):
        label = Label(parent,text="城市列表",anchor="center", )
        label.place(x=175, y=10, width=100, height=30)
        return label
    def __tk_label_m4m4w2a1(self,parent):
        label = Label(parent,text="选中城市",anchor="center", )
        label.place(x=340, y=10, width=100, height=30)
        return label
    def __tk_label_m4m4w42r(self,parent):
        label = Label(parent,text="选中城市区号",anchor="center", )
        label.place(x=595, y=10, width=100, height=30)
        return label
    def __tk_button_m4m52n3t(self,parent):
        btn = Button(parent, text="清空选中城市", takefocus=False,)
        btn.place(x=340, y=370, width=100, height=30)
        return btn
    def __tk_text_m4m54np9(self,parent):
        text = Text(parent)
        text.place(x=595, y=50, width=185, height=300)
        return text
    def __tk_button_m4m55wky(self,parent):
        btn = Button(parent, text="清空查询结果", takefocus=False,)
        btn.place(x=595, y=370, width=100, height=30)
        return btn
    def __tk_button_m4m56ffb(self,parent):
        btn = Button(parent, text="查询区号", takefocus=False,)
        btn.place(x=505, y=190, width=80, height=30)
        return btn
    def __tk_button_m4m4m82p(self,parent):
        btn = Button(parent, text="导入号段表", takefocus=False,)
        btn.place(x=10, y=10, width=100, height=30)
        return btn
    def __tk_button_m4m4m9qw(self,parent):
        btn = Button(parent, text="导入城市表", takefocus=False,)
        btn.place(x=120, y=10, width=100, height=30)
        return btn
    def _event_bind(self):
        self.tk_button_m4m4l7ba.bind('<Button-1>', self.ctl.upload_file_to_input)
        self.tk_button_m4m4lfqn.bind('<Button-1>', self.ctl.process_numbers)
        self.tk_button_m4m4lhjh.bind('<Button-1>', self.ctl.export_results)
        self.tk_button_m4m52n3t.bind('<Button-1>', self.ctl.clear_selected_cities)
        self.tk_button_m4m55wky.bind('<Button-1>', self.ctl.clear_results)
        self.tk_button_m4m56ffb.bind('<Button-1>', self.ctl.display_area_codes)
        self.tk_button_m4m4m82p.bind('<Button-1>', self.ctl.import_segments)
        self.tk_button_m4m4m9qw.bind('<Button-1>', self.ctl.import_cities)
        pass
class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.db = Database()  # 创建数据库实例
        self._event_bind()
        self.__style_config()
        self.ctl.init(self)
        
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()
    def __style_config(self):
        pass
if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()