import random
from tkinter import Widget
from tkinter.ttk import Style

from core.models import WidgetModel


def v_scrollbar(vbar, widget, x, y, w, h, pw, ph):
    widget.configure(yscrollcommand=vbar.set)
    vbar.config(command=widget.yview)
    vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')


def h_scrollbar(hbar, widget, x, y, w, h, pw, ph):
    widget.configure(xscrollcommand=hbar.set)
    hbar.config(command=widget.xview)
    hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')


def scrollbar_autohide(vbar, hbar, widget):
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


def place(widget: Widget, info, p_info, is_auto_size: bool):
    if is_auto_size:
        widget.place(relx=info.left / p_info.width,
                     rely=info.top / p_info.height,
                     relwidth=info.width / p_info.width,
                     relheight=info.height / p_info.height
                     )
    else:
        widget.place(x=info.left,
                     y=info.top,
                     width=info.width,
                     height=info.height
                     )


def style_config(wgt: WidgetModel, widget: Widget):
    if wgt.styles is None:
        return

    style = Style()
    ctl = widget.cget('style')
    ctl = "".join(random.sample('zyxwvutsrqponmlkjihgfedcba', 4)) + "." + ctl
    widget.configure(style=ctl)

    _font = ['', 10, []]
    if wgt.styles['font_family']:
        _font[0] = wgt.styles['font_family']
    if wgt.styles['font_size']:
        _font[1] = - int(wgt.styles['font_size'])
    if wgt.styles['font_bold']:
        _font[2].append('bold')
    if wgt.styles['font_italic']:
        _font[2].append('italic')
    if wgt.styles['font_underline']:
        _font[2].append('underline')
    if wgt.styles['font_overstrike']:
        _font[2].append('overstrike')

    font = (_font[0], _font[1], " ".join(_font[2]))
    style.configure(ctl, font=font)
