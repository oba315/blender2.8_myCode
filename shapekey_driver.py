import bpy
from bpy.props import (BoolProperty, IntProperty, FloatProperty, PointerProperty)


bl_info = {
    "name": "original_search_shapekey_and_set_driver",
    "author": "Aobayuki",
    "version": (0, 0),
    "blender": (2, 83, 0),
    "location": "3Dビュー > Propatyシェルフ",
    "description": "シェイプキーを検索してfacialボーンのプロパティをドライバに設定します",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "User Interface"
}


#ドライバを設定する関数
def add_driver(
        source,     #ドライバを設定するオブジェクト
        target,     #操作用オブジェクト
        prop,       #ドライバを設定するオブジェクトの、ドライバを設定するプロパティのデータパス(strings)(データパスのコピーから入手できるもの) 
        dataPath,   #操作用オブジェクトの、操作用プロパティのデータパス(strings)(データパスのコピーから入手できるもの)
        index = -1, #ドライバを設定するプロパティが配列だった時のインデックス(配列でないときは-1)    
        negative = False,
        func = ''
    ):
    ''' Add driver to source prop (at index), driven by target dataPath '''

    if index != -1:
        d = source.driver_add( prop, index ).driver
    else:
        d = source.driver_add( prop ).driver

    #変数は1つのみ許可
    if len(d.variables) == 0:
        v = d.variables.new()
    else:
        v = d.variables[0]
            
    print (target)
    v.name                 = prop
    v.targets[0].id        = target
    v.targets[0].data_path = dataPath
    print ("ppp")
    d.expression = func + "(" + v.name + ")" if func else v.name
    d.expression = d.expression if not negative else "-1 * " + d.expression



class SearchShapeKeys(bpy.types.Operator):
    bl_idname = "object.searchshapekeys_or"
    bl_label = "NOP"
    bl_description = "何もしない"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        
        '''ボーンを設定します'''
        arm = bpy.data.objects['_arm_nizi']
        bone_name = 'facial'
        
        ''''''''''''''''''''''''
        
        
        KeySetList = bpy.data.shape_keys
        
        for keyset in KeySetList:
            print("\n",keyset.user)
            for key in keyset.key_blocks:
                print(key.name)
                
                if key.name == "Basis" or key.name == "ベース":
                    continue
                
                #プロパティの追加
                if key.name not in arm.pose.bones[bone_name]:
                    arm.pose.bones[bone_name][key.name] = 0.0
                    
                #ドライバの設定
                add_driver( 
                    key, arm, 'value',
                    'pose.bones["' + bone_name + '"]["' + key.name + '"]'
                    )
               
        return {'FINISHED'}

    
# ツールシェルフに追加するクラス
class MYADDON_PT_SetShapeofMouthUI(bpy.types.Panel):

    bl_label = "シェイプキー設定"             # タブに表示される文字列
    bl_space_type = 'VIEW_3D'           # メニューを表示するエリア
    bl_region_type = 'UI'               # メニューを表示するリージョン
    bl_category = "シェイプキー"    # タブを開いたメニューのヘッダーに表示される文字列
    #bl_context = "objectmode"           # パネルを表示するコンテキスト

    # 本クラスの処理が実行可能かを判定する
    @classmethod
    def poll(cls, context):
        # 常に表示
        return True
    
    # ヘッダーのカスタマイズ
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='PLUGIN')

        
    # メニューの描画処理
    def draw(self, context):
       
        layout = self.layout
       
        
        layout.label(text="シェイプキーを検索してボーンfacialのプロパティをドライバとして設定します")
        layout.operator(SearchShapeKeys.bl_idname, text="update")
        
       
classes = [
    SearchShapeKeys,
    MYADDON_PT_SetShapeofMouthUI
] 

def register():
    for c in classes:
        bpy.utils.register_class(c)
    print("Addon 'shapekey_driver' is Active")
    #bpy.types.Object.sample_props=PointerProperty(type=SampleProperties) 
        

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    global targetarm
    del targetarm
    print("Addon 'shapekey_driver' is Inactive")


if __name__ == "__main__":
    register()
    