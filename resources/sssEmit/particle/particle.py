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
import math
import mathutils


def updateValues():
    """Update the particle values."""
    pass


def generateObjectProperties(update_callback):
    """Generate the Blender object properties.

    Position arguments:
    update_callback -- Function that must be called when the object is
    modified. It must be included into a bpy.types.Panel class.
    """
    pass


def draw(context, layout):
    """Draw the particle stuff.

    Position arguments:
    context -- Calling context.
    layout -- Window layout assigned for the emitter.
    """
    row = layout.row()
    row.label("Particle settings", icon='GREASEPENCIL')


def create_particle():
    """Create a particle object in the last layer, and return its name"""
    obj_backup = bpy.context.active_object
    basename = obj_backup.name
    layers = [False]*20
    layers[-1] = True
    bpy.ops.object.empty_add(type='ARROWS', layers=layers)
    obj = bpy.context.active_object

    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = obj_backup
    bpy.context.scene.objects[obj_backup.name].select = True

    obj.name = basename + ".sssemit_particle"

    return obj.name


def remove_particle():
    """Remove the particle object associated with the emitter"""
    # To delete the object we need to select it before
    obj_backup = bpy.context.active_object
    name = bpy.context.active_object.game.properties['particle'].value
    obj = bpy.context.scene.objects[name]
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = obj
    obj.select = True

    # We also need to move to its active layer
    layers = bpy.context.scene.layers[:]
    bpy.context.scene.layers = obj.layers

    bpy.ops.object.delete()

    # Now we can restore the old selection and layers
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = obj_backup
    obj_backup.select = True
    bpy.context.scene.layers = layers
    

    


