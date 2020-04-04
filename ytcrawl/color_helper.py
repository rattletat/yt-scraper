#!/usr/bin/env python

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'

class markup:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

info = markup.BOLD + color.PURPLE + "[INFO] " + markup.END
usage = markup.BOLD + color.YELLOW + "[USAGE] " + markup.END
error = markup.BOLD + color.RED + "[ERROR] " + markup.END
warning = markup.BOLD + color.YELLOW + "[WARNING] " + markup.END

def bold_blue(txt):
    return markup.BOLD + color.BLUE + txt + markup.END

def bold_purple(txt):
    return markup.BOLD + color.PURPLE + txt + markup.END
