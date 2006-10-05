#! /usr/bin/env python
#
# arid - Daemon for running demos on a diode wall
# Copyright (C) 2006 Stein Magnus Jodal
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

import sys
import threading
import time
import libari.config

class Base(threading.Thread):
    """
    Base class for demos
    
    Demos must inherit from this class.
    """

    runnable = True
    drawable = False
    fps = 25

    def __init__(self, canvas):
        """
        Input:
            canvas  Canvas to paint on.
        """

        threading.Thread.__init__(self)
        self.config = libari.config.Config()
        self.canvas = canvas
        self.setup()

    def setfps(self, fps):
        if type(fps) is int or type(fps) is float:
            self.fps = fps

    def sleep(self):
        time.sleep(1.0 / self.fps)

    def start(self):
        self.prepare()
        self.drawable = True
        if not self.isAlive():
            threading.Thread.start(self)

    def stop(self):
        self.drawable = False

    def exit(self):
        self.runnable = False

    def setup(self):
        """
        setup() is ment as an addition to the inherited __init__()
        You MAY override this method in your demo
        """
        pass

    def prepare(self):
        """
        prepare() is where you clear the wall and prepare for a new run
        You MAY override this method in your demo
        """
        pass

    def run(self):
        """
        run() is where the actual calculation and drawing is done
        You MUST override this method in your demo
        """
        b = 0
        while self.runnable:
            if self.drawable:
            # Do your magic here
                if b == 0:
                    b = 99
                else:
                    b = 0
                self.canvas.update()
            self.sleep()
