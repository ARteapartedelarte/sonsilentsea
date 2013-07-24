#    Copyright (c) 2013, 2014
#    Jose Luis Cercos-Pita <jlcercos@gmail.com>
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from bge import logic as g
from mathutils import *
from math import *

# Maximum and minimum distance to
# the objects
objZ      = [-100.0, 45.0]

def setLight(cam,water,light,r,t,p):
    """ Set the light depending on the
    camera position, and the desired
    position of the light.
    @param cam Active camera
    @param water Water plane
    @param light Sun light
    @param r distance to the sun
    @param t theta angle in radians
    @param p phi angle in radians
    """
    # Compute the camera center of view
    c_pos = cam.worldPosition
    w_pos = water.worldPosition
    vec   = cam.getScreenVect(0.5,0.5)
    mat   = cam.projection_matrix
    if vec.z > 0.0:
        vec = -vec

    # Compute the new light position and orientation
    dir   = Vector((r*sin(t)*cos(p),
                   r*sin(t)*sin(p),
                   r*cos(t)))
    light.worldPosition    = w_pos + dir
    eul = Euler((0.0, t, p), 'XYZ')
    light.worldOrientation = eul

def update():
    controller = g.getCurrentController()
    light      = controller.owner
    scene      = g.getCurrentScene()
    objlist    = scene.objects
    water      = objlist.get('waterPlane')
    if not water:
        raise Exception("Can't find the object 'waterPlane'")
    cam        = objlist.get('Camera')
    if not cam:
        raise Exception("Can't find the object 'Camera'")
    r = light['r']
    t = radians(light['theta'])
    p = radians(light['phi'])
    setLight(cam, water, light, r,t,p)