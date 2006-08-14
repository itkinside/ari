#! /usr/bin/env python

import sys
import libari.wall
import libari.canvas
import demos.fade
import demos.chess
import demos.stars

class Arid:
    def __init__(self):
        pass

    def main(self, args):
        # Init output device
        # FIXME: Read from config
        self.output = libari.wall.Wall()

        # Init canvas
        self.canvas = libari.canvas.Canvas(self.output)

        # Load demos
        self.demos = {}
        self.demos['fade'] = demos.fade.Fade(self.canvas, 10, 60)
        self.demos['chess'] = demos.chess.Chess(self.canvas)
        self.demos['stars'] = demos.stars.Stars(self.canvas, 0, 60)

        # Start rolling demos!
        # FIXME!
        try:
            self.demos['stars'].execute()
        except KeyboardInterrupt, e:
            pass

if __name__ == '__main__':
    arid = Arid()
    arid.main(sys.argv[1:])
