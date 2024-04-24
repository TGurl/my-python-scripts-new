import os
import sys

from utils import TransgirlUtils
from pytube import Channel, Playlist
from pyfzf.pyfzf import FzfPrompt


class GirlTubeCore(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.base_dir = os.path.expanduser(
                os.path.join('~', '.local', 'share', 'transgirl', 'girltube'))
        self.youtube_urls = os.path.join(self.base_dir, 'girltube_urls.csv')
        self.lock_file = os.path.join(self.base_dir, 'girltube.lock')
        self.start_oldest = True
        self.continue_last = False

    def preflight_check(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)

    def lock_girltube(self):
        if not os.path.exists(self.lock_file):
            with open(self.lock_file, 'w', encoding='utf-8') as f:
                f.write('Want to get laid?')

    def unlock_girltube(self):
        if os.path.exists(self.lock_file):
            os.remove(self.lock_file)

    def check_lock(self):
        if os.path.exists(self.lock_file):
            self.girltube_banner(slogan=False)
            self.error_message('There already is an instance of %rGirlTube%R running...')
            sys.exit()

    def reverse_m3u_list(self, path):
        data = self.read_file(path)
        data.reverse()

        m3u_path = os.path.join(self.base_dir, 'playlist.m3u')
        with open(m3u_path, 'w', encoding='utf-8') as m3u:
            for url in data:
                m3u.write(url + '\n')

    def movie_player(self, m3u_list):
        self.default_message('Starting player...')
        if self.continue_last and not self.start_oldest:
            self.default_message('Starting with last video first...')
            self.reverse_m3u_list(m3u_list)

        cmd = f"mpv --really-quiet -loop-playlist --playlist={m3u_list} --volume=75"
        os.system(cmd)

        if self.continue_last and not self.start_oldest:
            self.reverse_m3u_list(m3u_list)

        self.clear_lines()

    def generate_initial_data(self):
        urls = ['https://www.youtube.com/@Excinderella,Excinderella TRY ON',
                 'https://www.youtube.com/@CelestRayanneMann,Celest Rayanne',
                 'https://www.youtube.com/@LouisaKhovanski,LouisaKhovanski']
        with open(self.youtube_urls, 'w', encoding='utf-8') as f:
            for url in urls:
                f.write(url + '\n')

    def import_data(self):
        if not os.path.exists(self.youtube_urls):
            self.generate_initial_data()
        return self.read_file(self.youtube_urls)

    def check_if_playlist(self, youtube_url):
        is_playlist = 'playlist?list=' in youtube_url
        return is_playlist

    def split_line(self, line) -> tuple:
        url, title = line.split(',')
        return title, url

    def generate_local_m3u(self, youtube_url):
        self.default_message(f'Fetching information from YouTube...')
        self.check_if_playlist(youtube_url)

        is_playlist = self.check_if_playlist(youtube_url)
        i = Playlist(youtube_url) if is_playlist else Channel(youtube_url)

        vods = list(i.video_urls)
        if self.start_oldest:
            vods.reverse()

        total = len(vods)
        indent = len(str(total))

        m3u_path = os.path.join(self.base_dir, 'playlist.m3u')
        with open(m3u_path, 'w', encoding='utf-8') as m3u:
            for uidx, url in enumerate(vods, start=1):
                self.default_message(f"Processing {uidx:{indent}}/{total} videos...")
                m3u.write(url + '\n')
                self.get_fucked(0.002)
                self.clear_lines()
        return m3u_path

    def girltube_banner(self, slogan=True):
        os.system('clear')
        self.show_title(appname='GirlTube', width=65)
        if slogan:
            self.cprint(self.random_slogan(), width=65, new_line=True)

    def delete_youtube_url(self):
        cmd = f"nvim {self.youtube_urls}"
        os.system(cmd)

    def add_youtube_url_to_db(self):
        while True:
            data = self.import_data()

            self.girltube_banner()
            self.printr('%wWelcome to %rGirlTube.%R Please enter the url you want to add.')
            self.printr('Just leave it empty to exit this menu.', new_line=True)
            prompt = self.colorize('%r>%g>%y>%R ')
            new_url = input(prompt)

            if new_url in ['', 'q', 'quit', 'Q', 'QUIT']:
                break

            if '/videos' in new_url:
                new_url = new_url.replace('/videos', '')

            found = False
            for line in data:
                _, url = self.split_line(line)
                if new_url == url:
                    found = True
                    break

            if found:
                self.error_message('That URL is already in the database.')
                self.get_fucked(seconds=1.8)
            else:
                self.default_message('Adding URL to database.')
                if self.check_if_playlist(new_url):
                    i = Playlist(new_url)
                    title = i.title
                else:
                    i = Channel(new_url)
                    title = i.channel_name

                line2add = f"{new_url},{title}\n"
                with open(self.youtube_urls, 'a', encoding='utf-8') as f:
                    f.write(line2add)

    def channel_switcher(self):
        while True:
            self.girltube_banner(slogan=False)

            if not self.continue_last:
                data = self.import_data()

                channel_list = []
                for line in data:
                    title, _ = self.split_line(line)
                    channel_list.append(title)
                channel_list.sort()

                the_chosen_one = FzfPrompt().prompt(channel_list, '--reverse --exact')

                if not the_chosen_one:
                    break

                youtube_url = ''
                for line in data:
                    title, url = self.split_line(line)
                    if title == the_chosen_one[0]:
                        youtube_url = url

                path = self.generate_local_m3u(youtube_url)
            else:
                self.default_message('Continuing last watched videos...')
                path = os.path.join(self.base_dir, 'playlist.m3u')
                if not os.path.exists(path):
                    self.clear_lines()
                    self.error_message("You didn't watch any videos yet, please do that first.")
                    sys.exit()

            self.movie_player(path)
            if self.continue_last:
                break

        self.girltube_banner()
        self.default_message('Was it exciting?')
