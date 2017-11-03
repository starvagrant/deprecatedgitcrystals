# Git Crystals: A Git Tutorial Game

## Under Development ##
Git Crystals is not currently a working project. When it is, this notice will be removed.
Read on:

Git Crystals is a text based game designed to teach the git version control system.
Learning the git version control system typically leaves the learning with the following conundrum:

1. You can't really understand what git is useful for until you start using it.
2. You can't really start using git until you understand it.

**Every solution I've seen for getting through this conundrum involves this:**

1. I know it's hard and doesn't make sense. Just keep using it.
2. I know it doesn't seem useful, but just keep learning about it.
3. You'll realize how awesome it is eventually.

The above approach is fine for developers, for whom source control is a necessary skill. They are
likely surrounded by other developers that will encourage learning git, make it a requirement for
a project, etc. I learned git because I was lead to believe as a developer I would have to. But for
those curious about the technology for other reasons, this approach is woefully in adequate.

**The game Git Crystals take the following approach:**

1. Make learning git actually fun.
2. Get the user using git immediately. Don't worry about whether the user "understands" git "correctly". Understanding will grow after use.
3. Though the game is text based for simplicity, do not expect familiarity with the command line.

**The Setup:**

Git crystals is a Python 3 script that makes use of the Python bindings for the libgit2 C library (The module pygit2) which is not
included in this repo. There may be a pre-compiled version for your operating system that you can grab with pip3. (The case for Ubuntu). Otherwise you might have to compile it. If so, make sure you compile the version of the libgit2 library pygit2 is built on (as of this writing 0.26, but check the docs), which is not necessarily the most up-to-date version of the C library. When you get pygit2 installed, playing is just a matter of running the executable gitgame.py.

I'm not planning on making use of super-advanced features of Python, so getting the latest version for your OS should be sufficient to fulfill this requirement. The current trick is getting pygit2 on your computer. This involves compiling the correct version of libgit2, which is 0.26. You have to compile the python module against the version of libgit that the module is built against, which is not necessarily the latest. I plan on writing more documentation and getting more cross-platform support when I get the programming running on my own computer in the first place.
