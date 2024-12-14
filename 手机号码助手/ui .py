"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
import random
from tkinter import *
from tkinter.ttk import *
class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_label_frame_m4kxyyht = self.__tk_label_frame_m4kxyyht(self)
        self.tk_label_m4kxfddq = self.__tk_label_m4kxfddq( self.tk_label_frame_m4kxyyht) 
        self.tk_button_m4kxol1b = self.__tk_button_m4kxol1b( self.tk_label_frame_m4kxyyht) 
        self.tk_table_m4kxipbw = self.__tk_table_m4kxipbw( self.tk_label_frame_m4kxyyht) 
        self.tk_input_m4kxfxva = self.__tk_input_m4kxfxva( self.tk_label_frame_m4kxyyht) 
        self.tk_label_m4kxm40b = self.__tk_label_m4kxm40b( self.tk_label_frame_m4kxyyht) 
        self.tk_button_m4kxhuem = self.__tk_button_m4kxhuem( self.tk_label_frame_m4kxyyht) 
        self.tk_button_m4kyq80g = self.__tk_button_m4kyq80g( self.tk_label_frame_m4kxyyht) 
        self.tk_label_frame_m4ky4w2t = self.__tk_label_frame_m4ky4w2t(self)
        self.tk_list_box_m4ky8nqz = self.__tk_list_box_m4ky8nqz( self.tk_label_frame_m4ky4w2t) 
        self.tk_label_m4ky8uos = self.__tk_label_m4ky8uos( self.tk_label_frame_m4ky4w2t) 
        self.tk_label_m4kyaur7 = self.__tk_label_m4kyaur7( self.tk_label_frame_m4ky4w2t) 
        self.tk_list_box_m4kyb2b7 = self.__tk_list_box_m4kyb2b7( self.tk_label_frame_m4ky4w2t) 
        self.tk_label_m4kycih3 = self.__tk_label_m4kycih3( self.tk_label_frame_m4ky4w2t) 
        self.tk_list_box_m4kycpf8 = self.__tk_list_box_m4kycpf8( self.tk_label_frame_m4ky4w2t) 
        self.tk_text_m4kye8u1 = self.__tk_text_m4kye8u1( self.tk_label_frame_m4ky4w2t) 
        self.tk_label_m4kyek2a = self.__tk_label_m4kyek2a( self.tk_label_frame_m4ky4w2t) 
        self.tk_button_m4kyjbqf = self.__tk_button_m4kyjbqf( self.tk_label_frame_m4ky4w2t) 
        self.tk_button_m4kykh9g = self.__tk_button_m4kykh9g( self.tk_label_frame_m4ky4w2t) 
        self.tk_button_m4kyl3uf = self.__tk_button_m4kyl3uf( self.tk_label_frame_m4ky4w2t)

    def __win(self):
        self.title("Tkinter布局助手")
        # 设置窗口大小、居中
        width = 765
        height = 880
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
    def __tk_label_frame_m4kxyyht(self,parent):
        frame = LabelFrame(parent,text="手机号码处理",)
        frame.place(x=5, y=30, width=755, height=450)
        return frame
    def __tk_label_m4kxfddq(self,parent):
        label = Label(parent,text="手动输入号码",anchor="center", )
        label.place(x=10, y=10, width=100, height=30)
        return label
    def __tk_button_m4kxol1b(self,parent):
        btn = Button(parent, text="导出查询结果", takefocus=False,)
        btn.place(x=650, y=390, width=100, height=30)
        return btn
    def __tk_table_m4kxipbw(self,parent):
        # 表头字段 表头宽度
        columns = {"手机号码":99,"区号":99,"省份":99,"城市":99,"运营商":99}
        tk_table = Treeview(parent, show="headings", columns=list(columns),)
        for text, width in columns.items():  # 批量设置列属性
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', width=width, stretch=False)  # stretch 不自动拉伸
        
        tk_table.place(x=250, y=50, width=500, height=330)
        return tk_table
    def __tk_input_m4kxfxva(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=10, y=50, width=200, height=330)
        return ipt
    def __tk_label_m4kxm40b(self,parent):
        label = Label(parent,text="查询结果",anchor="center", )
        label.place(x=250, y=10, width=100, height=30)
        return label
    def __tk_button_m4kxhuem(self,parent):
        btn = Button(parent, text="上传文件", takefocus=False,)
        btn.place(x=10, y=390, width=100, height=30)
        return btn
    def __tk_button_m4kyq80g(self,parent):
        btn = Button(parent, text="查询", takefocus=False,)
        btn.place(x=250, y=390, width=80, height=30)
        return btn
    def __tk_label_frame_m4ky4w2t(self,parent):
        frame = LabelFrame(parent,text="城市区号查询",)
        frame.place(x=5, y=500, width=755, height=375)
        return frame
    def __tk_list_box_m4ky8nqz(self,parent):
        lb = Listbox(parent)
        
        lb.place(x=10, y=50, width=150, height=260)
        return lb
    def __tk_label_m4ky8uos(self,parent):
        label = Label(parent,text="省份",anchor="center", )
        label.place(x=10, y=10, width=100, height=30)
        return label
    def __tk_label_m4kyaur7(self,parent):
        label = Label(parent,text="城市",anchor="center", )
        label.place(x=170, y=10, width=100, height=30)
        return label
    def __tk_list_box_m4kyb2b7(self,parent):
        lb = Listbox(parent)
        
        lb.place(x=170, y=50, width=150, height=260)
        return lb
    def __tk_label_m4kycih3(self,parent):
        label = Label(parent,text="选中城市",anchor="center", )
        label.place(x=330, y=7, width=100, height=30)
        return label
    def __tk_list_box_m4kycpf8(self,parent):
        lb = Listbox(parent)
        
        lb.place(x=330, y=50, width=150, height=260)
        return lb
    def __tk_text_m4kye8u1(self,parent):
        text = Text(parent)
        text.place(x=500, y=50, width=250, height=260)
        return text
    def __tk_label_m4kyek2a(self,parent):
        label = Label(parent,text="选中城市区号结果",anchor="center", )
        label.place(x=500, y=10, width=150, height=30)
        return label
    def __tk_button_m4kyjbqf(self,parent):
        btn = Button(parent, text="清空选中城市", takefocus=False,)
        btn.place(x=330, y=320, width=100, height=30)
        return btn
    def __tk_button_m4kykh9g(self,parent):
        btn = Button(parent, text="显示区号", takefocus=False,)
        btn.place(x=500, y=320, width=80, height=30)
        return btn
    def __tk_button_m4kyl3uf(self,parent):
        btn = Button(parent, text="清空查询结果", takefocus=False,)
        btn.place(x=670, y=320, width=80, height=30)
        return btn
class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.config(menu=self.create_menu())
        self.ctl.init(self)
    def __event_bind(self):
        pass
    def __style_config(self):
        pass

    def create_menu(self):
        menu = Menu(self,tearoff=False)
        menu.add_cascade(label="文件", menu=menu)
        return menu

if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()