from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt5.QtGui import QIntValidator
from PyQt5 import uic
from PyQt5.QtCore import QThread

from src.controllers.procurar_vila_controller import ProcuradorDeVila

UI_PATH = "src/views/clash_gui.ui"


class gui_clash(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        # Definindo Variaveis
        self.worker = None
        self.thread2 = None

        # Definindo widgets
        self.lineEdit_gold = self.findChild(QLineEdit, "lineEdit_gold")
        self.lineEdit_elixir = self.findChild(QLineEdit, "lineEdit_elixir")
        self.lineEdit_dark = self.findChild(QLineEdit, "lineEdit_dark")

        self.procurar = self.findChild(QPushButton, "procurar")
        self.parar = self.findChild(QPushButton, "parar")

        self.gold_reset_btn = self.findChild(QPushButton, "reset_gold")
        self.elixir_reset_btn = self.findChild(QPushButton, "reset_elixir")
        self.dark_reset_btn = self.findChild(QPushButton, "reset_dark")

        # Configurando Widgets
        self.lineEdit_gold.setValidator(QIntValidator())
        self.lineEdit_elixir.setValidator(QIntValidator())
        self.lineEdit_dark.setValidator(QIntValidator())

        self.lineEdit_gold.textChanged.connect(
            lambda: self.__formatar_numero(self.lineEdit_gold)
        )
        self.lineEdit_elixir.textChanged.connect(
            lambda: self.__formatar_numero(self.lineEdit_elixir)
        )
        self.lineEdit_dark.textChanged.connect(
            lambda: self.__formatar_numero(self.lineEdit_dark)
        )

        self.gold_reset_btn.clicked.connect(lambda: self.__resetar(self.lineEdit_gold))
        self.elixir_reset_btn.clicked.connect(lambda: self.__resetar(self.lineEdit_elixir))
        self.dark_reset_btn.clicked.connect(lambda: self.__resetar(self.lineEdit_dark))

        self.parar.setEnabled(False)
        self.procurar.clicked.connect(self.__inicializar_procura_de_vila)
        self.parar.clicked.connect(self.__parar)

    def __formatar_numero(self, qlineedit: QLineEdit) -> None:
        try:
            numero = qlineedit.text().replace(".", "")
            numero_formatado = "{:,}".format(int(numero)).replace(",", ".")
            qlineedit.setText(numero_formatado)
        except:
            pass

    def __inicializar_procura_de_vila(self):
        self.parar.setEnabled(True)
        self.procurar.setEnabled(False)
        self.worker = ProcuradorDeVila(self.lineEdit_gold.text(), self.lineEdit_elixir.text(), self.lineEdit_dark.text())
        self.thread2 = QThread()

        self.worker.moveToThread(self.thread2)

        self.thread2.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread2.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread2.finished.connect(self.thread2.deleteLater)
        self.worker.finished.connect(self.__parar)

        self.thread2.start()
        print("começando Procura")

    def __parar(self):
        if self.worker:
            self.worker.stop()
        self.parar.setEnabled(False)
        self.procurar.setEnabled(True)
        print("parou de procurar")

    def __resetar(self, inputbox):
        inputbox.setText("")