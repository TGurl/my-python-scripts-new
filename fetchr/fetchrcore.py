import os

from utils import TransgirlUtils


class fetchrCore(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.transgender = False
        self.maxwidth = 40

    def print(self, string:str, cr=False):
        end = '\n\n' if cr else '\n'
        string = self.colorize(string)
        print(string, end=end)

    def render_transflag(self):
        line = self.maxwidth * '█'

        def render_blue():  
            self.print(f"%c{line}%R")

        def render_purple():
            self.print(f"%p{line}%R")
    
        def render_white():
            self.print(f"%w{line}%R")

        render_blue()
        render_blue()
        render_purple()
        render_purple()
        render_white()
        render_white()
        render_purple()
        render_purple()
        render_blue()
        render_blue()
