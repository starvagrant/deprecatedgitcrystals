#!/usr/bin/python3

import unittest
import gitgame
from BaseController import BaseController

class MyTests(unittest.TestCase):
    def test_parse_json(self):
        testJson = BaseController.parseJson('{"a":"a","b":"b"}')
        self.assertEquals(testJson['a'], "a")
        self.assertEquals(testJson['b'], "b")
    def test_load_json(self):
        """ Load Mock Data """
    def test_write_json(self):
        """ Write Base Controller's Json to File """

    def test_write_game(self):
        """ Test games are being property written """

unittest.main()
