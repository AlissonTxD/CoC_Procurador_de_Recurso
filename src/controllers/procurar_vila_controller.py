from collections import namedtuple
from time import sleep

from pyautogui import pixelMatchesColor

from PyQt5.QtCore import QObject, pyqtSignal


class ProcuradorDeVila(QObject):
    finished = pyqtSignal()
    message = pyqtSignal(str)

    def __init__(self, ouro_minimo: str, elixir_minimo: str, dark_minimo: str):
        super().__init__()
        self.ouro_minimo = ouro_minimo
        self.elixir_minimo = elixir_minimo
        self.dark_minimo = dark_minimo

        Coord = namedtuple("Coord", "x y")
        CoordCorte = namedtuple("Corte", "x1 y1 x2 y2")
        RedGreenBlue = namedtuple("RGB", "r g b")

        self.pixel_verificador = Coord(1642, 762)  # NOT
        # self.pixel_verificador = Coord(1644, 733)  # PC
        self.rgb = RedGreenBlue(255, 255, 255)
        self.rgb2 = RedGreenBlue(224, 224, 224)
        self.corte_ouro = CoordCorte(147, 140, 284, 176)
        self.corte_elixir = CoordCorte(147, 188, 284, 217)
        self.corte_dark = CoordCorte(140, 220, 250, 270)

        self.rodando = True

    def run(self) -> None:
        try:
            self.__validate_fields()
            print(self.ouro_minimo, self.elixir_minimo, self.dark_minimo)
            while True:
                print("aguardando inicio de procura de partida...")
                vila_carregada = pixelMatchesColor(
                    self.pixel_verificador.x,
                    self.pixel_verificador.y,
                    (self.rgb.r, self.rgb.g, self.rgb.b),
                ) or pixelMatchesColor(
                    self.pixel_verificador.x,
                    self.pixel_verificador.y,
                    (self.rgb2.r, self.rgb2.g, self.rgb2.b),
                )
                if vila_carregada or not self.rodando:
                    break
                sleep(0.5)
            print("vila carregada")

        except Exception as exception:
            print(str(exception))
            self.message.emit(str(exception))

        self.finished.emit()

    def stop(self) -> None:
        self.rodando = False

    def __validate_fields(self) -> None:
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
