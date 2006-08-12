#! /usr/bin/env python

import math
import lib.outputhandler

class Canvas:
    """Paint on the canvas, and the wall shows your art!"""

    def __init__(self):
        self.oh = lib.outputhandler.OutputHandler()
        self.output = self.oh.getOutput()

        # FIXME: Read from config
        self.model = {
            0: {
                'xpos': 0,
                'ypos': 0,
                'width': 2,
                'height': 6,
                '0,0': 12, '1,0': 13,
                '0,1': 10, '1,1': 11,
                '0,2':  8, '1,2':  9,
                '0,3':  6, '1,3':  7,
                '0,4':  4, '1,4':  5,
                '0,5':  2, '1,5':  3
            },
            1: {
                'xpos': 0,
                'ypos': 7,
                'width': 9,
                'height': 6,
                '0,0': 59, '1,0': 60, '2,0': 61, '3,0': 62, '4,0': 63,
                    '5,0': 64, '6,0': 65, '7,0': 66, '8,0': 67,
                '0,1': 50, '1,1': 51, '2,1': 52, '3,1': 53, '4,1': 54,
                    '5,1': 55, '6,1': 56, '7,1': 57, '8,1': 58,
                '0,2': 41, '1,2': 42, '2,2': 43, '3,2': 44, '4,2': 45,
                    '5,2': 46, '6,2': 47, '7,2': 48, '8,2': 49,
                '0,3': 32, '1,3': 33, '2,3': 34, '3,3': 35, '4,3': 36,
                    '5,3': 37, '6,3': 38, '7,3': 39, '8,3': 40,
                '0,4': 23, '1,4': 24, '2,4': 25, '3,4': 26, '4,4': 27,
                    '5,4': 28, '6,4': 29, '7,4': 30, '8,4': 31,
                '0,5': 14, '1,5': 15, '2,5': 16, '3,5': 17, '4,5': 18,
                    '5,5': 19, '6,5': 20, '7,5': 21, '8,5': 22
            },
            2: {
                'xpos': 0,
                'ypos': 25,
                'width': 3,
                'height': 6,
                '0,0': 83, '1,0': 84, '2,0': 85,
                '0,1': 80, '1,1': 81, '2,1': 82,
                '0,2': 77, '1,2': 78, '2,2': 79,
                '0,3': 74, '1,3': 75, '2,3': 76,
                '0,4': 71, '1,4': 72, '2,4': 73,
                '0,5': 68, '1,5': 69, '2,5': 70
            },
            3: {
                'xpos': 0,
                'ypos': 49,
                'width': 6,
                'height': 6,
                '0,0': 116, '1,0': 117, '2,0': 118, '3,0': 119, '4,0': 120,
                    '5,0': 121,
                '0,1': 110, '1,1': 111, '2,1': 112, '3,1': 113, '4,1': 114,
                    '5,1': 115,
                '0,2': 104, '1,2': 105, '2,2': 106, '3,2': 107, '4,2': 108,
                    '5,2': 109,
                '0,3':  98, '1,3':  99, '2,3': 100, '3,3': 101, '4,3': 102,
                    '5,3': 103,
                '0,4':  92, '1,4':  93, '2,4':  94, '3,4':  95, '4,4':  96,
                    '5,4':  97,
                '0,5':  86, '1,5':  87, '2,5':  88, '3,5':  89, '4,5':  90,
                    '5,5':  91
            },
            4: {
                'xpos': 0,
                'ypos': 67,
                'width': 1,
                'height': 6,
                '0,0': 127,
                '0,1': 126,
                '0,2': 125,
                '0,3': 124,
                '0,4': 123,
                '0,5': 122
            },
        }

        self.struct = self.createstruct()

    def createstruct(self):
        struct = {}
        for p in self.model:
            panel = self.model[p]
            struct[p] = {}
            for bx in range(panel['width']):
                struct[p][bx] = {}
                for by in range(panel['height']):
                    struct[p][bx][by] = {}
                    for px in range(5):
                        struct[p][bx][by][px] = {}
                        for py in range(5):
                            struct[p][bx][by][px][py] = 0
        return struct

    def getstructpos(self, x, y):
        # Find panel
        p = 0
        dx = 0
        for p in range(len(self.model)):
            dx += self.model[p]['width'] * 5
            if x < dx:
                dx -= self.model[p]['width'] * 5
                break

        # Find board positions
        bx = int(math.floor((x - dx) / 5))
        by = int(math.floor(y / 5))

        # Find pixel positions
        px = (x - dx) % 5
        py = y % 5

        return (p, bx, by, px, py)

    def getallboards(self):
        boards = []
        for p in self.struct:
            for bx in self.struct[p]:
                for by in self.struct[p][bx]:
                    boards.append((p, bx, by))
        return boards

    def getpixel(self, x, y):
        if x < 0 or x >= 105 or y < 0 or y >= 30:
            return False
        
        (p, bx, by, px, py) = self.getstructpos(x, y)
        return self.struct[p][bx][by][px][py]

    def setpixel(self, x, y, b):
        if x < 0 or x >= 105 or y < 0 or y >= 30:
            return False

        (p, bx, by, px, py) = self.getstructpos(x, y)
        self.struct[p][bx][by][px][py] = b

    def updateboard(self, p, bx, by):
        data = []
        for px in range(5):
            for py in range(5):
                data.append(self.struct[p][bx][by][px][py])
        self.output.send(data, self.model[p]['%d,%d' % (bx, by)])

    def updateall(self):
        for board in self.getallboards():
            (p, bx, by) = board
            self.updateboard(p, bx, by)

# OLD STUFF

    def fillboard(self, brightness, panel, xpos, ypos):
        data = []
        for i in range(25):
            data.append(brightness)
        self.output.send(data,
            self.model[panel]['%d,%d' % (xpos, ypos)])

    def fill(self, brightness, startx = 0, starty = 0, endx = 105, endy = 30):
        """
        Fill area.

        Input:
            brightness: The brightness of the area.
            startx: X-position of start point, default 0.
            starty: Y-position of start point, default 0.
            endx: X-position of end point, default 105.
            endy: Y-position of end point, default 30.
        """

        data = []
        for i in range(25):
            data.append(brightness)
        self.output.sendtoall(data)

    def line(self, brightness, startx, starty, endx, endy):
        """
        Paint a line between to points.

        Input:
            brightness: The brightness of the line.
            startx: X-position of start point.
            starty: Y-position of start point.
            endx: X-position of end point.
            endy: Y-position of end point.
        """

        pass # FIXME: Implement this!
