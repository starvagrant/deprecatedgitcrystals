#!/usr/bin/python3

import cmd, textwrap
from BaseController import *
from ControllerFactory import *

SCREEN_WIDTH = 80

SCREEN_RED = "\033[31m"
SCREEN_ORANGE = "\033[33m"
SCREEN_CYAN = "\033[36m"
SCREEN_GREEN = "\033[32m"
SCREEN_BLUE = "\033[34m"
SCREEN_PURPLE = "\033[35m"
SCREEN_WHITE = "\033[0m"


class ExampleCmd(cmd.Cmd):

    prompt = '\n' + SCREEN_ORANGE + 'Git Gems *>' + SCREEN_WHITE

    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    def loadControllers(self, controllers):
        self.alive = controllers['alive']
        self.temp = controllers['temp']
        self.worldRooms = controllers['worldRooms']
        self.inventory = controllers['inventory']
        self.characters = controllers['characters']


    def do_echo(self,arg):
        print(arg.lower())


if __name__ == '__main__':

    # Initialize Objects, send them to command loop
    factory = ControllerFactory()
    controllers = factory.initGame()
    game = ExampleCmd()
    game.loadControllers(controllers)

    # Play Game
    game.cmdloop()
    print("Bye!")
