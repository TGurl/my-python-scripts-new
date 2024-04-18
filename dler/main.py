#!/usr/bin/env python
import os
import shutil
import argparse

from utils import TransgirlUtils
from time import sleep


class Downloader(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.from_list = False

    def banner(self):
        self.show_title(appname='DLer', width=65)

    def error(self, message):
        self.error_message(message)

    def read_contents_of_file(self, filename):
        if not os.path.exists(filename):
            self.banner()
            self.error(f"File %i{filename}%R does not seem to exist.")
        with open(filename, 'r', encoding='utf-8') as filename:
            data = filename.readlines()
        return data

    def video_downloader(self, video_url):
        if not self.from_list:
            self.banner()
        url = self.shorten_string(video_url, width=54)
        self.default_message(f"URL     : {url}")
        self.drawline(width=65)
        self.default_message("Output  :", dot='>')

        ytdlp = f"yt-dlp --quiet --progress --no-warnings {video_url}"
        os.system(ytdlp)

    def parse_download_list(self, video_list):
        self.from_list = True
        data = self.read_contents_of_file(video_list)
        total = len(data)
        lead = len(str(total))

        for idx, line in enumerate(data, start=1):
            line = line.strip()
            self.banner()
            self.default_message(f"Parsing : %i{video_list}%R")
            self.default_message(f"Count   : {idx:{lead}}/{total}")
            self.video_downloader(line)
            sleep(1.3)
        self.clear_lines()
        os.remove(video_list)
        self.default_message("All done.", dot='>')

    def run(self, args):
        # -- you can't pass -v and -i at the same time
        if args.video and args.input:
            self.error("You can't use -v and -i at the same time.")

        # -- download single video when -v is passed
        if args.video and not self.from_list:
            self.video_downloader(args.video)

        # -- download videos from a given list
        if args.input:
            self.parse_download_list(args.input)


if __name__ == '__main__':
    app = Downloader()
    
    parser = argparse.ArgumentParser(prog='dler',
                                     description='A simple downloader',
                                     epilog='I want my own b(.)(.)bs')

    parser.add_argument('-v', '--video',
                        type=str,
                        metavar='X',
                        required=False,
                        help='single video download')

    parser.add_argument('-i', '--input',
                        type=str,
                        metavar='X',
                        required=False,
                        help='list of videos to download')

    app.run(parser.parse_args())
