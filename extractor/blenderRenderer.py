import bpy

from core import Layout

async def render_as_blender(layout, filename):
    width = 0.1
    im = { 'value': 1 }

    def addMesh(surface):
        points = []
        vertices = []
        edges = []
        faces = []

        for p in surface.outer.points:
            points.append([p.x/10, p.y/10])

        np = len(points)
        for p in points:
            vertices.append(tuple([p[0], -p[1], 0.0]))
        for p in points:
            vertices.append(tuple([p[0], -p[1], width]))

        faces = [
            tuple(range(0, np)),
            tuple(range(np, np*2)),
        ]

        for i in range(0, np-1):
            faces.append(tuple([i, i+1, np+i+1, np+i]))
        faces.append(tuple([0, np-1, np*2-1, np]))

        idm = im['value']
        im['value']+=1
        mesh = bpy.data.meshes.new("Mesh "+str(idm))
        mesh.from_pydata(vertices, edges, faces)
        new_object = bpy.data.objects.new("Object "+str(idm), mesh)
        collection = bpy.data.collections['Collection']
        collection.objects.link(new_object)


    def processLayout(layout):
        if type(layout.content) != list:
            for surface in layout.content.surfaces:
                addMesh(surface)
        else:
            for obj in layout.content:
                processLayout(obj)

    processLayout(layout)
    '''
    
        paths = self.content.as_svg_paths()
        resp.extend(paths)
    else:
        for obj in self.content:
            paths = obj.as_svg_paths()
            resp.extend(paths)
    return resp
    '''

    '''
    points = [[4,4],[5,5.5],[3,5.5]]
    vertices = []
    edges = []
    faces = []

    width = 0.1
    np = len(points)
    for p in points:
       vertices.append(tuple([p[0], -p[1], 0.0]))
    for p in points:
       vertices.append(tuple([p[0], -p[1], width]))

    faces = [
      tuple(range(0, np)),
      tuple(range(np, np*2)),
    ]

    for i in range(0, np-1):
        faces.append(tuple([i, i+1, np+i+1, np+i]))
    faces.append(tuple([0, np-1, np*2-1, np]))


    mesh = bpy.data.meshes.new("My mesh")
    mesh.from_pydata(vertices, edges, faces)
    new_object = bpy.data.objects.new('new_object', mesh)
    new_collection = bpy.data.collections['Collection']
    new_collection.objects.link(new_object)
    '''

    try:
        mesh = bpy.data.meshes['Cube']
        bpy.data.meshes.remove(mesh)
    except KeyError:
        pass

    for obj in bpy.data.collections['Collection'].objects:
        if obj.type == "CAMERA":
            obj.location.x = 4
            obj.location.y = -4
            obj.location.z = 15
            obj.rotation_euler.x = 0
            obj.rotation_euler.y = 0
            obj.rotation_euler.z = 0 #1.5708
        if obj.type == "LIGHT":
            obj.location.x = 1.8
            obj.location.y = -3.2
            obj.location.z = 3.2
    
    bpy.ops.wm.save_as_mainfile(filepath=filename)

    scene = bpy.context.scene
    scene.frame_start = 0
    scene.frame_end = 1
    scene.render.film_transparent = True
    scene.render.image_settings.color_mode = 'RGBA'

    # render settings
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = filename+".png"
    bpy.ops.render.render(write_still = 1)

    return True