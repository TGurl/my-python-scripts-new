import requests
import textwrap
import json
import os

from colors import Colors


class Utils:
    def __init__(self):
        pass

    def colorize(self, message:str, remove:bool=False) -> str:
        for color in Colors.colors:
            repl = '' if remove else color[1]
            message = message.replace(color[0], repl)
        return message

    def printr(self, message: str, nl:bool=False) -> None:
        end = '\n\n' if nl else '\n'
        message = self.colorize(message)
        print(message, end=end)

    def boxit(self, message: str) -> None:
        chars = ['┌', '┐', '└', '┘', '─', '│']
        message = f"%y{message} %R- %bTransgirl Coding Studios%R"
        temp = self.colorize(message, remove=True)
        line = (len(temp) + 2) * chars[4]
        self.printr(f"%c{chars[0]}{line}{chars[1]}%R")
        self.printr(f"%c{chars[5]} {message} %c{chars[5]}%R")
        self.printr(f"%c{chars[2]}{line}{chars[3]}%R")
        del temp
    
    def shorten_string(self, message: str, max_length:int=80) -> list:
        lines = textwrap.wrap(message, max_length, break_long_words=False)
        return lines

    def qotd(self, width=80, version='kjv'):
        url = f"https://bible-api.com/?translation={version}&random=verse"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).text
        data = json.loads(response)
        reference = f"%c~ {data['reference']}%R"
        temp = self.colorize(reference, remove=True)
        spc = (width - len(temp)) * ' '
        quote = data['text'].strip().replace('\n', ' ')
        for line in self.shorten_string(quote, max_length=width):
            self.printr(line)
        self.printr(f"{spc}{reference}")

    def read_bible(self, width=80):
        bible = [line.rstrip() for line in open('kjv.txt')]
        total = len(bible)

        for verse_idx in range(0, total, 10):
            os.system('clear')
            for line in range(verse_idx, verse_idx + 9):
                verse = self.shorten_string(bible[line].split('\t')[1], max_length=width)
                for line in verse:
                    self.printr(line)
            _ = input('- ENTER -')
