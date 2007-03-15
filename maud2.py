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
Maud - the Ari daemon

Usage: maud [-h] [-d] -w|-s

  -h, --help        Show this help text
  -d, --debug       Turn on debug logging
  -w, --wall        Output to physical wall
  -s, --simulator   Output to wall simulator
"""

import getopt
import logging
import sys
import time
import lib.util.dict
import maud.daemon

debug = False
logger = logging.getLogger('maud')

class Maud:
    def __init__(self):
        pass

    def main(self, args):
        """Maud main method"""

        # Simple pre-daemon console logging
        console = logging.StreamHandler()
        logger.addHandler(console)

        # Get command line arguments
        opts = self.getopt(args)

        # FIXME: Read config from file using ConfigParser
        # FIXME: Support pidfile with relative path
        logfile = '/home/cassarossa/itk/jodal/projects/ari/maud.log'
        pidfile = '/home/cassarossa/itk/jodal/projects/ari/maud.pid'

        # Init logger
        logconf = {}
        logconf['logfile'] = logfile
        if debug:
            logconf['level'] = logging.DEBUG
        self.initlogging(kwargs=logconf)

        # Switch users
        # FIXME: If root, switch to dedicated user

        # Check if alone
        try:
            maud.daemon.justme(pidfile)
        except maud.daemon.AlreadyRunningError:
            logger.error('Daemon is already running. Exiting.')
            sys.exit(1)
        except maud.daemon.PidFileReadError:
            logger.error('PID file is unreadable. Exiting.')
            sys.exit(1)

        # Daemonize
        try:
            maud.daemon.daemonize(pidfile)
            logger.removeHandler(console)
        except maud.daemon.ForkError:
            logger.error('Fork failed. Exiting.')
            sys.exit(1)
        except maud.daemon.PidFileWriteError:
            logger.error('Write to PID file failed. Exiting.')
            sys.exit(1)

        # Program loop
        try:
            # FIXME: Do something
            while True:
                logger.info('Hi!')
                time.sleep(60)
        except Exception, e:
            # Log all non-fetched exceptions
            logger.exception(e)
            sys.exit(1)

    def getopt(self, args):
        """Get command line arguments"""

        try:
            opts, args = getopt.getopt(args, 'hdws',
                ['help', 'debug', 'wall', 'simulator'])
        except getopt.GetoptError:
            logger.error('Option does not exist.')
            sys.exit(1)

        result = {}
        result['debug'] = False
        result['wall'] = False
        result['simulator'] = False

        for opt, val in opts:
            # Help
            if opt in ('-h', '--help'):
                print >> sys.stderr, __doc__
                sys.exit(0)

            # Debug
            if opt in ('-d', '--debug'):
                result['debug'] = True
                debug = True

            # Output
            if opt in ('-w', '--wall'):
                result['wall'] = True
            if opt in ('-s', '--simulator'):
                result['simulator'] = True

        # Require output
        if not result['wall'] and not result['simulator']:
            print >> sys.stderr, __doc__
            sys.exit(1)

        return result

    def initlogging(self, **kwargs):
        """Setup root logger"""

        kwargs = lib.util.dict.explode_kwargs(kwargs)
        rootLogger = logging.getLogger('')

        if 'level' in kwargs:
            rootLogger.setLevel(kwargs['level'])

        if 'logfile' in kwargs:
            handler = logging.FileHandler(kwargs['logfile'])
            format = '%(asctime)s [%(process)d %(threadName)s] [%(name)s] %(levelname)s %(message)s'
        else:
            handler = logging.StreamHandler() # stderr
            format = '%(levelname)s %(message)s'

        if 'format' in kwargs:
            format = kwargs['format']
        formatter = logging.Formatter(format)

        handler.setFormatter(formatter)
        rootLogger.addHandler(handler)

        rootLogger.debug('Logging init complete')

if __name__ == '__main__':
    maudInstance = Maud()
    maudInstance.main(sys.argv[1:])
