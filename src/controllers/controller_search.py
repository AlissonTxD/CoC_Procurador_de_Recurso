from PyQt5.QtCore import QThread

from src.views.view_main import MainGuiView
from src.models.model_image_generator import ImageGerenatorModel
from src.models.model_ocr_reading import SearchModel

thread = None
village_searcher = None


def search_village():
    global thread, village_searcher
    view = MainGuiView()
    view.btn_stop.setEnabled(True)
    view.btn_search.setEnabled(False)
    view.tooltip("Buscando Vilas com Recursos")

    img_generator = ImageGerenatorModel()
    village_searcher = SearchModel(view.ocr, img_generator, view.minimum)
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


def show_error(error_msg: str):
    print(error_msg)
