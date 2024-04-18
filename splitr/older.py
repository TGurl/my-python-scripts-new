#!/usr/bin/env python
import os
import sys
import shutil
import argparse
import readchar

from utils import TransgirlUtils
from time import sleep


class Splitr(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.download_folder = 'downloads'
        self.image_folder = 'images'
        self.keep_folder = 'keep'

    def clean_up_at_isle_seven(self):
        folders = [self.download_folder]
        for folder in folders:
            if os.path.exists(folder):
                shutil.rmtree(folder)

    def process_videos(self):
        if not os.path.exists(self.image_folder):
            os.mkdir(self.image_folder)

        data = self.collect_items_in_folder(self.download_folder)
        images_allowed = ['.png', '.jpg', '.jpeg']
        videos_allowed = ['.mp4', '.webm', '.avi']

        self.show_title(appname='Splitr', width=65)
        for item in data:
            _, ext = os.path.splitext(item[0])
            if ext in images_allowed and not item[1]:
                filename = item[0].split('/')[-1]
                target = os.path.join(self.image_folder, filename)
                shutil.move(item[0], target)

            if ext in videos_allowed and not item[1]:
                filename, ext = os.path.splitext(item[0])
                filename = filename.split('/')[-1]
                if ext in videos_allowed and not item[1]:
                    self.default_message(f"Processing : %i{item[0]}%R")
                    ffmpeg = f"ffmpeg -y -loglevel error -hide_banner -stats "
                    ffmpeg += f"-i {item[0]} -vf fps=1 {self.image_folder}/{filename}-%06d.jpg"
                    os.system(ffmpeg)

    def image_viewer(self):
        if not os.path.exists(self.keep_folder):
            os.mkdir(self.keep_folder)

        data = self.collect_items_in_folder(self.image_folder)
        msg = self.colorize("%g·%R Want to keep this image? (y/n/q)")

        os.system('clear')
        for image in data:
            if not image[1]:
                os.system(f"timg -U {image[0]}")
                print(msg, end='', flush=True)

                key = readchar.readchar().lower()

                if key == 'q':
                    sys.exit()
                elif key == 'y':
                    filename = image[0].split('/')[-1]
                    shutil.move(image[0], os.path.join(self.keep_folder, filename))
                elif key == 'n':
                    os.remove(image[0])
                else:
                    self.error_message('Wrong key, you slut!', exit_app=False)
                    sleep(1.2)

        self.show_title(appname='Splitr', width=65)
        self.default_message('All done.')

    def download_video(self, video_url):
        if not os.path.exists(self.download_folder):
            os.mkdir(self.download_folder)

        self.show_title(appname='Splitr', width=65)
        self.default_message(self.shorten_string(video_url, width=55), new_line=True)
        #self.drawline(width=65)

        filename = self.generate_random_string()
        ytdlp = f"yt-dlp --write-thumbnail --quiet --progress "
        ytdlp += f"-o '{self.download_folder}/{filename}.%(ext)s' {video_url}"

        self.default_message("System output:", dot=">")
        os.system(ytdlp)
        self.clear_lines()
        self.default_message("Video download complete.")

    def run(self, args):
        self.clean_up_at_isle_seven()

        if not args.video:
            self.show_title(appname='Splitr', width=65)
            self.error_message("You did not tell me which video to download.")

        if args.video:
            self.download_video(args.video)

        self.process_videos()
        self.image_viewer()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--video',
                        type=str,
                        metavar='X',
                        required=False,
                        help='download single video')

    app = Splitr()
    app.run(parser.parse_args())
