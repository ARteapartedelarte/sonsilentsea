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
import sssSDK.objects.dynamic as dynamic


# Module data
NAME = 'Bullet'
DESCRIPION = 'Bullet'
SELECTABLE = True
CLASS_NAME = 'sssBullet'
SCRIPT_NAME = 'sss_bullet'


def scriptPaths():
    """Return all the possible locations for the scripts."""
    paths = bpy.utils.script_paths(check_all=True)
    paths.append(path.join(bpy.utils.resource_path('USER'), 'scripts'))
    paths.append(path.join(bpy.utils.resource_path('LOCAL'), 'scripts'))
    paths.append(path.join(bpy.utils.resource_path('SYSTEM'), 'scripts'))
    return paths


def addonsPaths():
    """ Return all the possible locations for the addons """
    paths = []
    for folder in scriptPaths():
        f = path.join(folder, 'addons')
        if path.isdir(f):
            paths.append(f)
        f = path.join(folder, 'addons_extern')
        if path.isdir(f):
            paths.append(f)
    return paths


def addProperty(name, type_id, value):
    """Test if a property exist in the object, adding it otherwise.

    Keyword arguments:
    name -- Property name
    type_id -- Type of property
    value -- Property value
    """
    obj = bpy.context.object
    if not name in obj.game.properties.keys():
        bpy.ops.object.game_property_new()
        obj.game.properties[-1].name = name
        obj.game.properties[name].type = type_id
        obj.game.properties[name].value = value


def delProperty(name):
    """Remove a property from the object if it exist.

    Keyword arguments:
    name -- Property name
    """
    obj = bpy.context.object
    if not name in obj.game.properties.keys():
        return

    for i, p in enumerate(obj.game.properties):
        if p.name == name:
            bpy.ops.object.game_property_remove(i)
            return


def generateProperties():
    """Ensure that the object has the required properties."""
    obj = bpy.context.object
    addProperty('shell', 'FLOAT', 10.0)
    addProperty('explosion', 'STRING', '')
    addProperty('water', 'STRING', '')


def updateValues():
    """Update the particles emitter values."""
    dynamic.updateValues()
    generateProperties()
    loadScript()

    obj = bpy.context.object
    obj.game.properties['shell'].value = obj.sss_shell
    obj.game.properties['explosion'].value = obj.sss_bullet_explosion
    obj.game.properties['water'].value = obj.sss_bullet_water


def generateObjectProperties(update_callback):
    """Generate the Blender object properties.
    """
    bpy.types.Object.sss_shell = bpy.props.FloatProperty(
        default=10.0,
        min=0.0,
        update=update_callback,
        description='Explosive shell in kilograms')
    bpy.types.Object.sss_bullet_explosion = bpy.props.StringProperty(
        default='',
        update=update_callback,
        description="Explosion object. Leave it empty to don't generate any"
             " object when the bullet collides")
    bpy.types.Object.sss_bullet_water = bpy.props.StringProperty(
        default='',
        update=update_callback,
        description="Water explosion object. Leave it empty to don't generate"
             " any object when the bullet hits the water")


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


def createPhysics():
    obj = bpy.context.active_object

    obj.game.damping = 0.0
    obj.game.rotation_damping = 0.0


def create():
    dynamic.create()
    generateProperties()
    loadScript()
    createLogic()
    createPhysics()


def draw(context, layout):
    dynamic.draw(context, layout)
    row = layout.row()
    row.prop(context.object,
             "sss_shell",
             text="shell (kg)")
    row = layout.row()
    row.prop(context.object,
             "sss_bullet_explosion",
             text="Explosion object")
    row = layout.row()
    row.prop(context.object,
             "sss_bullet_water",
             text="Water explosion object.")
