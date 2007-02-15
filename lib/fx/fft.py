#! /usr/bin/env python
#
# Copyright (C) 2006 Vidar Wahlberg
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
# Authors: Vidar Wahlberg <canidae@samfundet.no>
#

import lib.fx.base
import array
import numarray
import numarray.fft

class FFT(lib.fx.base.Base):
    """A histogrammy demo reflecting the music"""

    def run(self):
        # The demo
        ar = AudioReader()
        while self.runnable:
            if self.drawable:
                ar.read()
                minv = 20
                maxv = 40
                step = 30.0 / (maxv - minv)
                for x in xrange(105):
                    for y in xrange(29, int(29 - (ar.data[x] - minv) * step) or 0, -1):
                        self.image[x][y] = 99
                self.canvas.update(self.image)
                self.canvas.flush()
                for x in xrange(105):
                    for y in xrange(30):
                        self.image[x][y] = self.image[x][y] - 33

class AudioReader:
    def __init__(self):
        self.dsp = open('/dev/dsp', 'r', 0)

    def read(self):
        self.data = array.array('B', self.dsp.read(256))
        self.data = array.array('h', self.data)
        for x in range(0, 256, 1):
            self.data[x] -= 128
        self.data = 10 * numarray.log10(1e-20 + abs(numarray.fft.fft(self.data)))

    def quit(self):
        self.dsp.close()
