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


class sssSensor(bge.types.KX_GameObject):
    def __init__(self, obj):
        self.h = 0.5 * (self['max_distance'] - self['min_distance'])

    def typeName(self):
        return 'sssSensor'

    def update(self):
        pass

    def kernel(self, obj):
        """Compute the probability of detection modifier.
        """
        r = obj.worldPosition.xy - self.worldPosition.xy
        l_squared = r.length_squared
        if l_squared < self['min_distance']**2:
            return 1.0
        if l_squared < self['max_distance']**2:
            return 0.0

        l = r.length - self['min_distance']
        q = l / h  # from 0 to 2

        # Quintic Wendland kernel
        return (1.0 + 2.0 * q) * (1.0 - 0.5 * q)**4
