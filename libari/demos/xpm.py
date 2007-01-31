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
#
# Authors: Stein Magnus Jodal <jodal@samfundet.no>
#

import gd
import libari.demos.base
import math
import numarray
import os

class XPM(libari.demos.base.Base):
    """
    Draw XPM image at wall.
    """

    def setup(self, imagefile = None):
        if imagefile == None:
            imagefile = 'samfundet-logo.xpm'
        self.image = gd.image(os.getcwd() + '/libari/demos/xpm/' + imagefile)
        (self.iw, self.ih) = self.image.size()
        self.setfps(2)

    def prepare(self):
        self.canvas.blank()
        self.pix = numarray.zeros((self.iw+2, self.ih+2))
        colormap = {}
        for x in xrange(self.iw):
            for y in xrange(self.ih):
                i = self.image.getPixel((x, y))
                if i not in colormap:
                    (r, g, b) = self.image.colorComponents(i)
                    colormap[i] = math.fabs(((r + g + b) * 99 / (3 * 255)) - 99)
                    #colormap[i] = (r + g + b) * 99 / (3 * 255)
                self.pix[x+1][y+1] = colormap[i]
        (self.iw, self.ih) = (self.iw + 2, self.ih + 2)

    def run(self):
        x = 0
        y = 4
        sx = 1
        sy = 1
        while self.runnable:
            if self.drawable:
                x += sx
                y += sy

                self.canvas.update(self.pix, x, y)

                if x == self.sizex - self.iw:
                    sx = -1
                if x == 0:
                    sx = 1

                if y == 6:
                    sy = -1
                elif y == 0:
                    sy = +1

                self.sleep()
