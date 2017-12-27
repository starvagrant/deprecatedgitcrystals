# Git Crystals: Git, the Video Game

## Under Development
Git Crystals is Under Development. Please See The Disclaimers section
before trying to use it.

## Git Crystals (the game)
Git Crystals is a text based adventure game that uses the git version
control system as its major mechanic. _What does that mean_?

That means it's a little like those old 80's DOS games the require
you to type a command in order to get your character to do something.
A good text based puzzle game is full of explorations, riddles, creative
mixing and using of items, and other thinking challenges. Above all,
experimentation is part of the game. It just so happens that a simplified
version of git is a major game mechanic you can use to solve problems.

_How does that work exactly_? Git is used by pro's in the software
industry to keep track of changes in files. In Git Crystals, all
data is kept in reasonably readable text files. For instance, when
change rooms, your location is kept in a file. When you die, the fact
that you are not alive is kept in a different file. You can use git
to track and manipulate how game data is stored, and cause the game
to forget that you are dead but remember where you are.

Entering rooms with deadly traps, carrying infinite items, telling
a character two conflicting pieces of information so you can receive
the rewards for saying both: these are the methods that can get you
through your adventures in Git Crystals.

## Git Crystals (the philosophy)
If you're just interested in playing the game skip to requirements. But
I also wanted to add some of the thinking going behind this project. The
major thinking behind this project is simple. Your first experience with
the git version control system does not have to be frustration,confusion,
and feelings with inadequacy. In fact, as a game designer, I'd be happy
if the user had fun with my game, understood the basics of how git worked,
and never ended up finding a use for it later on. Of course, I love git
as a tool and hope I can get the end user started on wanting to use it
in their personal work (or at least not shoot down the idea if a developer is
interested in implementing it in a work place).

Git, in real life, had most of its implementation decisions based on
performance and flexibility: not ease of entry for the newbie. The Git
Crystals project is an attempt to push things in a different direction.
It is also intended to fill a noticeable gap in the numerous git tutorials
out there. Almost every manual explains git. Git Crystals has you using
git, no coding experience required!

## Git Crystals (the reassurances)
1. Git Crystals requires no coding experience. It does involve looking
at data in JSON format, which should be simple enough to understand for
the novice.
2. Though git crystals is meant to played in a command line interface,
it does not require any knowledge of the command line.
3. Since Git Crystals manages all game data in a git repository, you
can manage your game with other implementations of git than the simple
version employed within the game engine. This includes graphical and
text-based implementation.

**The Setup:**

Git crystals is a Python 3 script that makes use of the Python bindings
for the libgit2 C library (The module pygit2). Here's what you'll
need to play:

- python3
- libgit2
- pygit2

## Installation

### MacOS X

Commands:
1. /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
2. brew install python3
3. brew install libgit2
4. brew install pip3
5. pip3 install pygit2
6. git clone https://github.com/starvagrant/gitcrystals
7. cd gitcrystals
8. chmod u+x game.py
9. ./game.py

Explanation:
1. Install Homebrew, the Mac OS package manager
2. Install Python3 (modern MacOS only comes with Python 2.7)
3. Install The Git C bindings
4. Install Python3's package manager
5. Install the Python3 package pygit2, which allows Python to use libgit2
6. Clone the git repo
7. cd into created gitcrystals directory
8. Ensure file has execute permissions.
9. Call the game file.

### Ubuntu 16.04
1. sudo apt install python3-pip
2. pip3 install pygit2
3. git clone https://github.com/starvagrant/gitcrystals
4. cd gitcrystals
5. chmod u+x game.py
6. ./game.py

1. Install pip3, Python's package manager
2. Install pygit2 python package.
3. Clone the gitcrystals repo.
4. cd into gitcrystals directory
5. in case executable permission is not set for game.py
6. Call the game file

# Windows
There are known inconsistencies between git's behavior on Windows and Linux.
As I have not done development work to handle them, I suggest either buying
me a Windows computer or hiring a Windows developer to port this code.

# Other Operating Systems should have similar installation methods:
1. Get a python3 interpreter if your system doesn't have one.
2. Get a python3 package manager to go with your interpret
3. Install the pygit2 library the game depends on
4. Clone the Git Crystals repo.

If for some reason you get stuck trying to compile this program's
dependencies (python3, python3 standard libraries, and the pygit2
package. **You have to compile the right version of the libgit2 C
library against the right version of pygit2** See pygit2's repository
on Github for the most up-to-date instructions.
