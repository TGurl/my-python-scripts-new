#!/usr/bin/env python
import argparse
import glob
import os
import pathlib
import shutil
import sys
from random import choice
from time import sleep
from zipfile import ZipFile

import psutil

from colors import Colors


class Archiver:
    def __init__(self, args):
        self.folder = args.folder
        self.keepsaves = args.keepsaves
        self.usb = args.usb
        self.delete = args.delete
        self.remove = args.remove
        self.source = args.source
        self.porn = args.porn
        self.remove_zips = args.remove_zips
        self.archive_size = 0
        self.cursor = True
        self.usbdir = os.path.join("/", "USB", "sexgames")
        self.loredir = os.path.join("/", "lore", "sexgames")
        self.donedir = os.path.join("/", "lore", "sexgames", "done")

    def readable_size(self, num, suffix="b"):
        for unit in ["", "k", "M", "G", "T", "P", "E", "Z"]:
            if abs(num) < 1024.0:
                # return "%3.1f %s%s" % (num, unit, suffix)
                return f"{num:3.1f} {unit}{suffix}"
            num /= 1024.0
        # return "%.1f%s%s" % (num, "Yi", suffix)
        return f"{num:.1f} Yi{suffix}"

    def get_free_space(self):
        destdir = self.usbdir if self.usb else self.loredir
        free = psutil.disk_usage(destdir).free
        total = psutil.disk_usage(destdir).total
        percent = free * 100 // total
        free_space = self.readable_size(free)

        if self.porn:
            self.msg(f"Your pussy is {free_space} ({percent}%) open")
        else:
            self.msg(f"Free space: {free_space} ({percent}%)")

    def toggle_cursor(self):
        if self.cursor:
            print("\033[? 25l", end="")
            self.cursor = False
        else:
            print("\033[? 25h", end="")
            self.cursor = True

    def clearline(self, num=1):
        for _ in range(num):
            print("\033[1A", end="\x1b[2K")

    def colorize(self, text):
        for color in Colors.colors:
            text = text.replace(color[0], color[1])
        return text

    def decolorize(self, text):
        for color in Colors.colors:
            text = text.replace(color[0], "")
        return text

    def myprint(self, text):
        text = self.colorize(text)
        print(text)

    def msg(self, text, exit_app=False):
        prompt = " %r♥%R " if self.porn else " >"
        self.myprint(f"{prompt} {text}")
        if exit_app:
            sys.exit()

    def info(self, text):
        if self.porn:
            spaces = 4 * " "
        else:
            spaces = 3 * " "
        self.myprint(f"{spaces}%b└>%R {text}")

    def banner(self):
        os.system("clear")
        slogans = [
            "I %r♥%c  (.)(.) ",
            "I %r♥%c  K9 Cock  ",
            "I %r♥%c  Big Black Cocks",
            "I %r♥%c  Creampies  ",
            "I %r♥%c  Creampies  ",
            "I %r♥%c  Gangbangs  ",
        ]
        slogan = choice(slogans)
        title = (
            "%yArc v5.02%R - %cA Simple Game Archiver%R"
            if not self.porn
            else f"%yARC v5.02%R - %c{slogan}%R"
        )
        width = 36
        spaces = ((width - len(self.decolorize(title))) // 2) * " "
        line = width * "─"
        topline = f"%c╭{line}╮"
        midline = f"│%R{spaces}{title}{spaces}%c│"
        botline = f"╰{line}╯%R"
        self.myprint(topline)
        self.myprint(midline)
        self.myprint(botline)

    def read_folder(self):
        return glob.glob(os.path.join(self.folder, "**"), recursive=True)

    def check_if_archived(self):
        archive_name = self.folder + ".zip"
        folders = [self.usbdir, self.loredir, self.donedir]
        for folder in folders:
            check = os.path.join(folder, archive_name)
            if os.path.exists(check):
                if self.delete:
                    os.remove(check)
                    if self.porn:
                        self.msg("You took home a stranger from the bar")
                    else:
                        self.msg("Archived version deleted")
                else:
                    if self.porn:
                        self.msg(f"You rented a room with {archive_name} in {folder}")
                        self.msg("Use -d to have sex for the money he offers")
                    else:
                        self.msg(f"{archive_name} found in {folder}")
                        self.msg("Use -d to delete it")
                    # self.toggle_cursor()
                    sys.exit()

    def sync(self):
        if self.porn:
            self.msg("Cumming...")
        else:
            self.msg("Syncing...")
        os.system("sync")
        self.clearline()
        if self.porn:
            self.msg("You came so loud!")
        else:
            self.msg("Syncing done")

    def clean_folder(self, keepsaves=False):
        # --- step 1: setting up

        remove_list = []
        files = self.read_folder()
        extensions = [".log", ".code-workspace"]
        if not keepsaves:
            extensions.append(".save")
            extensions.append(".rpgsave")

        if self.remove_zips:
            print("---> Remove zips:", self.remove_zips)
            # extensions.append(".zip")

        remove = ["log.txt", "errors.txt", "traceback.txt", "memory.txt", "desktop.ini"]

        # --- step 2: check the extensions
        for file in files:
            if pathlib.Path(file).suffix in extensions:
                remove_list.append(file)

        # --- step 3: check the full filenames
        for file in files:
            for item in remove:
                if item.lower() == file.split("/")[-1].lower():
                    remove_list.append(file)

        # --- step 4: remove all files in the created list
        if len(remove_list) > 0:
            remove_list.sort()
            if self.porn:
                self.msg(f"Undressing in front of {self.folder}")
            else:
                self.msg(f"Cleaning folder {self.folder}")
            for item in remove_list:
                if self.porn:
                    self.info(f"taking of {item}")
                else:
                    self.info(f"removing {item}")
                os.remove(item)
                sleep(0.4)
                self.clearline()

            # --- step 4a: end message
            self.clearline()
            if self.porn:
                self.msg("You are naked now")
            else:
                self.msg("Cleaning done")
        else:
            # --- step 4b: no cleaning msg
            if self.porn:
                self.msg("You were alone in the room")
            else:
                self.msg("No cleaning needed")

    def zipit(self):
        destdir = self.usbdir if self.usb else self.loredir
        if self.porn:
            self.msg(f"You are sleeping with {self.folder} in {destdir}")
        else:
            self.msg(f"Archiving {self.folder} to {destdir}")

        files = self.read_folder()
        total = len(files)
        destination = os.path.join(destdir, self.folder + ".zip")

        with ZipFile(destination, "w", compresslevel=9) as zip_file:
            for idx, item in enumerate(files):
                percent = idx * 100 // total
                filename = item if len(item) < 40 else ".." + item[-38:]
                if os.path.isdir(item):
                    if self.porn:
                        self.info(f"sucking [{percent:3}%] {filename}")
                    else:
                        self.info(f"creating [{percent:3}%] {filename}")

                else:
                    if self.porn:
                        self.info(f"fucking [{percent:3}%] {filename}")
                    else:
                        self.info(f"adding [{percent:3}%] {filename}")

                zip_file.write(item)
                self.clearline()

            # --- Check the archive
            self.msg(f"Checking {destination}...")
            try:
                ret = zip_file.testzip()
                if ret is not None:
                    self.msg(f"First bad file in {destination}: {ret}", exit_app=True)
            except Exception as ex:
                self.msg(f"ERROR: {ex}", exit_app=True)

        self.clearline()
        self.archive_size = os.stat(destination).st_size
        size = self.readable_size(self.archive_size)
        if self.porn:
            self.msg(f"You have sex with {self.folder} ({size})")
        else:
            self.msg(f"{self.folder} archived ({size})")
        self.sync()

    def remove_archive(self):
        if ".zip" not in self.folder:
            archive_name = self.folder + ".zip"
        else:
            archive_name = self.folder

        destdir = self.usbdir if self.usb else self.loredir
        destination = os.path.join(destdir, archive_name)

        if os.path.exists(destination):
            arc_size = os.stat(destination).st_size
            size = self.readable_size(arc_size)
            os.remove(destination)
            if self.porn:
                self.msg(f"You sent {archive_name} ({size}) home after having sex")
            else:
                self.msg(f"{archive_name} ({size}) removed from archives")

            # self.toggle_cursor()
            sys.exit()

    def remove_source(self):
        if self.porn:
            self.msg(f"{self.folder} drove you home after having sex")
        else:
            self.msg("Removing source folder")
        shutil.rmtree(self.folder)
        self.clearline()
        if self.porn:
            self.msg(f"{self.folder} went home after a booty call")
        else:
            self.msg("Source folder removed")

    def check_if_folder_exists(self):
        if not os.path.exists(self.folder):
            if self.porn:
                self.msg(f"Oh no, {self.folder} didn't show up for a booty call")
            else:
                self.msg(f"Oops, {self.folder} doesn't seem to exist")

            # self.toggle_cursor()
            sys.exit()

    def run(self):
        # self.toggle_cursor()
        self.banner()
        self.check_if_folder_exists()
        if self.remove:
            self.get_free_space()
            self.remove_archive()
        self.check_if_archived()
        self.clean_folder(keepsaves=self.keepsaves)
        self.get_free_space()
        self.zipit()
        if not self.source:
            self.remove_source()
        # self.toggle_cursor()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("folder", help="Folder to archive")
    parser.add_argument(
        "-k", "--keepsaves", action="store_true", help="Keep the save files"
    )
    parser.add_argument(
        "-u", "--usb", action="store_true", help="Store the archive to usb"
    )
    parser.add_argument(
        "-d", "--delete", action="store_true", help="Delete the archived version"
    )
    parser.add_argument(
        "-r", "--remove", action="store_true", help="Remove the archived version"
    )
    parser.add_argument(
        "-s", "--source", action="store_true", help="Keep the source folder"
    )
    parser.add_argument(
        "-z", "--remove-zips", action="store_true", help="Remove zip files"
    )
    parser.add_argument("-p", "--porn", action="store_true", help="Pornify ARC")

    app = Archiver(parser.parse_args())
    app.run()
