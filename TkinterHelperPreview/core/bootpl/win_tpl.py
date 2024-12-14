from ttkbootstrap import Window


class WinTpl:
    def make(self, win, is_auto_size):
        root = Window(hdpi=False, themename=win.ttkbootstrap_theme)
        root.title(win.text)
        width = win.width
        height = win.height
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(geometry)
        if is_auto_size:
            root.minsize(width, height)
        else:
            root.resizable(width=False, height=False)
        return root
