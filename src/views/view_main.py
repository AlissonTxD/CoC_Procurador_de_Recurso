from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QIntValidator
from PyQt5 import uic


UI_PATH = "src/views/clash_gui.ui"


class MainGuiView(QMainWindow):
    def __init__(self, constructor):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self.constructor = constructor

        # Definindo widgets
        self.lineEdit_gold = self.findChild(QLineEdit, "lineEdit_gold")
        self.lineEdit_elixir = self.findChild(QLineEdit, "lineEdit_elixir")
        self.lineEdit_dark = self.findChild(QLineEdit, "lineEdit_dark")

        self.btn_procurar = self.findChild(QPushButton, "procurar")
        self.btn_parar = self.findChild(QPushButton, "parar")

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
        self.elixir_reset_btn.clicked.connect(
            lambda: self.__resetar(self.lineEdit_elixir)
        )
        self.dark_reset_btn.clicked.connect(lambda: self.__resetar(self.lineEdit_dark))

        self.btn_parar.setEnabled(True)
        self.btn_procurar.setEnabled(True)
        self.btn_procurar.clicked.connect(self.__inicializar_procura_de_vila)
        self.btn_parar.clicked.connect(self.__parar)

    def __formatar_numero(self, qlineedit: QLineEdit) -> None:
        try:
            numero = qlineedit.text().replace(".", "")
            numero_formatado = "{:,}".format(int(numero)).replace(",", ".")
            qlineedit.setText(numero_formatado)
        except:
            pass

    def __resetar(self, qlineedit: QLineEdit):
        qlineedit.setText("")

    def popup_erro(self, mensagem):
        msg = QMessageBox()
        msg.setWindowTitle("Erro")
        msg.setText(mensagem)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def __inicializar_procura_de_vila(self):
        print("inicando procura de vila")

    def __parar(self):
        print("parou")
