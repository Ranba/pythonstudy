from operator import methodcaller
from tkinter import Menu

from core.models import TkModel, WinModel
from core.utils import style_config


class GenerateWin:
    def __init__(self, tk: TkModel):
        self.tk: TkModel = tk
        self.maps = {}

    def build(self):
        win = self.tk.win
        if win.is_ttkbootstrap:
            from core.bootpl.base_tpl import BaseTpl
            from core.bootpl.frame_tpl import FrameTpl
            from core.bootpl.label_frame_tpl import LabelFrameTpl
            from core.bootpl.tabs_frame_tpl import TabsFrameTpl
            from core.bootpl.win_tpl import WinTpl
            from core.bootpl.ext_tabs_frame_tpl import ExtTabsFrameTpl
            self.maps = {
                'tk_frame': FrameTpl(),
                'tk_label_frame': LabelFrameTpl(),
                'tk_tabs': TabsFrameTpl(),
                'ext_tabs': ExtTabsFrameTpl(),
                'BaseTpl': BaseTpl,
                'WinTpl': WinTpl
            }
        else:
            from core.pytpl.base_tpl import BaseTpl
            from core.pytpl.frame_tpl import FrameTpl
            from core.pytpl.label_frame_tpl import LabelFrameTpl
            from core.pytpl.tabs_frame_tpl import TabsFrameTpl
            from core.pytpl.win_tpl import WinTpl
            self.maps = {
                'tk_frame': FrameTpl(),
                'tk_label_frame': LabelFrameTpl(),
                'tk_tabs': TabsFrameTpl(),
                'BaseTpl': BaseTpl,
                'WinTpl': WinTpl
            }
        root = self.maps['WinTpl']().make(win, win.is_auto_size)
        if win.is_ttkbootstrap:
            from pytkUI.locale_zh_cn import zh_cn_initialize
            zh_cn_initialize()
        root.attributes("-topmost", True)
        self.create_elements(elements=win.elements, parent=win, top=win, root=root)
        if len(win.menus) > 0:
            root.config(menu=self.create_menu(win.menus, root))
        root.mainloop()

    def create_elements(self, elements, parent, top: WinModel, root):
        base_tpl = self.maps['BaseTpl'](root)
        for wgt in elements:
            if wgt.frame is True:
                if wgt.type == 'tk_tabs':
                    frame = self.maps[wgt.type].make(wgt, parent, top.is_auto_size, root)
                    tabs = self.maps[wgt.type].make_tabs(wgt, frame)
                    tabs_elements = wgt.elements
                    for tab_index, tab in enumerate(tabs):
                        self.create_elements(elements=[e for e in tabs_elements if e.tab == tab_index],
                                             parent=wgt,
                                             top=top,
                                             root=tab)
                elif wgt.type == 'ext_tabs':
                    frame = self.maps[wgt.type].make(wgt, parent, top.is_auto_size, root)
                    tabs = self.maps[wgt.type].make_tabs(wgt, frame)
                    tabs_elements = wgt.elements
                    for tab_index, tab in enumerate(tabs):
                        self.create_elements(elements=[e for e in tabs_elements if e.tab == tab_index],
                                             parent=wgt,
                                             top=top,
                                             root=tab)
                else:
                    frame = self.maps[wgt.type].make(wgt, parent, top.is_auto_size, root)

                    self.create_elements(elements=wgt.elements, parent=wgt, top=top, root=frame)

            else:
                caller = methodcaller(wgt.type, wgt, parent, top.is_auto_size)
                widget = caller(base_tpl)
                if top.is_ttkbootstrap:
                    style_config(wgt, widget)

    def create_menu(self, menus, root):
        menu_obj = Menu(root, tearoff=False)
        for menu in menus:
            if 'children' in menu.keys():
                submenu = self.create_submenu(menu['children'], menu_obj)
                menu_obj.add_cascade(label=menu['name'], menu=submenu)
            else:
                menu_obj.add_command(label=menu['name'])
        return menu_obj

    def create_submenu(self, menus, parent):
        menu_obj = Menu(parent, tearoff=False)
        for menu in menus:
            if 'children' in menu.keys():
                submenu = self.create_submenu(menu['children'], menu_obj)
                menu_obj.add_cascade(label=menu['name'], menu=submenu)
            else:
                menu_obj.add_command(label=menu['name'])
        return menu_obj
