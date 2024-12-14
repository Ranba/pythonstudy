from tkinter import Frame

from pytkUI.ext.ext_tabs import ExtTabs, TabItem

from core.utils import place


class ExtTabsFrameTpl:
    def make(self, ele, parent, is_auto_size, root):
        frame = ExtTabs(root)
        place(frame, ele, parent, is_auto_size)
        return frame

    def make_tabs(self, ele, root):
        tabs = []
        frames = []
        for tab in ele.tabs:
            frame = Frame(root)
            tabObj = TabItem(tab['icon'], tab['label'], frame)
            tabs.append(tabObj)
            frames.append(frame)
        root.init(tabs=tabs)
        return frames
