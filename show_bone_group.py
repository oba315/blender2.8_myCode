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
    "name": "サンプル 2-7: BlenderのUIを制御するアドオン",
    "author": "ぬっち（Nutti）",
    "version": (3, 0),
    "blender": (2, 80, 0),
    "location": "3Dビューポート > Sidebar",
    "description": "BlenderのUIを制御するアドオン",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "User Interface"
}



class MYADDON_OP_ShowBoneGroupe_RefleshUI(bpy.types.Operator):

    bl_idname = "button.showbonegrouperefleshui"
    bl_label = "NOP"
    bl_description = "何もしない"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        scene = context.scene
        
        amt = bpy.data.objects[scene.show_bone_groupe_amtname]
        for b in amt.pose.bones :
                print( b.bone.name ) 
                
                
        bone_group_to_bone_layer(amt)
        return {'FINISHED'}
    
class MYADDON_OP_ShowBoneGroupe_ShowAll(bpy.types.Operator):

    bl_idname = "button.showbonegroupshowall"
    bl_label = "NOP"
    bl_description = "何もしない"
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
            
            
class SAMPLE27_OT_Nop(bpy.types.Operator):

    bl_idname = "object.sample27_nop"
    bl_label = "NOP"
    bl_description = "何もしない"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}


class SAMPLE27_MT_NopMenu(bpy.types.Menu):

    bl_idname = "SAMPLE27_MT_NopMenu"
    bl_label = "NOP メニュー"
    bl_description = "何もしないオペレータを複数持つメニュー"

    def draw(self, context):
        layout = self.layout
        # メニュー項目の追加
        for i in range(3):
            layout.operator(SAMPLE27_OT_Nop.bl_idname, text=("項目 %d" % (i)))


# Sidebarのタブ [カスタムタブ] に、パネル [カスタムパネル] を追加
class SAMPLE27_PT_CustomPanel(bpy.types.Panel):

    bl_label = "カスタムパネル"         # パネルのヘッダに表示される文字列
    bl_space_type = 'VIEW_3D'           # パネルを登録するスペース
    bl_region_type = 'UI'               # パネルを登録するリージョン
    bl_category = "カスタムタブ"        # パネルを登録するタブ名
    bl_context = "objectmode"           # パネルを表示するコンテキスト

    # 本クラスの処理が実行可能かを判定する
    @classmethod
    def poll(cls, context):
        # オブジェクトが選択されているときのみメニューを表示させる
        for o in bpy.data.objects:
            if o.select_get():
                return True
        return False

    # ヘッダーのカスタマイズ
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='PLUGIN')

    # メニューの描画処理
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        amt = bpy.data.objects[scene.show_bone_groupe_amtname]
        
        layout.prop(scene, "show_bone_groupe_amtname", text="プロパティ 3")
        
        # ボタンを追加
        layout.operator(MYADDON_OP_ShowBoneGroupe_RefleshUI.bl_idname, text="refleshUi")
        
        num_of_bone_groups = len( amt.pose.bone_groups )
        
        ## ---------------------------------------------------------------------------------            
        box = layout.box()
        box.label(text="Selection Tools")
        for i in range (num_of_bone_groups ) : 
            box.prop( amt.data, 'layers', index=i, 
                      toggle=True, text=amt.pose.bone_groups[i].name)
        
        box.prop( amt.data, 'layers', index=31, 
                      toggle=True, text="その他")
        layout.operator(MYADDON_OP_ShowBoneGroupe_ShowAll.bl_idname, text="ALL")
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
        name="プロパティ 5",
        description="プロパティ（bool）",
        default='this'
    )
    


# プロパティを削除
def clear_props():
    scene = bpy.types.Scene
    del scene.sample27_prop_int
    del scene.sample27_prop_float
    del scene.sample27_prop_floatv
    del scene.sample27_prop_enum
    del scene.sample27_prop_bool


classes = [
    SAMPLE27_OT_Nop,
    SAMPLE27_MT_NopMenu,
    SAMPLE27_PT_CustomPanel,
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