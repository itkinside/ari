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
# Authors: Stein Magnus Jodal <jodal@samfundet.no>
#

"""
arid - Daemon for running demos on a diode wall

Usage: arid [-h] [-s] [-l] [-d demo]

  -h, --help        Show this help text
  -s, --simulate    Start simulator and use as output
  -l, --list        List loaded demos
  -d, --demo        Run given demo
"""

import getopt
import sys
import threading
import time

import libari.wall
import libari.martha

import libari.demos.blank
import libari.demos.blob
import libari.demos.chess
import libari.demos.fade
import libari.demos.stars
import libari.demos.fft
import libari.demos.test

class Arid(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.timeout = 10

    def main(self, args):
        # Get command line arguments
        try:
            opts, args = getopt.getopt(args, 'hsld:',
                ['help', 'simulate', 'list', 'demo='])
        except getopt.GetoptError, error:
            print >> sys.stderr, 'Option does not exist.'
            sys.exit(1)
        optsim = False
        optlist = False
        optdemo = False
        for opt, val in opts:
            # Show help
            if opt in ('-h', '--help'):
                print >> sys.stderr, __doc__
                sys.exit(0)
            # Simulate diode wall
            if opt in ('-s', '--simulate'):
                optsim = True
            # List demos
            if opt in ('-l', '--list'):
                optlist = True
            # Run requested demo
            if opt in ('-d', '--demo'):
                optdemo = val

        # Init output device and canvas
        if optsim:
            # Output to the Martha simulator
            self.canvas = libari.martha.Martha()
        else:
            # Output to the physical wall
            self.canvas = libari.wall.Wall()

        # Load demos
        self.demos = {}

        # Test demos
        self.demos['blank'] = libari.demos.blank.Blank(self.canvas)
        self.demos['blob'] = libari.demos.blob.Blob(self.canvas)
        self.demos['fade'] = libari.demos.fade.Fade(self.canvas)
        self.demos['fade'].setup(10, 60)
	self.demos['fft'] = libari.demos.fft.FFT(self.canvas)
	self.demos['test'] = libari.demos.test.Test(self.canvas)

        # Carousel/real demos
        self.demos['chess'] = libari.demos.chess.Chess(self.canvas)
        self.demos['chess'].setup()
        self.demos['stars'] = libari.demos.stars.Stars(self.canvas)
        self.demos['stars'].setup(20, 99)

        # Load demos onto the carousel
        self.democarousel = ['stars', 'chess', 'blob']
        self.currentdemo = None

        # List demos
        if optlist:
            if len(self.demos):
                print 'Loaded demos:'
                demos = self.demos.keys()
                demos.sort()
                for demo in demos:
                    if self.democarousel.count(demo):
                        print "  " + demo + " [carousel]"
                    else:
                        print "  " + demo
                sys.exit(0)
            else:
                print 'No demos loaded.'
                sys.exit(1)

        # Requested demo: put it on the carousel
        if optdemo:
            if self.demos.has_key(optdemo):
                self.democarousel = [optdemo]
            else:
                print >> sys.stderr, "No '%s' demo loaded." % optdemo

        # Default: Run a carousel of demos
        try:
            while True:
                for demo in self.democarousel:
                    # Start demo
                    self.currentdemo = demo
                    self.demos[demo].start()
                    
                    # Wait for demo. If it exits we will immediately continue
                    if len(self.democarousel) == 1:
                        self.demos[demo].join()
                    else:
                        self.demos[demo].join(self.timeout)

                    # Timeout reached, ask it to stop
                    if self.demos[demo].isAlive():
                        self.demos[demo].stop()
                    else:
                        pass # Thread has already exited
                    self.currentdemo = None
        except KeyboardInterrupt, e:
            # Interrupt recieved, ask all alive demos to exit
            for demo in self.demos:
                if self.demos[demo].isAlive():
                    self.demos[demo].exit()
                    self.demos[demo].join(2)
        sys.exit(0)

if __name__ == '__main__':
    arid = Arid()
    arid.main(sys.argv[1:])
