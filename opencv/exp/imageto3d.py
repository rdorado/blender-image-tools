import cv2
import numpy as np
import pickle
import math
import sys

# grab the image dimensions
#h = img.shape[0]
#w = img.shape[1]

#col = img[0, 0]


def find_segment(nx, ny, img, mask, h, w, col):
    tmp = [(nx, ny)]
    resp = [(nx, ny)]
    color = img[nx, ny]
    mask[nx, ny] = col
    while len(tmp) > 0:
        (x, y) = tmp.pop(0)
        if (x > 0) and np.array_equal(img[x-1, y], img[x, y]) and (mask[x-1, y] == 0):
            resp.append((x-1, y))
            tmp.append((x-1, y))
            mask[x-1, y] = col
        if (x < h-1) and np.array_equal(img[x+1, y], img[x, y]) and (mask[x+1, y] == 0):
            resp.append((x+1, y))
            tmp.append((x+1, y))
            mask[x+1, y] = col
        if (y > 0) and np.array_equal(img[x, y-1], img[x, y]) and (mask[x, y-1] == 0):
            resp.append((x, y-1))
            tmp.append((x, y-1))
            mask[x, y-1] = col
        if (y < w-1) and np.array_equal(img[x, y+1], img[x, y]) and (mask[x, y+1] == 0):
            resp.append((x, y+1))
            tmp.append((x, y+1))
            mask[x, y+1] = col
    return (resp, color)


def calculate_center(cluster):
    sx = 0
    sy = 0
    n = len(cluster)
    for (x, y) in cluster:
        sx += x
        sy += y
    return (sx/n, sy/n)

def calculate_ditances(center, cluster):
    dists = []
    (cx, cy) = center
    for (x, y) in cluster:
       dists.append((x, y, math.dist([cx, cy],[x, y])))
    return dists

def order_by_distance(center, cluster):
    dists = calculate_ditances(center, cluster)
    dists = sorted(dists, key = lambda d: d[2])
    return ([(x,y) for (x,y,d) in dists], dists[0][2])


def segmentate(img):
    h = img.shape[0]
    w = img.shape[1]
    print("Segmenting image h:",h,", w:",w)
    mask = np.zeros((h,w), np.uint16)
    col = 1
    clusters = {}
    for y in range(0, w):
        for x in range(0, h):
            if mask[x, y] == 0: 
                nclust = find_segment(x, y, img, mask, h, w, col)
                clusters[col] = nclust
                col += 1
    return (clusters, mask)

def find_segments_borders(clusters, mask):
    h = mask.shape[0]
    w = mask.shape[1]
    border_clusters = []
    for col, cluster in clusters.items():
        (points, color) = cluster
        border_cluster = []
        for (x, y) in points:
            count = 0
            if x < h-1 and mask[x+1, y] == col: count +=1
            if x > 0 and mask[x-1, y] == col: count +=1
            if y < w-1 and mask[x, y+1] == col: count +=1
            if y > 0 and mask[x, y-1] == col: count +=1

            if count <= 3:
                border_cluster.append((x, y))
        border_clusters.append((border_cluster,color))
    return border_clusters


def get_surfaces(border_clusters, h, w):
    #bord_img = np.zeros((h,w,1), np.uint8)
    surfaces = []
    for (border_cluster, color) in border_clusters:
        surface = []
        point = border_cluster.pop(0)
        vector = [point]
        #bord_img[point[0], point[1]] = 255
        while len(border_cluster) > 0:
            (border_cluster, closest) = order_by_distance(point, border_cluster)
            point = border_cluster.pop(0)
            #print(closest)
            if closest < 2:
                vector.append(point)
            else:
                if math.dist(vector[0], vector[-1]) < 2: surface.append(vector)
                vector = [point]
            #bord_img[point[0], point[1]] = 255
            #cv2.imshow("output", bord_img)
            #cv2.waitKey(0)
        if len(vector) > 1 and math.dist(vector[0], vector[-1]): surface.append(vector)
        surfaces.append((surface, color))
    return surfaces
'''
surf_img = np.zeros((h,w,1), np.uint8)

surfaces = []

   for (x, y) in border_cluster:
     surf_img[x, y] = 255
   
   surface = []
   point = border_cluster.pop()
   surface.append(point)
   surf_img[point[0], point[1]] = 255
   while len(border_cluster) > 0:
       border_cluster = order_by_distance(point, border_cluster)
       ppoint = point
       point = border_cluster.pop()
       surface.append(point)
       surf_img[point[0], point[1]] = 255
       #surf_img = cv2.line(surf_img, ppoint, point, 255, 1)
   '''

#cv2.imshow("output", surf_img)
#cv2.waitKey(0)


'''
for border_cluster in border_clusters:
    (x, y) = calculate_center(border_cluster)
    borders[int(x), int(y)] = 255
    
    dists = calculate_ditances((x, y), border_cluster)
    dists = sorted(dists, key = lambda x: x[2])
    #borders[dists[0][0],dists[0][1]] = 255
    #borders[dists[1][0],dists[1][1]] = 255
    #borders[dists[2][0],dists[2][1]] = 255
    borders = cv2.line(borders, (dists[0][0],dists[0][1]), (dists[1][0],dists[1][1]), 255, 1)
    borders = cv2.line(borders, (dists[1][0],dists[1][1]), (dists[2][0],dists[2][1]), 255, 1)
    borders = cv2.line(borders, (dists[0][0],dists[0][1]), (dists[2][0],dists[2][1]), 255, 1)
'''


def main():
    args = sys.argv[1:]
    img = cv2.imread(args[0])

    h = img.shape[0]
    w = img.shape[1]

    #cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    #cv2.imshow("output", img)
    #cv2.waitKey(0)

    (clusters, mask) = segmentate(img)
    print("Segmentation done")
    
    border_clusters = find_segments_borders(clusters, mask)
    print("Finding borders done")
    
    surfaces = get_surfaces(border_clusters, h, w)
    print("Finding surfaces done")


    with open(args[1], "wb") as outfile:
        pickle.dump(surfaces, outfile)
        
    bord_img = np.zeros((h,w,3), np.uint8)
    for (surface, color) in surfaces:
        #col = 0
        #print(color)
        #if np.array_equal(color, [0,0,0]): col = 255
        #elif np.array_equal(color, [255,255,255]): col = 180
        for vector in surface:
            for (x,y) in vector:
                bord_img[x,y] = color
    cv2.imshow("output", bord_img)
    cv2.waitKey(0)
    
    
    '''
    for id, cluster in clusters.items():
      (points, color) = cluster
      print(color)
    cv2.imshow("output", mask)
    cv2.waitKey(0)
    '''

if __name__ == "__main__":
    sys.exit(main())