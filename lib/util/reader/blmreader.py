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

from lib.util.dict import *
from lib.util.reader import Reader, ReaderException
import numarray
import re

class BLMReader(Reader):
    """Reader for the BlinkenLights Movie (BLM) format"""

    def parse(self, *args, **kwargs):
        """Loads and parses a BLM file. See parent for more doc."""

        kwargs = explode_kwargs(kwargs)

        try:
            duration = kwargs['duration']
        except:
            duration = 0

        frames = []
        (framew, frameh) = (0, 0)
        frame = None

        filehandle = open(kwargs['filepath'])
        try:
            for line in filehandle:
                # Strip whitespace
                line = line.strip()

                # Identification line: Get frame width and height
                if line.startswith('# BlinkenLights Movie'):
                    m = re.search(r"(\d+)x(\d+)", line)
                    if m is None or len(m.groups()) < 2:
                        raise ReaderException, 'BLM frame dimensions not found'
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
                if frame is None:
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
            filehandle.close()

        return frames
