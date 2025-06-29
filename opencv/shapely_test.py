import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.geometry import LineString
from shapely.plotting import plot_polygon, plot_points, plot_line

#from figures import SIZE, BLUE, GRAY, RED, set_limits

import shapely
import pickle
import sys

import time

def to_rgba(color):
    #return [0 for x in color]
    return [x/255 for x in color]

def main():
    args = sys.argv[1:]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    data = None
    polygons = []
    with (open(args[0], "rb")) as openfile:
        data = pickle.load(openfile)
        
        for (surface, color) in data:
            i = 0
            extp = []
            intp = []
            
            for vector in surface:
                vector = vector + [vector[0]]
                if i == 0:
                    extp = vector[::-1]
                else:
                    intp.append(vector)
                i+=1
            polygon = Polygon(extp, intp)
            #polygon = polygon.simplify(tolerance=0.2)
            #polygons.append((polygon, to_rgba(color)))\
                #print(vector)
                #print(color)
                #line = LineString(vector)
                #plot_line(line, ax=ax, add_points=False, color=to_rgba(color), alpha=1)
            #plt.clf()

            plot_polygon(polygon, ax=ax, add_points=False, color=to_rgba(color))
            plot_points(polygon, ax=ax, color=[0.5,0.5,0.5], alpha=0.7)
            #fig.canvas.draw()
            #fig.canvas.flush_events()
    plt.show()
            #time.sleep(0.1)


    #for (polygon, color) in polygons:
    #    plot_polygon(polygon, ax=ax, add_points=False, color=color)
    #plt.show()


if __name__ == "__main__":
    sys.exit(main())