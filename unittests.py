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
        """ Load Directory of Mock Data"""
        test = (gitgame.loadGameData('mock-data/'))
        self.assertEqual(test['test']['filename'], 'alive')
        self.assertEqual(test['test2']['filename'], 'alive')

    def test_write_game(self):
        """ Test games are being property written """
        game = (gitgame.loadGameData('mock-data/'))
        save = (gitgame.writeGameData(game,'mock-data'))
        files = game.keys()
        test = []

        for item in files:
            test.append(item)

        test.sort()


        self.assertEqual(test, ['alive', 'characters', 'game', 'inventory', 'player', 'rooms', 'test', 'test2', 'worldRooms'])
                                                                        # The Json Files in Mock-Data
        self.assertEqual(game.keys(), save)                             # writeGameData returns game.keys()

    def test_death(self):
        prompt = gitgame.ExampleCmd()
        prompt.do_load()
        prompt.do_north('north')
        prompt.do_north('north')
        prompt.do_west('west')
        prompt.do_west('west')                                                # Navigate to Bottomless Pit, Character is Dead
        game = prompt.get_game()
        print(game['alive'])
        self.assertFalse(game['alive'])

unittest.main()
