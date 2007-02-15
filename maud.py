#! /usr/bin/env python
#
# Copyright (C) 2006-2007 Stein Magnus Jodal
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
Maud - Diode wall demo player daemon

Usage: maud [-h|-l] [-w|-s [-d demo]]

  -h, --help        Show this help text
  -l, --list        List loaded demos
  -w, --wall        Output to physical wall
  -s, --simulator   Output to Simulator wall simulator
  -d, --demo DEMO   Run DEMO, else run playlist
"""

import getopt
import sys

import lib.canvas.wall
import lib.canvas.simulator

import lib.fx.arrows
import lib.fx.blank
import lib.fx.blob
import lib.fx.chess
import lib.fx.fade
import lib.fx.fft
import lib.fx.fire
import lib.fx.plasma
import lib.fx.spiral
import lib.fx.stars
import lib.fx.tetris
import lib.fx.spritebitmap
import lib.fx.spriteblm

class Maud:
    def __init__(self):
        # Time given to each demo in the playlist
        self.timeout = 10

    def main(self, args):
        # Get command line arguments
        opts = self.getopt(args)

        # Init canvas
        canvas = None
        if opts['wall']:
            canvas = lib.canvas.wall.Wall()
        elif opts['simulator']:
            canvas = lib.canvas.simulator.Simulator()

        # Load demos
        demos = self.loaddemos(canvas)
        playlist = ['isfit']

        # List demos
        if opts['list']:
            self.listdemos(demos.keys(), playlist)

        # Run requested demo
        if canvas is not None and opts['demo']:
            playlist = self.requestdemo(demos.keys(), opts['demo'])

        # Run the demo playlist
        if canvas is not None:
            self.runplaylist(demos, playlist)

        # Exit nicely
        sys.exit(0)

    def getopt(self, args):
        """Get command line arguments"""

        try:
            opts, args = getopt.getopt(args, 'hwsld:',
                ['help', 'wall', 'simulator', 'list', 'demo='])
        except getopt.GetoptError:
            print >> sys.stderr, 'Option does not exist.'
            sys.exit(1)

        # No opts, show help
        if len(opts) == 0:
            print >> sys.stderr, __doc__
            sys.exit(0)

        result = {}
        result['wall'] = False
        result['simulator'] = False
        result['list'] = False
        result['demo'] = False

        for opt, val in opts:
            # Show help
            if opt in ('-h', '--help'):
                print >> sys.stderr, __doc__
                sys.exit(0)

            # Output to physical wall
            if opt in ('-w', '--wall'):
                result['wall'] = True

            # Output to simulator
            if opt in ('-s', '--simulator'):
                result['simulator'] = True

            # List demos
            if opt in ('-l', '--list'):
                result['list'] = True

            # Run requested demo
            if opt in ('-d', '--demo'):
                result['demo'] = val

        if result['demo'] and not (result['wall'] or result['simulator']):
            print >> sys.stderr, __doc__
            sys.exit(0)

        return result

    def loaddemos(self, canvas):
        """Load demos"""

        demos = {}

        # Test demos
        demos['blank'] = lib.fx.blank.Blank(canvas)
        demos['fade'] = lib.fx.fade.Fade(canvas)
        demos['fft'] = lib.fx.fft.FFT(canvas)
        demos['spiral'] = lib.fx.spiral.Spiral(canvas)
        demos['arrows'] = lib.fx.arrows.Arrows(canvas)
        demos['fire'] = lib.fx.fire.Fire(canvas)
        demos['tetris'] = lib.fx.tetris.Tetris(canvas)

        # Sprite demos
        demos['allyourbase'] = lib.fx.spriteblm.SpriteBLM(canvas)
        demos['allyourbase'].setup(blmfile='allyourbase.blm')
        demos['ball'] = lib.fx.spritebitmap.SpriteBitmap(canvas)
        demos['ball'].setup(imagefile='ball.xpm', fps=20)
        demos['behappy'] = lib.fx.spriteblm.SpriteBLM(canvas)
        demos['behappy'].setup(blmfile='behappy.blm')
        demos['camel'] = lib.fx.spriteblm.SpriteBLM(canvas)
        demos['cometogether'] = lib.fx.spriteblm.SpriteBLM(canvas)
        demos['cometogether'].setup(blmfile='cometogether.blm')
        demos['isfit'] = lib.fx.spriteblm.SpriteBLM(canvas)
        demos['isfit'].setup(blmfile='isfitcamel.blm')
        demos['samfundet'] = lib.fx.spritebitmap.SpriteBitmap(canvas)

        # Playlist/real demos
        demos['arrows'] = lib.fx.arrows.Arrows(canvas)
        demos['blob'] = lib.fx.blob.Blob(canvas)
        demos['chess'] = lib.fx.chess.Chess(canvas)
        demos['plasma'] = lib.fx.plasma.Plasma(canvas)
        demos['stars'] = lib.fx.stars.Stars(canvas)

        return demos

    def listdemos(self, demos, playlist):
        """List demos"""

        if len(demos):
            print 'Loaded demos:'
            demos.sort()
            for demo in demos:
                if playlist.count(demo):
                    print "  " + demo + " [playlist]"
                else:
                    print "  " + demo
            sys.exit(0)
        else:
            print >> sys.stderr, 'No demos loaded.'
            sys.exit(1)

    def requestdemo(self, demos, requested):
        """Put requested demo on the playlist"""
        if requested in demos:
            return [requested]
        else:
            print >> sys.stderr, "No '%s' demo loaded." % requested
            sys.exit(1)

    def runplaylist(self, demos, playlist):
        """Run a playlist of demos"""

        runnable = True

        try:
            while runnable:
                for demo in playlist:
                    # Start demo
                    demos[demo].start()

                    # Wait for demo. If it exits we will immediately continue
                    if len(playlist) == 1:
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
        except KeyboardInterrupt:
            # Interrupt recieved (Ctrl-C or DEL)
            pass

        # Ask all alive demos to exit
        for demo in demos:
            if demos[demo].isAlive():
                demos[demo].exit()
                demos[demo].join(2)

if __name__ == '__main__':
    maud = Maud()
    maud.main(sys.argv[1:])
