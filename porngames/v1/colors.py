#!/usr/bin/env python

class Colors:
    reset = "\033[0m"
    black = "\033[30;1m"
    red = "\033[31;1m"
    green = "\033[32;1m"
    yellow = "\033[33;1m"
    blue = "\033[34;1m"
    pink = "\033[35;1m"
    cyan = "\033[36;1m"
    white = "\033[37;1m"
    gray = "\033[37m"
    italic = "\x1B[3m"

    codes = ['%R', '%B', '%G', '%r', '%g', '%y', '%b', '%p', '%c', '%w', '%i']
    colors = [
            ('%R', reset),
            ('%B', black),
            ('%G', gray),
            ('%r', red),
            ('%g', green),
            ('%y', yellow),
            ('%b', blue),
            ('%p', pink),
            ('%c', cyan),
            ('%w', white),
            ('%i', italic)
    ]
