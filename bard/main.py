#!/usr/bin/env python
"""BARD - A simple music streamer"""

import os

import tomli
from pyfzf.pyfzf import FzfPrompt

YOUTUBE = "https://www.youtube.com/watch?v="
MPVOPTIONS = "--fs --volume=60 --really-quiet"
TOML = os.path.expanduser(os.path.join("~", ".bin", "stations.toml"))


def read_config():
    with open(TOML, "rb") as file:
        config = tomli.load(file)
    return config


def main():
    config = read_config()
    fzf = FzfPrompt()

    station_list = []
    for station_info in config["stations"]:
        station_list.append(station_info["name"])

    while True:
        answer = fzf.prompt(station_list, "--reverse")
        if not answer:
            break

        req = answer[0]
        station_id = station_list.index(req)

        stream_name = config["stations"][station_id]["name"]
        stream_id = config["stations"][station_id]["stream_id"]

        os.system("clear")
        print(f"Connecting to {stream_name}")

        os.system(f"mpv {YOUTUBE}{stream_id} {MPVOPTIONS}")

    os.system("clear")
    print("Thank you for listening...")


if __name__ == "__main__":
    main()
