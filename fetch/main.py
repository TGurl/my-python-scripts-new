#!/usr/bin/env python
import os
import sys
import platform
import distro
import json
import psutil
import math

from colors import Colors
from random import choice


class Fetchr:
    def __init__(self):
        self.distro = ''
        self.kernel = ''
        self.cpu = ''
        self.memory = ''
        self.uptime = ''
        self.wallpaper = ''
        self.timeleft = ''

    def colorize(self, text, remove_colors=False) -> str:
        for color in Colors.colors:
            repl = '' if remove_colors else color[1]
            text = text.replace(color[0], repl)
        return text

    def printr(self, text) -> None:
        text = self.colorize(text)
        print(text)

    def cprint(self, text, width=30):
        temp = self.colorize(text, remove_colors=True)
        text = self.colorize(text)
        spaces = ((width - len(temp)) // 2) * ' '
        print(f"{spaces}{text}")
        del(temp)
    
    def banner(self, clear=True):
        if clear:
            os.system('clear')
        banner = [
                '┌────────────────────────────┐',
                '│    ╭━━╮   ╭╮╭╮╭╮           │',
                '│    ┃╭╮┣┳┳━┫╰┫┃┣╋━┳┳┳┳┳╮    │',
                '│    ┃┣┫┃╭┫━┫┃┃╰┫┃┃┃┃┃┣┃┫    │',
                '│    ╰╯╰┻╯╰━┻┻┻━┻┻┻━┻━┻┻╯    │',
                '└────────────────────────────┘'
                ]
        for line in banner:
            self.printr(f"%b{line}%R")

    def choose_slogan(self):
        slogans = ["Fuck me daddy!", "I <3 b(.)(.)bs", "I <3 BBC",
                   "I'm a K9 slut", "Life needs sex to live",
                   "Fucky, fucky! 5 dollars!", "Oh daddy, make me a mommy!",
                   "Careful daddy, I'm a virgin"]
        return choice(slogans)

    def get_current_wallpaper(self):
        if not os.path.exists('~/.config/transgirl/wallpaper.json'):
            return 'Unknown'
        
        with open('~/.config/transgirl/wallpaper.json') as file:
            data = json.load(file)
        return data['current']

    def get_wallpaper_time_left(self):
        if self.wallpaper == 'Unknown':
            return 'n/a'

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return '0B'
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def get_uptime(self):
        with open('/proc/uptime', 'r') as file:
            uptime = float(file.readline().split(maxsplit=1)[0])

        minutes, seconds = divmod(uptime, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        
        time_str = ''
        if days > 0:
            ext = 's' if days != 1 else ''
            time_str += f"{round(days)} day{ext}, "
        if hours > 0:
            time_str += f"{round(hours):02}:"
        if minutes > 0:
            time_str += f"{round(minutes):02}:"
        if seconds > 0:
            time_str += f"{round(seconds):02}"

        return time_str

    def collect_info(self):
        # mem_avail = self.convert_size(psutil.virtual_memory().available)
        # per_avail = psutil.virtual_memory().available * 100 // psutil.virtual_memory().total

        mem_total = psutil.virtual_memory().total
        mem_used = psutil.virtual_memory().used
        per_avail = mem_used * 100 // mem_total
    
        #v_memfree = self.convert_size(mem_used)
        #v_memtotal = self.convert_size(mem_total)

        self.distro = distro.name()
        self.kernel = platform.release()
        self.cpu = f"{round(psutil.cpu_percent())}% used"
        self.memory = f"{per_avail}% used"
        self.uptime = self.get_uptime()
        #self.wallpaper = self.get_current_wallpaper()
        #self.timeleft = self.get_wallpaper_time_left()


    def run(self):
        dot = '•'
        self.collect_info()
        self.banner()
        self.cprint(f"%i{self.choose_slogan()}%R")
        print()
        self.printr(f" %y{dot} %cDistro :%R {self.distro}")
        self.printr(f" %y{dot} %cKernel :%R {self.kernel}")
        self.printr(f" %y{dot} %cCPU    :%R {self.cpu}")
        self.printr(f" %y{dot} %cMemory :%R {self.memory}")
        self.printr(f" %y{dot} %cUptime :%R {self.uptime}")
        #self.printr(f" %y{dot} %cWallpaper :%R {self.wallpaper}")
        #self.printr(f" %y{dot} %cTime left :%R {self.timeleft}")
        print()
        sys.exit()


if __name__ == '__main__':
    app = Fetchr()
    app.run()
