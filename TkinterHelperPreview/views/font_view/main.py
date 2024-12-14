from views.font_view.controller import Controller as MainController
from views.font_view.ui import Win as MainWin


def run():
    app = MainWin(MainController())
    app.mainloop()


if __name__ == '__main__':
    run()
