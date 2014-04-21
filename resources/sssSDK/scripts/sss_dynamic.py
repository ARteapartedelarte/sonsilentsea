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


MASS_FACTOR = 1e-3


class sssDynamic(bge.types.KX_GameObject):
    def __init__(self, obj):
        self.v = None
        self.vback = None

    def update(self):
        self.vback = self.v
        self.v = self.getLinearVelocity()
        if self.vback is None:
            self.vback = self.v

    def getLinearMomentum(self):
        """Returns the linear momentum p = m * v. You may consider using the
        kinetic energy instead, which is cheaper computed.
        """
        if self.vback is None:
            return 0.0
        m = self.mass
        if 'real_mass' in self:
            m = float(self['real_mass'])
        v = self.vback.length
        return m * v

    def getKineticEnergy(self):
        """Returns the kinetic energy e = 1/2 m * v**2. It is cheaper to the
        linear momentum computation.
        """
        if self.vback is None:
            return 0.0
        m = self.mass
        if 'real_mass' in self:
            m = float(self['real_mass'])
        v2 = self.vback.length_squared
        return 0.5 * m * v2
