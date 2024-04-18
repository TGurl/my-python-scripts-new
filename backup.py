#!/usr/bin/env python
import os
from shutil import move

def main():
    for entry in os.scandir('.'):
        if not os.path.exists('archives'):
            os.mkdir('archives')

        if entry.is_dir():
            if entry.name == '.git':
                continue
            zfile = entry.name + '.7z'
            os.system(f"7z a {zfile} {entry.name}")
            move(zfile, os.path.join('archives', zfile))


if __name__ == "__main__":
    main()
