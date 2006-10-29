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

class Arid:
    def __init__(self):
        self.timeout = 10

    def main(self, args):
        # Get command line arguments
        opts = self.getopt(args)

        # Init canvas
        if opts['simulate']:
            canvas = libari.martha.Martha()
        else:
            canvas = libari.wall.Wall()

        # Load demos
        demos = self.loaddemos(canvas)
        carousel = ['stars', 'chess', 'blob']

        # List demos
        if opts['list']:
            self.listdemos(demos.keys(), carousel)

        # Requested demo
        if opts['demo']:
            carousel = self.requestdemo(demos.keys(), opts['demo'])

        # Run the demo carousel
        self.runcarousel(demos, carousel)

        # Exit nicely
        sys.exit(0)

    def getopt(self, args):
        """Get command line arguments"""

        try:
            opts, args = getopt.getopt(args, 'hsld:',
                ['help', 'simulate', 'list', 'demo='])
        except getopt.GetoptError, error:
            print >> sys.stderr, 'Option does not exist.'
            sys.exit(1)

        result = {}
        result['simulate'] = False
        result['list'] = False
        result['demo'] = False

        for opt, val in opts:
            # Show help
            if opt in ('-h', '--help'):
                print >> sys.stderr, __doc__
                sys.exit(0)

            # Simulate diode wall
            if opt in ('-s', '--simulate'):
                result['simulate'] = True

            # List demos
            if opt in ('-l', '--list'):
                result['list'] = True

            # Run requested demo
            if opt in ('-d', '--demo'):
                result['demo'] = val

        return result

    def loaddemos(self, canvas):
        """Load demos"""

        demos = {}

        # Test demos
        demos['blank'] = libari.demos.blank.Blank(canvas)
        demos['fade'] = libari.demos.fade.Fade(canvas)
        demos['fade'].setup(10, 60)
	demos['fft'] = libari.demos.fft.FFT(canvas)
	demos['test'] = libari.demos.test.Test(canvas)

        # Carousel/real demos
        demos['chess'] = libari.demos.chess.Chess(canvas)
        demos['chess'].setup()
        demos['blob'] = libari.demos.blob.Blob(canvas)
        demos['stars'] = libari.demos.stars.Stars(canvas)
        demos['stars'].setup(20, 99)

        return demos

    def listdemos(self, demos, carousel):
        """List demos"""

        if len(demos):
            print 'Loaded demos:'
            demos.sort()
            for demo in demos:
                if carousel.count(demo):
                    print "  " + demo + " [carousel]"
                else:
                    print "  " + demo
            sys.exit(0)
        else:
            print >> sys.stderr, 'No demos loaded.'
            sys.exit(1)

    def requestdemo(self, demos, requested):
        """Put requested demo on the carousel"""
        if requested in demos:
            return [requested]
        else:
            print >> sys.stderr, "No '%s' demo loaded." % requested
            sys.exit(1)

    def runcarousel(self, demos, carousel):
        """Run a carousel of demos"""

        runnable = True

        try:
            while runnable:
                for demo in carousel:
                    # Start demo
                    demos[demo].start()
                    
                    # Wait for demo. If it exits we will immediately continue
                    if len(carousel) == 1:
                        demos[demo].join()
                        return True
                    else:
                        demos[demo].join(self.timeout)

                    # Timeout reached, ask it to stop
                    if demos[demo].isAlive():
                        demos[demo].stop()
                    else:
                        # Thread has already exited
                        # (e.g. it's done or ESC was pushed)
                        runnable = False
                        break
        except KeyboardInterrupt, e:
            # Interrupt recieved (Ctrl-C or DEL)
            pass

        # Ask all alive demos to exit
        for demo in demos:
            if demos[demo].isAlive():
                demos[demo].exit()
                demos[demo].join(2)

if __name__ == '__main__':
    arid = Arid()
    arid.main(sys.argv[1:])
