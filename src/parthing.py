import json

class Parseurjson():
    def __init__(self):
        pass

    def parse(self, json_string):
        return json.loads(json_string)