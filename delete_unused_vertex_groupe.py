import bpy
from bpy.types import Menu, Panel, UIList
from rna_prop_ui import PropertyPanel

## ウエイト０の頂点グループを削除
## ミラーモディファイアに対応するために左右どちらかにウエイトがあれば残す。

bl_info = {
    "name": "ウエイト０の頂点グループを削除",
    "author": "Aobayu",
    "version": (0, 0),
    "blender": (2, 81, 0),
    "location": "PROPATY > WINDOW > DATA",
    "description": "ウエイト０の頂点グループを削除",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "User Interface"
}


class MYADDON_PT_DeleteUnusedVertexGroupUI(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_label = "頂点グループ操作"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    @classmethod
    def poll(cls, context):
        engine = context.engine
        return context.mesh and (engine in cls.COMPAT_ENGINES)
        
    def draw(self, context):
        
        layout = self.layout
        row = layout.row()
        
        # row.operator("object.select_all").action = 'INVERT'
        row.operator(MYADDON_OP_DeleteUnusedVertexGroup.bl_idname, text = "ウエイト0の頂点グループを削除")


class MYADDON_OP_DeleteUnusedVertexGroup(bpy.types.Operator):
    bl_idname = "button.deleteunusedvertexgroup"
    bl_label = "deleteUnusedVertexGroup"

    mirroredNameMap = {"L": "R", "R":"L", "l": "r", "r": "l"}
        
    def execute(self, context):
        self.mainprocess(context)
        return {'FINISHED'}

    ### 以下、参考　https://scrapbox.io/keroxp/Blender%E3%81%A7%E3%82%A6%E3%82%A7%E3%82%A4%E3%83%88%E3%81%AE%E3%81%AA%E3%81%84%E9%A0%82%E7%82%B9%E3%82%B0%E3%83%AB%E3%83%BC%E3%83%97%E3%82%92%E3%81%99%E3%81%B9%E3%81%A6%E5%89%8A%E9%99%A4%E3%81%99%E3%82%8B
    def survey(self, obj):
        maxWeight = {}
        nameByIndex = {}
        indexByName = {}
        for vg in obj.vertex_groups:
            maxWeight[vg.index] = 0
            nameByIndex[vg.index] = vg.name;
            indexByName[vg.name] = vg.index;
        for v in obj.data.vertices:
            for g in v.groups:
                gn = g.group
                w = obj.vertex_groups[g.group].weight(v.index)
                if (maxWeight.get(gn) is None or w > maxWeight[gn]):
                    maxWeight[gn] = w
        return maxWeight, nameByIndex, indexByName
     # bone_name.(l|L) <-> bone_name.(r|R)
    
    def getMirroredName(self, name):
        prefix = self.mirroredNameMap.get(name[-1])
        return name[0:-1]+prefix if prefix is not None else name
    
    def mainprocess(self, context):
        obj = bpy.context.active_object
        maxWeight, nameByIndex, indexByName = self.survey(obj)
        print(indexByName)
        ka = []
        ka.extend(maxWeight.keys())
        ka.sort(key=lambda gn: -gn)
        removalFlags = {}
        for gn in ka:
            if removalFlags.get(gn) is not None:
                continue
            removalFlags[gn] = maxWeight[gn] <= 0
            group_name = nameByIndex[gn]
            mirror = self.getMirroredName(group_name)
            mirror_index = indexByName.get(mirror)
            if mirror_index is not None:
                if removalFlags.get(mirror_index) is None:
                    removalFlags[gn] = maxWeight[gn] <= 0
                if maxWeight[gn] > 0 or maxWeight[mirror_index] > 0:
                    removalFlags[gn] = removalFlags[mirror_index] = False
            else:
                removalFlags[gn] = maxWeight[gn] <= 0
        for gn in ka:
            if removalFlags[gn]:
                obj.vertex_groups.remove(obj.vertex_groups[gn])
                print ("deleted: "+nameByIndex[gn])



        
        
classes = [
    MYADDON_PT_DeleteUnusedVertexGroupUI,
    MYADDON_OP_DeleteUnusedVertexGroup
]
        
# register
def register():
    for c in classes:
        bpy.utils.register_class(c)
    print("MyAddon: アドオン『StorageSelection』が有効化されました。")


# unregister
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    print("MyAddon: アドオン『StorageSelection』が無効化されました。")


#
# AddOn Entry
#
if __name__ == "__main__":
  register()