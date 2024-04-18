#!/usr/bin/env python
import os
import sys
import json
import subprocess
import argparse

from utils import TransgirlUtils
from pyfzf.pyfzf import FzfPrompt


class Girltube(TransgirlUtils):
    def __init__(self):
        super().__init__()
        config_path = os.path.join('~', '.config', 'transgirl', 'girlytube.json')
        self.channel_list = os.path.expanduser(config_path)

    def load_config(self):
        with open(self.channel_list, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

    def save_config(self, data):
        with open(self.channel_list, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)

    def timeout(self, message, seconds=4):
        self.default_message(message)
        subprocess.call(f'read -t {seconds}', shell=True)
    
    def channel_chooser(self):
        data = self.load_config()
        fzf = FzfPrompt()
        channels = []
        for item in data['channel']:
            channels.append(item['title'])
        channels.sort()
        result = fzf.prompt(channels, '--reverse --exact')
        if not result:
            self.show_title(appname='Girltube', width=65)
            self.error_message('No channel chosen.')
        channel_url = ''
        for item in data['channel']:
            if item['title'] == result[0]:
                channel_url = item['channel_url']
        return channel_url

    def watch_channel(self, url):
        from pytube import Channel, YouTube
        c = Channel(url)
        print(c.channel_name)
        for vurl in c.video_urls:
            self.show_title(appname='Girltube', width=65)
            i = YouTube(vurl)
            self.default_message(f"Channel : {c.channel_name}")
            self.default_message(f"Showing : {self.shorten_string(i.title, width=45)}")
            os.system(f"mpv --fs --volume=90 --really-quiet {vurl}")
            self.timeout("Press CTRL+C to stop. Waiting for 4 seconds...")

    def add_a_channel(self, dot='·'):
        data = self.load_config()
        self.show_title(appname='Girltube', width=65)
        self.default_message('Add a new channel.')
        msg = self.colorize(f"%g{dot}%R Channel name : ")
        name = input(msg)
        msg = self.colorize(f"%g{dot}%R Channel url  : ")
        url = input(msg)
        data['channel'].append({ "title": name, "channel_url": url})
        self.save_config(data)

    def run(self, args):
        os.system('clear')
        if args.add:
            self.add_a_channel()

        try:
            url = self.channel_chooser()
            self.watch_channel(url)
        except KeyboardInterrupt:
            self.show_title(appname='Girltube', width=65)
            self.default_message("Showing videos stopped.")
            try:
                sys.exit()
            except SystemExit:
                os._exit(0)
        


if __name__ == "__main__":
    app = Girltube()

    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--add',
                        action='store_true',
                        required=False,
                        help='add a channel')

    app.run(parser.parse_args())
