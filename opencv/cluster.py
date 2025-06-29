from sklearn.cluster import KMeans
import numpy as np
import statistics
import cv2
import sys
import os


def cluster(img, n_clusters):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.namedWindow("result", cv2.WINDOW_NORMAL)
    cv2.imshow("result", gray)

    X = gray.reshape(-1, 1)

    print("Start k-means")
    kmeans = KMeans(n_clusters=n_clusters).fit(X)
    print("End k-means")
    #print(kmeans.cluster_centers_)
    #print(kmeans.labels_)

    h = img.shape[0]
    w = img.shape[1]
    result = np.zeros((h,w,1), np.uint8)
    repls = []

    print("Calculating reps")
    for c in range(n_clusters):
        pixels = []
        for i in range(len(kmeans.labels_)):
            if kmeans.labels_[i] == c: pixels.append(int(X[i,0]))
        print("Calculating mode for center "+str(c+1))
        repls.append(statistics.mode(pixels))
        print("Mode calculated for center "+str(c+1))

    for i in range(len(kmeans.labels_)):
        result[int(i/w), i%w] = repls[kmeans.labels_[i]]
        #print(int(i/w), i%w, i)
    return result


def main():
    args = sys.argv[1:]
    img = cv2.imread(args[0])
    result = cluster(img, int(args[1]))

    if os.path.isdir(args[2]):
        filename = os.path.basename(args[0])
        cv2.imwrite(os.path.join(args[2], filename), result)
    elif os.path.isfile(args[2]):
        cv2.imwrite(args[2], result)

    cv2.namedWindow("result2", cv2.WINDOW_NORMAL)
    cv2.imshow("result2", result)
    cv2.waitKey(0)

if __name__ == "__main__":
    sys.exit(main())