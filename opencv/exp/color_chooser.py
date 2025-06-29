import numpy as np
import cv2 as cv

from matplotlib.colors import hsv_to_rgb

def nothing(x):
 pass
# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)
cv.namedWindow('image')
# create trackbars for color change
cv.createTrackbar('R','image',0,255,nothing)
cv.createTrackbar('G','image',0,255,nothing)
cv.createTrackbar('B','image',0,255,nothing)
# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv.createTrackbar(switch, 'image',0,1,nothing)

color1 = (18, 255, 255)
while(1):
 cv.imshow('image',img)
 k = cv.waitKey(1) & 0xFF
 if k == 27: break
 # get current positions of four trackbars
 r = cv.getTrackbarPos('R','image')
 g = cv.getTrackbarPos('G','image')
 b = cv.getTrackbarPos('B','image')
 s = cv.getTrackbarPos(switch,'image')
 
 if s == 0:
  
  img[:] = 0
 else:
  color1 = (r, g, b)
  lo_square = np.full((300,512,3), color1, dtype=np.uint8) / 255.0
  img = hsv_to_rgb(lo_square)
  #img[:] = [b,g,r]
cv.destroyAllWindows()