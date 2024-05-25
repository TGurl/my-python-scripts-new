import os

from utils import TransgirlUtils
from time import sleep


class PutaCore(TransgirlUtils):
    def __init__(self):
        super().__init__()
        self.usb_folder = os.path.join('/', 'USB', 'sexgames')
        self.lore_folder = os.path.join('/', 'lore', 'sexgames')

    def add_a_game(self, folder, to_usb: bool = False) -> None:
        # -- check if folder exists
        if not os.path.exists(folder):
            self.error(f"{folder} not found.")

        destination = self.usb_folder if to_usb else self.lore_folder
        self.clear_saves(folder)
        archive = self.zipit(folder)
        self.move_file(archive, destination)
