from src.views.view_main import MainGuiView
from src.models.model_image_generator import ImageGerenatorModel
from src.models.model_ocr_reading import SearchModel


def search_village():
    view = MainGuiView() 
    view.btn_stop.setEnabled(True)
    view.btn_search.setEnabled(False)
    view.tooltip("Buscando Vilas com Recursos")
    img_generator = ImageGerenatorModel()
    village_searcher = SearchModel(view.ocr, img_generator, view.minimum)
    village_searcher.run()
    
  

def stop_searching():
    print("botao parar apertado")