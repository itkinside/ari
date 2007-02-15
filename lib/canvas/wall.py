#! /usr/bin/env python
#
# lib - Library for manipulating a diode wall
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

import lib.canvas.canvas
import lib.canvas.wallnet

class Wall(lib.canvas.canvas.Canvas):
    """Canvas for the physical wall"""

    def __init__(self):
        """
        Setup the Wall object.

        """

        # Init mother
        lib.canvas.canvas.Canvas.__init__(self)

        # Setup output
        self.output = lib.canvas.wallnet.WallNet()

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
        for p in self.config.model:
            for bx in xrange(self.config.model[p]['width']):
                for by in xrange(self.config.model[p]['height']):
                    boards.append((p, bx, by))
        return boards

    def update(self, canvas = None, cx = 0, cy = 0):
        """For doc, see Canvas"""

        # Call mother
        lib.canvas.canvas.Canvas.update(self, canvas, cx, cy)

    def flush(self):
        """For doc, see Canvas"""

        # FIXME: Loop over the canvas instead of all boards?

        # Loop over all boards
        for (p, bx, by) in self.__getallboards():
            # Find board position in canvas
            px = self.config.model[p]['pxpos'] + bx * self.config.boardsizex
            py = by * self.config.boardsizey

            # Init data struct
            data = []

            # Loop over all pixels on the board
            for y in xrange(py, py + self.config.boardsizey):
                for x in xrange(px, px + self.config.boardsizex):
                    # Add brightness value to the data struct
                    data.append(self.wall[x][y])

            # Get address of board
            address = self.config.model[p]['%d,%d' % (bx, by)]

            # Send data to board
            self.output.sendto(data, address)

