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
from mathutils import *
from math import *

# Get the owner (should be the camera)
cont = bge.logic.getCurrentController()
own  = cont.owner

# Get the general scene
scene = g.getCurrentScene()

# And get the missions manager from the owner.
# The mission manager has several utilities like
# loading objects from other blender files
Manager = own['mission_manager']

# Useful global variables
loaded  = False
player  = None

def update():
	""" This method is called each frame. """
	if not loaded:
		return
	return

def load():
	# We will add the objects in the scene origin, and move later
	objlist = scene.objects
	origin  = objlist.get('MainScene.Origin')
	if not origin:
		raise Exception("Can't find the object 'MainScene.Origin'")
	
	print('Loading U48 player object...')
	Manager.load_blender_file('Player/U48/U48.kk.blend')
	active   = scene.objects
	inactive = scene.objectsInactive
	if (not 'Ship.Main.U48' in active) and (not 'Ship.Main.U48' in inactive):
		print('FAIL! The file was not loaded')
		return
	if 'Ship.Main.U48' in inactive:
		player = scene.addObject('Ship.Main.U48', origin)
	print('OK!')

