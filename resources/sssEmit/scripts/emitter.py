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
    obj['t'] = 0.0  # Emitter lifetime
    obj['count'] = 0  # Number of particles emitted
    return


def getVertexes(obj):
    """Get the vertexes of an object"""
    vertexes = []
    for mesh in obj.meshes:
        for m_index in range(len(mesh.materials)):
            for v_index in range(mesh.getVertexArrayLength(m_index)):
                vertex = mesh.getVertex(m_index, v_index)
                vertexes.append(vertex)
    return vertexes


def meshVertex(obj):
    """Select the emission point and the normal in the vertex mode"""
    v = getVertexes(obj)
    if not v:
        obj['point'] = POINT_ALTERNATIVES[0]
        raise ValueError(
            'Vertex emmision mode selected, but no vertexes found in the'
            ' object (the emission point will be moved to the center)')
    
    i = random.randrange(len(v))
    p = mathutils.Vector(v[i].XYZ)
    n = mathutils.Vector(v[i].normal)

    return p, n


def getPolygons(obj):
    """Get the polygons of an object"""
    polygons = []
    for mesh in obj.meshes:
        for p_index in range(mesh.numPolygons):
            polygon = mesh.getPolygon(p_index)
            polygons.append(polygon)
    return polygons


def meshPoint(obj):
    """Select the emission point and the normal"""
    p = getPolygons(obj)
    if not p:
        obj['point'] = POINT_ALTERNATIVES[0]
        raise ValueError(
            'Polygon emmision mode selected, but no polygons found in the'
            ' object (the emission point will be moved to the center)')

    # Select a random polygon
    p = p[random.randrange(len(p))]

    # Get the vertexes
    m = p.getMesh()
    v = []
    for i in range(p.getNumVertex()):
        m_index = p.getMaterialIndex()
        v_index = p.getVertexIndex(i)
        v.append(m.getVertex(m_index, v_index))

    # Give random weights to the vertexes (normalized)
    norm = 1.0
    weights = []
    for i in range(len(v)):
        weights.append(random.uniform(0.0, norm))
        norm -= weights[-1]
    weights[-1] += norm
    random.shuffle(weights)

    # Compute the averaged value
    p = mathutils.Vector((0.0, 0.0, 0.0))
    n = mathutils.Vector((0.0, 0.0, 0.0))
    for i in range(len(v)):
        p += weights[i]*mathutils.Vector(v[i].XYZ)
        n += weights[i]*mathutils.Vector(v[i].normal)

    return p, n


def point(obj):
    """Select the emission point and the normal"""
    if obj['point'] not in POINT_ALTERNATIVES:
        obj['point'] = POINT_ALTERNATIVES[0]

    if obj['point'] == POINT_ALTERNATIVES[0]:
        return obj.worldPosition, mathutils.Vector((0.0, 0.0, 0.0))

    elif obj['point'] == POINT_ALTERNATIVES[1]:
        return meshVertex(obj)

    return meshPoint(obj)


def velocity(obj, n):
    """Select the initial particle velocity"""
    if obj['direction'] not in DIR_ALTERNATIVES:
        obj['direction'] = DIR_ALTERNATIVES[3]

    vel = mathutils.Vector((0.0, 0.0, 0.0))
    if obj['direction'] == DIR_ALTERNATIVES[0]:
        vel = mathutils.Vector((0.0, 0.0, 1.0))
    elif obj['direction'] == DIR_ALTERNATIVES[1]:
        vel = mathutils.Vector((0.0, 1.0, 0.0))
    elif obj['direction'] == DIR_ALTERNATIVES[2]:
        vel = mathutils.Vector((1.0, 0.0, 0.0))
    if obj['direction'] == DIR_ALTERNATIVES[3]:
        vel = obj.getAxisVect(mathutils.Vector((0.0, 0.0, 1.0)))
    elif obj['direction'] == DIR_ALTERNATIVES[4]:
        vel = obj.getAxisVect(mathutils.Vector((0.0, 1.0, 0.0)))
    elif obj['direction'] == DIR_ALTERNATIVES[5]:
        vel = obj.getAxisVect(mathutils.Vector((1.0, 0.0, 0.0)))
    elif obj['direction'] == DIR_ALTERNATIVES[6]:
        vel = n

    norm = obj['velocity'] + random.uniform(-obj['velocity_var'],
                                            obj['velocity_var'])

    return norm*vel


def initialValues(obj):
    """Compute the initial values for the particle"""
    p, n = point(obj)
    v = velocity(obj, n)
    return p, v


def generateParticle(obj):
    """Generate a particle from the emitter"""
    scene = g.getCurrentScene()
    part = scene.addObject(obj['particle'], obj, 0)

    p, v = initialValues(obj)
    part.worldPosition = p
    part.setLinearVelocity(v)

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
