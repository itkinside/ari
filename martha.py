#! /usr/bin/env python
#
# Martha - Diode wall simulator
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

import sys
import time

import libari.config
import libari.martha

class Martha:
    def __init__(self):
        # Set variables
        pixelsize = 1
        pixelspacing = 9

        # Get config
        self.config = libari.config.Config()

        # Get simulator canvas
        self.canvas = libari.martha.Martha(self.config.wallsizex,
                                           self.config.wallsizey,
                                           pixelsize,
                                           pixelspacing)
    
    def main(self, args):
        time.sleep(10)
        # FIXME: Implement demo loading et al here

if __name__ == '__main__':
    martha = Martha()
    martha.main(sys.argv[1:])
