#!/usr/bin/env python
import os, sys
import fnmatch
import argparse
import glob
from zipfile import ZipFile, ZipInfo
from pyfzf.pyfzf import FzfPrompt


class ZipFileWithPermissions(ZipFile):
    """ Custom ZipFile class handling file permissions. """
    def _extract_member(self, member, targetpath, pwd):
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)

        targetpath = super()._extract_member(member, targetpath, pwd)

        attr = member.external_attr >> 16
        if attr != 0:
            os.chmod(targetpath, attr)
        return targetpath


def collect_games():
    folders = [os.path.join('~', 'Games', 'archives'),
               os.path.join('~', 'USB', 'sexgames'),
               os.path.join('~', 'USB', 'sexgames', 'keep')]
    games = []
    for folder in folders:
        path = os.path.expanduser(folder)
        for file in os.listdir(path):
            if fnmatch.fnmatch(file, '*.zip'):
                games.append(os.path.join(path, file))
    games.sort()
    return games

def collect_games_new():
    folders = [os.path.join('~', 'Games', 'archives'),
               os.path.join('~', 'USB', 'sexgames'),
               os.path.join('~', 'USB', 'sexgames', 'keep')]
    extensions = ['**.zip', '**.tar.gz', '**.tar.bz2', '**.tar.xz']
    games = []
    found = []
    for folder in folders:
        path = os.path.expanduser(folder)
        for extension in extensions:
            found = glob.glob(os.path.join(path, extension), recursive=True)
        games.append(found)
    games.sort()
    print(games)
    _ = input('...')
    # return games

def parse_target(target):
    if target == 'playing':
        path = os.path.expanduser(os.path.join('~', 'Games', 'playing'))
    else:
        path = os.path.expanduser(os.path.join('~', 'Games', 'todo'))
    return path

def install(target):
    """Install a porn game"""
    games = collect_games_new()
    target = parse_target(target)
    fzf = FzfPrompt()
    game = fzf.prompt(games, '--reverse')
    os.system('clear')
    print(f"Installing {game[0].split('/')[-1]} to {target}", end='\n\n\n')

    with ZipFileWithPermissions(game[0]) as archive:
        INFO = archive.namelist()
        TOTAL = len(INFO)
        LEAD = len(str(TOTAL))
        count = 1
        name = ""
        for file in INFO:
            percent = (count * 100 // TOTAL)
            name = file if len(file) < 35 else ".." + file[-35:]
            print('\033[1A', end='\x1b[2K')
            print(f"Extracting {count:{LEAD}}/{TOTAL} ({percent:3}%) : {name}")
            archive.extract(file, target)
            count += 1
    os.remove(game[0])

def remove():
    """Remove a porn game"""
    print('-- removing a game --')

def main(args):
    """Install/Remove a porn game. Defaults to install"""
    if args.remove:
        print('-- removing a game --')
    else:
        print(f'-- install a game to {args.target} --')
        _ = input('... [1]')

        install(args.target)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Install or remove a porn game.',
            epilog='If no argument is passed we will install a game to ~/Games/playing')
    
    parser.add_argument('-r', '--remove',
                        action='store_true',
                        default=False,
                        required=False,
                        help='Remove a game')
    parser.add_argument('-t', '--target',
                        choices=['playing', 'todo'],
                        default='playing',
                        required=False,
                        help='Where to install the game')

    args = parser.parse_args()
    main(args)
