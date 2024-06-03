#!/usr/bin/env python
import sys

from core import WallGirlCore


class WallGirl(WallGirlCore):
    def __init__(self):
        super().__init__()

    def run(self, args):
        self.load_config()
        if '-n' in args:
            self.change_wallpaper(direction='next')
        elif '-p' in args:
            self.change_wallpaper(direction='prev')
        elif '-r' in args:
            self.set_random_wallpaper()
        else:
            self.set_category()

if __name__ == "__main__":
    app=WallGirl()
    app.run(sys.argv)
