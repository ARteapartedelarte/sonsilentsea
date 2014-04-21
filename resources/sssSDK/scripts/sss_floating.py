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


GRAV = 9.81
RHO = 1025.0


class sssFloating(sssDynamic):
    def __init__(self, obj):
        super(sssFloating, self).__init__(obj)
        self.collisionCallbacks.append(self.collision)

    def displacement(self):
        z = -self.worldPosition[2]
        vols_z = eval(self['vols_z'])
        vols_v = eval(self['vols_v'])
        if z <= vols_z[0]:
            vol = 0.0
        elif z >= vols_z[-1]:
            vol = vols_v[-1]
        else:
            i = 1
            while i < len(vols_z):
                if vols_z[i] > z:
                    tg = (vols_v[i] - vols_v[i - 1]) / (vols_z[i] - vols_z[i - 1])
                    vol = vols_v[i - 1] + (z - vols_z[i - 1]) * tg
                    break
                i += 1
        return vol * RHO

    def rightingMoment(self):
        X = Vector((-1.0, 0.0, 0.0))
        Y = Vector((0.0, 1.0, 0.0))
        Z = Vector((0.0, 0.0, 1.0))
        mat = self.localOrientation
        mx = Z.dot(mat * Y) - radians(self['roll'])
        my = Z.dot(mat * X) - radians(self['pitch'])
        return -float(self['real_mass']) * GRAV * Vector((self['GMT'] * mx,
                                                          self['GML'] * my,
                                                          0.0))

    def update(self):
        super(sssFloating, self).update()

        fz = GRAV * self.displacement()
        f = Vector((0.0, 0.0, fz)) * MASS_FACTOR
        self.applyForce(f, False)

        m = (self.rightingMoment()) * MASS_FACTOR
        self.applyTorque(m, False)    

    def collision(self, obj):
        """ Perform the explosion against an object
        @param obj Collider object
        """
        pass
