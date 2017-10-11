#!/usr/bin/python3
import json

class BaseController:
    name = "base"
    def parseJson(text):
        return json.loads(text)
    def loadJson(self, data):
        return

    def loadJsonFile(self, fileName = 'saved-game/base.json'):
        return

    def writeJsonFile(self, dirName = 'saved-game'):
        return

    def print():
        return
