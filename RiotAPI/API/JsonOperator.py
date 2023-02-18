import json


class JsonOperator:

    @staticmethod
    def write(fn, data):
        data = json.dumps(data)
        with open(fn, "w") as f:
            f.write(data)

    @staticmethod
    def champions():
        with open("C:/Users/gr801/PycharmProjects/Project/riotAPI/API/RiotAPI/Models/Data/champions.json", "r") as f:
            return json.load(f)

    @staticmethod
    def ranks():
        with open("C:/Users/gr801/PycharmProjects/Project/riotAPI/API/RiotAPI/Models/Data/ranks.json", "r") as f:
            return json.load(f)
