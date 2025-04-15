from PyQt5.QtCore import QThread

from src.views.view_main import MainGuiView
from src.models.model_image_generator import ImageGerenatorModel
from src.models.model_ocr_reading import SearchModel
from src.models.model_config import ConfigModel

thread = None
village_searcher = None


def search_village():
    global thread, village_searcher
    view = MainGuiView()
    config = ConfigModel()
    view.stop_signal.connect(handle_stop_signal)
    config_data = config.get_json_data()
    view.btn_stop.setEnabled(True)
    view.btn_search.setEnabled(False)
    view.tooltip("Buscando Vilas com Recursos")
    img_generator = ImageGerenatorModel(config_data)
    village_searcher = SearchModel(view.ocr, img_generator, view.minimum, config_data)
    thread = QThread()
    village_searcher.moveToThread(thread)
    thread.started.connect(village_searcher.run)
    village_searcher.error.connect(show_error)
    village_searcher.finished.connect(thread.quit)
    village_searcher.finished.connect(village_searcher.deleteLater)
    village_searcher.finished.connect(thread.deleteLater)
    village_searcher.finished.connect(stop_searching)
    thread.start()
    print("thread started")


def stop_searching():
    global thread, village_searcher

    if thread and thread.isRunning():
        thread.quit()
        thread.wait(500)
    view = MainGuiView()
    view.tooltip()
    view.btn_stop.setEnabled(False)
    view.btn_search.setEnabled(True)
    thread = None
    village_searcher = None


def handle_stop_signal():
    village_searcher.stop()


def show_error(error_msg: str):
    print(error_msg)
