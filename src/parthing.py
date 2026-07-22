import json
from typing import Any


class Parseurjson:
    def __init__(
        self,
        function_call: str = "data/input/function_calling_tests.json",
        function_define: str = "data/input/functions_definition.json",
    ):
        self.function_call = self.readjson(function_call)
        self.function_define = self.readjson(function_define)
        pass

    def parse(self, json_string):
        return json.loads(json_string)

    def readjson(self, folders: str) -> list[Any]:
        with open(folders, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
