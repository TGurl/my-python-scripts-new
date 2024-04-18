#!/usr/bin/env python
# --------------------------------------------- #
#  An easy way to download YouTube thumbnails   #
#  and transform them into wallpapers.          #
# --------------------------------------------- #
# Todo list:                                    #
#   - create main skeleton structure            #
#   - add download thumbbal function            #
#   - add transform into wallpaper function     #
#   - add move wallpapers to walls/nfsw/youtube #
# --------------------------------------------- #

# --------------------------------------------- imports
import os
import shutil
import sys

from time import sleep
from utils import TransgirlUtils
from pytube import YouTube
from PIL import Image

# --------------------------------------------- thumbr class
class Thumbr(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.debug = False
        self.random_filenames = False
        self.created_wallpapers = False
        self.parsing_list = False
        self.move_to_wallpapers = False
        self.appname = 'Thumbr'
        self.appwidth = 65

    def show_help(self):
        self.show_title(appname=self.appname, width=self.appwidth)
        self.cprint(self.random_slogan(), width=self.appwidth, new_line=True)

        self.printr('%wThumbr%R is a simple app to help you download thumbnails from')
        self.printr('YouTube. The use of this app is rather simple. You can either')
        self.printr('use an individual YouTube url or a list of urls in a simple')
        self.printr('textfile.', new_line=True)
        self.printr('Usage:')
        self.printr('    thumbr [options] -v <YouTube url>')
        self.printr('    thumbr [options] -i <textfile>', new_line=True)
        self.printr('Options:')
        self.printr('    -w  Create wallpapers from thumbnails')
        self.printr('    -m  Move wallpapers to correct folder when done')
        self.printr('    -c  Clean up once all is done')
        self.printr('    -h  Show this friendly help', new_line=True)
        sys.exit()

    def show_exit_message(self):
        self.show_title(appname=self.appname, width=self.appwidth)
        self.cprint(self.random_slogan(), width=self.appwidth, new_line=True)
        if self.created_wallpapers:
            self.default_message('Your wallpapers have been stored in the %iwallpapers%R folder.')
            self.default_message('Maybe check them using %wGiMP%R.')
            self.default_message('Just an idea.')
        else:
            self.default_message('The thumbnail(s) have been downloaded into the %ithumbs%R folder.')
            self.default_message('You could have converted them to wallpapers with the %w-w%R option.')
            self.default_message('Just a suggestion.')
        sys.exit()

    def cleanup_at_isle_three(self):
        for folder in ['thumbs', 'wallpapers']:
            if os.path.exists(folder):
                shutil.rmtree(folder)

    def move_wallpapers(self):
        destination = os.path.join("/", "data", "pictures", "walls", "nsfw", "youtube")

        for item in os.scandir('wallpapers'):
            self.show_title(appname=self.appname, width=self.appwidth)
            _, ext = os.path.splitext(item.name)
            if ext == ".jpg":
                self.default_message(f"Moving %i{item.name}%R to YouTube wallpapers.")
                shutil.move(item.path, destination)
                sleep(1.2)

    def convert_thumbs_to_wallpapers(self):
        self.created_wallpapers = True
        if not os.path.exists('wallpapers'):
            os.mkdir('wallpapers')

        thumbs = []
        for entry in os.scandir('thumbs'):
            if os.path.isfile(entry.path):
                thumbs.append(entry.path)
        total = len(thumbs)
        indent = len(str(total))

        if not total:
            self.show_title(appname=self.appname, width=self.appwidth)
            self.error_message('No thumbnails downloaded...')

        for idx, entry in enumerate(thumbs, start=1):

            self.show_title(appname=self.appname, width=self.appwidth)
            self.default_message(f"Converting : {entry}")
            self.default_message(f"Counter    : {idx:{indent}}/{total}")
            tfile, _ = os.path.splitext(entry)
            wallpaper = os.path.join('wallpapers', tfile.split('/')[-1] + '.jpg')

            img = Image.open(entry)
            w_width = 1920
            w_percent = w_width / float(img.size[0])
            w_height = int((float(img.size[1]) * float(w_percent)))
            img = img.resize((w_width, w_height), Image.Resampling.LANCZOS)
            img.save(wallpaper)
            sleep(0.6)

        # -- now that we've created the wallpapers we can delete
        # -- the thumbs folder.
        if os.path.exists('thumbs'):
            shutil.rmtree('thumbs')

        # -- if selected move the wallpapers
        if self.move_to_wallpapers:
            self.move_wallpapers()

    def fetch_thumbnail_extension(self, youtube_url):
        self.warning_message('Fetching info from YouTube...', dot='>>')
        tempdir = self.generate_random_string()
        ext = ''
        os.mkdir(tempdir)
        random_filename = self.generate_random_string()
        ytdlp = "yt-dlp --no-warnings --write-thumbnail --quiet "
        ytdlp += f"--skip-download -o '{tempdir}/{random_filename}.%(ext)s' {youtube_url}"
        os.system(ytdlp)
        for entry in os.scandir(tempdir):
            _, ext = os.path.splitext(entry.name)
        shutil.rmtree(tempdir)
        self.clear_lines()
        return ext

    def download_thumbnail(self, youtube_url=''):
        if not os.path.exists('thumbs'):
            os.mkdir('thumbs')

        if 'youtube.com' not in youtube_url:
            self.error_message('Not a YouTube url, skipping...', exit_app=False)
            sleep(1.5)
        else:
            short_url = self.shorten_string(youtube_url, width=self.appwidth - 15)
            self.default_message(f"YouTube url  : {short_url}")

            info = YouTube(youtube_url)
            whore_name = info.author

            if not self.parsing_list:
                self.show_title(appname=self.appname, width=self.appwidth)

            if not whore_name:
                filename = self.generate_random_string()
            else:
                filename = whore_name.replace(' ', '_') + "-" + self.generate_random_string(length=5)

            ext = self.fetch_thumbnail_extension(youtube_url)

            self.default_message(f"Channel name : {whore_name}")
            self.default_message(f"Saving as    : {filename}{ext}")

            ytdlp = "yt-dlp --no-warnings --progress --write-thumbnail --quiet "
            ytdlp += f"--skip-download -o 'thumbs/{filename}.%(ext)s' {youtube_url}"

            if self.debug:
                print(ytdlp)
                _ = input('...')
            else:
                os.system(ytdlp)

    def parse_list(self, filename=''):
        self.parsing_list = True
        if not os.path.exists(filename) or filename == '':
            self.show_title(appname=self.appname, width=self.appwidth)
            self.error_message('No filename given or file does not exist.')

        list_of_videos = self.read_file(filename)
        total = len(list_of_videos)
        indent = len(str(total))

        for uidx, url in enumerate(list_of_videos, start=1):
            self.show_title(appname=self.appname, width=self.appwidth)
            self.default_message(f"Parsing      : {filename}")
            self.default_message(f"Counter      : {uidx:{indent}}/{total}")
            self.download_thumbnail(url)

    def run(self, arguments):
        if not arguments or '-h' in arguments:
            self.show_help()

        if '-d' in arguments:
            self.debug = True

        if '-m' in arguments:
            self.move_to_wallpapers = True

        if '-c' in arguments:
            self.cleanup_at_isle_three()

        if '-i' in arguments and '-v' in arguments:
            self.show_title(appname=self.appname, width=self.appwidth)
            self.error_message('You cannot use -i and -v at the same time.')

        if '-i' in arguments:
            idx = arguments.index('-i') + 1
            self.parse_list(filename=arguments[idx])

        if '-v' in arguments and not self.parsing_list:
            idx = arguments.index('-v') + 1
            self.download_thumbnail(youtube_url=arguments[idx])

        if '-w' in arguments:
            self.convert_thumbs_to_wallpapers()

        self.show_exit_message()

# --------------------------------------------- main loop
if __name__ == "__main__":
    args = []
    if len(sys.argv) > 1:
        args = sys.argv[1:]

    app = Thumbr()
    app.run(args)
