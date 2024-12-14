from tkinter import *
from tkinter.ttk import *

from core.utils import place


class LabelFrameTpl:
    def make(self, wgt, parent, is_auto_size, root):
        frame = LabelFrame(root, text=wgt.text)
        place(frame, wgt, parent, is_auto_size)
        return frame
