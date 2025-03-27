from PyQt5.QtCore import QObject, pyqtSignal

from pyautogui import pixelMatchesColor, click

from src.models.model_image_generator import ImageGerenatorModel

GOLD_IMAGE_PATH = "temp/gold.png"
ELIXIR_IMAGE_PATH = "temp/elixir.png"
DARK_IMAGE_PATH = "temp/dark.png"

class SearchModel:
    def __init__(self, ocr, image_generator: ImageGerenatorModel, minimum):
        self.image_generator = image_generator
        self.ocr = ocr
        self.minimum = minimum

    def run(self):
        self.__format_minimum(self.minimum)
        self.image_generator.generate_image()
        self.read_response = self.__format_response_ocr()
        print(self.minimum)
        print(self.read_response)

    def __format_response_ocr(self):
        gold_in_village = self.__read_img_ocr(GOLD_IMAGE_PATH)
        elixir_in_village = self.__read_img_ocr(ELIXIR_IMAGE_PATH)
        dark_in_village = self.__read_img_ocr(DARK_IMAGE_PATH)
        return (gold_in_village, elixir_in_village, dark_in_village)

    def __format_minimum(self, minimum: tuple[str]):
        new_list = []
        for min in minimum:
            try:
                nd = min.replace(".","")
                nd = int(nd)
                new_list.append(nd)
            except ValueError:
                new_list.append(0)
        self.minimum = tuple(new_list)
        

    def __read_img_ocr(self, path):
        try:
            img_path = path
            result = self.ocr.ocr(img_path, cls=True)
            textolido = ""
            for line in result:
                for word_info in line:
                    text = word_info[1][0]
                    textolido += text
            valor = ""
            for caractere in textolido:
                if caractere.isdigit():
                    valor += caractere
            textolido = int(valor)
            return textolido
        except:
            return 0