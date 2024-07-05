# -*- coding: utf-8 -*-
from __future__ import print_function

import re
import sys
import math

class ProgressBar:
    """
    ----------------------------------------------------------------
    A simple progress bar for terminal
    https://gist.github.com/romuald/1a9e0f9bf7c9c45838111d6f0e55b26e

    Slightly adapted by: Transgirl
    ----------------------------------------------------------------
    Simple example::

        progress = ProgressBar(20, width=25, fmt=ProgressBar.FULL)
        for i in range(20):
            progress()
            progress.current = i
            sleep(0.05)
        progress.done()

        # ==> [=====                    ]  4/20 ( 20%) 16 to go

    """
    DEFAULT = 'Progress: %(bar)s %(percent)3d%%'
    FULL = '%(bar)s %(current)d/%(total)d (%(percent)3d%%) %(remaining)d to go'
    PUTA = '> Archiving %(bar)s %(current)d/%(total)d (%(percent)3d%%)'
    PUTA_MOVE = '> Moving %(bar)s (%(percent)3d%%)'
    PUTA_INST = '> Installing %(bar)s %(current)d/%(total)d (%(percent)3d%%)'
    PUTA_ZIP = '> Unzipping %(bar)s %(current)d/%(total)d (%(percent)3d%%)'
    PUTA_CLN = '> Cleaning %(bar)s %(current)d/%(total)d (%(percent)3d%%) %(remaining)d to go'
    
    def __init__(self, total, width=40, fmt=DEFAULT,
                 symbol='=', empty=' ', output=sys.stderr):
        assert len(symbol) == 1
        assert total >= 0
        assert width >= 0
       
        self.total = total
        self.width = width
        self.empty = empty
        self.symbol = symbol
        self.output = output
        self.fmt = re.sub(r'(?P<name>%\(.+?\))d',
                             r'\g<name>%dd' % len(str(total)), fmt)
                             
        self.current = 0
        
    def __call__(self):
        percent = self.current / float(self.total)
        size = int(self.width * percent)
        remaining = self.total - self.current
        bar = '[' + self.symbol * size + self.empty * (self.width - size) + ']'

        args = {
            'total': self.total,
            'bar': bar,
            'current': self.current,
            'percent': percent * 100,
            'remaining': remaining,
        }
        print('\r' + self.fmt % args, file=self.output, end='')
    
    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def done(self):
        self.current = self.total
        self()
        print('', file=self.output)
