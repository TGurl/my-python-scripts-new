#!/usr/bin/env python
import os
import re
import sys
import shutil
import argparse
import subprocess

from utils import TransgirlUtils
from pytube import YouTube


class Downloader(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.appname = 'dler'
        self.appwidth = 55
        self.download_folder = 'downloaded'
        self.screenshot_folder = 'screenshots'
        self.keep_folder = 'keep'
        self.video_length = 0
        self.split_video = False

    def cleanup_first(self):
        if os.path.exists(self.download_folder):
            shutil.rmtree(self.download_folder)
        if os.path.exists(self.screenshot_folder):
            shutil.rmtree(self.screenshot_folder)
        if os.path.exists(self.keep_folder):
            shutil.rmtree(self.keep_folder)

    def determine_video_type(self, video_url):
        self.default_message('Fetching info...')
        ytdlp = f"yt-dlp --no-warnings --print filename --skip-download -o '%(ext)s' {video_url}"
        result = subprocess.getoutput(ytdlp).strip()
        cr = 0
        if '\n' in result:
            cr = result.index('\n')
        if cr:
            result = result[:cr]
        self.clear_lines()
        return result

    def download_video(self, video_url, from_list=False, list_count=0, list_total=0):
        if not os.path.exists(self.download_folder):
            os.mkdir(self.download_folder)

        self.banner(appname=self.appname, width=self.appwidth)
        if from_list:
            self.default_message(f"Counter  : {list_count}/{list_total}")

        extension = self.determine_video_type(video_url)
        max_width = self.appwidth - 11
        local_filename = self.generate_random_string()
        url = self.shorten_string(video_url, width=max_width)

        if 'youtube.com' in video_url:
            video = YouTube(video_url)
            title = self.shorten_string(video.title, width=max_width)
            creator = self.shorten_string(video.author, width=max_width)
            self.video_length = self.convert_to_readable_time(video.length)

            self.default_message("Platform : YouTube")
            self.default_message(f"Parsing  : {url}")
            self.default_message(f"Creator  : {creator}")
            self.default_message(f"Title    : {title}")
            self.default_message(f"Length   : {self.video_length}")
        else:
            self.default_message("Platform : Other")
            self.default_message(f"Parsing  : {url}")
        
        fullpath = os.path.join(self.download_folder, f"{local_filename}.{extension}")
        self.default_message(f"Local    : {local_filename}.{extension}")
        self.default_message('System output:')
        ytdlp = "yt-dlp --quiet --progress --write-thumbnail --no-warnings "
        ytdlp += f"-o '{fullpath}' {video_url.strip()}"
        os.system(ytdlp)
        self.clear_lines()
        self.default_message("Download : completed")

    def generate_screenshots(self):
        pass

    def image_viewer(self):
        pass

    def parse_url_list(self, filename):
        if not os.path.exists(filename):
            self.error_message(f"File %i{filename}%R does not exist")

        with open(filename, 'r', encoding='utf-8') as urllist:
            data = urllist.readlines()

        total = len(data)
        if not total:
            self.error_message(f"File %i{filename}%R does not contain any URI.")

        for idx, line in enumerate(data, start=1):
            video_url = line.strip()
            self.download_video(video_url, from_list=True, list_count=idx, list_total=total)

        if not self.split_video:
            self.banner(appname=self.appname, width=self.appwidth)
            self.default_message('All downloads completed.')
            sys.exit()

        self.generate_screenshots()
        self.image_viewer()

    def run(self, args):
        self.split_video = args.split

        if args.clean:
            self.cleanup_first()
        
        if args.video and args.input:
            self.banner(appname=self.appname, width=self.appwidth)
            self.error_message('You cannot issue -v and -i at the same time.')

        if args.video:
            self.download_video(args.video)

        if args.input:
            self.parse_url_list(args.input)

if __name__ == '__main__':
    app = Downloader()
    parser = argparse.ArgumentParser(
            prog='dler',
            epilog='I want to have b(.)(.)bs'
            )

    parser.add_argument('-v', '--video',
                        type=str,
                        metavar='X',
                        required=False,
                        help='video to download')

    parser.add_argument('-i', '--input',
                        type=str,
                        metavar='Y',
                        required=False,
                        help='use list of videos')

    parser.add_argument('-c', '--clean',
                        action='store_true',
                        required=False,
                        help='clean before start')

    parser.add_argument('-s', '--split',
                        action='store_true',
                        required=False,
                        help='split video to images')

    app.run(parser.parse_args())
