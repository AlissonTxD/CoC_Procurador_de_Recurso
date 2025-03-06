from collections import namedtuple
from time import sleep

from playsound import playsound
from pyautogui import pixelMatchesColor,click

from PyQt5.QtCore import QObject, pyqtSignal
from src.models.image_editor_model import ImageGeneratorModel

PATH_IMAGEM_GOLD = "src/midia/temp/gold.png"
PATH_IMAGEM_ELIXIR = "src/midia/temp/elixir.png"
PATH_IMAGEM_DARK = "src/midia/temp/dark.png"

class ProcuradorDeVilaController(QObject):
    finished = pyqtSignal()
    erro = pyqtSignal(str)

    def __init__(self, ouro_minimo: str, elixir_minimo: str, dark_minimo: str, ocr):
        super().__init__()
        self.ouro_minimo = ouro_minimo
        self.elixir_minimo = elixir_minimo
        self.dark_minimo = dark_minimo
        self.image_generator = ImageGeneratorModel()
        self.ocr = ocr

        Coord = namedtuple("Coord", "x y")
        RedGreenBlue = namedtuple("RGB", "r g b")

        self.pixel_verificador = Coord(1642, 762)  # NOT
        # self.pixel_verificador = Coord(1644, 733)  # PC
        self.rgb = RedGreenBlue(255, 255, 255)
        self.rgb2 = RedGreenBlue(224, 224, 224)

        self.rodando = True

    def run(self) -> None:
        try:
            print("run iniciado")
            self.__format_numbers()
            self.__validate_fields()
            print(self.ouro_minimo, self.elixir_minimo, self.dark_minimo)

            while True:
                print("Aguardando Iniciar Processo de Busca...")
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

            while self.rodando:
                self.image_generator.gerar_imagens()
                ouro_na_vila, elixir_na_vila, dark_na_vila = self.__salvar_resultados_da_leitura()
                print(ouro_na_vila, elixir_na_vila, dark_na_vila)

                ouro_is_good = ouro_na_vila >= self.ouro_minimo and self.ouro_minimo != 0
                elixir_is_good = elixir_na_vila >= self.elixir_minimo and self.elixir_minimo != 0
                dark_is_good = dark_na_vila >= self.dark_minimo and self.dark_minimo != 0

                if ouro_is_good or elixir_is_good or dark_is_good:
                    playsound("src/midia/mp3/vila.mp3")
                    print("achou a vila carai")
                    self.stop()
                    break
                else:
                    click(x=self.pixel_verificador.x, y=self.pixel_verificador.y)
                    
                sleep(2)
                while True:
                    print("Aguardando proxima vila...")
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

        except Exception as ex:
            self.erro.emit(str(ex))

        self.finished.emit()

    def stop(self) -> None:
        self.rodando = False

    def __validate_fields(self) -> None:
        if self.ouro_minimo == 0 and self.elixir_minimo == 0 and self.dark_minimo == 0:
            print("validade zerado")
            raise Exception(
                "Campos Zerados, Por favor coloque pelomenos 1 valor para iniciar a procura"
            )

    def __format_numbers(self) -> None:
        self.ouro_minimo = self.__checking(self.ouro_minimo)
        self.elixir_minimo = self.__checking(self.elixir_minimo)
        self.dark_minimo = self.__checking(self.dark_minimo)

    def __checking(self, valor: str) -> int:
        if valor:
            corrido = int(valor.replace(".", ""))
            return corrido
        else:
            return 0

    def __ler_imagem(self, path):
        try:
            img_path = path
            result = self.ocr.ocr(img_path, cls=True)
            textolido = ""
            for line in result:
                for word_info in line:
                    text = word_info[1][0]
                    textolido += text
            textolido = textolido.replace(" ", "")
            textolido = textolido.replace("S", "5")
            textolido = textolido.replace("s", "5")
            valor = ""
            for caractere in textolido:
                if caractere.isdigit():
                    valor += caractere
            textolido = int(valor)
            return textolido
        except:
            return 0

    def __salvar_resultados_da_leitura(self):
        ouro_na_vila = self.__ler_imagem(PATH_IMAGEM_GOLD)
        elixir_na_vila = self.__ler_imagem(PATH_IMAGEM_ELIXIR)
        dark_na_vila = self.__ler_imagem(PATH_IMAGEM_DARK)
        return ouro_na_vila, elixir_na_vila, dark_na_vila