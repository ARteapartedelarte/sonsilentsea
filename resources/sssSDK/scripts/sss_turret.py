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
from sss_dynamic import sssDynamic
from sss_destroyable import sssDestroyable


class sssTurret(sssDynamic, sssDestroyable):
    def __init__(self, obj):
        sssDynamic.__init__(self, obj)
        sssDestroyable.__init__(self, obj)
        self.min_yaw = radians(self['min_angle'])
        self.max_yaw = radians(self['max_angle'])
        self.vel_yaw = radians(self['vel_angle'])
        self.yaw0 = self.localOrientation.to_euler().z
        self.aim = None

    def typeName(self):
        return 'sssTurret'

    def aimTo(self, point):
        self.aim = point.xy

    def getDYaw(self):
        if self.aim is None:
            return 0.0
        vec = self.aim - self.worldPosition.xy
        vec = vec.normalized()
        aim_yaw = atan2(vec.y, vec.x)
        vec = self.getAxisVect(Vector((1.0, 0.0, 0.0))).xy
        vec = vec.xy.normalized()
        yaw = atan2(vec.y, vec.x)
        return aim_yaw - yaw

    def update(self):
        sssDynamic.update(self)
        sssDestroyable.update(self)
        if self.aim is None:
            return

        dyaw = self.getDYaw()
        yaw = self.localOrientation.to_euler().z - self.yaw0
        # Get the sortest way
        if yaw < -pi:
            yaw += 2.0 * pi
        if yaw > pi:
            yaw -= 2.0 * pi
        if dyaw < -pi:
            dyaw += 2.0 * pi
        if dyaw > pi:
            dyaw -= 2.0 * pi

        # Test if we are trying to pass through the forbidden zone
        # In that case we must change the rotation direction
        if yaw + dyaw > self.max_yaw:
            dyaw -= 2.0 * pi
        if yaw + dyaw < self.min_yaw:
            dyaw += 2.0 * pi

        # Test if we are trying to aim out of the bounds
        if yaw + dyaw > self.max_yaw or yaw + dyaw < self.min_yaw:
            return

        dt = 1.0 / g.getLogicTicRate()
        max_rot = dt * self.vel_yaw
        if abs(dyaw) > max_rot:
            dyaw = copysign(max_rot, dyaw)
        else:
            # We will be already aimed at the end of this iteration
            self.aim = None

        self.applyRotation(Vector((0.0, 0.0, dyaw)), True)
