#!/usr/bin/python3

import gamerepo, gitgame, recordable

playing = True
aliveJson = recordable.Recordable('saved-game', 'alive')
gameIntro = """    Welcome to Git Crystals!')
    ========================')

    Type "help" for commands.'
    Press Ctrl-C to Quit at Any Time
"""
gitIntro = """     Welcome to Git Crystals!
    ========================')
    You are dead. Git Crystals
    is playing in Git Mode.
    Press Ctrl-C to Quit at Any Time
"""

while playing:
    if aliveJson.data['alive'] == True:
        game = gitgame.GitGameCmd('saved-game')
        print(gameIntro)
        print(game.displayPlayerLocation(game.map))
        game.cmdloop()
        aliveJson.load()
    else:
        game = gamerepo.GitCmd('saved-game')
        print(gitIntro)
        game.cmdloop()
        aliveJson.load()

    gameContinue = input('Continue Y/N?')
    if gameContinue.lower() == 'n':
        break
