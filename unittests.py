#!/usr/bin/python3

import unittest
import gitgame
import json
import os
from pprint import pprint
from BaseController import BaseController
from ControllerFactory import ControllerFactory

class MyTests(unittest.TestCase):
    def test_parse_json(self):
        """ test static method BaseController.parseJson parses Json """
        testJson = BaseController.parseJson('{"a":"a","b":"b"}')
        self.assertEqual(testJson['a'], "a")
        self.assertEqual(testJson['b'], "b")
    def test_load_json(self):
        """ test loading a json file via BaseController """
        base = BaseController('mock-data', 'base')
        base.loadJsonFile()
        self.assertEqual(base.data['first'], "first")
        self.assertEqual(base.data['second'], "second")
    def test_write_json(self):
        """ test writing a json file via BaseController """
        base = BaseController('mock-data', 'base')
        base.loadJsonFile()
        base.writeJsonFile()
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
        factory = ControllerFactory(True)
        jsonFileList = factory.scanDir('mock-data')

        testFactory = factory.createController(jsonFileList[1])                      # jsonFileList item should = 'base'
        self.assertEqual(testFactory.data, BaseController('mock-data', 'base').data) # Python can't compare two objects,
                                                                                     # except by reference

    def test_game_init(self):
        factory = ControllerFactory(True)
        files = factory.scanDir('mock-data')
        game = factory.initGame('mock-data')
        self.assertIsInstance(game, dict)                   # test variables are of right type
        self.assertIsInstance(files, list)
        self.assertEqual(len(game), len(files))             # test that a controller is produced per file
        for data in game:                                   # test all controllers are BaseControllers
            self.assertIsInstance(game[data], BaseController)

    def test_game_controllers(self):
        factory = ControllerFactory(True)
        controllers = factory.initGame('mock-data')

        game = gitgame.ExampleCmd()
        game.loadControllers(controllers)

        # One assertion per file

        self.assertEqual(game.alive.data['alive'], True)
        self.assertEqual(game.inventory.data['weapons'][0], "Unarmed")
        self.assertEqual(game.characters.data['dragon']['asleep'], True)
        self.assertEqual(game.temp.data['location'], "Mountain Gate")
        self.assertEqual(game.worldRooms.data['Abandoned Treasury']['danger'][0], "Search")

    def test_checkDeath(self):
        """ Test Internal Death Checking Method """
        factory = ControllerFactory(True)
        controllers = factory.initGame('mock-data')
        game = gitgame.ExampleCmd()
        game.loadControllers(controllers)

        self.assertFalse(game.checkDeath())
        game.alive.data['alive'] = False
        self.assertTrue(game.checkDeath())

    def test_north(self):
        """ Test Internal Method changeLocation """
        factory = ControllerFactory(True)
        controllers = factory.initGame('mock-data')
        game = gitgame.ExampleCmd()
        game.loadControllers(controllers)

        self.assertFalse(game.changeLocation('spiral'))
        self.assertFalse(game.changeLocation('west'))                       # North Only at Game Beginning
        game.changeLocation('north')
        self.assertEqual(game.temp.data['location'], "Git Crystal")


    def test_north_south_east_west(self):
        factory = ControllerFactory(True)
        controllers = factory.initGame('mock-data')
        game = gitgame.ExampleCmd()
        game.loadControllers(controllers)

        game.changeLocation('north')
        game.changeLocation('east')
        game.changeLocation('west')
        game.changeLocation('south')

        self.assertEqual(game.temp.data['location'], "Mountain Gate")

    def test_death_upon_entry(self):                                        # NNWW leads to the bottomless pit
        """ Test to See if Deadly Rooms Kill Character """
        factory = ControllerFactory(True)
        controllers = factory.initGame('mock-data')

        game = gitgame.ExampleCmd()
        game.loadControllers(controllers)

        game.changeLocation('north')
        game.changeLocation('north')
        game.changeLocation('west')
        game.changeLocation('west')

        self.assertEqual(game.temp.data['location'], "Bottomless Pit")
        self.assertEqual(game.alive.data['alive'], False)

unittest.main()
