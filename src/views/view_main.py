from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QMessageBox, QLabel
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from PyQt5 import uic

from src.models.model_ocr_loader import OCRLoader
from src.utils import resource_path

UI_PATH = resource_path("src/views/view_main.ui")


class ToolTipWindow(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setStyleSheet(
            """
            background-color: #0f0f0f;
            color: white;
            padding: 2px;
            border-radius: 3px;
            font: 87 18pt "Arial Black";
        """
        )
        self.move(0, 0)


class MainGuiView(QMainWindow):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.initialized = False
        return cls.__instance

    def __init__(self, controller=None):
        if not self.initialized:
            super(MainGuiView, self).__init__()
            self.initialized = True
            uic.loadUi(UI_PATH, self)
            self.tooltip_widget = ToolTipWindow("", self)
            self.controller_main = controller
            self.ocr = None
            self.minimum = ()

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

            self.btn_reset_gold.clicked.connect(
                lambda: self.__resetar(self.lineedit_gold)
            )
            self.btn_reset_elixir.clicked.connect(
                lambda: self.__resetar(self.lineedit_elixir)
            )
            self.btn_reset_dark.clicked.connect(
                lambda: self.__resetar(self.lineedit_dark)
            )

            self.btn_search.setEnabled(False)
            self.btn_stop.setEnabled(False)
            self.btn_search.clicked.connect(self.__inicializar_procura_de_vila)
            self.btn_stop.clicked.connect(self.parar)

            self.start_ocr_load()

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

    def popup_error(self, mensagem: str) -> None:
        """shows a popup with the given message.

        Args:
            mensagem (str): message to be shown.
        """
        msg = QMessageBox()
        msg.setWindowTitle("Erro")
        msg.setText(mensagem)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def tooltip(self, text: str = "") -> None:
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

    def __inicializar_procura_de_vila(self) -> None:
        """Starts the search."""
        if self.__verify_emptiness():
            self.popup_error("Por favor, coloque pelomenos 1 valor para a procura")
            return
        self.minimum = self.__return_inputs()
        self.controller_main.search(self.ocr)

    def parar(self) -> None:
        """Disables the stop button and enables the search button. Stops the search."""
        self.btn_stop.setEnabled(False)
        self.btn_search.setEnabled(True)
        self.tooltip()
        self.controller_main.stop()

    def __return_inputs(self):
        input_tuple = (
            self.lineedit_gold.text(),
            self.lineedit_elixir.text(),
            self.lineedit_dark.text(),
        )
        return input_tuple

    def __verify_emptiness(self):
        gold_input_is_empty = self.lineedit_gold.text() == ""
        elixir_input_is_empty = self.lineedit_elixir.text() == ""
        dark_input_is_empty = self.lineedit_dark.text() == ""
        if gold_input_is_empty and elixir_input_is_empty and dark_input_is_empty:
            return True

    def start_ocr_load(self):
        self.worker = OCRLoader()
        self.worker.loaded.connect(self.on_ocr_loaded)
        self.worker.error.connect(self.on_ocr_error)
        self.worker.start()  # Inicia a thread
        print("Carregando OCR em segundo plano...")

    def on_ocr_loaded(self, ocr_instance):
        self.ocr = ocr_instance
        self.btn_search.setText("Procurar")
        self.btn_search.setEnabled(True)

    def on_ocr_error(self, error_msg):
        self.popup_error(f"Erro: {error_msg}")
