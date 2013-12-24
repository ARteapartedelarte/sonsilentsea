import bpy
import math
import mathutils
from bpy.props import BoolProperty

from sssEmit.preset import *
from sssEmit.particle import *

SSS_EMIT_MAJOR_VERSION = 0
SSS_EMIT_MINOR_VERSION = 3

bl_info = {
    "name": "SonSilentSea particles system",
    "author": "Andreas Esau, Jose Luis Cercos-Pita",
    "version": (0, 3),
    "blender": (2, 6, 9),
    "api": 60518,
    "location": "Properties > Particles",
    "description": "An Easy to use Particle System for the Blender Game Engine",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Game Engine"}

class sssEmitPresets(bpy.types.Panel):
    bl_label = "sssEmit Presets"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "particle"
    COMPAT_ENGINES = {'BLENDER_GAME'}

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        rd = context.scene.render
        return ob and ob.game and (rd.engine in cls.COMPAT_ENGINES)
    
    def draw(self, context):
        col = self.layout.column()
        row = self.layout.row()
        # split = self.layout.split()
        scene = bpy.data.scenes[0]
        obj = context.object
        scn = context.scene
        
        # The title
        row.label("Presets", icon='FILESEL')
        row = self.layout.row()

        # The list of presets
        row.template_list("UI_UL_list","dummy", scene, "preset", scene, "preset_index")

        # The operators
        col = row.column(align=True)
        col.operator("scene.add_preset", icon='ZOOMIN', text="")
        col.operator("scene.remove_preset", icon='ZOOMOUT', text="")
        col.operator("scene.init_preset", icon='RECOVER_LAST', text="")

        # Add
        try:
            preset = scn.preset[scn.preset_index]
            row = self.layout.row()
            row.prop(preset, "name", text="Name")
        except:
            pass
        row = self.layout.row()
        row.operator("export.load_preset",text="Import Particle Presets", icon='FILESEL') 
        row = self.layout.row()    
        row.operator("export.save_preset",text="Export Particle Presets", icon='FILESEL')      

class sssEmit(bpy.types.Panel):
    bl_label = "sssEmit"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "particle"
    COMPAT_ENGINES = {'BLENDER_GAME'}
    
    def update_values(self, context):
        bpy.ops.object.apply_values()
    
    bpy.types.Object.particlesystem = bpy.props.BoolProperty(default=False)
    bpy.types.Object.particle = bpy.props.BoolProperty(default=False)
    bpy.types.Object.frustumCulling = bpy.props.BoolProperty(default=True,
        update=update_values,
        description='Allows you to disable the Emitter automatically if it is not viewable!')
    bpy.types.Object.frustumRadius = bpy.props.IntProperty(default=4,
        min=1,
        update=update_values,
        description='Distance to the emmiter where it is considered viewable')
    
    bpy.types.Object.localEmit = bpy.props.BoolProperty(default=True,
        update=update_values,
        description='Particle is emitted global or local')
    
    bpy.types.Object.emitTime = bpy.props.IntProperty(name='',
        default=0,
        min=0,
        update=update_values,
        description='Emission Time. 0 to emit always')
    bpy.types.Object.amount = bpy.props.IntProperty(name='',
        default=10, 
        min=1,
        max=18000,
        update=update_values,
        description='Amount of Particles that are emitted in 60 Tics (1 Second)')
    bpy.types.Object.lifetime = bpy.props.IntProperty(name='',
        default=60,
        min=1,
        update=update_values,
        description='Particle Lifetime in tics (60 tics = 1 second)')
    bpy.types.Object.randomlifetimevalue = bpy.props.IntProperty(name='',
        default=0,
        min=0,
        update=update_values,
        description='Particle lifetime random variation')
    bpy.types.Object.emitteron = bpy.props.BoolProperty(name='',
        default=True,
        update=update_values,
        description='Switch on/off the emitter')
    bpy.types.Object.emitterinvisible = bpy.props.BoolProperty(name='',
        default=True,
        update=update_values,
        description='Sets the emitter itself visible or invisble in the Game')
    
    bpy.types.Object.cone = bpy.props.FloatVectorProperty(name='',
        default=(0.261800, 0.261800, 0.261800),
        precision=1,
        min=0,
        max=2*math.pi,
        subtype='EULER',
        update=update_values,
        description='Sperical Emission Range')
    bpy.types.Object.startscale = bpy.props.FloatProperty(name='',
        default=1.0,
        min=0,
        update=update_values,
        description='Particles scale on birth')
    bpy.types.Object.endscale = bpy.props.FloatProperty(name='',
        default=1.0,
        min=0,
        update=update_values,
        description='Particles scale on death')
    bpy.types.Object.scalefade_start = bpy.props.IntProperty(name='',
        default=1,
        min=1,
        update=update_values,
        description='Adjust the scale fading for the particle lifetime')
    bpy.types.Object.scalefade_end = bpy.props.IntProperty(name='',
        default=60,
        min=1,
        update=update_values,
        description='Adjust the scale fading for the particle lifetime')
    bpy.types.Object.speedfade_start = bpy.props.IntProperty(name='',
        default=1,
        min=1,
        update=update_values,
        description='Adjust the speed fading for the particle lifetime')
    bpy.types.Object.speedfade_end = bpy.props.IntProperty(name='',
        default=60,
        min=1,
        update=update_values,
        description='Adjust the speed fading for the particle lifetime')

    bpy.types.Object.ellipsoidalRange = bpy.props.BoolProperty(default=False,
        update=update_values,
        description='Force the particles to be generated inside the ellipsoide limited by emission range values, otherwise a cube will be considered')
    bpy.types.Object.rangeEmit = bpy.props.FloatVectorProperty(name='',
        default=(0.0, 0.0, 0.0),
        min=0,
        subtype='XYZ',
        update=update_values,
        description='Particle Emission Range')

    bpy.types.Object.startcolor = bpy.props.FloatVectorProperty(name='',
        default=(0.499987, 0.293760, 0.037733),
        min=0,
        max=1,
        step=1,
        precision=3,
        subtype='COLOR_GAMMA',
        size=3,
        update=update_values,
        description='Particle Start Color')
    bpy.types.Object.endcolor = bpy.props.FloatVectorProperty(name='',
        default=(0.506654, 0.000000, 0.011944),
        min=0,
        max=1,
        step=1,
        precision=3,
        subtype='COLOR_GAMMA',
        size=3,
        update=update_values,
        description='Particle End Color')
    bpy.types.Object.alpha = bpy.props.FloatProperty(name='',
        default=1.0,
        min=0,
        max=1,
        subtype='FACTOR',
        update=update_values,
        description='Particle Alpha Value')
    bpy.types.Object.colorfade_start = bpy.props.IntProperty(name='',
        default=1,
        min=1,
        update=update_values,
        description='Adjust the color fading for Particle Lifetime')
    bpy.types.Object.colorfade_end = bpy.props.IntProperty(name='',
        default=60,
        min=1,
        update=update_values,
        description='Adjust the color fading for Particle Lifetime')
    bpy.types.Object.fadein = bpy.props.IntProperty(name='',
        default=10,
        min=1,
        update=update_values,
        description='Particle Fade in time')
    bpy.types.Object.fadeout = bpy.props.IntProperty(name='',
        default=30,
        min=1,
        update=update_values,
        description='Particle Fade out time')
    
    bpy.types.Object.randomMovement = bpy.props.FloatProperty(name='',
        default=0,
        min=0.0,
        max=math.pi*2,
        subtype='ANGLE',
        update=update_values,
        description='Particle angular random motion')
    bpy.types.Object.startspeed = bpy.props.FloatProperty(name='',
        default=0.0,
        min=-100,
        max=100,
        update=update_values,
        description='Particle Startspeed')
    bpy.types.Object.startspeedRadial = bpy.props.StringProperty(name='',
        default='1',
        update=update_values,
        description='Normalized radial multiplier factor for the starting particles speed (for instance "(1 - r)**2.0")')

    modes = [('0', 'End speed', '0'),
             ('1', 'Gravity', '1')]
    bpy.types.Object.endspeed_mode = EnumProperty( name="Speed evolution mode",
        items=modes,
        default='0',
        update=update_values,
        description="Set the speed modifier")

    bpy.types.Object.endspeed = bpy.props.FloatProperty(name='',
        default=10,
        min=-100,
        max=100,
        update=update_values,
        description='Particle Endspeed')
    bpy.types.Object.endspeedRadial = bpy.props.StringProperty(name='',
        default='1',
        update=update_values,
        description='Normalized radial multiplier factor for the final particles speed (for instance "(1 - r)**2.0")')

    bpy.types.Object.particlerotation = bpy.props.FloatProperty(name='',
        default=0.0,
        min=0,
        max=math.pi*2,
        subtype='ANGLE',
        update=update_values,
        description='Particle Rotation')
    bpy.types.Object.halo = bpy.props.BoolProperty(default=True,
        update=update_values,
        description='Particle is Facing to the Camera')

    
    @classmethod
    def poll(cls, context):
        ob = context.active_object
        rd = context.scene.render
        return ob and ob.game and (rd.engine in cls.COMPAT_ENGINES)
    
    def draw(self, context):
        col = self.layout.column()
        row = self.layout.row()
        split = self.layout.split()
        scene = bpy.data.scenes[0]
        ob = context.object
        sce = context.scene
        version = '{0}.{1}'.format(
            SSS_EMIT_MAJOR_VERSION,
            SSS_EMIT_MINOR_VERSION)
        
        if bpy.context.object.particlesystem == True:
            need_reload = False
            text_reload = 'Reload'
            if('particles' not in bpy.types.Scene.__dict__.keys()):
                need_reload = True
                text_reload = 'Reload (Some data missed)'
            if('version' not in ob.game.properties.keys()):
                need_reload = True
                text_reload = 'Upgrade (0.0 -> {0})'.format(version)
            elif(ob.game.properties['version'].value != version):
                obj_ver = ob.game.properties['version'].value
                text_reload = 'Upgrade ({0} -> {1})'.format(obj_ver, version)
                if float(obj_ver) < float(version):
                    text_reload = 'Downgrade ({0} -> {1})'.format(obj_ver,
                        version)
                need_reload = True
            
            if(need_reload):
                row.operator("object.reload_upgrade",
                    icon='RECOVER_LAST',
                    text=text_reload)
                return

            # It is a particle system, display all the options
            row = self.layout.row()
            row.label("Emitter Settings", icon='GREASEPENCIL')
            
            row = self.layout.row()
            row.prop(context.object, "frustumCulling", text="Enable Frustum Culling")
            row.prop(context.object, "frustumRadius", text="Radius")
            
            row = self.layout.row()
            row.prop(context.object, "emitteron", text="Emitter On")
            row.prop(context.object, "emitterinvisible", text="Emitter Invisible")
            row = self.layout.row()
            row.prop(scene, 'particles', text='')
            row.operator("object.particle_to_list", icon='ZOOMIN', text="")
            row = self.layout.row()
            row.template_list("UI_UL_list","dummy",ob, "particle_list", ob, "particle_list_index")
            col = row.column(align=True)
            
            col.operator("object.particle_from_list", icon='ZOOMOUT', text="")
            
            try:
                row = self.layout.row(align=True)
                row.label("Particle Scale:")
                row.prop(context.object.particle_list[context.object.particle_list_index], 'scale', text='Scale')
            except:
                pass    
            
            row = self.layout.row()
            
            
            row.label("Emission Time:")
            row.prop(context.object, "emitTime", text="Tics")
            row = self.layout.row()
            row.label("Particle Lifetime:")
            row.prop(context.object, "lifetime", text="Tics")
            row = self.layout.row()
#            row.label("Particle Random Death:")
#            row.prop(context.object, "randomlifetimevalue", text="Tics")
#            row = self.layout.row()
            row.label("Emission Amount:")
            row.prop(context.object, "amount", text="Amount")
            
            
            row = self.layout.row()
            row.label("Spherical Emission:")
            row.column().prop(context.object, "cone", text="")
            row = self.layout.row()
            col = row.column()
            col.label("Emission Range:")
            col.prop(context.object, "ellipsoidalRange", text="as ellipsoide")
            col = row.column()
            col.prop(context.object, "rangeEmit", text="")
            
            row = self.layout.row()
            row.label("Color Settings", icon='COLOR')
            
            row = self.layout.row().column(align=True)
            row = self.layout.row()
            row.label("Start Color:")
            row.prop(context.object, "startcolor", text="")
            row = self.layout.row()
            row.label("End Color:")
            row.prop(context.object, "endcolor", text="")
            row = self.layout.row()
            row.label("Alpha Value:")
            row.prop(context.object, "alpha", text="")
            row = self.layout.row(align=True)
            row.label("Color Fading:")
            row.label("")
            row.prop(context.object, "colorfade_start", text="Start")
            row.prop(context.object, "colorfade_end", text="End")
            
            row = self.layout.row(align=True)
            row.label("Fade In/Out:")
            row.label("")
            row.prop(context.object, "fadein", text="In")
            row.prop(context.object, "fadeout", text="Out")
            row = self.layout.row()
            
            
            row = self.layout.row()
            row.label("Physics Settings",icon='MOD_ARRAY')
            row = self.layout.row()
            row.label("Particle Rotation:")
            row.prop(context.object, "particlerotation", text="Rotation Speed")
            row = self.layout.row()
            row.label("Start Speed:")
            row.prop(context.object, "startspeed", text="Start Speed")
            row.prop(context.object, "startspeedRadial", text="")
            
            row = self.layout.row()
            # row.label("End Speed:")
            row.prop(context.object, "endspeed_mode", text="")
            if(context.object.game.properties['endspeed_mode'].value == '0'):
                row.prop(context.object, "endspeed", text="End Speed")
                row.prop(context.object, "endspeedRadial", text="")
            else:
                row.prop(context.object, "endspeed", text="")
            
            row = self.layout.row(align=True)
            row.label("Speed Fading:")
            row.label("")
            row.prop(context.object, "speedfade_start", text="Start")
            if(context.object.game.properties['endspeed_mode'].value == '0'):
                row.prop(context.object, "speedfade_end", text="End")
            row = self.layout.row()
            row.label("Random Movement:")
            row.prop(context.object, "randomMovement", text="Random Movement")
            
            
            row = self.layout.row()
            row.label("Start Size:")
            row.column().prop(context.object, "startscale", text="Start Size")
            row = self.layout.row()
            row.label("End Size:")
            row.column().prop(context.object, "endscale", text="End Size")
            row = self.layout.row(align=True)
            row.label("Size Fading:")
            row.label("")
            row.prop(context.object, "scalefade_start", text="Start")
            row.prop(context.object, "scalefade_end", text="End")
            
            row = self.layout.row()
            row = self.layout.row()
            row = self.layout.row()
            row = self.layout.row()
            
            
            row = self.layout.row()
            row.operator("object.delete_particle_system",
                         text="Delete the particle system (the object will not be destroyed)",
                         icon='CANCEL')

        elif bpy.context.object.particle == False:
            # It is not a particle system, or a particle either, so
            # transforming it into a particles system can be offered
            row = self.layout.row()
            row.operator("scene.generate_particle_system",
                         text="Create a particle system",
                         icon='PARTICLES')
            # Also we can transform it into a new particle
            row = self.layout.row()
            row.operator("object.add_to_particle_list",
                         text="Create a new type of particle",
                         icon='PARTICLES')
        else:
            # It is a particle
            row = self.layout.row()
            row.operator("object.remove_from_particle_list",
                         text="Remove from the particles list",
                         icon='PARTICLES')

def register():
    # Presets
    bpy.utils.register_class(preset)
    bpy.types.Scene.preset = bpy.props.CollectionProperty(type=preset)
    bpy.types.Scene.preset_index = bpy.props.IntProperty()
    bpy.utils.register_class(init_presets)
    bpy.utils.register_class(add_preset)
    bpy.utils.register_class(apply_preset)
    bpy.utils.register_class(remove_preset)
    # Export/Import
    bpy.utils.register_class(save_preset)
    bpy.utils.register_class(load_preset)
    # Particles
    bpy.utils.register_class(particle_list)
    bpy.types.Object.particle_list = bpy.props.CollectionProperty(type=particle_list)
    bpy.types.Object.particle_list_index = bpy.props.IntProperty()
    bpy.utils.register_class(generate_particle_system)
    bpy.utils.register_class(delete_particle_system)
    bpy.utils.register_class(apply_values)
    bpy.utils.register_class(particle_to_list)
    bpy.utils.register_class(particle_from_list)
    bpy.utils.register_class(reload_upgrade)
    bpy.utils.register_class(load_script)
    bpy.utils.register_class(create_default_particle)
    bpy.utils.register_class(add_to_particle_list)
    bpy.utils.register_class(remove_from_particle_list)
    bpy.utils.register_class(update_particle_list)
    # GUI
    bpy.utils.register_class(sssEmitPresets)
    bpy.utils.register_class(sssEmit)

def unregister():
    # Presets
    bpy.utils.unregister_class(preset)
    bpy.utils.unregister_class(init_presets)
    bpy.utils.unregister_class(add_preset)
    bpy.utils.unregister_class(apply_preset)
    bpy.utils.unregister_class(remove_preset)
    # Export/Import
    bpy.utils.unregister_class(save_preset)
    bpy.utils.unregister_class(load_preset)
    # Particles
    bpy.utils.unregister_class(particle_list)
    bpy.utils.unregister_class(generate_particle_system)
    bpy.utils.unregister_class(delete_particle_system)
    bpy.utils.unregister_class(apply_values)
    bpy.utils.unregister_class(particle_to_list)
    bpy.utils.unregister_class(particle_from_list)
    bpy.utils.unregister_class(reload_upgrade)
    bpy.utils.unregister_class(load_script)
    bpy.utils.unregister_class(create_default_particle)
    bpy.utils.unregister_class(add_to_particle_list)
    bpy.utils.unregister_class(remove_from_particle_list)
    bpy.utils.unregister_class(update_particle_list)
    # GUI
    bpy.utils.unregister_class(sssEmitPresets)
    bpy.utils.unregister_class(sssEmit)

if __name__ == "__main__":
    register()

