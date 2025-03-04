from sys import argv

from PyQt5.QtWidgets import QApplication

from src.views.main_gui import gui_clash


def iniciar() -> None:
    app = QApplication(argv)
    view = gui_clash()
    view.show()
    app.exec_()
