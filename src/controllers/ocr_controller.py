from PyQt5.QtCore import QThread, pyqtSignal

class OCRLoaderThread(QThread):
    ocr_loaded = pyqtSignal(object)  # Sinal para emitir o objeto PaddleOCR carregado

    def run(self):
        # Carrega o PaddleOCR em uma thread separada
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang="en")
        self.ocr_loaded.emit(ocr)  # Emite o objeto carregado