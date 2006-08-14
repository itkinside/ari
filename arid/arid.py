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

"""
arid - Daemon for running demos on a diode wall

Usage: arid [-h] [-l] [-d demo]

  -h, --help        Show this help text
  -l, --list        List loaded demos
  -d, --demo        Run given demo
"""

import getopt
import sys
import threading
import time

import libari.wall
import libari.canvas
import demos.blank
import demos.chess
import demos.fade
import demos.stars

class Arid:
    def __init__(self):
        # Init output device
        # FIXME: Read from config
        self.output = libari.wall.Wall()

        # Init canvas
        self.canvas = libari.canvas.Canvas(self.output)

        # Load demos
        self.demos = {}
        self.demos['blank'] = demos.blank.Blank(self.canvas)
        self.demos['chess'] = demos.chess.Chess(self.canvas)
        self.demos['fade'] = demos.fade.Fade(self.canvas, 10, 60)
        self.demos['stars'] = demos.stars.Stars(self.canvas, 0, 60)
        self.defaultdemos = ['stars', 'fade']
        self.currentdemo = None

    def main(self, args):
        # Get command line arguments
        try:
            opts, args = getopt.getopt(args, 'hld:', ['help', 'list', 'demo='])
        except getopt.GetoptError, error:
            print >> sys.stderr, 'Option does not exist.'
            sys.exit(1)
        optdemo = False
        for opt, val in opts:
            # Show help
            if opt in ('-h', '--help'):
                print >> sys.stderr, __doc__
                sys.exit(0)
            # List demos
            if opt in ('-l', '--list'):
                if len(self.demos):
                    print 'Loaded demos:'
                    demos = self.demos.keys()
                    demos.sort()
                    for demo in demos:
                        if self.defaultdemos.count(demo):
                            print "  " + demo + " [default]"
                        else:
                            print "  " + demo
                    sys.exit(0)
                else:
                    print 'No demos loaded.'
                    sys.exit(1)
            # Run demo
            if opt in ('-d', '--demo'):
                optdemo = val

        # Run requested demo
        if optdemo:
            if self.demos.has_key(optdemo):
                self.demos[optdemo].start()
                try:
                    while True:
                        time.sleep(60)
                except KeyboardInterrupt, e:
                    self.demos[optdemo].stop()
                    sys.exit(0)
            else:
                print >> sys.stderr, "No '%s' demo loaded." % optdemo
            self.currentdemo = self.defaultdemo

        # Run a carusel of demos
        try:
            while True:
                for demo in self.defaultdemos:
                    self.currentdemo = demo
                    self.demos[demo].start()
                    self.demos[demo].join(10)
                    while self.demos[demo].isAlive():
                        self.demos[demo].stop()
                        self.demos[demo].join(10)
                    self.currentdemo = None
                break # FIXME run() vs start()
        except KeyboardInterrupt, e:
            self.demos[self.currentdemo].stop()
            self.demos[self.currentdemo].join()
            sys.exit(0)

if __name__ == '__main__':
    arid = Arid()
    arid.main(sys.argv[1:])
