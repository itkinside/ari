#! /usr/bin/env python

"""
distutils installation script for Ari

Parts of this script are taken from the distutils script for Django.

"""

from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES
import os

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages = []
data_files = []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
ari_dir = 'ari'
for dirpath, dirnames, filenames in os.walk(ari_dir):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([
                dirpath,
                [os.path.join(dirpath, f) for f in filenames]
            ])

setup(
    name = 'Ari',
    version = '0.1',
    description = 'Controlling system for animations on a LED wall',
    url = 'http://itk.samfundet.no/dok/ari',
    author = 'The Ari project',
    author_email = 'itk-lysfontene@samfundet.no',
    license = 'GPLv2',

    packages = packages,
    data_files = [('/etc/init.d', ['tools/ari'])] + data_files,
    scripts = ['ari-server.py'],
)
