#! /usr/bin/env python

import random
import time

class Chess:
    """Color every second board."""

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
        b1, b2 = 0, self.max
        while self.run:
            for panelno in self.canvas.model:
#                if panelno == 1:
#                    continue
                panel = self.canvas.model[panelno]
                for y in range(panel['height']):
                    if panel['width'] % 2 == 0:
                        b1, b2 = b2, b1
                    for x in range(panel['width']):
                        b1, b2 = b2, b1
                        if b1 > 0:
                            b1 = random.randint(self.min, self.max)
                        self.canvas.fillboard(b1, panelno, x, y)
            time.sleep(0.2)
            b1, b2 = b2, b1
        self.running = False
