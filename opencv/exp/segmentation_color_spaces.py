import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import argparse

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
from matplotlib.colors import hsv_to_rgb

## [load_image]
# Load the image
parser = argparse.ArgumentParser(description='Code for Image Segmentation with Distance Transform and Watershed Algorithm.\
    Sample code showing how to segment overlapping objects using Laplacian filtering, \
    in addition to Watershed and Distance Transformation')
parser.add_argument('--input', help='Path to input image.', default='cards.png')
args = parser.parse_args()

src = cv.imread(cv.samples.findFile(args.input))
plt.imshow(src)
plt.show()

src = cv.cvtColor(src, cv.COLOR_BGR2RGB)
plt.imshow(src)
plt.show()


# Visualizing Nemo in RGB Color Space
r, g, b = cv.split(src)
fig = plt.figure()
axis = fig.add_subplot(1, 1, 1, projection="3d")


pixel_colors = src.reshape((np.shape(src)[0]*np.shape(src)[1], 3))
norm = colors.Normalize(vmin=-1.,vmax=1.)
norm.autoscale(pixel_colors)
pixel_colors = norm(pixel_colors).tolist()


axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")
axis.set_xlabel("Red")
axis.set_ylabel("Green")
axis.set_zlabel("Blue")
plt.show()


# Visualizing Nemo in HSV Color Space
hsv_src = cv.cvtColor(src, cv.COLOR_RGB2HSV)

h, s, v = cv.split(hsv_src)
fig = plt.figure()
axis = fig.add_subplot(1, 1, 1, projection="3d")

axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
axis.set_xlabel("Hue")
axis.set_ylabel("Saturation")
axis.set_zlabel("Value")
plt.show()

#flags = [i for i in dir(cv) if i.startswith('COLOR_')]

#

#nemo = cv2.imread('./images/nemo0.jpg')

#light_orange = (1, 190, 200)
#dark_orange = (18, 255, 255)

#(147, 82, 249)

#color1 = (35, 55, 205)
#color2 = (75, 85, 255)

#color1 = (25, 35, 105)
#color2 = (95, 105, 255)

color1 = (5, 5, 5)
color2 = (225, 255, 255)


lo_square = np.full((10, 10, 3), color1, dtype=np.uint8) / 255.0
do_square = np.full((10, 10, 3), color2, dtype=np.uint8) / 255.0

plt.subplot(1, 2, 1)
plt.imshow(hsv_to_rgb(do_square))
plt.subplot(1, 2, 2)
plt.imshow(hsv_to_rgb(lo_square))
plt.show()



mask = cv.inRange(hsv_src, color1, color2)
result = cv.bitwise_and(src, src, mask=mask)


plt.subplot(1, 2, 1)
plt.imshow(mask, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(result)
plt.show()