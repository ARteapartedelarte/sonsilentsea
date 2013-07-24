#    Copyright (c) 2013, 2014
#    Jose Luis Cercos-Pita <jlcercos@gmail.com>
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import bge
from bge import logic as g
from math import *
from mathutils import *

max_angle  = radians(30.0)
d_angle    = radians(0.1)

def update():
    """ Update the rudders orientation
    @note Call this method each frame
    """
    controller = g.getCurrentController()
    wing       = controller.owner
    ship       = wing.parent
    rudder     = ship['rudder']
    angle      = wing['angle']
    objective  = max_angle * rudder/3.0
    if (angle < objective + d_angle) and (angle > objective - d_angle):
        return
    rot = copysign(d_angle, objective - angle)
    wing.applyRotation(Vector((0.0,0.0,-rot)), True)
    wing['angle'] += rot
