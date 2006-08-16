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
from pygame.locals import *
import sys

import libari.config

class Simulator:
    def __init__(self, dw = False, dh = False, ps = False, pd = False):
        # Load config
        self.config = libari.config.Config()

        # Get arguments
        # Display size
        if dw:
            self.dw = dw
        else:
            self.dw = self.config.wallsizex
        if dh:
            self.dh = dh
        else:
            self.dh = self.config.wallsizey
        # Pixel size and spacing
        if ps:
            self.ps = ps
        else:
            self.ps = self.config.simpixelsize
        if pd:
            self.pd = pd
        else:
            self.pd = self.config.simpixeldistance

        # Calculate panel spacing
        self.panelcount = len(self.config.model)
        self.paneldistance = self.config.simpixelsize * 20

        # Create screen
        pygame.init()
        pygame.display.set_caption('Martha')
        self.screen = pygame.display.set_mode(self.__convert((self.dw,
                                                              self.dh)))
    
        # Add panel spacing
        px = 0
        for p in range(len(self.config.model) - 1):
            # Panel start in x direction
            px += self.config.model[p]['width'] * self.config.boardsizex

            # Convert to simulator coordinates
            # Add distance to skip the panel spacers
            x = self.__convert(px) + (p * self.paneldistance)
            y = 0
            
            # Get size of panel spacer
            dx = self.paneldistance
            dy = self.__convert(self.dh)

            # Paint panel spacer
            self.screen.fill((119, 49, 0), pygame.Rect(x, y, dx, dy))
            
    def __convert(self, i):
        if type(i) is tuple:
            (x, y) = i
            # Find panel
            p = 0
            dx = 0
            for p in range(len(self.config.model)):
                dx += self.config.model[p]['width'] * self.config.boardsizex
                if x < dx:
                    dx -= self.config.model[p]['width'] * self.config.boardsizex
                    break

            # Add paneldistance, so we do not paint on the panel spacers
            x = x * (self.pd + self.ps) + (p * self.paneldistance)

            # No panel spacers in the y direction
            y = y * (self.pd + self.ps)

            return (x, y)
        if type(i) is int:
            return (i * (self.pd + self.ps))

    def getpixel(self, x, y):
        # Calculate position
        (x, y) = self.__convert((x, y))
        x = x + self.pd / 2
        y = y + self.pd / 2

        # Read from screen
        (r, g, b) = self.screen.get_at((x, y))
        return (99 * b) / 255

    def setpixel(self, x, y, b):
        # Calculate brightness and position
        b = (255 * b) / 99
        (x, y) = self.__convert((x, y))
        x = x + self.pd / 2
        y = y + self.pd / 2
    
        # Paint on screen
        self.screen.fill((b, b, b), pygame.Rect(x, y, self.ps, self.ps))

    def update(self):
        # Update screen
        pygame.display.update()

        # Check events
        if not self.__processEvents():
            sys.exit(0)

    def blank(self, b = 0):
        # Loop over all pixels and set brightness
        for x in range(self.dw):
            for y in range(self.dh):
                self.setpixel(x, y, b)

    def __processEvents(self):
        """Process events and take appropriate action"""

        for event in pygame.event.get():
            if event.type is QUIT:
                return False
            elif event.type is KEYDOWN and event.key is K_ESCAPE:
                return False
        return True
