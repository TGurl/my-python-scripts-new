#!/usr/bin/env python3
""" CR is a simple app to watch their YouTube streams """
import sys
import shlex
import requests

from subprocess import call

# ---------------------------------------------------------------------------
# ---------------------------------------------------------- class mightynein
# ---------------------------------------------------------------------------
class MightyNein:
    def __init__(self):
        self.hd = False
        self.fs = False
        self.hs = False
        self.sm = False
        self.pname = ''
        self.playlists = [
            ('Vox Machina', 'PL1tiwbzkOjQz7D0l_eLJGAISVtcL7oRu_'),
            ('The Mighty Nein', 'PL1tiwbzkOjQxD0jjAE7PsWoaCrs0EkBH2'),
            ('Bells Hells', 'PL1tiwbzkOjQydg3QOkBLG9OYqWJ0dwlxF'),
            ('Candela Obscura', 'PL1tiwbzkOjQwrPBNkPgQEQtNVDvJwrqTm')
        ]

    def check_internet(self):
        try:
            res = requests.get('https://www.google.com', timeout=5)
            connected = res.status_code == 200
        except requests.ConnectionError:
            connected = False
        if not connected:
            self.mprint("So sorry, but it seems there is no connection to")
            self.mprint('the internet. Please try again later...')
            sys.exit()

        
    def colorize(self, string, remove=False):
        for color in Colors.colors:
            repl = '' if remove else color[1]
            string = string.replace(color[0], repl)
        return string

    def mprint(self, string, cr=False):
        end = '\n\n' if cr else '\n'
        print(self.colorize(string), end=end)

    def fprint(self, key, value, fmt='    {:<5} {}', cr=False):
        self.mprint(fmt.format(key, value), cr=cr)

    def show_help(self):
        call('clear')
        self.mprint(" %cTransgirl %bpresents %yCritical Role%R", cr=True)
        self.mprint(f' %cUsage%R: {self.pname} [vm|m9|bh|co] -hd [-fs|-sm]', cr=True)
        self.mprint(' %cOptions%R:')
        self.fprint('vm', 'Vox Machina')
        self.fprint('m9', 'The Mighty Nein (default)')
        self.fprint('bh', 'Bells Hells')
        self.fprint('co', 'Candela Obscura', cr=True)
        self.mprint(' %cFlags%R:')
        self.fprint('-fs', 'Show fullscreen')
        self.fprint('-hs', 'Use 800x450 window')
        self.fprint('-sm', 'Use 400x225 window')
        self.fprint('-hd', 'Use HD Streams')
        sys.exit()


    def start_streaming(self, idx):
        stream_title = self.playlists[idx][0]
        stream_id = self.playlists[idx][1]

        opts = '-hwdec --slang=en --really-quiet'
        opts += ' --fs' if self.fs else ''
        opts += ' --ytdl-format=bestvideo+bestaudio/best' if self.hd else ''
        opts += ' --geometry="400x225"' if self.sm else ''
        opts += ' --geometry="800x450"' if self.hs else ''

        yturl = 'https://www.youtube.com/playlist?list='
        yturl += stream_id
        cmd = f"mpv {opts} {yturl}"
        fmt = " {:<13}: {}"
        if self.hs:
            sz = "800x450"
        elif self.sm:
            sz = "400x225"
        else:
            sz = "1600x900"
        
        if self.fs:
            sz = 'Fullscreen'

        self.mprint(' %c~~~~~~~~~~~~~~~~~~~~~%R')
        self.mprint(' %c~   %bCritical Role   %c~%R')
        self.mprint(' %c~~~~~~~~~~~~~~~~~~~~~%R')
        self.fprint('Streaming', stream_title, fmt=fmt)
        self.fprint('HD', self.hd, fmt=fmt)
        self.fprint('Screensize', sz, fmt=fmt, cr=True)

        self.mprint(f' %b> %cConnecting to %yYou%rTube%c...%R')
        # prompt = self.colorize(f' %b> %cConnecting to %yYou%rTube%c...%R')
        # print(prompt, end='', flush=True)
        call(shlex.split(cmd))
        # print('\n')


    def main(self, args):
        self.check_internet()
        args = list(map(str.lower, args))
        self.pname, *args = args

        if '-h' in args:
            self.show_help()
            
        if '-hd' in args:
            self.hd = True
            args.remove('-hd')

        if '-fs' in args and '-sm' in args and '-hs' in args:
            self.mprint("Sorry, you can't use -fs, -sm  and -hs at the same time.")
        elif '-fs' in args:
            self.fs = True
            args.remove('-fs')
        elif '-sm' in args:
            self.sm = True
            args.remove('-sm')
        elif '-hs' in args:
            self.hs = True
            args.remove('-hs')

        options = ['vm', 'm9', 'bh', 'co']
        found = False
        for idx, option in enumerate(options):
            if option in args:
                found = True
                self.start_streaming(idx)

        if not found:
            self.start_streaming(1)


# ---------------------------------------------------------------------------
# -------------------------------------------------------------- class colors
# ---------------------------------------------------------------------------
class Colors:
    reset  = "\x1b[0m"
    black  = "\x1b[0;30;40m"
    red    = "\x1b[0;31;40m"
    green  = "\x1b[0;32;40m"
    yellow = "\x1b[0;33;40m"
    blue   = "\x1b[0;34;40m"
    purple = "\x1b[0;35;40m"
    cyan   = "\x1b[0;36;40m"
    white  = "\x1b[0;37;40m"
    gray   = "\x1b[0;37;0m"
    italic = "\x1B[3m"

    colors = [
            ('%R', reset),
            ('%B', black),
            ('%G', gray),
            ('%r', red),
            ('%g', green),
            ('%y', yellow),
            ('%p', purple),
            ('%b', blue),
            ('%c', cyan),
            ('%w', white),
            ('%i', italic)
    ]

# ---------------------------------------------------------------------------
# ----------------------------------------------------------------- main loop
# ---------------------------------------------------------------------------
# ----------------------------------------------------------------- main loop
if __name__ == '__main__':
    app = MightyNein()
    app.main(sys.argv)
