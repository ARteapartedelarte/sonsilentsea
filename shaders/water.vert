/***************************************************************************
 *                                                                         *
 *   Copyright (c) 2013, 2014                                              *
 *   Jose Luis Cercos-Pita <jlcercos@gmail.com>                            *
 *                                                                         *
 *   This program is free software: you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation, either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program.  If not, see <http://www.gnu.org/licenses/>. *
 *                                                                         *
 ***************************************************************************/

// Used later to determine the screen coordinates
varying vec4 fragPos;
// tangent, binormal, normal
varying vec3 T, B, N;
// Camera position and water point position (In the model space)
varying vec3 viewPos, worldPos;
// Vertex position in real and in view spaces
varying vec3 pos, vPos;
// World timer
varying float timer;
// Input Model matrix, used just to compute the water point position
uniform mat4 ModelMatrix;

void main() 
{	
	fragPos = ftransform();

	T   = vec3(1.0,0.0,0.0);
	B   = cross(gl_Normal.xyz, T);
	N   = gl_Normal; 

    viewPos  = (gl_Vertex - gl_ModelViewMatrixInverse[3]).xyz;
	worldPos = (ModelMatrix*gl_Vertex).xyz;
	pos      = gl_Vertex.xyz;
	vPos     = (gl_ModelViewMatrix*gl_Vertex).xyz;

    timer = gl_Color.w*2.0;

    gl_Position = ftransform();
}
