# Commandline interface to adjust display brightness through sys files
#
# Author: Kevin Thomas <hamgom95@gmail.com>
# Last Change: March 10, 2017
# URL https://github.com/hamgom95/sys_backlight

"""
commandline interface
"""

import sys
import argparse

import sys_backlight
from .. import backlight, ncurses, pyqt

def interface():

    b = backlight.Backlight()

    parser = argparse.ArgumentParser(description='Backlight utility', add_help=True)
    parser.add_argument('--set', '-s', metavar='P', type=int,
                        help='set brightness')
    parser.add_argument('--get', '-g', action='store_true',
                        help='get brightness')
    parser.add_argument('--inc', '-i', metavar='P', type=int, nargs='?', const=-1,
                        help='increase brightness')
    parser.add_argument('--dec', '-d', metavar='P', type=int, nargs='?', const=-1,
                        help='decrease brightness')
    parser.add_argument('--max', '-1', action='store_true',
                        help='increment brightness')
    parser.add_argument('--min', '-0', action='store_true',
                        help='decrement brightness')
    parser.add_argument('--ncurses','-n', action='store_true',
                        help='ncurses mode')
    parser.add_argument('--qt', '-q', action='store_true',
                        help='qt gui mode')

    # Parse arguments
    args = parser.parse_args()

    if args.set:
        b.setrel(args.set)
    elif args.get:
        print(b.getrel())
    elif args.inc:
        inc = args.inc if args.inc is not -1 else sys_backlight.default["step"]
        b.addrel(inc)
    elif args.dec:
        dec = args.dec if args.dec is not -1 else sys_backlight.default["step"]
        b.subrel(dec)
    elif args.min:
        b.setrel(0)
    elif args.max:
        b.setrel(100)
    elif args.ncurses:
        ncurses.main()
    elif args.qt:
        pyqt.main()

    sys.exit(0)


def main():
    interface()

if __name__ == "__main__":
    main()