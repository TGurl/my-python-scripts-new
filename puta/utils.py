import os
import sys
import glob
import math
import zipfile

from datetime import datetime
from time import sleep


class TransgirlUtils:
    def __init__(self):
        self.twdith = 55
        self.usb_folder = os.path.join('/', 'USB', 'sexgames')
        self.lore_folder = os.path.join('/', 'lore', 'sexgames')

    # ---------------------------------------------------------------- UI Stuff
    def draw_title_box(self, cls = True) -> None:
        if cls:
            os.system('clear')
        lines = ['┌─────────────────────────────────────┐',
                 '│ Puta - 2024 Trangirl Coding Studios │',
                 '└─────────────────────────────────────┘']
        for line in lines:
            print(line)

    def message(self, msg: str, prompt: str = '·'):
        print(f" {prompt} {msg}")

    def done(self, msg: str, numlines:int = 1, prompt: str = '✓'):
        self.clearlines(numlines=numlines)
        print(f" {prompt} {msg}")

    def error(self, msg: str, do_exit: bool = True, prompt: str = '×') -> None:
        print(f" {prompt} {msg}")
        if do_exit:
            sys.exit()

    # ---------------------------------------------------------------- IO stuff
    def convert_size(self, size_bytes) -> str:
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    def collect_files(self, pattern: str) -> list:
        files = glob.glob(pattern, recursive=True)
        files.sort()
        return files

    def clear_saves(self, folder: str) -> None:
        msg = f"Cleaning {folder}"
        pattern = os.path.join(folder, '**', 'saves', '**')
        files = self.collect_files(pattern)

        if len(files) < 3:
            self.done(f"Folder {folder} didn't need cleaning", numlines=0)
            return

        self.message(msg)
        for file in files:
            if not 'persistent' in file and not os.path.isdir(file):
                os.remove(file)
                sleep(0.2)
        self.done(msg)

    def shorten(self, msg: str, max_width: int = 36):
        left = (max_width // 2) - 2
        if len(msg) > max_width:
            right = left * -1
            msg = msg[:left] + '..' + msg[right:]
        return msg

    def move_file(self, source_file: str, dest_folder: str):
        source_size = os.stat(source_file).st_size
        destination = os.path.join(dest_folder, source_file)
        perc = 0
        copied = 0

        source = open(source_file, 'rb')
        target = open(destination, 'wb')

        while True:
            self.message(f"[{perc:3}] moving {source_file} to {dest_folder}")
            chunk = source.read(32768)
            if not chunk:
                break
            target.write(chunk)
            copied += len(chunk)
            perc = int(copied * 100 / source_size)
            self.clearlines()

        target.close()
        source.close()
        os.remove(source_file)
        self.clearlines()
        self.done(f"{source_file} moved to {dest_folder}", numlines=0)

    def check_if_archived(self, archive: str) -> None:
        folders = [self.lore_folder, self.usb_folder]

    # ------------------------------------------------------------------- Zipit
    def zipit(self, folder: str) -> str:
        archive = folder + '.zip'
        if os.path.exists(archive):
            os.remove(archive)

        pattern = os.path.join(folder, '**')
        files = self.collect_files(pattern)
        total = len(files)

        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_STORED) as zip_handle:
            for idx, file in enumerate(files, start=1):
                filestr = self.shorten(file)
                percent = idx * 100 // total
                action = 'creating' if os.path.isdir(file) else 'deflating'
                self.message(f"[{percent:3}%] {action} {filestr}")
                zip_handle.write(file)
                self.clearlines()
        size = self.convert_size(os.stat(archive).st_size)
        self.done(f"{archive} created successfully ({size})", numlines=0)
        return archive

    # --------------------------------------------------------- KEEP THIS LAST!
    def clearlines(self, numlines: int = 1) -> None:
        for _ in range(numlines):
            sys.stdout.write("\033[F") #back to previous line
            sys.stdout.write("\033[K") #clear line
