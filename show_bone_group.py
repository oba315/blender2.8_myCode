import bpy 


# ボーングループに属するボーンを非表示(表示)
def hide_bone_group(amt, group_name, show = False) :
        
    for b in amt.pose.bones :
        if b.bone_group != None :
            if b.bone_group.name == group_name :
                b.bone.hide = not show
                

def hide_all_bones(amt, show = False):
    for b in amt.pose.bones :
            b.bone.hide = not show



amt = bpy.data.objects['Armature']
hide_bone_group(amt, "G1")
hide_all_bones(amt,1)
#hide_bone_group(amt, "G1", True)