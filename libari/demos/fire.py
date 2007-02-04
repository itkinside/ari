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
import random

class Fireball:
    
    def __init__(self, col, canvas):
        self.step = 0
        self.col = col
        self.canvas = canvas
        self.toStep = random.randint(2,30)
        self.step = random.randint(5,10)
        self.deadStep = 0
        self.init_pattern = [random.randint(0,99), random.randint(0,99), random.randint(0,99), random.randint(0,99), random.randint(0,99), random.randint(0,99), random.randint(0,99), random.randint(0,99), random.randint(30,99), random.randint(30,99), random.randint(30,99), random.randint(30,99), random.randint(40,99), random.randint(40,99), random.randint(40,99), random.randint(40,99), random.randint(50,99), random.randint(50,99), random.randint(50,99), random.randint(60,99), random.randint(60,99), random.randint(60,99), random.randint(60,99), random.randint(60,99), random.randint(70,99), random.randint(70,99), random.randint(70,99)]
        self.pattern = self.init_pattern
        
    def draw(self):
        for val in xrange(len(self.pattern)):
            try:
                self.canvas.setpixel(self.col, self.step+val, self.pattern[val])
            except:
                pass
            
        self.pattern.append(self.pattern[0])
        del(self.pattern[0])
        
        if self.step >= self.toStep:
            for val in xrange(len(self.pattern)):
                self.pattern[val] = self.pattern[val]/2
            self.deadStep += 1
        if self.deadStep == 3:
            self.__init__(self.col, self.canvas)


class Fire(libari.demos.base.Base):
    """A test to see how slow Python is"""

    def setup(self):
        self.drops = []
        for x in xrange(self.config.wallsizex):
            self.drops.append(Fireball(x, self.canvas))
            
    def run(self):
        while self.runnable:
            if self.drawable:
                for drop in self.drops:
                    drop.draw()
                    self.canvas.update()
                    self.canvas.flush()
