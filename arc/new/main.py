#!/usr/bin/env python
import argparse

from utils import Utils


class Archiver:
    def __init__(self):
        self.utils = Utils()

    def run(self, args):
        self.utils.main_loop(args.folder, args.yes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("folder", help="Folder to archive")

    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        default=False,
        help="Assume yes to all questions",
    )

    app = Archiver()
    app.run(parser.parse_args())
