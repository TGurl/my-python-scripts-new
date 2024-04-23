import os
import pickle

from colors import Colors
from pyfzf.pyfzf import FzfPrompt
from dataclasses import dataclass

@dataclass
class Config:
    configdir: str
    configfile: str
    wallpaperdir: str
    rootdir: str
    category: str
    current: str
    feh: bool
    random: bool
    sddm: bool

class Core:
    def __init__(self):
        self.fzf = FzfPrompt()
        self.__initialize()

    def __initialize(self):
        Config.configdir = os.path.expanduser(
                os.path.join("~", ".config", "wallpaper")
                )
        Config.configfile = os.path.join(Config.configdir, "config.pickle")
        Config.wallpaperdir = os.path.join("/", "data", "pictures", "walls")
        Config.rootdir = "nsfw"
        Config.category = "girls"
        Config.current = "girls-001.png"
        Config.feh = True
        Config.random = False
        Config.sddm = True

    def save_config(self):
        # --- convert dataclass to json
        config = {
                "configdir": Config.configdir,
                "configfile": Config.configfile,
                "wallpaperdir": Config.wallpaperdir,
                "rootdir": Config.rootdir,
                "category": Config.category,
                "current": Config.current,
                "feh": Config.feh,
                "random": Config.random,
                "sddm": Config.sddm
                }
        # --- check if configpath exists, if not create it
        if not os.path.exists(Config.configdir):
            print("Created config folder...")
            os.mkdir(Config.configdir)
        
        # --- store the configuration in a pickle file
        with open(Config.configfile, "wb") as handler:
            pickle.dump(config, handler)

    def read_config(self):
        # -- check if the path exists, if not return
        if not os.path.exists(Config.configfile):
            return

        # --- read the configuration from a pickle file
        with open(Config.configfile, "rb") as handler:
            config = pickle.load(handler)

        Config.configdir = config['configdir']
        Config.configfile = config['configfile']
        Config.wallpaperdir = config['wallpaperdir']
        Config.rootdir = config['rootdir']
        Config.category = config['category']
        Config.current = config['current']
        Config.random = config['random']
        Config.feh = config['feh']
        Config.sddm = config['sddm']

    def __collect_folders(self, workdir: str, ignorelist: list):
        folders = []
        for item in os.scandir(workdir):
            if item.is_dir() and item.name not in ignorelist:
                folders.append(item.name)
        folders.sort()
        return folders

    def __collect_wallpapers(self, workdir:str, ignorelist: list):
        image_list = []
        for item in os.scandir(workdir):
            if item.is_file() and item.name not in ignorelist:
                image_list.append(item.name)
        image_list.sort()
        return image_list

    def __colorize(self, message: str, remove_colors = False):
        for color in Colors.colors:
            replace = '' if remove_colors else color[1]
            message = message.replace(color[0], replace)
        return message

    def printf(self, message, new_line=False):
        newline = '\n\n' if new_line else '\n'
        message = self.__colorize(message)
        print(message, end=newline)

    def ask_yes_no(self, message, default_yes=True):
        prompt = "(Y/n)" if default_yes else "(y/N)"
        while True:
            answer = input(message + f"? {prompt} : ").lower()
            if answer in 'yn' or answer == '':
                break

        if answer == 'y' or default_yes:
            return True
        else:
            return False

    def show_info(self):
        os.system('clear')
        setter = "feh" if Config.feh else "nitrogen"
        current = os.path.join(Config.rootdir, Config.category, Config.current)
        self.printf('%y-= Wallpaper info =-%R')
        self.printf(f"Current    : {current}")
        self.printf(f"Setter     : {setter}")
        self.printf(f"Randomized : {Config.random}")
        self.printf(f"SDDM/GRUB  : {Config.sddm}")

    def select_wallpaper_setter(self):
        # Config.feh = self.ask_yes_no('Use feh as wallpaper setter')
        answer = self.ask_yes_no('Use feh as wallpaper setter')
        print("-->", answer)
        _ = input('[ENTER]')
        Config.feh = answer

    def toggle_randomize(self):
        Config.random = self.ask_yes_no('Randomize wallpapers', default_yes=False)

    def toggle_sddm_change(self):
        Config.sddm = self.ask_yes_no('Change SDDM/GRUB background')

    def select_root_dir(self):
        ignore_list = ['.git', 'downloads', 'keepers']
        folders = self.__collect_folders(Config.wallpaperdir, ignore_list)
        result = self.fzf.prompt(folders, '--reverse')
        Config.rootdir = result[0]

    def select_category(self):
        path = os.path.join(Config.wallpaperdir, Config.rootdir)
        ignore_list = ['removed']
        folders = self.__collect_folders(path, ignore_list)
        result = self.fzf.prompt(folders, '--reverse')
        Config.category = result[0]

    def set_wallpaper(self):
        path = os.path.join(Config.wallpaperdir, Config.rootdir, Config.category, Config.current)
        if Config.feh:
            command = f"feh --bg-scale {path}"
        else:
            command = f"nitrogen --set-scaled {path}"
        os.system(command)
    
    def select_wallpaper(self):
        path = os.path.join(Config.wallpaperdir, Config.rootdir, Config.category)
        ignorelist = ['README.md']
        wallpapers = self.__collect_wallpapers(path, ignorelist)
        result = self.fzf.prompt(wallpapers, '--reverse')
        Config.current = result[0]
        self.set_wallpaper()
    
    def next_wallpaper(self):
        path = os.path.join(Config.wallpaperdir, Config.rootdir, Config.category)
        ignorelist = ['README.md']
        wallpapers = self.__collect_wallpapers(path, ignorelist)
        idx = wallpapers.index(Config.current)
        total = len(wallpapers) - 1
        next = 0 if idx + 1 > total else idx + 1
        Config.current = wallpapers[next]
        self.set_wallpaper()
    
    def previous_wallpaper(self):
        path = os.path.join(Config.wallpaperdir, Config.rootdir, Config.category)
        ignorelist = ['README.md']
        wallpapers = self.__collect_wallpapers(path, ignorelist)
        idx = wallpapers.index(Config.current)
        total = len(wallpapers) - 1
        next = total if idx - 1 < 0 else idx - 1
        Config.current = wallpapers[next]
        self.set_wallpaper()

    def interactive_setup(self):
        self.select_root_dir()
        self.select_category()
        self.select_wallpaper_setter()
        self.toggle_randomize()
        self.toggle_sddm_change()
        self.save_config()
        self.show_info()
