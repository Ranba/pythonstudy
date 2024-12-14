from ttkbootstrap import Frame

from core.bootpl.utils import merge_style
from core.utils import place


class FrameTpl:
    def make(self, ele, parent, is_auto_size, root):
        frame = Frame(root, bootstyle=merge_style(ele.boot_type, ele.boot_color))
        place(frame, ele, parent, is_auto_size)
        return frame
