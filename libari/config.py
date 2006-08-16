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

class Config:
    """A very simple form of config file. ;-)"""

    def __init__(self):
        """
        Setup the Config object.

        """

        # First three parts of the IP addresses of the boards
        self.hostprefix = '192.168.0.'

        # Number of pixels on one board, x and y direction
        self.boardsizex = 5
        self.boardsizey = 5

        # Simulator settings
        self.simpixelsize = 2
        self.simpixeldistance = 6

        # A model of the physical and logical layout of the wall
        #
        # Panels
        #   xpos    Physical position of panel, x direction, in boards
        #   ypos    Physical position of panel, y direction, in boards
        #   width   Width of panel, in boards
        #   height  Height of panel, in boards
        #
        # Boards (30x30cm)
        #   x,y: ip Position of boards with last part of IP address
        #
        # Everything is 0-indexed from the upper left corner
        #
        self.model = {
            0: {
                'xpos': 0,
                'ypos': 0,
                'width': 2,
                'height': 6,
                '0,0': 12, '1,0': 13,
                '0,1': 10, '1,1': 11,
                '0,2':  8, '1,2':  9,
                '0,3':  6, '1,3':  7,
                '0,4':  4, '1,4':  5,
                '0,5':  2, '1,5':  3
            },
            1: {
                'xpos': 7,
                'ypos': 0,
                'width': 9,
                'height': 6,
                '0,0': 59, '1,0': 60, '2,0': 61, '3,0': 62, '4,0': 63,
                    '5,0': 64, '6,0': 65, '7,0': 66, '8,0': 67,
                '0,1': 50, '1,1': 51, '2,1': 52, '3,1': 53, '4,1': 54,
                    '5,1': 55, '6,1': 56, '7,1': 57, '8,1': 58,
                '0,2': 41, '1,2': 42, '2,2': 43, '3,2': 44, '4,2': 45,
                    '5,2': 46, '6,2': 47, '7,2': 48, '8,2': 49,
                '0,3': 32, '1,3': 33, '2,3': 34, '3,3': 35, '4,3': 36,
                    '5,3': 37, '6,3': 38, '7,3': 39, '8,3': 40,
                '0,4': 23, '1,4': 24, '2,4': 25, '3,4': 26, '4,4': 27,
                    '5,4': 28, '6,4': 29, '7,4': 30, '8,4': 31,
                '0,5': 14, '1,5': 15, '2,5': 16, '3,5': 17, '4,5': 18,
                    '5,5': 19, '6,5': 20, '7,5': 21, '8,5': 22
            },
            2: {
                'xpos': 25,
                'ypos': 0,
                'width': 3,
                'height': 6,
                '0,0': 83, '1,0': 84, '2,0': 85,
                '0,1': 80, '1,1': 81, '2,1': 82,
                '0,2': 77, '1,2': 78, '2,2': 79,
                '0,3': 74, '1,3': 75, '2,3': 76,
                '0,4': 71, '1,4': 72, '2,4': 73,
                '0,5': 68, '1,5': 69, '2,5': 70
            },
            3: {
                'xpos': 49,
                'ypos': 0,
                'width': 6,
                'height': 6,
                '0,0': 116, '1,0': 117, '2,0': 118, '3,0': 119, '4,0': 120,
                    '5,0': 121,
                '0,1': 110, '1,1': 111, '2,1': 112, '3,1': 113, '4,1': 114,
                    '5,1': 115,
                '0,2': 104, '1,2': 105, '2,2': 106, '3,2': 107, '4,2': 108,
                    '5,2': 109,
                '0,3':  98, '1,3':  99, '2,3': 100, '3,3': 101, '4,3': 102,
                    '5,3': 103,
                '0,4':  92, '1,4':  93, '2,4':  94, '3,4':  95, '4,4':  96,
                    '5,4':  97,
                '0,5':  86, '1,5':  87, '2,5':  88, '3,5':  89, '4,5':  90,
                    '5,5':  91
            },
            4: {
                'xpos': 67,
                'ypos': 0,
                'width': 1,
                'height': 6,
                '0,0': 127,
                '0,1': 126,
                '0,2': 125,
                '0,3': 124,
                '0,4': 123,
                '0,5': 122
            },
        }

        # Size of entire wall, in pixels
        # wallsizex is the width of all panels added
        # wallsizey is the maximum height of a panel
        #
        # FIXME: It is assumed that panels are placed side-to-side and not
        # above/below each other
        self.wallsizex = 0
        self.wallsizey = 0
        for p in self.model:
            self.wallsizex += self.model[p]['width'] * self.boardsizex

            if self.model[p]['height'] * self.boardsizey > self.wallsizey:
                self.wallsizey = self.model[p]['height'] * self.boardsizey
