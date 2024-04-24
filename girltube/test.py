#!/usr/bin/env python
from pyfzf.pyfzf import FzfPrompt


FILE = 'girltube.csv'
DATA = []
OWNERS = []
LINE_TO_REMOVE = ''


with open(FILE, 'r') as f:
    data = f.readlines()

for line in data:
    line = line.strip().split(',')
    OWNERS.append(line[1])

OWNERS.sort()

o = FzfPrompt().prompt(OWNERS, '--reverse --exact')

for line in data:
    if o[0] in line:
        LINE_TO_REMOVE = line
        break

print('Removing', LINE_TO_REMOVE)

with open(FILE, 'r+') as f:
    d = f.readlines()
    f.seek(0)
    for i in d:
        if i != LINE_TO_REMOVE:
            f.write(i)
    f.truncate()
