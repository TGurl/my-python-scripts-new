#!/usr/bin/env python
import os
import sys
import math
import argparse

from zipfile import ZipFile


class MunZip():
    def __init__(self):
        self.remove_archive = False
        self.twidth = os.get_terminal_size().columns - 2

    def clear_lines(self, number=1):
        for _ in range(number):
            print('\033[1A', end='\x1b[2K')

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KiB", "MiB", "GiB", "TiB",
                     "PiB", "EiB", "ZiB", "YiB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s}{size_name[i]}"

    def shorten_string(self, message, width=0):
        if not width:
            width = self.twidth
        if len(message) <= width:
            return message

        middle = (width // 2) - 2
        left = message[:middle].strip()
        right = message[(middle * -1):].strip()
        return f"{left}..{right}"

    def unzipper(self, path, target_folder, length=45):
        with ZipFile(path, 'r') as archive:
            filelist = archive.infolist()
            total = len(filelist)
            for i, item in enumerate(filelist, start=0):
                perc = i * 100 // total
                fn = self.shorten_string(item.filename, width=length)
                action = 'creating' if item.is_dir() else 'inflating'
                print(f"-> [{perc:3}%] {action} {fn}")
                extracted_path = archive.extract(item, target_folder)
                if item.create_system == 3:
                    unix_attr = item.external_attr >> 16
                    if unix_attr:
                        os.chmod(extracted_path, unix_attr)
                self.clear_lines()

    def check_extension(self, archive):
        _, ext = os.path.splitext(archive)
        if ext.lower() not in ['.zip', '.epub', '.cbz']:
            print("Error: mUnzip can't unpack this archive!")
            sys.exit()

    def run(self, args):
        self.check_extension(args.archive)

        print("-= mUnzip - Transgirl Coding Studios 2024 =-")
        # filename = archive.replace('.zip', '')
        size = self.convert_size(os.stat(args.archive).st_size)
        # dest = os.path.join(os.getcwd(), filename)
        dest = os.getcwd()

        print(f"> Unzipping {args.archive} ({size})...")
        self.unzipper(args.archive, dest)
        if args.remove:
            os.remove(args.archive)
        self.clear_lines()
        print(f"> Unzipping {args.archive} ({size})... Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('archive',
                        help='Archive to unzip')

    parser.add_argument('-r', '--remove',
                        action='store_true',
                        required=False,
                        help='Remove archive once done')

    app = MunZip()
    app.run(parser.parse_args())
