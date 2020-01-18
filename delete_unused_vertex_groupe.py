import bpy
from bpy.types import Menu, Panel, UIList
from rna_prop_ui import PropertyPanel

class MeshButtonsPanel:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        engine = context.engine
        return context.mesh and (engine in cls.COMPAT_ENGINES)


class DATA_PT_uv_texture(MeshButtonsPanel, Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_label = "TEST"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw(self, context):
        self.layout.label(text="Hello World")
        
        
bpy.utils.register_class(DATA_PT_uv_texture)