#!/usr/bin/python3

import cmd, textwrap

class ExampleCmd(cmd.Cmd):

    prompt = '\n\033[033m *>\033[0m '

    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    def do_help(self, arg):
        print('Help not avialable on <' + arg + '>')

if __name__ == '__main__':
    print("Example")
    print("=======")
    ExampleCmd().cmdloop()
    print("Bye!")
