import numpy as np
from PIL import Image

from PIL import Image
import numpy as np
from os import listdir

def crop(png_image_name):
    " This does not work"
    pil_image = Image.open(png_image_name)
    np_array = np.array(pil_image)
    blank_px = [255, 255, 255, 0]
    mask = np_array != blank_px
    coords = np.argwhere(mask)
    x0, y0, z0 = coords.min(axis=0)
    x1, y1, z1 = coords.max(axis=0) + 1
    cropped_box = np_array[x0:x1, y0:y1, z0:z1]
    pil_image = Image.fromarray(cropped_box, 'RGBA')
    print(pil_image.width, pil_image.height)
    pil_image.save(png_image_name+".tmp.png")
    print(png_image_name)

def crop2(crop_file):
    " This does not work"
    """crop the image, removing invisible borders"""
    image = bpy.data.images.load(crop_file, check_existing=False)
    w, h = image.size

    print("Original size: " + str(w) + " x " + str(h))

    linear_pixels = image.pixels[:]
    pixels4d = np.reshape(linear_pixels, (h, w, 4))
    
    mask = pixels4d [:,:,3] != 0.
    coords = np.argwhere(mask)
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1
    cropped_box = pixels4d[y0:y1, x0:x1, :]
    
    w1, h1 = x1 - x0, y1 - y0
    print("Crop size: " + str(w1) + " x " + str(h1))
    
    temp_image = bpy.data.images.new(crop_file, alpha=True, width=w1, height=h1)
    temp_image.pixels[:] = cropped_box.ravel()
    temp_image.filepath_raw = crop_file+".tmp.png"
    temp_image.file_format = 'PNG'
    temp_image.alpha_mode = 'STRAIGHT'
    temp_image.save()

def bbox(im):
    " This does not work"
    a = np.array(im)[:,:,:3]  # keep RGB only
    m = np.any(a != [255, 255, 255], axis=2)
    coords = np.argwhere(m)
    y0, x0, y1, x1 = *np.min(coords, axis=0), *np.max(coords, axis=0)
    return (x0, y0, x1+1, y1+1)



def crop3(file):
    " This works!!! "
    im = Image.open(file)
    im.getbbox()
    im2 = im.crop(im.getbbox())
    im2.save("result.png")

def scale(file):
    base_width = 300
    img = Image.open(file)
    wpercent = (base_width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    img.save('somepic.jpg')

def resize(file, w, h):
    img = Image.open(file)
    img = img.resize((w, h), Image.Resampling.LANCZOS)
    img.save('thubmnail.png')

#crop3('D:/project/blender/data/image.png')
resize('result.png', 24, 24)
#im = Image.open('D:/project/blender/data/image.png')
#print(bbox(im))  # (33, 12, 223, 80)
#im2 = im.crop(bbox(im))
#im2.save('test_cropped.png')

