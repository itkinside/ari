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
import threading
import time

class Stars(threading.Thread):
    """A heaven of stars."""

    def __init__(self, canvas, min = 1, max = 99):
        """
        Input:
            canvas  Canvas to paint on
            min     Minimum brightness, default 0
            max     Maximum brightness, default 99
        """

        threading.Thread.__init__(self)

        self.canvas = canvas
        self.running = True

        if int(min) > 0 and int(min) < 100:
            self.min = int(min)
        else:
            self.min = 1

        if int(max) >= 0 and int(max) < 100:
            self.max = int(max)
        else:
            self.max = 99

        if self.min > self.max:
            self.min, self.max = self.max, self.min

    def stop(self):
        self.running = False

    def run(self):
        xmax = 104
        ymax = 29
        b = 0
        self.canvas.blank()
        while self.running:
            for i in range(10):
                x = random.randint(0, xmax)
                y = random.randint(0, ymax)
                b = random.randint(self.min, self.max)
                for c in range(0, b, 3):
                    self.canvas.setpixel(x, y, b)
            self.canvas.update()
            time.sleep(0.5)
