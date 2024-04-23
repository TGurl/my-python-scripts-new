#!/usr/bin/env python
import os
import sys
import json
import random
import readchar
import argparse
import subprocess

from utils import TransgirlUtils
from time import sleep
from pyfzf.pyfzf import FzfPrompt


class Wallpaper(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.cursor = True
        self.twidth = os.get_terminal_size().columns
        self.walldir = os.path.join("/", "data", "pictures", "walls")
        self.config = os.path.expanduser(
                os.path.join("~", ".config", "transgirl", "wallpapers.json"))

    def wp_init(self):
        self.data.update({'current': '', 'maincat': 'nsfw',
                          'subcat': 'girls', 'setter': 'feh',
                          'random': False, 'sddm': False,
                          'notify': True})


    def load_config(self):
        if not os.path.exists(self.config):
            self.wp_init()
            self.save_config()
        with open(self.config, 'r', encoding='utf-8') as json_file:
            self.data = json.load(json_file)

    def save_config(self):
        with open(self.config, 'w', encoding='utf-8') as json_file:
            json.dump(self.data, json_file, indent=4)

    def collect_wallpapers(self, folder) -> list:
        pic_list = []
        allowed = ['.jpg', '.png', '.webp']
        for item in os.scandir(folder):
            _, ext = os.path.splitext(item.name)
            if ext in allowed:
                pic_list.append(item.path)
        pic_list.sort()
        return pic_list

    def change_grub_wallpaper(self):
        grub = os.path.join("/", "boot", "grub", "themes", "girls", "background.png")
        password = 'cyber008'
        wall = self.data['current']
        _, ext = os.path.splitext(wall)
        if ext == '.png':
            subprocess.call(f'echo {password} | sudo -S cp {wall} {grub} > /dev/null 2>&1', shell=True)
        else:
            subprocess.call(f'echo {password} | sudo -S convert {wall} {grub} > /dev/null 2>&1', shell=True)
        self.clear_lines()

    def change_wallpaper(self, option='next'):
        self.load_config()
        fullpath = os.path.join(self.walldir, self.data['maincat'], self.data['subcat'])
        images = self.collect_wallpapers(fullpath)
        total = len(images)
        current = self.data['current']
        new_wall = ''

        if self.data['random']:
            new_wall = random.choice(images)
            self.data.update({'current': new_wall})
        elif option == 'next':
            if current == '':
                new_wall = images[0]
            else:
                idx = images.index(current) + 1 
                if idx >= total:
                    idx = 0
                new_wall = images[idx]
        elif option == 'previous':
            if current == '':
                new_wall = images[-1]
            else:
                idx = images.index(current) - 1
                if idx < 0:
                    idx = -1
                new_wall = images[idx]
        self.data.update({'current': new_wall})
        self.save_config()
        if self.data['setter'] == 'feh':
            cmd = f"feh --bg-scale {new_wall} > /dev/null 2>&1"
        else:
            cmd = f"nitrogen --set-scaled {new_wall} > /dev/null 2>&1"
        os.system(cmd)
        self.clear_lines()

        if self.data['sddm']:
            self.change_grub_wallpaper()

        if self.data['notify']:
            wp_name = new_wall.split('/')[-1]
            os.system(f"notify-send --icon=dialog-information -u low 'Wallpaper:' '{wp_name}'")

    def collect_folders(self, folder, discard=[]) -> list:
        folders = []
        for entry in os.scandir(folder):
            if entry.is_dir() and entry.name not in discard:
                folders.append(entry.name)
        folders.sort()
        return folders

    def select_main_category(self):
        categories = self.collect_folders(self.walldir, discard=['.git', 'downloads', 'keepers'])
        main_cat = FzfPrompt().prompt(categories, '--reverse --exact')
        self.data.update({'maincat': main_cat[0]})
        self.select_sub_category()
        # self.data.update({'curent': ''})
        # self.save_config()

    def select_sub_category(self):
        fullpath = os.path.join(self.walldir, self.data['maincat'])
        categories = self.collect_folders(fullpath, discard=['removed'])
        sub_cat = FzfPrompt().prompt(categories, '--reverse --exact')
        self.data.update({'subcat': sub_cat[0]})
        self.data.update({'current': ''})
        self.save_config()
        self.change_wallpaper()

    def setup(self):
        true = '%gTrue%R'
        false = '%rFalse%R'

        while True:
            self.load_config()
            self.show_title(appname='WP', width=65)
            self.cprint(self.random_slogan(), width=65, new_line=True)
            random = true if self.data['random'] else false
            sddm = true if self.data['sddm'] else false
            notify = true if self.data['notify'] else false
            curwall = self.data['current'].split('/')[-1]
            self.printr(f"Current wallpaper              : %y{curwall}%R", new_line=True)
            self.printr(f"[%g1%R] Change main category       : %y{self.data['maincat']}%R")
            self.printr(f"[%g2%R] Change sub category        : %y{self.data['subcat']}%R")
            self.printr(f"[%g3%R] Toggle wallpaper setter    : %y{self.data['setter']}%R")
            self.printr(f"[%g4%R] Toggle random wallpaper    : {random}")
            self.printr(f"[%g5%R] Toggle sddm/grub wallpaper : {sddm}")
            self.printr(f"[%g6%R] Toggle notifications       : {notify}", new_line=True)
            self.printr(f"[%rq%R] Quit setup", new_line=True)
            print(self.colorize('%y>>%R '), end='', flush=True)

            key = readchar.readchar().lower()
            if key not in '123456q':
                self.error_message("Really? You pressed a wrong key? Are you that stupid?", dot='')
                sleep(1.5)
            elif key == '1':
                self.select_main_category()
            elif key == '2':
                self.select_sub_category()
            elif key == '3':
                self.data['setter'] = 'nitrogen' if self.data['setter'] == 'feh' else 'feh'
                self.save_config()
            elif key == '4':
                random = not self.data['random']
                self.data.update({'random': random})
                self.save_config()
            elif key == '5':
                sddm = not self.data['sddm']
                self.data.update({'sddm': sddm})
                self.save_config()
            elif key == '6':
                notify = not self.data['notify']
                self.data.update({'notify': notify})
                self.save_config()
            else:
                break

        self.show_title(appname='WP', width=65)
        self.cprint(self.random_slogan(), width=65, new_line=True)
        self.printr("%y>>%R WP setup complete.")
        sys.exit()

    def run(self, args):
        if args.setup:
            self.setup()

        if args.next:
            self.toggle_cursor()
            self.change_wallpaper(option='next')
            self.toggle_cursor()

        if args.previous:
            self.toggle_cursor()
            self.change_wallpaper(option='previous')
            self.toggle_cursor()

    def toggle_cursor(self):
        if self.cursor:
            print('\033[? 25l', end="")
            self.cursor = False
        else:
            print('\033[? 25h', end="")
            self.cursor = True


if __name__ == "__main__":
    app = Wallpaper()

    parser = argparse.ArgumentParser()
    mgroup = parser.add_mutually_exclusive_group(required=True)

    mgroup.add_argument('-n', '--next',
                        action='store_true',
                        help='go to next wallpaper')

    mgroup.add_argument('-p', '--previous',
                        action='store_true',
                        help='go to previous wallpaper')

    mgroup.add_argument('-s', '--setup',
                        action='store_true',
                        help='enter setup')

    app.run(parser.parse_args())
