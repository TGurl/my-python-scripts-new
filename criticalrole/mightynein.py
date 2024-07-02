#!/usr/bin/env python

import os
import sys

class MightyNein:
    def __init__(self):
        self.hd = False
        self.fs = False

    def show_error(self):
        print("I didn't quite understand that.")
        print("Please try again.")
        exit()

    def run(self):
        MPVOPTIONS = "-hwdec --slang=en "
        notification = "Starting M9<--HD--><--FS-->"
        if self.fs:
             MPVOPTIONS += "--fs "
             notification = notification.replace("<--FS-->", " FS")
        else:
            notification = notification.replace("<--FS-->", "")

        if self.hd:
            notification = notification.replace("<--HD-->", " HD")
            MPVOPTIONS += "--ytdl-format=bestvideo+bestaudio/best"
            # MPVOPTIONS += "--ytdl-format=137+140 "
            # MPVOPTIONS += "--af=rubberband=pitch-scale=0.9818181818181"
        else:
            notification = notification.replace("<--HD-->", "")

        NOTIFY = f"notify-send -u low '{notification}'"

        PLAYLIST = "https://www.youtube.com/playlist?list="
        PLAYLIST += "PL1tiwbzkOjQxD0jjAE7PsWoaCrs0EkBH2"

        CMD = f"mpv {MPVOPTIONS} {PLAYLIST}"

        os.system(NOTIFY)
        os.system(CMD)


if __name__ == "__main__":
    m9 = MightyNein()

    if len(sys.argv) == 1:
        m9.run()
    else:
        for item in sys.argv:
            if item.lower() == "hd":
                m9.hd = True
            elif item.lower() == "fs":
                m9.fs = True
        m9.run()
