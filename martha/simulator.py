#! /usr/bin/env python
#
# Martha - Diode wall simulator
# Copyright (C) 2006 Thomas Adamcik, Stein Magnus Jodal
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
# Authors: Thomas Adamcik <adamcik@samfundet.no>
#          Stein Magnus Jodal <jodal@samfundet.no>
#

import pygame

class Simulator:
	def __init__(self, w = 105, h = 30, p = 1, d = 9):
		pygame.init()
		self.w = w
		self.h = h
		self.p = p
		self.d = d
		pygame.display.set_caption('Martha')
		self.screen = pygame.display.set_mode((self.__convert(w),
											   self.__convert(h)))

	def __convert(self, i):
		return i * (self.d + self.p)

	def setpixel(self, x, y, i):
		i = (i / 99) * 255
		self.screen.fill((i, i, i),
						 pygame.Rect(self.__convert(x),
									 self.__convert(y),
									 self.p,
									 self.p))

	def getpixel(self, x, y):
		(r, g, b) = self.screen.get_at(self.__convert(x),
									   self.__convert(y))
		return (r / 255) * 99

	def update(self):
		pygame.display.update()

	def blank(self, b = 0):
		for x in range(self.w):
			for y in range(self.h):
				self.setpixel(x, y, b)
