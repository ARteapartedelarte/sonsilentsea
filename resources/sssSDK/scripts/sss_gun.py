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
from sss_dynamic_loader import sssDynamicLoader


ERROR_RADIUS = 200.0


class sssGun(sssDynamic, sssDestroyable, sssDynamicLoader):
    def __init__(self, obj):
        sssDynamic.__init__(self, obj)
        sssDestroyable.__init__(self, obj)
        sssDynamicLoader.__init__(self, obj)
        self.min_pitch = radians(self['min_pitch'])
        self.max_pitch = radians(self['max_pitch'])
        self.vel_pitch = radians(self['vel_pitch'])
        self.aim = None
        self.aiming = False
        self.reloading = 0.0
        self.sounds = []
        for act in self.actuators:
            if type(act) == type(bge.types.KX_SoundActuator):
                self.sounds.append(act)

    def typeName():
        return 'sssGun'

    def isAimed(self, point=None, threshold=ERROR_RADIUS):
        if point is None:
            point = self.aim
        grav = abs(g.getCurrentScene().gravity.z)
        vec = self.getAxisVect(Vector((1.0, 0.0, 0.0)))
        vel = vec * self['bullet_vel']
        pos = self.worldPosition
        # Compute the flighting time
        # z = 0 = z_0 + v_0 t - 1/2 g t^2 
        t = (vel.z + sqrt(vel.z**2 + 2.0 * grav * pos.z)) / grav
        # Compute the impact point
        # x = x_0 + v_0 t
        p = pos.xy + vel.xy * t
        err = p - point.xy
        if err.dot(err) > ERROR_RADIUS**2:
            return False
        return True

    def aimTo(self, point, shoot=True):
        if self.reloading > 0.0:
            return
        if shoot:
            if not self.isAimed(point):
                self.aim = point.xy
                self.aiming = True
                try:
                    self.parent.aimTo(point)
                except:
                    pass
                return
            self.fire()
        else:
            self.aim = point.xy
            self.aiming = True
            try:
                self.parent.aimTo(point)
            except:
                pass

    def fire(self):
        if self.reloading > 0.0:
            return
        self.reloading = self['reload_time']
        scene = g.getCurrentScene()

        # Play sounds
        for s in self.sounds:
            s.startSound()

        # Create the smoke object
        if self['smoke_obj'] != '':
            smoke = scene.addObject(self['smoke_obj'], self)

        # Create the bullet object
        if self['bullet_obj'] != '':
            bullet = scene.addObject(self['bullet_obj'], self)
            vec = self.getAxisVect(Vector((1.0, 0.0, 0.0)))
            bullet.worldPosition += vec * 32.0
            bullet.setLinearVelocity(vec * self['bullet_vel'])

    def getDPitch(self):
        if self.aim is None:
            return 0.0
        grav = abs(g.getCurrentScene().gravity.z)
        vec = self.aim - self.worldPosition.xy
        dist = vec.length
        # Compute the aiming pitch angle. For the pitch angle
        # it will be suposed that the gun is in the water
        # level (z=0), which should imply an error that is
        # several times smaller than the ships motion induced
        # ones.
        arg = grav * dist / (self['bullet_vel']**2)
        if arg < -1.0:
            aim_pitch = self.min_pitch
        elif arg > 1.0:
            aimPitch = self.max_pitch
        else:
            aim_pitch = 0.5 * asin(arg)
            aim_pitch = max(self.min_pitch, aim_pitch)
            aim_pitch = min(self.max_pitch, aim_pitch)
        # Compute the error
        aim_pitch = -aim_pitch # Pitch angles are negative
        pitch = self.localOrientation.to_euler().y
        return aim_pitch - pitch

    def update(self):
        sssDynamic.update(self)
        sssDestroyable.update(self)
        sssDynamicLoader.update(self)
        dt = 1.0 / g.getLogicTicRate()
        if self.reloading > 0.0:
            self.reloading -= dt
            return
        else:
            self.reloading = 0.0
        if not self.aiming:
            return

        dpitch = self.getDPitch()
        max_rot = dt * self.vel_pitch
        if abs(dpitch) > max_rot:
            dpitch = copysign(max_rot, dpitch)
        else:
            parent_aimed = True
            try:
                if self.parent.aim is not None:
                    parent_aimed = False
            except:
                pass
            if parent_aimed:
                self.aiming = False

        self.applyRotation(Vector((0.0, dpitch, 0.0)), True)
