import os
from zipfile import ZIP_DEFLATED

class Config:
    title = 'Puta'
    version = '0.1g'
    build = '20240609'
    width = 20
    lorefolder = os.path.join('/', 'lore', 'sexgames')
    donefolder = os.path.join('/', 'lore', 'sexgames', 'done')
    usbfolder = os.path.join('/', 'USB', 'sexgames')
    playfolder = os.path.join('/', 'lore', 'playing')
    lzma = False
    bzip2 = False
    delete = False
    destination = ''
    query = ''
    compress = ZIP_DEFLATED
