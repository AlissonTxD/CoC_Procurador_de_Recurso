#TODO model que ira ler a config do json e utilizara nas outras classes
import json
from typing import List, Dict

PATH = "config.json"


class ConfigurationRepository:
    def __init__(self) -> None:
        self. configurations = []

    def get_json_data(self, path: str= PATH) -> List:
        self.__load_data(path)
        return self. configurations

    def register_in_json(self, configuration: Dict, path: str= PATH) -> None:
        self.__load_data(path)
        self. configurations.append(configuration)
        self.__save_json(self. configurations, path)
        
    def delete_in_json(self, driver: Dict, path: str= PATH) -> None:
        self.__load_data(path)
        self. configurations.remove(driver)
        self.__save_json(self. configurations, path)
 
    def __save_json(self, obj: List, path: str) -> None:
        sorted_list = sorted(obj, key=lambda motorista: motorista["name"])
        with open(path, "w") as fp:
            json.dump(sorted_list, fp, indent=2)

    def __load_data(self, path: str) -> None:
        try:
            self. configurations = self.__open_json(path)
        except FileNotFoundError:
            with open(path, "w") as fp:
                json.dump([], fp)

    def __open_json(self, path: str) -> list:
        with open(path, "r") as fp:
            var = json.load(fp)
            return var