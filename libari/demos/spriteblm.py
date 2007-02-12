#! /usr/bin/env python
#
# Sprite demo for BlinkenLights Movies for libari
# Copyright (C) 2007 Stein Magnus Jodal
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

import libari.blmreader
import libari.demos.sprite

class SpriteBLM(libari.demos.sprite.Sprite):
    """
    Draw BlinkenLights Movie at wall. Extends the general sprite demo.

    """

    def setup(self, dx = 0, dy = 0, blmfile = None):
        """
        Input (inherited from sprite):
            dx          Speed in horisontal direction, default 1
            dy          Speed in vertical direction, default 1

        Input (custom for BLM):
            blmfile     BlinkenLights Movie to play, must recide in media/blm

        """

        # Default BLM
        if blmfile == None:
            dx = 0
            dy = 0
            blmfile = 'camel.blm'
        self.blmfile = blmfile

        # Call parent
        libari.demos.sprite.Sprite.setup(self, dx, dy)

    def prepare(self):
        # Call parent
        libari.demos.sprite.Sprite.prepare(self)

        # Load BLM
        blmr = libari.blmreader.BLMReader()
        self.frames = blmr.load('media/blm/%s' % self.blmfile)

        # Find sprite size by looking at first frame
        (_, frame) = self.frames[0]
        (self.spritew, self.spriteh) = frame.shape

    def run(self):
        # Call parent
        libari.demos.sprite.Sprite.run(self)
