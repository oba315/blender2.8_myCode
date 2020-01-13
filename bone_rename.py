import bpy
import sys

print("\nRename Bone from dictionary")
 
fn = "bone_name_dict.txt"

# read dictionary
text = bpy.data.texts.get(fn)
if text == None:
    print ('ERROR : text "'+fn+  '" is not exist.')
lines = [x.body.split() for x in text.lines]


inverse = True

# 選択されているボーンについて
# 最も長く一致した文字列で置換
a = 1 if inverse else 0
b = 0 if inverse else 1
buffer = [0, "befor", "after"]
for bone in bpy.context.object.data.bones:
    for pair in lines:
        if pair[a] in bone.name and buffer[0] < len(pair[a]):
            buffer = [ len(pair[a]), pair[a], pair[b] ]

    if (buffer[0] != 0):
        bone.name = bone.name.replace( buffer[1], buffer[2])
    
    buffer[0] = 0

    


        
        
#f.close()