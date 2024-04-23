#!/usr/bin/env python
import sys
import argparse
from core import Core

def main(args):
    app = Core()
    app.read_config()

    if args.next:
        app.next_wallpaper()
        app.save_config()
        sys.exit()

    if args.previous:
        app.previous_wallpaper()
        app.save_config()
        sys.exit()

    if args.setup:
        app.interactive_setup()
        app.save_config()
        sys.exit()

    if args.info:
        app.show_info()
        sys.exit()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--next',
                        action='store_true',
                        required=False,
                        help='Go to next wallpaper')

    parser.add_argument('-p', '--previous',
                        action='store_true',
                        required=False,
                        help='Go to previous wallpaper')

    parser.add_argument('-i', '--info',
                        action='store_true',
                        required=False,
                        help='Show wallpaper info')

    parser.add_argument('-s', '--setup',
                        action='store_true',
                        required=False,
                        help='Interactive setup')

    main(parser.parse_args())
