#!/usr/bin/env python3

import unittest, os, pygit2
import recordable, character, cavemap, gitgame, gamerepo

class Tests(unittest.TestCase):
    def reset_repo(self):
        repo = pygit2.Repository('mock-data/.git')
        repo.checkout('HEAD', strategy = pygit2.GIT_CHECKOUT_FORCE)

    def test_reset_repo(self):
        """ Reset Changes to the Repo from Previous Testing """
        self.reset_repo()

        repo = pygit2.Repository('mock-data/.git')
        self.assertEqual(repo.status(), {})

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
        self.reset_repo()

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
        self.reset_repo()

        """ Test Map Returns Correct Room"""
        roomJson = recordable.Recordable('mock-data', 'worldRooms')
        rooms = cavemap.Map(roomJson)
        self.assertEqual(rooms.move('north','Mountain Gate'), 'Git Crystal')

    def test_character_movement(self):
        """ Test A Character moves, and the data of movement to disk """
        self.reset_repo()

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
        self.reset_repo()

        game = gitgame.GitGameCmd('mock-data')
        locationJson = recordable.Recordable('mock-data', 'location')

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

        game.do_west('')
        self.assertEqual(game.player.location['location'], "Mountain Gate") # Invalid move

    def test_game_display(self):
        """ Test Game Room Display """
        self.reset_repo()

        game = gitgame.GitGameCmd('mock-data')
        firstRoom = game.displayPlayerLocation(game.map)

        roomText = "You are located in the Mountain Gate\n"
        roomText += "The adjacent rooms are :\n"
        roomText += "north: Git Crystal\n"
        self.assertEqual(firstRoom, """[34m+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    You are located in the [36mMountain Gate[34m
The adjacent rooms are :
north: [32mGit Crystal[34m
[34m+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[0m
""")

        game.do_north('')
        secondRoom = game.displayPlayerLocation(game.map)
        self.assertEqual(secondRoom, """[34m+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    You are located in the [36mGit Crystal[34m
The adjacent rooms are :
north: [32mStalagmite Central[34m
east: [32mMine Entrance[34m
south: [32mMountain Gate[34m
west: [32mWizard's Library[34m
[34m+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[0m
""")

        game.do_south('') # Reset to initial location

    def test_git_status(self):
        """ Test the git status command """
        self.reset_repo()
        repo = pygit2.Repository('mock-data/.git')
        with open(os.path.join(repo.workdir, 'game.json'), 'a') as f:
            f.write('#comment')
        repo.index.add('game.json')
        repo.index.write()
        with open(os.path.join(repo.workdir, 'game.json'), 'a') as f:
            f.write('#comment')
        game = gitgame.GitGameCmd('mock-data')
        game.do_status('')
        self.assertEqual(game.statusMessage, """[34mRepository Status
-----------------------------------------------------------------
[32mStaging Area
    Files:
     game.json Staged File Changes

[0m[31mUnstaged Changes
    Files:
     game.json Unstaged File Changes

[0m""")

        repo.checkout('HEAD', strategy=pygit2.GIT_CHECKOUT_FORCE)

    def test_git_diff(self):
        repo = gamerepo.GitCmd('mock-data2')

        repo.do_diff('')
        self.assertEqual(repo.fullDiff, """[0m=================================================================
[31m--- old file: game.json in commit 21b4f39
[32m+++ new file: game.json in unstaged changes

[0m     },
[0m     "player":{
[0m         "filename":"alive",
[31m-        "player":"alive"
[0m[32m+        "player":"player"
[0m[0m     },
[0m     "rooms":{
[0m         "filename":"alive",
""")

        repo.do_diff('cached')
        self.assertEqual(repo.fullDiff, """[0m=================================================================
[31m--- old file: game.json in commit 21b4f39
[32m+++ new file: game.json in staged changes

[0m     "alive":true,
[0m     "inventory":{
[0m         "filename":"alive",
[31m-        "player":"alive"
[0m[32m+        "player":"player"
[0m[0m     },
[0m     "player":{
[0m         "filename":"alive",

[0m             "west":"Impressive Caverns"
[0m         }
[0m     }
[31m-}[0m[0m>
\ No newline at end of file
[32m+}
[0m""")

        repo.do_diff('HEAD')
        self.assertEqual(repo.fullDiff, """[0m=================================================================
[31m--- old file: game.json in commit 21b4f39
[32m+++ new file: game.json in working directory

[0m     "alive":true,
[0m     "inventory":{
[0m         "filename":"alive",
[31m-        "player":"alive"
[0m[32m+        "player":"player"
[0m[0m     },
[0m     "player":{
[0m         "filename":"alive",
[31m-        "player":"alive"
[0m[32m+        "player":"player"
[0m[0m     },
[0m     "rooms":{
[0m         "filename":"alive",

[0m             "west":"Impressive Caverns"
[0m         }
[0m     }
[31m-}[0m[0m>
\ No newline at end of file
[32m+}
[0m""")

        repo.do_diff('staged HEAD~1')
        self.assertEqual(repo.fullDiff, """[0m=================================================================
[31m--- characters/alive.jsondoes not exist in commit a7c0de9
[32m+++ new file: characters/alive.json in staged changes

[32m+{
[0m[32m+    "alive":true
[0m[32m+}
[0m[0m=================================================================
[31m--- characters/relationship.jsondoes not exist in commit a7c0de9
[32m+++ new file: characters/relationship.json in staged changes

[32m+{
[0m[32m+    "knows_player": false,
[0m[32m+    "aware_of_presence": false,
[0m[32m+    "hostility_level": 4
[0m[32m+}
[0m[0m=================================================================
[31m--- characters/status.jsondoes not exist in commit a7c0de9
[32m+++ new file: characters/status.json in staged changes

[32m+{
[0m[32m+    "asleep":true
[0m[32m+}
[0m[0m=================================================================
[31m--- old file: game.json in commit a7c0de9
[32m+++ new file: game.json in staged changes

[0m     "alive":true,
[0m     "inventory":{
[0m         "filename":"alive",
[31m-        "player":"alive"
[0m[32m+        "player":"player"
[0m[0m     },
[0m     "player":{
[0m         "filename":"alive",

[0m             "west":"Impressive Caverns"
[0m         }
[0m     }
[31m-}[0m[0m>
\ No newline at end of file
[32m+}
[0m""")

        repo.do_diff('HEAD~1 HEAD')
        self.assertEqual(repo.fullDiff, """[0m=================================================================
[31m--- characters/alive.jsondoes not exist in commit a7c0de9
[32m+++ new file: characters/alive.json in commit 21b4f39

[32m+{
[0m[32m+    "alive":true
[0m[32m+}
[0m[0m=================================================================
[31m--- characters/relationship.jsondoes not exist in commit a7c0de9
[32m+++ new file: characters/relationship.json in commit 21b4f39

[32m+{
[0m[32m+    "knows_player": false,
[0m[32m+    "aware_of_presence": false,
[0m[32m+    "hostility_level": 4
[0m[32m+}
[0m[0m=================================================================
[31m--- characters/status.jsondoes not exist in commit a7c0de9
[32m+++ new file: characters/status.json in commit 21b4f39

[32m+{
[0m[32m+    "asleep":true
[0m[32m+}
[0m""")

    def test_git_log(self):
        """ Test the git log command """

    def test_revparsing(self):
        git = gamerepo.GitCmd('mock-data')
        rev1 = git.revparse('HEAD~2')
        rev2 = git.revparse('revparse')
        rev3 = git.revparse('test')
        rev5 = git.revparse('a7c0d')

        self.assertEqual(rev1.hex[:7], '21b4f39')
        self.assertEqual(rev2.hex[:7], '21b4f39')
        self.assertEqual(rev3.hex[:7], '775c873')
        self.assertEqual(rev5.hex[:7], 'a7c0de9')

        with self.assertRaises(ValueError) as context1:
            git.revparse('0df')

        with self.assertRaises(ValueError) as context2:
            git.revparse('eec655')

        with self.assertRaises(ValueError) as context3:
            git.revparse('fecfda')

        with self.assertRaises(ValueError) as context4:
            git.revparse('notabranch')

        self.assertEqual(str(context1.exception), '0df: ambiguous lookup - OID prefix is too short')
        self.assertEqual(str(context2.exception),'Object is not a commit.')
        self.assertEqual(str(context3.exception),'Object is not a commit.')
        self.assertEqual(str(context4.exception), "Value 'notabranch' does not refer to a git commit")

    def test_statusparsing1(self):
        """ Test statusParse Checking Active Changes """
        self.reset_repo()
        repo = pygit2.Repository('mock-data/.git')

        status = repo.status()
        self.assertEqual(status, {})

        git = gamerepo.GitCmd('mock-data')

        with open(os.path.join(repo.workdir, 'game.json'), 'a') as f:
            f.write('#comment')
        repo.index.add('game.json')
        status = repo.status()
        parsed = git.statusParse('game.json', status['game.json'])
        self.assertEqual(parsed, {'name': 'game.json', 'status': ['Staged File Changes']})

        with open(os.path.join(repo.workdir, 'game.json'), 'a') as f:
            f.write('#comment')
        status = repo.status()
        parsed = git.statusParse('game.json', status['game.json'])
        self.assertEqual(parsed, {'name': 'game.json', 'status':
                            ['Unstaged File Changes','Staged File Changes', ]})

        self.reset_repo()

    def test_statusparsing2(self):
        """ Test statusParse Theoretical States """
        git = gamerepo.GitCmd('mock-data')
        self.assertEqual(git.statusParse('staged_modified', 258), {'name': 'staged_modified', 'status':['Unstaged File Changes','Staged File Changes']})
        self.assertEqual(git.statusParse('ignored', 16384), {'name': 'ignored', 'status': ['Ignored']})
        self.assertEqual(git.statusParse('wtdeleted_staged', 514), {'name': 'wtdeleted_staged', 'status': ['Unstaged File Deletion','Staged File Changes']})

    def test_check_dangers(self):
        self.reset_repo()
        # Test Method on Map Object
        roomsJson = recordable.Recordable('mock-data', 'worldRooms')
        rooms = cavemap.Map(roomsJson)
        danger = rooms.getDanger('Bottomless Pit')
        self.assertEqual(danger, {'entry':'floating'})
        game = gitgame.GitGameCmd('mock-data')
        game.do_north('')
        game.do_north('')
        game.do_west('')
        game.do_west('')    # Enter Bottomless Pit
        alive = game.player.alive
        status = game.player.status
        self.assertTrue(status['floating'])
        self.assertFalse(alive['alive'])
        self.assertTrue(game.postcmd('','')) # True Exits The Game Playing Loop

        self.reset_repo()

    def test_file_check(self):

        fileName1 = os.pardir + os.sep
        fileName2 = "mock-data"
        fileName3 = "fileisnthere.cxx"
        GitCmd = gamerepo.GitCmd('mock-data')
        self.assertFalse(GitCmd.fileIsValid(fileName1))
        self.assertTrue(GitCmd.fileIsValid(fileName2))
        self.assertFalse(GitCmd.fileIsValid(fileName3))

    def test_file_stage(self):
        self.reset_repo()
        game = gitgame.GitGameCmd('mock-data')
        with open(os.path.join(game.repo.workdir, 'game.json'), 'a') as f:
            f.write('#comment')
        game.do_stage('game.json')
        status = game.repo.status()
        parsed = game.statusParse('game.json', status['game.json'])
        self.assertEqual(parsed, {'name': 'game.json', 'status': ['Staged File Changes']})

        self.reset_repo()

    def test_file_unstage(self):

        self.reset_repo()
        game = gitgame.GitGameCmd('mock-data')
        with open(os.path.join(game.repo.workdir, 'game.json'), 'a') as f:
            f.write('#comment')

        with open(os.path.join(game.repo.workdir, 'base.json'), 'a') as f:
            f.write('#comment')
        game.do_stage('game.json')
        game.do_stage('base.json')
        status = game.repo.status()
        parsed1 = game.statusParse('game.json', status['game.json'])
        parsed2 = game.statusParse('base.json', status['base.json'])
        self.assertEqual(parsed1, {'name': 'game.json', 'status': ['Staged File Changes']})
        self.assertEqual(parsed2, {'name': 'base.json', 'status': ['Staged File Changes']})

        game.do_unstage('')

        status = game.repo.status()
        parsed1 = game.statusParse('game.json', status['game.json'])
        parsed2 = game.statusParse('base.json', status['base.json'])
        self.assertEqual(parsed1, {'name': 'game.json', 'status': ['Unstaged File Changes']})
        self.assertEqual(parsed2, {'name': 'base.json', 'status': ['Unstaged File Changes']})

        self.reset_repo()

    def test_gitconfig_identity(self):
        """ Test that one can change identifying information via commandline"""

        game = gitgame.GitGameCmd('mock-data')
        game.do_setname('Aaron Ginns')
        game.do_setemail('yoyoyo@aol.com')

        self.assertEqual(game.repo.config['user.name'], 'Aaron Ginns')
        self.assertEqual(game.repo.config['user.email'], 'yoyoyo@aol.com')

        game.do_setemail('invalidurl')  # invalid email
        self.assertEqual(game.repo.config['user.email'], 'yoyoyo@aol.com')

    def test_createSignature(self):
        """ Test internal createSignature Method """
        game = gitgame.GitGameCmd('mock-data')
        signature = game.createSignature()
        self.assertTrue(isinstance(signature, pygit2.Signature))

    def test_checkCanCommit(self):
        """ Test User Provided Pre-commit Message """
        self.reset_repo()
        game = gitgame.GitGameCmd('mock-data')
        self.assertFalse(game.checkCanCommit()) # No changes
        game.do_north('')
        self.assertFalse(game.checkCanCommit()) # No staged changes
        game.do_stage('location.json')
        self.assertTrue(game.checkCanCommit())

        # Note: writing this test involves both provided command line input
        # And doing a git reset on the tested repo.
        a = "No Test"

unittest.main()
