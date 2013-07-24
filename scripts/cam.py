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

import bge
from bge import logic as g
from mathutils import *
from math import *

# Maximum and minimum heights (only in
# the z direction) of the camera
camZ      = [55.0, 1000.0]

# Maximum and minimum distance to
# the objects
objZ      = [-100.0, 45.0]

def mousePos():
    """ Return the mouse position in pixels
    @note [0,0] for the upper-left corner.
    @note The mouse can be out of the screen, returning values out of [0,1] range.
    @return The mouse position.
    """
    x = bge.render.getWindowWidth()*mouse.position[0]
    y = bge.render.getWindowWidth()*mouse.position[1]
    return (x, y)

def setNearFar(cam):
    """ Set the clipping range depending on the
    camera position, in order to fit to the scene.
    @param cam Active camera
    """
    # Get the actual position of the camera, and
    # the main focal direction
    pos = cam.worldPosition
    vec = cam.getScreenVect(0.5,0.5)
    mat = cam.projection_matrix
    if vec.z > 0.0:
        vec = -vec
    
    # Get the field of view at near distance
    htg  = 1.0 / mat[0][0]
    vtg  = 1.0 / mat[1][1]
    
    # Create the vector for the lower point
    # of the screen
    rot = Matrix.Rotation( 0.25*pi,3,'Z') * \
          Matrix.Rotation(-atan(vtg),3,'X') * \
          Matrix.Rotation(-0.25*pi,3,'Z')
    dir = rot*vec
    # And compute near field
    dir *= (pos[2] - objZ[1])/abs(dir.z)
    cam.near = dir.dot(vec)
    if(cam.near <= 0.0):
        cam.near = 0.1
    
    # Create the vector for the upper-left point
    # of the screen
    rot = Matrix.Rotation( atan(htg),3,'Z') * \
          Matrix.Rotation( 0.25*pi,3,'Z') * \
          Matrix.Rotation( atan(vtg),3,'X') * \
          Matrix.Rotation(-0.25*pi,3,'Z')
    dir = rot*vec
    # And compute near field
    dir *= (pos[2] - objZ[0])/abs(dir.z)
    cam.far = dir.dot(vec)

def setWaterPlane(cam,water):
    """ Scale and move the water plane to
    the best fit for the camera.
    @param cam Active camera.
    @param water Water plane
    """
    # Get the actual position of the camera
    # and the water plane
    c_pos = cam.worldPosition
    w_pos = water.worldPosition
    vec = cam.getScreenVect(0.5,0.5)
    mat = cam.projection_matrix
    if vec.z > 0.0:
        vec = -vec

    # Get the field of view at near distance
    htg  = 1.0 / mat[0][0]
    vtg  = 1.0 / mat[1][1]
    
    # Get the vertical limits of the water plane
    vLims = []
    for v in (-1.0,1.0):
        rot = Matrix.Rotation( 0.25*pi,3,'Z') * \
              Matrix.Rotation(v*atan(vtg),3,'X') * \
              Matrix.Rotation(-0.25*pi,3,'Z')
        dir = rot*vec
        # And compute near field
        dir *= (c_pos[2] - w_pos[2])/abs(dir.z)
        vLims.append(c_pos + dir)

    # Compute the center for the plane
    center = 0.5*(vLims[0]+vLims[1])
    water.worldPosition = center

    # Compute the required dimensions
    vDim2 = (vLims[1]-center).length_squared
    hDim2 = (c_pos-center).length_squared * htg*htg
    Dim   = sqrt(hDim2 + vDim2)
    water.worldScale = Vector((Dim, Dim, Dim))

def zoom(sign):
    """ Moves the camera in/out from the water plane
    @param sign 1.0 to move in, -1.0 otherwise.
    """
    # Sensivity (meters per wheel action)
    sensivity = 10.0
    
    # Get the actual position and the moving
    # direction
    pos = cam.worldPosition
    dir = cam.getScreenVect(0.5,0.5)
    if dir.z > 0.0:
        dir = -dir

    # Test if the camera is at the minimum distance
    if (sign > 0.0) and (pos.z <= camZ[0]):
        return
    if (sign < 0.0) and (pos.z >= camZ[1]):
        return

    # Move the camera
    cam.worldPosition = pos + sign*sensivity*dir

    # Compute the new clipping
    setNearFar(cam)

    # Fit the water plane to the viewable region
    setWaterPlane(cam,water)

def zoomIn():
    """ Performs an in zoom.
    """
    zoom(1.0)

def zoomOut():
    """ Performs an out zoom.
    """
    zoom(-1.0)

def update():
    """ This method updates the camera, including
    the position if movements are required.
    @remarks Call this method every frame.
    """
    if not cam['midPress']:
        # The button was not pressed, we must
        # Store the coordinates
        cam['midU'] = mouse.position[0]
        cam['midV'] = mouse.position[1]
        arrows.visible = False
        return

    arrows.visible = True
    # The sensitivity must depends on the cam heigh
    sensivity = cam.worldPosition.z/20.0

    # Mid button is pressed, compute the
    # displacement cuantity
    du = mouse.position[0] - cam['midU']
    dv = mouse.position[1] - cam['midV']
    uVec = Vector(( 0.707106781, 0.707106781,0.0))
    vVec = Vector(( 0.707106781,-0.707106781,0.0))
    dir  = du*uVec + dv*vVec
    # Move the camera and the water
    cam.worldPosition   += sensivity*dir
    water.worldPosition += sensivity*dir

# Get the camera
controller = g.getCurrentController()
cam        = controller.owner

# Get the other related objects
mouse   = g.mouse
scene   = g.getCurrentScene()
objlist = scene.objects
water   = objlist.get('waterPlane')
if not water:
    raise Exception("Can't find the object 'waterPlane'")
waterCam = objlist.get('waterCamera')
if not waterCam:
    raise Exception("Can't find the camera 'waterCamera'")
arrows = objlist.get('dispArrows')
if not arrows:
    raise Exception("Can't find the object 'dispArrows'")
