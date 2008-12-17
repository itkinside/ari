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

import math
import numarray

def growtobox(array, boxw, boxh):
    """Grow numarray to fill box while keeping aspect ratio"""

    # Find max scale ratio
    (oldw, oldh) = array.shape
    ratiow = int(math.floor(boxw / oldw))
    ratioh = int(math.floor(boxh / oldh))
    if ratiow < ratioh:
        ratio = ratiow
    else:
        ratio = ratioh

    # Scale array
    res = scale(array, ratio)

    return res

def scale(array, ratio):
    """Scale numarray with given ratio"""

    # Growth not possible, return array
    if ratio == 1:
        return array

    # New array of max size
    (oldw, oldh) = array.shape
    resw = oldw * ratio
    resh = oldh * ratio
    res = numarray.zeros((resw, resh))

    # Scale old array to new array
    for x in range(resw):
        for y in range(resh):
            res[x][y] = array[x / ratio][y / ratio]

    return res

