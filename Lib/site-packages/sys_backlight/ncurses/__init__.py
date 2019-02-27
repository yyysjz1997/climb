# Ncurses interface to adjust display brightness through sys files
#
# Author: Kevin Thomas <hamgom95@gmail.com>
# Last Change: March 10, 2017
# URL https://github.com/hamgom95/sys_backlight

"""
ncurses interface
"""

import sys
import curses

import sys_backlight
from .. import backlight

keys = {
    'esc': 27,
    'q': 113,
    'up': 259,
    'down': 258,
    'left': 260,
    'right': 261
}

alias = {
    'esc': 'quit',
    'q': 'quit',
    'up': 'inc',
    'down': 'dec',
    'left': 'min',
    'right': 'max',
}

action = {
    "quit": (lambda _: sys.exit(sys_backlight.success)),
    "inc": (lambda b: b.addrel(sys_backlight.default['step'])),
    "dec": (lambda b: b.subrel(sys_backlight.default['step'])),
    "min": (lambda b: b.setrel(0)),
    "max": (lambda b: b.setrel(100)),
}

def interface():
    b = backlight.Backlight()

    screen = curses.initscr()
    curses.noecho()
    screen.keypad(1)

    try:
        while True:
            char = screen.getch()  # fetch input
            for keyname, keycode in keys.items():  # loop through defined keys
                if char == keycode:  # inputed key matches definied entry
                    if alias[keyname]:  # alias for key exists
                        if action[alias[keyname]]:  # action for alias exists
                            action[alias[keyname]](b)  # execute key action
    finally:
        screen.keypad(0)
        curses.endwin()
        curses.echo()

def main():
    interface()
    sys.exit(sys_backlight.success)

if __name__ == "__main__":
    main()