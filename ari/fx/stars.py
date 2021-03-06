#! /usr/bin/env python
#
# Copyright (C) 2006 Stein Magnus Jodal
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2
# as published by the Free Software Foundation.
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
#
# Authors: Stein Magnus Jodal <jodal@samfundet.no>
#

import random
import ari.fx.base

class Stars(ari.fx.base.Base):
    """A heaven of stars"""

    def setup(self, min = 1, max = 99, stars = 200):
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
        self.setfps(10)

        # Create stars
        self.stars = []
        for _ in range(self.starcount):
            self.stars.append(Star(self.sizex,
                                   self.sizey,
                                   self.min,
                                   self.max))

    def prepare(self):
        self.canvas.blank()
        self.canvas.flush()

    def run(self):
        while self.runnable:
            if self.drawable:
                for i in range(self.starcount):
                    (x, y, b) = self.stars[i].run()
                    self.canvas.setpixel(x, y, b)
                self.canvas.update()
                self.canvas.flush()
            self.sleep()


class Star:
    def __init__(self, wx, wy, min, max):
        self.min = min
        self.max = random.randint(min, max)

        self.setpos(wx, wy)
        self.b = self.min
        if random.randint(0, 1):
            self.rising = True
        else:
            self.rising = False

    def setpos(self, wx = False, wy = False):
        if wx:
            self.wx = wx
        if wy:
            self.wy = wy
        self.x = random.randint(0, self.wx - 1)
        self.y = random.randint(0, self.wy - 1)

    def run(self):
        # If star is dead, make another one
        if self.b == 0:
            self.setpos()
            #self.b = self.min
            self.rising = True

        # Fade
        if self.rising:
            self.b += random.randint(0, 2)
        else:
            self.b -= random.randint(0, 2)

        # Fade in done, start fade out
        if self.b >= self.max:
            self.b = self.max
            self.rising = False

        # Faded out, clean up
        if not self.rising and self.b <= self.min:
            self.b = 0

        # Return position and brightness
        return (self.x, self.y, self.b)
