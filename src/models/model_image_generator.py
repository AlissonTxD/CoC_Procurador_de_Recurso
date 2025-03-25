from collections import namedtuple
import os

from pyautogui import screenshot
from PIL import Image, ImageEnhance, ImageOps

CoordCut = namedtuple("Corte", "x1 y1 x2 y2")
FATORES_IMG = [2.0, 0.5, 1.0, 2.5]
GOLD_CUT = CoordCut(150, 140, 284, 176)
ELIXIR_CUT = CoordCut(150, 188, 284, 217)
DARK_CUT = CoordCut(150, 220, 250, 270)

PATH_IMAGEM_MAIN = "temp/clash.png"
PATH_IMAGEM_GOLD = "temp/gold.png"
PATH_IMAGEM_ELIXIR = "temp/elixir.png"
PATH_IMAGEM_DARK = "temp/dark.png"


class ImageGerenatorModel:
    def generate_image(self):
        try:
            self.__take_screenshot()
            self.__enchance_image()
        except Exception as exception:
            print(str(exception))

    def __take_screenshot(self) -> None:
        """Takes a screenshot of the screen and saves it to a file.
        """
        first_image = screenshot()
        first_image.save(PATH_IMAGEM_MAIN)

    def __enchance_image(self):
        """Enhances the image to make it easier to read the numbers.
        """
        img = Image.open(PATH_IMAGEM_MAIN).convert("RGB")
        img = ImageEnhance.Contrast(img).enhance(FATORES_IMG[0])
        img = ImageEnhance.Color(img).enhance(FATORES_IMG[1])
        img = ImageEnhance.Brightness(img).enhance(FATORES_IMG[2])
        img = ImageEnhance.Sharpness(img).enhance(FATORES_IMG[3])
        img = ImageOps.invert(img)
        img = img.convert("L")
        img.save(PATH_IMAGEM_MAIN)


if __name__ == "__main__":
    model = ImageGerenatorModel()
    model.generate_image()
