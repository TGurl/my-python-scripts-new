import os
import sys
import glob

from settings import *
from zipfile import ZipFile


class Utils:
    def __init__(self):
        pass

    def collect_games(self):
        zipfiles = glob.glob(os.path.join(ZIPFOLDER, "*.zip"))
        zipfiles.sort()
        return zipfiles

    def check_if_extraced(self, filename):
        filename = filename.replace('.zip', '')
        if os.path.exists(os.path.join(GAMEFOLDER, filename)):
            return True
        else:
            return False

    def remove(self, filepath):
        self.header()
        os.remove(filepath)
        print(f"{filepath} removed")

    def unzip(self, filepath, keep=True):
        self.header()
        filename = filepath.split('/')[-1]
        deleted = False

        if self.check_if_extraced(filename):
            self.header()
            print(f"{filename} has already been extracted.")
            sys.exit()
        
        size = self.convert_size(os.stat(filepath).st_size)
        print(f"=> Unzipping {filename} ({size})")
        with ZipFile(filepath, 'r') as zf:
            filelist = zf.infolist()
            total = len(filelist)

            for i, item in enumerate(filelist, start=1):
                percent = i * 100 // total
                fn = item.filename if len(item.filename) < 30 else ".." + item.filename[-28:]
                print(f"-> [{percent:3}%] Extracting: {fn}")
                extracted_path = zf.extract(item, GAMEFOLDER)
                if item.create_system == 3:
                    unix_attr = item.external_attr >> 16
                    if unix_attr:
                        os.chmod(extracted_path, unix_attr)
                print('\033[1A', end='\x1b[2K')
        print('\033[1A', end='\x1b[2K')

        if not keep:
            print(f'=> Deleting archive...')
            os.remove(filepath)
            deleted = True

        if deleted:
            print('\033[1A', end='\x1b[2K')
        print(f"\nHave fun playing {filename.replace('.zip', '')}!")

    def convert_size(self, size: float, decimals=2):
        unit = 'B'
        for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']:
            if size < 1024.0 or unit == 'PiB':
                break
            size /= 1024.0
        return f"{size:.{decimals}f} {unit}"

    def header(self):
        os.system('clear')
        title = ' Porngames v4 - Copyright 2023 Transgirl '
        line = len(title) * '-'
        print(line)
        print(title)
        print(line, end='\n')
