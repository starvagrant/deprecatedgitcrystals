#!/usr/bin/python3

import cmd, textwrap
from BaseController import *
from ControllerFactory import *

SCREEN_WIDTH = 65

SCREEN_RED = "\033[31m"
SCREEN_ORANGE = "\033[33m"
SCREEN_CYAN = "\033[36m"
SCREEN_GREEN = "\033[32m"
SCREEN_BLUE = "\033[34m"
SCREEN_PURPLE = "\033[35m"
SCREEN_WHITE = "\033[0m"
DEATH_MESSAGE = "***You Are Dead. Commit Your Progress. Type help git for further details.\n"
T = "| "
U = "    "


class ExampleCmd(cmd.Cmd):

    prompt = '\n' + SCREEN_ORANGE + 'Git Gems *> ' + SCREEN_WHITE

    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    def loadControllers(self, controllers):
        self.alive = controllers['alive']
        self.temp = controllers['temp']
        self.worldRooms = controllers['worldRooms']
        self.inventory = controllers['inventory']
        self.characters = controllers['characters']

    def checkDeath(self):
        if self.alive.data['alive'] == True:
            return False
        else:
            return True

    def describeLocation(self):
        if self.checkDeath():
            return textwrap.fill(SCREEN_RED + DEATH_MESSAGE +SCREEN_WHITE, SCREEN_WIDTH)

        location = self.temp.data['location']
        description = SCREEN_CYAN + '\n' + T + location + '\n\n' + SCREEN_WHITE                         # Location Name
        description += U + textwrap.fill(self.worldRooms.data[location]['desc'], SCREEN_WIDTH) + '\n\n' # Location Description
        description += SCREEN_BLUE + T + "Exits" + SCREEN_WHITE + '\n\n'
        for direction in ('north','east','west','south'):
            if direction in self.worldRooms.data[location].keys():
               description += U + direction.title() + " : " + self.worldRooms.data[location][direction]  + '\n' # Exits

        return description

    def changeLocation(self, direction=False):
        if not direction:
            return False

        if self.checkDeath():
            return textwrap.fill(SCREEN_RED + DEATH_MESSAGE +SCREEN_WHITE, SCREEN_WIDTH)

        location = self.temp.data['location']
        if location in self.worldRooms.data.keys():
            if direction in self.worldRooms.data[location]:
                self.temp.data['location'] = self.worldRooms.data[location][direction]
                location = self.temp.data['location']
                if 'danger' in self.worldRooms.data[location]:
                    if "Entry" in self.worldRooms.data[location]['danger']:
                        self.alive.data['alive'] = False
                return self.temp.data['location']
            else:
                return False

    def do_echo(self,args):
        print(args.lower())

    def do_show(self, args):
        print(self.describeLocation())

    def do_north(self, args):
        if self.checkDeath():
            print(SCREEN_RED + DEATH_MESSAGE + SCREEN_WHITE)
        else:
            if not (self.changeLocation('north')):
                print(SCREEN_RED + "You cannot go north" + SCREEN_WHITE)

            print(self.describeLocation())

    def do_south(self, args):
        if self.checkDeath():
            print(SCREEN_RED + DEATH_MESSAGE + SCREEN_WHITE)
        else:
            if not (self.changeLocation('south')):
                print(SCREEN_RED + "You cannot go south" + SCREEN_WHITE)

            print(self.describeLocation())

    def do_east(self, args):
        if self.checkDeath():
            print(SCREEN_RED + DEATH_MESSAGE + SCREEN_WHITE)
        else:
            if not (self.changeLocation('east')):
                print(SCREEN_RED + "You cannot go east" + SCREEN_WHITE)

            print(self.describeLocation())

    def do_west(self, args):
        if self.checkDeath():
            print(SCREEN_RED + DEATH_MESSAGE + SCREEN_WHITE)
        else:
            if not (self.changeLocation('west')):
                print(SCREEN_RED + "You cannot go west" + SCREEN_WHITE)

            print(self.describeLocation())

if __name__ == '__main__':

    # Initialize Objects, send them to command loop
    factory = ControllerFactory()
    controllers = factory.initGame()
    game = ExampleCmd()
    game.loadControllers(controllers)

    # Play Game
    print(game.describeLocation())
    game.cmdloop()
    print("Bye!")
