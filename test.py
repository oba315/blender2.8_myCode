import bpy

def print_obj_name() :
    for obj in bpy.data.objects:
        print( obj.name )
        
        
print_obj_name()