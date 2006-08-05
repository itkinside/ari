#! /usr/bin/env python

import sys
import time
import lib.out.wall

# Set socket paramters
hostprefix = '192.168.0.'
hosts = xrange(2, 128) # 192.168.0.2..127
port = 5001
buf = 32

def main(args):
    # Brightness
    if len(args) and int(args[0]) >= 0 and int(args[0]) < 100:
        brightness = int(args[0])
    else:
        brightness = 99 # 0..99

    wall = lib.out.wall.Wall()
    while True:
        for i in range(30, 99):
            wall.send(i)
            time.sleep(0.01)
        for i in range(99, 30, -3):
            wall.send(i)
            time.sleep(0.01)

if __name__ == '__main__':
    main(sys.argv[1:])
