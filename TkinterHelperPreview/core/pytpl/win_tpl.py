from tkinter import *

from core.models import WinModel


class WinTpl:
    def make(self, ele: WinModel, is_auto_size):
        root = Tk()
        root.title(ele.text)
        width = ele.width
        height = ele.height
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(geometry)
        if is_auto_size:
            root.minsize(width, height)
        else:
            root.resizable(width=False, height=False)
        return root
