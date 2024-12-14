from tkinter import *
from tkinter.ttk import *

from core.utils import place


class FrameTpl:
    def make(self, ele, parent, is_auto_size, root):
        frame = Frame(root)
        place(frame, ele, parent, is_auto_size)
        return frame
