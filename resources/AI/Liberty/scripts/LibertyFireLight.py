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
import random 
from mathutils import *

def update():
	""" Updates the fire light
	"""
	# Several instances will call this script, we need to
	# renew the instance each time
	controller = g.getCurrentController()
	own        = controller.owner

	own.color    = [own['multiplier']*0.40,
	                own['multiplier']*0.12,
	                0.0]
	A = 5.0
	T = own['period']
	P = own['phase']
	t = own['timer']
	own.distance = 25.0 + A*sin(2*pi/T*t + P)

def load():
	""" Load the light, selecting a ramdom phase
	"""
	controller   = g.getCurrentController()
	own          = controller.owner
	own['phase'] = random.uniform(0, 2.0*pi)

