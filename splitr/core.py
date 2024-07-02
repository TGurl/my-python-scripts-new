import os
import sys
import shlex
import shutil
import random

from time import sleep
from colors import Colors
from subprocess import call
from urllib.parse import urlparse


class Core:
    def __init__(self, args):
        self.set_variables(args)

    # ------------------------------------------------------------------------
    # -- Set some important variables
    # ------------------------------------------------------------------------
    def set_variables(self, args):
        self.input = args.input
        self.output = args.output
        self.webp = args.google
        self.watch = args.watch
        self.split = args.split
        self.delete = args.delete
        self.clean = args.clean
        self.quiet = not args.verbose
        self.image_folder = 'images'
        self.video_folder = 'videos'
        self.video_filename = ''
        self.video_extension = ''
        self.domain = ''
        self.line = ''
        self.youtube = False
        self.width = 79

    # ------------------------------------------------------------------------
    # -- Video downloader
    # ------------------------------------------------------------------------
    def video_downloader(self):
        if not self.check_if_file_exists():
            insta = ' --cookies-from-browser chrome' if self.check_if_instagram() else ''
            opts = ' -q --progress --no-warnings -i' if self.quiet else ''

            output = os.path.join(self.video_folder, self.video_filename)
            cmd = f"yt-dlp{opts}{insta} -i {self.input} -o {output}"
        
            self.fprint('Downloading video', '')
            self.run(cmd)
            if self.quiet:
                self.clearlines()
            self.fprint('Downloading video', 'done')
        else:
            self.fprint(f'The video exists', 'skipping download')

    # ------------------------------------------------------------------------
    # -- Video player
    # ------------------------------------------------------------------------
    def video_player(self):
        if self.watch:
            self.fprint('Showing video', '')
            video = os.path.join(self.video_folder, self.video_filename)
            opts = '--really-quiet --volume=90' if self.quiet else '--volume=100'
            opts += ' --geometry=800x450'
            cmd = f"mpv {opts} {video}"
            self.run(cmd)
            if self.quiet:
                self.clearlines()
            self.fprint('Showing video', 'done')

    # ------------------------------------------------------------------------
    # -- Split video into images
    # ------------------------------------------------------------------------
    def split_video(self):
        if self.split:
            self.fprint('Splitting video', '')

            _, ext = os.path.splitext(self.video_filename)
            basename = self.video_filename.replace(ext, '')
            input = os.path.join(self.video_folder, self.video_filename)
            template = f"{basename}%04d.{self.set_image_type()}"
            output = os.path.join(self.image_folder, basename, template)
            
            if os.path.exists(os.path.join(self.image_folder, basename)):
                shutil.rmtree(os.path.join(self.image_folder, basename))

            opt1 = '-hide_banner -loglevel error -stats' if self.quiet else ''
            opt2 = '-c:v libwebp' if self.webp else ''
            cmd = f"ffmpeg -y {opt1} -i {input} -vf fps=1 {opt2} {output}"

            if not os.path.exists(os.path.join(self.image_folder, basename)):
                os.mkdir(os.path.join(self.image_folder, basename))
            else:
                shutil.rmtree(os.path.join(self.image_folder, basename))

            self.run(cmd)

            if self.quiet:
                self.clearlines(num=2)
            self.fprint('Splitting video', 'done')

    def finished(self):
        if self.delete:
            self.fprint('Deleting video', '')
            os.remove(os.path.join(self.video_folder, self.video_filename))
            self.clearlines()
            self.fprint('Deleting video', 'done')

    # ------------------------------------------------------------------------
    # -- Small helper functions
    # ------------------------------------------------------------------------
    def clean_workspace(self):
        if self.clean:
            prompt = f"%r>> This will delete everything! <<\nAre you sure?(y,%gN%r)%R "
            while True:
                answer = input(self.colorize(prompt))
                if answer in ['y', 'yes', 'n', 'no', '']:
                    break
                else:
                    self.print('%g~ Please answer the question with either y or N')
                    sleep(1.2)
                    self.clearlines(num=2)

            if answer in ['y', 'yes']:
                shutil.rmtree(self.image_folder)
                shutil.rmtree(self.video_folder)
                self.banner()
                self.print("%y~ Cleaned up workspace.")
                self.print('%y~ You can start fresh now.')
                sys.exit()
            else:
                self.print('Okay, then....')
                self.print('You can restart splitr now.')
                sys.exit()

    def run(self, cmd):
        call(shlex.split(cmd))

    def preflight_checks(self):
        self.check_terminal_width()

        if not self.input and not self.output:
            self.print(f"%rERROR%R : This is not the response you are looking for.")
            sys.exit()
        
        if not self.input:
            self.print(f"%rERROR%R : No url to download!")
            sys.exit()

        if not self.output:
            self.print(f"%rERROR%R : No filename to save video as!")
            sys.exit()

        folders = [self.image_folder, self.video_folder]
        for folder in folders:
            if not os.path.exists(folder):
                os.mkdir(folder)

    def check_terminal_width(self):
        if os.get_terminal_size().columns < self.width:
            w = self.width
            self.width = 46
            self.banner()
            self.print(f"%ySplitr%R needs at least %b{w}%R columns to function.")
            self.print("Please enlarge your terminal window.")
            sys.exit()

    def check_if_file_exists(self):
        path = os.path.join(self.video_folder, self.video_filename)
        return os.path.exists(path)

    def get_download_location(self):
        self.domain = urlparse(self.input).netloc
    
    def check_if_youtube(self):
        if 'youtube.com' in self.input.lower():
            self.video_extension = '.webm'
        else:
            self.video_extension = '.mp4'

    def check_if_instagram(self):
        return 'instagram.com' in self.input.lower()

    def set_image_type(self):
        return 'webp' if self.webp else 'png'

    def set_video_filename(self):
        self.video_filename = self.output + self.video_extension

    def slogan(self):
        slogans = ['Happy fapping!',
                   'Go suck a BBC!',
                   'Get raped!',
                   'Sucky, sucky. Five dollars!',
                   "I'm just a dumb slut!",
                   'Wanna get fucked?',
                   'Show me your boobs!',
                   "You are a horny bitch, aren't you?",
                   "I'm gonna sell you for 10 dollars!",
                   "You're daddy's little whore now!",
                   "Did you like it when daddy fucked you?"]
        return random.choice(slogans)

    # ------------------------------------------------------------------------
    # -- Simple TUI functions
    # ------------------------------------------------------------------------
    def colorize(self, string):
        for color in Colors.colors:
            string = string.replace(color[0], color[1])
        return string

    def print(self, string, cr=False):
        end = '\n\n' if cr else '\n'
        print(self.colorize(string), end=end)

    def fprint(self, key, value, fmt='%g~ %y{:21}%R : %c{}%R'):
        self.print(fmt.format(key, value))

    def clearlines(self, num=1):
        for _ in range(num):
            print('\033[1A', end='\x1b[2K')

    def drawline(self):
        self.print(f"%g{self.width * '~'}%R")

    def banner(self):
        call('clear')
        title = '%g~ %bSplitr%g an easy way to download videos%R'
        self.drawline()
        self.print(title)
        self.drawline()
