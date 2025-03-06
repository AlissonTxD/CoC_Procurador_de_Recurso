from collections import namedtuple
from pyautogui import screenshot
from PIL import Image, ImageEnhance, ImageOps

PATH_IMAGEM_MAIN = "src/midia/temp/clash.png"
PATH_IMAGEM_GOLD = "src/midia/temp/gold.png"
PATH_IMAGEM_ELIXIR = "src/midia/temp/elixir.png"
PATH_IMAGEM_DARK = "src/midia/temp/dark.png"


class ImageGeneratorModel:
    def __init__(self):
        CoordCorte = namedtuple("Corte", "x1 y1 x2 y2")
        self.fatores_img = [2.0, 0.5, 1.0, 2.5]
        self.corte_ouro = CoordCorte(150, 140, 284, 176)
        self.corte_elixir = CoordCorte(150, 188, 284, 217)
        self.corte_dark = CoordCorte(150, 220, 250, 270)

    def gerar_imagens(self):
        try:
            self.__tirar_foto_inicial()
            self.__melhorar_imagem()
            self.__gerar_subimages()
        except Exception as exception:
            print(str(exception))

    def __tirar_foto_inicial(self) -> None:
        imagem_inicial = screenshot()
        imagem_inicial.save(PATH_IMAGEM_MAIN)

    def __melhorar_imagem(self) -> None:
        imagem_editada = Image.open(PATH_IMAGEM_MAIN).convert("RGB")
        imagem_editada = ImageEnhance.Contrast(imagem_editada).enhance(
            self.fatores_img[0]
        )
        imagem_editada = ImageEnhance.Color(imagem_editada).enhance(self.fatores_img[1])
        imagem_editada = ImageEnhance.Brightness(imagem_editada).enhance(
            self.fatores_img[2]
        )
        imagem_editada = ImageEnhance.Sharpness(imagem_editada).enhance(
            self.fatores_img[3]
        )
        limiar = 200
        # imagem_editada = imagem_editada.point(lambda p: p > limiar and 255)
        imagem_editada = ImageOps.invert(imagem_editada)
        imagem_editada = imagem_editada.convert("L")
        imagem_editada.save(PATH_IMAGEM_MAIN)

    def __gerar_subimages(self) -> None:
        img = Image.open(PATH_IMAGEM_MAIN)
        self.__cortar_subimage(
            img,
            self.corte_ouro.x1,
            self.corte_ouro.y1,
            self.corte_ouro.x2,
            self.corte_ouro.y2,
            PATH_IMAGEM_GOLD,
        )
        self.__cortar_subimage(
            img,
            self.corte_elixir.x1,
            self.corte_elixir.y1,
            self.corte_elixir.x2,
            self.corte_elixir.y2,
            PATH_IMAGEM_ELIXIR,
        )
        self.__cortar_subimage(
            img,
            self.corte_dark.x1,
            self.corte_dark.y1,
            self.corte_dark.x2,
            self.corte_dark.y2,
            PATH_IMAGEM_DARK,
        )
        

    def __cortar_subimage(
        self, img, x1: int, y1: int, x2: int, y2: int, path: str
    ) -> None:
        img_cortada = img.crop((x1, y1, x2, y2))
        img_cortada = img_cortada.resize(
            (img_cortada.width * 2, img_cortada.height * 2), Image.LANCZOS
        )
        img_cortada.save(path)
        pass


if __name__ == "__main__":
    teste = ImageGeneratorModel()
    teste.gerar_imagens()
