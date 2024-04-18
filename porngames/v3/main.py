#!/usr/bin/env python
import os
import sys
import argparse

from utils import Utils
from settings import *
from pyfzf.pyfzf import FzfPrompt


class Porngames:
    def __init__(self):
        self.utils = Utils()
        self.fzf = FzfPrompt()

    def select_game(self):
        games = self.utils.collect_games()
        game = self.fzf.prompt(games, '--reverse')
        if not game:
            self.utils.header()
            print("You did not select anything...")
            sys.exit()
        return game

    def remove(self):
        game = self.select_game()
        self.utils.remove(game[0])

    def install(self, keep=True):
        game = self.select_game()
        self.utils.unzip(game[0], keep=keep)

    def run(self, args):
        try:
            if args.install:
                self.install(keep=not args.delete)
            elif args.remove:
                self.remove()
            else:
                self.install(keep=not args.delete)


        except KeyboardInterrupt:
            self.utils.header()
            print("Process interrupted!")
            sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--install',
                        action = 'store_true',
                        help='Install a game')

    parser.add_argument('-d', '--delete',
                        action = 'store_true',
                        help='Delete archive after install')

    parser.add_argument('-r', '--remove',
                        action = 'store_true',
                        help='Remove an archive')

    app = Porngames()
    app.run(parser.parse_args())
