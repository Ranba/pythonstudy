from ttkbootstrap import Notebook, Frame

from core.bootpl.utils import merge_style
from core.utils import place


class TabsFrameTpl:
    def make(self, wgt, parent, is_auto_size, root):
        frame = Notebook(root, bootstyle=merge_style(wgt.boot_type, wgt.boot_color))
        place(frame, wgt, parent, is_auto_size)
        return frame

    def make_tabs(self, wgt, root):
        tabs = []
        for tab in wgt.tabs:
            frame = Frame(root)
            root.add(frame, text=tab)
            tabs.append(frame)
        return tabs
