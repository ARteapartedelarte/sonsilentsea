import bpy
import math
from os import path

def script_paths():
    """ Return all the possible locations for the scripts """
    paths = bpy.utils.script_paths(check_all=True)
    paths.append(path.join(bpy.utils.resource_path('USER'), 'scripts'))
    paths.append(path.join(bpy.utils.resource_path('LOCAL'), 'scripts'))
    paths.append(path.join(bpy.utils.resource_path('SYSTEM'), 'scripts'))
    return paths

def addons_paths():
    """ Return all the possible locations for the scripts """
    paths = []
    for folder in script_paths():
        f = path.join(folder, 'addons')
        if path.isdir(f):
            paths.append(f)
        f = path.join(folder, 'addons_extern')
        if path.isdir(f):
            paths.append(f)
    return paths

class generate_particle_system(bpy.types.Operator):
    bl_idname = "scene.generate_particle_system" 
    bl_label = "Generate a new particle system"
    bl_description = "Generate a new particle system on top of the selected object"
    
    def __init__(self):
        self.particle = False
        self.emitter_mat = False
        bpy.ops.object.material_slot_remove()
    
    def createMaterial(self, name):
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = (1,1,1)
        mat.type = 'WIRE'
        bpy.context.active_object.data.materials.append(bpy.data.materials['Emitter'])
        
    def gen_particle_logic(self,context):
        bpy.context.active_object.draw_type = 'WIRE'
        # Add a sensor in order to execute the script each frame
        bpy.ops.logic.sensor_add(type='ALWAYS', name="", object="")
        bpy.context.object.game.sensors['Always'].frequency = 0
        bpy.context.object.game.sensors['Always'].use_pulse_true_level = True
        # Add a controller to launch the script
        bpy.ops.logic.controller_add(type='PYTHON', name="", object="")
        bpy.context.object.game.controllers['Python'].mode = 'MODULE'
        bpy.context.object.game.controllers['Python'].module = 'emitter.emitter'
        bpy.context.object.game.controllers['Python'].link(bpy.context.object.game.sensors['Always'])
        bpy.context.object.game.physics_type = 'NO_COLLISION'
        # Add a controller to reference the script (but never used). It is
        # useful if the object will be imported from other blender file,
        # inserting the script in the importing scene
        bpy.ops.logic.controller_add(type='PYTHON', name="Reference", object="")
        bpy.context.object.game.controllers['Python'].mode = 'SCRIPT'
        bpy.context.object.game.controllers['Python'].module = 'emitter.py'
        try:
            iten = bpy.context.object.particle_list[0]
        except:
            item = bpy.context.object.particle_list.add()
            item.name = 'Particle_Fire'
 
    def gen_properties(self,context):
        ### frustum Culling
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'culling'
        bpy.context.object.game.properties['culling'].type = 'BOOL'
        bpy.context.object.game.properties['culling'].value = True
        
        ### frustum Culling Radius
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'cullingRadius'
        bpy.context.object.game.properties['cullingRadius'].type = 'INT'
        bpy.context.object.game.properties['cullingRadius'].value = 4
        
        ### particle list
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'particleList'
        bpy.context.object.game.properties['particleList'].type = 'STRING'
        bpy.context.object.game.properties['particleList'].value = '[]'
        
        ### particle list
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'particleAddMode'
        bpy.context.object.game.properties['particleAddMode'].type = 'STRING'
        bpy.context.object.game.properties['particleAddMode'].value = '[]'
        
        ### particle list
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'particleScale'
        bpy.context.object.game.properties['particleScale'].type = 'STRING'
        bpy.context.object.game.properties['particleScale'].value = '[]'
        
        ### particle emitter on/off
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'emitteron'
        bpy.context.object.game.properties['emitteron'].type = 'BOOL'
        bpy.context.object.game.properties['emitteron'].value = True
        
        ### particle local or global Emission
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'localEmit'
        bpy.context.object.game.properties['localEmit'].type = 'BOOL'
        bpy.context.object.game.properties['localEmit'].value = True
        
        ### particle amount
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'amount'
        bpy.context.object.game.properties['amount'].type = 'INT'
        bpy.context.object.game.properties['amount'].value = 1
        
        ### particle emission time
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'emitTime'
        bpy.context.object.game.properties['emitTime'].type = 'INT'
        bpy.context.object.game.properties['emitTime'].value = 0
        
        ### particle lifetime
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'lifetime'
        bpy.context.object.game.properties['lifetime'].type = 'INT'
        bpy.context.object.game.properties['lifetime'].value = 60
        
        ### particle random lifetime
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'randomlifetimevalue'
        bpy.context.object.game.properties['randomlifetimevalue'].type = 'INT'
        bpy.context.object.game.properties['randomlifetimevalue'].value = 10
        
        ### particle range Emit
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'rangeEmitX'
        bpy.context.object.game.properties['rangeEmitX'].type = 'FLOAT'
        bpy.context.object.game.properties['rangeEmitX'].value = 0.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'rangeEmitY'
        bpy.context.object.game.properties['rangeEmitY'].type = 'FLOAT'
        bpy.context.object.game.properties['rangeEmitY'].value = 0.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'rangeEmitZ'
        bpy.context.object.game.properties['rangeEmitZ'].type = 'FLOAT'
        bpy.context.object.game.properties['rangeEmitZ'].value = 0.0
        
        ### particle startcolor
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'start_r'
        bpy.context.object.game.properties['start_r'].type = 'FLOAT'
        bpy.context.object.game.properties['start_r'].value = 1.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'start_g'
        bpy.context.object.game.properties['start_g'].type = 'FLOAT'
        bpy.context.object.game.properties['start_g'].value = 0.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'start_b'
        bpy.context.object.game.properties['start_b'].type = 'FLOAT'
        bpy.context.object.game.properties['start_b'].value = 0.0
        
        ### particle endcolor
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'end_r'
        bpy.context.object.game.properties['end_r'].type = 'FLOAT'
        bpy.context.object.game.properties['end_r'].value = 0.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'end_g'
        bpy.context.object.game.properties['end_g'].type = 'FLOAT'
        bpy.context.object.game.properties['end_g'].value = 0.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'end_b'
        bpy.context.object.game.properties['end_b'].type = 'FLOAT'
        bpy.context.object.game.properties['end_b'].value = 1.0
        
        ### particle alpha
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'alpha'
        bpy.context.object.game.properties['alpha'].type = 'FLOAT'
        bpy.context.object.game.properties['alpha'].value = 1.0
        
        ### particle color fade start
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'colorfade_start'
        bpy.context.object.game.properties['colorfade_start'].type = 'FLOAT'
        bpy.context.object.game.properties['colorfade_start'].value = 1.0
        
        ### particle color fade end
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'colorfade_end'
        bpy.context.object.game.properties['colorfade_end'].type = 'FLOAT'
        bpy.context.object.game.properties['colorfade_end'].value = 1.0
        
        ### particle startspeed
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'startspeed'
        bpy.context.object.game.properties['startspeed'].type = 'FLOAT'
        bpy.context.object.game.properties['startspeed'].value = 0.0
        
        ### particle endspeed
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'endspeed'
        bpy.context.object.game.properties['endspeed'].type = 'FLOAT'
        bpy.context.object.game.properties['endspeed'].value = 0.1
        
        ### particle random movemen
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'randomMovement'
        bpy.context.object.game.properties['randomMovement'].type = 'FLOAT'
        bpy.context.object.game.properties['randomMovement'].value = 0.0
        
        ### particle startscale
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'startscale_x'
        bpy.context.object.game.properties['startscale_x'].type = 'FLOAT'
        bpy.context.object.game.properties['startscale_x'].value = 1.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'startscale_y'
        bpy.context.object.game.properties['startscale_y'].type = 'FLOAT'
        bpy.context.object.game.properties['startscale_y'].value = 1.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'startscale_z'
        bpy.context.object.game.properties['startscale_z'].type = 'FLOAT'
        bpy.context.object.game.properties['startscale_z'].value = 1.0
        
        ### particle endscale
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'endscale_x'
        bpy.context.object.game.properties['endscale_x'].type = 'FLOAT'
        bpy.context.object.game.properties['endscale_x'].value = 0.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'endscale_y'
        bpy.context.object.game.properties['endscale_y'].type = 'FLOAT'
        bpy.context.object.game.properties['endscale_y'].value = 0.0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'endscale_z'
        bpy.context.object.game.properties['endscale_z'].type = 'FLOAT'
        bpy.context.object.game.properties['endscale_z'].value = 0.0
        
        ### particle randomscale
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'randomscale'
        bpy.context.object.game.properties['randomscale'].type = 'FLOAT'
        bpy.context.object.game.properties['randomscale'].value = 1.0
        
        ### particle scalefade_start
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'scalefade_start'
        bpy.context.object.game.properties['scalefade_start'].type = 'INT'
        bpy.context.object.game.properties['scalefade_start'].value = 1.0
        
        ### particle scalefade_end
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'scalefade_end'
        bpy.context.object.game.properties['scalefade_end'].type = 'INT'
        bpy.context.object.game.properties['scalefade_end'].value = 1.0
        
        ### particle speedfade_start
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'speedfade_start'
        bpy.context.object.game.properties['speedfade_start'].type = 'INT'
        bpy.context.object.game.properties['speedfade_start'].value = 1.0
        
        ### particle speedfade_end
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'speedfade_end'
        bpy.context.object.game.properties['speedfade_end'].type = 'INT'
        bpy.context.object.game.properties['speedfade_end'].value = 1.0
    
        ### particle cone emission
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'coneX'
        bpy.context.object.game.properties['coneX'].type = 'FLOAT'
        bpy.context.object.game.properties['coneX'].value = 0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'coneY'
        bpy.context.object.game.properties['coneY'].type = 'FLOAT'
        bpy.context.object.game.properties['coneY'].value = 0
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'coneZ'
        bpy.context.object.game.properties['coneZ'].type = 'FLOAT'
        bpy.context.object.game.properties['coneZ'].value = 0
        
        ### particle fade in/out
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'fadein'
        bpy.context.object.game.properties['fadein'].type = 'INT'
        bpy.context.object.game.properties['fadein'].value = 10
        
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'fadeout'
        bpy.context.object.game.properties['fadeout'].type = 'INT'
        bpy.context.object.game.properties['fadeout'].value = 30
        
        ### particle rotation speed
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'rotation'
        bpy.context.object.game.properties['rotation'].type = 'FLOAT'
        bpy.context.object.game.properties['rotation'].value = 0
        
        ### particle halo -> particle is facing to camera
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'halo'
        bpy.context.object.game.properties['halo'].type = 'BOOL'
        bpy.context.object.game.properties['halo'].value = 1
        
        ### kill the emitter
        bpy.ops.object.game_property_new()
        bpy.context.object.game.properties['prop'].name = 'kill'
        bpy.context.object.game.properties['kill'].type = 'BOOL'
        bpy.context.object.game.properties['kill'].value = 0       
        
    def execute(self, context):
        active_ob = bpy.context.active_object

        self.gen_particle_logic(context)
        self.gen_properties(context)
        bpy.context.object.particlesystem = True
        
        try:
            material = bpy.context.active_object.material_slots['Emitter']
        except:
            # The material does not exist yet, so we need to generate it
            for x in bpy.data.materials:
                if x.name == 'Emitter':
                    self.emitter_mat = True
            if self.emitter_mat == False:
                self.createMaterial('Emitter')
            if self.emitter_mat == True:
                bpy.context.active_object.data.materials.append(bpy.data.materials['Emitter'])
        
        # Look if exist at least one particle type, creating the default
        # particles otherwise
        for x in bpy.data.scenes[0].objects:
            if x.particle == True:
                self.particle = True
        if self.particle == False:
            print("Info: No particles to use, the default ones will be generated")
            bpy.ops.scene.create_default_particle()
            bpy.ops.object.add(type='EMPTY', view_align=False,
                               enter_editmode=False, location=(0, -2, 0),
                               rotation=(0, 0, 0),
                               layers=(False, False, False, False, False,
                                       False, False, False, False, False,
                                       False, False, False, False, False,
                                       False, False, False, False, True))
            bpy.context.active_object.name = 'ParticleParent'
        
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = active_ob
        bpy.context.scene.objects[active_ob.name].select = True
        
        try:
            bpy.ops.scene.apply_preset()
        except:
            self.report("Warning: No presets to apply")
        bpy.ops.object.apply_values()
        
        self.report({'INFO'}, "Particle System added!")
        return{'FINISHED'}


class delete_particle_system(bpy.types.Operator):
    bl_idname = "object.delete_particle_system" 
    bl_label = "Delete the particle system"
    bl_description = "Delete the particle system (the object will not be removed)"
    
    def del_particle_logic(self,context):
        for x in range(0,len(bpy.context.object.game.properties)):
            bpy.ops.object.game_property_remove(index=0)
        bpy.ops.logic.sensor_remove(sensor="Always", object=bpy.context.active_object.name)
        bpy.ops.logic.controller_remove(controller="Python", object=bpy.context.active_object.name)
        bpy.ops.logic.controller_remove(controller="Reference", object=bpy.context.active_object.name)
        
    def execute(self, context):
        bpy.context.active_object.draw_type = 'TEXTURED'
        self.del_particle_logic(context)
        bpy.context.object.particlesystem = False
        self.report({'INFO'}, "Particle System deleted!")
        return{'FINISHED'}

class apply_values(bpy.types.Operator):
    bl_idname = "object.apply_values" 
    bl_label = "Apply the values to the particle system"
    
    def execute(self, context):
        try:
            bpy.context.object.game.properties['culling'].value = bpy.context.object.frustumCulling
            bpy.context.object.game.properties['cullingRadius'].value = bpy.context.object.frustumRadius
            
            bpy.context.object.game.properties['start_r'].value = bpy.context.object.startcolor[0]
            bpy.context.object.game.properties['start_g'].value = bpy.context.object.startcolor[1]
            bpy.context.object.game.properties['start_b'].value = bpy.context.object.startcolor[2]
            
            bpy.context.object.game.properties['end_r'].value = bpy.context.object.endcolor[0]
            bpy.context.object.game.properties['end_g'].value = bpy.context.object.endcolor[1]
            bpy.context.object.game.properties['end_b'].value = bpy.context.object.endcolor[2]
            
            bpy.context.object.game.properties['alpha'].value = bpy.context.object.alpha
    
            bpy.context.object.game.properties['colorfade_start'].value = bpy.context.object.colorfade_start
            bpy.context.object.game.properties['colorfade_end'].value = bpy.context.object.colorfade_end
            
            bpy.context.object.game.properties['emitteron'].value = bpy.context.object.emitteron
            bpy.context.object.game.properties['emitTime'].value = bpy.context.object.emitTime
            bpy.context.object.game.properties['lifetime'].value = bpy.context.object.lifetime
            bpy.context.object.game.properties['randomlifetimevalue'].value = bpy.context.object.randomlifetimevalue
            bpy.context.object.game.properties['amount'].value = bpy.context.object.amount
            
            bpy.context.object.game.properties['startscale_x'].value = bpy.context.object.startscale
            bpy.context.object.game.properties['startscale_y'].value = bpy.context.object.startscale
            bpy.context.object.game.properties['startscale_z'].value = bpy.context.object.startscale
            
            bpy.context.object.game.properties['endscale_x'].value = bpy.context.object.endscale
            bpy.context.object.game.properties['endscale_y'].value = bpy.context.object.endscale
            bpy.context.object.game.properties['endscale_z'].value = bpy.context.object.endscale
            
            bpy.context.object.game.properties['rangeEmitX'].value = bpy.context.object.rangeEmit[0]
            bpy.context.object.game.properties['rangeEmitY'].value = bpy.context.object.rangeEmit[1]
            bpy.context.object.game.properties['rangeEmitZ'].value = bpy.context.object.rangeEmit[2]
            bpy.context.active_object.dimensions = bpy.context.object.rangeEmit*2 + mathutils.Vector((1,1,1))
    
            
            bpy.context.object.game.properties['scalefade_start'].value = bpy.context.object.scalefade_start
            bpy.context.object.game.properties['scalefade_end'].value = bpy.context.object.scalefade_end
            bpy.context.object.game.properties['speedfade_start'].value = bpy.context.object.speedfade_start
            bpy.context.object.game.properties['speedfade_end'].value = bpy.context.object.speedfade_end
            
            bpy.context.object.game.properties['startspeed'].value = bpy.context.object.startspeed
            bpy.context.object.game.properties['endspeed'].value = bpy.context.object.endspeed
            bpy.context.object.game.properties['randomMovement'].value = bpy.context.object.randomMovement
            
            bpy.context.object.game.properties['coneX'].value = bpy.context.object.cone[0]
            bpy.context.object.game.properties['coneY'].value = bpy.context.object.cone[1]
            bpy.context.object.game.properties['coneZ'].value = bpy.context.object.cone[2]
            
            bpy.context.object.game.properties['fadein'].value = bpy.context.object.fadein
            bpy.context.object.game.properties['fadeout'].value = bpy.context.object.fadeout
            
            bpy.context.object.hide_render = bpy.context.object.emitterinvisible
            
            bpy.context.object.game.properties['localEmit'].value = bpy.context.object.localEmit
            
            bpy.context.object.game.properties['rotation'].value = bpy.context.object.particlerotation
            bpy.context.object.game.properties['halo'].value = bpy.context.object.halo
            #bpy.context.object.particle_list[bpy.context.object.particle_list_index].name = bpy.context.scene.particles
        except:
            pass
        self.report({'INFO'}, "Changes applied!")
        
        
        for i in bpy.context.object.particle_list:
            try:
                if bpy.data.materials[i.name].game_settings.alpha_blend == 'ADD':
                    i.addmode = True
                else:
                    i.addmode = False
            except:
                self.report({'INFO'}, "No Particle found called:    " + "'"+i.name + "'")
        
        PARTICLES=[]
        SCALE=[]
        ADDMODE=[]
        for i in range(len(bpy.context.object.particle_list)):
            PARTICLES.append(bpy.context.object.particle_list[i].name)
            SCALE.append(bpy.context.object.particle_list[i].scale)
            ADDMODE.append(bpy.context.object.particle_list[i].addmode)
        bpy.context.object.game.properties['particleList'].value = str(PARTICLES)
        bpy.context.object.game.properties['particleScale'].value = str(SCALE)
        bpy.context.object.game.properties['particleAddMode'].value = str(ADDMODE)
        return {'FINISHED'}

class particle_list(bpy.types.PropertyGroup):
    def update_values(self, context):
        bpy.ops.object.apply_values()
    name = bpy.props.StringProperty(default="")
    scale = bpy.props.FloatProperty(default=1.0,update=update_values)
    addmode = bpy.props.BoolProperty(default=True)
    
class particle_to_list(bpy.types.Operator):
    bl_idname = "object.particle_to_list" 
    bl_label = "Send a particle to the available ones list"        
    
    def execute(self, context):
        item = bpy.context.object.particle_list.add()
        #item.name = bpy.context.scene.objects[int(bpy.context.scene.object_list[0])].name
        item.name = bpy.data.scenes[0].particles
        item.scale = 1.0
        item.addmode = True
        #print(bpy.context.object.particle_list)
        bpy.ops.object.apply_values()
        return{'FINISHED'}
    
class particle_from_list(bpy.types.Operator):
    bl_idname = "object.particle_from_list" 
    bl_label = "Remove a particle from the available ones list"
    
    def __init__(self):
        pass
    
    def execute(self, context):
        bpy.ops.object.apply_values()
        item = bpy.context.object.particle_list.remove(bpy.context.object.particle_list_index)
        #print(bpy.context.object.particle_list)
        bpy.ops.object.apply_values()
        return{'FINISHED'}
    
class add_to_particle_list(bpy.types.Operator):
    bl_idname = "object.add_to_particle_list" 
    bl_label = "Add the particle to the list"
    
    def __init__(self):
        self.PARTICLE_NAMES = []
        self.current_ob = bpy.context.active_object
    
    def execute(self, context):
        try:
            bpy.context.active_object.data.materials[0].use_object_color = True
            scene = bpy.data.scenes[0].name
            self.current_ob.particle = True
            
            for x in bpy.data.scenes[scene].objects:
                bpy.data.scenes[scene].objects.active = x
                ob = bpy.context.active_object
                if ob.particle == True:
                    name = ob.name
                    self.PARTICLE_NAMES.append((name,name,name))
                    #print(name)
            
            self.PARTICLE_NAMES.sort()
            bpy.types.Scene.particles = bpy.props.EnumProperty(
            items = self.PARTICLE_NAMES,
            name = "choose a Particle")
            bpy.data.scenes[scene].objects.active = self.current_ob
        except:
            self.report({'WARNING'}, "Particle has no Material!")
        return{'FINISHED'}

class remove_from_particle_list(bpy.types.Operator):
    bl_idname = "object.remove_from_particle_list" 
    bl_label = "Remove a particle from the list"
    
    def __init__(self):
        self.PARTICLE_NAMES = []
        self.current_ob = bpy.context.active_object
    
    def execute(self, context):
        scene = bpy.data.scenes[0].name     
        self.current_ob.particle = False

        for x in bpy.data.scenes[scene].objects:
            ob = bpy.context.active_object
            bpy.data.scenes[scene].objects.active = x
            if ob.particle == True:
                name = ob.name
                self.PARTICLE_NAMES.append((name,name,name))
                #print(name)
        bpy.types.Scene.particles = bpy.props.EnumProperty(
        items = self.PARTICLE_NAMES,
        name = "choose a Particle")
        bpy.data.scenes[scene].objects.active = self.current_ob
        return{'FINISHED'}

class update_particle_list(bpy.types.Operator):
    bl_idname = "scene.update_particle_list" 
    bl_label = "Update the particle list"
    
    def __init__(self):
        self.PARTICLE_NAMES = []
        self.current_ob = bpy.context.active_object
    
    def execute(self, context):
        scene = bpy.data.scenes[0].name

        for x in bpy.data.scenes[scene].objects:
            ob = bpy.context.active_object
            bpy.data.scenes[scene].objects.active = x
            if ob.particle == True:
                name = ob.name
                self.PARTICLE_NAMES.append((name,name,name))
        bpy.types.Scene.particles = bpy.props.EnumProperty(
            items = self.PARTICLE_NAMES,
            name = "choose a Particle")
        bpy.data.scenes[scene].objects.active = self.current_ob
        return{'FINISHED'}

class create_default_particle(bpy.types.Operator):
    bl_idname = "scene.create_default_particle"
    bl_label = "Create the default particles"
    
    def loadScript(self):
        filepath = None
        for folder in addons_paths():
            f = path.join(folder, "sssEmit/emitter.py")
            if not path.isfile(f):
                continue
            filepath = f
            break
        if not filepath:
            raise Exception('I can not find the script file "emitter.py"')
        bpy.ops.text.open(filepath=filepath,
                          filter_blender=False,
                          filter_image=False,
                          filter_movie=False,
                          filter_python=True,
                          filter_font=False,
                          filter_sound=False,
                          filter_text=True,
                          filter_btx=False,
                          filter_collada=False,
                          filter_folder=True,
                          filemode=9,
                          internal=True)
    
    def createParticle(self,name,nameNew,position,shape_type,shadeless,addmode):
        scene_layers = bpy.data.scenes[0].layers[:]
        bpy.data.scenes[0].layers[19] = True
        for i in range(0,19):
            bpy.data.scenes[0].layers[i] = False
        if shape_type == 'Plane' or shape_type == 'PlaneShaded':
            bpy.ops.mesh.primitive_plane_add(view_align=False,
                enter_editmode=False, location=(0, position, 0),
                rotation=(0, 0, 0),
                layers=(bpy.data.scenes[0].layers[0],
                        bpy.data.scenes[0].layers[1],
                        bpy.data.scenes[0].layers[2],
                        bpy.data.scenes[0].layers[3],
                        bpy.data.scenes[0].layers[4],
                        bpy.data.scenes[0].layers[5],
                        bpy.data.scenes[0].layers[6],
                        bpy.data.scenes[0].layers[7],
                        bpy.data.scenes[0].layers[8],
                        bpy.data.scenes[0].layers[9],
                        bpy.data.scenes[0].layers[10],
                        bpy.data.scenes[0].layers[11],
                        bpy.data.scenes[0].layers[12],
                        bpy.data.scenes[0].layers[13],
                        bpy.data.scenes[0].layers[14],
                        bpy.data.scenes[0].layers[15],
                        bpy.data.scenes[0].layers[16],
                        bpy.data.scenes[0].layers[17],
                        bpy.data.scenes[0].layers[18],
                        bpy.data.scenes[0].layers[19]))
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.flip_normals()
            bpy.ops.object.mode_set(mode = 'OBJECT')
        elif shape_type == 'Volume':
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, size=1,
                view_align=False, enter_editmode=False,
                location=(0, position, 0), rotation=(0, 0, 0),
                layers=(bpy.data.scenes[0].layers[0],
                        bpy.data.scenes[0].layers[1],
                        bpy.data.scenes[0].layers[2],
                        bpy.data.scenes[0].layers[3],
                        bpy.data.scenes[0].layers[4],
                        bpy.data.scenes[0].layers[5],
                        bpy.data.scenes[0].layers[6],
                        bpy.data.scenes[0].layers[7],
                        bpy.data.scenes[0].layers[8],
                        bpy.data.scenes[0].layers[9],
                        bpy.data.scenes[0].layers[10],
                        bpy.data.scenes[0].layers[11],
                        bpy.data.scenes[0].layers[12],
                        bpy.data.scenes[0].layers[13],
                        bpy.data.scenes[0].layers[14],
                        bpy.data.scenes[0].layers[15],
                        bpy.data.scenes[0].layers[16],
                        bpy.data.scenes[0].layers[17],
                        bpy.data.scenes[0].layers[18],
                        bpy.data.scenes[0].layers[19]))
            bpy.ops.object.shade_smooth()
            
        bpy.context.active_object.game.physics_type = 'NO_COLLISION'
        bpy.context.active_object.name = nameNew
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.uv.unwrap(method='ANGLE_BASED', fill_holes=True, correct_aspect=True)
        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0),
                                 constraint_axis=(False, True, False),
                                 constraint_orientation='GLOBAL',
                                 mirror=False, proportional='DISABLED',
                                 proportional_edit_falloff='SMOOTH',
                                 proportional_size=1, snap=False,
                                 snap_target='CLOSEST', snap_point=(0, 0, 0),
                                 snap_align=False, snap_normal=(0, 0, 0),
                                 release_confirm=False)
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        mat = bpy.data.materials.new(nameNew)
        if shadeless == True:
            mat.use_shadeless = True
            mat.game_settings.use_backface_culling = True
        if addmode == True:
            mat.diffuse_color = (0,0,0)
            mat.game_settings.alpha_blend = 'ADD'
            mat.game_settings.use_backface_culling = False
        else:
            mat.diffuse_color = (0,0,0)
        mat.use_object_color = True
        
        bpy.context.active_object.data.materials.append(mat)

        img = None
        for folder in addons_paths():
            filepath = path.join(folder, "sssEmit/images", name+".png")
            try:
                img = bpy.data.images.load(filepath)
            except:
                continue
            break
        if not img:
            raise Exception('I can not find the image file "{0}"'.format(name+".png"))
        img.pack()
        img.use_alpha = True
        
        cTex = bpy.data.textures.new(nameNew, type = 'IMAGE')
        cTex.image = img
        
        mtex = mat.texture_slots.add()
        mtex.texture = cTex
        mtex.use_stencil = True
        if shape_type == 'Plane':
            mtex.use_map_color_diffuse = True 
            mtex.use_map_alpha = True
            mtex.texture_coords = 'UV'
        elif shape_type == 'Volume':
            mtex.texture_coords = 'NORMAL'
            mat.use_transparency = True
            mat.alpha = 0.0
            mtex.use_map_alpha = True
            #mtex.use_rgb_to_intensity = True
            mtex.use_map_color_diffuse = False
        elif shape_type == 'PlaneShaded':
            mat.game_settings.use_backface_culling = False
            mtex.texture_coords = 'UV'
            mat.use_transparency = True
            mat.alpha = 0.0
            mtex.use_map_alpha = True
            #mtex.use_rgb_to_intensity = True
            mtex.use_map_color_diffuse = False
        
        mtex.diffuse_color_factor = 1.0 
        
        for x in bpy.context.active_object.layers:
            x = False
        bpy.context.active_object.layers[19] = True
        bpy.data.scenes[0].layers = scene_layers[:]
        bpy.ops.object.add_to_particle_list()
    
    def execute(self, context):
        self.createParticle('particle_smooth','Particle_Smooth',0,'Plane',True,True)
        self.createParticle('particle_hard','Particle_Hard',2,'Plane',True,True)
        self.createParticle('particle_scattered','Particle_Scattered',4,'Plane',True,True)
        self.createParticle('particle_fire','Particle_Fire',6,'Plane',True,True)
        self.createParticle('particle_star','Particle_Star',8,'Plane',True,True)
        self.createParticle('particle_blade','Particle_Blade',10,'Plane',True,True)
        self.createParticle('particle_smoke','Particle_Smoke',12,'Volume',False,False)
        self.createParticle('particle_smoke','Particle_Water',12,'PlaneShaded',False,False)
        self.loadScript()
        return{'FINISHED'}

