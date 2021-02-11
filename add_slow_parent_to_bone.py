import bpy

def test() :
    if bpy.context.object.mode != "POSE" :
        return -1;
    
    # 複数ボーンの処理も欲しい
    amt    = bpy.context.object
    bone   = bpy.context.selected_pose_bones[0] 
    p_bone = bone.parent 
    pos    = bone.tail
    bonename = bone.name
    
    print ( p_bone)
    
    # エンプティの作成
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    bpy.ops.object.empty_add( location=pos, rotation=(0.0, 0.0, 0.0))
    emp1 = bpy.context.view_layer.objects.active
    emp1.name = bonename + "_empty1"
    emp1.scale = (0.5,0.5,0.5)
    bpy.ops.object.constraint_add(type='CHILD_OF')
    emp1.constraints[0].target = amt
    emp1.constraints[0].subtarget = p_bone.name
    bpy.context.object.constraints[0].set_inverse_pending = True

    
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    bpy.ops.object.empty_add( location=pos, rotation=(0.0, 45/57.3, 0.0))
    emp2 = bpy.context.view_layer.objects.active
    emp2.name = bonename + "_empty2"
    emp2.scale = (0.5,0.5,0.5)
    
    # ドライバの設定
    emp2.driver_remove("location")
    list = ['LOC_X', 'LOC_Y', 'LOC_Z']
    for i in range(3) :
        d = bpy.context.object.driver_add("location", i)
        d.driver.type = "SCRIPTED"
        
        var = d.driver.variables.new()
        var.name = 'var'
        var.type = 'TRANSFORMS'
        var.targets[0].id = emp1
        var.targets[0].transform_type = list[i]

        var1 = d.driver.variables.new()
        var1.name = 'var1'
        var1.type = 'TRANSFORMS'
        var1.targets[0].id = emp2
        var1.targets[0].transform_type = list[i]

        var1 = d.driver.variables.new()
        var1.name = 'n'
        var1.type = 'SINGLE_PROP'
        var1.targets[0].id = amt
        var1.targets[0].data_path = 'data.["slow_parent_speed"]'

        d.driver.expression = '(var+var1*(n-1))/n'
    
    # IKの設定
    bpy.context.view_layer.objects.active = amt
    bpy.ops.object.mode_set(mode='POSE', toggle=False)

    ik = 0;
    for c in bone.constraints :
        if c.name == "slow_parent_IK" :
            ik = c
    if ik == 0 :
        ik = bone.constraints.new('IK')
        ik.name = "slow_parent_IK"
    
    ik.target = emp2
    ik.chain_count = 1

    
test()