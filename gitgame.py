#!/usr/bin/python3

import cmd, textwrap, json, os

DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
UP = 'up'
DOWN = 'down'
GROUND = 'ground'
SHOP = 'shop'
GROUNDDESC = 'grounddesc'
SHORTDESC = 'shortdesc'
LONGDESC = 'longdesc'
TAKEABLE = 'takeable'
EDIBLE = 'edible'
DESCWORDS = 'descwords'
DANGER = 'danger'

SCREEN_WIDTH = 80

SCREEN_RED = "\033[31m"
SCREEN_ORANGE = "\033[33m"
SCREEN_CYAN = "\033[36m"
SCREEN_GREEN = "\033[32m"
SCREEN_BLUE = "\033[34m"
SCREEN_PURPLE = "\033[35m"
SCREEN_WHITE = "\033[0m"

game = {}

def loadJsonFromFile(game_json, fileDir = "saved-game"):
    """ Load a single json file """
    fileName = fileDir + "/" + game_json + ".json" # Load Json
    with open(fileName, 'r') as f:
        text = f.read()
        return(json.loads(text))

def loadGameData(game_dir = "saved-game"):
    """ load all files in a directory. All files most be json and have a .json extension """
    for directory in os.walk(game_dir):
        for fileName in directory[2]:        # the file name list
            f = fileName[:-5]                # cut .json extension
            game[f] = loadJsonFromFile(f, game_dir)

    return game

def writeGameData(game, fileDir = "saved-game"):
    for saveData in game:
        saveGame = fileDir + "/" + saveData + '.json'
        with open(saveGame, 'w') as f:
            f.write(json.dumps(game[saveData], sort_keys=True,
                               indent=4, separators=(',',':')))
            f.close()

    return game.keys()

def displayLocation(location):
    """A helper function for displaying an area's description and exits."""
    # Print the room name.
    print(location)
    print('=' * len(location))

    # Print the room's description (using textwrap.wrap())
#    print('\n'.join(textwrap.wrap(game['rooms'][location][DESC], SCREEN_WIDTH)))
    # Print all the exits.
    exits = []
    for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
        if direction in game['rooms'][location].keys():
            exits.append(direction.title())
            print()
    for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
        if direction in game['rooms'][location]:
            print('%s: %s' % (direction.title(), game['rooms'][location][direction]))

def moveDirection(direction):
    """A helper function that changes the location of the player."""
    global game

    location = game['temp']['location']

    if direction in game['rooms'][location]:
        print("Moving to... %s" % direction)
        game['temp']['location'] = game['rooms'][location][direction]

        displayLocation(game['temp']['location'])

        if location in game['rooms']:
            if 'danger' in game['rooms'][location].keys() and 'Entry' in game['rooms'][location]['danger']:
                game['alive'] = False
                report_death()
                return
    else:
        print('You cannot move in that direction')

def report_death():
   print()
   print(SCREEN_RED + 'You are dead \n')
   print(SCREEN_GREEN + 'Commit your progress or restart')
   print(SCREEN_CYAN + 'Type help git for tutorial' + SCREEN_WHITE + '\n')

class ExampleCmd(cmd.Cmd):

    prompt = '\n\033[033m *>\033[0m '
    global game

    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    def do_echo(self, arg):
        """ echo what the user says """
        print(arg)

    def do_north(self, arg):
        """ head north if possible """
        if not(game['alive']):
            report_death()
            return
        moveDirection('north')

    def do_south(self, arg):
        """ head south if possible """
        if not(game['alive']):
            report_death()
            return
        moveDirection('south')

    def do_east(self, arg):
        """ head east if possible """
        if not(game['alive']):
            report_death()
            return
        moveDirection('east')

    def do_west(self, arg):
        """ head west if possible """
        if not(game['alive']):
            report_death()
            return
        moveDirection('west')

    def do_up(self, arg):
        """ go up if possible """
        if not(game['alive']):
            report_death()
            return
        moveDirection('up')

    def do_down(self, arg):
        """ go down if possible """
        if (not game['alive']):
            report_death()
            return
        moveDirection('down')

    def do_talk(self, arg):
        """ Command usage: talk person """
        print("Yak. Yak. Yak.")

    def do_look(self, arg):
        """ Command usage: look room
        Or: look object, look person, etc. """
        print("It looks nice.")

    def do_search(self, arg):
        """ Command usage: search room
        Evaluate an object, room, or person """

    def do_take(self, arg):
        """ take an object """

    def do_mix(self, arg):
        """ Mix two or more ingredients """
        print(arg.split(" "))

    def do_assess(self,arg):
        """ assess your player condition """
        print("You're fine")

    def do_shoot(self, arg):
        """ launch a projectile at a target """
        print(arg.split(" "))

    def do_give(self, arg):
        """ launch a projectile """
        print(arg.split(" "))

    def do_complete(self,arg):
        """ finish an interrupted command """
        print("Previous command incompete")
        print("Specify <arg>)")

    def do_git(self,arg):
        """ use a git command """
        print("Using an awesome version control command")

    def do_load(self,arg = 'saved-game'):
        """ Load a file """
        game = loadGameData()

    def do_write(self,arg):
        """ Write a file """
        print(writeGameData(game))

    def do_vardump(self,arg):
        """ give user ability to test loaded variables """
        key = arg.lower()
        print(repr(game[key]))

    def do_kill(self,arg):
        """ Command for killing things """
        target = arg.lower()
        if target == "yourself":
            game['alive'] = "False"
        print("You killed " + target)

    def do_guts(self,arg):
        print(repr(game))

    def get_game(self):
        return game

if __name__ == '__main__':
    print("Example")
    print("=======")

    game = loadGameData()
    displayLocation(game['temp']['location'])
    ExampleCmd().cmdloop()
    print("Bye!")
