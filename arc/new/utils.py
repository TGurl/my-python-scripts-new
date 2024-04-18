#!/usr/bin/env python
import glob
import os
from zipfile import ZipFile

from tui import TUI


class Utils(TUI):
    def __init__(self):
        self.arc_name = ""
        self.yes = False
        self.files = []
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

    def pre_checks(self, folder=""):
        self.info_msg("Checking...")
        if not folder:
            self.err_msg("No folder passed", exit_app=True)

        # --- Check if the given folder even exists
        if not os.path.exists(folder):
            self.err_msg("That folder doesn't seem to exist!", exit_app=True)

        # --- Check if <folder>.zip exists in current folder
        self.arc_name = folder + ".zip"
        if os.path.exists(self.arc_name):
            if self.yes:
                os.remove(self.arc_name)
            else:
                self.err_msg(
                    f"An archive named %i{self.arc_name}%R already exists in current folder!",
                    exit_app=True,
                )

        # --- All checks passed
        self.clearlines()
        self.ok_msg("All checks passed")

    def read_files(self, folder):
        pattern = os.path.join(folder, "**")
        self.files = glob.glob(pattern, recursive=True)

    def zipit(self, folder):
        arc_name = folder + ".zip"
        total = len(self.files)

        # --- Create the archive
        with ZipFile(arc_name, "w", compresslevel=9) as zip_file:
            for idx, item in enumerate(self.files):
                percent = idx * 100 // total
                filename = item if len(item) < 40 else ".." + item[-38:]
                if os.path.isdir(item):
                    self.info_msg(f"creating [{percent:3}%] {filename}")
                else:
                    self.info_msg(f"adding [{percent:3}%] {filename}")
                zip_file.write(item)
                self.clearlines()

            # --- Check the archive
            self.info_msg(f"Checking {arc_name}...")
            try:
                ret = zip_file.testzip()
                if ret is not None:
                    self.err_msg(f"First bad file in {arc_name}: {ret}", exit_app=True)
            except Exception as ex:
                self.err_msg(f"ERROR: {ex}", exit_app=True)

            size = self.readable_size(os.stat(arc_name).st_size)
            self.clearlines()
            self.ok_msg(f"Created {arc_name} ({size})")

    def main_loop(self, folder, yes=False):
        self.yes = yes
        destination =
        self.banner()
        self.pre_checks(folder)
        self.read_files(folder)
        self.zipit(folder)
