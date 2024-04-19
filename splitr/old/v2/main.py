#!/usr/bin/env python
# ------------------------------------------------------- #
# - Splitr - a simple script to download videos and split #
# -          them into individual images using ffmpeg.    #
# -          This is a reimagination of the original by   #
# -          Transgirl Coding Studios (TCS)               #
# ------------------------------------------------------- #

# -- imports
import os
import sys
import shutil
import argparse
import readchar

from utils import TransgirlUtils
from pytube import YouTube
from time import sleep

# -- class
class Splitr(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.download_folder = 'downloads'
        self.image_folder = 'images'
        self.keep_folder = 'keep'
        self.preview = False
        self.jpeg = False
        self.videos_allowed = ['.mp4', '.mkv', '.webm']
        self.thumbs_allowed = ['.png', '.jpg', '.jpeg', '.webp']

    def banner(self):
        self.show_title(appname='Splitr', width=65)

    def cleanup_at_isle_seven(self, keep=False):
        folders = [self.download_folder, self.image_folder]
        if not keep:
            folders.append(self.keep_folder)
        for folder in folders:
            if os.path.exists(folder):
                shutil.rmtree(folder)
    
    def execute(self, command):
        self.default_message('System output:', dot='>')
        os.system(command)

    def check_if_youtube(self, video_url):
        return 'youtube.com' in video_url

    def preview_video(self, video_url, from_list=False):
        if not from_list:
            self.banner()
        self.default_message("Starting preview...")
        mpv = f"mpv --really-quiet --no-terminal {video_url}"
        self.execute(mpv)
        self.clear_lines()

    def easy_downloader(self, video_url, from_list=False):
        if not os.path.exists(self.download_folder):
            os.mkdir(self.download_folder)

        if self.preview:
            self.preview_video(video_url, from_list=from_list)

        url = self.shorten_string(video_url, width=45)

        if not from_list:
            self.banner()
            self.default_message(f'Downloading  : {url}')

        if self.check_if_youtube(video_url):
            info = YouTube(video_url)
            self.default_message('Platform     : YouTube')
            self.default_message(f'Video title  : {info.title}')
            self.default_message(f'Channel name : {info.author}', new_line=True)
        else:
            self.default_message(f'Platform     : Other')
            self.default_message(f'No video info available', new_line=True)

        rstring = self.generate_random_string(length=4)
        msg = self.colorize("%g·%R Please enter a name for the video : ")
        istring = input(msg)
        filename = f"{istring}-{rstring}"

        self.default_message(f'Saving as    : {filename}')

        ytdlp = "yt-dlp --quiet --progress --no-warnings --write-thumb "
        ytdlp += f"-o '{self.download_folder}/{filename}.%(ext)s' {video_url}"
        self.execute(ytdlp)

    def parse_list(self, video_list):
        if not os.path.exists(video_list):
            self.banner()
            self.error_message(f"File %i{video_list}%R does not exist.")

        url_list = [line.rstrip() for line in open(video_list, 'r', encoding='utf-8')]
        total = len(url_list)

        for idx, url in enumerate(url_list, start=1):
            self.banner()
            if not url:
                continue

            percent = idx * 100 // total
            short = self.shorten_string(url, width=45)
            self.default_message(f"Parsing      : %i{video_list}%R")
            self.default_message(f"Url          : %i{short}%R")
            self.default_message(f"Counter      : {idx}/{total} [{percent:3}%]")
            self.easy_downloader(url, from_list=True)
        os.remove(video_list)
        self.default_message(f"Removed %i{video_list}%R.")

    def image_splitter(self):
        if not os.path.exists(self.image_folder):
            os.mkdir(self.image_folder)
        

        # -- move thumbnails to images folder
        for item in os.scandir(self.download_folder):
            _, ext = os.path.splitext(item.name)
            if ext in self.thumbs_allowed:
                destination = os.path.join(self.image_folder, item.name)
                shutil.move(item.path, destination)

        # -- collect all allowed videos into array
        videos = []
        for item in os.scandir(self.download_folder):
            _, ext = os.path.splitext(item.name)
            if ext in self.videos_allowed:
                videos.append(item.path)
        videos.sort()
        total = len(videos)

        # -- itterate over videos
        for idx, item in enumerate(videos, start=0):
            self.banner()
            self.default_message('Creating screenshots')
            percent = idx * 100 // total
            self.default_message(f"Processing : {idx}/{total} [{percent:3}%]")
            modelname, _ = os.path.splitext(item)
            modelname = modelname.split('/')[1]
            ext = 'jpg' if self.jpeg else 'png'
            destination = os.path.join(self.image_folder, f"{modelname}-%06d.{ext}")

            ffmpeg = "ffmpeg -y -hide_banner -loglevel error -stats "
            ffmpeg += f"-i {item} -vf fps=1 {destination}"
            self.execute(ffmpeg)

    def image_viewer(self):
        if not os.path.exists(self.keep_folder):
            os.mkdir(self.keep_folder)

        images = []
        for item in os.scandir(self.image_folder):
            _, ext = os.path.splitext(item.name)
            if ext in self.thumbs_allowed:
                images.append(item.path)
        images.sort()

        msg = self.colorize("%g·%R Do you want to keep this image? (y/n/q)")
        for idx, image in enumerate(images, start=1):
            os.system('clear')
            os.system(f"timg -U {image}")
            percent = idx * 100 // len(images)
            self.default_message(f"Showing {idx}/{len(images)} [{percent:3}%]")
            print(msg, end='', flush=True)
            key = readchar.readchar().lower()
            print('')
            if key not in 'ynq':
                self.default_message('Wrong key, girl...')
                sleep(1.5)
            elif key == 'y':
                filename = image.split('/')[1]
                destination = os.path.join(self.keep_folder, filename)
                shutil.move(image, destination)
            elif key == 'n':
                os.remove(image)
            else:
                self.banner()
                self.cleanup_at_isle_seven()
                self.default_message('Did you orgasm? You filthy slut, you.')
                sys.exit()

    def run(self, args):
        if args.clean:
            self.cleanup_at_isle_seven()

        from_list = False
        self.preview = args.preview
        self.jpeg = args.jpeg

        if args.input:
            from_list = True
            self.parse_list(args.input)

        if args.video and not from_list:
            self.easy_downloader(args.video)

        self.image_splitter()
        self.image_viewer()
        self.banner()
        self.cleanup_at_isle_seven(keep=True)
        self.default_message("You're done for the day.")
        self.default_message("Did you like servicing all those men? You whore.")
        sys.exit()


# -- main loop
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True, )

    group.add_argument('-v', '--video',
                        type=str,
                        metavar='X',
                        required=False,
                        help='url of video')

    group.add_argument('-i', '--input',
                        type=str,
                        metavar='X',
                        required=False,
                        help='list of videos')
    
    parser.add_argument('-p', '--preview',
                        action='store_true',
                        required=False,
                        help='preview video')

    parser.add_argument('-c', '--clean',
                        action='store_true',
                        required=False,
                        help='clean before start')

    parser.add_argument('-j', '--jpeg',
                        action='store_true',
                        required=False,
                        help='use jpeg images')
    
    app = Splitr()
    app.run(parser.parse_args())
