#! /usr/bin/env python
#
# libari - Library for manipulating a diode wall
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

import libari.config
import numarray

class Canvas:
    """Interface for modules implementing a canvas"""

    def __init__(self):
        """
        Setup the Canvas object.

        """

        # Load config
        self.config = libari.config.Config()

        # Local canvas for get/setpixel
        self.canvasw = self.config.wallsizex
        self.canvash = self.config.wallsizey
        self.canvas = numarray.zeros((self.canvasw, self.canvash))

        # What is displayed at the wall right now
        self.wall = self.canvas

    def getpixel(self, x, y):
        """
        Get brightness of pixel at pos x,y

        Input:
            x   Position in canvas, x direction
            y   Position in canvas, y direction

        Returns:
            b   Brightness of pixel

        Raises:
            CanvasOutOfBoundsException

        """

        # Check boundaries
        if x < 0 or x >= self.canvasw:
            raise CanvasOutOfBoundsException, \
                "getpixel: x is out of bounds: (%d, %d)" % (x, y)
        if y < 0 or y >= self.canvash:
            raise CanvasOutOfBoundsException, \
                "getpixel: y is out of bounds: (%d, %d)" % (x, y)

        # Return brightness
        return self.canvas[x][y]

    def setpixel(self, x, y, b, o = 100):
        """
        Set brightness of pixel at pos x,y

        Input:
            x   Position in canvas, x direction
            y   Position in canvas, y direction
            b   Brightness (0-99)
            o   Opacity (0-100), default 100

        Returns:
            b   Brightness of pixel, adjusted for opacity

        Raises:
            CanvasOutOfBoundsException

        """

        # Check boundaries
        if x < 0 or x >= self.canvasw:
            raise CanvasOutOfBoundsException, \
                "setpixel: x is out of bounds: (%d, %d)" % (x, y)
        if y < 0 or y >= self.canvash:
            raise CanvasOutOfBoundsException, \
                "setpixel: y is out of bounds: (%d, %d)" % (x, y)
        if b < 0:
            b = 0
        elif b > 99:
            b = 99
        if o < 0:
            o = 0
        elif o > 100:
            o = 100

        # Opacity
        if o < 100:
            b = int(self.canvas[x][y] * (100.0 - o) / 100.0 \
                    + b * o / 100.0)

        # Set brightness
        self.canvas[x][y] = b
        return b

    def update(self, canvas = None, cx = 0, cy = 0):
        """
        Paint the canvas on the wall

        Input:
            canvas  Canvas array with brightness values, optional
            cx      Position of canvas on wall, x direction, optional
            cy      Position of canvas on wall, y direction, optional

        """

        if canvas is None:
            # Use get/setpixel canvas
            self.wall = self.canvas
            self.cw = 0
            self.ch = 0
        else: 
            # Use supplied canvas
            (self.cw, self.ch) = canvas.shape
            if (cx == 0 and cy == 0 and
                self.cw == self.canvasw and self.ch == self.canvash):
                # Full size canvas, just copy
                self.wall = canvas
            else:
                # Add canvas to wall
                for x in xrange(self.cw):
                    for y in xrange(self.ch):
                        self.wall[cx+x][cy+y] = canvas[x][y]

        # Implement the acctual painting in the children

    def blank(self, b = 0):
        """
        Blank entire wall

        Input:
            b   Brightness, default 0

        """

        # Loop over all pixels and set brightness
        for x in xrange(self.canvasw):
            for y in xrange(self.canvash):
                self.canvas[x][y] = b
        self.update()

class CanvasException(Exception):
    """Base class for all exceptions raised by canvas."""

class CanvasOutOfBoundsException(CanvasException):
    """Raised when trying to access areas outside the canvas."""
