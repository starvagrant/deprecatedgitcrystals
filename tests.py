#!/usr/bin/python3

import unittest
import recordable, character, cavemap, gitgame, gamerepo

class Tests(unittest.TestCase):
    def test_recordable_reads(self):
        """ I need to test that the recordable class properly reads files"""
        jsonFile = recordable.Recordable('mock-data')
        self.assertEqual(jsonFile.data['first'], "first")
        self.assertEqual(jsonFile.data['second'], "second")

    def test_recordable_writes(self):
        """ I need to test that the recordable class properly writes files"""
        jsonFile = recordable.Recordable('mock-data')
        jsonFile.write()
        jsonFile.load()
        self.assertEqual(jsonFile.data['first'], "first")
        self.assertEqual(jsonFile.data['second'], "second")

    def test_recordable_repr(self):
        """ I need to test the recordable test implments __repr__ as expected """
        jsonFile = recordable.Recordable('mock-data')
        # Since dictionary keys can't be sorted, test with regex
        printed_regex = "The object base\nHas keys: \n(second|first), (first|second)"
        """
        self.assertRegex(jsonFile.__repr__(), printed_regex)
        """

    def test_player_character(self):
        aliveJson = recordable.Recordable('mock-data', 'alive')
        statusJson = recordable.Recordable('mock-data', 'status')
        locationJson = recordable.Recordable('mock-data', 'location')
        inventoryJson = recordable.Recordable('mock-data', 'inventory')
        recordables = [aliveJson, statusJson, locationJson, inventoryJson]
        testPlayer = character.Character(recordables)

        self.assertEqual(testPlayer.inventory['weapons'][0], "Unarmed")
        self.assertEqual(testPlayer.alive['alive'], True)
        self.assertEqual(testPlayer.status['floating'], False)
        self.assertEqual(testPlayer.location['location'], "Mountain Gate")

    def test_non_player_character(self):
        aliveJson = recordable.Recordable('mock-data/characters', 'alive')
        statusJson = recordable.Recordable('mock-data/characters', 'status')
        relationshipJson = recordable.Recordable('mock-data/characters', 'relationship')
        recordables = [aliveJson, statusJson, relationshipJson]
        testNonPlayer = character.Character(recordables)

        # Values Based on Dragon NPC
        self.assertEqual(testNonPlayer.alive['alive'], True)
        self.assertEqual(testNonPlayer.status['asleep'], True)
        self.assertEqual(testNonPlayer.relationship['knows_player'], False)
        self.assertEqual(testNonPlayer.isPlayer, False)

    def test_map_object(self):
        """ Test Map Returns Correct Room"""
        roomJson = recordable.Recordable('mock-data', 'worldRooms')
        rooms = cavemap.Map(roomJson)
        self.assertEqual(rooms.move('north','Mountain Gate'), 'Git Crystal')

    def test_character_movement(self):
        """ Test A Character moves, and the data of movement to disk """
        locationJson = recordable.Recordable('mock-data', 'location')
        roomJson = recordable.Recordable('mock-data', 'worldRooms')
        recordables = [locationJson]
        testPlayer = character.Character(recordables)
        rooms = cavemap.Map(roomJson)

        testPlayer.move('north', rooms)
        self.assertEqual(testPlayer.location['location'], "Git Crystal")

        testPlayer.move('east', rooms)
        self.assertEqual(testPlayer.location['location'], "Mine Entrance")

        changedLocationJson = recordable.Recordable('mock-data', 'location')

        testPlayer.move('invalid Direction', rooms)
        self.assertEqual(testPlayer.location['location'], "Mine Entrance")

        testPlayer.move('west', rooms)
        testPlayer.move('south', rooms)

        originalLocationJson = recordable.Recordable('mock-data','location')

        self.assertNotEqual(locationJson, changedLocationJson)
        self.assertEqual(locationJson, originalLocationJson)

    def test_game_initialization(self):
        """ Test GitGameCmd initializes correctly """
        game = gitgame.GitGameCmd('mock-data')
        self.assertIn('cmdloop', dir(game))

    def test_game_movement(self):
        """ Test Command Line Movement """
        game = gitgame.GitGameCmd('mock-data')
        locationJson = recordable.Recordable('mock-data', 'location')
        roomJson = recordable.Recordable('mock-data', 'worldRooms')
        recordables = [locationJson]
        testPlayer = character.Character(recordables)

        game.do_north('')
        self.assertEqual(game.player.location['location'], "Git Crystal")

        game.do_east('')
        self.assertEqual(game.player.location['location'], "Mine Entrance")

        changedLocationJson = recordable.Recordable('mock-data', 'location')

        game.do_west('')
        game.do_south('')

        originalLocationJson = recordable.Recordable('mock-data','location')

        self.assertNotEqual(locationJson, changedLocationJson)
        self.assertEqual(locationJson, originalLocationJson)

    def test_invalid_move(self):
        """ Test that an invalid movement can't be made """
        game = gitgame.GitGameCmd('mock-data')
        locationJson = recordable.Recordable('mock-data', 'location')
        roomJson = recordable.Recordable('mock-data', 'worldRooms')
        recordables = [locationJson]
        testPlayer = character.Character(recordables)

        game.do_west('')
        self.assertEqual(testPlayer.location['location'], "Mountain Gate") # Invalid move

    def test_game_display(self):
        """ Test Game Room Display """
        game = gitgame.GitGameCmd('mock-data')
        locationJson = recordable.Recordable('mock-data', 'location')
        roomJson = recordable.Recordable('mock-data', 'worldRooms')
        recordables = [locationJson]
        testPlayer = character.Character(recordables)
        worldMap = game.map

        firstRoom = game.displayPlayerLocation(worldMap)
        roomText = "You are located in the Mountain Gate\n"
        roomText += "The adjacent rooms are :\n"
        roomText += "north: Git Crystal\n"
        self.assertEqual(firstRoom, roomText)

        game.do_north('')
        secondRoom = game.displayPlayerLocation(worldMap)
        roomText = "You are located in the Git Crystal\n"
        roomText += "The adjacent rooms are :\n"
        roomText += "north: Stalagmite Central\n"
        roomText += "east: Mine Entrance\n"
        roomText += "south: Mountain Gate\n"
        roomText += "west: Wizard's Library\n"
        self.assertEqual(secondRoom, roomText)

        game.do_south('') # Reset to initial location

    def test_git_status(self):
        """ Test the git status command """
        repo = gamerepo.GitCmd('mock-data')
        repo.do_status('')
        self.assertEqual(repo.currentMessage, "{'untracked.txt': 128}")

    def test_git_diff(self, ref1, ref2, options=None, files = []):
        """ Test the git diff command """
        """
        Proposed Beginner's Diff Entry:
        File differences:
            from commit 24d23af (references)
            to commit f8f2231: (references)

        File 1:
            from commit 24d23af: <file-name>
            to commit f8f2231: <file-name>
        Diff:

        """
        repo = gamerepo.GitCmd('mock-data')
        repo.do_diff()
        self.assertEqual(repo.currentDiff, '')
        repo.do_diff('HEAD', 'HEAD~2')
        self.assertEqual(repo.currentDiff, '')

    def test_git_log(self, branchTip, depth=20):
        """ Test the git log command """


unittest.main()
