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
from sss_floating import sssFloating


WAYPOINT_TOLERANCE = 150.0
WAYPOINT_ROT_PID = (3 * 12 / pi,   # Maximum rotation for 15 degrees or higher
                    0.0,           # Integral control is disabled
                    3 * 180 / pi)  # Try to limit the rotation to 1 degrees/s
NEW_CONTACT_VALID_PERIOD = 1.0
MAX_CONTACT_VALID_PERIOD = 3.0


class sssShip(sssFloating):
    def __init__(self, obj):
        sssFloating.__init__(self, obj)
        self._march = None
        self._wheel = None
        self._waypoint = None
        self.getSubSystems()
        self._gun_target = [None] * len(self._guns)
        # List of known contacts and ghosts
        # Contacts are allies/enemies which are perfectly known, i.e. Ship
        # type, position, ...
        # Ghosts are contacts which just an approximation of its position is
        # known, but not if they are allies or enemies, the ship type, ...
        self.__contacts = {}
        self.__ghosts = {}

    def typeName(self):
        return 'sssShip'

    def getChildrenByType(self, type_name, obj=None):
        if obj is None:
            obj = self
        ents = []
        children = obj.children
        for c in children:
            try:
                if c.typeName() == type_name:
                    ents.append(c)
            except:
                pass
            ents.extend(self.getChildrenByType(type_name, c))
        return ents

    def getSubSystems(self):
        self._propellers = self.getChildrenByType('sssPropeller')
        self._rudders = self.getChildrenByType('sssRudder')
        self._guns = self.getChildrenByType('sssGun')
        self._sensors = self.getChildrenByType('sssSensor')

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

    def gunTarget(self, target, guns=None):
        """ Set the target for the guns
        target: Either a position or the name of an entity. The z coordinate
        will be discarded. None to don't assign a target
        guns: The list of guns affected (ids). None to select all.
        """
        if guns is None:
            guns = list(range(len(self._guns)))
        for g in guns:
            try:
                if isinstance(target, str):
                    self._gun_target[g] = target
                else:
                    self._gun_target[g] = None
                    self._guns[g].aimTo(target, True)
            except:
                continue

    def update(self):
        # Update the subsystems list, some subsystems could be not mutated
        # yet, or eventually added/removed
        self.getSubSystems()
        added = len(self._guns) - len(self._gun_target)
        self._gun_target.extend([None] * added)

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
        for i, gun in enumerate(self._guns):
            if self._gun_target[i] is None:
                continue
            self.setGun(gun, self._gun_target[i])
        for s in self._sensors:
            s.update()

        # Update the contacts and ghosts
        dt = 1.0 / g.getLogicTicRate()
        for obj in self.contacts.keys():
            self.contacts[obj]['t'] -= dt
            if self.contacts[obj]['t'] < 0.0:
                self.removeContact(obj)
        for obj in self.ghosts.keys():
            self.ghosts[obj]['t'] -= dt
            if self.ghosts[obj]['t'] < 0.0:
                self.removeGhost(obj)

    def goTo(self, w, tol=WAYPOINT_TOLERANCE):
        aim = w[0]
        vel = w[1]
        if not vel:
            self._waypoint = None
        # Lets see if we have arrived the point
        vec = (aim - self.worldPosition.xy)
        dist_squared = vec.length_squared
        if dist_squared < tol**2:
            self.march(0)
            self.wheel(0)
            return
        # Start moving
        self.orientate(vec, vel)

    def orientate(self, vec, vel):
        vec = vec.xy.normalized()
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
        # Activate propellers
        for p in self._propellers:
            if p['HP'] <= 0.0:
                continue
            p['march'] = vel
        # Ask to move the rudders
        w = int(round(WAYPOINT_ROT_PID[0] * dyaw - WAYPOINT_ROT_PID[2] * dyawdt))
        for r in self._rudders:
            if r['HP'] <= 0.0:
                continue
            r['rudder'] = w

    def setGun(self, gun, target):
        scene = g.getCurrentScene()
        pos = scene.objects[target].worldPosition
        vel = scene.objects[target].getLinearVelocity()
        d = (self.worldPosition.xy - pos.xy).length
        v = gun['bullet_vel']
        t = d / v
        aim = pos + t * vel
        if gun.aiming:
            gun.aimTo(aim, False)
            return
        gun.aimTo(aim, True)

    @property
    def contacts(self):
        return self.__contacts

    @contacts.setter
    def contacts(self, value):
        raise AttributeError('contacts is a read only attribute')

    def addContact(self, obj):
        # First check that it is not an already existing contact
        if obj in self.__contacts.keys():
            # It is a contact, add 1 second of validity
            self.__contacts[obj]['t'] = min(self.__contacts[obj]['t'] + 1.0,
                                            MAX_CONTACT_VALID_PERIOD)
            return
        # It is a new contact
        self.__contacts[obj] = {'t':NEW_CONTACT_VALID_PERIOD}
        
        # Check if it was a Ghost upgradable to contact, in that case we can sum
        # the valid time
        if obj in self.__ghosts.keys():
            t = self.__ghosts[obj]['t']
            self.__contacts[obj]['t'] = min(self.__contacts[obj]['t'] + t,
                                            MAX_CONTACT_VALID_PERIOD)
            # And remove the ghost
            self.removeGhost(self)
        
    def removeContact(self, obj):
        if obj not in self.__contacts.keys():
            return
        del self.__contacts[obj]

    @property
    def ghosts(self):
        return self.__ghosts

    @ghosts.setter
    def ghosts(self, value):
        raise AttributeError('contacts is a read only attribute')

    def addGhost(self, obj, max_error=100.0):
        # Check if it is an already existing contact. Contact is more elevated
        # than Ghost, so in this case we are increasing the contact validity
        # period.
        # It can be used, for instance, when you are submerged and only ghosts
        # can be received from the sonar, but you can have them already
        # identified.
        if obj in self.__contacts.keys():
            # It is a contact, add 1 second of validity
            self.__contacts[obj]['t'] = min(self.__contacts[obj]['t'] + 1.0,
                                            MAX_CONTACT_VALID_PERIOD)
            return
        # Otherwise check if it is an already existing ghost in order to
        # increment validity period, or ventually to reduce position error
        if obj in self.__ghosts.keys():
            # It is a contact, add 1 second of validity
            self.__ghosts[obj]['t'] = min(self.__ghosts[obj]['t'] + 1.0,
                                            MAX_CONTACT_VALID_PERIOD)
            if self.__ghosts[obj]['error'] > max_error:
                self.__ghosts[obj]['error'] = random.uniform(0.0, max_error)
            return
        # It is a new ghost
        error_dir = Vector((1.0, 0.0, 0.0))
        eul = mathutils.Euler((0.0, 0.0, random.uniform(0.0, 2.0 * pi)), 'XYZ')
        error_dir.rotate(eul)
        self.__ghosts[obj] = {'t':NEW_CONTACT_VALID_PERIOD,
                              'error_dir':error_dir,
                              'error':random.uniform(0.0, max_error)}

    def removeGhost(self, obj):
        if obj not in self.__ghosts.keys():
            return
        del self.__ghosts[obj]