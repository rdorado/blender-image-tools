import bpy

# make mesh
vertices = [(0, 0, 0),]
edges = []
#faces = []


#origin = Vector(origo)
points = [(0,0), (1,0), (1,1), (0,1)]
for point in points: 
  pass



#origin = Vector(origo)
(x,y,z) = (0.707107, 0.258819, 0.965926)
verts = tuple([(x,x,-1), (x,-x,-1), (-x,-x,-1), (-x,x,-1), (0,0,1)])
faces = tuple([(1,0,4), (4,2,1), (4,3,2), (4,0,3), (0,1,2,3)])


new_mesh = bpy.data.meshes.new('new_mesh')
new_mesh.from_pydata(verts, edges, faces)
new_mesh.update()

# make object from mesh
new_object = bpy.data.objects.new('new_object', new_mesh)

# add object to scene collection
my_collection = bpy.data.collections['Collection']
my_collection.objects.link(new_object)
my_collection.name = "My Collection"


mesh = bpy.data.meshes['Cube']
#mesh = bpy.data.collections['Collection']
print(mesh)
#mesh.user_clear()
bpy.data.meshes.remove(mesh)

bpy.ops.wm.save_as_mainfile(filepath='mesh.blend')