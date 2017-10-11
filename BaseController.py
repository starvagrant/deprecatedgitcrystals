#!/usr/bin/python3
import json

class BaseController:
    def __init__(self):
       self.name = "base"
       self.data = {"test": "test"}
       self.text = ""

    def parseJson(text):
        return json.loads(text)

    def loadJson(self, data):
        return

    def loadJsonFile(self, fileName = 'saved-game/base.json'):
        with open(fileName, 'r') as f:
            self.text = f.read()
            self.data = json.loads(self.text)
        return

    def writeJsonFile(self, dirName = 'saved-game'):
        fileName = dirName + "/" + self.name + ".json"
        with open(fileName, 'w') as f:
            f.write(json.dumps(self.data, sort_keys=True,
                               indent=4, separators=(',',':')))
            f.close()
        return

    def print():
        return
