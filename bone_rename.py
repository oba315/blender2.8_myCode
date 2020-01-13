import bpy

for x in bpy.context.object.data.bones:
    if x.name[-2:] == '.R':
        x.name = '右' + x.name[:-2]
    
    if x.name[-2:] == '.L':
        x.name = '左' + x.name[:-2]