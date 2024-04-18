#!/usr/bin/env python
import argparse
import glob
import os
import shutil
import sys
from random import choice, randint
from time import sleep
from zipfile import ZipFile

from pyfzf.pyfzf import FzfPrompt


class Porngames:
    def __init__(self):
        self.multi = False
        self.delete = False
        self.remove = False
        self.finished = False
        self.fzf = FzfPrompt()
        self.games = []
        self.playdir = os.path.join("/", "lore", "playing")
        self.folders = [
            os.path.join("/", "lore", "sexgames"),
            os.path.join("/", "USB", "sexgames"),
            os.path.join("/", "lore", "sexgames", "done"),
        ]

    def clear_line(self, num=1):
        for _ in range(num):
            print("\033[1A", end="\x1b[2K")

    def convert_size(self, size: float, decimals=2):
        unit = "B"
        for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
            if size < 1024.0 or unit == "PiB":
                break
            size /= 1024.0
        return f"{size:.{decimals}f} {unit}"

    def collect_games(self, query=None):
        self.games = []
        for folder in self.folders:
            pattern = os.path.join(folder, "**.zip")
            content = glob.glob(pattern, recursive=True)
            if query is None:
                self.games.extend(content)
            else:
                for item in content:
                    if query.lower() in item.lower():
                        self.games.append(item)

        self.games.sort()

    def fuzzy_find(self):
        data = self.fzf.prompt(self.games, "--reverse --multi --exact")
        return data

    def slogan(self):
        slogans = [
            "K9 Cock Lover",
            "Queen of Spades",
            "Bukake Lover",
            "Huge (.)(.) Lover",
            "Daddy's Whore",
            "Mom's Bull",
            "Mom fucks your bully",
            "Your mom is a whore",
            "I <3 BBC cum",
        ]
        return choice(slogans)

    def banner(self, clear=False, width=74):
        title = f"PORNGAMES v4.02 - {self.slogan()}"
        line = width * "─"
        spaces = ((width - len(title)) // 2) * " "

        if clear:
            os.system("clear")

        print(line)
        print(f"{spaces}{title}")
        print(line)

    def unzip(self, path, target_folder):
        # dest_path = os.path.join(self.playdir, target_folder)
        _ = target_folder

        with ZipFile(path, "r") as zf:
            filelist = zf.infolist()
            total = len(filelist)

            for i, item in enumerate(filelist, start=0):
                percent = i * 100 // total
                fn = (
                    item.filename
                    if len(item.filename) < 30
                    else ".." + item.filename[-28:]
                )
                print(f"  └> [{percent:3}%] inflating {fn}")
                extracted_path = zf.extract(item, self.playdir)
                if item.create_system == 3:
                    unix_attr = item.external_attr >> 16
                    if unix_attr:
                        os.chmod(extracted_path, unix_attr)
                self.clear_line()

        sleep(2)

    def extract_items(self, data):
        self.banner(clear=True)
        total = len(data)
        for idx, item in enumerate(data, start=1):
            # ----------------------------------------------
            # -- 1 Check if game has already been extracted
            # ----------------------------------------------
            target_folder = item.replace(".zip", "").split("/")[-1]
            size = self.convert_size(os.stat(item).st_size, decimals=1)

            if os.path.exists(os.path.join(self.playdir, target_folder)):
                print(f"› {target_folder} has already been extracted")
                sleep(1.2)
                self.clear_line()
                continue

            # ----------------------------------------------
            # -- 2 Extract the game
            # ----------------------------------------------
            print(f"› Extracting {idx}/{total} : {item} ({size})")
            try:
                self.unzip(item, target_folder)
                self.clear_line()
            except KeyboardInterrupt:
                print("› CTRL+C detected. Process halted!")
                sys.exit()

        # ----------------------------------------------
        # -- 3 Clear the previous line
        # ----------------------------------------------
        if self.delete:
            for idx, item in enumerate(data, start=1):
                size = self.convert_size(os.stat(item).st_size, decimals=1)

                try:
                    print(f"› Deleting {item} ({size})")
                    os.remove(item)
                    sleep(2.5)
                    self.clear_line()
                except KeyboardInterrupt:
                    print("› CTRL+C detected. Process halted!")
                    sys.exit()

        gstring = "games" if total > 1 else "game"
        print(f"› Extracted {total} {gstring}.")

    def remove_games(self, data):
        self.banner(clear=True)
        total = len(data)
        total_size = 0

        for idx, item in enumerate(data, start=1):
            total_size += os.stat(item).st_size
            size = self.convert_size(os.stat(item).st_size, decimals=1)
            print(f"› Removing {idx}/{total} : {item} ({size})")
            os.remove(item)
            sleep(0.5)
            self.clear_line()

        if total_size > 0:
            total_size = self.convert_size(total_size, decimals=1)
            print(f"› Freed up {total_size} of space.")

    def move_to_done(self, data):
        self.banner(clear=True)
        total = len(data)

        for idx, item in enumerate(data, start=1):
            filename = item.split("/")[-1]
            target = os.path.join("/", "lore", "sexgames", "done", filename)
            print(f"› Moving {idx}/{total} : {item}")
            shutil.move(item, target)
            sleep(0.5)
            self.clear_line()

        print("› Syncing...")
        os.system("sync")
        self.clear_line()

    def run(self, args):
        self.delete = args.delete
        self.remove = args.remove
        self.finished = args.finished
        self.collect_games(query=args.query)
        data = self.fuzzy_find()
        if len(data):
            if self.remove:
                self.remove_games(data)
                print("› You have removed the condom and got pregnant, you whore!")
            elif self.finished:
                self.move_to_done(data)
                x = randint(2, 101)
                print(
                    f"› You just had sex with {x} men, your pussy is full of their cum!"
                )
            else:
                self.extract_items(data)
                print("› Have fun playing, you slut!")
        else:
            self.banner(clear=True)
            print("› You didn't select any games, you slut!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-q", "--query", default=None, help="Query to search for")

    parser.add_argument(
        "-d", "--delete", action="store_true", help="Delete archive after extraction"
    )

    parser.add_argument(
        "-r", "--remove", action="store_true", help="Remove an archive from collection"
    )

    parser.add_argument(
        "-f", "--finished", action="store_true", help="Move game to done when finished"
    )

    app = Porngames()
    app.run(parser.parse_args())
