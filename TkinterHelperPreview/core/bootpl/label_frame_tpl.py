from ttkbootstrap import LabelFrame

from core.bootpl.utils import merge_style
from core.utils import place


class LabelFrameTpl:
    def make(self, ele, parent, is_auto_size, root):
        frame = LabelFrame(root, text=ele.text, bootstyle=merge_style(ele.boot_type, ele.boot_color))
        place(frame, ele, parent, is_auto_size)
        return frame
