"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
from tkinter import font, BooleanVar
from tkinter.ttk import Style

from views.font_view.ui import Win


class Controller:
    # 导入UI类后，替换以下的 object 类型，将获得 IDE 属性提示功能
    ui: Win

    def __init__(self):
        self.stl = None
        self.style = None
        self.underline = None
        self.overstrike = None
        self.italic = None
        self.bold = None

    def init(self, ui):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui
        # TODO 组件初始化 赋值操作

        self.ui.tk_select_box_font_list['values'] = font.families()
        self.ui.tk_select_box_font_list.set("微软雅黑")

        self.ui.tk_input_size.insert(0, 36)
        self.stl = self.ui.tk_label_preview.cget('style')
        self.stl = 'preview.' + self.stl
        self.ui.tk_label_preview.configure(text="字体演示", style=self.stl)

        self.style = Style()

        self.bold = BooleanVar(value=False)
        self.ui.tk_check_button_bold.configure(variable=self.bold, onvalue=True, offvalue=False)

        self.italic = BooleanVar(value=False)
        self.ui.tk_check_button_italic.configure(variable=self.italic, onvalue=True, offvalue=False)

        self.overstrike = BooleanVar(value=False)
        self.ui.tk_check_button_overstrike.configure(variable=self.overstrike, onvalue=True, offvalue=False)

        self.underline = BooleanVar(value=False)
        self.ui.tk_check_button_underline.configure(variable=self.underline, onvalue=True, offvalue=False)

    def on_preview(self, evt):
        family = self.ui.tk_select_box_font_list.get()
        size = self.ui.tk_input_size.get()
        other = []
        if self.bold.get():
            other.append("bold")
        if self.italic.get():
            other.append("italic")
        if self.overstrike.get():
            other.append('overstrike')
        if self.underline.get():
            other.append('underline')

        _font = (family, -int(size), ' '.join(other))
        self.style.configure(self.stl, font=_font)
