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
from bpy import types, props

import math

from sssEmit.particle import emitter
from sssEmit.particle import particle


bl_info = {
    "name": "Particles system (SonSilentSea)",
    "author": "Jose Luis Cercos-Pita",
    "version": (1, 0),
    "blender": (2, 6, 9),
    "api": 60610,
    "location": "Properties > Particles",
    "description": "Particles system for the BGE",
    "category": "Game Engine"}


class sssEmit(bpy.types.Panel):
    bl_label = "sssEmit"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "particle"
    COMPAT_ENGINES = {'BLENDER_GAME'}

    def updateValues(self, context):
        """ Method called when data has been changed.
        """
        emitter.updateValues()

    bpy.types.Object.emitter = bpy.props.BoolProperty(default=False)
    bpy.types.Object.draw_type_back = bpy.props.StringProperty()

    bpy.types.Object.frustrum_culling = bpy.props.BoolProperty(
        default=True,
        update=updateValues,
        description='Allows you to disable the Emitter automatically if it is'
        ' not viewable (in the camera frustrum)')
    bpy.types.Object.frustrum_radius = bpy.props.IntProperty(
        default=4,
        min=1,
        update=updateValues,
        description='Distance to the emitter where it is considered'
        ' viewable')

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        rd = context.scene.render
        return ob and ob.game and (rd.engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        col = self.layout.column()
        row = self.layout.row()
        split = self.layout.split()
        scene = bpy.data.scenes[0]
        obj = context.object
        sce = context.scene

        if obj.emitter is True:
            row = self.layout.row()
            row.label("Emitter Settings", icon='GREASEPENCIL')

            row = self.layout.row()
            row.operator("object.remove_emitter",
                         text="Remove the emitter stuff from the object",
                         icon='CANCEL')

            row = self.layout.row()
            row.prop(context.object,
                     "frustrum_culling",
                     text="Frustum based culling")
            row.prop(context.object,
                     "frustrum_radius",
                     text="Radius")

        else:
            row.operator("scene.create_emitter",
                         text="Transform into an emitter",
                         icon='PARTICLES')


def register():
    bpy.utils.register_class(emitter.create_emitter)
    bpy.utils.register_class(emitter.remove_emitter)
    bpy.utils.register_class(sssEmit)


def unregister():
    bpy.utils.unregister_class(emitter.create_emitter)
    bpy.utils.unregister_class(emitter.remove_emitter)
    bpy.utils.unregister_class(sssEmit)

if __name__ == "__main__":
    register()
