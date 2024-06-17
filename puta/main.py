#!/usr/bin/env python
import sys
from core import Core, Config


class Puta(Core):
    def show_help(self, error=''):
        spc = 5 * ' '
        end = '\n\n' if error else '\n'
        self.banner()
        print(' Usage: puta [-a <folder>] [switches]', end='\n\n')
        print(' Switches:')
        print(f'{spc}-d{spc}delete archive after extraction')
        print(f'{spc}-u{spc}store archive to USB')
        print(f'{spc}-f{spc}finishe game, store in DONE')
        print(f'{spc}-l{spc}use lzma compression')
        print(f'{spc}-b{spc}use bzip2 compression')
        print(f"{spc}-h{spc}show this help screen", end=end)
        if error:
            print('ERROR:')
            print(f'{spc}{error}')
        sys.exit()

    def run(self, args):
        if '-h' in args:
            self.show_help()

        # -- set the default destination to /lore
        Config.destination = Config.lorefolder

        # -- check if -u and -f are issued
        if '-u' in args and '-f' in args:
            self.show_help(error='You cannot issue -u and -f at the same time.')

        # -- check if /usb is chosen
        if '-u' in args:
            Config.destination = Config.usbfolder
            args.remove('-u')

        # -- check if finished
        if '-f' in args:
            Config.destination = Config.donefolder
            args.remove('-f')

        # -- check compression level
        if '-l' in args and '-b' in args:
            self.show_help(error='You cannot issue -l and -b at the same time.')

        if '-l' in args:
            self.set_compression(level=1)
            args.remove('-l')
        elif '-b' in args:
            self.set_compression(level=2)
            args.remove('-b')
        else:
            self.set_compression(level=0)

        # -- check if delete is issued
        if '-d' in args:
            Config.delete = True
            args.remove('-d')

        # -- check if user wants to search for something
        if '-q' in args:
            index = args.index('-q')
            Config.query = args[index + 1]
            args.remove('-q')

        # -- check if user wants to add a game
        if '-a' in args:
            args.remove('-a')
            if not args:
                self.show_help(error='No folder to process...')

            self.create_archive(args[0])

        self.install_a_game()

if __name__ == '__main__':
    app = Puta()
    if len(sys.argv) < 1:
        app.show_help()
    app.run(sys.argv[1:])
