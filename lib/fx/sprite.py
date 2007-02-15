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

import lib.fx.base
import numarray

class Sprite(lib.fx.base.Base):
    """
    Draw sprite image at wall. This is not a demo, but a framework for other
    sprite demos.

    """

    def setup(self, dx = 1, dy = 1):
        """
        Input:
            dx          Speed in horisontal direction, default 1
            dy          Speed in vertical direction, default 1

        """

        # Set defaults
        self.startx = 0
        self.starty = 0
        self.spritew = 0
        self.spriteh = 0

        # Check input
        if str(dx).isdigit() and dx >= 0:
            self.dx = dx
        else:
            self.dx = 1

        if str(dy).isdigit() and dy >= 0:
            self.dy = dy
        else:
            self.dy = 1

    def prepare(self):
        # Blank wall
        self.canvas.blank()
        self.canvas.update()

        # Sprite frames
        # Fill this list with tuples for frame duration in millisecs and the
        # numarrays with the frame data.
        self.frames = []

        # Get frames (done in the children)

    def run(self):
        # The demo

        # Start position
        frameindex = 0
        x = self.startx
        y = self.starty
        dx = self.dx
        dy = self.dy

        # Blanking frame
        blankframe = numarray.zeros((self.spritew, self.spriteh))

        while self.runnable:
            if self.drawable:
                # Clear previous position
                self.canvas.update(blankframe, x, y)

                # Move frame
                x += dx
                y += dy

                # Select next frame
                if frameindex + 1 < len(self.frames):
                    frameindex += 1
                else:
                    frameindex = 0

                # Paint frame
                (frameduration, frame) = self.frames[frameindex]
                self.setfps(1000.0 / frameduration)
                self.canvas.update(frame, x, y)

                # Flush updates to wall
                self.canvas.flush()

                # Boundary checks
                if x == 0 or x == self.sizex - self.spritew:
                    dx *= -1
                if y == 0 or y == self.sizey - self.spriteh:
                    dy *= -1

                # Take a nap
                self.sleep()
