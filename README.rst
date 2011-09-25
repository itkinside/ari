Ari
===


What is it?
-----------

Ari is a controlling system for animations on a LED wall, specifically
developed to manage the LED wall in "Bodegaen" of the student society in
Tronheim, Norway.

Hopefully, it may be possible to use the system for similar installations, like
the one at the Department of Computer and Information Science at the Norwegian
University of Science and Technology.

For more information on Ari, please refer to <http://itk.samfundet.no/dok/Ari>.


License
-------

Ari is made publicly available under the terms of the GNU General Public
License version 2. All contributions are the property of their respective
contributors.


Authors
-------

The following persons have contributed to the development of Ari:

    * Stein Magnus Jodal <jodal@samfundet.no>
    * Vidar Wahlberg <canidae@samfundet.no>
    * Thomas Adamcik <adamcik@samfundet.no>
    * Kristian Klette <klette@samfundet.no>

If you make a contribution to Ari, feel free to add yourself to this list.


Installing
----------

1. Install all dependencies, as found in docs/requirements.txt.

   On Debian systems, the following should suffice::

    sudo aptitude install python-gd python-numpy python-pygame

   Alternatively, the docs/requirements.txt file can maybe be used by ``pip``
   to install the needed libraries.

2. Install the Ari library, executable and init.d script::

    sudo python setup.py install


Running as a daemon
-------------------

To run Ari as a daemon, painting to the LED wall:

1. To make Ari start at boot, activate the init.d script::

    sudo update-rc.d ari defaults

2. Start ari using the init.d script::

    sudo invoke-rc.d ari start


Running the simulator
---------------------

To run Ari using the built-in simulator, run::

    ari-server.py --simulator

To get more help on how to use the ari-server.py command, run::

    ari-server.py --help

