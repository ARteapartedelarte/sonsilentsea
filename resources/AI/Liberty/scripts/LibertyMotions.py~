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
# Ship properties
# ----------------------------

# gravity [m/s2]
grav = 9.8

# Ship displacement [kg]
# Take care on the spinbox limits in the bullet
# physics engine
disp      = 14.0E6
# Total freeboard (later the floating will be substracted)
freeboard = 17.0

# Stability parameter [m]
GMT = 1.5
GML = 100.0

# Engine power [W]
dPower = 3*1.9E6

# Efficiency
nu_d = 0.6
nu_m = 0.8

# Reversed march efficiency
nu_r = 0.25

controller = g.getCurrentController()
ship       = controller.owner
# Force factor due to the Blender physic properties limit
mFact = ship.mass / disp

# ----------------------------
# Speed conversions
# ----------------------------
def knot_to_ms(speed):
	return 0.51444*speed

def ms_to_knot(speed):
	return 1.94386*speed

# ----------------------------
# Forces computation
# ----------------------------
def drag(speed):
	""" Computes the drag force
	@param speed Ship speed in m/s
	@return Drag force in Newtons.
	"""
	K = 0.24
	M = disp
	return K * M**0.666 * speed**3

def propulsion(power,speed):
	""" Propulsion force
	@param power Engine power applied (W).
	@param speed Ship speed in m/s
	@return Propulsion force in Newtons.
	"""
	return nu_d * nu_m * power # / speed

def force(ship):
	""" Compute the force vector
	@param ship Ship game object
	@return ship force [N]. 
	"""
	# The speed is known from the instance
	speed = ship.localLinearVelocity[0]
	# The power depends on the march
	march = ship['speed']
	if abs(march) > 3:
		march = int(copysign(3,march))
		ship['speed'] = march
	power = ship['propulsion']*dPower
	m = float(march)
	if m < 0:
		power *= nu_r
		m     *= -1.0
	power *= m*m/9.0
	# Compute advancing force vector
	fx = copysign(propulsion(power, speed),march) - drag(speed)
	# Compute the lateral advancing force (turning process)
	speed = ship.localLinearVelocity[1]
	fy = - 100.0 * drag(speed)
	# Align it with the ship
	f = ship.worldOrientation * Vector((fx,fy,0.0))
	# Add the hydrostatic lift and damping
	if ship['floating'] >= 0.0:
		aimZ  = -(1.0-ship['floating'])*freeboard
		z     = ship.worldPosition[2]
		dz    = (z - aimZ)/freeboard
		f[2] += (1.0 - dz)*grav*disp
	else:
		f[2] += (1.0 + ship['floating'])*grav*disp
	speed = ship.worldLinearVelocity[2]
	f[2] -= 10000.0 * drag(speed)
	return f

# ----------------------------
# Balancing motion computation
# ----------------------------
def sea(ship):
	""" Defines the moment by the sea
	@param ship Ship game object
	"""
	z = ship.worldPosition[2]
	if z + freeboard < 0.0:
		return 0.0
	T = 11.0
	w = 2*pi/T
	A = 0.5E8
	return A*cos(w*ship['timer'])

def righting(ship):
	""" Defines the righting moment
	@param ship Ship game object
	"""
	st = Vector((0.0,0.0,1.0)).dot(ship.localOrientation*Vector((0.0,1.0,0.0))) - ship['angles'][0]
	return -disp*GMT*st

def viscous(ship):
	""" Defines the viscouss moment
	@param ship Ship game object
	"""
	w = ship.localAngularVelocity[0]
	K = 1.0E8
	return -K*w

def heading(ship):
	""" Defines the heading moment
	@param ship Ship game object
	"""
	st = -Vector((0.0,0.0,1.0)).dot(ship.localOrientation*Vector((1.0,0.0,0.0))) - ship['angles'][1]
	w  = ship.localAngularVelocity[1]
	K  = 1.0E10
	return -(disp*GML*st + K*w)

def yaw(ship):
	""" Defines the yaw drag moment
	@param ship Ship game object
	"""
	w  = ship.localAngularVelocity[2]
	K  = 1.0E10
	return -K*w

def moment(ship):
	""" Compute the moment vector
	@param ship Ship game object
	@return ship moment [N m]. 
	"""
	# The angular velocity is known from the ship
	w = ship.localAngularVelocity[0]
	# Compute balancing moment vector
	mx = sea(ship) + righting(ship) + viscous(ship)
	# Compute heading moment vector
	my = heading(ship)
	# Compute the yaw damping
	mz = yaw(ship)
	# Align it with the ship
	m = Vector((mx,my,mz))
	m = ship.worldOrientation * m
	return m

def rudder(ship):
	""" Compute the rudder moment. The rudder introduce
	two moments, one to turn, and one to balance due to
	the excentric position.
	@param ship Ship game object
	@return ship moment vector [N m]. 
	"""
	r = ship['rudder']
	# Allowed 3 rudder levels
	if abs(r) > 3:
		r = int(copysign(3,r))
		ship['rudder'] = r
	if not r:
		return Vector((0.0,0.0,0.0))
	# Compute the force generated by the wings
	rad   = Vector((28.75,0.0,0.0))
	speed = ship.localLinearVelocity[0]
	K     = 1.0E3
	f     = K * r/3.0 * speed*speed
	m     = f*rad.zyx
	return m

def update():
	""" Update the ship motions.
	@note Call this method each frame
	"""
	# Renew the ship instance (several instances of the same ship can be used)
	controller = g.getCurrentController()
	ship       = controller.owner

	# Advancing forces
	f = force(ship)*mFact
	ship.applyForce(f, False)
	
	# Balacing moments
	m = moment(ship)*mFact
	ship.applyTorque(m, False)
	
	# Rudder moments
	m = rudder(ship)*mFact
	ship.applyTorque(Vector((m[0],0.0,0.0)), False)
	ship.applyTorque(Vector((0.0,0.0,m[2])), True)

def load():
	""" Register some data for the ship
	(in order to can be edited outside).
	@note Call this method only one time.
	"""
	# Register the data if it is not already done
	if 'floating' not in ship:    # Remaining floatibility
		ship['floating'] = 1.0
	if 'propulsion' not in ship:  # Remaining propulsion capabilities
		ship['propulsion'] = 1.0
	if 'team' not in ship:        # Ship team
		ship['team'] = 0
	if 'alive' not in ship:       # Alive/destroyed
		ship['alive'] = True
	if 'angles' not in ship:      # Stable angles (upright/damaged stability), [roll, heading]
		ship['angles'] = [0.0,0.0]

