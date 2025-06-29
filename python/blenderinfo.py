import bpy

#bpy.ops.wm.open_mainfile(filepath="D:/project/blender/data/cube_3_6_9.blend")
#bpy.ops.wm.open_mainfile(filepath="D:/project/blender/data/cube_2_93_9.blend")
bpy.ops.wm.open_mainfile(filepath="D:/project/blender/data/cube_2_82a.blend")

#bpy.data.meshes

#for key in bpy.data.meshes.keys():
#  print(key)


#print(dir(bpy.data.meshes['Cube']))
#print(materials)

#for key in bpy.data.meshes['Cube'].materials.keys():
#  print(key)

bpy.data.meshes['Cube'].materials['Material'].diffuse_color = (0.4980392156862745, 1.0, 0.8313725490196079, 1)

 
bpy.ops.wm.save_as_mainfile(filepath="D:/project/blender/data/cube_2_82a_out.blend")

