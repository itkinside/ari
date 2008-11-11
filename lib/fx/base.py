#! /usr/bin/env python
#
# Copyright (C) 2006-2007 Stein Magnus Jodal
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2
# as published by the Free Software Foundation.
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
# Authors: Stein Magnus Jodal <jodal@samfundet.no>
#          Vidar Wahlberg <canidae@samfundet.no>
#

import lib.config
import logging
import sys
import threading
import time

logger = logging.getLogger('lib.fx.base')

class Base(threading.Thread):
    """
    Base class for demos

    Demos must inherit from this class.
    """

    runnable = False
    drawable = False
    fps = 25
    lasttime = 0

    def __init__(self, canvas, sizex=None, sizey=None):
        """
        Input:
            canvas  Canvas to paint on.
        """

        self.config = lib.config.Config()
        self.canvas = canvas
        if sizex is None:
            self.sizex = self.config.wallsizex
        else:
            self.sizex = sizex
        if sizey is None:
            self.sizey = self.config.wallsizey
        else:
            self.sizey = sizey

    def setfps(self, fps):
        if type(fps) is int or type(fps) is float:
            self.fps = fps

    def sleep(self):
        sleeptime = (1.0 / self.fps) - (time.time() - self.lasttime)
        if sleeptime > 0:
            time.sleep(sleeptime)
        self.lasttime = time.time()

    def start(self):
        logger.debug('Starting demo/thread')
        self.prepare()
        threading.Thread.__init__(self)
        self.drawable = True
        self.runnable = True
        threading.Thread.start(self)

    def stop(self):
        logger.debug('Stopping demo/thread')
        self.drawable = False
        self.runnable = False

    def setup(self, *args, **kwargs):
        """
        setup() is ment as an addition to the inherited __init__()
        You MAY override this method in your demo
        """
        pass

    def prepare(self, *args, **kwargs):
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
                self.canvas.update()
                self.canvas.flush()
            self.sleep()
