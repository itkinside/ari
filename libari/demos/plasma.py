#! /usr/bin/env python
#
# arid - Daemon for running demos on a diode wall 
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

import libari.demos.base

class Plasma(libari.demos.base.Base):
    """Plasma demo"""

    def setup(self, min = 0, max = 99, step = 3):
        """
        Input:
            min     Minimum brightness, default 0
            max     Maximum brightness, default 99
            step    Brightness steps, default 3
        """

        # Check input
        if int(min) >= 0 and int(min) < 100:
            self.min = int(min)
        else:
            self.min = 0

        if int(max) >= 0 and int(min) < 100:
            self.max = int(max)
        else:
            self.max = 99

        if self.min > self.max:
            self.min, self.max = self.max, self.min

        if int(step) < 99:
            self.step = step
        else:
            self.step = 3

    def run(self):
        while True:
            if self.drawable:
                pass # FIXME

"""
void
generatePlasmaFrame(float timervalue)
{
  int x, y;
  float z1, z2, z3, freq1, freq2, freq3, shiftx, shifty, val;
  
  if (!imgbuffer) { 
    printf("EffectLib: Not initialized!\n");
    return;
  }
 
  freq1 = 30.0 + 20.0*sinf(timervalue);
  freq2 = 30.0 + 10.0*cosf(timervalue*2);
  freq3 = 30.0 + 20.*sinf(freq1); 
        
  shiftx = bufferwidth*sinf(timervalue) / 4.0;
  shifty = bufferheight*cosf(timervalue) / 4.0;
 
  for (y=0;y < bufferheight;++y) {
    for (x=0;x < bufferwidth;++x) {
      z1 = sinf( ((float) x)/freq1*1.7*3.1415 + shiftx);
      z2 = sinf( ((float) x)/3.0 + ((float) y)/freq2*1.5*3.1415 + shifty);
      z3 = sinf( ((float) y)/freq3*0.1*3.1415);
      val = fabs(z1+z2+z3) * 255;
      if (val > 255) val = 255;
      imgbuffer[(y*bufferwidth) + x] = (unsigned char) val;
    } 
  }
}
"""
