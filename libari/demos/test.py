#! /usr/bin/env python
#
# TODO
# insert various self-loving statements about how great i am
# insert various negative statements about how idiotic 4-space-indentation is

import libari.demos.base

class Test(libari.demos.base.Base):
	"""A test to see how slow python is"""

	def run(self):
		# The demo
		while True:
			if self.drawable:
				for x in range(0, 105, 1):
					for y in range(0, 30, 1):
						self.canvas.setpixel(x, y, 99 - self.canvas.getpixel(x, y))
				self.canvas.update()
			#self.sleep()
