#!/usr/bin/env python3
import glob
import os
import shutil
import sys
from random import choice, randint
from time import sleep

from colors import Colors


class Config:
    titles = [
        "Working the streets",
        "Lady of the night",
        "Callgirl on duty",
        "First class Escort",
        "Streetwhore",
        "Meth whore",
        "Daddy's little slut",
        "Shylark",
        "K9 Addict",
    ]
    version = "0.3b"
    keep = ["backups", "launcher-4", "tokens"]
    remarks = [
        "Fucking with",
        "Having sex with",
        "Being raped by",
        "Hooking for",
        "Kissing with",
        "Blowing",
        "Shooting meth with",
        "Being beaten by",
        "Dominating",
        "Pegging",
        "Having unsafe sex with",
        "Stretched out by",
        "Filming a porn with",
        "Streaming incest with",
        "Fucking my dog in front of",
        "Spreading my legs for",
    ]


class Cleaner:
    def __init__(self):
        self.title = self.choose_title()

    def colorize(self, text):
        for color in Colors.colors:
            text = text.replace(color[0], color[1])
        return text

    def decolorize(self, text):
        for code in Colors.codes:
            text = text.replace(code, "")
        return text

    def choose_title(self):
        return choice(Config.titles)

    def myprint(self, text, nl=False):
        newline = "\n\n" if nl else "\n"
        text = self.colorize(text)
        print(text, end=newline)

    def render_header(self):
        os.system("clear")
        self.myprint(f"%c>> %y{self.title}%R %g{Config.version} %c<<%R", nl=True)

    def collect_cache(self):
        renpycache = os.path.expanduser(os.path.join("~", "Downloads", "Renpy"))
        entries = glob.glob(os.path.join(renpycache, "**", "tmp"), recursive=True)
        return entries

    def collect_content(self):
        folder = os.path.expanduser(os.path.join("~", ".renpy"))
        entries = []
        for entry in os.listdir(folder):
            if os.path.isdir(os.path.join(folder, entry)) and entry not in Config.keep:
                entries.append(os.path.join(folder, entry))
        return entries

    def ledger(self, total_johns, earnings):
        os.system("clear")
        john = "Johns" if total_johns != 1 else "John"
        tabs = "\t" if total_johns < 2 else "\t"
        width = 30
        title = "%c>> %yL E D G E R %c<<%R"
        subtitle = f"%c{self.title}%R"
        wtitle = self.decolorize(title)
        wsub = self.decolorize(subtitle)

        numspc = (width - len(wtitle)) // 2
        numspc2 = (width - len(wsub)) // 2

        spcs = numspc * " "
        spcs2 = numspc2 * " "

        self.myprint(f"{spcs2}{subtitle}{spcs2}")
        self.myprint(f"{spcs}{title}{spcs}")
        self.myprint(width * "-")
        self.myprint(f"Total {john}:{tabs}{total_johns}")
        self.myprint(f"Earnings:{tabs}${earnings}")
        self.myprint(width * "-", nl=True)
        self.myprint("You filthy whore you!")
        sys.exit()

    def run(self):
        self.render_header()
        games = self.collect_content()
        cache = self.collect_cache()

        earned = 0
        total_johns = 0
        newline = False

        if len(games) == 0 and len(cache) == 0:
            self.myprint("You stood out there on the street for several hours,")
            self.myprint("and not a single John came. Could it be because it rained?")
            sys.exit()

        if len(games) > 0:
            newline = False
            for i, entry in enumerate(games, start=1):
                remark = choice(Config.remarks)
                earnings = randint(30, 500)
                earned += earnings
                total_johns += 1
                name = entry.split("/")[-1]
                if i == len(games):
                    newline = True
                self.myprint(
                    f"%b>%R {remark} %i%g{name}%R earning you ${earnings}", nl=newline
                )
                shutil.rmtree(entry)
                sleep(0.6)

        if len(cache) > 0:
            newline = False
            for i, entry in enumerate(cache, start=1):
                remark = choice(Config.remarks)
                earned += randint(50, 450)
                total_johns += 1
                name = entry.split("/")[-2]
                if i == len(cache):
                    newline = True
                self.myprint(f"%c>%R {remark} %i%y{name}%R", nl=newline)
                shutil.rmtree(entry)
                sleep(0.6)

        if total_johns == 0:
            self.myprint(
                "You didn't have any customers today. You go home empty handed..."
            )
            sys.exit()
        else:
            john = "John"
            if total_johns > 1:
                john += "s"

        self.ledger(total_johns, earned)


if __name__ == "__main__":
    app = Cleaner()
    app.run()
