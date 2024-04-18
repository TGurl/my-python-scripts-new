#!/usr/bin/env python
import os
from time import sleep

VOLUME = 40
YOUTUBE = "https://www.youtube.com/watch?v="
MPVOPTIONS = f"--fs --volume={VOLUME} --really-quiet"


stations = [
    ("Lofi Girl", "jfKfPfyJRdk"),
    ("Chillhop Radio - jazzy & lofi hip hop beats", "5yx6BWlEVcY"),
    ("Lofi Hip Hop Beats 24/7 Radio", "IRp0zhUFi-M"),
    ("Coffee Shop Radio", "lP26UCnoH9s"),
    ("Relaxing Jazz Piano Radio", "Dx5qFachd3A"),
    ("Coffee Jazz Music", "fEvM-OUbaKs"),
    ("Night Jazz New York", "aixaT5NjGo8"),
]


def get_input(available):
    while True:
        req = input("Select a station: ").lower()
        if req not in available:
            print("Not a valid option!")
            sleep(1.2)
            print("\033[1A", end="\x1b[2K")
        else:
            break
    return req


def menu():
    os.system("clear")
    print("BARD - A simple music streamer", end="\n\n")
    available = ["q"]
    for idx, station in enumerate(stations, start=1):
        print(f"[{idx}] {station[0]}")
        available.append(str(idx))
    print()
    print("[q] Quit", end="\n\n")
    return available


def main():
    while True:
        available = menu()
        req = get_input(available)

        if req == "q":
            break

        stream_id = stations[int(req) - 1][1]
        stream_ti = stations[int(req) - 1][0]
        stream = f"{YOUTUBE}{stream_id}"
        mpv = f"mpv {stream} {MPVOPTIONS}"
        os.system("clear")
        print(f"Connecting to {stream_ti}")
        os.system(mpv)


if __name__ == "__main__":
    main()
