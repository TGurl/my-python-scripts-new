# DLer
_a simple download script using yt-dlp_

![Screenshot](img/screenshot.png)

## Dependencies
* yt-dlp
* python 3


## Basic Usage
This script reads the contents of a text file and tries to download them using _yt-dlp_, so make sure that it's installed.

The lists will automatically be deleted when all downloads are finished, so you can always fix a typo and restart the downloads. To keep track whether a video has been downloaded already _dler_ uses an option of _yt-dlp_ called _download-archive_. In this case that file is named _done.txt_. 

With the _-k_ option you can instruct _dler_ not to delete the files afterwards.


## Instructions

### Step 1
Create a textfile containing the following urls (for example, you can use other ones of course) and save it as _list_
```
https://www.youtube.com/watch?v=z7DgP8sgM1A
https://www.youtube.com/watch?v=sB7XIlN0kWU
```


### Step 2
Now you can easily download them by issuing:
```
$ dler -i list
```

## Multiple lists
You can also issue multiple lists:

```
$ dler -i list1 list2 list3 [...]
```
The script utilizes a feature of _yt-dlp_ to check whether a video has been downloaded already, this file is called _done.txt_ by default, so you won't be downloading a video twice when it appears in multiple lists.


## Download subtitles
If you want to download subtitles with the files:

```
$ dler -s -i list
```


## Audio only
If you want to download the files as audio only:

```
$ dler -a -i list
```

## Hide yt-dlp output
If you don't want to see the _yt_dlp_ output:

```
$ dler -q -i list
```


## Keep the lists after completion
If you want to keep the lists (including done.txt) than issue:
```
$ dler -k -i list
```


It's a simple script, as I told you.
