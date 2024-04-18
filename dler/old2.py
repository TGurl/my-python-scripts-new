#!/usr/bin/env python
import os
import sys
import shutil
import argparse
import subprocess

from utils import TransgirlUtils
from time import sleep


class Downloader(TransgirlUtils):

    def __init__(self, args):
        super().__init__()
        self.video_url = args.video
        self.video_list = args.input

    def banner(self):
        self.show_title(appname='DLer', clear_screen=True, width=65)

    def download_video(self, from_list=False):
        if not from_list:
            self.banner()

        self.default_message(f"Downloading: {self.video_url}")

        ytdlp = "yt-dlp --no-warnings --quiet --progress "
        ytdlp += f"-o '%(title)s.%(ext)s' {self.video_url}"
        os.system(ytdlp)

    def process_video_list(self):
        if not os.path.exists(self.video_list):
            self.error_message("Where's my money? Huh? Whore, where's my money?!")
        
        with open(self.video_list, 'r', encoding='utf-8') as handler:
            data = handler.readlines()
        
        total = len(data)
        for idx, url in enumerate(data, start=1):
            self.banner()
            self.default_message(f"Processing: {self.video_list}")
            self.default_message(f"Progress  : {idx}/{total}")
            self.video_url = url.strip()
            self.download_video(from_list=True)
        
        self.banner()
        self.default_message('All done.')
        sys.exit()

    def run(self):
        if self.video_url and self.video_list:
            self.banner()
            self.error_message("So you want to have two cocks inside you? Really?")

        if not self.video_url and not self.video_list:
            self.banner()
            self.error_message("Yeah, you better be quiet, you slut!")

        if self.video_list:
            self.process_video_list()

        if self.video_url:
            self.download_video()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--video',
                        type=str,
                        metavar='X',
                        required=False,
                        help='video to download')

    parser.add_argument('-i', '--input',
                        type=str,
                        metavar='X',
                        required=False,
                        help='list of videos')
    
    app = Downloader(parser.parse_args())
    app.run()
