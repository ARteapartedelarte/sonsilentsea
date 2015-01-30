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


MISSION_POINT = 0
MISSION_DESTROY = 1


class sssAI(bge.types.KX_GameObject):
    def __init__(self, obj):
        # Get the instance to control
        self.top_parent = self.topParent()
        self.__ship = self.lookForShipChild()
        self.__mission = None

    def typeName(self):
        return 'sssAI'

    def update(self):
        if self.__ship is None:
            self.__ship = self.lookForShipChild()
        if self.__ship is None:
            return
        self.tryToAccomplishMission()

    @property
    def ship(self):
        return self.__ship

    @ship.setter
    def ship(self, value):
        raise AttributeError('ship is a read only attribute')

    def topParent(self, obj=None):
        if obj is None:
            obj = self
        if obj.parent is None:
            return obj
        return self.topParent(obj.parent)

    def lookForShipChild(self, obj=None):
        if obj is None:
            obj = self.top_parent
        try:
            if obj.typeName() == 'sssShip':
                    return obj
        except:
            pass
        children = obj.children
        for c in children:
            try:
                if c.typeName() == 'sssShip':
                    return c
            except:
                pass
            inst = self.lookForShipChild(c)
            if inst is None:
                continue
            return inst
        return None

    def guns(self, obj=None):
        if obj is None:
            obj = self.ship
        guns = []
        children = obj.children
        for c in children:
            try:
                if c.typeName() == 'sssGun':
                    guns.append(c)
            except:
                pass
            guns.extend(self.guns(c))
        return guns

    @property
    def mission(self):
        return self.__mission

    @mission.setter
    def mission(self, value):
        raise AttributeError('mission is a read only attribute')

    def assignMission(self, mission):
        self.__mission = mission

    def tryToAccomplishMission(self):
        if self.__mission == None:
            return
        if self.__mission['type'] == MISSION_POINT:
            self.ship.goTo((self.__mission['objective'], 2))
        elif self.__mission['type'] == MISSION_DESTROY:
            obj = self.__mission['objective']
            if obj not in self.__ship.contacts.keys():
                return
            # Look for a convenient shoting range
            dist = None
            guns = self.guns()
            if guns:
                dist = 0.7 * guns[0].fireRange()
                for gun in guns[1:]:
                    dist = min(dist, 0.7 * gun.fireRange())
            if dist is None:
                return
            mission_dir = obj.worldPosition.xy - self.worldPosition.xy
            mission_dist = mission_dir.length

            if mission_dist > dist:
                # If we are not in range, run against the objective
                # It is preferible to run directly against him trying to get the
                # stern, where they are more vulnerable
                self.ship.goTo((obj.worldPosition.xy, 3), tol=0.0)
            else:
                # Orientate the ship to give maximum damage
                obj_dir = obj.getAxisVect(Vector((1.0, 0.0, 0.0))).xy
                ship_dir = self.ship.getAxisVect(Vector((1.0, 0.0, 0.0))).xy
                orientation_dir = Vector((-mission_dir.y,
                                          mission_dir.x)).normalized()
                if orientation_dir.dot(obj_dir) < 0.0:
                    orientation_dir = -orientation_dir
                cos_angle = orientation_dir.dot(ship_dir)
                self.ship.orientate(orientation_dir,
                                    int(3.0 * (1.0 - cos_angle) + 0.5))

            self.ship.gunTarget(obj.name)