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

import math

class Canvas:
    """Paint on the canvas, and the wall shows your art!"""

    def __init__(self, output):
        """
        Setup the Canvas object.

        Input:
            output  Output object, e.g. Wall

        """

        # Read input
        self.output = output

        # Get config object from output class
        self.config = self.output.config

        # Build canvas
        self.canvas = self.__createcanvas()

    def __createcanvas(self):
        """
        Create a canvas for storing brightness values

        """

        canvas = {}
        for p in self.config.model:
            panel = self.config.model[p]
            canvas[p] = {}
            for bx in range(panel['width']):
                canvas[p][bx] = {}
                for by in range(panel['height']):
                    canvas[p][bx][by] = {}
                    for px in range(5):
                        canvas[p][bx][by][px] = {}
                        for py in range(5):
                            canvas[p][bx][by][px][py] = 0
        return canvas

    def __getcanvaspos(self, x, y):
        """
        Get position in canvas struct, given position in canvas

        Input:
            x   Position in canvas, x direction
            y   Position in canvas, y direction

        Return:
            A tuple containing the following five values:
            p   Panel number
            bx  Board position, x direction
            by  Board position, y direction
            px  Pixel position, x direction
            py  Pixel position, y direction

        """

        # Find panel
        p = 0
        dx = 0
        for p in range(len(self.config.model)):
            dx += self.config.model[p]['width'] * self.config.boardsizex
            if x < dx:
                dx -= self.config.model[p]['width'] * self.config.boardsizex
                break

        # Find board positions
        bx = int(math.floor((x - dx) / self.config.boardsizex))
        by = int(math.floor(y / self.config.boardsizey))

        # Find pixel positions
        px = (x - dx) % self.config.boardsizex
        py = y % self.config.boardsizey

        return (p, bx, by, px, py)

    def __getallboards(self):
        """
        Get a list of all boards.

        Returns:
            A list of boards, one tuple per board, containing:
            p   Panel number
            bx  Board position, x direction
            by  Board position, y direction

        """

        boards = []
        for p in self.canvas:
            for bx in self.canvas[p]:
                for by in self.canvas[p][bx]:
                    boards.append((p, bx, by))
        return boards

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

        if x < 0 or x >= self.wallsizex or y < 0 or y >= self.wallsizey:
            return False
        
        (p, bx, by, px, py) = self.__getcanvaspos(x, y)
        return self.canvas[p][bx][by][px][py]

    def setpixel(self, x, y, b):
        """
        Set brightness of pixel at pos x,y

        Input:
            x   Position in canvas, x direction
            y   Position in canvas, y direction

        Returns:
            True if brightness is set 
            False if pixel is outside the canvas

        """

        if x < 0 or x >= self.wallsizex or y < 0 or y >= self.wallsizey:
            return False

        (p, bx, by, px, py) = self.getcanvaspos(x, y)
        self.canvas[p][bx][by][px][py] = b
        return True

    def update(self):
        """
        Paint the canvas to the wall

        Only boards with changed pixels are updated

        Returns:
            n   Number of boards updated
        """

        # Loop over all boards
        n = 0
        for board in self.__getallboards():
            # Read board position
            (p, bx, by) = board

            # Init data struct
            data = []
            # Loop over all pixels on the board
            for px in range(self.config.boardsizex):
                for py in range(self.config.boardsizey):
                    # Add brightness value to the data struct
                    data.append(self.canvas[p][bx][by][px][py])

            # Get address of board
            host = self.config.model[p]['%d,%d' % (bx, by)]

            # Send data to board
            self.output.sendto(data, host)
            n += 1

        return n

    def blank(self, b = 0):
        """
        Blank entire wall

        Input:
            b   Brightness, default 0

        Returns:
            b   Brightness
            n   Number of boards updated
        """

        # Build data struct
        data = []
        for i in range(self.config.boardsizex * self.config.boardsizey):
            data.append(b)

        # Loop over all boards
        n = 0
        for board in self.__getallboards():
            # Read board position
            (p, bx, by) = board

            # Get address of board
            host = self.config.model[p]['%d,%d' % (bx, by)]

            # Send data to board
            self.output.sendto(data, host)
            n += 1

        return (b, n)
