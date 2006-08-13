#! /usr/bin/env python

import libari.wall
import libari.canvas

class OutputHandler:
    """Connects canvas with chosen output."""

    def __init__(self):
        # Init output device
        # FIXME: Read from config
        self.output = libari.wall.Wall()

        # Init canvas
        self.canvas = libari.canvas.Canvas(self.output)

    def getoutput(self):
        return self.output

    def getcanvas(self):
        return self.canvas
