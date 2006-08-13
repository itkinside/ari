#! /usr/bin/env python
#
# libari - Library for manipulating a diode wall
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

from distutils.core import setup
setup(name = "libari",
      version = "0.1",
      description = "Library for manipulating a diode wall.",
      author = "Stein Magnus Jodal",
      author_email = "jodal@samfundet.no",
      license = "GNU GPL v2",
      url = "http://itk.samfundet.no/dok/ari",
      packages = ['libari'],
      package_dir = {'libari': '.'})