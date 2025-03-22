from sys import argv,exit

from PyQt5.QtWidgets import QApplication

from src.views.view_main import MainGuiView


def iniciar() -> None:
    app = QApplication(argv)
    view = MainGuiView(None)
    view.show()
    print("gui mostrada")
    exit(app.exec_())
