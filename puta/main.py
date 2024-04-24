#!/usr/bin/env python
from putacore import PutaCore


class Puta(PutaCore):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            self.install_game()
            self.graceful_exit()


if __name__ == "__main__":
    app=Puta()
    app.run()
