#!/usr/bin/python3

import os
import json
from BaseController import *

class ControllerFactory:
    def __init__(self, mockData = False):
        self.mockData = mockData
        self.controllers = {}
        return

    def scanDir(self,jsonDirectory = "saved-game"):
        jsonFiles = []
        for directory in os.walk(jsonDirectory):
            for fileName in directory[2]:               # the file name list
                if (fileName[-5:] == '.json'):          # load .json files explicitly
                    f = fileName[:-5]                   # cut .json extension
                    jsonFiles.append(f)
                    jsonFiles.sort()
        return jsonFiles

    def createController(self,name='base'):
        """ Return Real or Mock Controllers By Name """

        if self.mockData:
            return {
            'alive': AliveController('mock-data', 'alive'),
            'characters': CharacterController('mock-data', 'characters'),
            'inventory': InventoryController('mock-data', 'inventory'),
            'temp': TempController('mock-data', 'temp'),
            'worldRooms' : WorldRoomsController('mock-data', 'worldRooms')
        }.get(name, BaseController('mock-data', 'base'))

        return {
            'alive': AliveController(),
            'characters': CharacterController(),
            'inventory': InventoryController(),
            'temp': TempController(),
            'worldRooms' : WorldRoomsController()
        }.get(name, BaseController('mock-data', 'base'))

    def initGame(self, jsonDirectory = "saved-game"):
        files = self.scanDir(jsonDirectory)
        for fileName in files:
            self.controllers[fileName] = self.createController(fileName)

        return self.controllers
