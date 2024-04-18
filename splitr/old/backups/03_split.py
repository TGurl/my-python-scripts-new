#!/usr/bin/env python
import os
import sys
import shutil
import cv2
import datetime
import argparse


def clean():
    for item in os.scandir('.'):
        if os.path.isdir(item.name) and os.path.exists(item.name):
            shutil.rmtree(item.name)
    print("All clean now")
    sys.exit()

def collect():
    movies = []
    for item in os.scandir('.'):
        _, ext = os.path.splitext(item.name)
        if ext == '.mp4':
            movies.append(item.name)
    # movies.sort()
    return movies

def convert(movie):
    mp4 = movie.replace('webm', 'mp4')
    if not os.path.exists(mp4):
        ffmpeg = f"ffmpeg -y -hide_banner -loglevel error -stats -i {movie} {mp4}"
        os.system(ffmpeg)
    os.remove(movie)

def process(movie, folder, secs=1, png=False):
    ext = 'png' if png else 'jpg'
    # ffmpeg -i input.mp4 -vf fps=1 out%d.png
    ffmpeg = 'ffmpeg -y -hide_banner -loglevel error -stats '
    ffmpeg += f"-i {movie} -vf fps=1/{secs} {folder}/{folder}%04d.{ext}"
    os.system(ffmpeg)

def get_duration(movie):
    video = cv2.VideoCapture(movie)
    frame_rate = video.get(cv2.CAP_PROP_FPS)
    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    length = int(total_frames / frame_rate)
    duration = str(datetime.timedelta(seconds=length))
    return duration, int(total_frames)

def main(args):
    if args.clean:
        clean()
    movies = collect()
    total = len(movies)
    ext = 'png' if args.png else 'jpeg'
    for idx, item in enumerate(movies, start=1):
        duration, _ = get_duration(item)
        os.system('clear')
        print(f"Processing {idx}/{total}")
        print(f"Filename  : {item}")
        print(f"Duration  : {duration}")
        print(f"Saving as : {ext}")
        folder = item.split('.')[0]
        if not os.path.exists(folder):
            os.mkdir(folder)
        else:
            shutil.rmtree(folder)
            os.mkdir(folder)
        process(item, folder, secs=args.secs, png=args.png)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--secs',
                        type=int,
                        default=1,
                        required=False,
                        help='Take a shot every x seconds')

    parser.add_argument('-p', '--png',
                        action='store_true',
                        required=False,
                        help='Save images as png')
    
    parser.add_argument('-c', '--clean',
                        action='store_true',
                        required=False,
                        help='Clean this shit up')

    main(parser.parse_args())
