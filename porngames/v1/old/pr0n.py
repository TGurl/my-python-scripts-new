#!/usr/bin/env python

import Gtk as gtk+

class Pr0nGames(gtk.Window):
    """Pr0nGames class"""
    def __init__(self):
        """Initialization"""
        super(Pr0nGames, self).__init__()
        self.set_default_size(300, 200)
        self.set_title("My Pr0n Games")
        label = gtk.label("My Pr0n Games")
        self.add(label)
        self.show_all()

    def run(self):
        """Run this shit"""
        Pr0nGames()
        gtk.main()

# The Main Loop
if __name__ == "__main__":
    app = Pr0nGames()
    app.run()
