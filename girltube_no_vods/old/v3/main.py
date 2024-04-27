#!/usr/bin/env python
import os
import sys
import json

from pytube import Channel, YouTube
from utils import TransgirlUtils
from pyfzf.pyfzf import FzfPrompt
from time import sleep
from shutil import copy2


class Girlytube(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.config = os.path.expanduser(os.path.join("~", ".config", "transgirl", "girlytube.json"))

    def show_help(self):
        self.banner()
        self.cprint(self.random_slogan(), new_line=True, width=65)
        self.printr("%wGirlyTube%R is a simple app that enables you to watch your favorite")
        self.printr("channels without having to use a browser.", new_line=True)
        self.printr("%wUsage%R:")
        self.printr("    girlytube <option>", new_line=True)
        self.printr("%wOptions%R:")
        self.printr("    -a    add a new channel")
        self.printr("    -b    create a backup of the database")
        self.printr("    -h    show this friendly help")
        sys.exit()

    def load_config(self):
        with open(self.config, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

    def save_config(self, data):
        with open(self.config, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)

    def banner(self, appname='GirlyTube', appwidth=65):
        self.show_title(appname=appname, width=appwidth)

    def choose_channel(self):
        fzf = FzfPrompt()
        data = self.load_config()

        channel_names = []
        for channel in data['channel']:
            channel_names.append(channel['title'])
        channel_names.sort()

        channel = fzf.prompt(channel_names, '--reverse --exact')
        if not channel:
            self.banner()
            self.error_message('You did not choose a channel.')
            sys.exit()

        cidx = 9999
        for idx, channel_info in enumerate(data['channel']):
            if channel[0] == channel_info['title']:
                cidx = idx

        if cidx == 9999:
            self.error_message('Channel not found...')
        else:
            curl = data['channel'][cidx]['channel_url']
            return curl

    def watch_videos(self, channel):
        self.banner()
        self.warning_message('Gathering information...')
        c_info = Channel(channel)
        v_urls = list(c_info.video_urls)
        v_urls.reverse()
        c_name = c_info.channel_name
        total = len(v_urls)
        indent = len(str(total))

        wait = False
        for idx, url in enumerate(v_urls, start=1):
            if wait:
                self.banner()
                self.default_message('You can press CTRL+C now to stop watching videos')
                self.warning_message('Waiting for 5 seconds...', dot='>>')
                sleep(5)

            v_info = YouTube(url)
            v_title = self.shorten_string(v_info.title, width=55)
            self.banner()
            self.default_message(f"Channel name  : {c_name}")
            self.default_message(f"Playing video : {idx:{indent}}/{total}")
            self.default_message(f"Video title   : {v_title}", new_line=True)
            self.warning_message("Starting playback...", dot='>>')
            os.system(f"mpv --fs --really-quiet {url}")
            wait = True

    def add_channel(self):
        data = self.load_config()

        while True:
            self.banner()
            self.cprint("%wAdd a new channel%R", width=65, new_line=True)
            self.printr("Here you can add a new channel to our database. Please enter the")
            self.printr("YouTube url and we will do the rest. Just leave empty to stop.", new_line=True)
            msg = self.colorize('%g>>%R URL : ')
            url = input(msg)
            if url == '':
                break

            if not 'videos' in url:
                url += "/videos"

            found=False
            for channel_info in data['channel']:
                if url == channel_info['channel_url']:
                    found = True

            if found:
                self.banner()
                self.warning_message("That channel was found in our database.")
                sleep(1.5)
            else:
                cinfo = Channel(url)
                c_name = cinfo.channel_name
                self.banner()
                self.default_message(f'Channel name : {c_name}')
                self.default_message(f"The channel has been added to our database.")
                data['channel'].append({'title': c_name, 'channel_url': url})
                self.save_config(data)
                sleep(1.5)

        self.banner()
        self.printr('Have fun watching the videos. ;)')
        sys.exit()


    def run(self, args):
        os.system('clear')
        if '-h' in args:
            self.show_help()

        if '-a' in args:
            self.add_channel()
            sys.exit()

        if '-b' in args:
            backup = self.config + "_"
            copy2(self.config, backup)
            self.banner()
            self.default_message('Database backup created.')
            sys.exit()

        try:
            channel = self.choose_channel()
            self.watch_videos(channel)
        except KeyboardInterrupt:
            self.banner()
            self.default_message("Video playback stopped.")


if __name__ == '__main__':
    app = Girlytube()
    args = sys.argv[1:]
    app.run(args)
