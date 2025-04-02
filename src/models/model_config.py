import json
from typing import List, Dict

PATH = "config.json"


class ConfigurationRepository:
    def __init__(self) -> None:
        self.configurations = []

    def get_json_data(self, path: str = PATH) -> List:
        self.__load_data(path)
        return self.configurations

    def __load_data(self, path: str) -> None:
        try:
            self.configurations = self.__open_json(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Aquivo de configuração não encontrado:")

    def __open_json(self, path: str) -> list:
        with open(path, "r") as fp:
            var = json.load(fp)
            return var


if __name__ == "__main__":
    repository = ConfigurationRepository()
    data = repository.get_json_data()
    print(data)
    for recurso in data["generator"]:
        for value in data["generator"][recurso]:
            print(value)
