from Classes.point import Point
from Classes.set import Set
from init import *
from Data.make_data import *
from connect import *

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import sys

counter = 0
row = 221
connections = get_connections(netlist_1)
gridpoints = make_grid(grid_1)

def disconnect_sets(sets_to_disconnect):
    for set in sets_to_disconnect:
        set.disconnect()

while counter < 1:
    # initializing the grid and making the points

    matrix = make_matrix(gridpoints)
    to_be_connected = make_conlist(connections, matrix)

    all_sets, connected_sets, unconnected_sets = connect(to_be_connected)

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

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_zlim(0, 6)
    ax.scatter3D(*zip(*wires))
    ax.scatter3D(*zip(*taken))
    # plt.show()



    print(f"After the first try {len(unconnected_sets)} are unconnected")

    # Breaks 15 % of connected sets and combines them with the unconnected sets to run the A algorithm on again

    hilltries = 0

    while len(unconnected_sets) > 0 and hilltries < 20:
        hilltries += 1
        new_connections = []

        for set in all_sets:
            if not set.is_it_connected():
                new_connections.append(set)

        sets_to_be_broken = int(len(connected_sets) * 0.1)
        for i in range(sets_to_be_broken):
            connected_sets[i].disconnect()
            new_connections.append(connected_sets[i])


        all_sets, connected_sets, unconnected_sets = connect(new_connections)

        print(f"After this {len(unconnected_sets)} are unconnected")

        counter += 1
