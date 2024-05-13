#!/usr/bin/env python
import os

from lifeplaycore import LifePlayCore


class LifePlay(LifePlayCore):
    def __init__(self):
        super().__init__()

    def run(self):
        self.splashscreen()
        os.system('clear')

if __name__ == "__main__":
    app=LifePlay()
    app.run()
