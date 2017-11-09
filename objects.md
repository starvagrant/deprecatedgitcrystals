# Git Game Objects:

Game: Command Loop
Repo: Pygit2 object

Other Objects:
Creatures
---------
Player,
NPC's,
Monsters,

Rooms
Items
Traps

Rooms can Contain
    Players, NPC's, Monsters, Rooms, Items, Traps

Players can
    die
    talk to NPC's
    rescue NPC's (if captured)
    attack NPC's (counterproductive, but possible)
    change rooms

NPC's can
    talk to player
    get rescued
    get killed
    receive items

Items
    be picked up
    be dropped
    be mixed with other items
    be equipped (if weapon / armor)

Traps
    can kill player
    can be disarmed

Repositories
    can save game information
    can load game information
    can manipulate game information via version control

### Consider a session class that contains all the data/functions to handle what the player can do / needs to know, etc. A session would include a player's life status, location, inventory, and generally determine what valid actions / input.

### Another idea: many objects are going to have their json file read and written. Objects need to have methods that don't need changing, reading, or writing, and data that does.
