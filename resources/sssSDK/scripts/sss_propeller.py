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


FACTOR = 1.0E6 * MASS_FACTOR


class sssPropeller(sssDynamic, sssDestroyable):
    def __init__(self, obj):
        sssDynamic.__init__(self, obj)
        sssDestroyable.__init__(self, obj)

    def update(self):
        sssDynamic.update(self)
        sssDestroyable.update(self)

        # Propeller stop conditions
        if not self['march'] or self['HP'] <= 0.0:
            self.setAngularVelocity(Vector((0.0, 0.0, 0.0)), True)
            return
        # Get the engine power and rotational velocity
        m = max(-3.0, min(3.0, self['march']))
        if m > 0:
            nu = self['nu_d']
        else:
            nu = self['nu_r']
        rpm = self['RPM'] * m / 3.0
        dt = 1.0 / g.getLogicTicRate()
        theta = 2.0 * pi / 60.0 * rpm * dt
        self.applyRotation(Vector((theta, 0.0, 0.0)), True)
        f = copysign(nu * self['power'] * sqrt(abs(m) / 3.0), m) * FACTOR
        if self.parent is not None:
            self.parent.applyForce(self.getAxisVect(Vector((f, 0.0, 0.0))),
                                   False)
