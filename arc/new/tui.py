#!/usr/bin/env python
import os
import sys

from colors import Colors


class TUI:
    def __init__(self):
        pass

    def clearscreen(self):
        os.system("clear")

    def clearlines(self, num=1):
        for _ in range(num):
            print("\033[1A", end="\x1b[2K")

    def colorize(self, text):
        for color in Colors.colors:
            text = text.replace(color[0], color[1])
        return text

    def decolorize(self, text):
        for color in Colors.colors:
            text = text.replace(color[0], "")
        return text

    def myprint(self, text, new_line=False):
        carriage_return = "\n\n" if new_line else "\n"
        text = self.colorize(text)
        print(text, end=carriage_return)

    def banner(self, width=40, clear=True):
        if clear:
            self.clearscreen()

        title = "%yARC 6.0%R - %gCopyright 2023 Transgirl%R"
        line = width * "─"
        spaces = (width - len(self.decolorize(title))) // 2 * " "
        topline = f"%c╭{line}╮%R"
        botline = f"%c╰{line}╯%R"
        midline = f"%c│%R{spaces}{title}{spaces}%c│%R"

        self.myprint(topline)
        self.myprint(midline)
        self.myprint(botline)

    def info_msg(self, text):
        prompt = f" [%b-%R] {text}"
        self.myprint(prompt)

    def ok_msg(self, text):
        prompt = f" [%g✔%R] {text}"
        self.myprint(prompt)

    def err_msg(self, text, exit_app=False):
        prompt = f" [%r✗%R] {text}"
        self.myprint(prompt)
        if exit_app:
            sys.exit()
