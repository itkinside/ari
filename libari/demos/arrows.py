#! /usr/bin/env python
#
# arrows demo for libari - Library for manipulating a diode wall
# Copyright (C) 2006 Kristian Klette
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
# Authors: Kristian Klette <klette@samfundet.no>

import libari.demos.base
import math

class Arrows(libari.demos.base.Base):
    """A test to see how slow Python is"""

    def buildRow(self, yRow, step):
        pattern = [40, 60, 99, 99, 0, 0, 0, 0]
        row = pattern * (self.config.wallsizex / len(pattern));
        if yRow < math.ceil(self.config.wallsizey / 2):
            for _ in range(yRow + step):
                row.insert(0, row.pop())
        else:
            nonzero = 0
            for p in pattern:
                if p > 0:
                    nonzero += 1
            for _ in range(nonzero):
                row.append(row[0])
                del row[0]
            for _ in range(yRow - step):
                row.append(row[0])
                del row[0]
        return row

    def run(self):
        step = 0
        while self.runnable:
            if self.drawable:
                for y in range(self.config.wallsizey):
                    curRow = self.buildRow(y, step)
                    for x in range(self.config.wallsizex):
                        try:
                            self.canvas.setpixel(x, y, curRow[x])
                        except:
                            pass
                
                self.canvas.update()
                step += 1
                if step > (self.config.wallsizey/2): step = 0
