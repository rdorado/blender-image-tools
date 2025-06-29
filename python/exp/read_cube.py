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
bpy.ops.wm.open_mainfile(filepath=filename)

print("Loaded file "+filename)

print("Collections:")
for k, v in bpy.data.collections.items():
    print('  '+str(k))
    for obj in v.objects:
        #print(obj.type)
        
        if obj.type == "MESH":
            print(obj.name)
            print(dir(obj))
            print(len(obj.children))
            for k2, v2 in obj.vertex_groups.items():
               print(k2, v2)
            print('"'+str(dir(obj.vertex_groups.values))+'"\n\n')


print("Meshes:")
for k, v in bpy.data.meshes.items():
    print('  '+str(k))
    for vvv in [(obj.matrix_world @ vv.co) for vv in v.vertices]:
        print('  '+str(vvv))
