#!/usr/bin/env python
import os
import re
import shutil
import argparse
import subprocess

from utils import TransgirlUtils
from time import sleep


class Downloader(TransgirlUtils):
    def __init__(self, args):
        super().__init__()
        self.init(args)

    def init(self, args):
        if args.input == 'NONE':
            self.error_message('No list supplied.')

        self.list_of_urls = args.input
        self.thumbnail = not args.nothumbnail
        self.dl_dir = 'downloaded'
        self.image_path = 'screenshots'
        self.keep_folder = 'keep'
        self.banner_width = 65
        self.split = args.split
        self.restart = args.restart
        self.debug = args.debug

    def wait_for_enter(self):
        if self.debug:
            _ = input('--ENTER--')

    def exit_app(self):
        self.banner(appname='DLer v6.0',clear_screen=True, width=self.banner_width)
        self.default_message('All done.')

    def cleanup(self):
        if os.path.exists(self.dl_dir):
            shutil.rmtree(self.dl_dir)

        if os.path.exists(self.image_path):
            shutil.rmtree(self.image_path)

        if os.path.exists(self.keep_folder):
            shutil.rmtree(self.keep_folder)

    def read_list(self):
        data = []
        with open(self.list_of_urls, 'r', encoding='utf-8') as file:
            data = file.readlines()
        return data

    def check_url(self, url):
        if not 'http://' in url and not 'https://' in url or 'ftp://' in url:
            self.error_message(f"{url} is not a valid URI.")
    
    def shorten(self, item):
        if len(item) > self.banner_width:
            left = ((self.banner_width - len(item)) // 2) - 4
            right = -1 * left
            item = item[:left] + '..' + item[right:]
        return item

    def rename_output_file(self, url):
        self.default_message('Detecting filename...')
        ytdlp = f"yt-dlp --no-warnings --quiet --progress --print filename {url}"
        output = subprocess.check_output(ytdlp, shell=True)
        output = output.decode("utf-8").strip()
        output = re.sub('\[.*?\]', '', output)
        output = output.replace('＂', '').replace(' ', '')
        self.clear_lines()
        return output.lower()

    def collect_videos(self):
        data = []
        allowed = ['.mkv', '.mp4', '.avi']
        for item in os.scandir(self.dl_dir):
            _, ext = os.path.splitext(item.name)
            if ext in allowed:
                data.append(item.path)
        data.sort()
        return data

    def split_into_images(self):
        if not os.path.exists(self.image_path):
            os.mkdir(self.image_path)

        videos = self.collect_videos()
        total = len(videos)
        
        for idx, item in enumerate(videos, start=1):
            self.banner(appname='DLer v6.0',clear_screen=True, width=self.banner_width)
            filename, _ = os.path.splitext(item)
            filename = filename.split('/')[-1]
            fullpath = os.path.join(self.image_path, filename)
            os.mkdir(fullpath)
            self.default_message(f"Splitting video {idx}/{total}.")
            self.default_message(f"Processing %i{item}%R")
            self.default_message("System output:")
            ffmpeg = "ffmpeg -y -hide_banner -loglevel error -stats "
            ffmpeg += f"-i {item} -vf fps=1 {fullpath}/%06d.png"
            os.system(ffmpeg)
            self.wait_for_enter()
    
    def collect_images(self):
        allowed = ['.png', '.jpg', '.jpeg']
        images = []
        for item in os.scandir(self.image_path):
            _, ext = os.path.splitext(item.name)
            if ext in allowed:
                images.append(item.path)
        images.sort()
        return images

    def view_images(self):
        if not os.path.exists(self.keep_folder):
            os.mkdir(self.keep_folder)
        images = self.collect_images()
        for image in images:
            os.system(f"timg -U {image}")
            answer = self.ask_yes_no("Do you want to keep this image?")
            if answer:
                folder = image.split('/')[-2]
                print(folder)
                self.wait_for_enter()
            else:
                pass

    def run(self):
        if self.restart:
            self.cleanup()

        if not os.path.exists(self.dl_dir):
            os.mkdir(self.dl_dir)

        data = self.read_list()
        if not data:
            self.banner(appname='DLer v6.0',clear_screen=True, width=self.banner_width)
            self.error_message(f'There are no urls listed in %i{self.list_of_urls}%R')

        total = len(data)
        for idx, item in enumerate(data):
            item = item.strip()
            percent = (idx * 100) // total
            self.banner(appname='DLer v6.0',clear_screen=True, width=self.banner_width)
            self.default_message(f"Downloading {idx + 1}/{total} URLs listed. ({percent:3}%)")
            self.check_url(item)
            filename = self.rename_output_file(item)
            fullpath = os.path.join(self.dl_dir, filename)

            if os.path.exists(fullpath):
                self.default_message(f"%i{filename}%R already exists.")
                sleep(1.8)
                continue

            ytdlp = "yt-dlp --no-warnings --quiet --progress"
            if self.thumbnail:
                ytdlp += " --write-thumbnail "
            ytdlp += f"-o {fullpath} {item}"
            display_item = self.shorten(item)
            self.default_message(f"URL   : %i{display_item}%R")
            self.default_message(f"Local : %i{filename}%R")
            self.default_message("System output:")
            os.system(ytdlp)

        if self.split:
            self.split_into_images()
            self.view_images()
        self.exit_app()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input',
                        type=str,
                        default='NONE',
                        required=False,
                        help='List of urls')

    parser.add_argument('-d', '--debug',
                        action='store_true',
                        required=False,
                        help='Enable debugging')

    parser.add_argument('-n', '--nothumbnail',
                        action='store_true',
                        required=False,
                        help='Do not write thumbnail')

    parser.add_argument('-s', '--split',
                        action='store_true',
                        required=False,
                        help='Split into images')

    parser.add_argument('-r', '--restart',
                        action='store_true',
                        required=False,
                        help='Restart process')

    app = Downloader(parser.parse_args())
    app.run()
