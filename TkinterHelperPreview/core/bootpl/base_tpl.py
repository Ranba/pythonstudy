from tkinter import Listbox

from pytkUI.widgets import Icon, TimePicker
from ttkbootstrap import *

from core.bootpl.utils import merge_style
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

    def tk_button(self, ele, parent, is_auto_size):
        widget = Button(self.root, text=ele.text, takefocus=False,
                        bootstyle=merge_style(ele.boot_type, ele.boot_color))
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_input(self, ele, parent, is_auto_size):
        widget = Entry(self.root, bootstyle=merge_style(ele.boot_type, ele.boot_color))
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_label(self, ele, parent, is_auto_size):
        widget = Label(self.root, text=ele.text, anchor="center",
                       bootstyle=merge_style(ele.boot_type, ele.boot_color))
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_text(self, ele, parent, is_auto_size):
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
        widget = Radiobutton(self.root, text=ele.text, bootstyle=merge_style(ele.boot_type, ele.boot_color))
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_check_button(self, ele, parent, is_auto_size):
        widget = Checkbutton(self.root, text=ele.text, bootstyle=merge_style(ele.boot_type, ele.boot_color))
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_list_box(self, ele, parent, is_auto_size):
        widget = Listbox(self.root)
        widget.insert(END, "列表框")
        widget.insert(END, "Python")
        widget.insert(END, "Tkinter Helper")
        place(widget, ele, parent, is_auto_size)
        if ele.vbar or ele.hbar: create_bar(self.root, widget, ele, parent)
        return widget

    def tk_select_box(self, ele, parent, is_auto_size):
        widget = Combobox(self.root,
                          bootstyle=merge_style(ele.boot_type, ele.boot_color))
        widget.configure(values=ele.options)
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_progressbar(self, ele, parent, is_auto_size):
        orient = HORIZONTAL
        if ele.width < ele.height:
            orient = VERTICAL
        widget = Progressbar(self.root, orient=orient, bootstyle=merge_style(ele.boot_type, ele.boot_color),
                             maximum=100, value=60)
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_scale(self, ele, parent, is_auto_size):
        orient = HORIZONTAL
        if ele.width < ele.height:
            orient = VERTICAL
        widget = Scale(self.root, orient=orient, from_=0, to=100, value=50,
                       bootstyle=merge_style(ele.boot_type, ele.boot_color))
        place(widget, ele, parent, is_auto_size)
        return widget

    def tb_meter(self, ele, parent, is_auto_size):
        widget = Meter(self.root, bootstyle=merge_style(
            ele.boot_type, ele.boot_color), amountused=100, amounttotal=100, subtext=ele.sub_text,
                       metersize=ele.width,
                       textleft=ele.text_left, textright=ele.text_right, interactive=ele.interactive)
        place(widget, ele, parent, is_auto_size)
        return widget

    def tk_table(self, ele, parent, is_auto_size):
        # 表头字段 表头宽度
        columns = dict()
        for column in ele.columns:
            columns[column['name']] = int((column['width'] * ele.width) / 100)

        # 初始化表格 表格是基于Treeview，tkinter本身没有表格。show="headings" 为隐藏首列。
        widget = Treeview(self.root, show="headings", columns=list(columns),
                          bootstyle=merge_style(ele.boot_type, ele.boot_color))
        for text, width in columns.items():  # 批量设置列属性
            widget.heading(text, text=text, anchor='center')
            widget.column(text, anchor='center', width=width, stretch=False)  # stretch 不自动拉伸

        place(widget, ele, parent, is_auto_size)
        if ele.vbar or ele.hbar: create_bar(self.root, widget, ele, parent)
        return widget

    def ext_icon(self, ele, parent, is_auto_size):
        widget = Icon(self.root, icon_name=ele.icon, size=int(ele.width * 0.9), color=ele.color)
        place(widget, ele, parent, is_auto_size)
        return widget

    def tb_date_input(self, ele, parent, is_auto_size):
        widget = DateEntry(self.root, width=1, bootstyle=merge_style(ele.boot_type, ele.boot_color))
        place(widget, ele, parent, is_auto_size)
        return widget

    def ext_time_input(self, ele, parent, is_auto_size):
        widget = TimePicker(self.root, bootstyle=merge_style(ele.boot_type, ele.boot_color))
        place(widget, ele, parent, is_auto_size)
        return widget
