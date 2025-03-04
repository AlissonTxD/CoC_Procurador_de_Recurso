from time import sleep
from PyQt5.QtCore import QObject,pyqtSignal

class ProcuradorDeVila(QObject):
    finished = pyqtSignal()

    def __init__(self, ouro_minimo, elixir_minimo, dark_minimo):
        super().__init__()
        self.ouro_minimo = ouro_minimo
        self.elixir_minimo = elixir_minimo
        self.dark_minimo = dark_minimo
        self.rodando = True
    
    def run(self):
        print(self.ouro_minimo, self.elixir_minimo, self.dark_minimo)
        while self.rodando:
            for i in range(40):
                print(i)
                sleep(0.5)
                if not self.rodando: break
            self.stop()
        self.finished.emit()

    def stop(self):
        self.rodando = False


