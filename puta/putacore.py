import os
import sys

from utils import TransgirlUtils
from pyfzf.pyfzf import FzfPrompt


class PutaCore(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.lore_folder = os.path.join("/", "lore", "sexgames")
        self.usb_folder = os.path.join("/", "USB", "sexgames")
        self.done_folder = os.path.join(self.lore_folder, "done")
        self.play_folder = os.path.join("/", "lore", "playing")
        self.sort = True
        self.store_to_usb = False

    # ------------------------------------------------------------------------
    # -------------------------------------------------------- Helpers section
    # ------------------------------------------------------------------------
    def puta_banner(self, slogan=True):
        os.system('clear')
        self.show_title(appname='Puta', width=65)
        if slogan:
            self.cprint(self.random_slogan(), width=65, new_line=True)

    def graceful_exit(self):
        self.puta_banner()
        self.default_message('Happy gaming!')
        sys.exit()

    def ask_for_another(self):
        pass

    # ------------------------------------------------------------------------
    # --------------------------------------------------- Install game section
    # ------------------------------------------------------------------------

    def collect_all_games(self, query='') -> list:
        all_games = []
        folders = [self.lore_folder, self.usb_folder, self.done_folder]
        for folder in folders:
            for item in os.scandir(folder):
                _, ext = os.path.splitext(item.name)
                if ext == '.zip' and query in item.path:
                    all_games.append(item.path)
        if self.sort:
            all_games.sort()
        return all_games

    def fuzzy_filewalker(self, query=''):
        data = self.collect_all_games(query=query)
        game = FzfPrompt().prompt(data, '--reverse --exact --multi')
        return game

    def process_files(self, game_list):
        self.default_message(f"Unzipping {len(game_list)} files.")
        for game in game_list:
            self.unzipper(game, self.play_folder)
            if len(game_list) > 1:
                self.get_fucked(seconds=1.5)

    def install_game(self, query=''):
        self.puta_banner()
        game_list = self.fuzzy_filewalker(query=query)
        self.process_files(game_list)

    # ------------------------------------------------------------------------
    # ------------------------------------------------------- Add game section
    # ------------------------------------------------------------------------
    def check_if_game_in_collection(self, archive):
        folders = [self.lore_folder, self.usb_folder, self.done_folder]
        found = False
        folder = ''
        for folder in folders:
            path = os.path.join(folder, archive)
            if os.path.exists(path):
                found = True
                break
        return found, folder

    def add_a_game(self, folder):
        self.puta_banner()
        archive = folder + '.zip'
        destination = self.usb_folder if self.store_to_usb else self.lore_folder
        found, path = self.check_if_game_in_collection(archive)
        if found and not self.always_yes:
            self.error_message(f"%i{archive}%R found in %i{path}%R. Use -y to remove it.")
            sys.exit()
        elif found:
            self.default_message(f"%i{archive}%R removed from %i{path}%R")
            os.remove(os.path.join(path, archive))

        self.zipper(folder)
        self.clear_lines()
        self.move_file_with_percentage(archive, os.path.join(destination, archive))
        sys.exit()

    # ------------------------------------------------------------------------
    # ---------------------------------------------------- Delete game section
    # ------------------------------------------------------------------------
    def delete_a_game(self):
        pass
