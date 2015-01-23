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

import bpy
from os import path
import math
from sssSDK.utils import *
import sssSDK.objects.dynamic as dynamic
import sssSDK.objects.destroyable as destroyable


# Module data
NAME = 'Turret'
DESCRIPION = 'Turret. The Turret will rotate around the Z axis.'
SELECTABLE = True
CLASS_NAME = 'sssTurret'
SCRIPT_NAME = 'sss_turret'


def generateProperties():
    """Ensure that the object has the required properties."""
    obj = bpy.context.object
    addProperty('min_angle', 'FLOAT', -360.0)
    addProperty('max_angle', 'FLOAT', 360.0)
    addProperty('vel_angle', 'FLOAT', 5.0)


def updateValues():
    """Update the particles emitter values."""
    dynamic.updateValues()
    destroyable.updateValues()
    generateProperties()
    loadScript()

    obj = bpy.context.object
    obj.game.properties['min_angle'].value = obj.sss_turret_min_angle
    obj.game.properties['max_angle'].value = obj.sss_turret_max_angle
    obj.game.properties['vel_angle'].value = obj.sss_turret_vel_angle

def generateObjectProperties(update_callback):
    """Generate the Blender object properties.
    """
    bpy.types.Object.sss_turret_min_angle = bpy.props.FloatProperty(
        default=-360.0,
        min=-360.0,
        max=0.0,
        update=update_callback,
        description='Minimum rotation angle (-360 to no limit)')
    bpy.types.Object.sss_turret_max_angle = bpy.props.FloatProperty(
        default=360.0,
        min=0.0,
        max=360.0,
        update=update_callback,
        description='Maximum rotation angle (360 to no limit)')
    bpy.types.Object.sss_turret_vel_angle = bpy.props.FloatProperty(
        default=5.0,
        min=1.0,
        max=360.0,
        update=update_callback,
        description='Rotation velocity')


def loadScript():
    """Load/update the text script in text editor."""
    filepath = None
    for folder in addonsPaths():
        f = path.join(folder, "sssSDK/scripts/{}.py").format(SCRIPT_NAME)
        if not path.isfile(f):
            continue
        filepath = f
        break
    if not filepath:
        raise Exception(
            'I can not find the script file "{}.py"'.format(SCRIPT_NAME))

    # We can try to update it, and if the operation fails is just because the
    # file has not been loaded yet
    try:
        text = bpy.data.texts['{}.py'.format(SCRIPT_NAME)]
        text.clear()
        f = open(filepath, 'r')
        text.write(f.read())
        f.close()
    except:
        bpy.ops.text.open(filepath=filepath,
                          filter_blender=False,
                          filter_image=False,
                          filter_movie=False,
                          filter_python=True,
                          filter_font=False,
                          filter_sound=False,
                          filter_text=True,
                          filter_btx=False,
                          filter_collada=False,
                          filter_folder=True,
                          filemode=9,
                          internal=True)


def createLogic():
    obj = bpy.context.active_object

    # Add a controller to reference the script (but never used). It is
    # useful if the object will be imported from other blender file,
    # inserting the script in the importer scene
    bpy.ops.logic.controller_add(type='PYTHON',
                                 name="{}.reference".format(SCRIPT_NAME),
                                 object="")
    text = None
    for t in bpy.data.texts:
        if t.name == '{}.py'.format(SCRIPT_NAME):
            text = t
            break
    if text is None:
        raise Exception('The script "{}.py is not loaded"'.format(SCRIPT_NAME))
    obj.game.controllers[-1].mode = 'SCRIPT'
    obj.game.controllers[-1].text = text

    # Set the object as non-actor ghost object, i.e. it will detect collisions
    # without either reacting or generating collisions.
    obj.game.use_actor = False
    obj.game.use_ghost = True


def create():
    dynamic.create()
    destroyable.create()
    generateProperties()
    loadScript()
    createLogic()


def draw(context, layout):
    dynamic.draw(context, layout)
    destroyable.draw(context, layout)
    row = layout.row()
    row.prop(context.object,
             "sss_turret_min_angle",
             text="Minimum angle (deg)")
    row = layout.row()
    row.prop(context.object,
             "sss_turret_max_angle",
             text="Maximum angle (deg)")
    row = layout.row()
    row.prop(context.object,
             "sss_turret_vel_angle",
             text="Rotation velocity (deg/s)")

