#! /usr/bin/env python

import sys
import lib.inputhandler
import lib.canvas

def main(args):
    # Get brightness
    if len(args) and int(args[0]) >= 0 and int(args[0]) < 100:
        brightness = int(args[0])
    else:
        brightness = 99 # 0..99

    canvas = lib.canvas.Canvas()
    ih = lib.inputhandler.InputHandler(canvas)

    ih.start()

if __name__ == '__main__':
    main(sys.argv[1:])
