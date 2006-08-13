#! /usr/bin/env python

import sys
import lib.outputhandler
import lib.inputhandler

def main(args):
    # Init handlers
    oh = lib.outputhandler.OutputHandler()
    ih = lib.inputhandler.InputHandler(oh.getcanvas())

    # Start rolling demos! ;-)
    ih.start()

if __name__ == '__main__':
    main(sys.argv[1:])
