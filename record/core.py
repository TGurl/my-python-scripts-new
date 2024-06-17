# ----------------------------------------------------------------------------
# -- Imports
# ----------------------------------------------------------------------------
import os
import sys
import shlex
import time
import shutil

from subprocess import call
from colors import Colors
from datetime import datetime


# ----------------------------------------------------------------------------
# -- Class Core
# ----------------------------------------------------------------------------
class Core:
    def __init__(self):
        self.initialize()

    # ------------------------------------------------------------------------
    # -- Initialize
    # ------------------------------------------------------------------------
    def initialize(self):
        self.max_width = 47
        self.width = self.max_width - 2
        self.filename = 'test.mp4'
        self.curdate = ''
        self.countdown = True
        self.record_sound = True
        self.record_mouse = False
        self.play_video = True
        self.qwidth = 31

    # ------------------------------------------------------------------------
    # -- Main loop
    # ------------------------------------------------------------------------
    def main_loop(self):
        self.check_prereqs()
        self.check_terminal_width()
        self.intro_questions()
        self.banner()
        self.show_info()
        if self.countdown:
            self.count_down()
        else:
            print()
        self.start_recording()
        if self.play_video:
            self.play_recording()
        self.finished()

    # ------------------------------------------------------------------------
    # -- Some simple helper functions
    # ------------------------------------------------------------------------
    def check_terminal_width(self):
        if os.get_terminal_size().columns < self.max_width:
            self.banner()
            self.error_msg('Your terminal is too small!')
            self.info_msg(f"It needs to be at least {self.max_width} columns wide.")
            sys.exit()

    def check_prereqs(self):
        self.banner()
        apps = ['ffmpeg', 'mpv']
        cunt = True
        for app in apps:
            if not shutil.which(app):
                self.error_msg(f"Can't find %y{app}%R")
                cunt = False
        if not cunt:
            print()
            self.info_msg('Please check if either of the apps is installed.')
            sys.exit()

    def current_date(self):
        return datetime.today().strftime('%Y%m%d-%H%M%S')

    def show_info(self):
        sound = '%gYes%R' if self.record_sound else '%rNo%R'
        mouse = '%gYes%R' if self.record_mouse else '%rNo%R'
        record = '%gYes%R' if self.play_video else '%rNo%R'

        self.curdate = self.current_date()

        #self.filename = self.filename + '_' + self.curdate
        tmp = self.filename.split('.')
        self.filename = tmp[0] + f"_{self.curdate}." + tmp[1] 
        del(tmp)

        # self.fprint('Date of recording', '%y' + self.curdate + '%R')
        self.fprint('Recording as', '%y' + self.filename + '%R')
        self.fprint('Recording sound', sound)
        self.fprint('Recording mouse', mouse)
        self.fprint('Show video when done', record)

    def count_down(self, counter=15):
        while counter:
            cstr = f"%y{counter}...%R" 
            self.fprint('Counting down', cstr)
            time.sleep(1)
            counter -= 1
            self.clearlines()
        self.fprint('Start recording', '%gRECORDING NOW!%R', cr=True)
        
    def ask_filename(self, question):
        prompt = self.format(question, '')
        while True:
            filename = input(self.colorize(prompt))
            if not filename:
                self.error_msg('The filename can not be empty. Please try again...')
                time.sleep(1.2)
                self.clearlines(2)
            else:
                break
        # -- check if filename has an extension, if so replace it with mp4 
        _, ext = os.path.splitext(filename)
        if not ext:
            filename += '.mp4'
        else:
            filename = filename.replace(ext, '.mp4')
        return filename

    def ask_yesno(self,question, default='y'):
        if default == 'y':
            prompt = f"{question} (%gY%R/n)"
        elif default == 'n':
            prompt = f"{question} (y/%gN%R)"
        else:
            self.info_msg('Function : askyesno')
            self.error_msg('Did not recognize the default variable!', exit=True)

        prompt = self.format(prompt, '', width=self.qwidth + 4)

        while True:
            res = input(self.colorize(prompt)).lower()
            res = default if not res else res
            result = res in ['y', 'n', 'yes', 'no']

            if result:
                break
            else:
                self.error_msg('You did not answer with yes or no!')
                time.sleep(1.2)
                self.clearlines(num =2)

        return res in ['y', 'yes']

    def intro_questions(self):
        self.banner()
        self.filename = self.ask_filename('Filename for the recording')

        self.record_sound = self.ask_yesno('Want to record sound?',
                                           default='y')
        self.record_mouse = self.ask_yesno('Want to record the mouse?',
                                           default='n')
        self.play_video = self.ask_yesno('Want to play recording?',
                                         default='y')
        self.countdown = self.ask_yesno('Want a countdown?', default='y')

    # ------------------------------------------------------------------------
    # -- The virtual VCR
    # ------------------------------------------------------------------------
    def start_recording(self):
        # -- recording will be done in the current working directory!
        self.status_msg(f"Recording %c{self.filename}%R, press %yq%R to quit)")

        audio = '-f pulse -i 0 ' if self.record_sound else ''
        mouse = '-draw_mouse 1' if self.record_mouse else '-draw_mouse 0'
        opts = '-y -hide_banner -loglevel error -stats'
        ffmpeg = f"ffmpeg {opts} -f x11grab -s 1920x1080 {mouse} -i :0.0 "
        ffmpeg += f"{audio}{self.filename}"

        self.run(ffmpeg)
        self.clearlines()
        self.status_msg("Recording stopped...")
        time.sleep(2)

    def play_recording(self):
        self.status_msg(f"Playing %c{self.filename}%R")

        if not os.path.exists(self.filename):
            self.error_msg(f"Can't find {self.filename}")
            self.info_msg('Did you even make a recording?')
            sys.exit()

        self.run(f"mpv --really-quiet -volume=90 {self.filename}")

    def finished(self):
        self.banner()
        self.print("Your recording is saved as%c{self.filename}%R", cr=True)
        self.info_msg('Thank you for using %gRecord Your Desktop%R.')
        sys.exit()

    # ------------------------------------------------------------------------
    # -- Some simple TUI stuff
    # ------------------------------------------------------------------------
    def run(self, command):
        call(shlex.split(command))

    def colorize(self, string, remove=False):
        for color in Colors.colors:
            repl = '' if remove else color[1]
            string = string.replace(color[0], repl)
        return string
    
    def print(self, string, cr=False):
        end = '\n\n' if cr else '\n'
        print(self.colorize(string), end=end)

    def format(self, key, value, fmt='', width=0):
        width = self.qwidth if not width else width

        if not fmt:
            fmt=' %y›%R {:<' + str(width) + '} : {}'
        return fmt.format(key, value)

    def fprint(self, key, value, cr=False, width=20):
        self.print(self.format(key, value, width=width), cr=cr)

    def status_msg(self, message):
        self.print(f" %g>>%R {message}")

    def info_msg(self, message):
        self.print(f" %y>>%R {message}")

    def error_msg(self, message, exit=False):
        self.print(f" %r>> Error%R : {message}")
        if exit:
            sys.exit()

    def banner(self, cls=True):
        if cls:
            call('clear')

        title = '%yRecord Your Desktop%R %b- %gTransgirl Coding Studio%R'
        length = len(self.colorize(title, remove=True)) + 2
        line = length * '~'

        self.print(f"%c{line}%R")
        self.print(f" {title}")
        self.print(f"%c{line}%R", cr=True)

    def clearlines(self, num=1):
        for _ in range(num):
            print('\033[1A', end='\x1b[2K')

