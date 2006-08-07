#! /usr/bin/env python

import lib.input.fade
import lib.input.chess

class InputHandler:
    """Handles input plugins: input connection, input selection."""
    def __init__(self, canvas):
        self.canvas = canvas

        # FIXME: Read from config
        self.input = lib.input.fade.Fade(canvas, 10, 60)
        self.input = lib.input.chess.Chess(canvas)

    def start(self):
        self.input.start()
