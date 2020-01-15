# アドオンについての説明
bl_info = {
    "name": "StorageSelection",
    "author": "oba315",
    "version": (0, 0),
    "blender": (2, 81, 0),
    "location": "",
    "description": "sample",
    "support": "TESTING",
    "wiki_url": "http://hogehoge.com",
    "tracker_url": "http://hogehoge2.com",
    "category": "Object"
}

# 可能な拡張
# 辺、面選択モードへの対応
# 選択記憶をオブジェクト単位にするか？
# 頂点番号がはみ出したときのエラー処理

import bpy
from bpy.props import ( IntProperty )


def storage_selection_func(index):
    
    # なぜかエディットモードを出ないと更新されない
    obj = bpy.context.active_object
    old_mode = obj.mode
    bpy.ops.object.mode_set(mode='OBJECT')
        
    selected = [v.index for v in obj.data.vertices if v.select]
    print(selected)
    
    # とりあえずシーンにカスタムプロパティを作るけどオブジェクトに作ったほうがいいかも？
    scene = bpy.context.scene
    scene["storage_selection_"+str(index)] = selected
    
    bpy.ops.object.mode_set(mode=old_mode)

def call_selection_func(index):
    
    obj = bpy.context.active_object
    old_mode = obj.mode
    
    bpy.ops.object.mode_set(mode="EDIT") #Activating Editmode
    bpy.ops.mesh.select_all(action='DESELECT')
    
    bpy.ops.object.mode_set(mode='OBJECT')    
    for p in bpy.context.scene["storage_selection_"+str(index)] :
        obj.data.vertices[p].select = True
        
    bpy.ops.object.mode_set(mode=old_mode)



class MYADDON_OP_StorageSelection1(bpy.types.Operator):
    bl_idname = "buttons.storageslection1"     # 必須
    bl_label = "StorageSelection"             # 必須
    def execute(self, context):
        storage_selection_func(1)
        return {'FINISHED'}
    
class MYADDON_OP_StorageSelection2(bpy.types.Operator):
    bl_idname = "buttons.storageslection2"     # 必須
    bl_label = "StorageSelection"             # 必須
    def execute(self, context):
        storage_selection_func(2)
        return {'FINISHED'}
    
class MYADDON_OP_StorageSelection3(bpy.types.Operator):
    bl_idname = "buttons.storageslection3"     # 必須
    bl_label = "StorageSelection"             # 必須
    def execute(self, context):
        storage_selection_func(3)
        return {'FINISHED'}
    
class MYADDON_OP_StorageSelection4(bpy.types.Operator):
    bl_idname = "buttons.storageslection4"     # 必須
    bl_label = "StorageSelection"             # 必須
    def execute(self, context):
        storage_selection_func(4)
        return {'FINISHED'}

class MYADDON_OP_CallSelection1(bpy.types.Operator):
    bl_idname = "buttons.callslection1"     # 必須
    bl_label = "StorageSelection"             # 必須
    def execute(self, context):
        call_selection_func(1)
        return {'FINISHED'}
    

class MYADDON_OP_CallSelection2(bpy.types.Operator):
    bl_idname = "buttons.callslection2"     # 必須
    bl_label = "StorageSelection"             # 必須
    def execute(self, context):
        call_selection_func(2)
        return {'FINISHED'}

class MYADDON_OP_CallSelection3(bpy.types.Operator):
    bl_idname = "buttons.callslection3"     # 必須
    bl_label = "StorageSelection"             # 必須
    def execute(self, context):
        call_selection_func(3)
        return {'FINISHED'}
    

class MYADDON_OP_CallSelection4(bpy.types.Operator):
    bl_idname = "buttons.callslection4"     # 必須
    bl_label = "StorageSelection"             # 必須
    def execute(self, context):
        call_selection_func(4)
        return {'FINISHED'}
    
class MYADDON_PT_StorageSelectionPanel(bpy.types.Panel):
    bl_label = "選択頂点を保存"          # パネルのヘッダに表示される文字列
    bl_space_type = "VIEW_3D"            # パネルを登録するスペース
    bl_region_type = "UI"                # パネルを登録するリージョン
    #bl_category = "カスタムタブ"         # パネルを登録するタブ名
    bl_context = "mesh_edit"            # パネルを表示するコンテキスト
    
    # 本クラスの処理が実行可能かを判定する
    @classmethod
    def poll(cls, context):
        # オブジェクトが選択されているときのみメニューを表示させる
        for o in bpy.data.objects:
            if o.select_get():
                return True
        return False
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text="選択頂点を記憶")
        row = layout.row(align=True)
        
        row.operator(MYADDON_OP_StorageSelection1.bl_idname, text="1")
        row.operator(MYADDON_OP_StorageSelection2.bl_idname, text="2")
        row.operator(MYADDON_OP_StorageSelection3.bl_idname, text="3")
        row.operator(MYADDON_OP_StorageSelection4.bl_idname, text="4")

        layout.separator()
        
        layout.label(text="選択頂点を呼び出し")
        row = layout.row(align=True)
        
        row.operator(MYADDON_OP_CallSelection1.bl_idname, text="1")
        row.operator(MYADDON_OP_CallSelection2.bl_idname, text="2")
        row.operator(MYADDON_OP_CallSelection3.bl_idname, text="3")
        row.operator(MYADDON_OP_CallSelection4.bl_idname, text="4")
        
        
    
        
classes = [
    MYADDON_OP_StorageSelection1,
    MYADDON_OP_StorageSelection2,
    MYADDON_OP_StorageSelection3,
    MYADDON_OP_StorageSelection4,
    MYADDON_OP_CallSelection1,
    MYADDON_OP_CallSelection2,
    MYADDON_OP_CallSelection3,
    MYADDON_OP_CallSelection4,
    MYADDON_PT_StorageSelectionPanel,
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



