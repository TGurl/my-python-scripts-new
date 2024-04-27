#!/usr/bin/env python
import os
import sys
import readchar
import random

from time import sleep
from googletrans import Translator


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


class WriterCore():
    def __init__(self):
        super().__init__()
        self.twidth = os.get_terminal_size().columns
        self.localpath = os.path.expanduser(
                os.path.join('~', '.local', 'share', 'transgirl'))

    def colorize(self, string, remove_colors=False):
        for color in Colors.colors:
            r = '' if remove_colors else color[1]
            string = string.replace(color[0], r)
        return string

    def printr(self, string, center=False, newline=False, cols=75):
        nl = '\n\n' if newline else '\n'
        sp = ''
        if cols == 0:
            cols = self.twidth
        if center:
            temp = self.colorize(string, remove_colors=True)
            sp = ((cols - len(temp)) // 2) * ' '
            del temp
        string = self.colorize(string)
        print(f"{sp}{string}", end=nl)

    def draw_line(self, cols=22, char='─', col='%c'):
        line = cols * char
        self.printr(f"{col}{line}%R")

    # def error_msg(self, string, dot='·', ttw=2):
    def error_msg(self, string, ttw=1):
        self.printr(f"%r{string}%R")
        sleep(ttw)

    def header(self, title='Writr', cols=22):
        os.system('clear')
        self.draw_line()
        self.printr(f'%y{title}%R', center=True, cols=cols)
        self.draw_line()

    def check_keypress(self, allowed=[]):
        key = readchar.readchar().lower()
        if key not in allowed:
            self.error_msg('Wrong key!')
        else:
            return key

    def graceful_exit(self, show=False):
        if show:
            self.header()
            self.printr('Was it a good story?')
        else:
            os.system('clear')
        sys.exit()

    def wait_for_enter(self):
        _ = input(self.colorize('%b>> %yENTER %b<<%R'))

    def google_translate(self):
        translator = Translator()
        self.header('Translate')
        self.printr('%b>%g>%y>%w Translate what?')
        prompt = self.colorize("%b>%R ")
        word = input(prompt).lower()
        if word:
            english = translator.translate(word, src='nl', dest='en_US')
            prompt = self.colorize("%g>%R ")
            self.printr(f"{prompt}{english.text}", newline=True)
            self.wait_for_enter()

    def choose_name(self, girls=True):
        filename = 'girlnames.lst' if girls else 'boynames.lst'
        title = 'Girl names' if girls else 'Boy names'
        self.header(title=title)

        path = os.path.join(self.localpath, filename)
        alist = [line.rstrip() for line in open(path, 'r')]
        name = random.choice(alist)
        self.printr(f"%b>%g>%y>%w {name} %y<%g<%b<%R", newline=True)
        self.wait_for_enter()

    def add_a_name(self, what='girl'):
        prompt = self.colorize("%r>%y>%g>%R ")
        title = f'Add a {what} name'
        file = 'girlnames.lst' if what == 'girl' else 'boynames.lst'
        path = os.path.join(self.localpath, file)
        data = [line.strip() for line in open(path)]

        self.header(title=title)
        name = input(prompt).lower()
        if not name:
            return

        found = False
        for cname in data:
            if name == cname.lower():
                found = True
                break

        if found:
            self.printr("%rKnown already%R")
            sleep(1.5)
        else:
            with open(path, 'a', encoding='utf-8') as f:
                f.write(name.title() + '\n')
            self.printr(f"%gName {name.title()} added%R")
            sleep(1.5)

    def add_name_menu(self):
        while True:
            self.header(title='Add a name')
            allowed = ['r']
            nl = False
            items = ['Add girlname', 'Add boyname', 'Return']
            for idx, item in enumerate(items, start=1):
                col = '%r' if item == 'Return' else '%g'
                if idx == len(items) - 1:
                    nl = True

                if idx == len(items):
                    keystr = 'r'
                else:
                    keystr = str(idx)
                    allowed.append(str(idx))
                self.printr(f"[{col}{keystr}%R] {item}", newline=nl)
            prompt = self.colorize("%r>%y>%g>%R ")
            print(prompt, end='', flush=True)
            key = self.check_keypress(allowed=allowed)
            print('')

            if key == 'r':
                break
            elif key == '1':
                self.add_a_name(what='girl')
            elif key == '2':
                self.add_a_name(what='boy')

    def main_menu(self):
        while True:
            self.header()
            allowed = ['q']
            nl = False
            items = ['Girl name', 'Boy name', 'Translate', 'Add a name', 'Quit']
            for idx, item in enumerate(items, start=1):
                col = '%r' if item == 'Quit' else '%g'
                if idx == len(items) - 1:
                    nl = True

                if idx == len(items):
                    keystr = 'q'
                else:
                    keystr = str(idx)
                    allowed.append(str(idx))
                self.printr(f"[{col}{keystr}%R] {item}", newline=nl)
            prompt = self.colorize("%r>%y>%g>%R ")
            print(prompt, end='', flush=True)
            key = self.check_keypress(allowed=allowed)
            print('')

            if key == 'q':
                break
            elif key == '1':
                self.choose_name(girls=True)
            elif key == '2':
                self.choose_name(girls=False)
            elif key == '3':
                self.google_translate()
            elif key == '4':
                self.add_name_menu()


class Writer(WriterCore):
    def __init__(self):
        super().__init__()

    def run(self):
        self.main_menu()
        self.graceful_exit()


if __name__ == "__main__":
    app=Writer()
    app.run()
