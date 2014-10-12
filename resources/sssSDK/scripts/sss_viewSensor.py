##############################################################################
#                                                                            #
#  This file is part of SonSilentSea, a free ships based combatr game.       #
#  Copyright (C) 2014  Jose Luis Cercos Pita <jlcercos@gmail.com>            #
#                                                                            #
#  AQUAgpusph is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by      #
#  the Free Software Foundation, either version 3 of the License, or         #
#  (at your option) any later version.                                       #
#                                                                            #
#  AQUAgpusph is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#  GNU General Public License for more details.                              #
#                                                                            #
#  You should have received a copy of the GNU General Public License         #
#  along with AQUAgpusph.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                            #
##############################################################################

import bge
from bge import logic as g
from math import *
from mathutils import *
import random
from sss_sensor import sssSensor


# Remote object volume of reference, i.e. The probability of detection of an
# object of this volume is determined only by kernel() function,
# proportionally increasing for bigger objects
_REF_VOL_ = 50000.0
# List of viewable objects
_VIEWABLE_OBJECTS_ = ('sssFloating', 'sssShip')


class sssViewSensor(sssSensor):
    def __init__(self, obj):
        sssSensor.__init__(self, obj)

    def typeName(self):
        return 'sssSensor'  # All the sensors will get the type 'sssSensor'

    def update(self):
        if self.parent is None:
            return
        # Scan all the scene objects
        scene = g.getCurrentScene()
        objlist = scene.objects
        for obj in objlist:
            # Discard self detection
            if obj == self.parent:
                continue
            # Analyze just the viewable objects
            if not hasattr(obj, 'typeName'):
                continue
            if not obj.typeName() in _VIEWABLE_OBJECTS_:
                continue
            # Get the viewable volume (an object is considered viewable if it
            # is emerged, or submerged least than 15 meters)
            z = -obj.worldPosition[2] - 15.0
            vol = obj.getVolume(z, False) / _REF_VOL_
            if vol == 0.0:
                continue
            # Get the probability kernel function
            W = self.kernel(obj)
            if W == 0.0:
                continue
            if W == 1.0:
                # It is closer than the minimum distance
                self.add_contact(obj)
                continue
            if random.random() < W * (vol**0.33):
                self.add_contact(obj)
