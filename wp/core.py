import os
import sys
import yaml
import random

from utils2 import TransgirlUtils
from time import sleep
from pyfzf.pyfzf import FzfPrompt


class WallGirlCore(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.configpath = os.path.expanduser(
            os.path.join('~', '.config', 'transgirl', 'wallflower.yaml'))
        self.basedir = os.path.join('/', 'data', 'pictures', 'walls')
        self.category = 'sfw'
        self.subcat = 'nature'
        self.setter = 'feh'
        self.current = None

    def save_config(self):
        config = {'basedir': self.basedir, 'category': self.category,
                  'subcat': self.subcat, 'setter': self.setter,
                  'current': self.current}
        with open(self.configpath, 'w') as yf:
            yaml.dump(config, yf, sort_keys=False, default_flow_style=False)

    def load_config(self):
        with open(self.configpath, 'r') as yf:
            data = yaml.safe_load(yf)
        self.basedir = data['basedir']
        self.category = data['category']
        self.subcat = data['subcat']
        self.current = data['current']
        self.setter = data['setter']

    def toggle_random(self):
        self.random = not self.random
        self.save_config()

    def toggle_setter(self):
        self.setter = 'feh' if self.setter == 'nitrogen' else 'nitrogen'
        self.save_config()

    def collect_folders(self, path:str, blacklist:list, sort:bool=False):
        folders = []
        for item in os.scandir(path):
            if item.name.lower() not in blacklist and os.path.isdir(item.path):
                folders.append(item.name)
        if sort:
            folders.sort()
        return folders

    def set_category(self):
        blacklist = ['downloads', 'keepers', '.git']
        folders = self.collect_folders(self.basedir, blacklist=blacklist)
        selected = FzfPrompt().prompt(folders, '--reverse --exact')
        self.category = selected[0]
        self.subcat = None
        self.current = None
        self.set_subcat()

    def set_subcat(self):
        blacklist = ['removed']
        path = os.path.join(self.basedir, self.category)
        folders = self.collect_folders(path, blacklist=blacklist)
        selected = FzfPrompt().prompt(folders, '--reverse --exact')
        self.subcat = selected[0]
        self.save_config()
        self.change_wallpaper()

    def construct_wallpaper_path(self) -> str:
        return os.path.join(self.basedir, self.category, self.subcat)

    def collect_wallpapers(self) -> list:
        images = []
        path = self.construct_wallpaper_path()
        allowed = ['.png', '.jpg', '.jpeg', '.webp']
        for image in os.scandir(path):
            _, ext = os.path.splitext(image.name)
            if ext.lower() in allowed:
                images.append(image.path)
        images.sort()
        return images

    def set_wallpaper(self, path:str) -> None:
        if self.setter == 'feh':
            command = f"feh --bg-scale {path}"
        else:
            command = f"nitrogen --set-scaled {path}"
        self.execute_as_user(command)

    def set_random_wallpaper(self):
        images = self.collect_wallpapers()
        self.current = random.choice(images)
        self.set_wallpaper(self.current)
        self.change_grub_wallpaper()
        self.save_config()

    def change_grub_wallpaper(self):
        gwall = os.path.join('/', 'boot', 'grub', 'themes',
                             'girls', 'background.png')
        _, ext = os.path.splitext(self.current)
        if ext.lower() != '.png':
            command = f"magick {self.current} {gwall}"
        else:
            command = f"cp {self.current} {gwall}"
        self.execute_as_root(command)

    def change_wallpaper(self, direction='next'):
        images = self.collect_wallpapers()
        if not self.current:
            self.current = images[0]
            self.set_wallpaper(self.current)
            self.save_config()
            sys.exit()

        current_id = images.index(self.current)
        if direction == 'next':
            current_id += 1
            if current_id >= len(images):
                current_id = 0
        else:
            current_id -= 1
            if current_id < 0:
                current_id = len(images) - 1
        self.current = images[current_id]
        self.set_wallpaper(self.current)
        self.save_config()
        self.change_grub_wallpaper()
