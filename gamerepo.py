#!/usr/bin/env python3
import cmd,os
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

    prompt = S_WHI + '\n Git Mode> '

    def __init__(self, repodir="saved-game"):
        super().__init__()

        repoName = repodir + os.sep + '.git'
        self.repo = pygit2.Repository(repoName)
        self.currentMessage = ''

    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    def revparse(self, obj):
        err = None
        if obj == 'staged' or obj == 'cached':
            return obj
        try:
            ref = self.repo.revparse_single(obj)
            if not isinstance(ref, pygit2.Commit):
                raise ValueError("Object is not a commit.")
        except KeyError as k:
            err = 'Value ' + str(k) + ' does not refer to a git commit'
        except (KeyError,ValueError) as e:
            err = str(e)
        finally:
            if err is not None:
                raise ValueError(err)

        return ref

    def formatPatch(self, patch, before, after):
        screen = S_WHI + '='*SCREEN_WIDTH + '\n'
        delta = patch.delta

        screen += S_RED
        if delta.status == 1:   # File Added
            screen += '--- ' + delta.old_file.path + "does not exist in " + before + '\n'
        else:
            screen += '--- old file: ' + delta.old_file.path + ' in ' + before + '\n'

        screen += S_GRE
        if delta.status == 2:  # File Removed
            screen += '+++ ' + delta.new_file.path + ' does not exist in ' + after + '\n'
        else:
            screen += '+++ new file: ' + delta.new_file.path + ' in ' + after + '\n'

        for hunk in patch.hunks:
            screen += '\n'
            for line in hunk.lines:
                if line.origin == '-':
                    screen += S_RED + line.origin + line.content + S_WHI
                elif line.origin == '+':
                    screen += S_GRE + line.origin + line.content + S_WHI
                else:
                    screen += S_WHI + line.origin + line.content

        return screen

    def statusParse(self, fileName, num):
        status = {'name': fileName, 'status': [] }
        if num > 17287 or num < 0:
            raise ValueError('Status Number Out of Bounds')
        if num//16384 > 0:
            status['status'].append('Ignored')
            num -= 16384
        if num//512 > 0:
            status['status'].append('Unstaged File Deletion')
            num -= 512
        if num//256 > 0:
            status['status'].append('Unstaged File Changes')
            num -= 256
        if num//128 > 0:
            status['status'].append('Untracked File')
            num -= 128
        if num//4 > 0:
            status['status'].append('Staged File Deletion')
            num -= 4
        if num//2 > 0:
            status['status'].append('Staged File Changes')
            num -= 2
        if num % 2 == 1:
            status['status'].append('Staged New File')

        return status

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
        entries = []
        for fileName in status.keys():
            entries.append(self.statusParse(fileName, status[fileName]))

        staged = []
        unstaged = []
        untracked = []

        for entry in entries:
            if entry['status'].__contains__('Staged File Deletion') or entry['status'].__contains__('Staged File Changes') or entry['status'].__contains__('Staged New File'):
                staged.append(entry)

            if entry['status'].__contains__('Unstaged File Deletion') or entry['status'].__contains__('Unstaged File Changes'):
                unstaged.append(entry)
            if entry['status'].__contains__('Untracked File'):
                untracked.append(entry)

        self.statusMessage = S_BLU + "Repository Status" + '\n'
        self.statusMessage += '-'*SCREEN_WIDTH + '\n'
        if len(staged) > 0:
            self.statusMessage += S_GRE + "Staging Area" + '\n' + '    Files:' + '\n'
            for fileName in staged:
                self.statusMessage += '     ' + fileName['name']
                for state in fileName['status']:
                    if state.startswith('Staged'):
                        self.statusMessage += " " + state + '\n'
            self.statusMessage += '\n' + S_WHI
        if len(unstaged) > 0:
            self.statusMessage += S_RED + "Unstaged Changes" + '\n' + '    Files:' +  '\n'
            for fileName in unstaged:
                self.statusMessage += '     ' + fileName['name']
                for state in fileName['status']:
                    if state.startswith('Unstaged'):
                        self.statusMessage += " " + state + '\n'
            self.statusMessage += '\n' + S_WHI
        if len(untracked) > 0:
            self.statusMessage += S_CYA + "Untracked Files" + '\n' + '    Files:' + '\n'
            for fileName in untracked:
                self.statusMessage += '     ' + fileName['name']
                for state in fileName['status']:
                    if state.startswith('Untracked'):
                        self.statusMessage += " " + state + '\n'
            self.statusMessage += '\n' + S_WHI

        print(self.statusMessage)

    def do_diff(self,arg):
        """
        Calculates the Diff between two commits
        DiffLine object: content_offset, content, origin, old_lineno, new_lineno
        """
        args = arg.split()
        try:
            if len(args) > 2:
                self.fullDiff = "Can only diff two commits"
                print(self.fullDiff)
                return

            commits = []
            for a in args:
               commits.append(self.revparse(a))

            if args == []:
                diff = self.repo.diff()
                before = "commit " + self.revparse('HEAD').hex[:7]
                after = "unstaged changes"
            elif commits[0] == 'cached' or commits[0] == 'staged' and len(commits) < 2:
                diff = self.repo.diff('HEAD', cached=True)
                before = "commit " + self.revparse('HEAD').hex[:7]
                after = "staged changes"
            elif commits[0] == 'cached' or commits[0] == 'staged' and isinstance(commits[1], pygit2.Commit):
                diff = self.repo.diff(a = commits[1], cached=True)
                before = "commit " + commits[1].hex[:7]
                after = "staged changes"
            elif isinstance(commits[0], pygit2.Commit) and len(commits) < 2:
                diff = self.repo.diff(a = commits[0])
                before = "commit " + commits[0].hex[:7]
                after = "working directory"
            elif isinstance(commits[0], pygit2.Commit) and isinstance(commits[1], pygit2.Commit):
                diff = self.repo.diff(a=commits[0],b=commits[1])
                before = "commit " + commits[0].hex[:7]
                after = "commit " + commits[1].hex[:7]
            else:
                raise ValueError("arguments to git diff must represent commits / staging area")

            patches = [p for p in diff]
            self.fullDiff = ""
            for patch in patches:
                self.fullDiff += self.formatPatch(patch, before, after)

            print(self.fullDiff)
            return

        except ValueError:
            self.fullDiff = None
            return """
Git Crystals Can Only Diff Two Commit Objects, or One Commit
Object and the working directory / or staging area. Refer to
the Refer them
via SHA, abbreviated SHA (at least 5 characters), branch,
tag name, or via HEAD, HEAD~1, HEAD^ style notation"""

    def do_show(self,arg):
        print(repr(arg.split()))

if __name__ == '__main__':
   print("Git Command Line")
   game = GitCmd('mock-data')
   game.cmdloop()
