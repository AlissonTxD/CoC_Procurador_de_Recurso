from sys import argv,exit

from PyQt5.QtWidgets import QApplication

from src.views.main_gui import MainGuiView
from src.main.constructors.procurar_vila_constructor import ProcuradorDeVilaConstructor


def iniciar() -> None:
    app = QApplication(argv)
    constructor = ProcuradorDeVilaConstructor(None)
    view = MainGuiView(constructor)
    view.show()
    constructor.view = view
    print("gui mostrada")
    exit(app.exec_())
