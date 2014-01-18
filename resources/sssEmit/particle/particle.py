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
    """Draw the emitter stuff.

    Position arguments:
    context -- Calling context.
    layout -- Window layout assigned for the emitter.
    """
    row = layout.row()
    row.label("Particle settings", icon='GREASEPENCIL')
