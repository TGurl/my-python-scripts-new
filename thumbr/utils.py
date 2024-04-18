#!/usr/bin/env python
import os
import sys
import readchar
import datetime
import random
import string
import math
import glob
import time

from colors import Colors
from time import sleep
from zipfile import ZipFile, ZIP_STORED


class TransgirlUtils:
    def __init__(self):
        self.initialize()

    def initialize(self):
        self.twidth = os.get_terminal_size().columns

    def random_slogan(self):
        slogans = ['I want to have my own b(.)(.)bs!',
                   'Trans rights are human rights!',
                   'I love BBC!',
                   'I am a K9 cock sucker!',
                   'I want to be raped!',
                   'I am just a dumb cumdump!',
                   'I want to be a free use whore!',
                   'I want to suck a huge =====)',
        ]
        return random.choice(slogans)

    def colorize(self, text, remove_colors=False):
        for color in Colors.colors:
            replacement = '' if remove_colors else color[1]
            text = text.replace(color[0], replacement)
        return text

    def printr(self, message, new_line=False):
        newline = '\n\n' if new_line else '\n'
        message = self.colorize(message)
        print(message, end=newline)

    def fprintr(self, message, dot='->'):
        print(f"%b{dot}%R {message}", end='', flush=True)

    def cprint(self, message, width=0, new_line=False):
        if not width:
            width = self.twidth
        temp = self.colorize(message, remove_colors=True)
        message = self.colorize(message)
        spaces = (width - len(temp)) // 2 * ' '
        self.printr(f"{spaces}{message}", new_line=new_line)

    def drawline(self, width=0, color='%c'):
        if not width:
            width = self.twidth
        line = width * '─'
        self.printr(f"{color}{line}%R")

    def arrow(self, message):
        self.printr(f"  %b-->%R {message}")

    def error_message(self, message, exit_app=True, dot='·'):
        if exit_app:
            self.printr(f"%r{dot}%R {message} Exiting.")
            sys.exit()
        else:
            self.printr(f"%r{dot}%R {message}")
    
    def ask_yes_no(self, message, dot='·'):
        msg = self.colorize(f"%g{dot}%R {message} (y/n) : ")
        keypressed = False
        key = ''
        while not keypressed:
            print(msg, end='', flush=True)
            key = readchar.readchar().lower()
            if key not in 'yn':
                self.error_message("That was a wrong key, you slut!")
                sleep(1.2)
            else:
                keypressed = True
        return True if key == 'y' else False

    def warning_message(self, message, dot='·'):
        self.printr(f"%y{dot}%R {message}")

    def default_message(self, message, dot='·', new_line=False):
        self.printr(f"%g{dot}%R {message}", new_line=new_line)

    def show_title(self, appname='APPNAME HERE', width=0, clear_screen=True):
        if not appname:
            self.error_message('No appname has been supplied.', exit_app=True)

        if not width:
            width = self.twidth

        copyright = f"%y{appname}%R - %bTransgirl Coding Studios 2024%R"
        if clear_screen:
            os.system('clear')
        self.drawline(width=width)
        self.cprint(copyright, width=width)
        self.drawline(width=width)

    def collect_items_in_folder(self, folder, extension=''):
        data = []
        for item in os.scandir(folder):
            isdir = os.path.isdir(item.path)
            if extension in item.name:
                entry = [item.path, isdir]
                data.append(entry)
        data.sort()
        return data

    def show_items_in_folder(self, folder, extension=''):
        data = self.collect_items_in_folder(folder=folder, extension=extension)
        for entry in data:
            file_color = '%g' if os.access(entry[0], os.X_OK) else '%r'
            sign = '%bDIR %R' if entry[1] else f'{file_color}FILE%R'
            self.printr(f"{sign} {entry[0]}")

    def shorten_string(self, message, width=0):
        if not width:
            width = self.twidth
        if len(message) <= width:
            return message

        middle = (width // 2) - 2
        left = message[:middle].strip()
        right = message[(middle * -1):].strip()
        return f"{left}..{right}"

    def convert_to_readable_time(self, seconds):
        readable = str(datetime.timedelta(seconds=seconds))
        if len(readable.split(':')[0]) == 1:
            readable = '0' + readable
        return readable

    def generate_random_string(self, length=16):
        chars = string.ascii_letters + string.digits
        random_chars = random.choices(chars, k=length)
        return ''.join(random_chars)

    def read_file(self, filename):
        if not os.path.exists(filename):
            self.error_message(f"File %i{filename}%R does not exist")
        data = [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]
        return data

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def move_file_with_percentage(self, source, destination):
        source_size = os.stat(source).st_size
        copied = 0
        source = open(source, 'rb')
        target = open(destination, 'wb')
        perc = 0
        self.default_message(f"Moving {source} -> {destination} [{perc:3}%]")
        while True:
            chunk = source.read(32768)
            if not chunk:
                break
            target.write(chunk)
            copied += len(chunk)
            perc = int(copied * 100 / source_size)
            self.clear_lines()
            self.default_message(f"Moving {source} -> {destination} [{perc:3}%]")
        target.close()
        source.close()

    def scantree(self, path, allowed=[]):
        data = []
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                yield from self.scantree(entry.path, allowed=allowed)
            else:
                item = yield entry.path
                if item:
                    _, ext = os.path.splitext(item)
                    if ext in allowed:
                        data.append(item)
        data.sort()
        return data

    def zipper(self, path, length=45, compresstype=ZIP_STORED):
        start_time = time.time()
        archive_name = path + ".zip"
        if os.path.exists(archive_name):
            self.error_message(f"File %i{archive_name}%R already exists. Removed it.", exit_app=False)
            os.remove(archive_name)
        data = glob.glob(os.path.join(path, "**"), recursive=True)
        total = len(data)
        perc = 0
        with ZipFile(archive_name, 'w', compresslevel=9, compression=compresstype) as archive:
            for idx, entry in enumerate(data, start=0):
                perc = idx * 100 // total
                fn = self.shorten_string(entry, width=length - 7)
                self.default_message(f"[{perc:3}%] Adding {fn}")
                archive.write(entry)
                self.clear_lines()
        size = self.convert_size(os.stat(archive_name).st_size)
        self.default_message(f"The size of {archive_name} is {size}.")
        time_taken = round(time.time() - start_time, 2)
        self.default_message(f"It took {time_taken} seconds.")

    def unzipper(self, path, target_folder, length=45):
        with ZipFile(path, 'r') as archive:
            filelist = archive.infolist()
            total = len(filelist)
            for i, item in enumerate(filelist, start=0):
                perc = i * 100 // total
                fn = self.shorten_string(item, width=length)
                self.default_message(f"[{perc:3}%] inflating {fn}")
                extracted_path = archive.extract(item, target_folder)
                if item.create_system == 3:
                    unix_attr = item.external_attr >> 16
                    if unix_attr:
                        os.chmod(extracted_path, unix_attr)
                self.clear_lines()

    # -- keep this one last because of stupid editor thingie
    def clear_lines(self, number=1):
        for _ in range(number):
            print('\033[1A', end='\x1b[2K')
