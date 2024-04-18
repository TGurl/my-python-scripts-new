#!/usr/bin/env python
import os
import sys
import readchar
import datetime
import random
import string

from colors import Colors
from time import sleep


class TransgirlUtils:
    def __init__(self):
        self.initialize()

    def initialize(self):
        self.twidth = os.get_terminal_size().columns

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

    def clear_lines(self, number=1):
        for _ in range(number):
            print('\033[1A', end='\x1b[2K')
