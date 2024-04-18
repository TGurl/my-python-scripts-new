#!/usr/bin/env python
import os

def read_list():
    lines = [line.rstrip() for line in open('list', 'r')]
    return lines

def main():
    lines = read_list()
    total = len(lines)

    for idx, item in enumerate(lines, start=1):
        percent = (idx * 100) // total
        os.system('clear')
        print(f"Downloading {idx}/{total} [{percent:3}%]")
        ytdl = f"yt-dlp -o '%(uploader)s-{idx:02}.%(ext)s' {item}"
        os.system(ytdl)



if __name__ == "__main__":
    main()
