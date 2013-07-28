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

# ----------------------------
# General properties
# ----------------------------

# Maximum view distance [m]
vMax = 10000.0
# Surely viewing distance [m]
vMin = 200.0


# ----------------------------
# AI properties
# ----------------------------

def update():
	""" Updates the list of enemies, and the commands
	(propulsion, firing, etc.)
	"""
	# Don't works if the object is destroyed
	if not ship['alive']:
		return

	# Several instances of the ship can be required,
	# so we need to get the object instance each time
	controller = g.getCurrentController()
	ship       = controller.owner

	# Ships can be added or removed from the scene, so
	# we need to renew the list of ships each frame
	scene      = g.getCurrentScene()
	objects    = scene.objects
	ships      = []
	for obj in objects:
		if 'Ship.Main' in obj.name:
			ships.append(obj)

