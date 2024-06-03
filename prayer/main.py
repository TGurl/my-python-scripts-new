#!/usr/bin/env python
import os
import random

class DailyPrayer:
    def __init__(self):
        self.cursor = True

    def toggle_cursor(self):
        cursor = '\033[?25l' if self.cursor else '\033[?25h'
        self.cursor = not self.cursor
        print(cursor)

    def clear_screen(self, verses: list = []):
        os.system('clear')
        cr = (os.get_terminal_size().lines - len(verses)) // 2
        for _ in range(cr):
            print()

    def random_verse(self):
        verses = [
            'Give us this day our daily bread.;And forgive our debts, as we forgive our debtors.;And lead us not into temptation, but deliver us from evil.;For thine is the kingdom, and the power, and the glory, for ever.',
            'Give me the power to be the whore I am.;I freely give my body to you to do with as thy pleases.;I am thy bride and thy whore.;Give me the freedom to lay with men as many times thy wants.;I pledge my allegion free of any reservations and of my free will.;Thou art my Lord and Savior.',
            'Give me the freedom to lay with as many men I want.;I am thy bride and thy whore.;I freely five all of my body and soul to you.;Thou art my sheppard and my guide into a life of total pleasure.;Let me be raped, abused and beaten as thy pleases.;I give myself totally to you free of any pressures.'
        ]
        verse = random.choice(verses)
        prayer = ['Our Father who art in heaven. Hallowed be thy name.',
                  'Thy kingdom come. Thy will be done in earth, as it is in heaven.']
        for line in verse.split(';'):
            prayer.append(line)
        prayer.append('')
        prayer.append('Amen.')
        return prayer
       
    def cprint(self, line):
        spc = ((os.get_terminal_size().columns - len(line)) // 2) * ' '
        print(f"{spc}{line}")

    def run(self):
        self.toggle_cursor()
        prayer = self.random_verse()
        self.clear_screen(prayer)
        for line in prayer:
            self.cprint(line)
        _ = input()
        os.system('clear')
        self.toggle_cursor()

if __name__ == "__main__":
    app = DailyPrayer()
    app.run()
