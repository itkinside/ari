#! /usr/bin/env python

import socket
import struct
import lib.output.output

class Wall(lib.output.output.Output):
    def __init__(self):
        # FIXME: Read from config!
        self.hostprefix = '192.168.0.'
        self.hosts = xrange(2, 128) # 192.168.0.2..127
        self.port = 5001

        # Init socket
        self.udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def pack(self, data):
        """Pack data into and UDP packet.

        One UDP pack is 26 bytes, 0x01 and one byte for each LED. First byte
        must always be 0x01, or the board will stop responding to network
        traffic.
        
        Takes an list with 25 brightness values between 0 and 99.
        Returns an UDP packet."""

        packet = struct.pack('bbbbbbbbbbbbbbbbbbbbbbbbbb', 1,
            data[0], data[1], data[2], data[3], data[4],
            data[5], data[6], data[7], data[8], data[9],
            data[10], data[11], data[12], data[13], data[14],
            data[15], data[16], data[17], data[18], data[19],
            data[20], data[21], data[22], data[23], data[24])

        return packet

    def sendall(self, data):
        """FIXME"""

        packet = self.pack(data)

        # Send to all boards
        for host in self.hosts:
            address = (self.hostprefix + str(host), self.port)
            self.udpsock.sendto(packet, address)
