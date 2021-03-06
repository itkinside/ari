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
#

"""
Ari server -- Controlling system for animations on a LED wall

Usage: ari-server [-h|-l] [-w|-s [-d demo]]

  -h, --help        Show this help text
  -l, --list        List loaded demos
  -w, --wall        Output to physical wall
  -s, --simulator   Output to wall simulator
  -d, --demo DEMO   Run DEMO, else run playlist
"""

import getopt
import logging
import os
import sys

import ari
import ari.canvas.wall
import ari.canvas.simulator

import ari.fx.arrows
import ari.fx.blank
import ari.fx.blob
import ari.fx.chess
import ari.fx.fade
import ari.fx.fft
import ari.fx.fire
import ari.fx.plasma
import ari.fx.spiral
import ari.fx.sprite
import ari.fx.stars
import ari.fx.tetris

# To make media lookup always work
os.chdir(os.path.dirname(ari.__file__))

logging.basicConfig(
    format='%(levelname)-5s:%(threadName)s:%(name)s:%(message)s',
    level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('ari-server')

class AriServer:
    def __init__(self):
        # Time given to each demo in the playlist
        self.timeout = 10

    def main(self, args):
        # Get command line arguments
        opts = self.getopt(args)
        logger.debug('Command line options parsed: %s', opts)

        # Init canvas
        canvas = None
        if opts['wall']:
            logger.info('Output canvas: wall')
            canvas = ari.canvas.wall.Wall()
        elif opts['simulator']:
            logger.info('Output canvas: simulator')
            canvas = ari.canvas.simulator.Simulator()

        # Load demos
        demos = self.loaddemos(canvas)
        playlist = ['stars', 'arrows', 'chess', 'blob', 'plasma']
        logger.debug('Demos loaded')

        # List demos
        if opts['list']:
            self.listdemos(demos.keys(), playlist)

        # Run requested demo
        if canvas is not None and opts['demo']:
            playlist = self.requestdemo(demos.keys(), opts['demo'])

        # Run the demo playlist
        if canvas is not None:
            logger.debug('Running playlist: %s', playlist)
            self.runplaylist(demos, playlist)

        # Exit nicely
        logger.debug('Main exiting')
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
        demos['blank'] = ari.fx.blank.Blank(canvas)
        demos['blank'].setup()

        demos['fade'] = ari.fx.fade.Fade(canvas)
        demos['fade'].setup()

        demos['fft'] = ari.fx.fft.FFT(canvas)
        demos['fft'].setup()

        demos['spiral'] = ari.fx.spiral.Spiral(canvas)
        demos['spiral'].setup()

        demos['fire'] = ari.fx.fire.Fire(canvas)
        demos['fire'].setup()

        demos['tetris'] = ari.fx.tetris.Tetris(canvas)
        demos['tetris'].setup()

        # Sprite demos
        demos['allyourbase'] = ari.fx.sprite.Sprite(canvas)
        demos['allyourbase'].setup(filepath='media/blm/allyourbase.blm')

        demos['ball'] = ari.fx.sprite.Sprite(canvas)
        demos['ball'].setup(filepath='media/bitmap/ball.xpm',
                            dx=1, dy=1, fps=20)

        demos['behappy'] = ari.fx.sprite.Sprite(canvas)
        demos['behappy'].setup(filepath='media/blm/behappy.blm')

        demos['camel'] = ari.fx.sprite.Sprite(canvas)
        demos['camel'].setup(filepath='media/blm/camel.blm',
                             scale=(30, 30))

        demos['cometogether'] = ari.fx.sprite.Sprite(canvas)
        demos['cometogether'].setup(filepath='media/blm/cometogether.blm')

        demos['isfit'] = ari.fx.sprite.Sprite(canvas)
        demos['isfit'].setup(filepath='media/blm/isfitcamel.blm')

        demos['mg'] = ari.fx.sprite.Sprite(canvas)
        demos['mg'].setup(filepath='media/bitmap/mg2.png', invert=True)

        demos['samfundet'] = ari.fx.sprite.Sprite(canvas)
        demos['samfundet'].setup(filepath='media/bitmap/samfundet-logo.xpm',
                                 dx=1, dy=1, fps=10, invert=True)

        # Playlist/real demos
        demos['arrows'] = ari.fx.arrows.Arrows(canvas)
        demos['arrows'].setup()

        demos['blob'] = ari.fx.blob.Blob(canvas)
        demos['blob'].setup()

        demos['chess'] = ari.fx.chess.Chess(canvas)
        demos['chess'].setup()

        demos['plasma'] = ari.fx.plasma.Plasma(canvas)
        demos['plasma'].setup()

        demos['stars'] = ari.fx.stars.Stars(canvas)
        demos['stars'].setup()

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
                    logger.debug('Starting "%s"', demo)
                    demos[demo].start()

                    # Wait for demo. If it exits we will immediately continue
                    if len(playlist) == 1:
                        demos[demo].join()
                        return True
                    else:
                        logger.debug('Waiting for %ds', self.timeout)
                        demos[demo].join(self.timeout)
                        if demos[demo].isAlive():
                            logger.debug('Timeout reached')
                        else:
                            logger.debug('Thread exited')

                    if demos[demo].isAlive():
                        logger.debug('Stopping "%s"', demo)
                        demos[demo].stop()
                    else:
                        logger.debug('Thread done or ESC pushed; stopping playlist loop')
                        runnable = False
                        break
        except KeyboardInterrupt:
            logger.info('Interrupt recieved (Ctrl-C or DEL)')
            pass

        for demo in demos:
            if demos[demo].runnable and demos[demo].isAlive():
                logger.debug('Stopping "%s"', demo)
                demos[demo].stop()
                demos[demo].join(2)

if __name__ == '__main__':
    ari_server = AriServer()
    ari_server.main(sys.argv[1:])
