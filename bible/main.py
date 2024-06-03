#!/usr/bin/env python
from core import bibleCore

class bible(bibleCore):
    def __init__(self):
        super().__init__()

    def run(self):
        self.banner()
        self.read_bible()

if __name__ == "__main__":
    app=bible()
    app.run()
