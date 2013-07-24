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
from bge import texture
from bge import types
from mathutils import *
from math import *
import bgl

# OPTIONS

# Offset = The distance to the water plane
# where the objects will be considered inside
# the water. Edit this value depending on your
# problem scale.
offset = 0.1

# Reflection map quality. If a texture has not already
# generated in your water plane, this method will
# generate one for you, with this resolution. Higher
# resolution will imply more complex scene, take care.
size   = [512,512]

def perform(waterPlane,viewerCam,waterCam):
    """ Performs the reflection and refraction textures
    @param waterPlane Water plane game object
    @param viewerCam Active camera
    @param waterCam Auxiliar camera used by water.
    """
    # REFLECTION
    
    # Reflect the camera respect to the water plane
    waterCam.lens = viewerCam.lens
    waterCam.projection_matrix = viewerCam.projection_matrix
    waterCam.position = viewerCam.position
    camToMirror = waterPlane.position - viewerCam.position
    waterCam.position[2] += 2.0*camToMirror[2]
    orientation = Matrix(viewerCam.orientation)
    orientation.transpose()
    orientation = orientation*Matrix.Rotation(radians(180),3,'Y')*Matrix.Scale(-1,3,Vector([1,0,0]))
    orientation.transpose()
    waterCam.orientation = orientation
    
    # Hide the water surface
    waterPlane.visible = False
    
    # Render the reflected scene
    bgl.glCullFace(bgl.GL_FRONT)
    clip = -1
    if viewerCam.position[2] < 0.0:
        clip = 1
    buffer = bgl.Buffer(bgl.GL_DOUBLE, [4], [0.0, 0.0, clip, waterPlane.position[2]+offset])
    bgl.glClipPlane(bgl.GL_CLIP_PLANE0,buffer)
    bgl.glEnable(bgl.GL_CLIP_PLANE0)
    g.reflection.refresh(True)
    
    # Restore
    bgl.glCullFace(bgl.GL_BACK)
    bgl.glDisable(bgl.GL_CLIP_PLANE0)
    # waterPlane.visible = True
    
    # REFRACTION
    
    # Reflect the camera respect to the water plane
    waterCam.lens = viewerCam.lens
    waterCam.projection_matrix = viewerCam.projection_matrix
    waterCam.position = viewerCam.position
    waterCam.orientation  = Matrix(viewerCam.orientation)
    
    # Hide the water surface
    # waterPlane.visible = False
    
    # Render the reflected scene
    clip = 1
    if viewerCam.position[2] < 0.0:
        clip = -1
    buffer = bgl.Buffer(bgl.GL_DOUBLE, [4], [0.0, 0.0, clip, waterPlane.position[2]+offset])
    bgl.glClipPlane(bgl.GL_CLIP_PLANE1,buffer)
    bgl.glEnable(bgl.GL_CLIP_PLANE1)
    g.refraction.refresh(True)
    
    # Restore
    bgl.glDisable(bgl.GL_CLIP_PLANE1)
    waterPlane.visible = True


# GET ENTITIES

# Get the selected water plane (we don't
# use the owner in order to allow other
# enbtities to call this script)
controller = g.getCurrentController()
# waterPlane = controller.owner
scene      = g.getCurrentScene()
objects    = scene.objects
waterPlane = objects.get('waterPlane')
if not waterPlane:
    raise Exception("Can't find the object 'waterPlane'")

# Get the active camera
viewerCam = scene.active_camera

# Get the water reflections camera
waterCam  = objects.get('waterCamera')
if not waterCam:
    raise Exception("Can't find the camera 'waterCamera'")

# Get the textures, or generate it
if not waterPlane['textures']:
    # Sometimes the image must be reduced in size
    sizeBackup = size[:]
    validTexture        = False
    while not validTexture:
        g.reflection        = texture.Texture(waterPlane, 0, 0)
        g.reflection.source = texture.ImageRender(scene,waterCam)
        g.reflection.source.capsize    = [size[0],size[1]]
        g.reflection.source.background = [32,128,128,0]
        bufout = texture.imageToArray(g.reflection.source)
        if(len(bufout)//size[0]//size[1] != 4):
            print("Warning: Reflection texture size {0}x{1} not supported, will be reduced".format(size[0],size[1]))
            size[0] = size[0] // 2
            size[1] = size[1] // 2
            continue
        validTexture = True
    print("Info: Reflection texture size = {0}x{1}".format(size[0],size[1]))
    size = sizeBackup[:]
    validTexture        = False
    while not validTexture:
        g.refraction        = texture.Texture(waterPlane, 0, 1)
        g.refraction.source = texture.ImageRender(scene,waterCam)
        g.refraction.source.capsize    = [size[0],size[1]]
        g.refraction.source.background = [0,0,0,0]
        bufout = texture.imageToArray(g.reflection.source)
        if(len(bufout)//size[0]//size[1] != 4):
            print("Warning: Refraction texture size {0}x{1} not supported, will be reduced".format(size[0],size[1]))
            size[0] = size[0] // 2
            size[1] = size[1] // 2
            continue
        validTexture = True
    print("Info: Refraction texture size = {0}x{1}".format(size[0],size[1]))
    waterPlane['textures'] = True

# Perform the work
perform(waterPlane,viewerCam,waterCam)

# The timer for the shader (we don't need emit)
waterPlane.color.w = waterPlane["timer"]