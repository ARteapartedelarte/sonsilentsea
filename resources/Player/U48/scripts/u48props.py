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

rpm = 150.0

def update():
    """ Update the propellers rotation and bubbles generation
    @note Call this method each frame
    """
    controller = g.getCurrentController()
    prop       = controller.owner
    ship       = prop.parent
    emitter    = prop.children[0]
    speed      = ship['speed']
    w          = copysign(2.0*pi/60.0 * speed*speed/9.0 * rpm, speed)
    # Since is an child object velocity will not work
    dt         = 1.0/g.getLogicTicRate()
    theta      = w*dt
    prop.applyRotation(Vector((theta,0.0,0.0)), True)
    
    emitter.applyRotation(Vector((-theta,0.0,0.0)), True)
    emitter['amount'] = abs(speed)**2

