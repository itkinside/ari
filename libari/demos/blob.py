#! /usr/bin/env python
#
# arid - Daemon for running demos on a diode wall 
# Copyright (C) 2006 Thomas Adamcik, Stein Magnus Jodal
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
# Authors: Thomas Adamcik <adamcik@samfundet.no>
#          Stein Magnus Jodal <jodal@samfundet.no>
#

import libari.demos.base
from Numeric import zeros
from random import randint

class Blob(libari.demos.base.Base):
    """Blob demo"""

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

        w = self.config.wallsizex
        h = self.config.wallsizey

        self.colors = zeros((w, h))
        self.blob = OneBlob(5, w, h, self.colors, self.canvas)
        self.i1 = Iter(randint(0, w), randint(0, h),
            w, h, self.blob, self.canvas)
        self.i2 = Iter(randint(0, w), randint(0, h),
            w, h, self.blob, self.canvas)
        self.i3 = Iter(randint(0, w), randint(0, h),
            w, h, self.blob, self.canvas)
        self.i4 = Iter(randint(0, w), randint(0, h),
            w, h, self.blob, self.canvas)

    def prepare(self):
        self.canvas.blank()

    def run(self):
        while self.runnable:
            if self.drawable:
                self.i1.move(3)
                self.i2.move(3)
                self.i3.move(3)
                self.i4.move(3)

class OneBlob:
    def __init__(self, r, w, h, colors, canvas):
        self.r = r
        self.w = w
        self.h = h
        self.colors = colors
        self.canvas = canvas
        x = r
        y = r
        blob = zeros((r*2, r*2))
        tx = 0
        ty = 0

        for a in range(r*2):
            for b in range(r*2):
                i =  pow(pow(x-a,2) + pow(y-b,2),0.5)
                if i < r:
                    if i != 0:
                        blob[a][b] += 1 / i * r * 10
                    else:
                        tx = a
                        ty = b

        blob[tx][ty] = (blob[tx][ty-1] + blob[tx-1][ty]
            + blob[tx+1][ty] + blob[tx][ty+1]) / 4
        self.blob = blob
        
    def draw(self, x, y, add=1, p=1):
        r = self.r
        x -=r
        y -=r

        for a in range(r*2):
            for b in range(r*2):
                if x+a >= 0 and y+b >= 0 and x+a < self.w and y+b < self.h:
                    if add:
                        self.colors[x+a][y+b] += self.blob[a][b] / p
                    else:
                        self.colors[x+a][y+b] -= self.blob[a][b] / p

                    if self.colors[x+a][y+b] < 99:
                        self.canvas.setpixel(x+a, y+b, self.colors[x+a][y+b])
                    else:
                        self.canvas.setpixel(x+a, y+b, 99)

class Iter:
    def __init__(self, x, y, w, h, blob, canvas):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.blob = blob
        self.canvas = canvas
        self.coords = []

    def move(self, p=1):
        x = self.x + randint(-10,10)
        y = self.y + randint(-10,10)

        if x < 0:
            x = self.w
        elif x > self.w:
            x = self.h

        if y < 0:
            y = self.h
        elif y > self.h:
            y = 0

        old = 0
        self.coords.append((x, y))
        if len(self.coords) > 20:
            old = self.coords.pop(0)
        for i in range(p):
            if old:
                self.blob.draw(old[0], old[1], 0, p)
            self.blob.draw(x, y, 1, p)
            self.canvas.update()
        self.x = x
        self.y = y
