#! /usr/bin/env python3

"""
Program to change display brightness from commandline
"""

# external imports
import sys
import os
from pathlib import Path
import configparser
from enum import Enum

# internal imports
import sys_backlight
from . import backlight, console, ncurses, pyqt

# meta variables
__version__ = '0.1'
__license__ = 'MIT'

# Exit states
success = 0
fail = 1

# Directories
cur_dir, cur_filename = os.path.split(__file__)
user_dir = os.path.expanduser("~")

# Configuration files
configfile_user = os.path.join(user_dir,".config/backlight.ini")
configfile_global = "/etc/default/backlight.ini"
configfile_pkg = os.path.join(cur_dir,"config","backlight.ini")

def loadconfig():
    """ parse configuration file"""
    config = configparser.ConfigParser()
    if os.path.isfile(configfile_user):
        configfile = configfile_user
    else:
        configfile = configfile_pkg
    config.read(configfile)
    return config

# save config options
config = loadconfig()

default = {
    "step": 2
}

def check():
    # check OS
    if os.name != "posix":
        print('Script only works on Linux')
        sys.exit(fail)

    # check file
    if (Path("/sys/class/backlight/intel_backlight/").is_dir() == False):
        print('System files do not exist')
        sys.exit(fail)

    # check root
    if (os.geteuid() != 0):
        print('Root rights required')
        sys.exit(fail)

class Mode(Enum):
    CONSOLE = 1,
    NCURSES = 2,
    GUI = 3

def main(mode=Mode.CONSOLE):

    check()

    # start interface
    if mode == Mode.CONSOLE:
        console.main()
    elif mode == Mode.NCURSES:
        ncurses.main()
    elif mode == Mode.GUI:
        pyqt.main()
    else:
        console.main()

    sys.exit(success)

def mode_console():
    main(Mode.CONSOLE)
def mode_ncurses():
    main(Mode.NCURSES)
def mode_gui():
    main(Mode.GUI)

if __name__ == "__main__":
    main()