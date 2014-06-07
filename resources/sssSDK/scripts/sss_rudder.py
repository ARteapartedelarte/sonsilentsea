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
from sss_dynamic import MASS_FACTOR
from sss_dynamic import sssDynamic
from sss_destroyable import sssDestroyable


D_ANGLE = radians(0.1)


class sssRudder(sssDynamic, sssDestroyable):
    def __init__(self, obj):
        sssDynamic.__init__(self, obj)
        sssDestroyable.__init__(self, obj)
        self.dist = 0.0
        ship = self.parent
        if not ship:
            return
        dr = self.worldPosition - ship.worldPosition
        self.dist = dr.length

    def setAngle(self):
        r = self['rudder']
        if abs(r) > 3:
            r = int(copysign(3, r))
            self['rudder'] = r
        aim_angle = radians(self['max_angle'] * r / 3.0)
        rot = aim_angle - self['angle']
        if rot == 0.0:
            return
        if abs(rot) > D_ANGLE:
            rot = copysign(D_ANGLE, rot)
        self.applyRotation(Vector((0.0, 0.0, -rot)), True)
        self['angle'] += rot


    def update(self):
        sssDynamic.update(self)
        sssDestroyable.update(self)
        self.setAngle()

        r = self['rudder']
        ship = self.parent
        if not r or not ship:
            return
        K = self['K']
        v = ship.getLinearVelocity(True)[0]
        f = K * r / 3.0 * v * abs(v)
        m = f * self.dist
        ship.applyTorque(Vector((0.0, 0.0, m)), True)
