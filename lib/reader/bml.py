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

import elementtree.ElementTree as ET
import math
import numarray
import os
import pickle

class BMLReader:
    """Reader for the BlinkenLights Markup Language (BML) format"""

    def __init__(self):
        # List of supported BML format versions
        self.supports = ['1.0']

    def load(self, filename):
        """
        Loads a BML file, if possible from cache

        Uses pickle to cache and reuse previously loaded BML files.

        Input:
            filename    File name of the BML file

        Returns:
            List of tuples with the following data:
            - Frame duration
            - Frame data as a numarray
       
        """

        cachefilename = 'cache/%s.pickle' % filename.replace('/', '_')

        if not os.path.isfile(cachefilename):
            frames = self.parse(filename)
            pickle.dump(frames, open(cachefilename, 'w'))
            return frames
        else:
            return pickle.load(open(cachefilename, 'r'))

    def parse(self, filename):
        """
        Loads and parses a BML file
        
        Input:
            filename    File name of the BML file

        Returns:
            List of tuples with the following data:
            - Frame duration
            - Frame data as a numarray
        
        """

        # Parse file
        tree = ET.parse(filename)
        root = tree.getroot()

        # Get and check version
        try:
            version = root.attrib['version']
        except:
            version = '1.0'
        if version not in self.supports:
            raise "BML version %s not supported!" % version

        # Get number of color channels
        try:
            channels = int(root.attrib['channels'])
        except:
            channels = 1

        # Get bits per channel
        try:
            bits = int(root.attrib['bits'])
        except:
            bits = 1

        # Chars per bit, assuming hexadecimal notation
        charsperbit = int(math.ceil(math.log(2**bits, 16)))

        # Get frame size
        framew = int(root.attrib['width'])
        frameh = int(root.attrib['height'])
        
        frames = []

        # Loop over frames
        for element in root.getchildren():
            # Ignore header and other non-frame tags
            if element.tag != 'frame':
                continue
            
            # Get duration
            duration = int(element.attrib['duration'])

            # Init frame
            frame = numarray.zeros((framew, frameh))
            
            # Loop over frame rows
            for y, row in enumerate(element.getchildren()):
                pixelchars = ''
                for i, char in enumerate(row.text.strip()):
                    if (i + 1) % charsperbit == 0:
                        # Pixel completed
                        pixelchars += char
                        pixel = int(pixelchars, 16)
                        pixelchars = ''

                        # FIXME: Support more than one channel

                        # Convert to brightness
                        b = pixel * 99 / (2**bits - 1)

                        # Find x position
                        x = i / charsperbit

                        # Set pixel brightness
                        frame[x][y] = b
                    else:
                        # Building the pixel value
                        pixelchars += char

            frames.append((duration, frame))

        return frames
