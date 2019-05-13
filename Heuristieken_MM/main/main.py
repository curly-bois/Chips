from Classes.point import Point
from init import *
from Data.make_data import *
from connect import *
from Preprocessing.sort_connections import *

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import sys

counter = 0
connections = get_connections(netlist_1)
gridpoints = make_grid(grid_1)

def disconnect_sets(sets_to_disconnect):
    for set in sets_to_disconnect:
        set.disconnect()

while counter < 1:
    # initializing the grid and making the points
    counter += 1
    matrix = make_matrix(gridpoints)
    to_be_connected = make_conlist(connections, matrix)

    all_sets, connected_sets, unconnected_sets = connect(to_be_connected)
    new_connections = []
    print(f"THIS MANY IS LEFT: {int(len(unconnected_sets) / len(all_sets) * 100)}%")

    # Breaks 15 % of connected sets and combines them with the unconnected sets to run the A algorithm on again

    for set in all_sets:
        if not set.is_it_connected():
            new_connections.append(set)

    hilltries = 0


    while len(unconnected_sets) > 0 and hilltries < 20:
        np.random.shuffle(connected_sets)
        hilltries += 1
        new_connections = []
        broken_sets = []

        for set in unconnected_sets:
            new_connections.append(set)

        sets_to_be_broken = int(len(connected_sets) * 0.2)
        for i in range(sets_to_be_broken):
            connected_sets[i].disconnect()
            new_connections.append(connected_sets[i])
            broken_sets.append(connected_sets[i])
        new_all_sets, new_connected_sets, new_unconnected_sets = connect(new_connections)

        print(f"After this {int(len(new_unconnected_sets) / len(all_sets) * 100)}% is unconnected")
        if len(new_unconnected_sets) == 0:
            wire_pieces = 0
            for three_dimensions in matrix:
                for two_dimensions in three_dimensions:
                    for point in two_dimensions:
                        if point.get_attribute() == "wire":
                            wire_pieces += 1
            print(f"SOLUTION HAS BEEN FOUND after {hilltries} hillclimbs, IT TOOK {wire_pieces} pieces of wire")



        #  make the plot

        wires = []
        taken = []
        wire_pieces = 0
        for three_dimensions in matrix:
            for two_dimensions in three_dimensions:
                for point in two_dimensions:
                    if point.get_attribute() == "wire":
                        wires.append(point.location)
                        wire_pieces += 1
                    if point.get_attribute() == "taken" or point.get_attribute() == "gate":
                        taken.append(point.location)


        routes = []
        for set in connected_sets:
            route = set.get_route()
            routearr = []
            for point in route:
                routearr.append(point.get_location())
            routes.append(routearr)

        fig = plt.figure()
        ax = plt.axes(projection='3d')

        for route in routes:
            if len(route) > 0:
                linex, liney, linez, = zip(*route)
                ax.plot(linex, liney, linez, linewidth=3, color='blue')

        ax.set_zlim(0, 6)
        ax.scatter3D(*zip(*wires))
        ax.scatter3D(*zip(*taken))
        plt.show()


        for set in new_connected_sets:
            set.disconnect()

        for set in broken_sets:
            set.reconnect()

     # make the plot
    taken = []
    routes = []
    for set in all_sets:
        taken.append(set.startpoint.location)
        taken.append(set.endpoint.location)

    for set in connected_sets:
        route = set.get_route()
        routearr = []
        for point in route:
            routearr.append(point.get_location())
        routes.append(routearr)

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_zlim(0, 6)
    for route in routes:
        if len(route) > 0:
            linex, liney, linez, = zip(*route)
            ax.plot(linex, liney, linez, linewidth=3, color='blue')

    # ax.scatter3D(*zip(*wires))
    ax.scatter3D(*zip(*taken),linewidth=4,color = "red")
    plt.show()
