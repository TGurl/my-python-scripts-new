#!/usr/bin/env python
import os
import sys
import cv2
import argparse
import datetime
import shutil
import readchar

# from time import sleep


class Imgr:
    def __init__(self, args):
        self.keep = args.keep
        self.png = args.png
        self.convert = args.convert
        self.skipdownload = args.skipdownload
        self.playlist = args.listofurls

    def msg(self, message) -> None:
        print(message)

    def err(self, message, exit=True) -> None:
        print(f"{message}")
        if exit:
            sys.exit()

    def banner(self, clear_screen=True) -> None:
        if clear_screen:
            os.system('clear')

        print("┌──────────────────────────────┐")
        print("│ IMGr - Split video to images │")
        print("│   Copyright 2024 Transgirl   │")
        print("└──────────────────────────────┘")

    def format_td(self, seconds, digits=2):
        isec, fsec = divmod(round(seconds*10**digits), 10**digits)
        return f'{datetime.timedelta(seconds=isec)}.{fsec:0{digits}.0f}'

    def get_duration(self, video):
        data = cv2.VideoCapture(video)
        frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = data.get(cv2.CAP_PROP_FPS)
        seconds = frames / fps
        video_time = self.format_td(seconds)
        return seconds, video_time

    def remove_spaces(self):
        files = self.collect_videos()
        for item in files:
            newname = item.replace(' ', '')
            os.rename(item, newname)

    def move_folder(self, folder):
        if not os.path.exists(folder):
            self.err("Oops, {folder} doesn't seem to exist...")
        else:
            os.system('clear')
            self.msg(f"{folder} is done, moving to 'keep'...")
            destination = os.path.join("keep", folder)
            shutil.move(folder, destination)
            self.msg(f"Moving {folder} done.")

    def collect_images(self, folder) -> list:
        images = []
        extensions = ['.png', '.jpg']
        for item in os.scandir(folder):
            _, img_extension = os.path.splitext(item.name)
            if img_extension.lower() in extensions:
                images.append(item.path)
        images.sort()
        return images

    def collect_folders(self, folder='.') -> list:
        folders = []
        ignore_these = ['backups', 'keep']
        for item in os.scandir(folder):
            if os.path.isdir(item.path) and item.name.lower() not in ignore_these:
                folders.append(item.name)
        folders.sort()
        return folders

    def collect_videos(self, folder='.', mp4=False) -> list:
        videos = []
        if mp4:
            extensions = ['.mp4']
        else:
            extensions = ['.webm', '.ogv', '.mkv']

        for extension in extensions:
            for item in os.scandir(folder):
                _, video_extension = os.path.splitext(item.name)
                if os.path.isfile(item.path) and video_extension.lower() == extension.lower():
                    videos.append(item.name)

        videos.sort()
        return videos

    def youtube_downloader(self, video_list):
        total = len(video_list)
        for idx, item in enumerate(video_list):
            percent = (idx * 100) // total
            self.banner()
            self.msg(f"Downloading {idx}/{total} [{percent:3}%]")
            ytdl = f"yt-dlp -o '%(uploader)s-{idx:02}.%(ext)s' {item}"
            os.system(ytdl)
            
    def download_videos(self):
        dl_list = 'list' if not self.playlist else self.playlist

        if not os.path.exists(dl_list):
            self.banner()
            self.msg(f"File '{dl_list}' not found!")
            self.msg(f"Please create a list of video urls,")
            self.err(f"then restart this script.")
        else:
            lines = [line.rstrip() for line in open(dl_list, 'r')]
            self.youtube_downloader(lines)
   
    def conversion_therapy(self, video_list):
        total = len(video_list)
        for vid, video in enumerate(video_list):
            self.banner()
            dur_seconds, dur_time = self.get_duration(video)
            _, video_extension = os.path.splitext(video)
            mp4 = video.replace(video_extension, '.mp4')
            ffmpeg = "ffmpeg -y -hide_banner -loglevel error -stats "
            ffmpeg += f"-i {video} -crf 0 -c:v libx264 {mp4}"
            self.msg(f"Converting {vid} out of {total} videos")
            self.msg(f"Original    : {video}")
            self.msg(f"Destination : {mp4}")
            self.msg(f"Duration    : 0{dur_time} ({dur_seconds:.2f} seconds)")
            os.system(ffmpeg)
            if not self.keep:
                os.remove(video)

    def convert_to_mp4(self):
        videos = self.collect_videos()
        if len(videos):
            self.conversion_therapy(videos)
        else:
            self.err('No videos found.')
    
    def screengrab(self, video_list, secs=1):
        img_extension = 'png' if self.png else 'jpg'
        total = len(video_list)

        for idx, video in enumerate(video_list, start=1):
            _, duration = self.get_duration(video)
            folder = video.split('.')[0]
            if not os.path.exists(folder):
                os.mkdir(folder)

            self.banner()
            self.msg(f"Processing {idx} out of {total}")
            self.msg(f"Filename  : {video}")
            self.msg(f"Duration  : 0{duration}")
            self.msg(f"Saving as : {img_extension}")

            ffmpeg = 'ffmpeg -y -hide_banner -loglevel error -stats '
            ffmpeg += f"-i {video} -vf fps=1/{secs} {folder}/{folder}%04d.{img_extension}"
            os.system(ffmpeg)

            if not self.keep:
                os.remove(video)

    def split_video(self):
        videos = self.collect_videos(mp4=self.convert)
        if len(videos):
            self.screengrab(videos)
        else:
            self.err('No videos found.')

    def luke_filewalker(self, folders):
        msg = 'Keep this images? (y/n/q) '
        total_folders = len(folders)

        for fid, folder in enumerate(folders, start=1):
            images = self.collect_images(folder)
            total_images = len(images)

            for iid, image in enumerate(images, start=1):
                os.system('clear')
                timg = f"timg -g64x {image}"
                os.system(timg)

                f_name = folder.split('/')[-1]
                i_name = image.split('/')[-1]
                left = total_images - iid
                percent = (iid * 100) // total_images

                self.msg(f"Reading {fid} out of {total_folders}")
                self.msg(f"Filename : {f_name}")
                if left > 0:
                    self.msg(f"Images left {left} [{percent:3}% done]: {i_name}")
                else:
                    self.msg(f"And the last one [{percent:3}% done]: {i_name}")

                print(msg, end="", flush=True)
                key = readchar.readchar().lower()

                if key == 'y':
                    pass
                elif key == 'q':
                    print("")
                    self.banner()
                    print("Thank you for using IMGr")
                    sys.exit()
                else:
                    os.remove(image)
            
            self.move_folder(folder)

    def view_images(self):
        folders = self.collect_folders()
        if len(folders):
            self.luke_filewalker(folders)
        else:
            self.err('No folders found.')

    def run(self):
        if not self.skipdownload:
            self.download_videos()
        self.remove_spaces()
        if self.convert:
            self.convert_to_mp4()
        self.split_video()
        self.view_images()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--listofurls',
                        type=str,
                        required=False,
                        help='List of urls')

    parser.add_argument('-c', '--convert',
                        action='store_true',
                        required=False,
                        help='Convert to mp4')
    
    parser.add_argument('-k', '--keep',
                        action='store_true',
                        required=False,
                        help='Keep originals')

    parser.add_argument('-s', '--skipdownload',
                        action='store_true',
                        required=False,
                        help='Skip download')

    parser.add_argument('-p', '--png',
                         action='store_true',
                         required=False,
                         help='Save images as png')
    
    app = Imgr(parser.parse_args())
    app.run()
