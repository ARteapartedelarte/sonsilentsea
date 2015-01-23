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
import sssSDK.objects.dynamic as dynamic
import sssSDK.objects.destroyable as destroyable


# Module data
NAME = 'Floating object'
DESCRIPION = 'A floating (non-propelled) object'
SELECTABLE = True
CLASS_NAME = 'sssFloating'
SCRIPT_NAME = 'sss_floating'


def generateProperties(v):
    """Ensure that the object has the required properties."""
    obj = bpy.context.object
    addProperty('t', 'TIMER', 0.0)
    addProperty('roll', 'FLOAT', 0.0)
    addProperty('pitch', 'FLOAT', 0.0)
    addProperty('GMT', 'FLOAT', 0.35)
    addProperty('GML', 'FLOAT', 1.0)
    addProperty('vols_n', 'INT', len(v[0]))
    for i in range(len(v[0])):
        zz = v[0][i]
        vv = v[1][i]
        addProperty('vols_z{}'.format(i), 'FLOAT', zz)
        addProperty('vols_v{}'.format(i), 'FLOAT', vv)
    # In this case we need to regenerate the displacement property
    vol = getVolume(0.0, v)
    obj.sss_dynamic_mass = '{}'.format(1025.0 * vol)
    obj.game.properties['real_mass'].value = obj.sss_dynamic_mass


def updateValues():
    """Update the particles emitter values."""
    dynamic.updateValues()
    destroyable.updateValues()
    loadScript()

    obj = bpy.context.object
    obj.game.properties['GMT'].value = obj.sss_floating_gmt
    obj.game.properties['GML'].value = obj.sss_floating_gml


def generateObjectProperties(update_callback):
    """Generate the Blender object properties.
    """
    bpy.types.Object.sss_floating_gmt = bpy.props.FloatProperty(
        default=0.35,
        min=0.0,
        update=update_callback,
        description='Transversal stability parameter')
    bpy.types.Object.sss_floating_gml = bpy.props.FloatProperty(
        default=0.35,
        min=0.0,
        update=update_callback,
        description='Longitudinal stability parameter')


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

    obj.game.damping = 0.1
    obj.game.rotation_damping = 0.1


def computeVolume():
    volumes = ([], [])
    obj = bpy.context.object

    loc = obj.location
    dim = obj.dimensions
    dim_x = dim.x
    dim_y = dim.y
    dim_z = dim.z
    z_min = loc.z - dim_z
    z_max = loc.z + dim_z

    n = 41
    dz = (z_max - z_min) / n
    if not dz:
        print('ERROR: Null dimension detected in z direction.')
        return volumes
    z = z_min + 0.5 * dz

    # Duplicate the object to cut it
    obj_dup = obj
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = obj_dup
    bpy.context.scene.objects[obj_dup.name].select = True
    bpy.ops.rigidbody.object_add()

    # Generate the cuting box
    objs = bpy.context.scene.objects.values()
    bpy.ops.mesh.primitive_cube_add(location=(loc.x, loc.y, z_min))
    for obj_cut in bpy.context.scene.objects.values():
        if obj_cut not in objs:
            break

    # Create an intersection modifier
    # The intersection may fail when the objects are completely included into
    # the cutting box, so we can use the difference operation
    mod = obj_dup.modifiers.new('mod', 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = obj_cut

    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = obj_dup
    bpy.context.scene.objects[obj_dup.name].select = True
    if list(bpy.ops.rigidbody.mass_calculate())[0] != 'FINISHED':
        print('ERROR: Total object mass cannot be computed.')
        # Remove the auxiliar generated objects
        obj_dup.modifiers.remove(mod)
        bpy.ops.rigidbody.object_remove()
        # bpy.context.scene.objects.unlink(obj_dup)
        bpy.context.scene.objects.unlink(obj_cut)

        # Set the original object as the selected one
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = obj
        bpy.context.scene.objects[obj.name].select = True
        return volumes
    v_max = obj_dup.rigid_body.mass
    while z < z_max:
        # Cut the object
        obj_cut.dimensions = (2.0 * dim_x, 2.0 * dim_y, 2.0 * (z - z_min))
        # bpy.ops.object.modifier_apply(modifier=mod.name)

        # Compute the mass
        v = 0.0
        if list(bpy.ops.rigidbody.mass_calculate())[0] == 'FINISHED':
            v = v_max - obj_dup.rigid_body.mass
        volumes[0].append(z)
        volumes[1].append(v)

        z += dz

    # Remove the auxiliar generated objects
    obj_dup.modifiers.remove(mod)
    bpy.ops.rigidbody.object_remove()
    # bpy.context.scene.objects.unlink(obj_dup)
    bpy.context.scene.objects.unlink(obj_cut)

    # Set the original object as the selected one
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = obj
    bpy.context.scene.objects[obj.name].select = True

    # Filter the null starting volumes
    while (len(volumes[0]) > 1) and (volumes[1][1] <= 0.0):
        del volumes[0][0]
        del volumes[1][0]
    # Filter the submerged volumes
    while (len(volumes[0]) > 1) and (volumes[1][-1] == volumes[1][-2]):
        del volumes[0][-1]
        del volumes[1][-1]
    # Filter the bad computed volumes
    for i in range(2, len(volumes[0])):
        if volumes[1][i] < volumes[1][i - 1]:
            volumes[1][i - 1] = 0.5 * (volumes[1][i - 2] + volumes[1][i])

    assert len(volumes[0])

    # remove odd elements to reduce the length (that could be acceptable)
    max_length = 11
    i = 1
    while len(volumes[0]) > max_length:
        del volumes[0][i]
        del volumes[1][i]
        i += 1
        if i >= len(volumes[0]) - 1:
            i = 1

    return volumes


def getVolumesFromObject(obj):
    z = []
    v = []
    try:
        n = obj.game.properties['vols_n'].value
        for i in range(n):
            z.append(obj.game.properties['vols_z{}'.format(i)].value)
            v.append(obj.game.properties['vols_v{}'.format(i)].value)
    except:
        return [],[]
    return z, v


def getVolume(z, vols):
    if z <= vols[0][0]:
        return 0.0
    if z >= vols[0][-1]:
        return vols[1][-1]
    i = 1
    while i < len(vols[0]):
        if vols[0][i] > 0.0:
            tg = (vols[1][i] - vols[1][i - 1]) / (vols[0][i] - vols[0][i - 1])
            vol = vols[1][i - 1] + (z - vols[0][i - 1]) * tg
            break
        i += 1
    return vol


def getZ(v, vols):
    if v <= 0.0:
        return vols[0][0]
    if v >= vols[1][-1]:
        return vols[0][-1]
    i = 1
    while i < len(vols[0]):
        if vols[1][i] > v:
            tg = (vols[0][i] - vols[0][i - 1]) / (vols[1][i] - vols[1][i - 1])
            z = vols[0][i - 1] + (v - vols[1][i - 1]) * tg
            break
        i += 1
    return z


def create():
    vol = computeVolume()
    dynamic.create()
    destroyable.create()
    generateProperties(vol)
    loadScript()
    createLogic()
    createPhysics()


def draw(context, layout):
    dynamic.draw(context, layout)

    row = layout.row()
    obj = context.object
    vols_z, vols_v = getVolumesFromObject(obj)
    vol = float(obj.game.properties['real_mass'].value) / 1025.0
    z = -getZ(vol, (vols_z, vols_v))
    row.label('z = {0:.3f} m'.format(z))

    row = layout.row()
    row.prop(context.object,
             "sss_floating_gmt",
             text="GMT (m)")
    row = layout.row()
    row.prop(context.object,
             "sss_floating_gml",
             text="GML (m)")

    destroyable.draw(context, layout)