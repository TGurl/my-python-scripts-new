import os
import base64
import subprocess

from colors import Colors


class TransgirlUtils:
    def __init__(self):
        self.appwidth = 64
        self.linechar = '─'
        self.rootpw = b'Y3liZXIwMDg='

    def b64_encode(self, string:str) -> bytes:
        """Encode a given string into b64 bytes"""
        return base64.b64encode(string.encode('utf-8'))

    def b64_decode(self, string:bytes) -> str:
        """Decode a given b64 byte string"""
        return base64.b64decode(string).decode('utf-8')

    def execute_as_root(self, command: str) -> None:
        """Execute a command as root. Output is hidden."""
        rootpw = self.b64_decode(self.rootpw)
        command = f"sudo -S {command} > /dev/null 2>&1"
        subprocess.call(f"echo {rootpw} | {command}", shell=True)

    def execute_as_user(self, command: str) -> None:
        """Execute a command as user. Output is hidden"""
        command = f"{command} > /dev/null 2>&1"
        subprocess.call(command, shell=True)

    def colorize(self, string:str, remove:bool=False) -> str:
        """
        Colorize a string

        string -> string to be colorized
        remove -> set to true to remove color codes

        returns string
        """
        for color in Colors.colors:
            replacement = '' if remove else color[1]
            string = string.replace(color[0], replacement)
        return string

    def check_appwidth(self) -> None:
        """
        Checks wether appwidth is even or not.
        If not add 1 to make it even.
        """
        if self.appwidth % 2 != 0:
            self.appwidth += 1

        if self.appwidth > os.get_terminal_size().columns:
            self.appwidth = os.get_terminal_size().columns - 1

    def print(self, string:str, cr:bool = False) -> None:
        """
        My print version

        Colorizes the string passed.
        cr -> adds an extra \\n if True
        """
        end = '\n\n' if cr else '\n'
        print(self.colorize(string), end=end)

    def cprint(self, string:str, short_string:str) -> None:
        """Center prints the given string"""
        self.check_appwidth()
        tmp = self.colorize(string, remove=True)
        
        if len(tmp) > self.appwidth:
            string = short_string
            tmp = self.colorize(string, remove=True)

        spcs = ((self.appwidth - len(tmp)) // 2) * ' '
        self.print(f"{spcs}{string}")
        del tmp

    def banner(self,
               string:str,
               short_string:str,
               line_color:str = '%c',
               cls:bool = True) -> None:
        """Prints a banner with the given string"""
        self.check_appwidth()
        if cls:
            os.system('clear')
        line = self.appwidth * self.linechar
        self.print(f"{line_color}{line}%R")
        self.cprint(string, short_string)
        self.print(f"{line_color}{line}%R")
