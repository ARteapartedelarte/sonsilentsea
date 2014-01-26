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


POINT_ALTERNATIVES = ('CENTER', 'VERTEX', 'MESH')
DIR_ALTERNATIVES = ('Z', 'Y', 'X', 'z', 'y', 'x', 'NORMAL')


def load():
    """Method called one time at the emitter generation"""
    cont = g.getCurrentController()
    obj = cont.owner
    scene = g.getCurrentScene()
    cam = scene.active_camera

    if obj['billboard']:
        obj.worldOrientation = cam.worldOrientation

    if obj['is_scale_fade']:
        obj['scale.x'] = obj.localScale.x
        obj['scale.y'] = obj.localScale.y
        obj['scale.z'] = obj.localScale.z


def lifetime(obj):
    """Test the object lifetime"""
    if not obj['is_lifetime']:
        return
    if obj['t'] >= obj['lifetime']:
        obj.endObject()


def scaleFade(obj):
    """Perform the scale fade if it is required"""
    if not obj['is_scale_fade']:
        return
    t = max(obj['t'] - obj['scale_fade_in'], 0.0)
    T = obj['scale_fade_out'] - obj['scale_fade_in']
    f = t/T
    if f > 1.0:
        f = 1.0
        obj['is_scale_fade'] = False
    s = f * obj['scale_fade'] + (1.0 - f)
    obj.localScale.x = s * obj['scale.x']
    obj.localScale.y = s * obj['scale.y']
    obj.localScale.z = s * obj['scale.z']


def update():
    """Method called each frame while the emitter exist"""
    cont = g.getCurrentController()
    obj = cont.owner
    scene = g.getCurrentScene()
    cam = scene.active_camera

    if obj['billboard']:
        obj.worldOrientation = cam.worldOrientation

    # Fades
    scaleFade(obj)

    # Test if the object must end
    lifetime(obj)

    return
