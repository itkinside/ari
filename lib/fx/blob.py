#! /usr/bin/env python
#
# Copyright (C) 2006 Thomas Adamcik, Stein Magnus Jodal
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
# Authors: Thomas Adamcik <adamcik@samfundet.no>
#          Stein Magnus Jodal <jodal@samfundet.no>
#

import lib.fx.base
from Numeric import zeros
from random import randint

class Blob(lib.fx.base.Base):
    """Blob demo"""

    def setup(self):
        self.colors = zeros((self.sizex, self.sizey))
        self.blob = OneBlob(5, self.sizex, self.sizey, self.colors, self.canvas)
        self.i1 = Iter(randint(0, self.sizex), randint(0, self.sizey),
            self.sizex, self.sizey, self.blob, self.canvas)
        self.i2 = Iter(randint(0, self.sizex), randint(0, self.sizey),
            self.sizex, self.sizey, self.blob, self.canvas)
        self.i3 = Iter(randint(0, self.sizex), randint(0, self.sizey),
            self.sizex, self.sizey, self.blob, self.canvas)
        self.i4 = Iter(randint(0, self.sizex), randint(0, self.sizey),
            self.sizex, self.sizey, self.blob, self.canvas)

    def prepare(self):
        self.canvas.blank()
        self.canvas.flush()

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
        for _ in range(p):
            if old:
                self.blob.draw(old[0], old[1], 0, p)
            self.blob.draw(x, y, 1, p)
            self.canvas.update()
            self.canvas.flush()
        self.x = x
        self.y = y
