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

import libari.demos.base

class Test(libari.demos.base.Base):
	"""A test to see how slow Python is"""

	def run(self):
		# The demo
		while self.runnable:
			if self.drawable:
				for x in xrange(0, 105, 1):
					for y in xrange(0, 30, 1):
						self.canvas.setpixel(x, y, 99 - self.canvas.getpixel(x, y))
				self.canvas.update()
			#self.sleep()
