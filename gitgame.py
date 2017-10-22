#!/usr/bin/python3


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


    def do_echo(self,arg):
        print(arg.lower())


if __name__ == '__main__':

    # Play Game
    game.cmdloop()
    print("Bye!")
