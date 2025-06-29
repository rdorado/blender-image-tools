import bpy

def strVector3( v3 ):
    return str(v3.x) + "," + str(v3.y) + "," + str(v3.z)

'''
# create a new cube
bpy.ops.mesh.primitive_cube_add()

# newly created cube will be automatically selected
cube = bpy.context.selected_objects[0]
# change name
cube.name = "MyLittleCube"

# change its location
cube.location = (0.0, 5.0, 0.0)

# done
print("Done creating MyCube at position " + strVector3(cube.location) + " with name " + cube.name)

# new mesh
vertices = [(0, 0, 0),]
edges = []
faces = []

new_mesh = bpy.data.meshes.new('new_mesh')

new_mesh.from_pydata(vertices, edges, faces)
new_mesh.update()



#print('\n\ndir(bpy.data)')
#print(dir(bpy.data))

#print('\n\ndir(bpy.data.collections)')
#print(dir(bpy.data.collections))
meshes = set()
for k, v in bpy.data.collections.items():
    #print('"'+str(k)+'"', dir(v))
    #for obj in [o for o in collection.objects if o.type == 'MESH']:
    for obj in v.objects:
        if obj.type == 'MESH':
            #print("\ndir(obj)")
            #print(obj.type)
            #print(dir(obj))
            #meshes.add( obj )
            bpy.data.objects.remove( obj )

for mesh in [m for m in meshes if m.users == 0]:
    # Delete the meshes
    bpy.data.meshes.remove( mesh )

print('\n\ndir(bpy.data.meshes)')
print(dir(bpy.data.meshes))
for k, v in bpy.data.meshes.items():
    print('"'+str(k)+'"', dir(v))

print("\n\nDone creating")

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete() 

'''

'''
# make mesh
vertices = [(0, 0, 0),]
edges = []
faces = []
new_mesh = bpy.data.meshes.new('new_mesh')
new_mesh.from_pydata(vertices, edges, faces)
new_mesh.update()
# make object from mesh
new_object = bpy.data.objects.new('new_object', new_mesh)
# make collection
new_collection = bpy.data.collections.new('new_collection')
bpy.context.scene.collection.children.link(new_collection)
# add object to scene collection
new_collection.objects.link(new_object)
'''

filename = 'cube.blend'

for obj in bpy.data.collections['Collection'].objects:
    print(obj.type)
    if obj.type == "CAMERA":
        obj.location.x = 0
        obj.location.z = 0
        obj.rotation_euler.x = 1.5708
        obj.rotation_euler.y = 0
        obj.rotation_euler.z = 0
    if obj.type == "LIGHT":
        obj.location.x = 1.8
        obj.location.y = -3.2
        obj.location.z = 3.2


bpy.ops.wm.save_as_mainfile(filepath=filename)


'''
image = bpy.data.images.new("Sprite", alpha=True, width=16, height=16)
#image.use_alpha = True
image.alpha_mode = 'STRAIGHT'
image.filepath_raw = "E:/project/blender/python/Sprite.png"
image.file_format = 'PNG'
image.save()
'''

'''
# Set save path
sce = bpy.context.scene.name
bpy.data.scenes[sce].render.filepath = "./image.png"

# Go into camera-view (optional)
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        break

# Render image through viewport
bpy.ops.render.opengl(write_still=True)
'''

scene = bpy.context.scene
scene.frame_start = 0
scene.frame_end = 1

# render settings
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = "E:/project/blender/python/Sprite.png"
bpy.ops.render.render(write_still = 1)

print("Creating file "+filename)

