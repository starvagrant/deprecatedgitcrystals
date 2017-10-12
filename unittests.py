#!/usr/bin/python3

import unittest
import gitgame
import json
import os
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
        base = BaseController()
        base.loadJsonFile('mock-data/base.json')
        self.assertEqual(base.data['first'], "first")
        self.assertEqual(base.data['second'], "second")
    def test_write_json(self):
        """ test writing a json file via BaseController """
        base = BaseController()
        base.loadJsonFile('mock-data/base.json')
        base.writeJsonFile('mock-data')
        with open('mock-data/base.json', 'r') as f:
            text = f.read()
            testJson = json.loads(text)
            f.close()

        self.assertEqual(testJson['first'], "first")
        self.assertEqual(testJson['second'], "second")

    def test_write_game(self):
        """ Test games are being property written """

unittest.main()
