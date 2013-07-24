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

import os
from os import path

try:
    import bgui
except:
    print('Warning! Can not import bgui')
import bge
from bge import logic as g
from bge import texture
from math import *
from mathutils import *

# Get the ship
controller = g.getCurrentController()
owner      = controller.owner
ship       = owner

# Get the GUI manager (if exist)
scene   = g.getCurrentScene()
objects = scene.objects
camera  = scene.active_camera
gui     = None
if 'gui' in camera:
		# Create our system and show the mouse
		gui = camera['gui']

# Generate a visibility factor table
visibility_table = [[ -10.5, -5.95, -5.90, -1.90, 1.0 ],
                    [   0.0,  0.05,  0.10,  0.25, 1.0 ]]
if not 'visibility' in ship:
	ship['visibility'] = visibility_table[1][-1]

# Setup the maximum dimensions
L = 67.2
B = 6.6
H = 15.65
if not 'L' in ship:
	ship['L'] = L
if not 'B' in ship:
	ship['B'] = B
if not 'L' in ship:
	ship['H'] = H

# Watts of noise generated per Watt of power generated
dPower = 1.0E6
ePower = 280.0E3
noise_dPower = 0.1
noise_ePower = 0.04

# Noise limit for the GUI (in Watts)
noise_max = 1.25*noise_dPower*dPower

if not 'noise' in ship:
	ship['noise'] = 0.0

# Get the images path
blend_file  = path.dirname(__file__)
images_path = path.join(path.dirname(blend_file), 'GUI')

# Compute de widgets dimensions
image_dims  = [0.05,0.05]
w = bge.render.getWindowWidth()
h = bge.render.getWindowHeight()
aspect_ratio = h / w
if aspect_ratio > 1.0:
	image_dims[0] *= aspect_ratio
else:
	image_dims[1] /= aspect_ratio
widget_dims  = [0.25,0.025]

# Create the widgets
if gui:
	img = path.join(images_path,'Actions-layer-visible-off-icon.png')
	widget = bgui.Image(gui, 'player_visibility_img', img, size=[image_dims[0], image_dims[1]],
	                    pos=[0.975-widget_dims[0]-image_dims[0], widget_dims[1] + image_dims[1]],
	                    options = bgui.BGUI_DEFAULT|bgui.BGUI_CACHE)
	widget = bgui.ProgressBar(gui, "player_visibility", percent=0.0, size=[widget_dims[0], widget_dims[1]],
	                    pos=[0.975-widget_dims[0], widget_dims[1] + image_dims[1]],
	                    sub_theme='Red', options = bgui.BGUI_DEFAULT)
	img = path.join(images_path,'Actions-speaker-icon.png')
	widget = bgui.Image(gui, 'player_noise_img', img, size=[image_dims[0], image_dims[1]],
	                    pos=[0.975-widget_dims[0]-image_dims[0], widget_dims[1]],
	                    options = bgui.BGUI_DEFAULT|bgui.BGUI_CACHE)
	widget = bgui.ProgressBar(gui, "player_noise", percent=0.0, size=[widget_dims[0], widget_dims[1]],
	                    pos=[0.975-widget_dims[0], widget_dims[1]],
	                    sub_theme='Red', options = bgui.BGUI_DEFAULT)

def _update_visibility():
	z        = ship.worldPosition[2]
	v_factor = visibility_table[1][-1]
	for i in range(1,len(visibility_table[0])):
		z_sup = visibility_table[0][i]
		v_sup = visibility_table[1][i]
		z_inf = visibility_table[0][i-1]
		v_inf = visibility_table[1][i-1]
		if z_sup > z:
			f        = (z_sup - z)/(z_sup - z_inf)
			v_factor = min(1.0,max(0.0,f*v_inf + (1.0 - f)*v_sup))
			break
	ship['visibility'] = v_factor
	# Update GUI
	if not gui:
		return
	gui.children['player_visibility'].percent = v_factor

def _update_noise():
	# Compute engine noise
	march = ship['speed']
	if abs(march) > 3:
		march = int(copysign(3,march))
		ship['speed'] = march
	factor = noise_dPower
	power  = dPower
	if ship.worldPosition[2] < -1.0:
		# ship is submerged
		factor = noise_ePower
		power  = ePower
	m = abs(float(march))
	noise_engine = m*m/9.0 * factor * power
	# Sum all the noise generated
	ship['noise'] = noise_engine
	# Update GUI
	if not gui:
		return
	gui.children['player_noise'].percent = min(1.0,ship['noise']/noise_max)

def update():
	""" Update the AI
	@note Call this method each frame
	"""
	# Update self data
	_update_visibility()
	_update_noise()

