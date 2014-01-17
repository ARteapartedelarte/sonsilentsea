###############################################################################
#                                                                             #
#  This file is part of SonSilentSea, a free ships based combatr game.        #
#  Copyright (C) 2014  Jose Luis Cercos Pita <jlcercos@gmail.com>             #
#                                                                             #
#  AQUAgpusph is free software: you can redistribute it and/or modify         #
#  it under the terms of the GNU General Public License as published by       #
#  the Free Software Foundation, either version 3 of the License, or          #
#  (at your option) any later version.                                        #
#                                                                             #
#  AQUAgpusph is distributed in the hope that it will be useful,              #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#  GNU General Public License for more details.                               #
#                                                                             #
#  You should have received a copy of the GNU General Public License          #
#  along with AQUAgpusph.  If not, see <http://www.gnu.org/licenses/>.        #
#                                                                             #
###############################################################################

import bpy
import math
import mathutils
from os import path


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
        obj.game.properties['prop'].name = name
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
    addProperty('culling', 'BOOL', True)
    addProperty('cullingRadius', 'FLOAT', 0.0)


def removeProperties():
    """Remove the properties the object."""
    delProperty('culling')
    delProperty('cullingRadius')


def updateValues():
    """Update the particles emmiter values."""
    generateProperties()

    obj = bpy.context.object
    obj.game.properties['culling'].value = obj.frustrum_culling
    obj.game.properties['cullingRadius'].value = obj.frustrum_radius


def loadScript():
    """Load/update the text script in text editor."""
    filepath = None
    for folder in addonsPaths():
        f = path.join(folder, "sssEmit/emitter.py")
        if not path.isfile(f):
            continue
        filepath = f
        break
    if not filepath:
        raise Exception('I can not find the script file "emitter.py"')

    # We can try to update it, and if the operation fails is just because the
    # file has not been loaded yet
    try:
        text = bpy.data.texts['emitter.py']
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


class create_emmiter(bpy.types.Operator):
    bl_idname = "scene.create_emmiter"
    bl_label = "Transform into an emmiter"
    bl_description = "Transform the object into an emmiter"

    def createLogic(self):
        obj = bpy.context.object
        bpy.context.active_object.draw_type = 'WIRE'
        # Add a sensor in order to execute the script each frame
        bpy.ops.logic.sensor_add(type='ALWAYS', name="", object="")
        obj.game.sensors['Always'].frequency = 0
        obj.game.sensors['Always'].use_pulse_true_level = True
        # Add a controller to launch the script
        bpy.ops.logic.controller_add(type='PYTHON', name="", object="")
        obj.game.controllers['Python'].mode = 'MODULE'
        obj.game.controllers['Python'].module = 'emitter.emitter'
        obj.game.controllers['Python'].link(obj.game.sensors['Always'])
        obj.game.physics_type = 'NO_COLLISION'
        # Add a controller to reference the script (but never used). It is
        # useful if the object will be imported from other blender file,
        # inserting the script in the importer scene
        bpy.ops.logic.controller_add(type='PYTHON',
                                     name="Reference",
                                     object="")
        text = None
        for t in bpy.data.texts:
            if t.name == 'emitter.py':
                text = t
                break
        if text is None:
            raise Exception('The script "emitter.py is not loaded"')
        obj.game.controllers['Reference'].mode = 'SCRIPT'
        obj.game.controllers['Reference'].text = text

    def execute(self, context):
        obj = bpy.context.active_object

        obj.emmiter = True
        obj.draw_type_back = obj.draw_type
        obj.draw_type = 'WIRE'
        generateProperties()
        loadScript()
        self.createLogic()

        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = obj
        bpy.context.scene.objects[obj.name].select = True

        return{'FINISHED'}


class remove_emmiter(bpy.types.Operator):
    bl_idname = "object.remove_emmiter"
    bl_label = "Remove the emmiter"
    bl_description = "Remove the object emmiter stuff"

    def del_particle_logic(self):
        obj = bpy.context.active_object
        bpy.ops.logic.sensor_remove(sensor="Always",
                                    object=obj.name)
        bpy.ops.logic.controller_remove(controller="Python",
                                        object=obj.name)
        bpy.ops.logic.controller_remove(controller="Reference",
                                        object=obj.name)

    def execute(self, context):
        obj = bpy.context.active_object

        obj.emmiter = False
        obj.draw_type = obj.draw_type_back
        removeProperties()
        self.del_particle_logic()

        return{'FINISHED'}
