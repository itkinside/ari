#! /usr/bin/env python
#
# Authors: Stein Magnus Jodal <jodal@samfundet.no>
#

import socket
import struct
import sys
import time

def main(args):
    # Config variables
    prefixnow = (192, 168, 0)
    prefixset = (192, 168, 0)
    hosts = range(2, 128)
    port = 5001

    # Init socket
    udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for i, host in enumerate(hosts):
        # Make packet
        packet = struct.pack('BBBBBBBBBBB', 2,
            prefixset[0], prefixset[1], prefixset[2], host, # IP
            19, 55, 186, 190, 0, host) # Mac (19, 55, 186, 190 = 13:37:ba:be)

        # Construct address
        host = '%d.%d.%d.%d' % (prefixnow[0], prefixnow[1], prefixnow[2], host)
        address = (host, port)

        # Debug output
        print "%s: %s" % (host, struct.unpack('BBBBBBBBBBB', packet))

        # Send packet
        if len(args) and args[0] == 'reallyset':
            udpsock.sendto(packet, address)

        # Sleep a bit, so the wall fades in a nicer fashion ;-)
        time.sleep(0.1)

    if not len(args) or not args[0] == 'reallyset':
        print "Run '" + sys.argv[0] + " reallyset' to actually send the packages to the wall."

if __name__ == '__main__':
    main(sys.argv[1:])
