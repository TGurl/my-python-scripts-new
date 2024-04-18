import os
import sys
import glob
import tarfile

from colors import Colors
from unzip import UnZip
from pyfzf.pyfzf import FzfPrompt


class Utils:
    def __init__(self):
        pass

    def __colorize(self, text="") -> str | None:
        if text == "":
            return None

        for color in Colors.colors:
            text = text.replace(color[0], color[1])
        return text

    def myprint(self, text, clear=False, nl=False):
        newline = "\n\n" if nl else "\n"
        text = self.__colorize(text)
        if clear:
            print("\033[1A", end="\x1b[2K")

        print(text, end=newline)

    def __collect_games_new(
        self, onlyzip=False, onlytars=False, oa=False, osf=False, ok=False, oc=False
    ):
        archives_folder = os.path.join("/", "data", "downloads", "SexGames")
        sexgames_folder = os.path.join("/", "backups", "sexgames")
        checked_folder = os.path.join(sexgames_folder, "checked")
        keep_folder = os.path.join(sexgames_folder, "keep")

        if oa:
            folders = [archives_folder]
        elif osf:
            folders = [sexgames_folder]
        elif ok:
            folders = [keep_folder]
        elif oc:
            folders = [checked_folder]
        else:
            folders = [archives_folder, sexgames_folder, keep_folder, checked_folder]

        if onlyzip:
            extensions = ["*.zip"]
        elif onlytars:
            extensions = ["*.tar.gz", "*.tar.bz2", "*.tar.xz"]
        else:
            extensions = ["*.zip", "*.tar.gz", "*.tar.bz2", "*.tar.xz"]

        games = []
        for folder in folders:
            for extension in extensions:
                folder = os.path.expanduser(folder)
                content = glob.glob(os.path.join(folder, extension))
                games.extend(content)

        games.sort()
        return games

    def select_game(
        self, onlyzip=False, onlytars=False, oa=False, osf=False, ok=False, oc=False, exact=False
    ) -> str | None:
        games = self.__collect_games_new(
            onlyzip=onlyzip, onlytars=onlytars, oa=oa, osf=osf, ok=ok, oc=oc
        )
        fzf = FzfPrompt()
        options = "--reverse --exact" if exact else "--reverse"
        game = fzf.prompt(games, options)
        if len(game) > 0:
            return game[0]
        else:
            return None

    def render_title(self):
        """render the title"""
        os.system('clear')
        lines = ['  %c┌──────────────────┐',
                 '  │%y┏┓      ┏┓        %c│ ',
                 '  │%y┃┃┏┓┏┓┏┓┃┓┏┓┏┳┓┏┓┏%c│',
                 '  │%y┣┛┗┛┛ ┛┗┗┛┗┻┛┗┗┗ ┛%c│',
                 '  └──────────────────┘%R',
                 '%cCopyright 2023 %pTransGirl%R']

        for line in lines:
            self.myprint(line)
        print()

    def render_header(self, game, target, prompt):
        self.render_title()
        gamename = game.replace('/home/geertje', '~')
        targetname = target.replace('/home/geertje', '~')
        # self.myprint("%yPorngame Collection%R - %cCopyleft 2023 %pTransGirl%R", nl=True)
        self.myprint(f"Extracting %i%c{gamename}%R to %i%c{targetname}%R")
        self.myprint(prompt, clear=False)

    def unzip(self, game, target):
        with UnZip(game) as archive:
            INFO = archive.namelist()
            TOTAL = len(INFO)
            LEAD = len(str(TOTAL))
            count = 1
            perc = 0
            name = ""

            prompt = f" %b└>%R {count:{LEAD}}/{TOTAL} [{perc:3}%] : {name}"
            self.render_header(game, target, prompt)

            for file in INFO:
                perc = count * 100 // TOTAL
                name = file if len(file) < 35 else "%c<<%R" + file[-35:]
                prompt = f" %b└>%R {count:{LEAD}}/{TOTAL} [{perc:3}%] : {name}"
                self.myprint(prompt, clear=True)
                archive.extract(file, target)
                count += 1

    def untar(self, game, target, atype):
        self.render_header(game, target, " └> Reading archive...")
        archive = tarfile.open(game, atype)
        files = archive.getnames()
        TOTAL = len(files)
        LEAD = len(str(TOTAL))
        perc = 0
        count = 1

        for file in files:
            perc = int(count * 100 / TOTAL)
            name = file if len(file) < 35 else ".." + file[-35:]
            prompt = f" └> {count:{LEAD}}/{TOTAL} [{perc:3}%] : {name}"
            self.myprint(prompt, clear=True)
            archive.extract(file, target, set_attrs=True)
            count += 1

        archive.close()

    def install_game(self, game, target, keep=False):
        target = os.path.expanduser(target)

        if ".zip" in game:
            self.unzip(game, target)
        elif ".tar.gz" in game:
            self.untar(game, target, "r:gz")
        elif ".tar.bz2" in game:
            self.untar(game, target, "r:bz2")
        elif ".tar.xz" in game:
            self.untar(game, target, "r:xz")
        else:
            self.render_title()
            self.myprint("%rUnkown archive type detected!%R")
            self.myprint("Exiting...")
            sys.exit()

        if not keep:
            os.remove(game)

        self.render_title()
        self.myprint("Done. Have fun playing...")
