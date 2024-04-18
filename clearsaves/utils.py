#!/usr/bin/env python
import os
import sys

from colors import Colors


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
        self.printr(f"%r{dot}%R {message}")
        if exit_app:
            self.arrow("Exiting...")
            sys.exit()

    def warning_message(self, message, dot='·'):
        self.printr(f"%y{dot}%R {message}")

    def default_message(self, message, dot='·'):
        self.printr(f"%g{dot}%R {message}")

    def banner(self, appname='APPNAME HERE', width=0, clear_screen=True):
        if not appname:
            self.error_message('No appname has been supplied.', exit_app=True)

        if not width:
            width = self.twidth

        copyright = f"%y{appname.title()}%R - %bTransgirl Coding Studios 2024%R"
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
