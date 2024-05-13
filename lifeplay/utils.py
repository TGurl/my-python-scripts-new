import os

from colors import Colors


class Utils:
    def __init__(self):
        self.gamewidth = os.get_terminal_size().columns

    def colorize(self, text, decolorize=False):
        for color in Colors.colors:
            rep = '' if decolorize else color[1]
            text = text.replace(color[0], rep)
        return text

    def printr(self, text, center=False, new_line=False):
        spaces = ''
        if center:
            temp = self.colorize(text, decolorize=True)
            spaces = ((self.gamewidth - len(temp)) // 2) * ' '
        nl = '\n\n' if new_line else '\n'
        text = self.colorize(text)
        print(f"{spaces}{text}", end=nl)

    def draw_line(self, width=0, color='%c'):
        width = self.gamewidth if not width else width
        line = width * '-'
        self.printr(f"{color}{line}%R")
