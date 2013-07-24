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

import sys
import os
from os import path

# Append the missions available paths.
# Should be improved...
paths = [path.join(sys.prefix,'share/sonsilentsea/resources/Campaigns'),
		 path.join(path.abspath('./'),'resources/Campaigns'),
		 path.expanduser('~/.sonsilentsea/resources/Campaigns')]
for p in paths:
    if not p in sys.path:
        sys.path.append(p)

import bgui
import bge
from bge import logic as g
from mathutils import *
from math import *

class MissionManager():

	def __init__(self):
		self._mission = None

	def load_mission(self,campaign,mission):
		""" Loads a mission from the campaign folder name and the mission folder name """
		exec( 'import {0}'.format(campaign) )
		exec( 'from {0} import {1}'.format(campaign, mission) )
		self._mission = eval('{0}'.format(mission))
		self._mission.load()

	def update(self):
		""" Call this method each frame """
		if self._mission != None:
			self._mission.update()

	def load_blender_file(self, file_name):
		""" Loads a blender file.
		@param file_name An absolute path to the file, or if a relative path such that
		the file will be looked for in the mission folder, in the user home resources folder,
		in the execution folder, or finally in the installation folder.
		@remarks Full scene will be loaded by default.
		"""
		# Locate the file
		file_path = self._locate_resource(file_name)
		if not file_path:
			return
		# Load it
		if file_path in g.LibList():
			return
		status = g.LibLoad(file_path,'Scene', load_actions=True, verbose=True, load_scripts=True)

	def _locate_resource(self, file_name):
		if path.isabs(file_name):
			return file_name
		# Default paths
		paths = [path.join(sys.prefix,'share/sonsilentsea/resources'),
				 path.join(path.abspath('./'),'resources'),
				 path.expanduser('~/.sonsilentsea/resources')]
		# Add the mission file path
		if self._mission:
			paths.append(path.dirname(path.abspath(self._mission.__file__)))
		# Look for the file in the paths
		for p in paths:
			file_path = path.join(p,file_name)
			if path.isfile(file_path):
				return file_path
		return None

def main(cont):
	if 'mission_manager' not in own:
		own['mission_manager'] = MissionManager()
	else:
		own['mission_manager'].update()

cont = bge.logic.getCurrentController()
own  = cont.owner
main(cont)
