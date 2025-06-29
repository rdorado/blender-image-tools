import cv2
import numpy as np
import pickle
import math
import sys
import os

def add_border(img, x, y, bwidth):
    '''
    Add a border to the image
    '''
    w = img.shape[0]
    h = img.shape[1]
    color = img[x,y]

    img = cv2.copyMakeBorder(img,bwidth,bwidth,bwidth,bwidth,cv2.BORDER_CONSTANT,value=0)

    for i in range(bwidth):
        img[i,:] = color
        img[w+bwidth+i:] = color
        img[:,i] = color
        img[:,h+bwidth+i] = color
    return img

def find_segment(nx, ny, img, mask, h, w, col):
    '''
    Finds a segment with the same color specified on pixel (nx, ny) on the image img.
    It only considers pixels where their value are 0 on the mask. 
    '''
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


def segmentate(img):
    '''
      Segments the image, returns:
      clusters: a dictionary containing an id: [points] for each cluster.
      mask: the masked image where each pixel has been replaced by cluster_id
      Returns: clusters as a dict construct {id: cluster}, where cluster is ([(points),], color)
    '''
    h = img.shape[0]
    w = img.shape[1]
    print("Segmenting image h:",h,", w:",w)
    mask = np.zeros((h,w), np.uint16)
    col = 130
    clusters = {}
    for y in range(0, w):
        for x in range(0, h):
            if mask[x, y] == 0: 
                nclust = find_segment(x, y, img, mask, h, w, col)
                clusters[col] = nclust
                col += 1
    return (clusters, mask)


def find_segments_borders(clusters, mask):
    '''
     Finds the pixels on the borders of the regions defined on the mask.
     Returns a structure [([(points),],color),]
    '''
    h = mask.shape[0]
    w = mask.shape[1]
    border_clusters = []
    for idc, cluster in clusters.items():
        (points, color) = cluster
        border_cluster = []
        for (x, y) in points:
            count = 0
            if x < h-1 and mask[x+1, y] == idc: count +=1
            if x > 0 and mask[x-1, y] == idc: count +=1
            if y < w-1 and mask[x, y+1] == idc: count +=1
            if y > 0 and mask[x, y-1] == idc: count +=1

            if count <= 3:
                border_cluster.append((x, y))
        border_clusters.append((border_cluster,color))
    return border_clusters

def get_surfaces(border_clusters, h, w):
    '''
    Find the surfaces as an array of closed vectors
    Returns a structure [([vector],color),] where vector is a set of points [(x,y),] where each point
    is interconected with the next and vector[0] is interconected with vector[-1]
    '''
    surfaces = []
    i=0
    for (border_cluster, color) in border_clusters:
        surface = []
        point = border_cluster.pop(0)
        vector = [point]
        
        print("Border:"+str(i+1))
        i+=1
        while len(border_cluster) > 0:
            (border_cluster, closest) = order_by_distance(point, border_cluster)
            point = border_cluster.pop(0)
            if closest < 2:
                vector.append(point)
            else:
                if len(vector) > 1:  # and math.dist(vector[0], vector[-1]) < 2
                    print("Middle: "+str(len(vector)))
                    surface.append(vector)
                vector = [point]
        print(vector)
        print("Last: "+str(len(vector)))
        if len(vector) > 1: #and math.dist(vector[0], vector[-1]) < 2
            surface.append(vector)
        if len(surface) > 0: surfaces.append((surface, color))
    return surfaces

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


def main():
    args = sys.argv[1:]
    img = cv2.imread(args[0])

    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    cv2.imshow("output", img)
    cv2.waitKey(0)

    img = add_border(img, 0, 0, 3)

    cv2.imshow("output", img)
    cv2.waitKey(0)

    (clusters, mask) = segmentate(img)
    print("Segmentation done")
    
    cv2.imshow("output", mask)
    cv2.waitKey(0)
    
    print("Finding borders...")
    border_clusters = find_segments_borders(clusters, mask)
    print("Finding borders done")
    print("Number of border clusters: "+str(len(border_clusters)))
    
    h = img.shape[0]
    w = img.shape[1]
    bord_img = np.zeros((h,w,3), np.uint8)
    for border_cluster, color in border_clusters:
      for (x, y) in border_cluster:
         bord_img[x, y] = color

    cv2.imshow("output", bord_img)
    cv2.waitKey(0)


    print("Finding surfaces...")
    surfaces = get_surfaces(border_clusters, h, w)
    print("Finding surfaces done")

    bord_img = np.zeros((h,w,3), np.uint8)
    print("Number of surfaces found: "+str(len(surfaces)))
    for (surface, color) in surfaces:
        print("Number of vector found: "+str(len(surface)))
        for vector in surface:
            for (x,y) in vector:
                bord_img[x,y] = [255,255,255]
            print(vector)
            print(color)
    cv2.imshow("output", bord_img)
    cv2.waitKey(0)


    outfilename = args[1]
    if os.path.isdir(args[1]):
        outfilename = os.path.join(args[1], os.path.basename(args[0])[:-4]+".dat")
    
    print("Saving to file...")
    with open(outfilename, "wb") as outfile:
        pickle.dump(surfaces, outfile)
    print("Saving to file done")


if __name__ == "__main__":
    sys.exit(main())