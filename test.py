import bpy

def print_obj_name() :
    for obj in bpy.data.objects:
        print( obj.name )
        
        
# test commit
print_obj_name()