#!/usr/bin/env python
import os
import sys
import shutil
import math
import glob
import zipfile
import argparse

from colors import Colors
from time import sleep
from zipfile import ZipFile, ZipInfo, ZIP_LZMA, ZIP_DEFLATED
from pyfzf.pyfzf import FzfPrompt


# ----------------------------------------------------------------------------
# -- Core Class
# ----------------------------------------------------------------------------
class Core:
    def __init__(self):
        self.activemark = '[·]'
        self.checkmark = '[%g✔%R]'
        self.errormark = '[%r✗%R]'
        self.emptychar = '-'
        self.fullchar = '#'
        self.pbar_length = 30

    def clear_lines(self, num: int = 1) -> None:
        for _ in range(num):
            print('\033[1A', end='\x1b[2K')

    def convert_size(self, filesize: int) -> str:
        if not filesize:
            return "0B"
        size_names = ["B", "KiB", "MiB", "GiB", "TiB",
                     "PiB", "EiB", "ZiB", "YiB"]
        i = int(math.floor(math.log(filesize, 1024)))
        p = math.pow(1024, i)
        s = round(filesize / p, 1)
        return f"{s} {size_names[i]}"

    def shorten_string(self, string: str, width:int = 28) -> str:
        if len(string) > width:
            length = int(width / 2) - 2
            front = string[:length]
            end = string[(length * -1):]
            string = front + '..' + end
        return string

    def colorize(self, string: str, remove: bool = False) -> str:
        for color in Colors.colors:
            replacement = '' if remove else color[1]
            string = string.replace(color[0], replacement)
        return string
   
    def print(self, string: str, carriage_return = False) -> None:
        end = '\n\n' if carriage_return else '\n'
        print(self.colorize(string), end=end)

    def boxit(self, string: str, rounded:bool = False, color:str = '%c') -> None:
        chars = ['┌', '┐', '└', '┘', '│', '─']
        if rounded:
            chars = ['╭', '╮', '╰', '╯', '│', '─']

        temp_string = self.colorize(string, remove=True)
        horline = (len(temp_string) + 2) * chars[5]
        del temp_string
        self.print(f"{color}{chars[0]}{horline}{chars[1]}")
        self.print(f"{color}{chars[4]} {string} {color}{chars[4]}")
        self.print(f"{color}{chars[2]}{horline}{chars[3]}%R")

    def message(self, string: str, prompt:str = '%g>%R') -> None:
        self.print(f" {prompt} {string}")
    
    def warning(self, string: str, prompt:str = '%y>%') -> None:
        self.print(f" {prompt} {string}")
    
    def error(self, string: str, prompt:str = '%r>%R') -> None:
        self.print(f" {prompt} {string}")

    def sub_message(self, string: str) -> None:
        self.print(f"{5 * ' '}%b└>%R {string}")

    def clean_up(self, folder: str) -> None:
        self.message(f'Cleaning up', prompt=self.activemark)

        # -- first clean up some shit
        contents = glob.glob(os.path.join(folder, '**'), recursive=True)
        total = len(contents)
        remove = ['desktop.ini', 'log.txt', 'traceback.txt']
        for i, filepath in enumerate(contents, start=1):
            p = i * 100 // total
            self.sub_message(f"{p:3}% done")
            filename = filepath.split('/')[-1]
            if filename in remove:
                os.remove(filepath)
            self.clear_lines()
        
        # -- clean up the save files
        contents = glob.glob(os.path.join(folder, 'game', 'saves', '**'), recursive=True)
        total = len(contents)
        for i, file in enumerate(contents, start=1):
            p = i * 100 // total
            self.sub_message(f"{p:3}% done")
            if '.save' in file:
                os.remove(file)
            self.clear_lines()

        # -- All done
        self.clear_lines()
        self.message(f'Cleaning up', prompt=self.checkmark)

    def check_zipfile(self, archive_path: str) -> None:
        if not os.path.exists(archive_path):
            self.error(f"{archive_path} does not seem to exist.")
            sys.exit()

        if not zipfile.is_zipfile(archive_path):
            self.error(f"{archive_path} is not a valid zip archive.")
            sys.exit()

        with ZipFile(archive_path, 'r') as zf:
            self.message(f"Checking {archive_path}", prompt=self.activemark)
            result = self.errormark if zf.testzip() else self.checkmark
            self.clear_lines()
            self.message(f"Checking {archive_path}", prompt=result)
            if result == self.errormark:
                sys.exit()

    def remove_source_folder(self, folder: str) -> None:
        self.message(f"Removing /{folder}", prompt=self.activemark)
        if os.path.exists(folder):
            shutil.rmtree(folder)
        self.clear_lines()
        self.message(f"Removing /{folder}", prompt=self.checkmark)

    def progress_bar(self, count:int, total:int, suffix='', bar_length=40):
        filled_up = int(round(bar_length * count / float(total)))
        percentage = round(100.0 * count / float(total))
        bar = self.fullchar * filled_up
        bar += self.emptychar * (bar_length - filled_up)
        full_bar = f"[{bar} {percentage:3}%]"
        if suffix:
            full_bar += f" {suffix}"
        return full_bar

    def zipitup(self, folder: str, archive_path: str, lzma:bool = False) -> None:
        self.clean_up(folder=folder)

        message = f"Creating {archive_path}"
        if lzma:
            message += " (LZMA)"

        compression = ZIP_LZMA if lzma else ZIP_DEFLATED
        self.message(message, prompt=self.activemark)
       
        pattern = os.path.join(folder, '**')
        file_list = glob.glob(pattern, recursive=True)
        total = len(file_list)

        with ZipFile(archive_path, 'w') as zf:
            for i, fp in enumerate(file_list, start=1):
                # p = i * 100 // total
                act = 'creating' if os.path.isdir(fp) else 'zipping'
                fps = self.shorten_string(fp)
                bar = self.progress_bar(i, total,
                                        bar_length=self.pbar_length,
                                        suffix=f"{act} {fps}")
                #self.sub_message(f"[{p:3}%] {act} {self.shorten_string(fp)}")
                self.sub_message(bar)
                zf.write(fp, compress_type=compression)
                self.clear_lines()

        self.clear_lines()
        self.message(message, prompt=self.checkmark)
        self.check_zipfile(archive_path)

    def undress(self, archive_path: str, dest_path: str) -> None:
        self.check_zipfile(archive_path)

        info = ZipInfo.from_file(archive_path)
        archive_size = self.convert_size(info.file_size)

        self.message(f"Parsing {archive_path} ({archive_size})", prompt=self.activemark)
        with ZipFile(archive_path, 'r') as zf:
            filelist = zf.infolist()

            for i, item in enumerate(filelist, start=1):
                percent = i * 100 // len(filelist)
                fn = self.shorten_string(item.filename)
                if item.is_dir():
                    fs = ''
                    action = 'creating'
                else:
                    fs = ' ' + self.convert_size(item.file_size)
                    action = 'unzipping'

                self.sub_message(f"[{percent:3}%] {action} {fn}{fs}")
                extracted_path = zf.extract(item, dest_path)
                if item.create_system == 3:
                    unix_attr = item.external_attr >> 16
                    if unix_attr:
                        os.chmod(extracted_path, unix_attr)
                self.clear_lines()
            self.clear_lines()
        self.message(f"Unzipping {archive_path} ({archive_size})", prompt=self.checkmark)


    def move_archive(self, archive_path: str, destination: str):
        drive = os.path.join('/', destination.split('/')[1])
        free_space = shutil.disk_usage(drive).free
        source_size = os.stat(archive_path).st_size
        target_fn = os.path.join(destination, archive_path)
        
        # -- check available diskspace on destionation
        if free_space <= source_size:
            self.error(f"There is not enough free disk space on {destination}",
                       prompt=self.errormark)
            sys.exit()

        # -- move the archive with percentage
        copied = 0
        source = open(archive_path, 'rb')
        target = open(target_fn, 'wb')
        s_str = self.convert_size(source_size)

        self.message(f"Moving {archive_path} to {destination}",
                     prompt=self.activemark)
        while True:
            chunk = source.read(32768)
            if not chunk:
                break
            copied += len(chunk)
            c_str = self.convert_size(copied)
           
            bar = self.progress_bar(copied, source_size,
                                    bar_length=self.pbar_length,
                                    suffix=f"{c_str}/{s_str}")

            self.sub_message(bar)
            target.write(chunk)
            self.clear_lines()

        target.close()
        source.close()
        os.remove(archive_path)
        self.clear_lines()
        self.message(f"Moving {archive_path} to {destination}",
                     prompt=self.checkmark)


# ----------------------------------------------------------------------------
# -- Puta Class
# ----------------------------------------------------------------------------
class Puta(Core):
    def __init__(self):
        super().__init__()
        self.playdir = os.path.join('/', 'lore', 'playing', 'temp')
        self.loredir = os.path.join('/', 'lore', 'sexgames')
        self.usbdir = os.path.join('/', 'USB', 'sexgames')
        self.donedir = os.path.join(self.loredir, 'done')

    def check_if_archived(self, archive:str, delete:bool = False):
        paths = [self.loredir, self.usbdir, self.donedir]
        found = []
        for path in paths:
            check_path = os.path.join(path, archive)
            if os.path.exists(check_path) and delete:
                os.remove(os.path.join(path, archive))
            elif os.path.exists(check_path) and not delete:
                found.append(path)

        if found:
            pronounce = 'them' if len(found) > 1 else 'her'
            self.print(f" {archive} found in:")
            for path in found:
                self.print(f" - {path}")
            print()
            self.print(f" You can use -d to remove {pronounce}.")
            sys.exit()

    def add_game(self, folder: str, destination: str,
                 lzma:bool = False, delete:bool = False):
        archive = folder + '.zip'
        if os.path.exists(archive):
            os.remove(archive)

        self.check_if_archived(archive, delete=delete)
        self.zipitup(folder, archive, lzma=lzma)
        self.move_archive(archive, destination)
        self.remove_source_folder(folder)

    def install_games(self, query:str = '', delete:bool = False):
        if not query:
            query = ''
        paths = [self.loredir, self.usbdir, self.donedir]
        all_games = []
        for path in paths:
            for item in os.scandir(path):
                if '.zip' in item.path.lower() and query.lower() in item.path.lower():
                    all_games.append(item.path)
        all_games.sort()

        if not all_games:
            self.error(f"No games found!", prompt=self.errormark)
            sys.exit()

        games = FzfPrompt().prompt(all_games, '--reverse --multi --exact')
        if games:
            total_games = len(games)
            ext = 's' if total_games != 1 else ''
            self.message(f"Unpacking {total_games} game{ext}",
                         prompt=self.activemark)
            for game in games:
                self.undress(game, self.playdir)
                self.clear_lines()
                if delete:
                    os.remove(game)
            self.message(f"Unpacking {total_games} game{ext}",
                         prompt=self.checkmark)
        else:
            self.print(" Really? No games to install?")
            sys.exit()

    def run(self, args):
        os.system('clear')
        self.boxit('%yPuta %R- %bTransgirl Coding Studios')
        

        destination = self.usbdir if args.usb else self.loredir
        destination = self.donedir if args.completed else destination

        if args.add:
            if not os.path.exists(args.add):
                self.error(f"{args.add} does not seem to exist.",
                           prompt=self.errormark)
                sys.exit()

            self.add_game(args.add, destination,
                          lzma=args.lzma,
                          delete=args.delete)
            sys.exit()

        self.install_games(delete=args.delete, query=args.query)


# ----------------------------------------------------------------------------
# -- Making it all work
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    exclusive  = parser.add_mutually_exclusive_group(required=False)
    parser.add_argument('-a', '--add',
                        type=str,
                        metavar='X',
                        help='Add a game')

    parser.add_argument('-q', '--query',
                        type=str,
                        metavar='X',
                        help='Search for a game')

    parser.add_argument('-u', '--usb',
                       action='store_true',
                       required=False,
                       help='Store on USB')

    parser.add_argument('-c', '--completed',
                       action='store_true',
                       required=False,
                       help='Store game as completed')
    
    parser.add_argument('-d', '--delete',
                       action='store_true',
                       required=False,
                       help='Delete existing archive')
    
    parser.add_argument('-l', '--lzma',
                        action='store_true',
                        required=False,
                        help='Use lzma compression')

    app = Puta()
    app.run(parser.parse_args())
