#!/usr/bin/env python
import sys

from fetchrcore import fetchrCore


class fetchr(fetchrCore):
    def __init__(self):
        super().__init__()

    def run(self, args):
        self.render_transflag()


if __name__ == "__main__":
    app=fetchr()
    app.run(sys.argv[1:])
