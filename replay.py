#! /usr/bin/python

'''
Launch using:
    xterm +t
        set xterm to 80x26 size
        ./replay.py [cap.file]
'''

import argparse
import base64
import sys
import os
import time
import datetime


def parse_args():
    parse = argparse.ArgumentParser(description='kevin on demand replayer')
    parse.add_argument(
        'file',
        help='capture file')
    return parse.parse_args()


def replay(file):
    start = datetime.datetime.now()
    for line in file.readlines():

        items = line.split()
        delay = float(items[0])
        dec = base64.b64decode(items[1])

        delta = lambda: (datetime.datetime.now() - start).total_seconds()
        while delta() < delay:
            time.sleep(0.01)

        os.write(sys.stdout.fileno(), dec)


def main():
    args = parse_args()
    with open(args.file) as cap:
        replay(cap)
    # clear the terminal
    os.write(sys.stdout.fileno(), chr(27) + "[2J")


main()
