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

class Chess(threading.Thread):
    """Color every second board."""

    def __init__(self, canvas, min = 1, max = 99):
        """
        Input:
            canvas  Canvas to paint on.
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

    def stop(self):
        self.running = False

    def run(self):
        b1, b2 = 0, self.max
        while self.running:
            for panelno in self.canvas.model:
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
