#!/usr/bin/env python
import os
import sys
import argparse

from pytube import Playlist

class YoutubeDL:
    def __init__(self, args):
        self.playlist = args.input

    def banner(self):
        os.system('clear')
        print("┌─────────────────────────────┐")
        print("│        YouTube Lister       │")
        print("│    Copyleft 2024 Transgirl  │")
        print("└─────────────────────────────┘")

    def message(self, msg):
        print(f"-> {msg}")

    def error(self, msg, exit=True):
        self.message(msg)
        if exit:
            sys.exit()

    def run(self):
        playlist = Playlist(self.playlist)
        total_videos = len(playlist)

        with open('list', 'w') as file:
            self.banner()
            self.message(f"Channel name : {playlist.title}")
            self.message(f"Total videos : {total_videos}")

            for url in playlist.video_urls:
                file.write(f"{url}\n")

            self.message("Download list created!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Playlist to download')
    
    app = YoutubeDL(parser.parse_args())
    app.run()
