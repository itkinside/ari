#! /usr/bin/env python

import lib.outputhandler

class Canvas:
    """Paint on the canvas, and the wall shows your art!"""
    def __init__(self):
        self.outputhandler = lib.outputhandler.OutputHandler()
        self.output = self.outputhandler.getOutput()

    def fill(self, brightness):
        data = []
        for i in range(25):
            data.append(brightness)
        self.output.sendall(data)
