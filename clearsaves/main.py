#!/usr/bin/env python
from utils import Core


class ClearSaves(Core):
    def __init__(self):
        super().__init__()

    def main(self):
        self.mprint("%yClearsaves v3 - Transgirl 2024%R")
        self.clear_save_files()
        self.clear_cache_files()
        self.clear_dist_files()


if __name__ == '__main__':
    app = ClearSaves()
    app.main()
