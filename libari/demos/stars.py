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

class Stars(libari.demos.base.Base):
    """A heaven of stars"""

    def setup(self, min = 1, max = 99, stars = 300):
        """
        Input:
            min         Minimum brightness, default 0
            max         Maximum brightness, default 99
            stars       Number of stars, default 300

        """

        # Check input
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

        if int(stars) > 0:
            self.starcount = int(stars)

        # Set update frequency
        self.setfps(5)

        # Create stars
        self.stars = []
        for i in range(self.starcount):
            self.stars.append(Star(self.config.wallsizex,
                                   self.config.wallsizey,
                                   self.min,
                                   self.max))

    def prepare(self):
        """Prepare demo run"""
        self.canvas.blank()

    def run(self):
        """The demo"""
        while self.runnable:
            if self.drawable:
                for i in range(self.starcount):
                    self.stars[i].run()
                    (x, y, b) = self.stars[i].get()
                    self.canvas.setpixel(x, y, b)
                self.canvas.update()
            self.sleep()


class Star:
    def __init__(self, wx, wy, min, max):
        self.min = min
        self.max = random.randint(min, max)

        self.setpos(wx, wy)
        self.b = self.min
        self.rising = True

    def setpos(self, wx = False, wy = False):
        if wx:
            self.wx = wx
        if wy:
            self.wy = wy
        self.x = random.randint(0, self.wx)
        self.y = random.randint(0, self.wy)

    def run(self):
        # If star is dead, make another one
        if self.b == 0:
            self.setpos()
            #self.b = self.min
            self.rising = True

        # Fade
        if self.rising:
            self.b += random.randint(1, 5)
        else:
            self.b -= random.randint(1, 5)

        # Fade in done, start fade out
        if self.b >= self.max:
            self.b = self.max
            self.rising = False

        # Faded out, clean up
        if not self.rising and self.b <= self.min:
            self.b = 0

    def get(self):
        return (self.x, self.y, self.b)
