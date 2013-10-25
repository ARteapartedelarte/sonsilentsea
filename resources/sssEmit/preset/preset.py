import bpy
import math
from bpy.props import StringProperty

class preset(bpy.types.PropertyGroup):
    """ Group of properties of the emmiter presets """
    particles = bpy.props.StringProperty(default='')
    particlesScale = bpy.props.StringProperty(default='')
    addmode = bpy.props.StringProperty(default='')
    name = bpy.props.StringProperty(default='')
    emitTime = bpy.props.IntProperty(default=60)
    lifetime = bpy.props.IntProperty(default=0)
    randomlifetimevalue = bpy.props.IntProperty(default=0)
    amount = bpy.props.IntProperty(default=10)
    cone = bpy.props.FloatVectorProperty(name='',default=(0.261800, 0.261800, 0.261800))
    rangeEmit = bpy.props.FloatVectorProperty(name='',default=(0.0,0.0,0.0))
    ellipsoidalRange = bpy.props.BoolProperty(name='',default=False)
    startcolor = bpy.props.FloatVectorProperty(name='',default=(0.0,0.0,0.0))
    endcolor = bpy.props.FloatVectorProperty(name='',default=(0.0,0.0,0.0))
    alpha = bpy.props.FloatProperty(default=1.0)
    colorfade_start = bpy.props.IntProperty(default=0)
    colorfade_end = bpy.props.IntProperty(default=60)
    fadein = bpy.props.IntProperty(default=10)
    fadeout = bpy.props.IntProperty(default=30)
    particlerotation = bpy.props.FloatProperty(default=0.0)
    startspeed = bpy.props.FloatProperty(default=0.0)
    startspeedRadial = bpy.props.StringProperty(default='1')
    endspeed = bpy.props.FloatProperty(default=0.1)
    endspeedRadial = bpy.props.StringProperty(default='1')
    speedfade_start = bpy.props.IntProperty(default=0)
    speedfade_end = bpy.props.IntProperty(default=60)
    randomMovement = bpy.props.FloatProperty(default=0.0)
    startscale = bpy.props.FloatProperty(default=1.0)
    endscale = bpy.props.FloatProperty(default=1.0)
    scalefade_start = bpy.props.FloatProperty(default=1.0)
    scalefade_end = bpy.props.FloatProperty(default=1.0)


class init_presets(bpy.types.Operator):
    bl_idname = "scene.init_preset" 
    bl_label = "Load the default particle presets"
    bl_description = "Create the default presets (if they does not exist yet)"
   
    def default_preset(self,
                     particles='"Particle_Generic",',
                     particlesScale='"1.0"',
                     addmode='"True"',
                     name='Generic',
                     emitTime=0,
                     lifetime=60,
                     randomlifetimevalue=0,
                     amount=10,
                     cone=(0,0,0),
                     rangeEmit=(0,0,0),
                     ellipsoidalRange=False,
                     startcolor=(0.5, 0.3, 0.0),
                     endcolor=(0.5, 0.0, 0.0),
                     alpha=1.0,
                     colorfade_start=0,
                     colorfade_end=60,
                     fadein=10,
                     fadeout=30,
                     particlerotation=0,
                     startspeed=0,
                     endspeed=0.1,
                     speedfade_start=0,
                     speedfade_end=60,
                     randomMovement=0,
                     startscale=1.0,
                     endscale=1.0,
                     scalefade_start=0,
                     scalefade_end=0):
        item = bpy.data.scenes[0].preset.add()
        item.particles = particles
        item.particlesScale = particlesScale
        item.addmode = addmode
        item.name = name
        item.emitTime = emitTime
        item.lifetime = lifetime
        item.randomlifetimevalue = randomlifetimevalue
        item.amount = amount
        item.cone = cone
        item.rangeEmit = rangeEmit
        item.ellipsoidalRange = ellipsoidalRange
        item.startcolor = startcolor
        item.endcolor = endcolor
        item.alpha = alpha
        item.colorfade_start = colorfade_start
        item.colorfade_end = colorfade_end
        item.fadein = fadein
        item.fadeout = fadeout
        item.particlerotation = particlerotation
        item.startspeed = startspeed
        item.startspeedRadial = startspeedRadial
        item.endspeed = endspeed
        item.endspeedRadial = endspeedRadial
        item.speedfade_start = speedfade_start
        item.speedfade_end = speedfade_end
        item.randomMovement = randomMovement
        item.startscale = startscale
        item.endscale = endscale
        item.scalefade_start = scalefade_start
        item.scalefade_end = scalefade_end 

    def execute(self, context):
        # Test for existing presets
        fire = False  
        smoke = False
        fireball = False
        waterfall = False
        snow = False
        for item in bpy.context.scene.preset:
            if item.name == 'Fire':
                fire = True
            if item.name == 'Smoke':
                smoke = True
            if item.name == 'Fireball':
                fireball = True
            if item.name == 'Waterfall':
                waterfall = True
            if item.name == 'Snow':
                snow = True
                
        if fire == False:
            self.default_preset(particles='"Particle_Fire",',
                              name='Fire',
                              startcolor=(0.500000, 0.308322, 0.022600),
                              endcolor=(0.500000, 0.026320, 0.019954),
                              particlerotation=0.001745,
                              startspeed=0,
                              endspeed=10,
                              speedfade_start=1,
                              speedfade_end=60,
                              randomMovement=0.261800,
                              startscale=1.0,
                              endscale=0.8,
                              scalefade_start=0,
                              scalefade_end=60)
        if smoke == False:
            self.default_preset(particles='"Particle_Water",',
                              name='Smoke',
                              addmode='"False"',
                              startcolor=(0.5, 0.5, 0.5),
                              endcolor=(0.5, 0.5, 0.5),
                              alpha=0.5,
                              fadein=10,
                              fadeout=50,
                              particlerotation=0.001745,
                              startspeed=5,
                              endspeed=7,
                              speedfade_start=1,
                              speedfade_end=60,
                              randomMovement=0.349066,
                              startscale=1.0,
                              endscale=2.0,
                              scalefade_start=20,
                              scalefade_end=60)
        if fireball == False:
            self.default_preset(particles='"Particle_Fire",',
                              name='Fireball',
                              lifetime=180,
                              cone=(2*math.pi,2*math.pi,2*math.pi),
                              startcolor=(0.459987, 0.283649, 0.020791),
                              endcolor=(0.193321, 0.010176, 0.007715),
                              fadein=10,
                              fadeout=50,
                              particlerotation=0.001745,
                              startspeed=0,
                              endspeed=2,
                              speedfade_start=1,
                              speedfade_end=60,
                              randomMovement=0.349066,
                              startscale=1.0,
                              endscale=2.0,
                              scalefade_start=20,
                              scalefade_end=60)
        if waterfall == False:
            self.default_preset(particles='"Particle_Water",',
                              name='Waterfall',
                              addmode='"False"',
                              rangeEmit=(0,1,0),
                              startcolor=(0.534287, 0.816591, 1.000000),
                              endcolor=(0.700371, 0.895857, 1.000000),
                              fadein=40,
                              fadeout=100,
                              particlerotation=0.034907,
                              startspeed=5,
                              endspeed=-20,
                              speedfade_start=1,
                              speedfade_end=60,
                              startscale=1.0,
                              endscale=4.0,
                              scalefade_start=10,
                              scalefade_end=160)
        if snow == False:
            self.default_preset(particles='"Particle_Hard",',
                              name='Snow',
                              lifetime=180,
                              amount=7,
                              rangeEmit=(10,10,0),
                              startcolor=(0.534287, 0.816591, 1.000000),
                              endcolor=(0.700371, 0.895857, 1.000000),
                              fadein=40,
                              fadeout=100,
                              startspeed=-6,
                              endspeed=-6,
                              speedfade_start=1,
                              speedfade_end=60,
                              randomMovement=0.349066,
                              scalefade_start=10,
                              scalefade_end=160)
        return{'FINISHED'}

class add_preset(bpy.types.Operator):
    bl_idname = "scene.add_preset" 
    bl_label = "Add a particle preset"        
    bl_description = "Add the active particle settings to a new item in the presets list"

    def execute(self, context):
        # Ensure that the object is a particles system
        try:
            particles = bpy.context.object.particle_list
        except:
            print('Error: You should execute this tool on top of a particles system')
            return{'FINISHED'}
        # Add the new preset with all the new data
        item = bpy.data.scenes[0].preset.add()
        for x in bpy.context.object.particle_list:
            item.particles += '"' + x.name + '"' +','
            item.particlesScale += '"' + str(x.scale) + '"' +','
            item.addmode += '"' + str(x.addmode) + '"' +','
        item.name = 'Preset'
        item.emitTime = bpy.context.active_object.emitTime
        item.lifetime = bpy.context.active_object.lifetime
        item.randomlifetimevalue = bpy.context.active_object.randomlifetimevalue
        item.amount = bpy.context.active_object.amount
        item.cone = bpy.context.active_object.cone
        item.rangeEmit = bpy.context.active_object.rangeEmit
        item.ellipsoidalRange = bpy.context.active_object.ellipsoidalRange
        item.startcolor = bpy.context.active_object.startcolor
        item.endcolor = bpy.context.active_object.endcolor
        item.alpha = bpy.context.active_object.alpha
        item.colorfade_start = bpy.context.active_object.colorfade_start
        item.colorfade_end = bpy.context.active_object.colorfade_end
        item.fadein = bpy.context.active_object.fadein
        item.fadeout = bpy.context.active_object.fadeout
        item.particlerotation = bpy.context.active_object.particlerotation
        item.startspeed = bpy.context.active_object.startspeed
        item.startspeedRadial = bpy.context.active_object.startspeedRadial
        item.endspeed = bpy.context.active_object.endspeed
        item.endspeedRadial = bpy.context.active_object.endspeedRadial
        item.speedfade_start = bpy.context.active_object.speedfade_start
        item.speedfade_end = bpy.context.active_object.speedfade_end
        item.randomMovement = bpy.context.active_object.randomMovement
        item.startscale = bpy.context.active_object.startscale
        item.endscale = bpy.context.active_object.endscale
        item.scalefade_start = bpy.context.active_object.scalefade_start
        item.scalefade_end = bpy.context.active_object.scalefade_end
        return{'FINISHED'}
    
class remove_preset(bpy.types.Operator):
    bl_idname = "scene.remove_preset" 
    bl_label = "Add Particle Preset" 
    bl_description = "Remove the selected preset from the list"       
    
    def execute(self, context):
        try:
            item = bpy.data.scenes[0].preset.remove(bpy.data.scenes[0].preset_index)
        except:
            print('Error: I can not delete the item {0}'.format(bpy.data.scenes[0].preset_index))
        return{'FINISHED'}

class apply_preset(bpy.types.Operator):
    bl_idname = "scene.apply_preset" 
    bl_label = ""
    bl_description = "Apply Preset to active Particle System"
    
    def execute(self,context):
        scene = bpy.data.scenes[0]
        try:
            particles = eval(scene.preset[scene.preset_index]['particles'])
            particlesScale = eval(scene.preset[scene.preset_index]['particlesScale'])
            addmode = eval(scene.preset[scene.preset_index]['addmode'])
        except:
            print("Error: The preset data can not be readed. Have you selected a preset?")
            return{'FINISHED'}
        print("addmode:",addmode)
        for i in range(len(bpy.context.object.particle_list)):
            bpy.context.object.particle_list.remove(0)
        for i in range(len(particles)):
            item = bpy.context.object.particle_list.add()
            item.name = particles[i]
            item.scale = float(particlesScale[i])
            print(addmode[i])
            if addmode[i] == 'T':
                item.addmode = True
            else:
                item.addmode = False
            
        context.object.emitTime = scene.preset[scene.preset_index]['emitTime']
        context.object.lifetime = scene.preset[scene.preset_index]['lifetime']
        context.object.randomlifetimevalue = scene.preset[scene.preset_index]['randomlifetimevalue']
        context.object.amount = scene.preset[scene.preset_index]['amount']
        context.object.cone = scene.preset[scene.preset_index]['cone']
        context.object.rangeEmit = scene.preset[scene.preset_index]['rangeEmit']
        context.object.startcolor = scene.preset[scene.preset_index]['startcolor']
        context.object.endcolor = scene.preset[scene.preset_index]['endcolor']
        context.object.alpha = scene.preset[scene.preset_index]['alpha'] 
        context.object.colorfade_start = scene.preset[scene.preset_index]['colorfade_start']
        context.object.colorfade_end = scene.preset[scene.preset_index]['colorfade_end']
        context.object.fadein = scene.preset[scene.preset_index]['fadein']
        context.object.fadeout = scene.preset[scene.preset_index]['fadeout']
        context.object.particlerotation = scene.preset[scene.preset_index]['particlerotation']
        context.object.startspeed = scene.preset[scene.preset_index]['startspeed']
        context.object.endspeed = scene.preset[scene.preset_index]['endspeed']
        context.object.randomMovement = scene.preset[scene.preset_index]['randomMovement']
        context.object.startscale = scene.preset[scene.preset_index]['startscale']
        context.object.endscale = scene.preset[scene.preset_index]['endscale']
        context.object.scalefade_start = scene.preset[scene.preset_index]['scalefade_start']
        context.object.scalefade_end = scene.preset[scene.preset_index]['scalefade_end']
        # New data which may don't exist in the saved file
        try:
            context.object.ellipsoidalRange = scene.preset[scene.preset_index]['ellipsoidalRange']
            context.object.startspeedRadial = scene.preset[scene.preset_index]['startspeedRadial']
            context.object.endspeedRadial = scene.preset[scene.preset_index]['endspeedRadial']
        except:
            pass
        return{'FINISHED'}

