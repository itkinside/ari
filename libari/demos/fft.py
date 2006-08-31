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
				minv = 0
				maxv = 65536
				#minv = min(ar.data[0:105])
				#maxv = max(ar.data[0:105])
				step = 30.0 / (maxv - minv)
				#print minv
				#print maxv
				#print step
				#print "--"
				for x in range(0, 105, 1):
					for y in range(30, int(30 - (ar.data[x] - minv) * step), -1):
						self.canvas.setpixel(x, y, 99)
					#self.canvas.setpixel(x, 30 - (ar.data[x] - minv) * step, 99)
				self.canvas.update()
				for x in range(0, 105, 1):
					for y in range(30, int(30 - (ar.data[x] - minv) * step), -1):
						self.canvas.setpixel(x, y, 0)
					#self.canvas.setpixel(x, 30 - (ar.data[x] - minv) * step, 0)
				#self.canvas.setpixel(x, y, 99)
				#self.canvas.update()
				#self.canvas.setpixel(x, y, 0)
				#ar.quit()
				#self.stop()
			#self.sleep()

class AudioReader:
	def __init__(self):
		# python loves self!
		self.dsp = ossaudiodev.open('/dev/dsp', 'r')
		self.dsp.setparameters(ossaudiodev.AFMT_S16_LE, 2, 44100)
		self.lol = 5000.0

	def read(self):
		self.data = array.array('h', self.dsp.read(2048))
		#x = numarray.arange(256.0)
		#self.data = numarray.sin(2 * math.pi * (1250.0 / self.lol) * x) + numarray.sin(2 * math.pi * (625.0 / self.lol) * x)
		#self.lol += 1
		#self.data = 10 * numarray.log10(1e-20 + abs(numarray.fft.fft(self.data)))
		self.data = 1e-20 + abs(numarray.fft.fft(self.data))
		#return (self.data[0], self.data[1])
		#print self.data
		#print self.data[0]
		#print self.data[1]

	def quit(self):
		self.dsp.close()
