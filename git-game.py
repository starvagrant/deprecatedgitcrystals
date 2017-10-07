#!/usr/bin/python3

import cmd, textwrap, json

game = { "player": None, "alive": None, "inventory": None, "rooms" : None, "characters": None}

def loadJsonFromFile(game_json):
    fileName = "saved-game/" + game_json + ".json" # Load Json
    with open(fileName, 'r') as f:
        text = f.read()
        return(json.loads(text))

def writeJsonToFile(game_json):
    fileName = "saved-game/" + game_json['file_name'] + ".json" # Write Json
    with open(fileName, 'w') as f:
        f.write(json.dumps(game_json, sort_keys=True,
                          indent=4, separators=(',', ':')))
        return "Json Written"

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

class ExampleCmd(cmd.Cmd):

    prompt = '\n\033[033m *>\033[0m '

    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    def do_echo(self, arg):
        """ echo what the user says """
        print(arg)

    def do_north(self, arg):
        """ head north if possible """
        print("Going North")

    def do_south(self, arg):
        """ head south if possible """
        print("Going South")

    def do_east(self, arg):
        """ head east if possible """
        print("Going East")

    def do_west(self, arg):
        """ head west if possible """
        print("Going West")

    def do_up(self, arg):
        """ go up if possible """
        print("Going West")

    def do_down(self, arg):
        """ go down if possible """
        print("Going West")

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
            game['alive'] = "false"
        print("You killed " + target)

if __name__ == '__main__':
    print("Example")
    print("=======")

    loadGameData(game)
    ExampleCmd().cmdloop()
    print("Bye!")
