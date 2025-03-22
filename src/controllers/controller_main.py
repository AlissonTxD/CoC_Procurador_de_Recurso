from .controller_search import search_village, stop_searching

class ControllerMain:
    def search(self):
        search_village()
        
    def stop(self):
        stop_searching()
        