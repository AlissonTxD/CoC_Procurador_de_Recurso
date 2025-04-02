from PyQt5.QtCore import QThread, pyqtSignal


class OCRLoader(QThread):
    loaded = pyqtSignal(object)  # Envia a instância do OCR quando pronto
    error = pyqtSignal(str)  # Envia mensagem de erro

    def run(self):
        try:
            # Import DENTRO da thread (isso é o pulo do gato)
            from paddleocr import PaddleOCR

            ocr = PaddleOCR(use_angle_cls=True, lang="pt")
            self.loaded.emit(ocr)
        except Exception as e:
            self.error.emit(f"Erro ao carregar OCR: {str(e)}")
