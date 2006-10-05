#! /usr/bin/env python
#
# arid - Daemon for running demos on a diode wall
# Copyright (C) 2006 Stein Magnus Jodal
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import random
import libari.demos.base

class Chess(libari.demos.base.Base):
    """A flashy chess game"""

    def setup(self, min = 0, max = 99, blocksize = False):
        """
        Input:
            min         Minimum brightness, default 0
            max         Maximum brightness, default 99
            blocksize   Size of chess fields, default to board size
        """

        # Check input
        if int(min) >= 0 and int(min) < 100:
            self.min = int(min)
        else:
            self.min = 0

        if int(max) >= 0 and int(max) < 100:
            self.max = int(max)
        else:
            self.max = 99

        if self.min > self.max:
            self.min, self.max = self.max, self.min

        if int(blocksize) > 0:
            self.blocksize = int(blocksize)
        else:
            self.blocksize = self.config.boardsizex

        # Set update frequency
        self.setfps(5)

    def run(self):
        # The demo
        b = Cycler(0, self.max)
        while self.runnable:
            if self.drawable:
                for x in range(0, self.config.wallsizex, self.blocksize):
                    for y in range(0, self.config.wallsizey, self.blocksize):
                        for bx in range(x, x + self.blocksize):
                            for by in range(y, y + self.blocksize):
                                self.canvas.setpixel(bx, by, b.get())
                        b.cycle(True)
                    b.cycle(True)
                self.canvas.update()
            self.sleep()

class Cycler:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.current = self.v1
        if self.v1 > self.v2:
            self.max = self.v1
            self.min = self.v2
        else:
            self.max = self.v2
            self.min = self.v1

    def get(self):
        return self.current

    def cycle(self, rand = False):
        # Switch value
        if self.current == self.v1:
            self.current = self.v2
        else:
            self.current = self.v1

        # Randomize value
        if self.current and rand:
            self.current = random.randint(1, self.max)
