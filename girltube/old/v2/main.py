#!/usr/bin/env python
import os
import sys
import json

from utils import TransgirlUtils
from pytube import Channel, YouTube
from time import sleep


class Girlytube(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.config = os.path.expanduser(os.path.join('~', '.config', 'transgirl', 'girlytube.json'))
        self.appname = 'GirlyTube'
        self.appwidth = 65
        self.waittime = 5

    def banner(self, slogan=True):
        self.show_title(appname=self.appname, width=self.appwidth)
        if slogan:
            self.cprint(self.random_slogan(), width=self.appwidth, new_line=True)

    def show_help(self):
        self.banner()
        self.printr('%wGirlyTube%R is a simple app to watch YouTube videos. You can select')
        self.printr('a channel to watch and this app will do the rest. There is basically')
        self.printr('just one option for you to remember.', new_line=True)
        self.printr('%wOptions:%R')
        self.printr('    -a    Add a YouTube channel')
        self.printr('    -h    Show this friendly help')
        sys.exit()

    def load_config(self):
        with open(self.config, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

    def save_config(self, data):
        with open(self.config, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)

    def select_channel(self):
        from pyfzf.pyfzf import FzfPrompt
        data = self.load_config()
        channels = []
        for item in data['channel']:
            channels.append(item['title'])
        channels.sort()
        result = FzfPrompt().prompt(channels, '--reverse --exact')
        if not result:
            self.exit_gracefully()
            sys.exit()

        curl = ''
        for item in data['channel']:
            if result[0] == item['title']:
                curl = item['channel_url']
        return curl

    def check_if_url_in_database(self, curl):
        data = self.load_config()
        checklist = []
        for item in data['channel']:
            checklist.append(item['channel_url'])
        return True if curl in checklist else False

    def add_channel(self):
        data = self.load_config()
        while True:
            self.banner()
            self.printr('You are about to add a YouTube channel. Please give us the')
            self.printr('the channel url and we will do the rest. Just leave it empty')
            self.printr('to exit and enter the world of YouTube.', new_line=True)
            try:
                channel_url = input('URL : ')
                print()
            except KeyboardInterrupt:
                self.exit_gracefully()
                sys.exit()

            if not channel_url:
                break

            if not 'videos' in channel_url:
                channel_url += '/videos'

            if self.check_if_url_in_database(channel_url):
                self.error_message(f"{channel_url} already exists in database...", exit_app=False)
                self.default_message("Please try another one.")
                sleep(2)
            else:
                cinfo = Channel(channel_url)
                channel_title = cinfo.channel_name
                self.default_message(f"Adding : {channel_title}")
                data['channel'].append({'title': channel_title, 'channel_url': channel_url})
                self.save_config(data)
                sleep(2)
        self.banner()
        self.printr("You have added new urls to %wGirlytube%R. Now you can restart the")
        self.printr("app and watch some videos.")
        sys.exit()

    def view_videos(self):
        self.banner()
        self.default_message('Collecting all information...')

        curl = self.select_channel()
        try:
            cinfo = Channel(curl)
        except:
            self.banner()
            self.error_message('Connection error.', exit_app=False)
            sys.exit()

        ctitle = cinfo.channel_name
        cvideos = list(cinfo.video_urls)
        cvideos.reverse()
        total = len(cvideos)
        indent = len(str(total))

        for vidx, video_url in enumerate(cvideos, start=1):
            vinfo = YouTube(video_url)
            vtitle = self.shorten_string(vinfo.title, width=self.appwidth - 15)
            short_url = self.shorten_string(video_url, width=self.appwidth - 15)

            self.banner()
            self.default_message(f"Channel title : {ctitle}")
            self.default_message(f"Total videos  : {total}")
            self.default_message(f"Showing video : {vidx:{indent}}")
            self.default_message(f"Video url     : {short_url}")
            self.default_message(f"Video title   : {vtitle}", new_line=True)

            os.system(f"mpv -fs --volume=90 --really-quiet {video_url}")

            self.wait_for_x_seconds(f"Waiting for {self.waittime} seconds....", seconds=self.waittime)

    def exit_gracefully(self):
        self.banner()
        self.default_message('Thanks for playing! ;)')

    def run(self, args):
        os.system('clear')
        if '-h' in args:
            self.show_help()
        elif '-a' in args:
            self.add_channel()
        else:
            try:
                self.view_videos()
            except KeyboardInterrupt:
                self.exit_gracefully()
                sys.exit()


if __name__ == '__main__':
    args = []
    if len(sys.argv) > 1:
        args = sys.argv[1:]

    app = Girlytube()
    app.run(args)
