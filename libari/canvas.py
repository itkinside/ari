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

class Canvas:
    """Interface for modules implementing a canvas"""

    def __init__(self):
        """
        Setup the Canvas object.

        """

        # Load config
        self.config = libari.config.Config()

    def getpixel(self, x, y):
        """
        Get brightness of pixel at pos x,y

        Input:
            x   Position in canvas, x direction
            y   Position in canvas, y direction

        Returns:
            b   Brightness of pixel
            False if pixel is outside the canvas

        """

        raise CanvasException, "Not Implemented"

    def setpixel(self, x, y, b, o = 100):
        """
        Set brightness of pixel at pos x,y

        Input:
            x   Position in canvas, x direction
            y   Position in canvas, y direction
            o   Opacity (0-100), default 100

        Returns:
            True if brightness is set 
            False if pixel is outside the canvas

        """

        raise CanvasException, "Not Implemented"

    def update(self):
        """
        Paint the canvas to the wall

        Only boards with changed pixels are updated.

        """

        raise CanvasException, "Not Implemented"

    def blank(self, b = 0):
        """
        Blank entire wall

        Also updates the canvas with the new state of the wall.

        Input:
            b   Brightness, default 0

        """

        raise CanvasException, "Not Implemented"

class CanvasException(Exception):
    """Base class for all exceptions raised by canvas."""

class CanvasOutOfBoundsException(CanvasException):
    """Raised when trying to access areas outside the canvas."""
