class Colors:
    reset  = "\033[0m"
    black  = "\x1b[0;30;40m"
    red    = "\x1b[0;31;40m"
    green  = "\x1b[0;32;40m"
    yellow = "\x1b[0;33;40m"
    blue   = "\x1b[0;34;40m"
    purple = "\x1b[0;35;40m"
    cyan   = "\x1b[0;36;40m"
    white  = "\x1b[0;37;40m"
    italic = "\x1b[3m"

    colors = [
            ('%R', reset),
            ('%B', black),
            ('%r', red),
            ('%g', green),
            ('%y', yellow),
            ('%p', purple),
            ('%b', blue),
            ('%c', cyan),
            ('%w', white),
            ('%i', italic)
    ]
