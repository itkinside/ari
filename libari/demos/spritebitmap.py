#! /usr/bin/env python
#
# Sprite demo for bitmaps for libari
# Copyright (C) 2006-2007 Stein Magnus Jodal
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
import libari.demos.sprite
import math
import numarray

class SpriteBitmap(libari.demos.sprite.Sprite):
    """
    Draw bitmap sprite at wall. Extends the general sprite demo.

    """

    def setup(self, dx = 1, dy = 1, imagefile = None, fps = 1, invert = False):
        """
        Input (inherited from sprite):
            dx          Speed in horisontal direction, default 1
            dy          Speed in vertical direction, default 1

        Input (custom for bitmap):
            imagefile   Image to display, must recide in media/bitmap
            fps         Frames per second, default 1
            invert      Invert image colors, default False

        """

        # Default image
        if imagefile == None:
            dx = 1
            dy = 1
            fps = 5
            imagefile = 'samfundet-logo.xpm'
            invert = True

        # Call parent
        libari.demos.sprite.Sprite.setup(self, dx, dy)

        # Check input
        if str(fps).isdigit() and fps > 0:
            self.fps = fps
        else:
            self.fps = 1

        if invert == True or invert == False:
            self.invert = invert
        else:
            self.invert = False

        # Load image
        self.image = gd.image('media/bitmap/%s' % imagefile)
        (self.spritew, self.spriteh) = self.image.size()

    def prepare(self):
        # Call parent
        libari.demos.sprite.Sprite.prepare(self)

        # Sprite the same size as the image
        sprite = numarray.zeros((self.spritew, self.spriteh))

        # Color convertion map
        colormap = {}

        # Convert image to brightness values
        for x in xrange(self.spritew):
            for y in xrange(self.spriteh):
                i = self.image.getPixel((x, y))

                # Add new colors to colormap
                if i not in colormap:
                    (r, g, b) = self.image.colorComponents(i)
                    colormap[i] = (r + g + b) * 99 / (3 * 255)

                    # Invert color
                    if self.invert:
                        colormap[i] = math.fabs(colormap[i] - 99)

                # Fill array with brightness values
                sprite[x][y] = colormap[i]
        
        # Only got one frame
        self.frames.append((1000 / self.fps, sprite))

    def run(self):
        # Call parent
        libari.demos.sprite.Sprite.run(self)
