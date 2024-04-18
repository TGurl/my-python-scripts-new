import os
import random
import tarfile
import glob

from colors import Colors
from pyfzf.pyfzf import FzfPrompt
from zipfile import ZipFile


class Utils:
    def __init__(self):
        self.fzf = FzfPrompt()
        self.color = self.select_color()

    # ---------------------------------------
    # -- Collect the games
    # ---------------------------------------
    def collect_games(self, folder='all', atype='all'):
        show_all = False
        if atype == 'zip':
            pattern = ["*.zip"]
        elif atype == 'tar.gz':
            pattern = ["*.tar.gz"]
        else:
            pattern = ["*.zip", "*.tar.gz"]

        path = ""
        paths = [
            os.path.join("~", "Games", "archives"),
            os.path.join("~", "Games", "archives", "checked"),
            os.path.join("~", "USB", "sexgames"),
            os.path.join("~", "USB", "sexgames", "keep")
        ]

        match folder:
            case 'archives':
                path = paths[0]
            case 'checked':
                path = paths[1]
            case 'usb':
                path = paths[2]
            case 'keep':
                path = paths[3]
            case _:
                show_all = True

        games = []
        if not show_all:
            games = []
            for suffix in pattern:
                fullpath = os.path.join(path, suffix)
                games.extend(glob.glob(os.path.expanduser(fullpath)))
        else:
            games = []
            for path in paths:
                for suffix in pattern:
                    fullpath = os.path.join(path, suffix)
                    games.extend(glob.glob(os.path.expanduser(fullpath)))

        games.sort()
        return games

    # ---------------------------------------
    # -- Fuzzy finder
    # ---------------------------------------
    def fuzzy_finder(self, folder="all", atype="all"):
        games = self.collect_games(folder, atype)
        game = self.fzf.prompt(games, '--reverse')
        return game

    # ---------------------------------------
    # -- Unpack archive to destination
    # ---------------------------------------
    def unpack(self, game, destpath, keep=False):
        if ".zip" in game:
            self.unzip(game, destpath, keep=keep)
        else:
            self.untar(game, destpath, keep=keep)

    def unzip(self, game, destpath, keep=False):
        self.render_header()
        game_title = game.split('/')[-1]
        self.myprint(f" {self.color}∙%R Extracting {game_title}...")

        with ZipFile(game, 'r') as zf:
            filelist = zf.infolist()
            total = len(filelist)
            digits = len(str(total))

            for num, item in enumerate(filelist, start=1):
                percent = int(num * 100 / total)
                name = item.filename
                if len(name) > 40:
                    name = ".." + name[-38:]

                self.myprint(f"   {self.color}└>%R {num:{digits}}/{total} [{percent:3}%]: {name}")
                extracted_path = zf.extract(item, destpath)
                if item.create_system == 3:
                    unix_attributes = item.external_attr >> 16
                    if unix_attributes:
                        os.chmod(extracted_path, unix_attributes)
                self.clearline()
        
        if not keep:
            os.remove(game)

    def untar(self, game, destpath, keep=False):
        self.render_header()
        game_title = game.split('/')[-1]

        # -- unpack the archive
        with tarfile.open(game) as tar:
            self.myprint(f" {self.color}∙%R Reading {game_title}...")
            total = len(tar.getnames())
            digits = len(str(total))
            self.clearline()
            self.myprint(f" {self.color}∙%R Extracting {game_title}...")
            for num, member in enumerate(tar.getmembers(), start=1):
                percent = (num * 100) // total
                name = member.name
                if len(name) > 40:
                    name = ".." + name[-38:]
                self.myprint(f"   {self.color}└>%R {num:{digits}}/{total} [{percent:3}%]: {name}")
                tar.extract(member, path=destpath)
                self.clearline()

        if not keep:
            os.remove(game)

    # ---------------------------------------
    # -- TUI functions
    # ---------------------------------------
    def clearline(self):
        print('\033[1A', end='\x1b[2K')

    def colorize(self, text) -> str:
        for color in Colors.colors:
            text = text.replace(color[0], color[1])
        return text

    def myprint(self, text, nl=False, clear=False) -> None:
        newline = '\n\n' if nl else '\n'

        if clear:
            os.system('clear')

        text = self.colorize(text)
        print(text, end=newline)

    def get_input(self, text="", nl=False):
        if text != "":
            text = f"{text} "
        prompt = self.colorize(f"{text}{self.color}»%R ")
        if nl:
            print()
        response = input(prompt).lower()
        return response

    def select_color(self):
        colors = ["%y", "%c", "%g", "%b", "%w"]
        col = random.choice(colors)
        return col

    def render_header(self, clear=True):
        if clear:
            os.system('clear')

        self.color = self.select_color()
        tc = ""
        while tc == self.color:
            tc = self.select_color()

        lines = [
            f"{self.color}╭───────────────────────────╮",
            f"│    {tc}Porngame Collection    {self.color}│",
            f"│ %RCopyright 2023, Transgirl {self.color}│",
            "╰───────────────────────────╯%R"
        ]

        for line in lines:
            self.myprint(line)
