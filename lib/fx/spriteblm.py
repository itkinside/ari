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

import lib.reader.blm
import lib.fx.sprite
import lib.utils.array

class SpriteBLM(lib.fx.sprite.Sprite):
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
        lib.fx.sprite.Sprite.setup(self, dx, dy)

        # Set offset
        # FIXME: Camel hack
        self.startx = 15
        self.starty = 7

    def prepare(self):
        # Call parent
        lib.fx.sprite.Sprite.prepare(self)

        # Load BLM
        blmr = lib.reader.blm.BLMReader()
        self.frames = blmr.load('media/blm/%s' % self.blmfile)

        # Scale frames
        # FIXME: This is the wrong place to do it
        for i, frame in enumerate(self.frames):
            (duration, array) = frame
            self.frames[i] = (duration,
              lib.utils.array.growtobox(array,
                self.config.model[1]['width'] * self.config.boardsizex,
                self.sizey));

        # Find sprite size by looking at first frame
        (_, frame) = self.frames[0]
        (self.spritew, self.spriteh) = frame.shape

    def run(self):
        # Call parent
        lib.fx.sprite.Sprite.run(self)
