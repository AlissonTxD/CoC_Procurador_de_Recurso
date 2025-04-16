import json
from typing import Dict

PATH = "config.json"


class ConfigModel:
    def __init__(self) -> None:
        self.configurations = []

    def get_json_data(self, path: str = PATH) -> Dict:
        try:
            self.__load_data(path)
            return {"sucess": True,"config" :self.configurations}
        except Exception as e:
            return {"sucess": False ,"error": str(e)}

    def __load_data(self, path: str) -> None:
        try:
            self.configurations = self.__open_json(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Aquivo de configuração não encontrado\n Fale com seu Omigador mais próximo")

    def __open_json(self, path: str) -> Dict:
        with open(path, "r") as fp:
            var = json.load(fp)
            return var


if __name__ == "__main__":
    repository = ConfigModel()
    data = repository.get_json_data()
    print(data)
    for recurso in data["generator"]:
        for value in data["generator"][recurso]:
            print(value)
