import multiprocessing
import webbrowser
from multiprocessing import active_children

import pystray as pystray
from pystray import MenuItem, Menu
from pytkUI.utils import draw_icon

from config import version, update_url, helper_url


def create_tray_menu():
    menu = (
        MenuItem(text="布局助手", action=on_start),
        MenuItem(text="检测更新", action=on_update),
        Menu.SEPARATOR,
        MenuItem(text="ttkbootstrap", action=lambda: multiprocessing.Process(target=on_ttkbootstrap).start()),
        Menu.SEPARATOR,
        MenuItem(text="系统字体", action=lambda: multiprocessing.Process(target=on_font).start()),
        Menu.SEPARATOR,
        MenuItem(text='退出', action=on_exit),
    )
    image = draw_icon(62177, 20, "#44BB86")
    msg = f"Tkinter布局助手\n预览服务已启动\nV{version}"

    return pystray.Icon("name", image, msg, menu)


def on_exit(icon: pystray.Icon):
    # 关闭http服务进程
    for p in active_children():
        if p.name == "api_server":
            p.kill()

    icon.stop()


def on_update():
    webbrowser.open(update_url)


def on_start():
    webbrowser.open(helper_url)


def on_ttkbootstrap():
    import ttkbootstrap
    from ttkbootstrap.__main__ import setup_demo
    ttkdemo = ttkbootstrap.Window("ttkbootstrap 组件演示")

    bagel = setup_demo(ttkdemo)
    bagel.pack(fill='both', expand='yes')
    ttkdemo.mainloop()


def on_font():
    from views.font_view.main import run
    run()
