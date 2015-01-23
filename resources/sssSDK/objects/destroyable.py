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
from sssSDK.utils import *


# Module data
NAME = 'Destroyable object'
DESCRIPION = 'A destroyable object'
SELECTABLE = False
CLASS_NAME = 'sssDestroyable'
SCRIPT_NAME = 'sss_destroyable'


def generateProperties():
    """Ensure that the object has the required properties."""
    addProperty('AP', 'FLOAT', 0.0)
    addProperty('HP', 'FLOAT', 1.0)


def updateValues():
    """Update the particles emitter values."""
    generateProperties()
    loadScript()

    obj = bpy.context.object
    obj.game.properties['AP'].value = obj.sss_destroyable_AP
    obj.game.properties['HP'].value = obj.sss_destroyable_HP


def generateObjectProperties(update_callback):
    """Generate the Blender object properties.
    """
    bpy.types.Object.sss_destroyable_AP = bpy.props.FloatProperty(
        default=0.0,
        update=update_callback,
        description='Armour points of the object. As more armour points more'
                    ' hard will be damaging the object')
    bpy.types.Object.sss_destroyable_HP = bpy.props.FloatProperty(
        default=1.0,
        update=update_callback,
        description='Health points of the object. As more health points more'
                    ' damage will be resisted')


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


def create():
    generateProperties()
    loadScript()
    createLogic()


def draw(context, layout):
    row = layout.row()
    row.prop(context.object,
             "sss_destroyable_AP",
             text="Armour points")
    row = layout.row()
    row.prop(context.object,
             "sss_destroyable_HP",
             text="Health points")
