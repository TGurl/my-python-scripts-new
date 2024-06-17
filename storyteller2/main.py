#!/usr/bin/env python
from core import Core

class StoryTeller(Core):
    def __init__(self):
        super().__init__()

    def run(self):
        self.select_story()


if __name__ == '__main__':
    app = StoryTeller()
    app.run()
