#! /usr/bin/env python

import lib.output.simulator
import lib.output.wall

class OutputHandler:
    """Connects canvas with chosen output."""

    def __init__(self):
        # FIXME: Read from config
        self.output = lib.output.wall.Wall()

    def getOutput(self):
        return self.output
