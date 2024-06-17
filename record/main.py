#!/usr/bin/env python

from core import Core

class RecordMyDesktop(Core):
    def __init__(self):
        super().__init__()

    def main(self):
        self.main_loop()


if __name__ == '__main__':
    app = RecordMyDesktop()
    app.main()

