import os

from utils import Utils
from time import sleep


class LifePlayCore(Utils):
    def __init__(self):
        super().__init__()

    def splashscreen(self):
        os.system('clear')
        lines = ['','','','','','','','',
                '%y██%b╗     %y██%b╗%y███████%b╗%y███████%b╗%y██████%b╗ %y██%b╗      %y█████%b╗ %y██%b╗   %y██%b╗%R',
                 '%y██%b║     %y██%b║%y██%b╔════╝%y██%b╔════╝%y██%b╔══%y██%b╗%y██%b║     %y██%b╔══%y██%b╗╚%y██%b╗ %y██%b╔╝%R',
                 '%y██%b║     %y██%b║%y█████%b╗  %y█████%b╗  %y██████%b╔╝%y██%b║     %y███████%b║ ╚%y████%b╔╝%R ',
                 '%y██%b║     %y██%b║%y██%b╔══╝  %y██%b╔══╝  %y██%b╔═══╝ %y██%b║     %y██%b╔══%y██%b║  ╚%y██%b╔╝%R  ',
                 '%y███████%b╗%y██%b║%y██%b║     %y███████%b╗%y██%b║     %y███████%b╗%y██%b║  %y██%b║   %y██%b║   %R',
                 '%b╚══════╝╚═╝╚═╝     ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   %R',
                 'a simple game of life by',
                 '%pTransgirl%R']
        for line in lines:
            self.printr(line, center=True)
        sleep(4)
