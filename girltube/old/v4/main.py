#!/usr/bin/env python
import os
import sys
import json
import shutil
import argparse

from utils import TransgirlUtils
from pytube import Channel, Playlist, YouTube
from pyfzf.pyfzf import FzfPrompt
from time import sleep


class GirlTube(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.data = []
        self.appname = 'GirlTube'
        self.appwidth = 67
        self.wait = 0
        self.config = os.path.expanduser(
                os.path.join("~", ".config", "transgirl", "girltube.json"))

    def init(self):
        self.data.append({'title': '', 'url': '', 'owner': ''})

    def load_config(self):
        if not os.path.exists(self.config):
            self.init()
            self.save_config()
        with open(self.config, 'r', encoding='utf-8') as jfile:
            data = json.load(jfile)
        return data

    def save_config(self):
        with open(self.config, 'w', encoding='utf-8') as jfile:
            json.dump(self.data, jfile)

    def banner(self, slogan=True):
        self.show_title(appname=self.appname, width=self.appwidth)
        if slogan:
            self.cprint(self.random_slogan(), width=self.appwidth, new_line=True)

    def wait_for_x_seconds(self, seconds=5):
        if self.wait:
            seconds = self.wait
        try:
            self.banner(slogan=False)
            msg = self.colorize(f'%y>>%R waiting for {seconds} seconds. Use CTRL+C to exit.')
            print(msg, end='', flush=True)
            sleep(seconds)
            print('')
        except KeyboardInterrupt:
            self.banner()
            self.printr(f"Thank for using %w{self.appname}%R!")
            sys.exit()

    def play_a_playlist(self, url):
        p = Playlist(url)

        for vurl in p.video_urls:
            self.banner(slogan=False)
            # short_url = self.shorten_string(url, width=50)
            # self.printr(f"Adding playlist : %y{short_url}%R")
            self.printr(f"Playlist title  : %y{p.title}%R")
            mpv = f"mpv --fs --really-quiet {vurl}"
            os.system(mpv)
            self.wait_for_x_seconds()

    def play_a_channel(self, url):
        if not 'videos' in url:
            url += '/videos'
        c = Channel(url)
        video_list = list(c.video_urls)
        video_list.reverse()
        total = len(video_list)
        indent = len(str(total))
        for cidx, curl in enumerate(video_list, start=1):
            self.banner(slogan=False)
            y = YouTube(curl)
            title = y.title
            if len(y.title) > 55:
                title = self.shorten_string(y.title, width=55)

            # short_url = self.shorten_string(url, width=50)
            self.printr(f"Channel title : %y{c.channel_name}%R")
            self.printr(f"Total videos  : %y{cidx:{indent}}/{total}%R")
            self.printr(f"Video title   : %y{title}%R")
            mpv = f"mpv --fs --really-quiet {curl}"
            os.system(mpv)
            self.wait_for_x_seconds(seconds=3)

    def add_a_playlist(self, url):
        p = Playlist(url)
        title = p.title
        owner = p.owner
        purl = p.playlist_url

        if len(title) > 55:
            title = self.shorten_string(title, width=55)
        
        self.banner(slogan=False)
        self.printr(f"Adding playist : %y{title}%R")
        self.printr(f"Playlist owner : %y{owner}%R", new_line=True)

        new = {'title': title, 'owner': owner, 'url': purl}
        self.data.append(new)

        self.printr(f"Playlist %y{title}%R added to database")
        self.save_config()
        sleep(1.5)

    def add_a_channel(self, url):
        c = Channel(url)
        title = c.channel_name
        curl = c.channel_url

        self.banner(slogan=False)
        #self.printr(f"Adding channel : %y{title}%R")

        found = False
        for entry in self.data:
            if title in entry['title']:
                found = True

        if not found:
            new = {'title': title, 'owner': '', 'url': curl}
            self.data.append(new)
            self.printr(f"Channel %y{title}%R added to database")
            self.save_config()
        else:
            self.printr(f"Channel %y{title}%R already existed in our database.")
        sleep(2.5)

    def add_from_youtube(self):
        while True:
            self.banner(slogan=False)
            self.printr(f'%w{self.appname}%R is a simple app to watch videos from %rYouTube%R. You can just')
            self.printr('choose a channel or a playlist and off you go without any hassle.', new_line=True)
            self.printr('In this section you can add either a playlist or a channel by simply')
            self.printr('entering the url to either of them.', new_line=True)
            self.printr('Just leave the url empty to exit.', new_line=True)
            prompt = self.colorize('%yURL >>%R ')
            url = input(prompt)

            # https://www.youtube.com/playlist?list=PLf7cBO2Vfd3X-NSnNNgUYw0KjQeMctbSI
            # https://www.youtube.com/@Crossdressing/videos

            if url == '' or url.lower() in ['q', 'quit']:
                break
            elif not 'youtube.com' in url:
                self.error_message('That is not a valid %rYouTube%R url!')
                sleep(1.5)
            elif 'playlist' in url:
                self.add_a_playlist(url)
            else:
                self.add_a_channel(url)

    def dispense_video_url(self, url):
        if 'playlist' in url:
            self.play_a_playlist(url)
        else:
            self.play_a_channel(url)

    def run(self, args):
        self.load_config()

        if args.seconds:
            self.wait = args.seconds

        if args.add:
            self.add_from_youtube()

        # self.choose_url()


if __name__ == '__main__':
    app = GirlTube()

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--seconds',
                        type=float,
                        metavar='X',
                        required=False,
                        help='change wait time between videos')

    parser.add_argument('-a', '--add',
                        action='store_true',
                        required=False,
                        help='add a playlist or channel')

    app.run(parser.parse_args())
