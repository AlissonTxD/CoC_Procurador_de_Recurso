from collections import namedtuple
import os
from time import sleep

from pyautogui import screenshot
from PIL import Image, ImageEnhance, ImageOps

CoordCut = namedtuple("Corte", "x1 y1 x2 y2")
IMG_FACTORS = (2.0, 0.5, 1.0, 2.5)
GOLD_CUT = (180, 145, 310, 175)
ELIXIR_CUT = (180, 188, 310, 217)
DARK_CUT = (180, 230, 310, 260)

MAIN_IMAGE_PATH = "temp/clash.png"
GOLD_IMAGE_PATH = "temp/gold.png"
ELIXIR_IMAGE_PATH = "temp/elixir.png"
DARK_IMAGE_PATH = "temp/dark.png"


class ImageGerenatorModel:
    def generate_image(self):
        try:
            self.__take_screenshot()
            self.__enchance_image()
            self.__generate_sub_images()
            self.__resize_subimages()
        except Exception as exception:
            print(exception)

    def __take_screenshot(self) -> None:
        """Takes a screenshot of the screen and saves it to a file."""
        try:
            first_image = screenshot()
            first_image.save(MAIN_IMAGE_PATH)
        except FileNotFoundError:
            os.makedirs("temp")
            self.__take_screenshot()

    def __enchance_image(self):
        """Enhances the image to make it easier to read the numbers."""
        img = Image.open(MAIN_IMAGE_PATH).convert("RGB")
        img = ImageEnhance.Contrast(img).enhance(IMG_FACTORS[0])
        img = ImageEnhance.Color(img).enhance(IMG_FACTORS[1])
        img = ImageEnhance.Brightness(img).enhance(IMG_FACTORS[2])
        img = ImageEnhance.Sharpness(img).enhance(IMG_FACTORS[3])
        img = ImageOps.invert(img)
        img = img.convert("L")
        img.save(MAIN_IMAGE_PATH)

    def __generate_sub_images(self):
        self.__cut_image(GOLD_CUT, GOLD_IMAGE_PATH)
        self.__cut_image(ELIXIR_CUT, ELIXIR_IMAGE_PATH)
        self.__cut_image(DARK_CUT, DARK_IMAGE_PATH)

    def __cut_image(self, cut_tuple, path):
        img = Image.open(MAIN_IMAGE_PATH)
        cutted_img = img.crop(cut_tuple)
        cutted_img.save(path)

    def __resize_subimages(self):
        self.__resize_image(GOLD_IMAGE_PATH)
        self.__resize_image(ELIXIR_IMAGE_PATH)
        self.__resize_image(DARK_IMAGE_PATH)

    def __resize_image(self, path):
        img = Image.open(path)
        img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
        img.save(path)


if __name__ == "__main__":
    model = ImageGerenatorModel()
    model.generate_image()
