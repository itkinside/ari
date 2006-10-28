#! /usr/bin/env python
#
# libari - Library for manipulating a diode wall
#
# This module is based on the nav.daemon module created for UNINETT AS by
# Stein Magnus Jodal, so the copyright is theirs:
#
# Copyright (C) 2006 UNINETT AS
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
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# Authors: Stein Magnus Jodal <jodal@samfundet.no>
#

"""
Help functions for daemonizing a process

The normal usage sequence for the functions is:
    1. switchuser(username)
        Switch user the process is running as
    2. justme(pidfile)
        Check that the daemon is not already running
    3. daemonize(pidfile)
        Go into the background
        NOTE: Sets atexit function to daemonexit()
    4. daemonexit(pidfile)
        Clean up and delete the pidfile

All exceptions raised subclasses DaemonError.

"""

__copyright__ = "Copyright 2006 UNINETT AS"
__license__ = "GPL"
__author__ = "Stein Magnus Jodal (stein.magnus@jodal.no)"
__id__ = "$Id: daemon.py 3494 2006-07-03 09:12:11Z jodal $"

import atexit
import grp
import logging # Requires Python >= 2.3
import os
import pwd
import sys

logger = logging.getLogger('ari.arid')

class DaemonError(Exception):
    """Base class for all exceptions raised by the daemon lib."""
    pass

class UserNotFoundError(DaemonError):
    """Raised if requested user is not found and we have to run as root."""

    def __init__(self, username):
        self.username = username

    def __str__(self):
        return "User (%s) not found, can't switch process user." \
         % self.username

class SwitchUserError(DaemonError):
    """Raised if user switch failes, e.g. we don't have enough permissions."""

    def __init__(self, olduid, oldgid, newuid, newgid):
        self.olduid = olduid
        self.oldgid = oldgid
        self.newuid = newuid
        self.newgid = newgid

    def __str__(self):
        return "Failed to switch uid/gid from %d/%d to %d/%d." \
         % (self.olduid, self.oldgid, self.newuid, self.newgid)

class AlreadyRunningError(DaemonError):
    """Raised if the daemon is alrady running."""

    def __init__(self, pid):
        self.pid = pid

    def __str__(self):
        return "Daemon is already running with pid %d." % self.pid

class PidFileReadError(DaemonError):
    """Raised if we can't read a numeric pid from the pidfile."""

    def __init__(self, pidfile):
        self.pidfile = pidfile

    def __str__(self):
        return "Can't read pid from pidfile (%s)." % self.pidfile

class PidFileWriteError(DaemonError):
    """Raised if we can't write the pid to the pidfile."""

    def __init__(self, pidfile, error):
        self.pidfile = pidfile
        self.error = error

    def __str__(self):
        return "Can't write pid to or remove pidfile (%s). (%s)" \
         % (self.pidfile, self.error)

class ForkError(DaemonError):
    """Raised if a fork fails."""

    def __init__(self, forkno, error):
        self.forkno = forkno
        self.error = error

    def __str__(self):
        return "Failed fork #%d. (%s)" % (self.forkno, self.error)

def switchuser(username):
    """
    Switch user the process is running as.

    This method will only work if is are running as root.

    Arguments:
        ``username'' is the username of the user we want to run as.

    Returns/raises:
        If switch is a success, returns True.
        If user is unknown and we're still running as root, raises
        UserNotFoundError.
        If failing to switch, raises SwitchUserError.

    """

    # Get UID/GID we're running as
    olduid = os.getuid()
    oldgid = os.getgid()

    try:
        # Try to get information about the given username
        name, passwd, uid, gid, gecos, dir, shell = pwd.getpwnam(username)
    except KeyError, error:
        raise UserNotFoundError(username)
    else:
        if olduid != uid:
            try:
                # Set primary group
                os.setgid(gid)

                # Set non-primary groups
                gids = []
                for (name, passwd, gid, members) in grp.getgrall():
                    if username in members:
                        gids.append(gid)
                if len(gids) > 0:
                    os.setgroups(gids)

                # Set user id
                os.setuid(uid)
            except OSError:
                # Failed changing uid/gid
                logger.debug("Failed chaning uid/gid from %d/%d to %d/%d.",
                 olduid, oldgid, uid, gid)
                raise SwitchUserError(olduid, oldgid, uid, gid)
            else:
                # Switch successfull
                logger.debug("uid/gid changed from %d/%d to %d/%d.",
                 olduid, oldgid, uid, gid)
                return True
        else:
            # Already running as the given user
            logger.debug("Running as uid/gid %d/%d.", olduid, oldgid)
            return True


def justme(pidfile):
    """
    Check if already running.

    Arguments:
        ``pidfile'' is the path to the process' pidfile.

    Returns/raises:
        If we're alone, returns True.
        If pidfile is unreadable, raises PidFileUnreadableError
        If daemon is already running, raises AlreadyRunningError.

    """

    # If pidfile exists (is readable)
    if os.access(pidfile, os.R_OK):
        fd = file(pidfile, 'r')
        pid = fd.readline().strip()
        fd.close()

        # Check if pid is readable
        if pid.isdigit():
            pid = int(pid) 
        else:
            logger.debug("Can't read pid from pid file %s.", pidfile)
            raise PidFileReadError(pidfile)

        try:
            # Sending signal 0 to check if process is alive
            os.kill(pid, 0)
        except OSError, error:
            # Normally this means "No such process", and thus we're alone
            return True
        else:
            # We assume the process lives and bails out
            logger.debug("%s already running with pid %d.",
             sys.argv[0], pid)
            raise AlreadyRunningError(pid)
    else:
        # No pidfile, assume we're alone
        return True


def daemonize(pidfile, stdout = '/dev/null', stderr = None,
 stdin = '/dev/null'):
    """
    Move the process to the background as a daemon and write the pid of the
    daemon to the pidfile.

    Inspired by
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012

    Arguments:
        ``pidfile'' is the path to the process' pidfile.
        ``stdout'' is where to redirect stdout. Defaults to /dev/null.
        ``stderr'' is where to redirect stderr. Defaults to stdout.
        ``stdin'' is where to redirect stdin. Defaults to /dev/null.

    Returns/raises:
        If success, returns True.
        If fork fails, raises ForkError.
        If writing of pidfile fails, raises PidFileWriteError.

    """

    # NOTE: When we require Python 2.4, replace '/dev/null' with
    # os.path.devnull in the default argument values above

    # Do first fork
    # (allow shell to return, and permit us to call setsid())
    try:
        pid = os.fork()
        if pid > 0:
            # We're the first parent. Exit!
            logger.debug("First parent exiting. Second has pid %d.", pid)
            sys.exit(0)
    except OSError, error:
        logger.debug("Fork #1 failed. (%s)", error)
        raise ForkError(1, error)

    # Decouple from parent environment
    os.chdir('/') # In case the dir we started in are removed
    os.umask(0)
    os.setsid()

    # Do second fork
    # (prevent us from accidentally reacquiring a controlling terminal)
    try:
        pid = os.fork()
        if pid > 0:
            # We're the second parent. Exit!
            logger.debug("Second parent exiting. Daemon has pid %d.", pid)
            sys.exit(0)
    except OSError, error:
        logger.exception("Fork #2 failed. (%s)", error)
        raise ForkError(2, error)

    # Now only the child is left :-)

    # Open file descriptors
    if not stderr:
        stderr = stdout
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    pid = os.getpid()
    logger.debug("Daemon started with pid %d.", pid)

    # Write pidfile
    try:
        fd = file(pidfile, 'w+')
    except IOError, error:
        logger.debug("Cannot open pidfile %s for writing. Exiting. (%s)",
         pidfile, error)
        raise PidFileWriteError(pidfile, error)

    fd.write("%d\n" % pid)
    fd.close()

    # Set cleanup function to be run at exit so pidfile always is removed
    atexit.register(daemonexit, pidfile)
    
    # Close newfds before dup2-ing them
    sys.stdout.flush()
    sys.stderr.flush()
    os.close(sys.stdin.fileno())
    os.close(sys.stdout.fileno())
    os.close(sys.stderr.fileno())

    # Redirect standard file descriptors
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

    return True


def daemonexit(pidfile):
    """
    Clean up after daemon process. This functions is only runned by the
    atexit handler.

    Arguments:
        ``pidfile'' is the path to the process' pidfile.

    Returns/raises:
        If success, returns True.
        If removal of pidfile fails, raises PidFileWriteError.

    """

    logger.debug("Daemon is exiting. Cleaning up...")

    try:
        os.remove(pidfile)
    except Exception, error:
        logger.debug("Can't remove pidfile (%s). (%s)", pidfile, error)
        raise PidFileWriteError(pidfile, error)

    logger.debug("pidfile (%s) removed.", pidfile)
    return True

