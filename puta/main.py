#!/usr/bin/env python
# ------------------------------------------------------ #
# PUTA is a simple app to manage my pr0ngames. It allows #
# me to add, install or remove games from my collection. #
# ------------------------------------------------------ #
# TODO:                                                  #
#    - add install game                                  #
#    + add remove game afer install                      #
#    - add archive game                                  #
#    - add remove game                                   #
#    + add search function                               #
#    - add help screen
# ------------------------------------------------------ #

# ------------------------------------------------------ #
# Imports
# ------------------------------------------------------ #

import os
import shutil
import sys

from utils import TransgirlUtils
from pyfzf.pyfzf import FzfPrompt
from time import sleep

# ------------------------------------------------------ #
# Class PUTA
# ------------------------------------------------------ #
class Puta(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.appname = 'Puta'
        self.appwidth = 65
        self.lore_folder = "/lore/sexgames"
        self.usb_folder = "/USB/sexgames"
        self.done_folder = "/lore/sexgames/done"
        self.play_folder = "/lore/playing"
        self.remove_after_install = False
        self.store_to_usb = False

    def show_help(self):
        self.show_title(appname=self.appname, width=self.appwidth)
        self.cprint(self.random_slogan(), width=self.appwidth, new_line=True)
        self.printr("%wPuta%R is a simple app to manage my pr0ngame collection. There")
        self.printr("aren't many options to use this app. Just a few good ones.", new_line=True)
        self.printr("In order to install a game you don't need to issue any option at")
        self.printr("all.", new_line=True)
        self.printr("%wUsage%R:")
        self.printr("    puta [options]", new_line=True)
        self.printr("%wOptions%R:")
        self.printr("    -q <query>  search for a game")
        self.printr("    -a          add a game to the collection")
        self.printr("    -r          remove a game after install")
        self.printr("    -d          delete a game without installing")
        self.printr("    -f          move game to done folder")
        self.printr("    -h          show this friendly help message")
        sys.exit()

    def is_zip(self, path):
        return '.zip' in path

    def collect_all_games(self, query='') -> list:
        games = []
        folders = [self.lore_folder, self.usb_folder, self.done_folder]
        for folder in folders:
            for item in os.scandir(folder):
                if  query.lower() in item.path.lower() and self.is_zip(item.path):
                    games.append(item.path)
        games.sort()
        return games

    def fuzzy_searcher(self, data):
        fzf = FzfPrompt()
        return fzf.prompt(data, '--reverse --multi --exact')
    
    def check_if_already_installed(self, game):
        folder = game.replace('.zip', '')
        return os.path.exists(os.path.join(self.play_folder, folder))

    def move_to_done(self, query=''):
        all_games = self.collect_all_games(query=query)
        mygames = self.fuzzy_searcher(all_games)
        total = len(mygames)
        indent = len(str(total))
        
        if not total:
            self.show_title(appname=self.appname, width=self.appwidth)
            self.error_message('You did not select any games to move.')
        
        for idx, game in enumerate(mygames, start=1):
            self.show_title(appname=self.appname, width=self.appwidth)
            game_name = game.split('/')[-1]
            self.default_message(f"Moving {idx:{indent}}/{total} : {game_name}")
            destination = os.path.join(self.done_folder, game_name)
            self.move_file_with_percentage(game, destination)
        
        self.show_title(appname=self.appname, width=self.appwidth)
        gstring = 'games' if total != 1 else 'game'
        self.default_message(f"Finished moving {total} {gstring}")
        sys.exit()

    def delete_games(self, query=''):
        all_games = self.collect_all_games(query=query)
        mygames = self.fuzzy_searcher(all_games)
        total = len(mygames)
        indent = len(str(total))

        total_removed = 0
        if not total:
            self.show_title(appname=self.appname, width=self.appwidth)
            self.error_message('You did not select any games to remove.')

        for idx, game in enumerate(mygames, start=1):
            self.show_title(appname=self.appname, width=self.appwidth)
            game_name = game.split('/')[-1]
            self.default_message(f"Removing {idx:{indent}}/{total} : {game_name}")
            total_removed += os.stat(game).st_size
            os.remove(game)
            sleep(1.2)

        self.show_title(appname=self.appname, width=self.appwidth)
        gstring = 'games' if total != 1 else 'game'
        self.default_message(f"Finished deleting {total} {gstring}")
        self.default_message(f"Freed up {self.convert_size(total_removed)} disk space.")
        sys.exit()

    def install_a_game(self, query=''):
        all_games = self.collect_all_games(query=query)
        mygames = self.fuzzy_searcher(all_games)
        total = len(mygames)
        indent = len(str(total))

        if not total:
            self.show_title(appname=self.appname, width=self.appwidth)
            self.error_message('You did not select any games to install.')

        for idx, game in enumerate(mygames, start=1):
            self.show_title(appname=self.appname, width=self.appwidth)
            game_name = game.split('/')[-1]
            if self.check_if_already_installed(game_name):
                self.default_message(f"{game_name} has been installed already.")
                sleep(1.5)
                continue

            game_name = self.shorten_string(game_name, width=self.appwidth - 20)
            self.default_message(f"Installing : {game_name}")
            if total > 1:
                self.default_message(f"Counter    : {idx:{indent}}/{total}")
            self.unzipper(game, self.play_folder)
            if self.remove_after_install:
                self.default_message(f'Removing   : {game_name}')
                os.remove(game)

        self.show_title(appname=self.appname, width=self.appwidth)
        gstring = 'games' if total != 1 else 'game'
        self.default_message(f"Finished installing {total} {gstring}")
        sys.exit()

    def check_if_already_archived(self, arc_name):
        print('Entering check_if_already_archived', arc_name)
        # folders = [self.lore_folder, self.usb_folder, self.done_folder]
        all_games = self.collect_all_games()
        found = False
        idx = 9999
        for gidx, game in enumerate(all_games):
            if arc_name.lower() in game.lower():
                idx = gidx
                found = True
                break
        
        return all_games[idx] if found else ''

    def add_game_to_collection(self, folder):
        if not os.path.exists(folder):
            self.show_title(appname=self.appname, width=self.appwidth)
            self.error_message(f"Can't find {folder}.")

        dest_folder = self.usb_folder if self.store_to_usb else self.lore_folder
        free_space = shutil.disk_usage(dest_folder).free
        total_space = shutil.disk_usage(dest_folder).total
        perc_free = free_space * 100 // total_space
        free_space_string = self.convert_size(free_space)
        arc_name = folder + ".zip"
        # destination = os.path.join(dest_folder, arc_name)
        check = self.check_if_already_archived(arc_name)

        if check != '':
            cfolder = check.replace('/' + arc_name, '')
            self.show_title(appname=self.appname, width=self.appwidth)
            self.error_message(f"{arc_name} already exists in {cfolder}.")
            answer = self.ask_yes_no('Do you want me to delete it?')
            if answer:
                os.remove(os.path.join(cfolder, arc_name))
                self.default_message(f"{arc_name} removed from collection")
                sleep(1.5)

        #if os.path.exists(destination):
        #    self.show_title(appname=self.appname, width=self.appwidth)
        #    self.error_message(f"{arc_name} already exists in {dest_folder}.\n ")


        self.show_title(appname=self.appname, width=self.appwidth)
        self.default_message(f"Free space {free_space_string} [{perc_free:3}%].")
        self.zipper(folder)
        self.default_message(f"Removed source folder.")
        shutil.rmtree(folder)
        if os.stat(arc_name).st_size > free_space:
            self.show_title(appname=self.appname, width=self.appwidth)
            self.error_message(f"There is not enough space left on {dest_folder}.\n ")

        self.move_file_with_percentage(arc_name, os.path.join(dest_folder, arc_name))
        self.clear_lines()
        self.default_message('Syncing to make sure everything has been moved...')
        os.system('sync')
        self.clear_lines()
        self.default_message("All done.")
        sys.exit()

    def run(self, args):
        query = ''
        if '-h' in args:
            self.show_help()

        if '-q' in args:
            query = args[args.index('-q') + 1]
        
        if '-u' in args:
            self.store_to_usb = True

        if '-a' in args and '-d' in args and '-f' in args:
            self.show_title(appname=self.appname, width=self.appwidth)
            self.error_message("You cannot use -a, -d and -f at the same time.")

        if '-a' in args:
            folder = args[args.index('-a') + 1]
            self.add_game_to_collection(folder)

        if '-d' in args:
            self.delete_games(query=query)

        if '-f' in args:
            self.move_to_done(query=query)

        if '-r' in args:
            self.remove_after_install = True

        self.install_a_game(query=query)


# ------------------------------------------------------ #
# Main loop to enable app
# ------------------------------------------------------ #
if __name__ == '__main__':
    app = Puta()
    app.run(sys.argv[1:])
