#!/usr/bin/python3

import unittest
import recordable
import json

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
        self.assertRegex(jsonFile.__repr__(), printed_regex)


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
