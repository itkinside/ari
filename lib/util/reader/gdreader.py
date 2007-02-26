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

import gd
from lib.util.dict import *
from lib.util.reader import Reader, ReaderException
import math
import numarray

class GDReader(Reader):
    """Reader for GD supported formats"""

    def parse(self, *args, **kwargs):
        """Loads and parses a BML file. See parent for more doc."""

        kwargs = explode_kwargs(kwargs)

        try:
            duration = kwargs['duration']
        except:
            duration = 1000.0

        try:
            invert = kwargs['invert']
        except:
            invert = False

        # Load image
        image = gd.image(kwargs['filepath'])

        frames = []
        (framew, frameh) = image.size()

        frame = numarray.zeros((framew, frameh))
        colormap = {}

        # Convert image to brightness values
        for x in xrange(framew):
            for y in xrange(frameh):
                i = image.getPixel((x, y))

                # Add new colors to colormap
                if i not in colormap:
                    (r, g, b) = image.colorComponents(i)
                    colormap[i] = (r + g + b) * 99 / (3 * 255)

                    # Invert color
                    if invert:
                        colormap[i] = math.fabs(colormap[i] - 99)

                # Fill array with brightness values
                frame[x][y] = colormap[i]

        # Frame done
        frames.append((duration, frame))

        # Movie done
        return frames
