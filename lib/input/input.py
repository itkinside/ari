#! /usr/bin/env python

import time

class Input:
    """
    Basic input plugin class.
    
    Other input plugins should inherit from this one.
    """

    def __init__(self, canvas):
        """
        Input:
            canvas: Canvas to paint on.
        """

        self.canvas = canvas
        self.run = True
        self.running = False

    def start(self):
        self.run = True
        if not self.running:
            try:
                self.loop()
            except KeyboardInterrupt, e:
                pass

    def stop(self):
        self.run = False

    def loop(self):
        self.running = True
        while self.run:
            # Do your job
            break
        self.running = False
