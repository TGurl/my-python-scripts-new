#!/usr/bin/env python

import os
import dataclasses
import distro
import psutil
from random import choice

# from time import sleep


@dataclasses.dataclass
class Colors:
    """A simple class defining colors"""
    reset = "\033[0m"
    black = "\033[30m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    pink = "\033[35m"
    cyan = "\033[36m"
    grey = "\033[37m"
    white = "\033[37:1m"
    blue2 = "\033[34:1m"
    cyan2 = "\033[36:1m"


@dataclasses.dataclass
class SysInfo:
    """Dataclass for all the information"""
    total_explicit: str
    distro_name: str
    time_left: str
    wallpaper: str
    kernel_id: str
    hostname: str
    username: str
    updates: str
    memory: tuple
    wpname: str
    uptime: str
    total: str
    arch: str
    aur: str
    cpu: tuple


# -----------------------------------------------------------
# System up-time
# -----------------------------------------------------------


def display_time(seconds, granularity=3):
    """Make time human readable"""
    result = []
    intervals = (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),    # 60 * 60 * 24
        ('hours', 3600),    # 60 * 60
        ('minutes', 60),
        ('seconds', 1),)

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


def get_uptime():
    """Get the uptime of the system"""
    with open('/proc/uptime', 'r', encoding='utf-8') as file_ptr:
        uptime_seconds = float(file_ptr.readline().split()[0])
    timer = display_time(int(uptime_seconds))
    return timer


# -----------------------------------------------------------
# System Information
# -----------------------------------------------------------

def get_memory_usage():
    #total_memory, used_memory, _ = map(
    #        int, os.popen('free -t -m').readlines()[-1].split()[1:])

    total_memory, used_memory, _, _, _, _ = map(
            int, os.popen('free -t -m').readlines()[1].split()[1:])

    return (total_memory, used_memory)

def get_cpu_info() -> tuple:
    load = psutil.getloadavg()
    cpu_count = os.cpu_count()
    load2 = round(load[2] * 100)
    cpu_usage = round(load2 / cpu_count)
    # cpu_usage2 = load2 / cpu_count
    return (cpu_usage, cpu_count)

# -----------------------------------------------------------
# Wallpaper information
# -----------------------------------------------------------


def get_wallpaper():
    """Get the current wallpaper."""
    path = os.path.join(os.path.expanduser('~'), ".fehbg")
    with open(path, 'r', encoding='utf-8') as file_ptr:
        fehbg = file_ptr.read().splitlines()
    wallpaper = fehbg[1].split()[-1]
    wpname = wallpaper.split('/')[-1].replace("'", "")
    return wallpaper, wpname


def get_timeleft():
    """Get the time until next wallpaper"""
    timer = os.popen("systemctl --user list-timers --all").read().split()

    if 'wallpaper.timer' not in timer:
        return "disabled"
    else:
        timer = os.popen("systemctl --user status wallpaper.timer").read().split()


    #if 'CET' in timer:
    #    idx = timer.index('CET')
    #else:
    #    idx = timer.index('CEST')

    idx = timer.index('left')
    mins = timer[idx - 1]
    hours = timer[idx - 2]

    if hours == 'CEST;' or hours == 'CET;':
        hours = ''
    timeleft = f"{hours}"
    if hours != '':
        timeleft += " "
    timeleft += f"{mins}"

    return timeleft

# -----------------------------------------------------------
# Collect all the information
# -----------------------------------------------------------


def collect_all_info():
    """Collect all the info"""
    SysInfo.distro_name = distro.name()
    SysInfo.hostname = os.popen("uname -n").read().strip()
    SysInfo.username = os.popen("whoami").read().strip()
    SysInfo.kernel_id = os.popen('uname -r').read().strip()
    SysInfo.uptime = get_uptime()
    SysInfo.total = os.popen("pacman -Q | wc -l").read().strip()
    SysInfo.total_explicit = os.popen("pacman -Qe | wc -l").read().strip()
    SysInfo.memory = get_memory_usage()
    SysInfo.cpu = get_cpu_info()

    SysInfo.wallpaper, SysInfo.wpname = get_wallpaper()
    SysInfo.time_left = get_timeleft()

# -----------------------------------------------------------
# Show the information in a nice box
# -----------------------------------------------------------

def select_quote():
    quotes = ['I want to have b(.)(.)bs',
              'I want to suck a BBC!',
              'Give me all your cum!',
              'I want to be a whore!',
              'Fill me up with your seed!',
              'Oh daddy, you feel so good!',
              'Did someone call a hooker?',
              'Are all those cocks for me?',
              '♠ I am a Queen of Spades ♠']
    return choice(quotes)

def show_info():
    collect_all_info()
    title2 = [
            '%b┌────────────────────────────────┐%r',
            '%b│      %y┌──┐   ┌┐┌┐┌┐             %b│%r',
            '%b│      %y│┌┐├┬┬─┤└┤│├┼─┬┬┬┬┬┐      %b│%r',
            '%b│      %y│├┤│┌┤─┤││└┤│││││├│┤      %b│%r',
            '%b│      %y└┘└┴┘└─┴┴┴─┴┴┴─┴─┴┴┘      %b│%r',
            '%b└────────────────────────────────┘%r'
            ]
    length = len(title2[0].replace('%b', '').replace('%r', ''))
    quote = select_quote()
    center = ((length - len(quote)) // 2) * ' '
    quote = f"{center}{quote}"

    for line in title2:
        line = line.replace("%b", f"{Colors.blue}")
        line = line.replace("%r", f"{Colors.reset}")
        line = line.replace("%y", f"{Colors.blue2}")
        print(f"{line}")
    print(f"\x1B[3m{quote}\x1B[0m", end='\n\n')
    
    mem_used = SysInfo.memory[1]
    mem_total = SysInfo.memory[0]

    mem_percentage = (mem_used * 100) // mem_total

    print(f"{Colors.cyan2}Kernel:{Colors.reset}     {SysInfo.kernel_id}")
    print(f"{Colors.cyan2}CPU:{Colors.reset}        {SysInfo.cpu[0]}% over {SysInfo.cpu[1]} cores")
    print(f"{Colors.cyan2}Memory:{Colors.reset}     {mem_used}/{mem_total} ({mem_percentage}%)")
    print(f"{Colors.cyan2}Uptime:{Colors.reset}     {SysInfo.uptime}")
    print(f"{Colors.cyan2}Installed:{Colors.reset}  {SysInfo.total} pkgs")
    print(f"{Colors.cyan2}Explicit:{Colors.reset}   {SysInfo.total_explicit} pkgs")
    print(f"{Colors.cyan2}Wallpaper:{Colors.reset}  {SysInfo.wpname}")
    if SysInfo.time_left == "disabled":
        print(f"{Colors.cyan2}Timer:{Colors.reset}      disabled")
    else:
        print(f"{Colors.cyan2}Time left:{Colors.reset}  {SysInfo.time_left}")
    print()


# -----------------------------------------------------------
# The main loop
# -----------------------------------------------------------


if __name__ == "__main__":
    show_info()
