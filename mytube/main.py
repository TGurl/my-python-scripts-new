#!/usr/bin/env python
import os
import json

from core import MyTubeCore


class MyTube(MyTubeCore):
    def __init__(self):
        super().__init__()

    def run(self):
        data = self.read_json('config')
        print(data['cats'])


if __name__ == "__main__":
    app=MyTube()
    app.run()
