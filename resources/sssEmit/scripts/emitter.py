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
import mathutils
import math
import random


def load():
    """Method called one time at the emitter generation"""
    cont = g.getCurrentController()
    obj = cont.owner
    obj['t'] = 0.0  # Emitter lifetime
    obj['count'] = 0  # Number of particles emitted
    return


def generateParticle(obj):
    """Generate a particle from the emitter"""
    obj['count'] += 1
    return


def lifetime(obj):
    """Test the object lifetime"""
    if not obj['is_lifetime']:
        return
    if obj['t'] >= obj['lifetime']:
        obj.endObject()


def update():
    """Method called each frame while the emitter exist"""
    cont = g.getCurrentController()
    obj = cont.owner
    scene = bge.logic.getCurrentScene()
    cam = scene.active_camera

    # Targeted number of particles and remaining ones to achieve it
    dt = 1.0/g.getLogicTicRate()
    obj['t'] += dt
    target = int(obj['t']*obj['rate'])
    n = target - obj['count']

    while(obj['count'] < n):
        generateParticle(obj)

    # Test if the object must end
    lifetime(obj)

    return
