from sys import argv, exit

from PyQt5.QtWidgets import QApplication

from src.views.view_main import MainGuiView
from src.controllers.controller_main import ControllerMain


def iniciar() -> None:
    app = QApplication(argv)
    controller = ControllerMain()
    view = MainGuiView(controller)
    view.show()
    exit(app.exec_())
