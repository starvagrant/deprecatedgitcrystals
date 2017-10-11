#!/usr/bin/python3

import unittest
import gitgame
import json
from BaseController import BaseController

class MyTests(unittest.TestCase):
    def test_parse_json(self):
        testJson = BaseController.parseJson('{"a":"a","b":"b"}')
        self.assertEqual(testJson['a'], "a")
        self.assertEqual(testJson['b'], "b")
    def test_load_json(self):
        base = BaseController()
        base.loadJsonFile('mock-data/base.json')
        self.assertEqual(base.data['first'], "first")
        self.assertEqual(base.data['second'], "second")
    def test_write_json(self):
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
