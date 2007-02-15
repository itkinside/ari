#! /usr/bin/env python
#
# Simulator - Diode wall simulator
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
#          Vidar Wahlberg <canidae@samfundet.no>
#

import lib.canvas.canvas
import numarray
import pygame
from pygame.locals import *
import sys
import time

class Simulator(lib.canvas.canvas.Canvas):
    """Canvas for the Simulator simulator"""

    def __init__(self, dw = False, dh = False, ps = False, pd = False):
        # Init mother
        lib.canvas.canvas.Canvas.__init__(self)

        # Prepare FPS calculation
        self.time = 0

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
        self.paneldistance = self.ps * 20

        # Create window
        self.windowcreated = False
 
    def __createwindow(self):
        """Create Simulator window"""
 
        # Create window
        pygame.display.init()
        pygame.display.set_caption('Simulator')
        self.screen = pygame.display.set_mode(self.__convert((self.dw,
                                                              self.dh)))
    
        # Add panel spacing
        px = 0
        for p in xrange(len(self.config.model) - 1):
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
            self.screen.fill((70, 70, 70), pygame.Rect(x, y, dx, dy))

        self.windowcreated = True

    def __convert(self, i):
        """Convert from virtual pixels to Simulator pixels"""

        if type(i) is tuple:
            (x, y) = i
            # Find panel
            p = 0
            dx = 0
            for p in xrange(len(self.config.model)):
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

    def __processevents(self):
        """Process events and take appropriate action"""

        for event in pygame.event.get():
            if event.type is QUIT:
                return False
            elif event.type is KEYDOWN and event.key is K_ESCAPE:
                return False
        return True

    def setpixel(self, x, y, b, o = 100):
        """For doc, see Canvas"""

        # Call mother
        b = lib.canvas.canvas.Canvas.setpixel(self, x, y, b, o)

        # Create window
        if not self.windowcreated:
            self.__createwindow()

        # Brightness
        b = b * 255 / 99

        # Position
        (x, y) = self.__convert((x, y))
        x = x + self.pd / 2
        y = y + self.pd / 2
    
        # Paint on screen
        self.screen.fill((b, b, b), pygame.Rect(x, y, self.ps, self.ps))

    def update(self, canvas = None, cx = 0, cy = 0):
        """For doc, see Canvas"""

        # Call mother
        lib.canvas.canvas.Canvas.update(self, canvas, cx, cy)

        # Create window
        if not self.windowcreated:
            self.__createwindow()

        # Draw wall (but only if canvas was supplied)
        for x in xrange(cx, cx + self.cw):
            for y in xrange(cy, cy + self.ch):
                # Calculate brightness
                b = self.wall[x][y] * 255 / 99
                if b > 255:
                    b = 255
                elif b < 0:
                    b = 0

                # Add pixelspacing
                # FIXME: This is a hack, but we don't want the overhead of
                # using __convert() 3150 times per frame
                px = x
                if x >= 100:
                    px += self.paneldistance / (self.ps + self.pd) * 4
                elif x >= 70:
                    px += self.paneldistance / (self.ps + self.pd) * 3
                elif x >= 55:
                    px += self.paneldistance / (self.ps + self.pd) * 2
                elif x >= 10:
                    px += self.paneldistance / (self.ps + self.pd)
                py = y

                # Paint to screen
                # FIXME: This is ugly
                self.screen.fill((b, b, b),
                    pygame.Rect(px * (self.ps + self.pd) + self.pd / 2, \
                                py * (self.ps + self.pd) + self.pd / 2,
                                self.ps,
                                self.ps))

        # Check events
        if not self.__processevents():
            sys.exit(0)

    def flush(self):
        """For doc, see Canvas"""

        # Flush screen to display
        pygame.display.update()

        # Calculate FPS
        print "\rFPS: %8.3f" % (1 / (time.time() - self.time)),
        self.time = time.time()

        # Check events
        if not self.__processevents():
            sys.exit(0)

