import bpy
import sys
import os

def print_usage():
    print("Usage: python '"+sys.argv[0]+"' <blender filename> <output filename>")
    print("Example: python "+sys.argv[0]+" cube.blend Cube.png")
    sys.exit(0)
    
def main():
    args = sys.argv[1:]
    if len(args) < 2: print_usage()
    
    input_filename = args[0]
    output_filename = args[1]

    bpy.ops.wm.open_mainfile(filepath=input_filename)

    for obj in bpy.data.collections['Collection'].objects:
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

    scene = bpy.context.scene
    scene.frame_start = 0
    scene.frame_end = 1
    scene.render.film_transparent = True
    scene.render.image_settings.color_mode = 'RGBA'
    
    # find absolute path for output
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    absolute_output_filename = os.path.join(current_directory, output_filename)

    # render settings
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = absolute_output_filename #"E:/project/blender/python/Sprite.png"
    bpy.ops.render.render(write_still = 1)


if __name__ == "__main__":
    sys.exit(main())