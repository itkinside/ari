#! /usr/bin/env python
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
