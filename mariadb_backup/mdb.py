#!/usr/bin/env python
"""
A simple script to backup mariadb databases.
Can be used in a systemd timer.
"""

import os
import sys


class Colors:
    reset = "\033[0m"
    black = "\033[30;1m"
    red = "\033[31;1m"
    green = "\033[32;1m"
    darkgreen = "\033[32m"
    yellow = "\033[33;1m"
    blue = "\033[34;1m"
    pink = "\033[35;1m"
    cyan = "\033[36;1m"
    white = "\033[37;1m"
    gray = "\033[37m"
    italic = "\x1B[3m"

    codes = ['%R', '%B', '%G', '%r', '%g', '%dg', '%y', '%b', '%p', '%c', '%w', '%i']
    colors = [
            ('%R', reset),
            ('%B', black),
            ('%G', gray),
            ('%r', red),
            ('%g', green),
            ('%dg', darkgreen),
            ('%y', yellow),
            ('%b', blue),
            ('%p', pink),
            ('%c', cyan),
            ('%w', white),
            ('%i', italic)
    ]


class MariadbBackup:
    def __init__(self):
        self.backup_path = os.path.join(
                "/",
                "data",
                "documents",
                "mariadb_backups",
                "all_databases.sql.gz")
    
    def colorize(self, text):
        for color in Colors.colors:
            text = text.replace(color[0], color[1])
        return text

    def myprint(self, text, nl=False):
        newline = '\n\n' if nl else '\n'
        text = self.colorize(text)
        print(text, end=newline)

    def notify(self, text):
        cmd = f"notify-send -u low '{text}'"
        os.system(cmd)

    def backup_databases(self):
        cmd = "mariadb-dump --single_transaction "
        cmd += "--flush-logs --events --routines --master-data=2 "
        # cmd += f"--all-databases -u root -p | gzip > {self.backup_path}"
        cmd += f"--all-databases | gzip > {self.backup_path}"
        os.system(cmd)
        self.notify("MDB backup created.")

    def restore_databases(self):
        cmd = f"zcat {self.backup_path} | mariadb -root -p"
        os.system(cmd)
        self.notify("MDB backup restored.")

    def show_help(self, error=""):
        if error == "":
            error = "You need to pass at least one argument."

        self.myprint("%c╭─────────────────────────╮")
        self.myprint("│ %yMariaDB Database Backup %c│")
        self.myprint("╰─────────────────────────╯%R", nl=True)
        self.myprint("Usage:", nl=True)
        self.myprint("  %c$ mdb backup%R")
        self.myprint("      Create a new backup for all databases", nl=True)
        self.myprint("  %c$ mdb restore%R")
        self.myprint("      Restore the backup")
        self.myprint("      You will be asked for the root password!", nl=True)
        self.myprint(f"%rERROR%R: {error}", nl=True)
        sys.exit()


if __name__ == "__main__":
    mbu = MariadbBackup()

    if len(sys.argv) == 1:
        mbu.show_help()
    else:
        match sys.argv[1].lower():
            case "backup":
                mbu.backup_databases()
            case "restore":
                mbu.restore_databases()
            case _:
                mbu.show_help("No or unknow parameter given.")
