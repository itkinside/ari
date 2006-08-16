#! /usr/bin/env python
#
# Martha - Diode wall simulator
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

import random
import time

import libari.config
import simulator

config = libari.config.Config()
sim = simulator.Simulator()

while True:
    for b in range(40, 100, 3) + range(99, 40, -3):
        for x in range(config.wallsizex):
            if x % config.boardsizex == 0 \
                or x % config.boardsizex == config.boardsizex - 1:
                for y in range(config.wallsizey):
                    sim.setpixel(x, y, b)
            else:
                sim.setpixel(x, 0, b)
                sim.setpixel(x, config.wallsizey - 1, b)
        sim.update()
        time.sleep(0.02)
