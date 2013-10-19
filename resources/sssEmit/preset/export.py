import bpy
import math
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty

class ExportSomeData(bpy.types.Operator):
    """Test exporter which just writes hello world"""
    bl_idname = "export.some_data"
    bl_label = "Export Some Data"

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        return context.object is not None


    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class save_preset(bpy.types.Operator, ExportHelper):
    bl_idname = "export.save_preset" 
    bl_label = "Export the presets to a text file"
    bl_description="Save all the active particle presets to a text file"
    
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    filename_ext = ".eep"
    filter_glob = StringProperty(default="*.eep", options={'HIDDEN'})

    def __init__(self):
        self.data = []

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def generate_list(self):
        presets = bpy.data.scenes[0].preset
        for preset in presets:
            particleDict = dict()
            particleDict['addmode'] = preset.addmode
            particleDict['alpha'] = preset.alpha
            particleDict['amount'] = preset.amount
            particleDict['colorfade_start'] = preset.colorfade_start
            particleDict['colorfade_end'] = preset.colorfade_end
            particleDict['coneX'] = preset.cone[0]
            particleDict['coneY'] = preset.cone[1]
            particleDict['coneZ'] = preset.cone[2]
            particleDict['emitTime'] = preset.emitTime
            particleDict['endcolorR'] = preset.endcolor[0]
            particleDict['endcolorG'] = preset.endcolor[1]
            particleDict['endcolorB'] = preset.endcolor[2]
            particleDict['endscale'] = preset.endscale
            particleDict['endspeed'] = preset.endspeed
            particleDict['fadein'] = preset.fadein
            particleDict['fadeout'] = preset.fadeout
            particleDict['lifetime'] = preset.lifetime
            particleDict['name'] = preset.name
            particleDict['particlerotation'] = preset.particlerotation
            particleDict['particles'] = preset.particles
            particleDict['particlesScale'] = preset.particlesScale
            particleDict['randomMovement'] = preset.randomMovement
            particleDict['randomlifetimevalue'] = preset.randomlifetimevalue
            particleDict['rangeEmitX'] = preset.rangeEmit[0]
            particleDict['rangeEmitY'] = preset.rangeEmit[1]
            particleDict['rangeEmitZ'] = preset.rangeEmit[2]
            particleDict['scalefade_end'] = preset.scalefade_end
            particleDict['scalefade_start'] = preset.scalefade_start
            particleDict['speedfade_end'] = preset.speedfade_end
            particleDict['speedfade_start'] = preset.speedfade_start
            particleDict['startcolorR'] = preset.startcolor[0]
            particleDict['startcolorG'] = preset.startcolor[1]
            particleDict['startcolorB'] = preset.startcolor[2]
            particleDict['startscale'] = preset.startscale
            particleDict['startspeed'] = preset.startspeed
            self.data.append(particleDict)
            
    def save_preset(self, data, filepath):
        f = open(filepath, "w")
        for preset in data:
            f.write('preset{\n')
            for field in preset:
                f.write('\t{0} = {1} {2};\n'.format(field, type(preset[field]), preset[field]))
            f.write('};\n')
        f.close()
        return {'FINISHED'}
    
    def execute(self, context):
        self.generate_list()
        return self.save_preset(self.data,self.filepath)

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
class load_preset(bpy.types.Operator, ExportHelper):
    bl_idname = "export.load_preset" 
    bl_label = "import Preset"
    bl_description="Load Particle Presets"
    
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    filename_ext = ".eep"
    filter_glob = StringProperty(default="*.eep",options={'HIDDEN'})
    
    def __init__(self):
        self.data = []
    
    def load_preset(self,filepath):
        f = open(filepath, "r")
        text = f.read()
        f.close()
        # Remove all the spaces, tabulators and line breaks
        text = text.replace(' ', '')
        text = text.replace('\t', '')
        text = text.replace('\n', '')
        # Look for preset sections
        while text.find('preset{') != -1:
            begin = text.find('preset{') + len('preset{')
            end = text.find('};')
            if end == -1:
                raise Exception('Unclosed preset section')
            preset = text[begin:end]
            text = text[end + len('};'):]
            # Get the data fields
            particleDict = dict()
            fields = preset.split(';')
            for field in fields:
                if field == '':
                    continue
                # Name and value
                name,value = field.split('=')
                # type and value
                begin = value.find('<') + len('<')
                end = value.find('>')
                if (begin == -1) or (end == '-1'):
                    raise Exception('Value specified without a class identifier')
                vtype = value[begin:end]
                value = value[end+len('>'):]
                # Decript the value using the type
                if vtype == "class'str'":
                    pass
                elif vtype == "class'int'":
                    value = int(value)
                elif vtype == "class'float'":
                    value = float(value)
                else:
                    raise Exception('Invalid class "{0}"'.format(vtype))
                # And store it
                particleDict[name] = value
            self.data.append(particleDict)
        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        self.load_preset(self.filepath)
        for particleDict in self.data:
            # Look for the existing item
            item = None
            for it in bpy.context.scene.preset:
                if it.name == particleDict['name']:
                    item = it
                    break
            if item == None:
                item = bpy.data.scenes[0].preset.add()
            item.addmode = particleDict['addmode']
            item.alpha = particleDict['alpha']
            item.amount = particleDict['amount']
            item.colorfade_start = particleDict['colorfade_start']
            item.colorfade_end = particleDict['colorfade_end']
            item.cone[0] = particleDict['coneX']
            item.cone[1] = particleDict['coneY']
            item.cone[2] = particleDict['coneZ']
            item.emitTime = particleDict['emitTime']
            item.endcolor[0] = particleDict['endcolorR']
            item.endcolor[1] = particleDict['endcolorG']
            item.endcolor[2] = particleDict['endcolorB']
            item.endscale = particleDict['endscale']
            item.endspeed = particleDict['endspeed']
            item.fadein = particleDict['fadein']
            item.fadeout = particleDict['fadeout']
            item.lifetime = particleDict['lifetime']
            item.name = particleDict['name']
            item.particlerotation = particleDict['particlerotation']
            item.particles = particleDict['particles']
            item.particlesScale = particleDict['particlesScale']
            item.randomMovement = particleDict['randomMovement']
            item.randomlifetimevalue = particleDict['randomlifetimevalue']
            item.rangeEmit[0] = particleDict['rangeEmitX']
            item.rangeEmit[1] = particleDict['rangeEmitY']
            item.rangeEmit[2] = particleDict['rangeEmitZ']
            item.scalefade_end = particleDict['scalefade_end']
            item.scalefade_start = particleDict['scalefade_start']
            item.speedfade_end = particleDict['speedfade_end']
            item.speedfade_start = particleDict['speedfade_start']
            item.startcolor[0] = particleDict['startcolorR']
            item.startcolor[1] = particleDict['startcolorG']
            item.startcolor[2] = particleDict['startcolorB']
            item.startscale = particleDict['startscale']
            item.startspeed = particleDict['startspeed']
        self.report({'INFO'}, "easyEmit Preset imported!")
        return{'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

