#! /usr/bin/env python

import random
import time
import lib.input.input

class Stars(lib.input.input.Input):
    """A heaven of stars."""

    def __init__(self, canvas, min = 1, max = 99):
        """
        Input:
            canvas: Canvas to paint on.
        """

        self.canvas = canvas
        self.run = True
        self.running = False

        if int(min) > 0 and int(min) < 100:
            self.min = int(min)
        else:
            self.min = 1
        if int(max) >= 0 and int(max) < 100:
            self.max = int(max)
        else:
            self.max = 99

    def execute(self):
        self.running = True
        self.canvas.fill(0)
        xmax = 104
        ymax = 29
        b = 0
        while self.run:
            for i in range(10):
                x = random.randint(0, xmax)
                y = random.randint(0, ymax)
                b = random.randint(self.min, self.max)
                for c in range(0, b, 3):
                    self.canvas.setpixel(x, y, b)
#                self.canvas.setpixel(x+1, y-1, 0)
#                self.canvas.setpixel(x+1, y,   0)
#                self.canvas.setpixel(x+1, y+1, 0)
#                self.canvas.setpixel(x,   y-1, 0)
#                self.canvas.setpixel(x,   y+1, 0)
#                self.canvas.setpixel(x-1, y-1, 0)
#                self.canvas.setpixel(x-1, y,   0)
#                self.canvas.setpixel(x-1, y+1, 0)
            self.canvas.updateall()
            time.sleep(0.0)
        self.running = False
