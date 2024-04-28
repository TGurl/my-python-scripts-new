#!/usr/bin/env python
from pytube import Channel

#url = 'https://www.youtube.com/channel/UCPKcixqVGkUUek75dZ0W9Tw'
url = 'https://www.youtube.com/@ElisaSoloFashion'

c = Channel(url)
print(c.channel_name)
print(c.video_urls)
