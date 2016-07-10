#! /usr/bin/python

import datetime
import socket
import select
import os
import base64
import argparse
import time


class Session(object):

    def __init__(self, host, port):
        self.sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_.connect((host, port))
        self.sock_.send(os.linesep + 'y' + os.linesep)
        self.sock_.setblocking(0)
        self.strike_ = 0

    def poll(self):
        while True:
            ready = select.select([self.sock_], [], [], 30)
            if ready[0]:
                buf = self.sock_.recv(1024 * 8)
                if buf == '':
                    self.strike_ += 1
                    time.sleep(0.05)
                else:
                    self.strike_ = 0
                if self.strike_ == 100:
                    print "timeout"
                    break
                yield buf
            else:
                break


def dump_session(port, host):
    sesh = Session(host, port)
    dump = open('{0}.dmp'.format(port), 'w')
    print 'begin {0}'.format(port)
    start = datetime.datetime.now()
    for item in sesh.poll():
        delta = datetime.datetime.now() - start
        dump.write('{0} {1}{2}'.format(
            delta.total_seconds(),
            base64.b64encode(item),
            os.linesep)
        )
    dump.close()
    print 'end'


def parse_args():
    parse = argparse.ArgumentParser(description='kevin on demand downloader')
    parse.add_argument(
        'start',
        type=int,
        help='start port')
    parse.add_argument(
        'end',
        type=int,
        help='end point')
    parse.add_argument(
        '-host',
        default='kevin-on-demand.takedown.com',
        help='remote host'
    )
    return parse.parse_args()


def main():
    args = parse_args()
    for port in range(args.start, args.end):
        try:
            dump_session(port, args.host)
        except socket.error:
            continue


main()
