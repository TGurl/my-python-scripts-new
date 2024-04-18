#!/usr/bin/env python
import os
import shutil

from utils import TransgirlUtils


class ClearSaves(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.renpy_folder = os.path.expanduser(
                os.path.join('~', '.renpy')
                )
        self.exec_folder = os.path.expanduser(
                os.path.join('~', 'Downloads', 'Renpy')
                )
        self.mygames_folder = os.path.expanduser(
                os.path.join('~', 'Dev', 'renpy', 'my_games')
                )

    def clear_dists_cache(self):
        data = self.collect_items_in_folder(self.mygames_folder)

        folders_to_remove = []
        for item in data:
            if 'dists' in item[0] and item[1] == True:
                folders_to_remove.append(item[0])

        if not len(folders_to_remove):
            self.default_message("No compiled distributions found.")
            return
        
        for item in folders_to_remove:
                self.default_message(f"Removing %i{item}%R.")
                shutil.rmtree(item)

    def clear_exec_cache(self):
        data = self.collect_items_in_folder(self.exec_folder)
        folders_to_remove = []
        for item in data:
            if '-sdk' in item[0] and item[1] == True:
                folder = os.path.join(item[0], 'tmp')
                if os.path.exists(folder):
                    folders_to_remove.append(folder)

        if not folders_to_remove:
            self.default_message('No SDK cache found.')
            return

        for item in folders_to_remove:
            self.default_message(f"Removing %i{item}%R.")
            shutil.rmtree(item)

    def clear_renpy_folder(self):
        if os.path.exists(self.renpy_folder):
            self.default_message('Removing renpy game cache.')
            shutil.rmtree(self.renpy_folder)
        else:
            self.default_message('Renpy game cache already cleared.')

    def run(self):
        self.banner(appname='clearsaves', width=50)
        self.clear_exec_cache()
        self.clear_dists_cache()
        self.clear_renpy_folder()


if __name__ == "__main__":
    app = ClearSaves()
    app.run()
