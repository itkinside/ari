#! /usr/bin/env python

import socket
import struct
import time

class Wall:
    def __init__(self):
        self.hostprefix = '192.168.0.'
        self.hosts = xrange(2, 128) # 192.168.0.2..127
        self.port = 5001

    def send(self, brightness):
        # Init socket
        udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Pack data
        # One UDP pack is 26 bytes, 0x01 and one byte for each LED
        # First byte must always be 0x01, or the board will stop responding to
        # network traffic.
        b = brightness
        data = struct.pack('bbbbbbbbbbbbbbbbbbbbbbbbbb', 1,
            b, b, b, b, b,
            b, b, b, b, b,
            b, b, b, b, b,
            b, b, b, b, b,
            b, b, b, b, b)

        # Send  
        try:    
            for host in self.hosts:
                addr = (self.hostprefix + str(host), self.port)
                udpsock.sendto(data, addr)
        except KeyboardInterrupt, e:
            pass

        # Close socket
        udpsock.close()
