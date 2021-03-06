#! /usr/bin/env python
#
# Copyright (C) 2007 Stein Magnus Jodal
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

import math
import numpy
import time
import pickle
import os

import ari.fx.base

class Plasma(ari.fx.base.Base):
    """Plasma demo"""

    def setup(self):
        # Precalc
        self.plasmas = []
        cachefilename = '%s/plasma.pickle' % self.config.cachedir
        if not os.path.isfile(cachefilename):
            # Precalc frames
            st = time.time()
            t = 0
            while t <= 2 * math.pi:
                self.plasmas.append(PlasmaFrame(self.sizex, self.sizey, t))
                t += 0.03
            pickle.dump(self.plasmas, open(cachefilename, 'w'))
            print "Precalc: %3.3fs" % (time.time() - st)
        else:
            # Load saved frames
            self.plasmas = pickle.load(open(cachefilename, 'r'))

        self.setfps(15)

    def run(self):
        t = 0
        while self.runnable:
            if self.drawable:
                self.canvas.update(self.plasmas[t].buffer, 0, 0)
                self.canvas.flush()
                t += 1
                if t == len(self.plasmas):
                    t = 0
                self.sleep()

class PlasmaFrame:
    def __init__(self, sx, sy, step):
        self.sx = sx
        self.sy = sy
        self.buffer = numpy.zeros((self.sx, self.sy), dtype=int)
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
                z2 = math.sin(x / 3.0 + y / freq2 * 1.5 * math.pi + shifty)
                z3 = math.sin(y / freq3 * 0.1 * math.pi)
                val = math.fabs(z1 + z2 + z3) * 99
                if val > 99:
                    val = 99 
                self.buffer[x][y] = val
