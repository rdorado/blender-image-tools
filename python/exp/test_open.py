import bpy

bpy.ops.wm.open_mainfile(filepath="test.blend")
obj = bpy.context.active_object

print(dir(bpy.data.objects))

i = 0
for ob in bpy.data.objects:
    print("\n" + str(i) + ": " + str(ob.type))
    print(dir(ob.data))
    i=i+1
    if ob.type == 'MESH':
        print('MESH')
        #print(dir(ob.data.edges))
        print(' Vertices:')
        for v in ob.data.vertices:
            print(v.co)
        print(' Edges:')
        for e in ob.data.edges:
            #print(dir(e.vertices))
            print('  Edge:')            
            for v in e.vertices:
                print(v)
            #    #print(dir(v))
        #mesh_owners.setdefault(ob.data, []).append(ob)


'''
print(dir(bpy))

print("\n")
print(dir(bpy.data))

print("\n")
print(dir(bpy.data.objects.items))


#print("\n")
#print(dir(bpy.data.meshes))

#print("\n")
#print(dir(bpy.data.meshes.items))
bpy.data.meshes.items()
#len(bpy.data.meshes.items)

'''