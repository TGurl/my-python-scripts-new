#!/usr/bin/env python
import os

from utils import TransgirlUtils

tgutils = TransgirlUtils()
FILENAME = os.path.expanduser("~/.local/share/transgirl/girltube/girltube_urls.csv")
NEWNAME = os.path.expanduser("~/.local/share/transgirl/girltube/girltube_urls_new.csv")
LINES = tgutils.read_file(FILENAME)

with open(NEWNAME, 'w') as f:
    for line in LINES:
        line += ",-1"
        f.write(line + '\n')

NEWLINES = tgutils.read_file(NEWNAME)
print(NEWLINES)
