#!/usr/bin/env python
import argparse
from core import Core


class Splitr(Core):
    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.clean_workspace()
        self.preflight_checks()
        self.banner()
        self.get_download_location()
        self.check_if_youtube()
        self.set_video_filename()
        self.fprint('Downloading from', self.domain)
        self.fprint('Saving video as', self.video_filename)
        self.fprint('Saving images as', self.set_image_type())
        self.drawline()
        self.video_downloader()
        self.video_player()
        self.split_video()
        self.finished()
        self.drawline()
        self.print(f"%g~ ALL DONE ~ {self.slogan()}%R")
        self.drawline()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='splitr',
                                     description='Download videos with ease',
                                     epilog='Jus be silent and suck that cock, bitch!')

    group = parser.add_argument_group(title = 'Other options')

    parser.add_argument('-i', '--input',
                        type=str,
                        metavar='<url>',
                        required=False,
                        help='URL of file to be downloaded')

    parser.add_argument('-o', '--output',
                        type=str,
                        metavar='<file>',
                        required=False,
                        help='Filename to save video as')
    
    group.add_argument('-c', '--clean',
                        action='store_true',
                        required=False,
                        help='Clean workspace')
    
    group.add_argument('-d', '--delete',
                        action='store_true',
                        required=False,
                        help='Delete video when finished')
    
    group.add_argument('-g', '--google',
                        action='store_true',
                        required=False,
                        help='Save images as Webp')
    

    group.add_argument('-s', '--split',
                        action='store_true',
                        required=False,
                        help='Split video after download')
    
    group.add_argument('-w', '--watch',
                        action='store_true',
                        required=False,
                        help='Watch video after download')
    
    group.add_argument('-v', '--verbose',
                        action='store_true',
                        required=False,
                        help='Show more info')


    app = Splitr(parser.parse_args())
    app.main()
