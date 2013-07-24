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

# View parameters
vSens  = 0.85    # Sensitivity, higher = best detection skills
vAngle = 0.0     # Actual looking angle    [deg]
vRange = 30.0    # Angle viewing amplitude [deg]
vOmega = 10.0    # Abgle rotation velocity [deg/s]

# Sonar parameters
sSens  = 0.5     # Sensitivity, higher = best detection skills
sAngle = 0.0     # Actual looking angle    [deg]
sRange = 15.0    # Angle viewing amplitude [deg]
sOmega = 2.0     # Abgle rotation velocity [deg/s]

def updateView():
    """ Updates the view for locating enemies
    """
    dt     = 1.0/g.getLogicTicRate()
    vAngle = vAngle + vOmega*dt
    # Look for the enemy ships in the viewing area
    for s in ships:
        # Discard allies
        if ship['team'] == s['team']:
            continue
        # Discard death
        if not s['alive']:
            continue
        [l,gV,lV] = ship.getVectTo(s)
        # Test if the object is viewable
        
        if l < vMin:
            # Perfect detection
            

def update():
    """ Updates the list of enemies, and the commands
    (propulsion, firing, etc.)
    """
    # Don't works if the object is destroyed
    if not ship['alive']:
        return
    
    
# Get the ship
controller = g.getCurrentController()
ship       = controller.owner
# Get the list of ships from the scene
scene      = g.getCurrentScene()
objects    = scene.objects
ships      = []
for obj in objects:
    if 'Ship.Main' in obj.name:
        ships.append(obj)

waterPlane = objects.get('waterPlane')
if not waterPlane:
    raise Exception("Can't find the object 'waterPlane'")

# Initialize the list of enemies
enemies    = []
enemiesVel = []

# Convert to radians
vAngle = vAngle * pi/180.0
vRange = vAngle * pi/180.0
vOmega = vAngle * pi/180.0
sAngle = vAngle * pi/180.0
sRange = vAngle * pi/180.0
sOmega = vAngle * pi/180.0
