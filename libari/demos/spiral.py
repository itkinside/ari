#! /usr/bin/env python
#
# Spiral demo for libari
# Copyright (C) 2006 Vidar Wahlberg
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
#
# Authors: Vidar Wahlberg <canidae@samfundet.no>
#

import libari.demos.base
import math

class Spiral(libari.demos.base.Base):
    """A spiral!"""

    def findxy(self, n):
        if n == 0:
            self.x = 0
            self.y = 0
            return
        d = (math.sqrt(n) + 1.0) / 2.0
        m = int(d) * 2
        c = n - (m - 1) * (m - 1)
        if c < m:
            self.x = int(d)
            self.y = 1 - int(d) + c % m
        elif c < 2 * m:
            self.x = int(d) - 1 - c % m
            self.y = int(d)
        elif c < 3 * m:
            self.x = int(-d)
            self.y = int(d) - 1 - c % m
        elif c < 4 * m:
            self.x = 1 - int(d) + c % m
            self.y = int(-d)

    def run(self):
        # The demo
        while self.runnable:
            if self.drawable:
                for n in xrange(500):
                    self.findxy(n)
                    self.image[self.x + 25][self.y + 15] = n % 80 + 20
                    self.findxy((n + 450) % 500)
                    self.image[self.x + 25][self.y + 15] = 0
                    self.canvas.update(self.image)
                    self.canvas.flush()
#            self.sleep()
