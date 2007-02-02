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

    def setup(self, imagefile = None, fps = 1, dx = 1, dy = 1, invert = False):
        """
        Input:
            imagefile   Image to display, must recide in libari/demos/xpm
            fps         Frames per second, default 1
            dx          Speed in horisontal direction, default 1
            dy          Speed in vertical direction, default 1
            invert      Invert image colors, default False

        """

        # Default image
        if imagefile == None:
            imagefile = 'samfundet-logo.xpm'
            fps = 5
            invert = True

        # Check input
        if str(fps).isdigit() and fps > 0:
            self.fps = fps
        else:
            self.fps = 1
        if str(dx).isdigit() and dx >= 0:
            self.dx = dx
        else:
            self.dx = 1
        if str(dy).isdigit() and dy >= 0:
            self.dy = dy
        else:
            self.dy = 1
        if invert == True or invert == False:
            self.invert = invert
        else:
            self.invert = False

        # Load image
        self.image = gd.image(os.getcwd() + '/libari/demos/xpm/' + imagefile)
        (self.iw, self.ih) = self.image.size()

        # Set update frequency
        self.setfps(self.fps)

    def prepare(self):
        # Blank wall
        self.canvas.blank()
        self.canvas.update()

        # Array the same size as the image
        self.pix = numarray.zeros((self.iw, self.ih))
        self.pixblank = numarray.zeros((self.iw, self.ih))

        # Color convertion map
        colormap = {}

        # Convert image to brightness values
        for x in xrange(self.iw):
            for y in xrange(self.ih):
                i = self.image.getPixel((x, y))

                # Add new colors to colormap
                if i not in colormap:
                    (r, g, b) = self.image.colorComponents(i)
                    colormap[i] = (r + g + b) * 99 / (3 * 255)

                    # Invert color
                    if self.invert:
                        colormap[i] = math.fabs(colormap[i] - 99)

                # Fill array with brightness values
                self.pix[x][y] = colormap[i]

    def run(self):
        # The demo

        # Start position
        x = y = 0
        dx = self.dx
        dy = self.dy

        while self.runnable:
            if self.drawable:
                # Clear previous position
                self.canvas.update(self.pixblank, x, y)

                # Move image
                x += dx
                y += dy

                # Paint image
                self.canvas.update(self.pix, x, y)

                # Flush updates to wall
                self.canvas.flush()

                # Boundary checks
                if x == 0 or x == self.sizex - self.iw:
                    dx *= -1
                if y == 0 or y == self.sizey - self.ih:
                    dy *= -1

                # Take a nap
                self.sleep()
