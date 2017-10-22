#!/usr/bin/python3

import unittest
import gitgame
import json
import os
from pprint import pprint
from BaseController import BaseController
from ControllerFactory import ControllerFactory

class MyTests(unittest.TestCase): #19 25 35 65 49
    def test_parse_json(self):
        """ test static method BaseController.parseJson parses Json """
        testJson = BaseController.parseJson('{"a":"a","b":"b"}')
        self.assertEqual(testJson['a'], "a")
        self.assertEqual(testJson['b'], "b")
    def test_load_json(self):
        """ test loading a json file via BaseController """
        base = BaseController()                             # test fails without saved-game/base.json
        base.loadJsonFile('mock-data/base.json')
        self.assertEqual(base.data['first'], "first")
        self.assertEqual(base.data['second'], "second")
    def test_write_json(self):
        """ test writing a json file via BaseController """
        base = BaseController()                             # test fails without saved-game/base.json
        base.loadJsonFile('mock-data/base.json')
        base.writeJsonFile('mock-data')
        with open('mock-data/base.json', 'r') as f:
            text = f.read()
            testJson = json.loads(text)
            f.close()

        self.assertEqual(testJson['first'], "first")
        self.assertEqual(testJson['second'], "second")

    def test_json_folder_scan(self):
        """ Test all json files being tested """
        factory = ControllerFactory()
        jsonFileList = factory.scanDir('mock-data')
        self.assertEqual(jsonFileList, ['alive','base','characters','game','inventory',
                                        'temp','worldRooms'])
                                                            # These will differ based on contents of
                                                            # Mock Data Directory

    def test_game_controller(self):
        factory = ControllerFactory()
        jsonFileList = factory.scanDir('mock-data')

        testFactory = factory.createController(jsonFileList[1])             # jsonFileList item should = 'base'
        self.assertEqual(testFactory.data, BaseController().data)           # Python can't compare two objects,
                                                                            # except by reference

    def test_game_init(self):
        factory = ControllerFactory()
        files = factory.scanDir('mock-data')
        game = factory.initGame('mock-data')
        self.assertIsInstance(game, dict)                   # test variables are of right type
        self.assertIsInstance(files, list)
        self.assertEqual(len(game), len(files))             # test that a controller is produced per file
        for data in game:                                   # test all controllers are BaseControllers
            self.assertIsInstance(game[data], BaseController)

    def test_game_controllers(self):
        factory = ControllerFactory()
        controllers = factory.initGame('mock-data')         # test fails without saved-game/base.json
        for name in controllers:
            pprint(name)

        game = gitgame.ExampleCmd()
        game.loadControllers(controllers)

        # One assertion per file

        self.assertEqual(game.alive.data['alive'], True)
        self.assertEqual(game.inventory.data['weapons'][0], "Unarmed")
        self.assertEqual(game.characters.data['dragon']['asleep'], True)
        self.assertEqual(game.temp.data['location'], "Mountain Cave")
        self.assertEqual(game.worldRooms.data['Abandoned Treasury']['danger'][0], "Search")

unittest.main()
