#! /usr/bin/env python
#
# Copyright (C) 2007 Stein Magnus Jodal
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

import os
import pickle

import ari.config
from ari.util.dict import *

class Reader:
    """General file reader"""

    def __init__(self):
        self.config = ari.config.Config()

    def load(self, *args, **kwargs):
        """
        Loads a media file, if possible from cache

        Uses pickle to cache and reuse previously loaded media files.

        Input:
            filepath    File name of the BML file

        Returns:
            List of tuples with the following data:
            - Frame duration
            - Frame data as a numpy array

        """

        kwargs = explode_kwargs(kwargs)
        cachefilename = '%s/%s.pickle' % (
            self.config.cachedir,
            kwargs['filepath'].replace('/', '_'),
        )

        if not os.path.isfile(cachefilename):
            frames = self.parse(kwargs=kwargs)
            pickle.dump(frames, open(cachefilename, 'w'))
            return frames
        else:
            return pickle.load(open(cachefilename, 'r'))

    def parse(self, *args, **kwargs):
        """
        Loads and parses a media file

        Identifies the correct reader and loads of the dirty work to it.

        Input:
            filepath    File name of the BML file

        Returns:
            List of tuples with the following data:
            - Frame duration
            - Frame data as a numpy array

        """

        kwargs = explode_kwargs(kwargs)
        (_, ext) = os.path.splitext(kwargs['filepath'])
        ext = ext.replace('.', '').lower()
        reader = None

        if ext == 'bml':
            import ari.util.reader.bmlreader
            reader = ari.util.reader.bmlreader.BMLReader()
        elif ext == 'blm':
            import ari.util.reader.blmreader
            reader = ari.util.reader.blmreader.BLMReader()
        else:
            import ari.util.reader.gdreader
            reader = ari.util.reader.gdreader.GDReader()

        return reader.parse(kwargs=kwargs)

class ReaderException(Exception):
    """Base class for all exceptions raised by readers."""
