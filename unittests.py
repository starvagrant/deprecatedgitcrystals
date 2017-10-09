#!/usr/bin/python3

import unittest
import gitgame

class MyTests(unittest.TestCase):
    def test_load_json(self):
        """ Load Mock Data """
        json = (gitgame.loadJsonFromFile('test','mock-data/'))
        self.assertEqual(json['filename'], 'alive')
        self.assertEqual(json['player'] , 'alive')

    def test_game(self):
        test = (gitgame.loadGameData('mock-data/'))
        self.assertEqual(test['test']['filename'], 'alive')
        self.assertEqual(test['test2']['filename'], 'alive')

    def test_write_game(self):
        game = (gitgame.loadGameData('mock-data/'))
        save = (gitgame.writeGameData(game,'mock-data'))
        self.assertEqual(save, True)


unittest.main()
