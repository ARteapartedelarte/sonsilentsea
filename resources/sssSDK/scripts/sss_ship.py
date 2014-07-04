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
from sss_floating import sssFloating


WAYPOINT_TOLERANCE = 150.0
WAYPOINT_ROT_PID = (3 * 12 / pi,   # Maximum rotation for 15 degrees or higher
                    0.0,           # Integral control is disabled
                    3 * 180 / pi)  # Try to limit the rotation to 1 degrees/s


class sssShip(sssFloating):
    def __init__(self, obj):
        sssFloating.__init__(self, obj)
        self._march = None
        self._wheel = None
        self._waypoint = None
        self.getSubSystems()

    def typeName(self):
        return 'sssShip'

    def getSubSystems(self):
        children = self.children
        self._propellers = []
        self._rudders = []
        self._guns = []
        for c in children:
            try:
                if c.typeName() == 'sssPropeller':
                    self._subsystems = True
                    self._propellers.append(c)
                elif c.typeName() == 'sssRudder':
                    self._subsystems = True
                    self._rudders.append(c)
                elif c.typeName() == 'sssGun':
                    self._subsystems = True
                    self._guns.append(c)
                elif c.typeName() == 'sssTurret':
                    self._subsystems = True
                    for cc in c.children:
                        if cc.typeName() == 'sssGun':
                            self._guns.append(cc)
            except:
                continue

    def getMarch(self):
        return self._march

    def march(self, m):
        self._march = None
        for p in self._propellers:
            if p['HP'] <= 0.0:
                continue
            p['march'] = int(m)
            self._march = int(m)
            self._waypoint = None
        return self._march

    def getWheel(self):
        return self._wheel

    def wheel(self, w):
        self._wheel = None
        for r in self._rudders:
            if r['HP'] <= 0.0:
                continue
            r['rudder'] = int(w)
            self._wheel = int(w)
            self._waypoint = None
        return self._wheel

    def getWaypoint(self):
        return self._wheel

    def waypoint(self, w, m):
        ''' Set a way point.
        w: Point to reach, of type Vector (the z coordinate will be discarded)
        m: March used to do it
        '''
        self._waypoint = None
        can_do_it = False
        for p in self._propellers:
            if p['HP'] <= 0.0:
                continue
            can_do_it = True
        if not can_do_it:
            return None
        can_do_it = False
        for r in self._rudders:
            if r['HP'] <= 0.0:
                continue
            can_do_it = True
        if not can_do_it:
            return None
        self._march = None
        self._wheel = None
        self._waypoint = (w.xy, int(m))
        return self._waypoint

    def update(self):
        # Update the subsystems list, some subsystems could be not mutated
        # yet, or eventually added/removed
        self.getSubSystems()

        sssFloating.update(self)
        if self['HP'] <= 0.0:
            return
        if self._march is not None:
            for p in self._propellers:
                p['march'] = self._march
        if self._wheel is not None:
            for r in self._rudders:
                r['rudder'] = self._wheel            
        if self._waypoint is not None:
            self.goTo(self._waypoint)

    def goTo(self, w):
        aim = w[0]
        vel = w[1]
        if not vel:
            self._waypoint = None
        # Lets see if we have arrived the point
        vec = (aim - self.worldPosition.xy)
        dist_squared = vec.length_squared
        if dist_squared < WAYPOINT_TOLERANCE**2:
            self.march(0)
            self.wheel(0)
            return
        # Start moving
        for p in self._propellers:
            if p['HP'] <= 0.0:
                continue
            p['march'] = vel
        # Get the required yaw rotation
        vec = vec.normalized()
        aim_yaw = atan2(vec.y, vec.x)
        vec = self.getAxisVect(Vector((1.0, 0.0, 0.0))).xy.normalized()
        if vel < 0:
            vec = -vec
        yaw = atan2(vec.y, vec.x)
        dyaw = aim_yaw - yaw
        if dyaw < -pi:
            dyaw += 2.0 * pi
        if dyaw > pi:
            dyaw -= 2.0 * pi
        # Get the actual rotation velocity
        dyawdt = self.getAngularVelocity().z
        # Ask to move the rudders
        w = int(round(WAYPOINT_ROT_PID[0] * dyaw - WAYPOINT_ROT_PID[2] * dyawdt))
        for r in self._rudders:
            if r['HP'] <= 0.0:
                continue
            r['rudder'] = w
