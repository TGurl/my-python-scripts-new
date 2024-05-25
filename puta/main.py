#!/usr/bin/env python
import argparse

from putacore import PutaCore


class Puta(PutaCore):
    def __init__(self):
        super().__init__()

    def run(self, args):
        self.draw_title_box()
        if args.add:
            self.add_a_game(args.add)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--add',
                        type=str,
                        metavar='X',
                        required=False,
                        help='Add a game')

    app=Puta()
    app.run(parser.parse_args())
