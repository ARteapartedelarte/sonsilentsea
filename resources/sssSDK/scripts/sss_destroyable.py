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


class sssDestroyable():
    def __init__(self, obj):
        self.added_mass = 0.0
        self.collisionCallbacks.append(self.recv_collision)

    def update(self):
        if self['HP'] < 0.0:
            self.added_mass += -self['HP']

    def recv_collision(self, obj):
        """Detect and parse a collision with other object.
        """
        # Test that the object is not related with you
        if obj == self.parent or obj in self.children:
            return

        # Try to compute the effect from the self object
        try:
            p1 = self.getLinearMomentum(True)
            p0 = self.getLinearMomentum(False)
            p = abs(p1 - p0)
        except:
            # Try to compute the effect from the collider
            try:
                p1 = obj.getLinearMomentum(True)
                p0 = obj.getLinearMomentum(False)
                p = abs(p1 - p0)
            except:
                # None one of the objects have info about the collision
                p = 0.0
        # Substract the armour avoided damage
        p /= 1000.0
        p = max(0.0, p - self['AP'])
        # Damage the object
        self['HP'] -= p

    def recv_explosion(self, shell, obj=None):
        """Compute a received explosion.
        If obj is not None, the armour penetrating test will be performed
        """
        if obj is not None:
            p = 0
            try:
                p1 = obj.getLinearMomentum(True)
                p0 = obj.getLinearMomentum(False)
                p = abs(p1 - p0)
            except:
                # None one of the objects have info about the collision
                p = 0.0
            p /= 1000.0
            if p < self['AP']:
                return
        # Damage the object
        self['HP'] -= shell
