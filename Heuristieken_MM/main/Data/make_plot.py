from Classes.point import Point
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np



def make_plot(all_sets):
    # make the plot
    dot = []
    routes = []

    for set in all_sets:
        dot.append(set.get_startpoint().get_location())
        dot.append(set.get_endpoint().get_location())
        if set.is_it_connected():
            route = set.get_route()
            routearr = []
            routearr.append(set.get_startpoint().get_location())
            for point in route:
                routearr.append(point.get_location())
            routearr.append(set.get_endpoint().get_location())
            routes.append(routearr)

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_zlim(0, 6)
    for route in routes:
        linex, liney, linez, = zip(*route)
        ax.plot(linex, liney, linez, linewidth=3, color='blue')
    ax.scatter3D(*zip(*dot),linewidth=4,color = "red")
    plt.show()
