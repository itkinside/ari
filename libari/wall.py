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

import libari.config
import socket
import struct

class Wall:
    """The wall of diodes in Bodegaen at Studentersamfundet."""

    def __init__(self, hosts = [], port = 5001):
        """
        Setup the Wall object.

        Input:
            hosts   A list of all hosts
            port    UDP port number to connect to

        """

        # Read input
        self.hosts = hosts
        self.port = port

        # Get config object
        self.config = config.Config()

        # Init UDP socket
        self.udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __pack(self, data):
        """
        Pack data into an UDP packet.
        
        Input:
            A list with 25 brightness values between 0 and 99.
        Returns:
            A UDP packet.

        Internal info:
            One UDP pack has 26 bytes, the init byte and one byte for each of
            the 25 LEDS on a board. The bytes represents a brightness value,
            and should be between 0 and 99 decimal.
            
            WARNING! First/init byte must always be 0x01 as other values may
            trig undocumented operations, like resetting IP and MAC.
        """

        packet = struct.pack('BBBBBBBBBBBBBBBBBBBBBBBBBB', 1,
            data[0], data[1], data[2], data[3], data[4],
            data[5], data[6], data[7], data[8], data[9],
            data[10], data[11], data[12], data[13], data[14],
            data[15], data[16], data[17], data[18], data[19],
            data[20], data[21], data[22], data[23], data[24])

        return packet

    def sendto(self, data, host):
        """
        Send data to one board.

        Input:
            data: Data to send.
            host: Destination for the data.
        """

        # If only last part of address is given, add prefix
        if len(str(host)) <= 3:
            host = self.config.hostprefix + str(host)

        packet = self.__pack(data)
        self.udpsock.sendto(packet, (host, self.port))

    def sendtoall(self, data):
        """
        Send data to all boards.
        
        Input:
            data: Data to send.
        """

        for host in self.hosts:
            self.send(data, host)

