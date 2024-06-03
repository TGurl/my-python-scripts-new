import os

from utils import Utils


class bibleCore(Utils):
    def __init__(self):
        super().__init__()

    def banner(self):
        os.system('clear')
        self.boxit('Study the Bible')
