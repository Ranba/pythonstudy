from tkinter import *
from tkinter.ttk import *

from core.models import WidgetModel
from core.utils import place, v_scrollbar, h_scrollbar, scrollbar_autohide


def create_bar(master, widget, ele, parent):
    vbar, hbar = None, None
    if ele.vbar:
        vbar = Scrollbar(master)
        v_scrollbar(vbar, widget, ele.left, ele.top, ele.width, ele.height, parent.width,
                    parent.height)
    if ele.hbar:
        hbar = Scrollbar(master, orient="horizontal")
        h_scrollbar(hbar, widget, ele.left, ele.top, ele.width, ele.height, parent.width,
                    parent.height)
    scrollbar_autohide(vbar, hbar, widget)


class BaseTpl:
    def __init__(self, root):
        self.root = root

    def tk_button(self, ele: WidgetModel, parent, is_auto_size):
        widget = Button(self.root, text=ele.text, takefocus=False, )
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_input(self, ele, parent, is_auto_size):
        widget = Entry(self.root)
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_label(self, ele, parent, is_auto_size):
        widget = Label(self.root, text=ele.text, anchor="center")
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_text(self, ele: WidgetModel, parent, is_auto_size):
        widget = Text(self.root)
        place(widget, ele, parent, is_auto_size)
        if ele.vbar or ele.hbar: create_bar(self.root, widget, ele, parent)
        return widget

    def tk_canvas(self, ele, parent, is_auto_size):
        widget = Canvas(self.root)
        widget.create_rectangle((0, 0, ele.width - 1, ele.height - 1), fill="#aaa")  # 绘制矩形
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_radio_button(self, ele, parent, is_auto_size):
        widget = Radiobutton(self.root, text=ele.text)
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_check_button(self, ele, parent, is_auto_size):
        widget = Checkbutton(self.root, text=ele.text)
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_list_box(self, ele, parent, is_auto_size):
        widget = Listbox(self.root, highlightthickness=0)
        for option in ele.options:
            widget.insert(END, option)
        place(widget, ele, parent, is_auto_size)
        if ele.vbar or ele.hbar: create_bar(self.root, widget, ele, parent)
        return widget

    def tk_select_box(self, ele, parent, is_auto_size):
        widget = Combobox(self.root)
        widget.configure(values=ele.options)
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_progressbar(self, ele, parent, is_auto_size):
        widget = Progressbar(self.root, maximum=100, value=60)
        orient = HORIZONTAL
        if ele.width < ele.height:
            orient = VERTICAL
        widget.configure(orient=orient)
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_scale(self, ele, parent, is_auto_size):
        widget = Scale(self.root, from_=0, to=100, value=50)
        orient = HORIZONTAL
        if ele.width < ele.height:
            orient = VERTICAL
        widget.configure(orient=orient)
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_table(self, ele, parent, is_auto_size):
        # 表头字段 表头宽度
        columns = dict()
        _width = ele.width - 1
        for e in ele.columns:
            columns[e['name']] = int((e['width'] * _width) / 100)

        # 初始化表格 表格是基于Treeview，tkinter本身没有表格。show="headings" 为隐藏首列。
        widget = Treeview(self.root, show="headings", columns=list(columns))
        for text, width in columns.items():  # 批量设置列属性
            widget.heading(text, text=text, anchor='center')
            widget.column(text, anchor='center', width=width, stretch=False)  # stretch 不自动拉伸

        place(widget, ele, parent, is_auto_size)
        if ele.vbar or ele.hbar: create_bar(self.root, widget, ele, parent)
        return widget
