#!/usr/bin/python3

import unittest
import recordable, character, cavemap

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

    def test_game_recordables_initialized(self):
        """ I need to test that a game contains the proper recordables.
                An important criterion is this: an object that is a recordable means
                by definition both possible to affect with git, and expected to be affected
                by git (depending on the insight of the user). Moreover, to make the game easy
                I am preventing merge conflicts under the hood. (By forcing --ours / --theirs
                style resolutions). If two events are to be independent on each other, they have to
                be placed in separate recordables even if this leads to less than ideal classes.
                As a game designer I intend to allow for a great deal of puzzle solving by allowing
                the opportunity to muck around with the affects of dying. As such, I have to keep the
                player's life and death state in a separate recordable.

                The following recordable's are planned so far.
                    - Player location:
                    - Player life: (alive or dead)
                    - Player status: status effects are picked up from interacting with objects, including
                        objects that kill you. One of the fun quirks in this game is it's bizarre humor.
                        Having a trap slice off your head may kill you and gave you the "beheaded" status.
                        As these two effects are recorded in different files, you could use git to set your
                        status back to alive, without restoring you from the status. (This could lead to a
                        number of possibilities, such as being able to access secret areas because you are
                        shorter to being able to add your head to your inventory use it as an item.)

                        The noted downside is this: each recordable is responsible for a file, as opposed to
                        a concept. A Player, for instance, would need to tie together several recordables rather
                        than be a straightforward class that maps directly to functionality.
                   - Player inventory
                   - The Dragon
                   - Your Grandfather
                   - The Princess

                Now that I think of it, it would probably be useful to implement a base NPC class and throw
                each instance a different recordable.
        """

unittest.main()
