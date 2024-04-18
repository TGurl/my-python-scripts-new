#!/usr/bin/env python
import os
import argparse
import cv2
import datetime

def collect(folder='.'):
    files = []
    allowed = ['.webm', '.mkv', '.ogv']
    for item in os.scandir(folder):
        _, extension = os.path.splitext(item.name)
        if os.path.isfile(item.name) and extension in allowed:
            files.append(item.name)
    files.sort()
    return files

def format_td(seconds, digits=2):
    isec, fsec = divmod(round(seconds*10**digits), 10**digits)
    return f'{datetime.timedelta(seconds=isec)}.{fsec:0{digits}.0f}'

def get_duration(video):
    data = cv2.VideoCapture(video)
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = data.get(cv2.CAP_PROP_FPS)
    seconds = frames / fps
    video_time = format_td(seconds)
    return seconds, video_time

def remove_spaces():
    files = collect()
    for item in files:
        newname = item.replace(' ', '')
        os.rename(item, newname)

def main(args):
    remove_spaces()
    files = collect()
    total = len(files)
    for idx, item in enumerate(files, start=1):
        os.system('clear')
        dur_seconds, dur_time = get_duration(item)
        dur_time = str(dur_time)
        _, extension = os.path.splitext(item)
        mp4 = item.replace(extension, ".mp4")
        ffmpeg = f"ffmpeg -y -hide_banner -loglevel error -stats "
        ffmpeg += f"-i {item} -crf 0 -c:v libx264 {mp4}"
        print(f"Converting {idx}/{total}")
        print(f"Original    : {item}")
        print(f"Destination : {mp4}")
        print("Codec       : libx264")
        print(f"Duration    : {dur_time} ({dur_seconds:.2f} seconds)")
        os.system(ffmpeg)
        if not args.keep:
            os.remove(item)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-k', '--keep',
                        action='store_true',
                        required=False,
                        help='Keep the originals')
    main(parser.parse_args())
