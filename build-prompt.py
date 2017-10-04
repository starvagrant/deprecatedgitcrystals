#!/usr/bin/python3

import cmd, textwrap

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
        print(arg.split(" ")

    def do_give(self, arg):
        """ launch a projectile """
        print(arg.split(" ")

    def do_complete(self,arg):
        """ finish an interrupted command """
        print("Previous command incompete")
        print("Specify <arg>)")

    def do_git(self,arg):
        """ use a git command """
        print("Using an awesome version control command")


if __name__ == '__main__':
    print("Example")
    print("=======")
    ExampleCmd().cmdloop()
    print("Bye!")
