#!/usr/bin/env python
import os
import sys
import glob
import shutil

from colors import Colors
from time import sleep


class ClearSaves:
    def __init__(self):
        self.renpy_cache = os.path.join('/', 'data', 'downloads', 'Renpy')
        self.game_cache = os.path.expanduser(os.path.join('~', '.renpy'))
        wine_folder = os.path.expanduser(os.path.join('~', '.wine', 'drive_c', 'users', 'geertje'))
        self.wine_cache = os.path.join(wine_folder, 'RenPy')
        self.app_data = os.path.join(wine_folder, 'AppData', 'Roaming', 'RenPy')
        self.files_to_remove = []
   
    def clear_lines(self, num=1):
        for _ in range(num):
            print('\033[1A', end='\x1b[2K')

    def fprint(self, message, clear=False, new_line=False):
        if clear:
            os.system('clear')
        carriage_return = '\n\n' if new_line else '\n'
        for color in Colors.colors:
            message = message.replace(color[0], color[1])
        print(f"{message}", end=carriage_return)
   
    def message(self, text):
        self.fprint(f"%y>%R {text}")

    def error(self, text):
        self.fprint(f"%r>%R {text}")

    def banner(self):
        self.fprint("%c------------------------------------------%R", clear=True)
        self.fprint(" %yClearSaves - Copyright 2023-24 Transgirl%R")
        self.fprint("%g  a simple cache clearer for RenPy games %R")
        self.fprint("%c------------------------------------------%R")

    def collect_info(self):
        game_path = os.path.join(self.game_cache, '**')
        renpy_path = os.path.join(self.renpy_cache, '**', 'tmp')
        app_path = os.path.join(self.app_data, '**')
        wine_path = os.path.join(self.wine_cache, '**')

        game_files = glob.glob(game_path, recursive=True)
        renpy_files = glob.glob(renpy_path, recursive=True)
        app_data = glob.glob(app_path, recursive=True)
        wine_files = glob.glob(wine_path, recursive=True)

        if len(game_files) > 0:
            self.files_to_remove.extend(game_files)

        if len(renpy_files) > 0:
            self.files_to_remove.extend(renpy_files)

        if len(app_data) > 0:
            self.files_to_remove.extend(app_data)

        if len(wine_files) > 0:
            self.files_to_remove.extend(wine_files)

    def clear_system(self, wait=0.1):
        total = len(self.files_to_remove)
        if not total:
            self.message('There were no files to remove...')
            sys.exit()

        for idx, item in enumerate(self.files_to_remove, start=1):
            percent = (idx * 100) // total
            name = item if len(item) < 40 else item[:18] + ".." + item[-18:]
            self.message(f"Removing {percent:3}% : {name}")
            if os.path.isdir(item):
                shutil.rmtree(item)
            sleep(wait)
            self.clear_lines()
        self.message("All clean now...")

    def run(self):
        self.banner()
        self.collect_info()
        self.clear_system()

if __name__ == "__main__":
    app = ClearSaves()
    app.run()
