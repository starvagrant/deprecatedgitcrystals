#!/usr/bin/python3
import json

class BaseController:
    def __init__(self, dirName="saved-game", name="base"):
       self.name = name
       self.text = ""
       self.dir = dirName
       self.jsonFile = dirName + "/" + name + ".json"
       self.data = self.loadJsonFile()

    def parseJson(text):
        return json.loads(text)

    def loadJson(self, data):
        return

    def loadJsonFile(self):
        with open(self.jsonFile, 'r') as f:
            self.text = f.read()
            self.data = json.loads(self.text)
        return self.data

    def writeJsonFile(self):
        with open(self.jsonFile, 'w') as f:
            f.write(json.dumps(self.data, sort_keys=True,
                               indent=4, separators=(',',':')))
            f.close()
        return

    def print():
        return

class AliveController(BaseController):
    def __init__(self, dirName="saved-game", name="alive"):
       self.name = name
       self.text = ""
       self.dir = dirName
       self.jsonFile = dirName + "/" + name + ".json"
       self.data = self.loadJsonFile()


class CharacterController(BaseController):
    def __init__(self, dirName="saved-game", name="characters"):
       self.name = name
       self.text = ""
       self.dir = dirName
       self.jsonFile = dirName + "/" + name + ".json"
       self.data = self.loadJsonFile()


class InventoryController(BaseController):
    def __init__(self, dirName="saved-game", name="inventory"):
       self.name = name
       self.text = ""
       self.dir = dirName
       self.jsonFile = dirName + "/" + name + ".json"
       self.data = self.loadJsonFile()


class TempController(BaseController):
    def __init__(self, dirName="saved-game", name="temp"):
       self.name = name
       self.text = ""
       self.dir = dirName
       self.jsonFile = dirName + "/" + name + ".json"
       self.data = self.loadJsonFile()

class WorldRoomsController(BaseController):
    def __init__(self, dirName="saved-game", name="worldRooms"):
       self.name = name
       self.text = ""
       self.dir = dirName
       self.jsonFile = dirName + "/" + name + ".json"
       self.data = self.loadJsonFile()
