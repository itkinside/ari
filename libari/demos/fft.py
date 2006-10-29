#! /usr/bin/env python
#
# libari - Library for manipulating a diode wall
# Copyright (C) 2006 Vidar Wahlberg
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
# Authors: Vidar Wahlberg <canidae@samfundet.no>
#

import random
import libari.demos.base
import ossaudiodev
import array
import math
import numarray
import numarray.fft

class FFT(libari.demos.base.Base):
	"""A histogrammy demo reflecting the music"""

	def run(self):
		# The demo
		ar = AudioReader()
		while self.runnable:
			if self.drawable:
				ar.read()
				#minv = 0
				#maxv = 65536
				#minv = min(ar.data[0:105])
				#maxv = max(ar.data[0:105])
				minv = 20
				maxv = 40
				step = 30.0 / (maxv - minv)
				#print minv
				#print maxv
				#print step
				#print "--"
				for x in xrange(105):
					for y in xrange(29, int(29 - (ar.data[x] - minv) * step) or 0, -1):
						self.image[x][y] = 99
						#self.canvas.setpixel(x, y, 99)
				self.canvas.update(self.image)
				#for x in range(0, 105, 1):
				#	for y in range(30, int(30 - (ar.data[x] - minv) * step), -1):
				#		self.canvas.setpixel(x, y, 0)
				for x in xrange(105):
					for y in xrange(30):
						self.image[x][y] = self.image[x][y] - 33
						#self.canvas.setpixel(x, y, self.canvas.getpixel(x, y) - 33)
				#ar.quit()
				#self.stop()
			#self.sleep()

class AudioReader:
	def __init__(self):
		# python loves self!
		#self.dsp = ossaudiodev.open('/dev/dsp', 'r')
		#self.dsp.setparameters(ossaudiodev.AFMT_S16_LE, 2, 44100)
		self.dsp = open('/dev/dsp', 'r', 0)

	def read(self):
		self.data = array.array('B', self.dsp.read(256))
		self.data = array.array('h', self.data)
		for x in range(0, 256, 1):
			self.data[x] -= 128
		#print self.data
		#self.data = array.array('h', self.dsp.read(8192))
		self.data = 10 * numarray.log10(1e-20 + abs(numarray.fft.fft(self.data)))
		#print self.data
		#print "ok"

	def quit(self):
		self.dsp.close()
