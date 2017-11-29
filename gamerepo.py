#!/usr/bin/python3
import cmd
import pygit2

SCREEN_WIDTH = 65
S_RED = "\033[31m"
S_ORA = "\033[33m"
S_CYA = "\033[36m"
S_GRE = "\033[32m"
S_BLU = "\033[34m"
S_PUR = "\033[35m"
S_WHI = "\033[0m"
DEATH_MESSAGE = "***You Are Dead. Commit Your Progress. Type help git for further details.\n"

class GitCmd(cmd.Cmd):


    def __init__(self, repodir="saved-game"):
        super().__init__()

        self.gamedir = repodir
        prompt = '\n Git Mode> '
        repoName = repodir + '/.git'
        self.repo = pygit2.Repository(repoName)
        self.currentMessage = ''

    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    # A very simple "quit" command to terminate the program:
    def do_quit(self, arg):
        """Quit the game."""
        return True # this exits the Cmd application loop in TextAdventureCmd.cmdloop()

    def do_status(self, arg):
        """
        GIT_STATUS_CURRENT = 0
        GIT_STATUS_IGNORED = 16384
        GIT_STATUS_INDEX_DELETED = 4
        GIT_STATUS_INDEX_MODIFIED = 2
        GIT_STATUS_INDEX_NEW = 1
        GIT_STATUS_WT_DELETED = 512
        GIT_STATUS_WT_MODIFIED = 256
        GIT_STATUS_WT_NEW = 128
        for filepath, flags in status.items():
            if flags != GIT_STATUS_CURRENT:
                print("Filepath %s isn't clean" % filepath)
        """
        status = self.repo.status()
        self.currentMessage = repr(status)
        print(self.currentMessage)

    def do_diff(self,arg):
        """
        Calculates the Diff between two commits
        DiffLine object: content_offset, content, origin, old_lineno, new_lineno
        """
        ref1 = "HEAD~2"
        ref2 = "HEAD"
        c1 = self.repo.revparse_single(ref1)
        c2 = self.repo.revparse_single(ref2)
        diff = self.repo.diff(c1, c2)

        fullDiff = S_RED + '--- prev: ' + ref1 + ' (commit ' + c1.hex[:7] + ')\n'
        fullDiff += S_GRE + '+++ current: ' + ref2 + ' (commit ' + c2.hex[:7] + ')\n'
        patches = [p for p in diff]
        for p in patches:
            fullDiff += S_WHI + '='*SCREEN_WIDTH + '\n'
            fullDiff += S_RED

            if p.delta.status == 1:
                fullDiff += '--- ' + p.delta.old_file.path + ' does not exist in commit ' + c1.hex[:7] + '\n'
            else:
                fullDiff += '--- old file: ' + p.delta.old_file.path + ' in commit ' + c1.hex[:7] + '\n'

            fullDiff += S_GRE
            if p.delta.status == 2:
                fullDiff += '+++ ' + p.delta.new_file.path + ' does not exist in commit ' + c1.hex[:7] + '\n'
            else:
                fullDiff += '+++ new file: ' + p.delta.new_file.path + ' in commit ' + c2.hex[:7] + '\n'

            fullDiff += S_WHI + '='*SCREEN_WIDTH + '\n'

            for h in p.hunks:
                fullDiff += '\n'
                for l in h.lines:
                    if l.origin == '-':
                        fullDiff = S_RED + l.origin + l.content + S_WHI
                    elif l.origin == '+':
                        fullDiff += S_GRE + l.origin + l.content + S_WHI
                    else:
                        fullDiff += l.origin + l.content + S_WHI

                fullDiff += '\n'

        self.fullDiff = fullDiff
        print(self.fullDiff)

if __name__ == '__main__':
   print("Git Command Line")
   game = GitCmd('mock-data')
   game.cmdloop()
