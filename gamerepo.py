#!/usr/bin/env python3
import cmd,os,re
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
        if 'user.name' not in self.repo.config:
            self.repo.config['user.name'] = "Adventurer"
        if 'user.email' not in self.repo.config:
            self.repo.config['user.email'] = "adventurer@gitcrystals.com"

    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    def createSignature(self):
            return pygit2.Signature(self.repo.config['user.name'], self.repo.config['user.email'])

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

    def fileIsValid(self,fileName):
        invalid = os.pardir # strings with parent directories considered invalid
        if isinstance(fileName,str):
            if fileName.find(invalid) is not -1:
                return False
            else:
                try:
                    x = os.stat(fileName)   # Test File Exists
                except FileNotFoundError:
                    return False
            return True

    def checkCanCommit(self):
        entries = []
        status = self.repo.status()
        for fileName in status.keys():
            entries.append(self.statusParse(fileName, status[fileName]))

        for entry in entries:
            if entry['status'].__contains__('Staged File Deletion') or entry['status'].__contains__('Staged File Changes') or entry['status'].__contains__('Staged New File'):
                return True
            else:
                return False

    def getCommitMessage(self):
        print("Enter One Line Summary of Commit. Blank entry or 'quit' aborts the commit")
        self.commitHeader = input()
        if self.commitHeader == "quit" or self.commitHeader == "":
            print("Type ",S_CYA,"commit",S_WHI,"to commit again\n",
                        S_CYA,"status ",S_WHI,"to see what you've staged\n",
                        S_CYA,"diff ",S_WHI,"to changes since your last commit\n",
                        S_CYA,"stage or unstage ",S_WHI,"to stage or unstage file changes\n",)
            return False
        print("Enter more commit info if desired or quit to abort the commit")
        self.commitBody = input()
        if self.commitBody == "quit":
            print("Type ",S_CYA,"commit",S_WHI,"to commit again\n",
                        S_CYA,"status ",S_WHI,"to see what you've staged\n",
                        S_CYA,"diff ",S_WHI,"to changes since your last commit\n",
                        S_CYA,"stage or unstage ",S_WHI,"to stage or unstage file changes\n",)
            return False
        if self.commitBody != "":
            self.commitMessage = self.commitHeader + '\n\n' + self.commitBody
        else:
            self.commitMessage = self.commitHeader

        return self.commitMessage

    def printPostCommitInfo(self,head,commit):
        message = '\n'
        message += "New Commit " + S_CYA + commit.hex[:8] + S_WHI + " Added to repo\n"
        message +="Branch " + S_CYA + head.name[11:] + S_WHI + " Updated"
        return message

    def do_quit(self, arg):
        """Quit the game."""
        return True # this exits the Cmd application loop in TextAdventureCmd.cmdloop()

    def do_setname(self, arg):
        """ Set the commit author's name """
        self.repo.config['user.name'] = arg
        print("Your name is set to " + arg + '\n')

    def do_setemail(self, arg):
        """ Set the commit author's email """
        match = re.fullmatch('[A-Za-z0-9_-]+@[A-Za-z0-9_-]+\.[a-z.]{2,9}', arg)
        if match is not None:
            self.repo.config['user.email'] = arg
            print(self.repo.config['user.email'] + " is set to " + arg)
        else:
            print("Please input a valid email address such as example@gitcrystals.com")

    def do_stage(self, arg):
        self.stageMessage = ""
        args = arg.split()
        if len(args) == 0:
            self.stageMessage += """Type the file name you wish to stage:
stage <file name>
Type status to see a list of changed files
Type ls to see a list of all game files
"""

        if len(args) > 0:
            for fileName in args:
                absFilePath = os.path.join(self.repo.workdir, fileName)
                if self.fileIsValid(absFilePath):
                   self.repo.index.add(fileName)
                   self.repo.index.write()
                   self.stageMessage += S_ORA + fileName + "added to staging area " + S_WHI + '\n'
                else:
                   self.stageMessage += S_RED + fileName + 'is not in the repository' + S_WHI + '\n'
            self.stageMessage += S_WHI + "Type " + S_CYA + "status" + S_WHI + "to inspect staging area" + '\n'
            self.stageMessage += S_WHI + "Type " + S_CYA + "diff staged" + S_WHI + "to inspect staged changes" + '\n'
            self.stageMessage += S_WHI + "Type " + S_CYA + "commit" + S_WHI + "to commit changes" + '\n'

        print(self.stageMessage)

    def do_unstage(self, arg):
        self.unstageMessage = "All changes removed from staging area\n"
        self.unstageMessage += "Type" + S_CYA + "stage <file name> " + S_WHI + "\n"
        self.unstageMessage += "to stage changes for commit.\n"

        HEAD = self.repo.revparse_single('HEAD').hex
        print(HEAD)
        self.repo.reset(HEAD, pygit2.GIT_RESET_MIXED)
        print(self.unstageMessage)

    def do_commit(self, arg):
        """ Command to Let User Commit Changes """

        if self.checkCanCommit() == False:
            self.message = """ You haven't staged any changes for commit
Type stage """ + S_CYA + """<filename>""" + S_WHI + """where filename is
the name of the file whose changes you wish to commit"""
            print(self.message)
            return

        if self.repoName == "mock-data" + os.sep + ".git" and arg =='test': # For Unit Tests
            message = "Test Commit Message"
        else:
            self.do_status('')
            message = self.getCommitMessage()
            if message == False:
                return


        signature = self.createSignature()
        tree = self.repo.TreeBuilder(self.repo.index.write_tree()).write() # Create commit's associated tree
        head = self.repo.head
        self.commit = self.repo.create_commit(head.name, signature, signature, message, tree, [head.target])
        print(self.printPostCommitInfo(head,self.commit))

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
