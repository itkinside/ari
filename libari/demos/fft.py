#! /usr/bin/env python
#
# TODO
# insert various self-loving statements about how great i am
# insert various negative statements about how idiotic 4-space-indentation is

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
		while True:
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
				for x in range(0, 105, 1):
					for y in range(30, int(30 - (ar.data[x] - minv) * step), -1):
						self.canvas.setpixel(x, y, 99)
				self.canvas.update()
				#for x in range(0, 105, 1):
				#	for y in range(30, int(30 - (ar.data[x] - minv) * step), -1):
				#		self.canvas.setpixel(x, y, 0)
				for x in range(0, 105, 1):
					for y in range(0, 30, 1):
						self.canvas.setpixel(x, y, self.canvas.getpixel(x, y) - 33)
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
