import os
import shutil

from colors import Colors


class Core:
    def __init__(self):
        self.colors = Colors.colors
        self.renpy_folder = os.path.expanduser(os.path.join('~', '.renpy'))
        self.exec_folder = os.path.expanduser(os.path.join('~', 'Downloads', 'Renpy'))
        self.mygames_folder = os.path.expanduser(os.path.join('~', 'Dev', 'renpy', 'my_games'))


    # ------------------------------------------------------------------------
    # --------------------------------------------------------------- FILE I/O
    # ------------------------------------------------------------------------
    def collect_files(self, folder):
        files = []
        for item in os.listdir(folder):
            files.append(item)
        return files
    
    def clear_save_files(self):
        skip = ['launcher-4', 'tokens']
        self.tprint('Clearing save files  ', '')
        files = self.collect_files(self.renpy_folder)
        counter = 0
        for file in files:
            if file in skip:
                continue
            counter += 1
            path = os.path.join(self.renpy_folder, file)
            shutil.rmtree(path)
        self.clearlines()
        action = 'Done' if counter else 'Not Needed'
        self.tprint('Clearing save files  ', action)

    def clear_cache_files(self):
        self.tprint('Clearing cache files ', '')
        versions = self.collect_files(self.exec_folder)
        counter = 0
        for version in versions:
            path = os.path.join(self.exec_folder, version)
            folders = self.collect_files(os.path.join(path))
            for folder in folders:
                if folder == 'tmp' or 'dists' in folder:
                    full_path = os.path.join(path, folder)
                    shutil.rmtree(full_path)
                    counter += 1
        self.clearlines()
        action = 'Done' if counter else 'Not Needed'
        self.tprint('Clearing cache files ', action)

    def clear_dist_files(self):
        self.tprint('Clearing dev files   ', '')
        counter = 0

        folders = self.collect_files(self.mygames_folder)
        for folder in folders:
            if not 'dists' in folder:
                continue
            path = os.path.join(self.mygames_folder, folder)
            shutil.rmtree(path)
            counter += 1

        self.clearlines()
        action = 'Done' if counter else 'Not Needed'
        self.tprint('Clearing dev files   ', action)

    # ------------------------------------------------------------------------
    # -------------------------------------------------------------- TUI Stuff
    # ------------------------------------------------------------------------
    def colorize(self, string, remove=False):
        for color in self.colors:
            repl = '' if remove else color[1]
            string = string.replace(color[0], repl)
        return string

    def mprint(self, string, nl=False):
        end = '\n\n' if nl else '\n'
        print(self.colorize(string), end=end)

    def tprint(self, key, value, nl=False, template='- %(key)s: %(value)s'):
        args = {'key': key, 'value': value}
        text = template % args
        self.mprint(text, nl=nl)

    def clearlines(self, nr=1):
        for _ in range(nr):
            print('\033[1A', end='\x1b[2K')
