#! /usr/bin/env python
#
# libari - Library for manipulating a diode wall
# Copyright (C) 2006 Vidar Wahlberg
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
#
# Authors: Vidar Wahlberg <canidae@samfundet.no>
#

import libari.demos.base
import random

class Tetris(libari.demos.base.Base):
    """Tetris!"""

    # variables
    curpiece = 1
    curpiecedir = 1
    curpiecex = 0
    curpiecey = 0
    tardir = 0
    tarx = 0
    movesperdrop = 2

    # height penalty
    heightpenalty = 10
    # space beneath piece penalty
    spacebeneathpiecepenalty = 42

    # pieces
    # 1. ****
    # 2. **
    #     **
    # 3.  **
    #    **
    # 4. ***
    #     *
    # 5. ***
    #    *
    # 6. ***
    #      *
    # 7. **
    #    **
    piece = [
                [
                    [
                        [99, 99, 99, 99]
                    ],
                    [
                        [99],
                        [99],
                        [99],
                        [99]
                    ]
                ],
                [
                    [
                        [99, 99],
                        [ 0, 99, 99]
                    ],
                    [
                        [ 0, 99],
                        [99, 99],
                        [99]
                    ]
                ],
                [
                    [
                        [ 0, 99, 99],
                        [99, 99]
                    ],
                    [
                        [99],
                        [99, 99],
                        [ 0, 99]
                    ]
                ],
                [
                    [
                        [99, 99, 99],
                        [ 0, 99]
                    ],
                    [
                        [ 0, 99],
                        [99, 99],
                        [ 0, 99]
                    ],
                    [
                        [ 0, 99],
                        [99, 99, 99]
                    ],
                    [
                        [99],
                        [99, 99],
                        [99]
                    ]
                ],
                [
                    [
                        [99, 99, 99],
                        [99]
                    ],
                    [
                        [99, 99],
                        [ 0, 99],
                        [ 0, 99]
                    ],
                    [
                        [ 0,  0, 99],
                        [99, 99, 99]
                    ],
                    [
                        [99],
                        [99],
                        [99, 99]
                    ]
                ],
                [
                    [
                        [99, 99, 99],
                        [ 0,  0, 99]
                    ],
                    [
                        [ 0, 99],
                        [ 0, 99],
                        [99, 99]
                    ],
                    [
                        [99],
                        [99, 99, 99]
                    ],
                    [
                        [99, 99],
                        [99],
                        [99]
                    ]
                ],
                [
                    [
                        [99, 99],
                        [99, 99]
                    ]
                ]
            ]

    def prepare(self):
        self.curpiece = random.randint(0, len(self.piece) - 1)
        self.curpiecedir = random.randint(0, len(self.piece[self.curpiece]) - 1)
        self.curpiecex = self.sizex / 2 - 20
        self.curpiecey = 0
        self.movesperdrop = int(self.sizex / self.sizey) + 1
        if self.movesperdrop <= 0:
            self.movesperdrop = 1
        self.canvas.blank()
        self.findtarget()

    def findtarget(self):
        # when a new piece appears we figure out where to ultimately place it
        score = -1
        self.tardir = 0
        self.tarx = 0
        for piecedir in xrange(len(self.piece[self.curpiece])):
            piecewidth = 1
            for py in xrange(len(self.piece[self.curpiece][piecedir])):
                if len(self.piece[self.curpiece][piecedir][py]) > piecewidth:
                    piecewidth = len(self.piece[self.curpiece][piecedir][py])
            for sx in xrange(self.sizex - piecewidth + 1):
                totheight = self.sizey
                for px in xrange(piecewidth):
                    height = self.sizey
                    for sy in xrange(self.sizey):
                        if self.canvas.getpixel(sx + px, sy) > 0:
                            height = sy
                            break;
                    for py in xrange(len(self.piece[self.curpiece][piecedir]) - 1, -1, -1):
                        if len(self.piece[self.curpiece][piecedir][py]) > px and self.piece[self.curpiece][piecedir][py][px] > 0:
                            break
                        height += 1
                    if height < totheight:
                        totheight = height
                # calculate penalty
                hp = (self.sizey + len(self.piece[self.curpiece][piecedir]) - totheight) * self.heightpenalty
                sbpp = 0
                for px in xrange(piecewidth):
                    for sy in xrange(totheight, self.sizey - 1):
                        if self.canvas.getpixel(sx + px, sy) == 0:
                            sbpp += self.spacebeneathpiecepenalty
                    for py in xrange(1, len(self.piece[self.curpiece][piecedir])):
                        if (len(self.piece[self.curpiece][piecedir][py]) <= px or self.piece[self.curpiece][piecedir][py][px] == 0) and self.canvas.getpixel(sx + px, totheight - len(self.piece[self.curpiece][piecedir]) + py) == 0:
                            sbpp += self.spacebeneathpiecepenalty
                if score == -1 or hp + sbpp < score or (hp + sbpp == score and random.randint(0, self.sizex) == 0):
                    score = hp + sbpp
                    self.tardir = piecedir
                    self.tarx = sx

#        print "score : " + str(score)
#        print "tardir: " + str(self.tardir)
#        print "tarx  : " + str(self.tarx)

    def run(self):
        # The demo
        while self.runnable:
            if self.drawable:
                # undraw piece
                for py in xrange(len(self.piece[self.curpiece][self.curpiecedir])):
                    for px in xrange(len(self.piece[self.curpiece][self.curpiecedir][py])):
                        if self.piece[self.curpiece][self.curpiecedir][py][px] > 0:
                            self.canvas.setpixel(self.curpiecex + px, self.curpiecey + py, 0)
                # do the move
                for move in xrange(self.movesperdrop):
                    if self.curpiecedir != self.tardir: # and random.randint(0, self.sizey) == 0:
                        self.curpiecedir = (self.curpiecedir + 1) % len(self.piece[self.curpiece])
                    elif self.curpiecex < self.tarx:
                        self.curpiecex += 1
                    elif self.curpiecex > self.tarx:
                        self.curpiecex -= 1
                self.curpiecey += 1
                # check if we hit something
                crash = False
                for py in xrange(len(self.piece[self.curpiece][self.curpiecedir]) - 1, -1, -1):
                    for px in xrange(len(self.piece[self.curpiece][self.curpiecedir][py])):
                        if self.piece[self.curpiece][self.curpiecedir][py][px] > 0 and (self.curpiecey + py + 1 >= self.sizey or self.canvas.getpixel(self.curpiecex + px, self.curpiecey + py + 1) > 0):
                            # dude, we like totally hit something
                            crash = True
                            break
                    if crash:
                        break
                # draw piece
                for py in xrange(len(self.piece[self.curpiece][self.curpiecedir])):
                    for px in xrange(len(self.piece[self.curpiece][self.curpiecedir][py])):
                        if self.piece[self.curpiece][self.curpiecedir][py][px] > 0:
                            self.canvas.setpixel(self.curpiecex + px, self.curpiecey + py, self.piece[self.curpiece][self.curpiecedir][py][px])
                # update
                self.canvas.update()
                if crash:
                    # check if we can remove some lines
                    # FIXME
                    print self.curpiecey, self.curpiecey + len(self.piece[self.curpiece][self.curpiecedir])
                    for sy in xrange(self.curpiecey, self.curpiecey + len(self.piece[self.curpiece][self.curpiecedir])):
                        remove = True
                        for sx in xrange(self.sizex):
                            if self.canvas.getpixel(sx, sy) == 0:
                                remove = False
                                break
                        if remove:
                            for sy2 in xrange(sy):
                                for sx in xrange(self.sizex):
                                    self.canvas.setpixel(sx, sy, self.canvas.getpixel(sx, sy2))
                    # fetch a new piece
                    self.curpiece = random.randint(0, len(self.piece) - 1)
                    self.curpiecedir = random.randint(0, len(self.piece[self.curpiece]) - 1)
                    self.curpiecex = self.sizex / 2 - 20
                    self.curpiecey = 0
                    self.findtarget()
            #self.sleep()
