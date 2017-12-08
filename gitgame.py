#!/usr/bin/python3
import cmd
import recordable
import cavemap,character
import gamerepo

SCREEN_WIDTH = 65
S_RED = "\033[31m"
S_ORA = "\033[33m"
S_CYA = "\033[36m"
S_GRE = "\033[32m"
S_BLU = "\033[34m"
S_PUR = "\033[35m"
S_WHI = "\033[0m"

class GitGameCmd(gamerepo.GitCmd):
    prompt = '\n\033[0mGit Crystals> '

    def __init__(self, gamedir="saved-game"):
        super().__init__(gamedir)

        self.gamedir = gamedir

        # Player Data
        inventory = recordable.Recordable(gamedir, 'inventory')
        alive = recordable.Recordable(gamedir, 'alive')
        status = recordable.Recordable(gamedir, 'status')
        location = recordable.Recordable(gamedir, 'location')
        playerRecordables = [inventory,alive,status,location]

        # Player Variable
        self.player = character.Character(playerRecordables)

        # Map
        worldMap = recordable.Recordable(gamedir, 'worldRooms')
        self.map = cavemap.Map(worldMap)

    def default(self, args):
        print("I do not understand that command. Type help for a list of commands.")

    def displayPlayerLocation(self, mapObject):
        location = self.player.location['location']

        text = S_BLU + '+'*SCREEN_WIDTH + '\n'
        text += "    You are located in the " + S_CYA + location + S_BLU + '\n'
        text += "The adjacent rooms are :\n"
        for direction in ('north','east','south','west'):
            if self.map.move(direction,location) is not None:
                text += direction + ": " + S_GRE + self.map.move(direction, location) + S_BLU + "\n"
        text += S_BLU + '+'*SCREEN_WIDTH + S_WHI + '\n'

        return text

    def do_north(self, args):
        self.player.move('north', self.map)
        print(self.displayPlayerLocation(self.map))

    def do_south(self, args):
        self.player.move('south', self.map)
        print(self.displayPlayerLocation(self.map))

    def do_east(self, args):
        self.player.move('east', self.map)
        print(self.displayPlayerLocation(self.map))

    def do_west(self, args):
        self.player.move('west', self.map)
        print(self.displayPlayerLocation(self.map))

if __name__ == '__main__':
    print('Welcome to Git Crystals!')
    print('========================')
    print()
    print('(Type "help" for commands.)')
    print()
    GitGameCmd().cmdloop()
    print('Thanks for playing!')
