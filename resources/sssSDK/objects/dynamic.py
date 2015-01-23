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
NAME = 'Dynamic object'
DESCRIPION = 'A dynamic object'
SELECTABLE = True
CLASS_NAME = 'sssDynamic'
SCRIPT_NAME = 'sss_dynamic'

MASS_FACTOR = 1E-4


def generateProperties():
    """Ensure that the object has the required properties."""
    addProperty('real_mass', 'STRING', '1.0')


def updateValues():
    """Update the particles emitter values."""
    generateProperties()
    loadScript()

    obj = bpy.context.object
    obj.game.properties['real_mass'].value = obj.sss_dynamic_mass
    m = min(10000.0, max(0.01, MASS_FACTOR * float(obj.sss_dynamic_mass)))
    obj.game.mass = m


def generateObjectProperties(update_callback):
    """Generate the Blender object properties.
    """
    bpy.types.Object.sss_dynamic_mass = bpy.props.StringProperty(
        default='1.0',
        update=update_callback,
        description='Real mass of the object. It is needed due to the'
                    ' restrictions imposed by Blender in the mass field')


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
    # Now we must set some script data
    text = bpy.data.texts[SCRIPT_NAME + '.py']
    text.clear()
    f = open(filepath, 'r')
    txt = f.read()
    txt = txt.replace('@MASS_FACTOR@', '{}'.format(MASS_FACTOR))
    text.write(txt)
    f.close()


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


def createPhysics():
    obj = bpy.context.active_object

    obj.game.physics_type = 'RIGID_BODY'
    mask = list(obj.game.collision_group)
    mask[-1] = False
    mask[-2] = False
    obj.game.collision_group = mask
    mask = list(obj.game.collision_mask)
    mask[-1] = False
    mask[-2] = False
    obj.game.collision_mask = mask
    obj.game.mass = MASS_FACTOR * float(obj.sss_dynamic_mass)


def create():
    generateProperties()
    loadScript()
    createLogic()
    createPhysics()


def draw(context, layout):
    row = layout.row()
    row.prop(context.object,
             "sss_dynamic_mass",
             text="mass (kg)")
