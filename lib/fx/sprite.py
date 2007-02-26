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
import lib.utils.array
import lib.utils.reader
import numarray

class Sprite(lib.fx.base.Base):
    """
    Draw sprite image at wall. This is not a demo, but a framework for other
    sprite demos.

    """

    def setup(self, filepath, dx = 0, dy = 0, fps = False,
              invert = False, scale = False):
        """
        Input:
            filepath    Path to media file
            dx          Speed in horisontal direction, default 0
            dy          Speed in vertical direction, default 0
            fps         Frames per second, default False
            invert      Invert colors, default False
            scale       Scale, default False, n for ratio, (w, h) for grow to
                        fit box while keeping proportions

        """

        # Set defaults
        self.startx = 0
        self.starty = 0
        self.framew = 0
        self.frameh = 0

        # Check input
        if str(dx).isdigit() and dx >= 0:
            self.dx = dx
        else:
            self.dx = 1

        if str(dy).isdigit() and dy >= 0:
            self.dy = dy
        else:
            self.dy = 1

        if str(fps).isdigit() and fps > 0:
            self.fps = fps
        else:
            self.fps = 1

        if type(invert) == type(True):
            self.invert = invert
        else:
            self.invert = False

        # Load media
        reader = lib.utils.reader.Reader()
        self.frames = reader.load(filepath=filepath,
                                  duration=(1000.0 / self.fps),
                                  invert=self.invert)

        # Scale frames
        if type(scale) == int:
            # With ratio
            ratio = scale
            for i, frame in enumerate(self.frames):
                (duration, array) = frame
                self.frames[i] = (duration,
                                  lib.utils.array.scale(array, ratio));
        elif type(scale) == tuple:
            # Grow to fit box
            (w, h) = scale
            for i, frame in enumerate(self.frames):
                (duration, array) = frame
                self.frames[i] = (duration,
                                  lib.utils.array.growtobox(array, w, h));

        # Find frame size by looking at first frame
        (_, frame) = self.frames[0]
        (self.framew, self.frameh) = frame.shape

    def prepare(self):
        # Blank wall
        self.canvas.blank()
        self.canvas.update()

    def run(self):
        # The demo

        # Start position
        frameindex = 0
        x = self.startx
        y = self.starty
        dx = self.dx
        dy = self.dy

        # Blanking frame
        blankframe = numarray.zeros((self.framew, self.frameh))

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
                if x == 0 or x == self.sizex - self.framew:
                    dx *= -1
                if y == 0 or y == self.sizey - self.frameh:
                    dy *= -1

                # Take a nap
                self.sleep()
