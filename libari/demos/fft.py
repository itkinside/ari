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
				(left, right) = ar.read()
				left = left * 1575 / 32768 + 1575
				x = left % 105
				y = left / 105
				self.canvas.setpixel(x, y, 99)
				#self.canvas.setpixel(16, 15 - right, 99)
				self.canvas.update()
				self.canvas.setpixel(x, y, 0)
				#self.canvas.setpixel(16, 15 - right, 0)
				#ar.quit()
				#self.stop()
			self.sleep()

class AudioReader:
	def __init__(self):
		# python loves self!
		self.dsp = ossaudiodev.open('/dev/dsp', 'r')
		self.dsp.setparameters(ossaudiodev.AFMT_S16_LE, 1, 44100)

	def read(self):
		self.data = array.array('h', self.dsp.read(256))
		self.data = 10 * numarray.log10(abs(numarray.fft.fft(self.data)))
		print self.data
		#return (self.data[0], self.data[1])
		#print self.data
		#print self.data[0]
		#print self.data[1]

	def quit(self):
		self.dsp.close()
