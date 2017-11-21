#!/usr/bin/python3
import cmd
import recordable
import cavemap,character

class GitGameCmd(cmd.Cmd):
    def __init__(self, gamedir="saved-game"):
        super().__init__()

        self.gamedir = gamedir
        prompt = '\n Git Crystals> '

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

    def do_north(self, args):
        self.player.move('north', self.map)

    def do_south(self, args):
        self.player.move('south', self.map)

    def do_east(self, args):
        self.player.move('east', self.map)

    def do_west(self, args):
        self.player.move('west', self.map)

if __name__ == '__main__':
    print('Welcome to Git Crystals!')
    print('========================')
    print()
    print('(Type "help" for commands.)')
    print()
    GitGameCmd().cmdloop()
    print('Thanks for playing!')
