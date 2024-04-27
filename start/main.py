#!/usr/bin/env python
import os
import readchar
from time import sleep


# ----------------------------------------------------------------------------
# ------------------------------------------------------------ Class StartGame
# ----------------------------------------------------------------------------

class StartGame():
    def __init__(self):
        self.title = ""
        self.games = [{'title': '', 'path': ''},
                      {'title': '', 'path': ''}]
        self.run_all = False

    def colorize(self, string, remove_colors=False):
        for color in Colors.colors:
            repl = '' if remove_colors else color[1]
            string = string.replace(color[0], repl)
        return string

    def printr(self, string, new_line=False, center=False, width=30):
        sp = ''
        if center:
            temp = self.colorize(string, remove_colors=True)
            sp = ((width - len(temp)) // 2) * ' '
        nl = '\n\n' if new_line else '\n'
        string = self.colorize(string)
        print(f"{sp}{string}", end=nl)

    def drawline(self, width=30, new_line=False):
        line = width * '─'
        self.printr(f"%c{line}%R", new_line = new_line)

    def banner(self, gametitle = ''):
        title = f"%y{self.title}%R"
        if gametitle:
            title += f" - %g{gametitle}%R"
        os.system('clear')
        # -------------------------------------------------- now show them all
        self.drawline()
        self.printr(title, center=True)
        self.drawline(new_line=True)

    def get_key(self, allowed=[], prompt="%b>%g>%y>%R "):
        print(self.colorize(prompt), end='', flush=True)
        key = readchar.readkey().lower()
        if key not in allowed:
            print(self.colorize("%rThat's not a valid key..."),
                  end='',
                  flush=True)
            sleep(1.2)
        print('')
        return key

    def look_for_executables(self, path=''):
        execs = []
        for entry in os.scandir(path):
            _, ext = os.path.splitext(entry)
            if ext in ['.sh', '.exe'] and not '-32' in entry.name:
                execs.append(entry.path)
        return execs

    def run_game(self, path=''):
        execs = self.look_for_executables(path)
        wine = False
        for exec in execs:
            path = exec
            if '.sh' in exec:
                break
            else:
                wine = True
                break

        cmd = path
        if wine:
            cmd = f"wine {path}"

        os.system(cmd)

    def run_all_games(self):
        for idx, game in enumerate(self.games, start=1):
            self.banner(gametitle=game['title'])
            self.printr("%b>%g>%y>%R Starting game...")
            self.run_game(game['path'])
            if idx < len(self.games):
                self.printr("%b>%g>%y>%R Please wait...")
                sleep(1.5)

    def run(self):
        while True:
            self.banner()
            allowed = ['q']
            for idx, game in enumerate(self.games, start=1):
                nl = idx == len(self.games)
                allowed.append(str(idx))
                self.printr(f"(%g{idx}%R) {game['title']}", new_line=nl)
            if self.run_all:
                allowed.append('a')
                self.printr("(%ga%R) Run all")
            self.printr("(%rq%R) Quit", new_line=True)
            key = self.get_key(allowed=allowed)
            if key == 'q':
                break
            elif key == 'a':
                self.run_all_games()
            else:
                self.banner(gametitle=self.games[int(key) - 1]['title'])
                self.printr("%b>%g>%y>%R Starting game...")
                self.run_game(self.games[int(key) - 1]['path'])

# ----------------------------------------------------------------------------
# --------------------------------------------------------------- Class Colors
# ----------------------------------------------------------------------------
class Colors:
    reset = "\033[0m"
    black = "\033[30;1m"
    red = "\033[31;1m"
    green = "\033[32;1m"
    darkgreen = "\033[32m"
    yellow = "\033[33;1m"
    blue = "\033[34;1m"
    pink = "\033[35;1m"
    cyan = "\033[36;1m"
    white = "\033[37;1m"
    gray = "\033[37m"
    italic = "\x1B[3m"

    colors = [
            ('%R', reset),
            ('%B', black),
            ('%G', gray),
            ('%r', red),
            ('%g', green),
            ('%dg', darkgreen),
            ('%y', yellow),
            ('%b', blue),
            ('%p', pink),
            ('%c', cyan),
            ('%w', white),
            ('%i', italic)
    ]


if __name__ == "__main__":
    app=StartGame()
    app.run()
