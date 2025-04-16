from collections import namedtuple
from time import sleep
import pygetwindow as gw

from PyQt5.QtCore import QObject, pyqtSignal
from pyautogui import pixelMatchesColor, click, pixel, moveTo
from playsound import playsound
from src.models.model_image_generator import ImageGerenatorModel
from src.utils import resource_path

RGB = (255, 255, 255)
RGB2 = (224, 224, 224)

GOLD_IMAGE_PATH = "temp/gold.png"
ELIXIR_IMAGE_PATH = "temp/elixir.png"
DARK_IMAGE_PATH = "temp/dark.png"
MP3_PATH = resource_path("src/midia/mp3/vila.mp3")
WINDOW_TITLE = "Clash of Clans"

Coord = namedtuple("Coord", "x y")


class SearchModel(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(
        self, ocr, image_generator: ImageGerenatorModel, minimum, config: dict
    ):
        super().__init__()
        self.image_generator = image_generator
        self.ocr = ocr
        self.minimum = minimum
        self.TARGET_PIXEL = Coord(config["target"][0], config["target"][1])
        self._running = True

    def run(self):
        try:
            self.__format_minimum(self.minimum)
            self.__focus_in_window(WINDOW_TITLE)
            click()
            sleep(1)
            while True:
                while True:
                    if (
                        self.__village_is_loaded()
                        or not self.__window_in_focus(WINDOW_TITLE)
                        or not self._running
                    ):
                        print("Vila carregada ou janela fora de foco")
                        break
                    sleep(1)
                    pix = pixel(self.TARGET_PIXEL.x, self.TARGET_PIXEL.y)
                    print(f"Aguardando vila ser carregada: {pix}")
                if not self.__window_in_focus(WINDOW_TITLE) or not self._running:
                    break
                sleep(1)
                self.image_generator.generate_image()
                village_resources = self.__format_response_ocr()
                print(self.minimum)
                print(village_resources)
                if self.__village_is_fat(self.minimum, village_resources):
                    print("Vila gorda encontrada")
                    playsound(MP3_PATH)
                    break
                else:
                    self.__focus_in_window(WINDOW_TITLE)
                    click(x=self.TARGET_PIXEL.x, y=self.TARGET_PIXEL.y)
                    sleep(2)
        except Exception as e:
            self.error.emit(f"Erro: {e}")
        self.finished.emit()

    def __format_response_ocr(self):
        gold_in_village = self.__read_img_ocr(GOLD_IMAGE_PATH)
        elixir_in_village = self.__read_img_ocr(ELIXIR_IMAGE_PATH)
        dark_in_village = self.__read_img_ocr(DARK_IMAGE_PATH)
        return (gold_in_village, elixir_in_village, dark_in_village)

    def __format_minimum(self, minimum: tuple[str]):
        new_list = []
        for min in minimum:
            try:
                nd = min.replace(".", "")
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

    def __village_is_loaded(self):
        test1 = pixelMatchesColor(self.TARGET_PIXEL.x, self.TARGET_PIXEL.y, RGB)
        test2 = pixelMatchesColor(self.TARGET_PIXEL.x, self.TARGET_PIXEL.y, RGB2)
        if test1 or test2:
            return True
        else:
            return False

    def __village_is_fat(self, minimum: tuple, village_resources: tuple) -> None:
        """ "Checks if the village has the minimum resources.
        Args:
            minimum (tuple): minimum resources to check.
            village_resources (tuple): resources in the actual village."""
        for min, resource in zip(minimum, village_resources):
            if min != 0 and resource < min:
                return False
        return True

    def __focus_in_window(self, window_name) -> None:
        try:
            window = gw.getWindowsWithTitle(window_name)[0]
            window.activate()
        except IndexError:
            print(f"Janela com o título '{window_name}' não encontrada.")
        except Exception as e:
            print(f"Erro ao focar na janela: {e}")

    def __window_in_focus(self, window_name) -> bool:
        try:
            active_window = gw.getActiveWindow()
            if active_window is not None and active_window.title == window_name:
                return True
            else:
                print("break por falta de foco na janela")
                return False
        except Exception as e:
            print(f"Erro ao verificar janela: {e}")
            return False

    def stop(self) -> None:
        """Stops the search."""
        self._running = False
        print("parou de procurar")
