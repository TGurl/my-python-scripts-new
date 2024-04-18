#!/usr/bin/env python
import os
import sys
import shutil
import argparse

from utils import TransgirlUtils
from PIL import Image

class Thumbr(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.parse_list = False

    def cleanup_at_isle_nine(self):
        folders = ['thumbs', 'wallpapers']
        for folder in folders:
            if os.path.exists(folder):
                shutil.rmtree(folder)

    def thumbnailer(self, video_url, solo=True, overall_filename='', dot='·'):
        random_filename = False
        filename = overall_filename

        if not os.path.exists('thumbs'):
            os.mkdir('thumbs')

        if solo:
            self.show_title(appname='Thumbr', width=65)
            self.default_message("Leave the following question empty for a random filename.")
            question = self.colorize(f"%g{dot}%R Filename : ")
            filename = input(question)
            random_filename = True if filename == '' else False

        random_filename = True if overall_filename == '' else False

        if random_filename:
            filename = self.generate_random_string()

        if not random_filename and not solo:
            filename = overall_filename + "-" + self.generate_random_string(length=5) 

        filename = filename.replace(' ', '_')

        ytdlp = "yt-dlp --no-warnings --progress --write-thumbnail --quiet "
        ytdlp += f"--skip-download -o 'thumbs/{filename}.%(ext)s' {video_url}"
        short = self.shorten_string(video_url, width=45)
        self.default_message(f"Url       : {short}")
        self.default_message(f"Saving as : {filename}")
        os.system(ytdlp)

    def process_list(self, video_list, dot='·'):
        data = self.read_file(video_list)
        print(data)
        total = len(data)
        indent = len(str(total))
        
        self.show_title(appname='Thumbr', width=65)
        self.default_message("Leave the following question empty for a random filename.")
        question = self.colorize(f"%g{dot}%R Filename : ")
        overall_filename = input(question)
        if overall_filename == '':
            overall_filename = self.generate_random_string()

        for idx, entry in enumerate(data, start=1):
            self.show_title(appname='Thumbr', width=65)
            self.default_message(f"Parsing   : %i{video_list}%R")
            perc = idx * 100 // total
            self.default_message(f"Counter   : {idx:{indent}}/{total} [{perc:3}%]")
            self.thumbnailer(entry, solo=False, overall_filename=overall_filename)

    def create_wallpapers(self):
        if not os.path.exists('wallpapers'):
            os.mkdir('wallpapers')

        allowed = ['.png', '.jpg', '.jpeg', '.webp']
        images = []
        for entry in os.scandir('thumbs'):
            _, ext = os.path.splitext(entry.name)
            if ext in allowed:
                images.append(entry.name)
        images.sort()
        total = len(images)

        for idx, image in enumerate(images, start=1):
            perc = idx * 100 // total
            indent = len(str(perc))
            thumbpath = os.path.join('thumbs', image)
            filename, _ = os.path.splitext(image)
            wallpath = os.path.join('wallpapers', f"{filename}.jpg")
            target_width = 1920

            self.show_title(appname='Thumbr', width=65)
            self.default_message(f"Processing : {idx:{indent}}/{total} [{perc:3}%]")
            self.default_message(f"Image name : {thumbpath}")
            self.default_message(f"Saving as  : {wallpath}")

            img = Image.open(thumbpath)
            wpercent = target_width / float(img.size[0])
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((target_width, hsize), Image.Resampling.LANCZOS)
            img.save(wallpath)

    def run(self, args):
        self.cleanup_at_isle_nine()

        if args.input:
            self.parse_list = True
            self.process_list(args.input)

        if args.video and not self.parse_list:
            self.thumbnailer(args.video)

        if args.wallpaper:
            self.create_wallpapers()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-v', '--video',
                       type=str,
                       metavar='X',
                       help='video to thumbnail')

    group.add_argument('-i', '--input',
                       type=str,
                       metavar='X',
                       help='list of videos')

    parser.add_argument('-w', '--wallpaper',
                        action='store_true',
                        required=False,
                        help='convert to wallpaper')

    app = Thumbr()
    app.run(parser.parse_args())
