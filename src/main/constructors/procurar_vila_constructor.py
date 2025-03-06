from PyQt5.QtCore import QThread

from src.controllers.procurar_vila_controller import ProcuradorDeVilaController
from src.views.main_gui import MainGuiView
from src.controllers.ocr_controller import OCRLoaderThread


class ProcuradorDeVilaConstructor:
    def __init__(self, view: MainGuiView):
        self.view = view
        self.worker = None
        self.thread = None
        self.ocr = None
        self.ocr_loader_thread = OCRLoaderThread()
        self.ocr_loader_thread.ocr_loaded.connect(self.__salvar_ocr)
        self.ocr_loader_thread.start()

    def iniciar_procura(self):
        try:
            self.view.btn_procurar.setEnabled(False)
            ouro_minimo, elixir_minimo, dark_minimo = self.__recuperar_dados_da_view()
            self.worker = ProcuradorDeVilaController(
                ouro_minimo, elixir_minimo, dark_minimo,self.ocr
            )
            self.thread = QThread()
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.erro.connect(self.__mostrar_erro)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.finished.connect(self.parar)
            self.thread.start()
            print("começando thread")
            self.view.btn_parar.setEnabled(True)
        except Exception as ex:
            self.__mostrar_erro(ex)

    def parar(self):
        if self.worker:
            print("parou de procurar")
            self.worker.stop()
        self.view.btn_parar.setEnabled(False)
        self.view.btn_procurar.setEnabled(True)

    def __recuperar_dados_da_view(self):
        gold = self.view.lineEdit_gold.text()
        elixir = self.view.lineEdit_elixir.text()
        dark = self.view.lineEdit_dark.text()
        return gold, elixir, dark

    def __mostrar_erro(self, msg):
        self.view.popup_erro(msg)

    def __salvar_ocr(self, ocr):
        self.ocr = ocr
        print("ocr carregado")
        self.view.btn_procurar.setEnabled(True)
