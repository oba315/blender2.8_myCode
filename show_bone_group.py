import bpy
from bpy.props import (
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    EnumProperty,
    BoolProperty,
    StringProperty
)


bl_info = {
    "name": "myaddon_show_bone_group",
    "author": "aobayu",
    "version": (3, 0),
    "blender": (2, 81, 0),
    "location": "3Dビューポート > Sidebar",
    "description": "myaddon_show_bone_group",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "User Interface"
}



class MYADDON_OP_ShowBoneGroupe_RefleshUI(bpy.types.Operator):

    bl_idname = "button.showbonegrouperefleshui"
    bl_label = "NOP"
    bl_description = "UIを更新"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        if scene.show_bone_groupe_amtname in bpy.data.objects :
            amt = bpy.data.objects[scene.show_bone_groupe_amtname]
            bone_group_to_bone_layer(amt)
        else :
            print("invalid armature name")
        return {'FINISHED'}
        
    
class MYADDON_OP_ShowBoneGroupe_ShowAll(bpy.types.Operator):

    bl_idname = "button.showbonegroupshowall"
    bl_label = "NOP"
    bl_description = " 全てを表示"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        amt = bpy.data.objects[scene.show_bone_groupe_amtname]
        amt.data.layers = [True for i in range(32)]
        return {'FINISHED'}

# ボーングループをレイヤーに分ける。
def bone_group_to_bone_layer(amt):
    for b in amt.pose.bones :
        if b.bone_group != None :
            amt.data.bones[b.name].layers = [
                     True  if i == b.bone_group_index else False for i in range(32)]
        else :
            amt.data.bones[b.name].layers = [
                     True  if i == 31 else False for i in range(32)]
            
            


class MYADDON_PT_ShowBoneGroupUI(bpy.types.Panel):

    bl_label = "ボーングループ"         # パネルのヘッダに表示される文字列
    bl_space_type = 'VIEW_3D'           # パネルを登録するスペース
    bl_region_type = 'UI'               # パネルを登録するリージョン
    #bl_category = "カスタムタブ"        # パネルを登録するタブ名
    #bl_context = "objectmode"           # パネルを表示するコンテキスト

    # 本クラスの処理が実行可能かを判定する
    @classmethod
    def poll(cls, context):
        # オブジェクトが選択されているときのみメニューを表示させる
            
        return True
        
    # メニューの描画処理
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene, "show_bone_groupe_amtname", text="arm ")
        
        
        # ボタンを追加
        layout.operator(MYADDON_OP_ShowBoneGroupe_RefleshUI.bl_idname, text="refleshUi")
        
        ## ---------------------------------------------------------------------------------            
        
        if scene.show_bone_groupe_amtname in bpy.data.objects :
            amt = bpy.data.objects[scene.show_bone_groupe_amtname]
            
            num_of_bone_groups = len( amt.pose.bone_groups )
            
            box = layout.box()
            box.label(text="Selection Tools")
            for i in range (num_of_bone_groups ) : 
                box.prop( amt.data, 'layers', index=i, 
                          toggle=True, text=amt.pose.bone_groups[i].name)
            
            box.prop( amt.data, 'layers', index=31, 
                          toggle=True, text="その他")
            layout.operator(MYADDON_OP_ShowBoneGroupe_ShowAll.bl_idname, text="ALL")
            
        else :
            layout.label(text = "invalid armature name")
        ## --------------------------------------------------------------------------------
        
        '''
        arm = bpy.data.armatures['アーマチュア']
        col = layout.column()
        col.label(text="Layers:")
        col.prop(arm, "layers", text="")
        '''
            
        ## -------------------------------------------------------------------------------
        


# プロパティの初期化
def init_props():
    scene = bpy.types.Scene
    
    scene.show_bone_groupe_amtname = StringProperty(
        name="armature name",
        description="armature name",
        default='arm'
    )
    


# プロパティを削除
def clear_props():
    scene = bpy.types.Scene
    del scene.show_bone_groupe_amtname


classes = [
    MYADDON_PT_ShowBoneGroupUI,
    MYADDON_OP_ShowBoneGroupe_RefleshUI,
    MYADDON_OP_ShowBoneGroupe_ShowAll
]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    init_props()
    print("サンプル 2-7: アドオン『サンプル 2-7』が有効化されました。")


def unregister():
    clear_props()
    for c in classes:
        bpy.utils.unregister_class(c)
    print("サンプル 2-7: アドオン『サンプル 2-7』が無効化されました。")


if __name__ == "__main__":
    register()
    #unregister()