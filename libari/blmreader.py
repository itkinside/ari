#! /usr/bin/env python
#
# BlinkenLights Movies (BLM) file format reader for libari
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

import numarray
import os
import pickle
import re

class BLMReader:
    """Reader for the BlinkenLights Movie (BLM) format"""

    def __init__(self):
        pass

    def load(self, filename):
        """
        Loads a BLM file, if possible from cache

        Uses pickle to cache and reuse previously loaded BLM files.

        Input:
            filename    File name of the BLM file

        Returns:
            List of tuples with the following data:
            - Frame duration
            - Frame data as a numarray
       
        """

        cachefilename = 'cache/%s.maud' % filename.replace('/', '_')

        if not os.path.isfile(cachefilename):
            frames = self.parse(filename)
            pickle.dump(frames, open(cachefilename, 'w'))
            return frames
        else:
            return pickle.load(open(cachefilename, 'r'))

    def parse(self, filename):
        """
        Loads and parses a BLM file
        
        Input:
            filename    File name of the BLM file

        Returns:
            List of tuples with the following data:
            - Frame duration
            - Frame data as a numarray
        
        """

        frames = []
        duration = 0
        (framew, frameh) = (0, 0)
        frame = numarray.zeros((framew, frameh))

        file = open(filename)
        try:
            for line in file:
                # Strip whitespace
                line = line.strip()

                # Identification line: Get frame width and height
                if line.startswith('# BlinkenLights Movie'):
                    m = re.search(r"(\d+)x(\d+)", line)
                    if m is None or len(m.groups()) < 2:
                        raise 'Error: Dimensions not found'
                    framew = int(m.group(1))
                    frameh = int(m.group(2))
                    continue

                # Comment line: Ignore
                if line.startswith('#'):
                    continue

                # Frame duration line: Start of frame
                if line.startswith('@'):
                    duration = int(line.replace('@', ''))
                    frame = numarray.zeros((framew, frameh))
                    y = 0
                    continue

                # Blank line before first frame: Skip to next line
                if not duration > 0:
                    continue

                # Blank line: End of frame
                if len(line) == 0:
                    frames.append((duration, frame))
                    continue

                # Else: Data line
                for x, value in enumerate(line):
                    frame[x][y] = int(value) * 99
                y += 1
        finally:
            file.close()

        return frames
