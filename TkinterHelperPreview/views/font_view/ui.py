"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
from tkinter import *

from pytkUI.locale_zh_cn import zh_cn_initialize
from ttkbootstrap import *


class WinGUI(Window):
    def __init__(self):
        super().__init__(themename="cosmo", hdpi=False)
        # ttkbootstrap 组件本地化
        zh_cn_initialize()
        self.__win()
        self.tk_frame_lpw0mlm7 = self.__tk_frame_lpw0mlm7(self)
        self.tk_select_box_font_list = self.__tk_select_box_font_list(self.tk_frame_lpw0mlm7)
        self.tk_label_lpw0srxb = self.__tk_label_lpw0srxb(self.tk_frame_lpw0mlm7)
        self.tk_label_lpw0svvg = self.__tk_label_lpw0svvg(self.tk_frame_lpw0mlm7)
        self.tk_input_size = self.__tk_input_size(self.tk_frame_lpw0mlm7)
        self.tk_check_button_bold = self.__tk_check_button_bold(self.tk_frame_lpw0mlm7)
        self.tk_check_button_italic = self.__tk_check_button_italic(self.tk_frame_lpw0mlm7)
        self.tk_check_button_underline = self.__tk_check_button_underline(self.tk_frame_lpw0mlm7)
        self.tk_check_button_overstrike = self.__tk_check_button_overstrike(self.tk_frame_lpw0mlm7)
        self.tk_button_on_preview = self.__tk_button_on_preview(self.tk_frame_lpw0mlm7)
        self.tk_frame_lpw0ndk6 = self.__tk_frame_lpw0ndk6(self)
        self.tk_label_preview = self.__tk_label_preview(self.tk_frame_lpw0ndk6)

    def __win(self):
        self.title("Tkinter布局助手")
        # 设置窗口大小、居中
        width = 600
        height = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.resizable(width=False, height=False)

    def scrollbar_autohide(self, vbar, hbar, widget):
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

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    def new_style(self, widget):
        ctl = widget.cget('style')
        ctl = join(random.sample('zyxwvutsrqponmlkjihgfedcba', 5)) + "." + ctl
        widget.configure(style=ctl)
        return ctl

    def __tk_frame_lpw0mlm7(self, parent):
        frame = Frame(parent, bootstyle="default")
        frame.place(x=0, y=0, width=600, height=192)
        return frame

    def __tk_select_box_font_list(self, parent):
        cb = Combobox(parent, state="readonly", bootstyle="default")
        cb['values'] = ("")
        cb.place(x=80, y=30, width=501, height=30)
        return cb

    def __tk_label_lpw0srxb(self, parent):
        label = Label(parent, text="字体", anchor="center", bootstyle="default")
        label.place(x=20, y=30, width=50, height=30)
        return label

    def __tk_label_lpw0svvg(self, parent):
        label = Label(parent, text="大小", anchor="center", bootstyle="default")
        label.place(x=20, y=69, width=47, height=30)
        return label

    def __tk_input_size(self, parent):
        ipt = Entry(parent, bootstyle="default")
        ipt.place(x=81, y=69, width=72, height=30)
        return ipt

    def __tk_check_button_bold(self, parent):
        cb = Checkbutton(parent, text="粗体", bootstyle="default")
        cb.place(x=185, y=68, width=80, height=30)
        return cb

    def __tk_check_button_italic(self, parent):
        cb = Checkbutton(parent, text="斜体", bootstyle="default")
        cb.place(x=288, y=68, width=61, height=30)
        return cb

    def __tk_check_button_underline(self, parent):
        cb = Checkbutton(parent, text="下划线", bootstyle="default")
        cb.place(x=382, y=68, width=80, height=30)
        return cb

    def __tk_check_button_overstrike(self, parent):
        cb = Checkbutton(parent, text="删除线", bootstyle="default")
        cb.place(x=492, y=71, width=80, height=30)
        return cb

    def __tk_button_on_preview(self, parent):
        btn = Button(parent, text="预览", takefocus=False, bootstyle="default")
        btn.place(x=175, y=130, width=247, height=47)
        return btn

    def __tk_frame_lpw0ndk6(self, parent):
        frame = Frame(parent, bootstyle="default")
        frame.place(x=0, y=190, width=600, height=310)
        return frame

    def __tk_label_preview(self, parent):
        label = Label(parent, text="标签", anchor="center", bootstyle="default")
        label.place(x=0, y=0, width=600, height=310)
        return label


class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.ctl.init(self)

    def __event_bind(self):
        self.tk_button_on_preview.bind('<Button-1>', self.ctl.on_preview)
        pass


if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()
