from sklearn.cluster import KMeans
import numpy as np
import statistics
import logging
import math
import cv2
import sys
import os

from core import GraphicObject, Point, PointSequence, Surface

def order_by_distance(center, cluster):
    dists = calculate_ditances(center, cluster)
    dists = sorted(dists, key = lambda d: d[2])
    return ([(x,y) for (x,y,d) in dists], dists[0][2])

def sort_by_distance(center, cluster):
    dists = calculate_ditances(center, cluster)
    return sorted(dists, key = lambda d: d[2])

def calculate_ditances(center, cluster):
    dists = []
    (cx, cy) = (center[0], center[1]) 
    for p in cluster:
       x, y = p[0], p[1]
       dists.append((x, y, math.dist([cx, cy],[x, y])))
    return dists

def cluster(img, n_clusters):
    '''
     Finds clusters un image:
     Receives:
         img as nparray, 
         n_clusters as int > 0
    '''
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    X = gray.reshape(-1, 1)

    #logging.debug("Start k-means")
    kmeans = KMeans(n_clusters=n_clusters).fit(X)
    #logging.debug("End k-means")

    h = img.shape[0]
    w = img.shape[1]
    result = np.zeros((h,w,1), np.uint8)
    repls = []

    #logging.debug("Calculating reps")
    for c in range(n_clusters):
        pixels = []
        for i in range(len(kmeans.labels_)):
            if kmeans.labels_[i] == c: pixels.append(int(X[i,0]))
        #logging.debug("Calculating mode for center "+str(c+1))
        repls.append(statistics.mode(pixels))
        #logging.debug("Mode calculated for center "+str(c+1))

    for i in range(len(kmeans.labels_)):
        result[int(i/w), i%w] = repls[kmeans.labels_[i]]
    #logging.debug("Kmeans finished")
    return result


def find_segment(nx, ny, img, mask, h, w, col):
    '''
    Finds a segment with the same color specified on pixel (nx, ny) on the image img.
    It only considers pixels where their value are 0 on the mask. 
    '''
    #logging.debug(img)
    tmp = [(nx, ny)]
    resp = [(nx, ny)]
    color = img[nx, ny]
    mask[nx, ny] = col
    #logging.debug(color)
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
    logging.debug("Segmenting image h: %s w: %s",h,w)
    mask = np.zeros((h,w), np.uint16)
    col = 60
    clusters = {}
    for y in range(0, w):
        for x in range(0, h):
            if mask[x, y] == 0:
                nclust = find_segment(x, y, img, mask, h, w, col)
                clusters[col] = nclust
                col += 1
                
    #cv2.imshow("output", mask)
    logging.debug("Segmented image")
    logging.debug("Clusters found: "+str(len(clusters)))
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
        border_clusters.append((border_cluster, color))
        #logging.debug(border_cluster)
        #logging.debug(color)
    return border_clusters


def get_surfaces(border_clusters):
    '''
    Find the surfaces as an array of closed vectors
    Returns a structure [([vector],color),] where vector is a set of points [(x,y),] where each point
    is interconected with the next and vector[0] is interconected with vector[-1]
    '''
    #surfaces = points_to_surface_naive(border_clusters)
    surfaces = points_to_surface_exp(border_clusters)
    return GraphicObject("Test Paintable Object", None, surfaces)


def points_to_surface_exp(border_cluster):
    surfaces = []
    i=1

    def disentangle(point, border_cluster, candidate, cost):
        border_cluster = sort_by_distance(point, border_cluster)
        
        if len(border_cluster) > 1 and border_cluster[1][2] >= 2:
            return (candidate, cost, border_cluster)
        
        cnt = 0
        best_cost = float("inf")
        best_candidate = None
        best_border_cluster = None
        while cnt < len(border_cluster) and border_cluster[cnt][2] < 2:
            border_cluster_copy = border_cluster.copy()
            new_candidate = candidate.copy()
            pnt = border_cluster_copy.pop(cnt)
            new_candidate.append(pnt)
            (tmp_cand, tmp_cost, tmp_border_cluster) = disentangle(pnt, border_cluster_copy, new_candidate, cost+pnt[2])
            if tmp_cost < best_cost:
                best_cost = tmp_cost
                best_candidate = tmp_cand
                best_border_cluster = tmp_border_cluster
            cnt += 1
        return (best_candidate, best_cost, best_border_cluster)


    
    point = border_cluster.pop(0)
    surface = [point]
    while len(border_cluster) > 0:
        border_cluster = sort_by_distance(point, border_cluster)
        cnt = 0
        while cnt < len(border_cluster) and border_cluster[cnt][2] < 2:
            cnt+=1
        if cnt > 2:
            (best, _, border_cluster) = disentangle(point, border_cluster, [], 0)
            border_cluster = border_cluster[len(best):]
            surface.extend([(p[0], p[1]) for p in best])
            point = best[-1]
            print("Step 1, rec", surfaces, surface, best, point)
        elif cnt == 1:
            point = border_cluster.pop(0)
            surface.append((point[0], point[1]))
            print("Step 2, cnt 1", surfaces, surface, point)
        else:
            surfaces.append(surface)
            point = border_cluster.pop(0)
            surface = [(point[0], point[1])]
            print("Step 3, cnt 0", surfaces, surface, point)
    if len(surface) > 1: surfaces.append(surface)
    print("Result", surfaces)  
    return surfaces


    '''
    def border_cluster_to_surface(border_cluster, cost):
        surface = []
        point = border_cluster.pop(0)
        vector = [(point[0], point[1])]
        
        while len(border_cluster) > 0:
            border_cluster = sort_by_distance(point, border_cluster)
            indx = 1
            
            while len(border_cluster) > 1 and border_cluster[indx] < 2:
                ncand = border_cluster_to_surface(border_cluster.copy(), cost + )
            

            point = border_cluster.pop(0)
            if dist < 2:
                vector.append((point[0], point[1]))
            else:
                if len(vector) > 1:  # and math.dist(vector[0], vector[-1]) < 2
                    surface.append(vector)
                vector = [(point[0], point[1])]
                
        if len(vector) > 1: #and math.dist(vector[0], vector[-1]) < 2
            surface.append(vector)

        return (cost, surface)
    
    for (border_cluster, color) in border_clusters:
        (cost, surface) = border_cluster_to_surface(border_cluster, 0)
        if len(surface) > 0:
            surfaces.append(Surface("Surface "+str(i), PointSequence([Point(x, y) for (x, y) in surface[0]]), [PointSequence([Point(x, y) for (x, y) in s]) for s in surface[1:]], color))
            i+=1
    return surfaces
    '''

def points_to_surface_naive(border_clusters):
    surfaces = []
    i=1
    print("border_cluster: "+str(len(border_clusters)))
    for (border_cluster, color) in border_clusters:
        surface = []
        point = border_cluster.pop(0)
        vector = [point]
        
        #print("Border:"+str(i+1))
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

        #print(vector)
        
        if len(vector) > 1: #and math.dist(vector[0], vector[-1]) < 2
            surface.append(vector)
        if len(surface) > 0:
            surfaces.append(Surface("Surface "+str(i), PointSequence([Point(x, y) for (x, y) in surface[0]]), [PointSequence([Point(x, y) for (x, y) in s]) for s in surface[1:]], color))
            i+=1
    return surfaces

def borders_to_image(border_clusters, h, w):
    bord_img = np.zeros((h,w,3), np.uint8)
    for border_cluster, color in border_clusters:
      for (x, y) in border_cluster:
         bord_img[x, y] = color
    return bord_img

def image_grey_to_color(grey):
    (h, w) = grey.shape
    resp = np.zeros((h ,w), np.uint8)
    resp = (grey[:]*5 + 50)%255
    return cv2.cvtColor(resp, cv2.COLOR_GRAY2RGB)

def mask_to_color(mask):
    grey = mask.astype(np.uint8)
    return cv2.cvtColor(grey, cv2.COLOR_GRAY2RGB)

def find_surfaces(img):
    (clusters, mask) = segmentate(img)





if __name__ == '__main__':
    #print(points_to_surface_exp([]))
    #print(points_to_surface_exp([(2,1)]))
    #print(points_to_surface_exp([(2,1), (1,1)]))
    #print(points_to_surface_exp([(2,1), (1,1), (4,1), (5,1)]))
    print(points_to_surface_exp([(1,2), (2,1), (1,1), (3,1), (3,2), (3,3), (2,3), (1,3), (1,5), (1,6), (2,6), (2,5), (1,9), (1,10)]))
    
