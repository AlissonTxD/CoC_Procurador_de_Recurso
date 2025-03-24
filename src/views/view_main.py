from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QMessageBox,QLabel
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from PyQt5 import uic


UI_PATH = "src/views/view_main.ui"

class ToolTipWindow(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setStyleSheet("""
            background-color: #0f0f0f;
            color: white;
            padding: 2px;
            border-radius: 3px;
            font: 87 18pt "Arial Black";
        """)
        self.move(0,0)

class MainGuiView(QMainWindow):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.initialized = False
        return cls.__instance

    def __init__(self, controller = None):
        if not self.initialized:
            super(MainGuiView, self).__init__()
            self.initialized = True
            uic.loadUi(UI_PATH, self)
            self.tooltip_widget = ToolTipWindow("", self)
            self.controller_main = controller

            # Definindo widgets
            self.lineedit_gold: QLineEdit = self.findChild(QLineEdit, "lineedit_gold")
            self.lineedit_elixir = self.findChild(QLineEdit, "lineedit_elixir")
            self.lineedit_dark = self.findChild(QLineEdit, "lineedit_dark")

            self.btn_search = self.findChild(QPushButton, "btn_search")
            self.btn_stop = self.findChild(QPushButton, "btn_stop")

            self.btn_reset_gold = self.findChild(QPushButton, "btn_reset_gold")
            self.btn_reset_elixir = self.findChild(QPushButton, "btn_reset_elixir")
            self.btn_reset_dark = self.findChild(QPushButton, "btn_reset_dark")

            # Configurando Widgets
            self.lineedit_gold.setValidator(QIntValidator())
            self.lineedit_elixir.setValidator(QIntValidator())
            self.lineedit_dark.setValidator(QIntValidator())

            self.lineedit_gold.textChanged.connect(
                lambda: self.__formatar_numero(self.lineedit_gold)
            )
            self.lineedit_elixir.textChanged.connect(
                lambda: self.__formatar_numero(self.lineedit_elixir)
            )
            self.lineedit_dark.textChanged.connect(
                lambda: self.__formatar_numero(self.lineedit_dark)
            )

            self.btn_reset_gold.clicked.connect(lambda: self.__resetar(self.lineedit_gold))
            self.btn_reset_elixir.clicked.connect(
                lambda: self.__resetar(self.lineedit_elixir)
            )
            self.btn_reset_dark.clicked.connect(lambda: self.__resetar(self.lineedit_dark))

            self.btn_search.setEnabled(True)
            self.btn_stop.setEnabled(False)
            self.btn_search.clicked.connect(self.__inicializar_procura_de_vila)
            self.btn_stop.clicked.connect(self.parar)

    def __formatar_numero(self, qlineedit: QLineEdit) -> None:
        """formats the given QLineEdit to a number format.

        Args:
            qlineedit (QLineEdit): QLineEdit to be formatted.
        """
        try:
            numero = qlineedit.text().replace(".", "")
            numero_formatado = "{:,}".format(int(numero)).replace(",", ".")
            qlineedit.setText(numero_formatado)
        except:
            pass

    def __resetar(self, qlineedit: QLineEdit) -> None:
        """resets the given QLineEdit.

        Args:
            qlineedit (QLineEdit): qlinedit to be reseted.
        """
        qlineedit.setText("")

    def popup_erro(self, mensagem: str) -> None:
        """shows a popup with the given message.

        Args:
            mensagem (str): message to be shown.
        """
        msg = QMessageBox()
        msg.setWindowTitle("Erro")
        msg.setText(mensagem)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def tooltip(self, text: str= "") -> None:
        """Shows a tooltip with the given text. If the text is empty, the tooltip is hidden.

        Args:
            text (str, optional): text to be show. Defaults to "".
        """
        if self.tooltip_widget.isVisible() and text == "" or text == "":
            self.tooltip_widget.hide()
        else:
            self.tooltip_widget.setText(text)
            self.tooltip_widget.adjustSize()
            self.tooltip_widget.show()
    
    def __inicializar_procura_de_vila(self)-> None:
        """Enables the stop button and disables the search button. Starts the search.
        """
        self.btn_stop.setEnabled(True)
        self.btn_search.setEnabled(False)
        self.tooltip("Buscando Vilas com Recursos")
        self.controller_main.search()

    def parar(self) -> None:
        """Disables the stop button and enables the search button. Stops the search.
        """
        self.btn_stop.setEnabled(False)
        self.btn_search.setEnabled(True)
        self.tooltip()
        self.controller_main.stop()
