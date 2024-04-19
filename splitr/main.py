#!/usr/bin/env python
import os
import re
import sys
import shutil
import argparse

from utils import TransgirlUtils
from pytube import YouTube, Channel, Playlist
from time import sleep


class Splitr(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.cleanup = True
        self.splitvideos = False
        self.thumbnail = False
        self.resize = False
        self.download_folder = 'downloads'
        self.screenshot_folder = 'screenshots'
        self.keep_folder = 'keep'

    def banner(self, slogan=False):
        self.show_title(appname='Splitr', width=65)
        if slogan:
            self.cprint(self.random_slogan(), width=55, new_line=True)

    def cleanup_at_isle_three(self):
        folders = [self.download_folder, self.screenshot_folder]
        for folder in folders:
            if os.path.exists(folder):
                shutil.rmtree(folder)

    def check_if_youtube(self, video_url):
        return "youtube.com" in video_url

    def download_video(self, video_url, solo=True):
        if solo:
            self.banner()
        platform = 'YouTube' if self.check_if_youtube(video_url) else 'Other'
        y = YouTube(video_url)
        title = re.sub('\(.*?\)', '', y.title).strip()
        filename = title.replace(' ', '-').lower() + '-' + self.generate_random_string(length=4)
        self.printr(f"Platform       : {platform}")
        self.printr(f"Downloading    : {video_url}")
        self.printr(f"Video title    : {title}")
        self.printr(f"Saving as      : {filename}")

        thumbnail = '--write-thumb' if self.thumbnail else ''
        template = f"-o 'downloads/{filename}.%(ext)s'"
        ytdlp = f"yt-dlp --quiet --progress --no-warnings {thumbnail} "
        ytdlp += f"{template} {video_url}"
        try:
            os.system(ytdlp)
        except KeyboardInterrupt:
            sys.exit()

    def download_playlist(self, playlist_url):
        if not os.path.exists(self.download_folder):
            os.mkdir(self.download_folder)
        if not self.check_if_youtube(playlist_url):
            self.banner(slogan=True)
            self.error_message("You can only use playlist from YouTube.")
            sys.exit()
        self.default_message('Collecting info...')
        p = Playlist(playlist_url)
        self.clear_lines()
        total = len(p.video_urls)
        indent = len(str(total))
        for pidx, url in enumerate(p.video_urls, start=1):
            self.banner()
            self.printr(f"Playlist title : {p.title}")
            self.printr(f"Parsing url    : {pidx:{indent}}/{total}")
            self.download_video(url, solo=False)

    def parse_list(self, list_of_videos):
        self.printr(f"Parsing {list_of_videos}")

    def run(self, args):
        self.cleanup_at_isle_three()

        if args.keep:
            self.cleanup = False

        self.splitvideos = args.split
        self.thumbnail = args.writethumb
        self.resize = args.resize

        if args.video:
            self.download_video(args.video)

        if args.input:
            self.parse_list(args.input)

        if args.playlist:
            self.download_playlist(args.playlist)


if __name__ == '__main__':
    app = Splitr()

    parser = argparse.ArgumentParser()
    mgroup = parser.add_mutually_exclusive_group(required=True)

    mgroup.add_argument('-v', '--video',
                        type=str,
                        metavar='X',
                        help='download a single video')

    mgroup.add_argument('-i', '--input',
                        type=str,
                        metavar='X',
                        help='download a list of videos')

    mgroup.add_argument('-p', '--playlist',
                        type=str,
                        metavar='X',
                        help='download a playlist')
    
    parser.add_argument('-s', '--split',
                        action='store_true',
                        required=False,
                        help='split video into images')

    parser.add_argument('-k', '--keep',
                        action='store_true',
                        required=False,
                        help="don't clean up after")
    
    parser.add_argument('-w', '--writethumb',
                        action='store_true',
                        required=False,
                        help="download thumbnail")

    parser.add_argument('-r', '--resize',
                        action='store_true',
                        required=False,
                        help='resise to 1920x1080')
    app.run(parser.parse_args())
