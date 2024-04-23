#!/usr/bin/env python
import argparse
from girltubecore import GirlTubeCore


class GirlTube(GirlTubeCore):
    def __init__(self):
        super().__init__()

    def run(self, args):
        self.preflight_check()
        self.start_oldest = not args.latest
        self.continue_last = args.continuelast

        if args.add:
            self.add_youtube_url_to_db()

        self.channel_switcher()


if __name__ == "__main__":
    app=GirlTube()

    parser = argparse.ArgumentParser(prog='girltube')

    parser.add_argument('-a', '--add',
                        action='store_true',
                        required=False,
                        help='add stuff')

    parser.add_argument('-l', '--latest',
                        action='store_true',
                        required=False,
                        help='start with the latest first')
 
    parser.add_argument('-c', '--continuelast',
                        action='store_true',
                        required=False,
                        help='continue last watched')

    app.run(parser.parse_args())
