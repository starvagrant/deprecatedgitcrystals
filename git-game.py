#!/usr/bin/python3

import cmd, textwrap, json

game = { "player": None, "alive": True, "inventory": None, "rooms" : None, "characters": None}

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

worldRooms = {
    'Abandoned Treasury': {
    DESC: 'An Abandoned Treasury Lies Before You. The room glitters and is full of treasure chests. Something smells of smoke',
    EAST: 'Dragon\'s Lair',
    SOUTH: 'Alchemist Lab',
    GROUND: ['Charcoal', 'Treasure Chest Key'],
    DANGER: ['Search']},

    'Alchemist Lab': {
    DESC: 'You see the Liquids and Vial\'s of an Alchemist Lab. A friendly Alchemist awaits, perhaps ready to do business',
    NORTH: 'Abadoned Treasury',
    WEST: 'Bottomless Pit',
    EAST: 'Stalagmite Central',
    SOUTH: 'Git Crystal',
    GROUND: ['Git Checkout Tutorial']},

    'Armory': {
    DESC: 'You see the armory. Swords, Spears, Polearms, Chainmail, and other items lay bent and burnt. There might still be something in working condition somewhere',
    NORTH: 'Mine Entrance',
    GROUND: ['Shield']},

    'Bottomless Pit': {
    DESC: 'Before you lies a hole from which no light escapes',
    WEST: 'Bottomless Pit',
    EAST: 'Alchemist Lab',
    GROUND: ['Dungeon Map'],
    DANGER: ['Entry']},

    'Dragon\'s Lair': {
    DESC: 'The following room contains enough gold to rule ten kingdoms. The dragon protecting it has not killed you yet. Perhaps it is sleeping',
    WEST: 'Abandoned Treasury',
    SOUTH: 'Stalagmite Central',
    GROUND: ['Sword','Crown'],
    DANGER: ['Noise']
    },

    'Git Crystal': {
    DESC: 'A large, skyblue crystal is in the center of a perfectly spherical room. The crystal looks like ones you\'ve seen in your grandfather\'s Workshop',
    NORTH: 'Stalagmite Central',
    EAST: 'Mine Entrance',
    SOUTH: 'Mountain Gate',
    WEST: 'Wizard\'s Library',
    GROUND: ['Intro Git Tutorial', 'Git Status Tutorial']},

    'Impressive Caverns': {
    DESC: 'Before you lies a large and winding maze of passageways. Is something lurking in here? You could get lost trying to find it',
    EAST: 'Wizard\'s Library',
    GROUND: ['Skeleton Key']},

    'Mine Entrance': {
    DESC: 'You see an expansive tunnel. A sign reads \'Dig Ore Get Out. With puns like this, it\'s no wonder it\'s abandoned.',
    EAST: 'Mines',
    SOUTH: 'Armory',
    WEST: 'Git Crystal',
    GROUND: ['Git Branch Tutorial','Git Merge Tutorial', 'Toolkit']},

    'Mines': {
    DESC: 'A labyrinth of passageways and abandoned mine equipment in good condition confront you',
    WEST: 'Mine Entrace',
    GROUND: ['Saltpeter'],
    DANGER: ['Search']},

    'Mountain Gate': {
    DESC: 'A sign reads: No Trespassing. Beware of Dragon',
    NORTH: 'Git Crystal',
    GROUND: ['No Trepassing Sign']
    },

    'Stalagmite Central': {
    DESC: 'Rocks rise from the floor in every part of this room. This is the place to be, if rocks are your best friend',
    NORTH: 'Dragon\'s Lair',
    SOUTH: 'Git Crystal',
    WEST: 'Alchemist Lab',
    GROUND: ['Stalagmite', 'Stalagmite']
    },

    'Wizard\'s Library': {
    DESC: 'A musty odor fills the air from the books, books, and more books that fill this old wizard\'s study. Maybe there\'s a tutorial?',
    NORTH: 'Alchemist Lab',
    EAST: 'Git Crystal',
    WEST: 'Impressive Caverns',
    GROUND: ['Git Diff Tutorial, Git Commit Tutorial']
    }
}

currentRoom = 'Mountain Gate'
showFullExits = True

def loadJsonFromFile(game_json):
    fileName = "saved-game/" + game_json + ".json" # Load Json
    with open(fileName, 'r') as f:
        text = f.read()
        return(json.loads(text))

def loadGameData(game):
    for fileName in game:
        f = fileName
        game[f] = loadJsonFromFile(f)

def writeGameData(game):
    for fileName in game:
        fi = fileName
        saveGame = "saved-game/" + fi + ".json"
        with open(saveGame, 'w') as f:
            f.write(json.dumps(game[fi], sort_keys=True,
                               indent=4, separators=(',',':')))
            return "Game Written"

def displayLocation(location):
    """A helper function for displaying an area's description and exits."""
    # Print the room name.
    print(location)
    print('=' * len(location))

    # Print the room's description (using textwrap.wrap())
    print('\n'.join(textwrap.wrap(worldRooms[location][DESC], SCREEN_WIDTH)))

    # Print all the exits.
    exits = []
    for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
        if direction in worldRooms[location].keys():
            exits.append(direction.title())
            print()
    if showFullExits:
        for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
            if direction in worldRooms[location]:
                print('%s: %s' % (direction.title(), worldRooms[location][direction]))

def moveDirection(direction):
    """A helper function that changes the location of the player."""
    global currentRoom
    global game

    if direction in worldRooms[currentRoom]:
        print("Moving to... %s" % direction)
        currentRoom = worldRooms[currentRoom][direction]
        displayLocation(currentRoom)
        if DANGER in worldRooms[currentRoom].keys() and 'Entry' in worldRooms[currentRoom][DANGER]:
            game['alive'] = False
            report_death()
            return
        print(repr(worldRooms[currentRoom]))
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

    def do_load(self,arg):
        """ Load a file """
        print(loadJsonFromFile(arg))

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

if __name__ == '__main__':
    print("Example")
    print("=======")

    loadGameData(game)
    displayLocation(currentRoom)
    ExampleCmd().cmdloop()
    print("Bye!")
