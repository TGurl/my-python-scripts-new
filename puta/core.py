import os
import sys
import glob
import shutil
import time
import math

from config import Config
from progressbar import ProgressBar
from zipfile import ZipFile, ZIP_LZMA, ZIP_DEFLATED, ZIP_BZIP2, is_zipfile
from pyfzf.pyfzf import FzfPrompt


class Core:
    # ------------------------------------------------------------------------
    # -- Design notes:
    # --     + a basic interface, nothing fancty like colors etc.
    # --     + prefer sys.argv over argparse, and make it work :)
    # --     + clean up trash, ren'py save files, rpgm save files
    # --     + multiple locations: lore, usb, and finished!
    # --     + check all possible locations before zipping
    # --     - what ever else I can think off
    # ------------------------------------------------------------------------
    def __init__(self):
        self.empty = ' '
        self.symbol = '≡'

    # ------------------------------------------------------------------------
    # -- main functions
    # ------------------------------------------------------------------------
    def choose_a_game(self):
        repos = [Config.lorefolder, Config.usbfolder, Config.donefolder]
        games = []
        for repo in repos:
            for file in os.scandir(repo):
                q = Config.query.lower()
                if '.zip' in file.name.lower() and q in file.path.lower():
                    games.append(file.path)
        games.sort()
        chosen = FzfPrompt().prompt(games, '--exact --reverse --multi')
        if not chosen:
            self.banner()
            self.print("You really don't want to get fucked?")
            sys.exit()
        chosen.sort()
        return chosen
    
    def install_a_game(self):
        install = self.choose_a_game()
        total = len(install)

        for i, entry in enumerate(install, start=1):
            self.banner()
            filename = entry.split('/')[-1]
            foldername = filename.replace('.zip', '')
            self.tprint(f'Processing {i}/{total}', filename)
            if os.path.exists(os.path.join(Config.playfolder, foldername)):
                self.print(f'> {foldername} already exists, skipping...')
                time.sleep(1.5)
                continue
            
            if is_zipfile(entry):
                self.unzip(entry)
            else:
                self.print(f"> {entry} is not a zip archive!")
                while True:
                    ans = input("> Want me to remove her? (Y/n) : ").lower()
                    if ans in "yn" or ans=='':
                        remove = ans == 'y' or ans == ''
                        break
                    else:
                        self.print("That's not an answer to my question...")
                        time.sleep(1.5)
                        self.clearlines(num=2)
                if remove:
                    os.remove(entry)
                self.clearlines()

            if Config.delete:
                os.remove(entry)

        self.clearlines(num=2)
        self.print(f"> Finished procesing {total} games")
        self.print(f"> Happy fapping!")
        sys.exit()

    def clear_trash(self, folder:str):
        def find_trash(folder, pattern):
            path = os.path.join(folder, '**', pattern)
            items = glob.glob(path, recursive=True)
            return items

        self.wait_start('Cleaning up')
        
        # -- clearsave files
        trash = []
        patterns = ['**.save', '*.rpgsave']
        for pattern in patterns:
            entries = find_trash(folder, pattern)
            trash.extend(entries)

        # -- find other filth
        patterns = ['desktop.ini', 'log.txt', 'errors.txt', 'traceback.txt']
        for pattern in patterns:
            entries = find_trash(folder, pattern)
            trash.extend(entries)

        if trash:
            progress = ProgressBar(len(trash), width=Config.width,
                                   symbol=self.symbol, empty=self.empty,
                                   fmt=ProgressBar.PUTA_CLN)
            for i, item in enumerate(trash):
                progress.current = i
                os.remove(item)
                progress()
                time.sleep(0.2)
            progress.done()
            self.clearlines()
            self.tprint('Cleaning', 'Done')

    def create_archive(self, folder:str):
        self.banner()
        self.check_repos(folder)
        self.tprint('Packing up', folder)
        self.tprint('Destination', Config.destination)
        self.show_compression_level()
        self.clear_trash(folder)
        self.zipit(folder)
        self.show_size(folder)
        self.check_archive(folder)
        self.move_archive(folder)
        shutil.rmtree(folder)
        sys.exit()
    
    # ------------------------------------------------------------------------
    # -- TUI functions
    # ------------------------------------------------------------------------
    def print(self, string:str, cr=False):
        end = '\n\n' if cr else '\n'
        print(string, end=end)

    def tprint(self, string:str, value:str, width:int = Config.width):
        template = "> {:" + str(width) + "}: {}"
        self.print(template.format(string, value))

    def wait_start(self, string: str, output=sys.stderr):
        print('\r' + string, file=output, end='')

    def wait_done(self, string: str, output=sys.stderr):
        print(string, file=output)

    def error(self, string:str):
        self.print(f"PUTA ERROR: {string}")
        sys.exit()

    def clearlines(self, num:int = 1):
        for _ in range(num):
            print('\033[1A', end='\x1b[2K')

    def banner(self, cls=True, char='-', split=' · '):
        if cls:
            os.system('clear')
        s = 2 * ' '
        chars = ['┌', '┐', '└',  '┘', '─', '│']
        banner = f"{chars[5]}{s}{Config.title} {Config.version}{split}"
        banner += f"Transgirl Coding Studios{split}{Config.build}{s}{chars[5]}"
        line = (len(banner) - 2) * chars[4]
        
        self.print(chars[0] + line + chars[1])
        self.print(banner)
        self.print(chars[2] + line + chars[3], cr=False)

    def show_compression_level(self):
        prompt = ('Compression level')
        if Config.compress != 8:
            match(Config.compress):
                case 14:
                    self.tprint(prompt, 'LZMA')
                case 12:
                    self.tprint(prompt, 'Bzip2')
                case _:
                    self.error('Unkown compression level chosen')

    def show_size(self, folder:str):
        archive = folder.replace(' ', '_') + '.zip'
        size_bytes = os.stat(archive).st_size
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "K", "M", "G", "T", "P", "E", "Z", "Y")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        size = size_name[i]
        size += 'iB' if size != 'B' else ''
        self.tprint('Archive size', f"{s} {size}")

    # ------------------------------------------------------------------------
    # -- Check if archive is already in repos
    # ------------------------------------------------------------------------
    def check_repos(self, folder:str):
        archive = folder.replace(' ', '_') + '.zip'
        repos = [Config.lorefolder, Config.usbfolder, Config.donefolder]
        found = []

        for repo in repos:
            if os.path.exists(os.path.join(repo, archive)):
                found.append(repo)

        if found and Config.delete:
            for entry in found:
                os.remove(os.path.join(entry, archive))
        elif found and not Config.delete:
            pronounce = 'her' if len(found) == 1 else 'them'
            self.print(f"> Archive {archive} found in:")
            for entry in found:
                self.print(f"  - {entry}")
        
            print()
            print(f'You can use the -d switch to delete {pronounce} first.')
            sys.exit()

    # ------------------------------------------------------------------------
    # -- You gotta move it, move it...
    # ------------------------------------------------------------------------
    def move_archive(self, folder:str):
        copied = 0
        archive = folder.replace(' ', '_') + '.zip'
        source_size = os.stat(archive).st_size
        target_fn = os.path.join(Config.destination, archive)

        source = open(archive, 'rb')
        target = open(target_fn, 'wb')

        progress = ProgressBar(source_size, width=Config.width,
                               symbol=self.symbol, empty=self.empty,
                               fmt=ProgressBar.PUTA_MOVE)
        while True:
            chunk = source.read(32768)
            if not chunk:
                break
            target.write(chunk)
            copied += len(chunk)
            progress.current = copied
            progress()
        progress.done()
        self.clearlines()
        self.tprint("Moving", "Done")

        target.close()
        source.close()
        self.do_sync()
        os.remove(archive)

    def do_sync(self, width:int = Config.width):
        template = "> {:" + str(width) + "}: "
        self.wait_start(template.format('Syncing'))
        os.system('sync')
        self.wait_done('Done')

    # ------------------------------------------------------------------------
    # -- ZIP functions
    # ------------------------------------------------------------------------
    def set_compression(self, level:int=0):
        """
        Set compression level:
            0 = deflated
            1 = lzma
            2 = bzip2
        """
        match(level):
            case 1:
                Config.compress = ZIP_LZMA
            case 2:
                Config.compress = ZIP_BZIP2
            case _:
                Config.compress = ZIP_DEFLATED

    def collect_files(self, folder):
        pattern = os.path.join(folder, '**')
        return glob.glob(pattern, recursive=True)

    def check_archive(self, folder: str, width:int = Config.width):
        archive = folder.replace(' ', '_') + '.zip'
        template = "> {:" + str(width) + "}: "
        with ZipFile(archive, mode='r', compression=Config.compress) as zf:
            self.wait_start(template.format('Checking archive'))
            if not zf.testzip():
                self.wait_done('OK')
            else:
                self.wait_done('NOK')
                self.print(f'Something went wrong creating {archive},')
                self.print('please try it again...')
                sys.exit()

    def zipit(self, folder:str = ''):
        if not folder:
            self.error('No folder passed to zipit function')

        if not os.path.exists(folder):
            self.error(f"{folder} does not exist")
        
        files = self.collect_files(folder)
        total = len(files)
        archive = folder.replace(' ', '_') + '.zip'

        if os.path.exists(archive):
            os.remove(archive)


        progress = ProgressBar(total, width=Config.width,
                               symbol=self.symbol, empty=self.empty,
                               fmt=ProgressBar.PUTA)
        with ZipFile(archive, mode='w', compression=Config.compress) as zf:
            for i, entry in enumerate(files, start=1):
                zf.write(entry)
                progress.current = i
                progress()
            progress.done()
        self.clearlines()
        self.tprint("Archiving", "Done")

    def unzip(self, archive_path:str):
        with ZipFile(archive_path, 'r') as zf:
            filelist = zf.infolist()
            total = len(filelist)

            progresszip = ProgressBar(total, width=Config.width,
                                      symbol=self.symbol, empty=self.empty,
                                      fmt=ProgressBar.PUTA_ZIP)
            for i, entry in enumerate(filelist):
                progresszip.current = i
                extracted_path = zf.extract(entry, Config.playfolder)
                if entry.create_system == 3:
                    unix_attr = entry.external_attr >> 16
                    if unix_attr:
                        os.chmod(extracted_path, unix_attr)
                progresszip()
            progresszip.done()
