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
from bpy import types, props
import math
import os
from os import path
import sssSDK
try:
    import sssSDK.objects as objects
except:
    from sssSDK import objects
# Try to import all the objects
mod_files = os.listdir(objects.__path__[0])
objects.modules = []
objects.all_modules = []
for f in mod_files:
    if f == '__init__.py':
        continue
    if f.startswith('__pycache__'):
        continue
    if f.endswith('.pyc'):
        continue
    if f.endswith('.py'):
        f = f[:-3]
    exec('import sssSDK.objects.{0} as {0}'.format(f))
    objects.all_modules.append(eval('{}'.format(f)))
    if eval('{}'.format(f)).SELECTABLE is False:
        continue
    objects.modules.append(eval('{}'.format(f)))

bl_info = {
    "name": "SonSilentSea SDK",
    "author": "Jose Luis Cercos-Pita",
    "version": (1, 0),
    "blender": (2, 7, 0),
    "location": "Properties > Physics",
    "description": "Tools to generate objects for SonSilentSea",
    "category": "Game Engine"}


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


def getModule():
    """Get the selected module. None if none is selected
    """
    obj = bpy.context.object
    module_id = int(obj.types)
    if module_id == len(objects.modules):
        return None
    return objects.modules[module_id]


def getValidName():
    """Convert the object name in a valid module identifier."""
    obj = bpy.context.object
    valid_name = 'sss_' + obj.name
    # Replace all the invalid chars by underscores
    for c in valid_name:
        if not c.isalnum():
            valid_name = valid_name.replace(c, '_')
    return valid_name


def loadScript():
    """Load/update the text script in text editor."""
    module = getModule()
    if module is None:
        return

    filepath = None
    for folder in addonsPaths():
        f = path.join(folder, "sssSDK/scripts/sss_object.py")
        if not path.isfile(f):
            continue
        filepath = f
        break
    if not filepath:
        raise Exception(
            'I can not find the script file "sss_object.py"')

    # We can try to update it, and if the operation fails is just because the
    # file has not been loaded yet
    script_name = getValidName()
    try:
        text = bpy.data.texts[script_name + '.py']
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
        bpy.data.texts['sss_object.py'].name = script_name + '.py'
    # Now we must addapt the script to the selected module
    text = bpy.data.texts[script_name + '.py']
    text.clear()
    f = open(filepath, 'r')
    txt = f.read()
    txt = txt.replace('@SCRIPT_NAME@', module.SCRIPT_NAME)
    txt = txt.replace('@CLASS_NAME@', module.CLASS_NAME)
    text.write(txt)
    f.close()


def createLogic():
    obj = bpy.context.object
    script_name = getValidName()

    bpy.ops.logic.sensor_add(type='ALWAYS',
                             name=script_name + '.init',
                             object="")
    obj.game.sensors[-1].frequency = 0
    obj.game.sensors[-1].use_pulse_true_level = False
    bpy.ops.logic.controller_add(type='PYTHON',
                                 name=script_name + '.pyinit',
                                 object="")
    obj.game.controllers[-1].mode = 'MODULE'
    obj.game.controllers[-1].module = script_name + '.load'
    obj.game.controllers[-1].link(obj.game.sensors[-1])
    # Per frame executing
    bpy.ops.logic.sensor_add(type='ALWAYS',
                             name=script_name + '.update',
                             object="")
    obj.game.sensors[-1].frequency = 0
    obj.game.sensors[-1].use_pulse_true_level = True
    bpy.ops.logic.controller_add(type='PYTHON',
                                 name=script_name + '.pyupdate',
                                 object="")
    obj.game.controllers[-1].mode = 'MODULE'
    obj.game.controllers[-1].module = script_name + '.update'
    obj.game.controllers[-1].link(obj.game.sensors[-1])

    # Add a controller to reference the script (but never used). It is
    # useful if the object will be imported from other blender file,
    # inserting the script in the importer scene
    bpy.ops.logic.controller_add(type='PYTHON',
                                 name=script_name + '.reference',
                                 object="")
    text = None
    for t in bpy.data.texts:
        if t.name == '{}.py'.format(script_name):
            text = t
            break
    if text is None:
        raise Exception('The script "{}.py is not loaded"'.format(script_name))
    obj.game.controllers[-1].mode = 'SCRIPT'
    obj.game.controllers[-1].text = text


class sssSDK(bpy.types.Panel):
    bl_label = "sssSDK"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "physics"
    COMPAT_ENGINES = {'BLENDER_GAME'}

    def setObject(self, context):
        """ Method called when data has been changed.
        """
        module = getModule()
        if module is None:
            obj = bpy.context.object
            script_name = getValidName()
            bpy.ops.logic.sensor_remove(sensor=script_name + '.init',
                                        object=obj.name)
            bpy.ops.logic.sensor_remove(sensor=script_name + '.update',
                                        object=obj.name)
            bpy.ops.logic.controller_remove(controller=script_name + '.pyinit',
                                            object=obj.name)
            bpy.ops.logic.controller_remove(controller=script_name + '.pyupdate',
                                            object=obj.name)
            bpy.ops.logic.controller_remove(controller=script_name + '.reference',
                                            object=obj.name)
            return
        module.create()

        loadScript()
        createLogic()

    def updateValues(self, context):
        """ Method called when data has been changed.
        """
        module = getModule()
        if module is None:
            return
        module.updateValues()

    def generateObjectProperties(create_callback, update_callback):
        """Generate the Blender object properties.
        """
        types = []
        for i, module in enumerate(objects.modules):
            iden = '{}'.format(i)
            name = module.NAME
            desc = module.DESCRIPION
            types.append((iden, name, desc))
        types.append(('{}'.format(len(objects.modules)),
                      'None',
                      'Non SonSilentSea object'))
        bpy.types.Object.types = bpy.props.EnumProperty(
            name="SonSilentSea object",
            items=types,
            default='{}'.format(len(objects.modules)),
            update=create_callback,
            description="Set the type of object")

        for module in objects.all_modules:
            module.generateObjectProperties(update_callback)

    generateObjectProperties(setObject, updateValues)

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        rd = context.scene.render
        return ob and ob.game and (rd.engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        self.layout.column()
        self.layout.row()
        self.layout.split()
        obj = context.object

        row = self.layout.row()
        row.prop(obj,
                 "types",
                 text="")
        module = getModule()
        if module is None:
            return
        module.draw(context, self.layout)


def register():
    bpy.utils.register_class(sssSDK)


def unregister():
    bpy.utils.unregister_class(sssSDK)


if __name__ == "__main__":
    register()
