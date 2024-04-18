#!/usr/bin/env python3
import os
import sys
import argparse
from utils import Utils


class Porngames:
    def __init__(self):
        self.utils = Utils()

    def run(self, args):
        if args.onlyarchives:
            folder = "archives"
        elif args.onlychecked:
            folder = "checked"
        elif args.onlyusb:
            folder = "usb"
        elif args.onlykeep:
            folder = "keep"
        else:
            folder = "all"
    
        if args.onlyzips:
            atype = 'zip'
        elif args.onlytar:
            atype = 'tar.gz'
        else:
            atype= 'all'

        match args.destination:
            case "playing":
                destpath = os.path.expanduser(os.path.join("~", "Games", "playing"))
            case "todo":
                destpath = os.path.expanduser(os.path.join("~", "Games", "todo"))
            case _:
                self.utils.myprint(" %r»%R That is not a valid destination")
                sys.exit()

        while True:
            game = self.utils.fuzzy_finder(folder=folder, atype=atype)
            if len(game) == 0:
                break
            else:
                self.utils.unpack(game[0], destpath, keep=args.keep)

        self.utils.render_header()
        self.utils.myprint(" %g∙%R Have fun playing!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--destination',
                        required=False,
                        default='playing',
                        help='Where to unpack')

    parser.add_argument('-k', '--keep',
                        action='store_true',
                        required=False,
                        default=False,
                        help="Don't remove the archive")

    parser.add_argument('-oa', '--onlyarchives',
                        action='store_true',
                        required=False,
                        default=False,
                        help='Show only archives')

    parser.add_argument('-oc', '--onlychecked',
                        action='store_true',
                        required=False,
                        default=False,
                        help='Show only checked')
    
    parser.add_argument('-ou', '--onlyusb',
                        action='store_true',
                        required=False,
                        default=False,
                        help='Show only usb')
    
    parser.add_argument('-ok', '--onlykeep',
                        action='store_true',
                        required=False,
                        default=False,
                        help='Show only keep')

    parser.add_argument('-oz', '--onlyzips',
                        action='store_true',
                        required=False,
                        default=False,
                        help='Show only zip files')

    parser.add_argument('-ot', '--onlytar',
                        action='store_true',
                        required=False,
                        default=False,
                        help='Show only tar balls')
    
    app = Porngames()
    app.run(parser.parse_args())
