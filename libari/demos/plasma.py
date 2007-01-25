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

import libari.demos.base
import math
import numarray
import time

class Plasma(libari.demos.base.Base):
    """Plasma demo"""

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

    def prepare(self):
        #self.setfps(20)
        st = time.time()
        self.plasmas = []
        t = 0
        while t <= math.pi:
            self.plasmas.append(PlasmaFrame(self.config.wallsizex,
                self.config.wallsizey, t))
            t += 0.01
        print "Precalc done in: "  + str(time.time()-st)

    def run(self):
        t = 0
        a = True
        while True:
            if self.drawable:
                self.canvas.update(self.plasmas[t].buffer, 0, 0)
                if a: t += 1
                else: t -= 1
                if t == len(self.plasmas): 
                    a = False
                    t -= 1
                if t == 0: 
                    a = True
                    t += 1
                # It's slow enough without any sleep
                #self.sleep()

class PlasmaFrame:
    def __init__(self, sx, sy, step):
        self.sx = sx
        self.sy = sy
        self.buffer = numarray.zeros((self.sx, self.sy))
        self.generate(step)

    def generate(self, timervalue):
        freq1 = 30.0 + 20.0 * math.sin(timervalue)
        freq2 = 30.0 + 10.0 * math.cos(timervalue*2)
        freq3 = 30.0 + 20.0 * math.sin(freq1)

        shiftx = self.sx * math.sin(timervalue) / 4.0
        shifty = self.sy * math.cos(timervalue) / 4.0

        for y in range(self.sy):
            for x in range(self.sx):
                z1 = math.sin(x / freq1 * 1.7 * math.pi + shiftx)
                z2 = math.cos(x / 3.0 + y / freq2 * 1.5 * math.pi + shifty)
                z3 = math.tan(y / freq3 * 0.1 * math.pi)
                val = math.fabs(z1 + z2 + z3) * 100
                if val > 100:
                    val = 100 
                self.buffer[x][y] = val
