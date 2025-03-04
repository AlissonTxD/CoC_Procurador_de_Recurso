from collections import namedtuple
from time import sleep

from PyQt5.QtCore import QObject, pyqtSignal


class ProcuradorDeVila(QObject):
    # Carregamento de Coordenadas
    Coord = namedtuple("Coord", "x y")
    CoordCorte = namedtuple("Corte", "x1 y1 x2 y2")
    RedGreenBlue = namedtuple("RGB", "r g b")

    finished = pyqtSignal()
    message = pyqtSignal(str)

    pixel_verificador = Coord(1642, 762)  # NOT
    pixel_verificador = Coord(1644, 733)  # PC
    rgb = RedGreenBlue(255, 255, 255)
    rgb2 = RedGreenBlue(224, 224, 224)
    corte_ouro = CoordCorte(147, 140, 284, 176)
    corte_elixir = CoordCorte(147, 188, 284, 217)
    corte_dark = CoordCorte(140, 220, 250, 270)

    def __init__(self, ouro_minimo, elixir_minimo, dark_minimo):
        super().__init__()
        self.ouro_minimo = ouro_minimo
        self.elixir_minimo = elixir_minimo
        self.dark_minimo = dark_minimo
        self.rodando = True

    def run(self):
        try:
            self.__validate_fields()
            print(self.ouro_minimo, self.elixir_minimo, self.dark_minimo)

            sleep(5)
        except Exception as exception:
            self.message.emit(str(exception))

        self.finished.emit()

    def stop(self):
        self.rodando = False

    def __validate_fields(self):
        self.ouro_minimo = self.__checking(self.ouro_minimo)
        self.elixir_minimo = self.__checking(self.elixir_minimo)
        self.dark_minimo = self.__checking(self.dark_minimo)

        if self.ouro_minimo == 0 and self.elixir_minimo == 0 and self.dark_minimo == 0:
            raise Exception(
                "Campos Zerados, Por favor coloque um valor em pelo menos um campo"
            )

    def __checking(self, valor: str) -> int:
        if valor:
            corrido = int(valor.replace(".", ""))
            return corrido
        else:
            return 0
