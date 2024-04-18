#!/usr/bin/env python
import os
import shutil
import sys
import readchar
from time import sleep


def collect_folders(folder='.'):
    folders = []
    ignore = ['backups', 'keep']
    for item in os.scandir(folder):
        if os.path.isdir(item.name) and item.name not in ignore:
            folders.append(item.path)
    folders.sort()
    return folders

def collect_images(folder):
    images = []
    for item in os.scandir(folder):
        images.append(item.path)
    images.sort()
    return images

def move_folder(folder):
    if not os.path.exists(folder):
        print("Oops, {folder} doesn't seem to exist...")
        sys.exit()
    else:
        os.system('clear')
        print(f"{folder} is done, moving to 'keep'...")
        destination = os.path.join("keep", folder)
        shutil.move(folder, destination)
        print(f"Moving {folder} done.")
        sleep(2.5)

def main():
    folders = collect_folders()

    msg = "Keep this image? y/n/q "
    total_folders = len(folders)
    for fid, folder in enumerate(folders, start=1):
        images = collect_images(folder)
        
        total_images = len(images)

        for iid, image in enumerate(images, start=0):
            os.system('clear')
            cmd = f"timg -g64x {image}"
            os.system(cmd)
            f_name = folder.split('/')[-1]
            i_name = image.split('/')[-1]

            left = total_images - iid
            percent = (iid * 100) // total_images
            print(f"Reading folder {fid}/{total_folders} : {f_name}")
            if left > 1:
                print(f"Images left {left} [{percent:3}% done]: {i_name}")
            else:
                print(f"And the last one [{percent:3}% done]: {i_name}")

            print(msg, end="", flush=True)
            key = readchar.readchar().lower()

            if key == 'y':
                pass
            elif key == 'q':
                print("")
                sys.exit()
            else:
                os.remove(image)
        move_folder(folder)

if __name__ == "__main__":
    main()
