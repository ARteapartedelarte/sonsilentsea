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


class sssBullet(sssDynamic):
    def __init__(self, obj):
        super(sssBullet, self).__init__(obj)
        self.collisionCallbacks.append(self.explode)

    def update(self):
        super(sssBullet, self).update()
        if self.worldPosition.z < 0.0:
            self.worldPosition.z = 0.0
            self.underwater_explode()

    def explode(self, obj):
        """ Perform the explosion against an object
        @param obj Collider object
        """
        shell = self['shell']

        # Send damages to the remote object
        try:
            obj.recv_explosion(shell, obj=self)
        except:
            pass

        self.endObject()

        if self['explosion'] == '':
            return
        orig = self.worldPosition - 5.0*self.getAxisVect(Vector((1,0,0)))
        dest = self.worldPosition + 5.0*self.getAxisVect(Vector((1,0,0)))
        hit, pos, dir = self.rayCast(dest, orig, 0, "", 1)
        if hit == None:
            dir = -self.getAxisVect(Vector((1,0,0)))
            pos = self.worldPosition - 4.0*dir
        scene = g.getCurrentScene()
        emitter = scene.addObject(self['explosion'], self)
        emitter.worldPosition = pos + 1.0*dir
        """
        emitter.worldPosition = self.worldPosition + \
            5.0*self.getAxisVect(Vector((1,0,0))) - \
            1.0*dir
        """
        emitter.alignAxisToVect(dir)

        r = 0.4 * sqrt(0.5 * shell)
        emitter.worldScale = Vector((r, r, r))
        for child in emitter.children:
            try:
                child['velocity'] *= r
                child['velocity_var'] *= r
            except:
                continue

    def underwater_explode(self):
        """ Perform the underwater explosion
        """
        self.endObject()

        if self['water'] == '':
            return

        scene = g.getCurrentScene()
        shell = self['shell']
        emitter = scene.addObject(self['water'], self)

        r = 0.4*sqrt(0.5*shell)
        emitter.worldPosition.z = 0.0
        emitter.worldScale = Vector((r, r, r))
        for child in emitter.children:
            try:
                child['velocity'] *= r
                child['velocity_var'] *= r
            except:
                continue
