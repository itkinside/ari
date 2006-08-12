#! /usr/bin/env python

import socket
import struct
import lib.output.output

class Wall(lib.output.output.Output):
    """The wall of diodes in Bodegaen at Studentersamfundet."""

    def __init__(self):
        # FIXME: Read from config!
        self.hostprefix = '192.168.0.'
        self.hosts = xrange(2, 128) # 192.168.0.2..127
        self.port = 5001

        # Init socket
        self.udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def pack(self, data):
        """
        Pack data into an UDP packet.

        One UDP pack has 26 bytes, the init byte and one byte for each of the
        25 LEDS on a board. The bytes represents a brightness value.
        
        WARNING! First/init byte must always be 0x01, or the board will stop
        responding to network traffic.
        
        Input:
            A list with 25 brightness values between 0 and 99.
        Returns:
            A UDP packet.
        """

        packet = struct.pack('BBBBBBBBBBBBBBBBBBBBBBBBBB', 1,
            data[0], data[1], data[2], data[3], data[4],
            data[5], data[6], data[7], data[8], data[9],
            data[10], data[11], data[12], data[13], data[14],
            data[15], data[16], data[17], data[18], data[19],
            data[20], data[21], data[22], data[23], data[24])

        return packet

    def send(self, data, host):
        """
        Send data to one board.

        Input:
            data: Data to send.
            host: Destination for the data.
        """

        if len(str(host)) <= 3:
            host = self.hostprefix + str(host)

        packet = self.pack(data)
        address = (host, self.port)
        self.udpsock.sendto(packet, address)

    def sendtoall(self, data):
        """
        Send data to all boards.
        
        Input:
            data: Data to send.
        """

        for host in self.hosts:
            self.send(data, host)

