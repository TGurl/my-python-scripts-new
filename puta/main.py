#!/usr/bin/env python
import argparse
from putacore import PutaCore


class Puta(PutaCore):
    def __init__(self):
        super().__init__()

    def run(self, args):
        self.always_yes = args.yes
        self.store_to_usb = args.usb

        while True:
            if args.add:
                self.add_a_game(args.add)
            elif args.delete:
                self.delete_a_game()
            else:
                self.install_game()
            self.graceful_exit()


if __name__ == "__main__":
    app=Puta()
    parser = argparse.ArgumentParser()

    egroup = parser.add_mutually_exclusive_group(required=False)

    egroup.add_argument('-a', '--add',
                        type=str,
                        metavar='x',
                        help='add a game')

    egroup.add_argument('-d', '--delete',
                        action='store_true',
                        help='delete a game')

    parser.add_argument('-u', '--usb',
                        action='store_true',
                        required=False,
                        help='move to USB after zipping')
    
    parser.add_argument('-r', '--remove',
                        action='store_true',
                        required=False,
                        help='remove archive after install')
    
    parser.add_argument('-y', '--yes',
                        action='store_true',
                        required=False,
                        help='presume yes')

    app.run(parser.parse_args())
