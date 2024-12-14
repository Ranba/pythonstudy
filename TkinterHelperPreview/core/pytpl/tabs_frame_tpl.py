from tkinter.ttk import *

from core.utils import place


class TabsFrameTpl:
    def make(self, ele, parent, is_auto_size, root):
        frame = Notebook(root)
        place(frame, ele, parent, is_auto_size)
        return frame

    def make_tabs(self, wgt, root):
        tabs = []
        for tab in wgt.tabs:
            frame = Frame(root)
            root.add(frame, text=tab)
            tabs.append(frame)
        return tabs
