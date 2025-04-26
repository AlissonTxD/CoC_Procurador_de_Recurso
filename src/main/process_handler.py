from sys import argv, exit
import logging

from PyQt5.QtWidgets import QApplication

from src.views.view_main import MainGuiView
from src.controllers.controller_main import ControllerMain


def iniciar() -> None:
    logging.getLogger('ppocr').setLevel(logging.CRITICAL)
    logging.getLogger('paddle').setLevel(logging.CRITICAL)
    logging.getLogger().setLevel(logging.CRITICAL) 
    app = QApplication(argv)
    controller = ControllerMain()
    view = MainGuiView(controller)
    view.show()
    view.raise_()
    view.activateWindow()
    exit(app.exec_())
