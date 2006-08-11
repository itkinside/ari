#! /usr/bin/env python

import time
import lib.input.input

class Fade(lib.input.input.Input):
    """Fade between to brightness values."""

    def __init__(self, canvas, min = 0, max = 99, step = 3):
        """
        Input:
            canvas: Canvas to paint on.
            min: Minimum brightness in fade, default 0.
            max: Maximum brightness in fade, default 99.
            step: Distance between brightness values used.
        """

        self.canvas = canvas
        self.run = True
        self.running = False

        if int(min) >= 0 and int(min) < 100:
            self.min = int(min)
        else:
            self.min = 0
        if int(max) >= 0 and int(min) < 100:
            self.max = int(max)
        else:
            self.max = 99
        if self.min > self.max:
            self.min, self.max = self.max, self.min
        if int(step) < 99:
            self.step = step
        else:
            self.step = 3

    def execute(self):
        self.running = True
        while self.run:
            for b in range(self.min, self.max, self.step):
                self.canvas.fill(b)
                time.sleep(0.01)
            for b in range(self.max, self.min, -self.step): 
                self.canvas.fill(b)
                time.sleep(0.01)
        self.running = False
