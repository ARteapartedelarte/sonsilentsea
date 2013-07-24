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

// Maximum number of lights <= gl_MaxLights (often 8)
#define MAX_LIGHTS gl_MaxLights

// Constant attenuation factor (1.0 = not effect)
#define CONS_ATT 1.0

// Linear attenuation factor (4.0 = 99% of reduction at 25.0 meters)
#define LIN_ATT 4.0

// Quad attenuation factor (0.16 = 99% of reduction at 25.0 meters)
#define QUAD_ATT 0.16


varying vec4 fragPos;
varying vec3 T, B, N;
varying vec3 viewPos;
varying vec3 worldPos;
varying vec3 pos;
varying vec3 vPos;
varying float timer;
uniform sampler2D reflectionSampler,refractionSampler,normalSampler;

// ----------------
// tweakables
// ----------------

float scale = 1.0;                 // overall wave scale (decrease it for longer waves)

vec2 windDir = vec2(0.5, -0.8);    // wind direction XY
float windSpeed = 0.2;             // wind speed

vec2 bigWaves = vec2(0.3, 0.3);    // strength of big waves
vec2 midWaves = vec2(0.3, 0.15);   // strength of middle sized waves
vec2 smallWaves = vec2(0.15, 0.1); // strength of small waves
float choppy = 0.15;               // wave choppyness
float aberration = 0.003;          // chromatic aberration amount
float bump = 1.5;                  // overall water surface bumpyness
float reflBump = 0.20;             // reflection distortion amount
float refrBump = 0.08;             // refraction distortion amount

float waterAlpha = 0.1;            // ammount of water color in front of reflection/refraction

// ----------------

/** Projects the surface normal (taken from a texture) over the tangent,binormal,normal
 * quaternion.
 * @param v surface normal
 * @return Projected normal
 */
vec3 tangentSpace(vec3 v)
{
	vec3 vec;
	vec.xy=v.xy;
	vec.z=sqrt(1.0-clamp(dot(vec.xy,vec.xy),0.0,1.0));
	vec.xyz= normalize(vec.x*T+vec.y*B+vec.z*N);
	return vec;
}

/** Computes the light direction and attenuation depending on the type of light and
 * the distance to the point.
 * @param i Light index.
 * @return Light direction (w = attenuation)
 */
vec4 lightDir(int i)
{
	vec3 lightDirection;
	float attenuation;

	if(0.0 == gl_LightSource[i].position.w) 
	{
		// It is a directional light
		attenuation    = 1.0;
		lightDirection = normalize((gl_ModelViewMatrixInverse*gl_LightSource[i].position).xyz);
	} 
	else
	{
		// point light / spotlight
		vec3 vertexToLightSource = (gl_ModelViewMatrixInverse*gl_LightSource[i].position).xyz - pos;
		float distance = length(vertexToLightSource);
		attenuation    = 1.0 / (CONS_ATT + LIN_ATT * distance + QUAD_ATT * distance * distance);
		// Don't works in Blender (1.0, 0.0, 0.0 are ever passed as parameters)
		/*
		attenuation    =   1.0 / (gl_LightSource[i].constantAttenuation 
		                 + gl_LightSource[i].linearAttenuation * distance
		                 + gl_LightSource[i].quadraticAttenuation * distance * distance);
		*/
		lightDirection = vertexToLightSource / distance;

		if (gl_LightSource[i].spotCutoff <= 90.0)
		{
			// Is a spotlight, we must see if the point is in the frustrum
			vec3 lDir = normalize(gl_LightSource[i].position.xyz - vPos.xyz);
			float clampedCosine = max(0.0, dot(-lDir, gl_LightSource[i].spotDirection));
			if (clampedCosine < gl_LightSource[i].spotCosCutoff) 
			{
				attenuation = 0.0;
			}
			else
			{
				attenuation = attenuation * pow(clampedCosine, gl_LightSource[i].spotExponent);
			}
		}
	}
	return vec4(lightDirection,attenuation);
}

float fresnel_dielectric(vec3 Incoming, vec3 Normal, float eta)
{
    /* compute fresnel reflectance without explicitly computing
       the refracted direction */

    float c = abs(dot(Incoming, Normal));
    float g = eta * eta - 1.0 + c * c;
    float result;

    if(g > 0.0) {
        g = sqrt(g);
        float A =(g - c)/(g + c);
        float B =(c *(g + c)- 1.0)/(c *(g - c)+ 1.0);
        result = 0.5 * A * A *(1.0 + B * B);
    }
    else
        result = 1.0;  // TIR (no refracted component)

    return result;
}

void main()
{
	int i;

	// --------------------
	// Compute the normals
	// --------------------
	vec2 nCoord;
  	nCoord = worldPos.xy * (scale * 0.05) + windDir * timer * (windSpeed*0.04);
	vec3 normal0 = 2.0*(texture2D(normalSampler, nCoord + vec2(-timer*0.015,-timer*0.005)).rgb - 0.5);
	nCoord = worldPos.xy * (scale * 0.1) + windDir * timer * (windSpeed*0.08)-(normal0.xy/normal0.zz)*choppy;
	vec3 normal1 = 2.0*(texture2D(normalSampler, nCoord + vec2(+timer*0.020,+timer*0.015)).rgb - 0.5);
 
 	nCoord = worldPos.xy * (scale * 0.25) + windDir * timer * (windSpeed*0.07)-(normal1.xy/normal1.zz)*choppy;
	vec3 normal2 = 2.0*(texture2D(normalSampler, nCoord + vec2(-timer*0.04,-timer*0.03)).rgb - 0.5);
	nCoord = worldPos.xy * (scale * 0.5) + windDir * timer * (windSpeed*0.09)-(normal2.xy/normal2.z)*choppy;
	vec3 normal3 = 2.0*(texture2D(normalSampler, nCoord + vec2(+timer*0.03,+timer*0.04)).rgb - 0.5);
  
  	nCoord = worldPos.xy * (scale* 1.0) + windDir * timer * (windSpeed*0.4)-(normal3.xy/normal3.zz)*choppy;
	vec3 normal4 = 2.0*(texture2D(normalSampler, nCoord + vec2(-timer*0.02,+timer*0.1)).rgb - 0.5);  
    nCoord = worldPos.xy * (scale * 2.0) + windDir * timer * (windSpeed*0.7)-(normal4.xy/normal4.zz)*choppy;
    vec3 normal5 = 2.0*(texture2D(normalSampler, nCoord + vec2(+timer*0.1,-timer*0.06)).rgb - 0.5);

	// This is the normal that will be used for reflections and refractions
	vec3 nVec = normalize(normal0 * bigWaves.x + normal1 * bigWaves.y +
                            normal2 * midWaves.x + normal3 * midWaves.y +
						    normal4 * smallWaves.x + normal5 * smallWaves.y);
    nVec = tangentSpace(nVec*bump);

    // And this other for ilumination
	vec3 lNormal = normalize(normal0 * bigWaves.x*0.5 + normal1 * bigWaves.y*0.5 +
                            normal2 * midWaves.x*0.2 + normal3 * midWaves.y*0.2 +
						    normal4 * smallWaves.x*0.1 + normal5 * smallWaves.y*0.1);
    lNormal = tangentSpace(lNormal*bump);

	// ---------------------------------------------
	// Compute the diffuse and specular reflections
	// ---------------------------------------------
    vec3 vVec = - normalize(viewPos);
	vec3 diff = vec3(0.0);
	vec3 spec = vec3(0.0);
	for(i=0;i<MAX_LIGHTS;i++){
		vec4 light = lightDir(i);
		vec3 lVec  = light.xyz;
		float att  = light.w;

		// Diffuse component factor
		float d = clamp(dot(lVec,lNormal),0.0,1.0);
		// Specular component factor
		vec3 lR = 2.0*d*lNormal - lVec;
		float s = pow(clamp(dot(lR, vVec),0.0,1.0), 4.0*gl_FrontMaterial.shininess);

		// Diffuse color
		diff += att * d * gl_LightSource[i].diffuse.xyz * gl_FrontMaterial.emission.xyz;
		// Specular color
		spec += att * s * gl_LightSource[i].specular.xyz * gl_FrontMaterial.specular.xyz;
	}

    vec2 fragCoord = (fragPos.xy/fragPos.w)*0.5+0.5;
    fragCoord = clamp(fragCoord,0.002,0.998);

    //texture edge bleed removal
    float fade = 12.0;
    vec2 distortFade = vec2(0.0);
    distortFade.x = clamp(fragCoord.x*fade,0.0,1.0);
    distortFade.x -= clamp(1.0-(1.0-fragCoord.x)*fade,0.0,1.0);
    distortFade.y = clamp(fragCoord.y*fade,0.0,1.0);
    distortFade.y -= clamp(1.0-(1.0-fragCoord.y)*fade,0.0,1.0); 
    
    vec3 reflection = texture2D(reflectionSampler, fragCoord+(nVec.st*reflBump*distortFade)).rgb;
    
    vec3 luminosity = vec3(0.30, 0.59, 0.11);
	float reflectivity = pow(dot(luminosity, reflection.rgb*2.0),3.0);
    
    vec2 rcoord = reflect(- vVec,nVec).st;
    vec3 refraction = vec3(0.0);
    refraction.r = texture2D(refractionSampler, (fragCoord-(nVec.st*refrBump*distortFade))*1.0).r;
    refraction.g = texture2D(refractionSampler, (fragCoord-(nVec.st*refrBump*distortFade))*1.0-(rcoord*aberration)).g;
    refraction.b = texture2D(refractionSampler, (fragCoord-(nVec.st*refrBump*distortFade))*1.0-(rcoord*aberration*2.0)).b;
    
    //fresnel term
    float ior = 1.333;
    float fresnel = fresnel_dielectric(vVec,nVec,ior);
    fresnel = clamp(fresnel+0.25,0.0,1.0);

    vec3 fresnelColor = mix(refraction,reflection,fresnel);
    vec3 color = mix(fresnelColor,diff,waterAlpha) + spec;

    gl_FragColor = vec4(color,1.0);
}
