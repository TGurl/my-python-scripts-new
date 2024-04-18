#!/usr/bin/env python
import sys
import os
import argparse
from utils import Utils


class PornGames(Utils):
    def __init__(self):
        super().__init__()

    def run(self, args):
        onlyzip = args.onlyzip
        onlytars = args.onlytars
        running = True

        onlyarchives = args.onlyarchives
        onlysexgames = args.onlysexgames
        onlykeep = args.onlykeep
        onlychecked = args.onlychecked
        exact = not args.exact

        while running:
            target = "TransGirlNeedsABigBlackCockInHerAss"
            match args.destination:
                case "todo":
                    target = os.path.join("~", "Games", "todo")
                case "playing":
                    target = os.path.join("~", "Games", "playing")
                case _:
                    self.myprint("%r!%R Unknown destination chosen")
                    sys.exit()

            try:
                game = self.select_game(
                    onlyzip=onlyzip,
                    onlytars=onlytars,
                    oa=onlyarchives,
                    osf=onlysexgames,
                    ok=onlykeep,
                    oc=onlychecked,
                    exact=exact
                )
            except KeyboardInterrupt:
                game = None

            if game is not None:
                try:
                    self.install_game(game, target, keep=args.keep)
                except KeyboardInterrupt:
                    running = False
            else:
                running = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d",
        "--destination",
        required=False,
        default="playing",
        help="Target destination for the game (playing)",
    )

    parser.add_argument(
        "-k",
        "--keep",
        action="store_true",
        required=False,
        default=False,
        help="Do not delete the archive",
    )

    parser.add_argument(
        "-e",
        "--exact",
        action="store_true",
        required=False,
        default=False,
        help="Do an exact search",
    )

    parser.add_argument(
        "-oz",
        "--onlyzip",
        action="store_true",
        required=False,
        default=False,
        help="show only zipfiles",
    )

    parser.add_argument(
        "-ot",
        "--onlytars",
        action="store_true",
        required=False,
        default=False,
        help="show only tarfiles",
    )

    parser.add_argument(
        "-oa",
        "--onlyarchives",
        action="store_true",
        required=False,
        default=False,
        help="show only archives",
    )

    parser.add_argument(
        "-os",
        "--onlysexgames",
        action="store_true",
        required=False,
        default=False,
        help="show only sexgames",
    )

    parser.add_argument(
        "-ok",
        "--onlykeep",
        action="store_true",
        required=False,
        default=False,
        help="show only keep",
    )

    parser.add_argument(
        "-oc",
        "--onlychecked",
        action="store_true",
        required=False,
        default=False,
        help="show only checked",
    )

    app = PornGames()
    app.run(parser.parse_args())
