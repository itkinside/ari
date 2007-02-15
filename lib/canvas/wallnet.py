#! /usr/bin/env python
#
# Copyright (C) 2006 Stein Magnus Jodal
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

import lib.config
import socket
import struct

class WallNet:
    """Packs and sends updates to the physical wall."""

    def __init__(self, hosts = [], port = 5001):
        """
        Setup the WallNet object.

        Input:
            hosts   A list of all hosts
            port    UDP port number to connect to

        """

        # Read input
        self.hosts = hosts
        self.port = port

        # Get config object
        self.config = lib.config.Config()

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
            data[4], data[3], data[2], data[1], data[0],
            data[9], data[8], data[7], data[6], data[5],
            data[14], data[13], data[12], data[11], data[10],
            data[19], data[18], data[17], data[16], data[15],
            data[24], data[23], data[22], data[21], data[20])

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
            self.sendto(data, host)

