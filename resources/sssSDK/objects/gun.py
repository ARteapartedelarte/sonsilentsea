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
import sssSDK.objects.dynamic_loader as loader


# Module data
NAME = 'Gun'
DESCRIPION = 'Gun. The gun can rotate just in pitch angle'
SELECTABLE = True
CLASS_NAME = 'sssGun'
SCRIPT_NAME = 'sss_gun'


def generateProperties():
    """Ensure that the object has the required properties."""
    obj = bpy.context.object
    addProperty('min_pitch', 'FLOAT', -10.0)
    addProperty('max_pitch', 'FLOAT', 30.0)
    addProperty('vel_pitch', 'FLOAT', 5.0)
    addProperty('reload_time', 'FLOAT', 7.0)
    addProperty('bullet_obj', 'STRING', '')
    addProperty('bullet_vel', 'FLOAT', 250.0)
    addProperty('smoke_obj', 'STRING', '')


def updateValues():
    """Update the particles emitter values."""
    dynamic.updateValues()
    destroyable.updateValues()
    loader.updateValues()
    generateProperties()
    loadScript()

    obj = bpy.context.object
    obj.game.properties['min_pitch'].value = obj.sss_min_pitch
    obj.game.properties['max_pitch'].value = obj.sss_max_pitch
    obj.game.properties['vel_pitch'].value = obj.sss_vel_pitch
    obj.game.properties['reload_time'].value = obj.sss_reload_time
    obj.game.properties['bullet_obj'].value = obj.sss_bullet_obj
    obj.game.properties['bullet_vel'].value = obj.sss_bullet_vel
    obj.game.properties['smoke_obj'].value = obj.sss_smoke_obj

def generateObjectProperties(update_callback):
    """Generate the Blender object properties.
    """
    bpy.types.Object.sss_min_pitch = bpy.props.FloatProperty(
        default=-10.0,
        min=-90.0,
        max=0.0,
        update=update_callback,
        description='Minimum pitch angle')
    bpy.types.Object.sss_max_pitch = bpy.props.FloatProperty(
        default=30.0,
        min=0.0,
        max=90.0,
        update=update_callback,
        description='Maximum pitch angle')
    bpy.types.Object.sss_vel_pitch = bpy.props.FloatProperty(
        default=5.0,
        min=1.0,
        max=90.0,
        update=update_callback,
        description='Rotation velocity')
    bpy.types.Object.sss_reload_time = bpy.props.FloatProperty(
        default=7.0,
        min=0.0,
        update=update_callback,
        description='Reload timelapse')
    bpy.types.Object.sss_bullet_obj = bpy.props.StringProperty(
        default='',
        update=update_callback,
        description='Bullet object to be shooted')
    bpy.types.Object.sss_bullet_vel = bpy.props.FloatProperty(
        default=250.0,
        min=50.0,
        max=1500.0,
        update=update_callback,
        description='Bullet launching speed')
    bpy.types.Object.sss_smoke_obj = bpy.props.StringProperty(
        default='',
        update=update_callback,
        description='Smoke object generated when shooting')


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
    loader.create()
    generateProperties()
    loadScript()
    createLogic()


def draw(context, layout):
    dynamic.draw(context, layout)
    destroyable.draw(context, layout)
    row = layout.row()
    row.prop(context.object,
             "sss_min_pitch",
             text="Minimum pitch (deg)")
    row = layout.row()
    row.prop(context.object,
             "sss_max_pitch",
             text="Maximum pitch (deg)")
    row = layout.row()
    row.prop(context.object,
             "sss_vel_pitch",
             text="Rotation velocity (deg/s)")
    row = layout.row()
    row.prop(context.object,
             "sss_reload_time",
             text="Reload (s)")
    row = layout.row()
    row.prop(context.object,
             "sss_bullet_obj",
             text="Bullet object")
    loader.draw(context, layout)
    row = layout.row()
    row.prop(context.object,
             "sss_bullet_vel",
             text="Bullet velocity")
    row = layout.row()
    row.prop(context.object,
             "sss_smoke_obj",
             text="Smoke object")
