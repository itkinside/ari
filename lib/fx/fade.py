#! /usr/bin/env python
#
# Fade demo for lib
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
#
# Authors: Stein Magnus Jodal <jodal@samfundet.no>
#

import lib.fx.base

class Fade(lib.fx.base.Base):
    """Fade between to brightness values."""

    def setup(self, min = 0, max = 99, step = 3):
        """
        Input:
            min     Minimum brightness, default 0
            max     Maximum brightness, default 99
            step    Brightness steps, default 3
        """

        # Check input
        if int(min) >= 0 and int(min) < 100:
            self.min = int(min)
        else:
            self.min = 0

        if int(max) >= 0 and int(min) < 100:
            self.max = int(max)
        else:
            self.max = 99

        if self.min > self.max:
            self.min, self.max = self.max, self.min

        if int(step) < 99:
            self.step = step
        else:
            self.step = 3

    def run(self):
        while self.runnable:
            if self.drawable:
                for b in range(self.min, self.max, self.step):
                    self.canvas.blank(b)
                    self.canvas.flush()
                    self.sleep()
                for b in range(self.max, self.min, -self.step): 
                    self.canvas.blank(b)
                    self.canvas.flush()
                    self.sleep()
