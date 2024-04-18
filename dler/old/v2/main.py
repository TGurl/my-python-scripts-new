#!/usr/bin/env python
import os
import argparse

from colors import Colors
from datetime import datetime
from time import sleep


class Downloader:
    def __init__(self):
        self.colors = Colors().colors

    # -------------------------------------------------------------- File IO
    def read_file(self, filename='list') -> list:
        content = []
        with open(filename, 'r', encoding='utf-8') as file:
            data = file.readlines()
        for line in data:
            content.append(line.strip())
        return content
    
    def write_log(self, logline, logfile='dler-log.txt') -> None:
        state = 'a' if os.path.exists(logfile) else 'w'
        ct = datetime.now()
        date = f"{ct.year:04}/{ct.month:02}/{ct.day:02}-{ct.hour:02}:{ct.minute:02}:{ct.second:02} - "
        with open(logfile, state, encoding='utf-8') as logfile:
            logfile.write(f"{date}{logline}\n")

    # -------------------------------------------------------------- TUI
    def colorize(self, msg, remove_colors=False) -> str:
        for color in self.colors:
            needle = '' if remove_colors else color[1]
            msg = msg.replace(color[0], needle)
        return msg

    def printr(self, msg) -> None:
        msg = self.colorize(msg)
        print(msg)

    def message(self, msg) -> None:
        msg = f'%g>%R {msg}'
        self.printr(msg)

    def banner(self, current=0, total=0):
        os.system('clear')
        self.printr("%yDLER v4.0 - Transgirl Coding Studios%R")
        spacing = len(str(total))
        self.message(f'Processing: {current:{spacing}}/{total:{spacing}}')

    # -------------------------------------------------------------- Main loop
    def run(self):
        urls = self.read_file()
        total = len(urls)

        for idx, url in enumerate(urls, start=1):
            self.banner(current=idx, total=total)
            self.message(f'URL : {url}')
            ytdlp = f"yt-dlp {url}"
            os.system(ytdlp)
            sleep(3)


if __name__ == "__main__":
    app = Downloader()

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='List with urls to download')

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        required=False,
                        help='Show more output')

    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        required=False,
                        help='Show no output')

    app.run()
