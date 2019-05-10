from point import Point
from init import *
from make_data import *
from connect import *

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import sys

counter = 0
row = 221
connections = get_connections(netlist_5)
gridpoints = make_grid(grid_2)

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
    print(f"THIS MANY ARE LEFT: {len(unconnected_sets)}")

    #  make the plot
    '''
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
    '''
    # plt.show()



    # print(f"After the first try {len(unconnected_sets)} are unconnected")

    # Breaks 15 % of connected sets and combines them with the unconnected sets to run the A algorithm on again

    for set in all_sets:
        if not set.is_it_connected():
            new_connections.append(set)

    hilltries = 0

    testlist = []
    testlist.append(connected_sets[0])
    connected_sets[0].disconnect()
    print(f"this set that was once in connected_sets is now {connected_sets[0].is_it_connected()} and this set in testlist should be the same and is {testlist[0].is_it_connected()}")
    testlist[0].reconnect()
    print(f"this set that was once in connected_sets is now {connected_sets[0].is_it_connected()} and this set in testlist should be the same and is {testlist[0].is_it_connected()}")


    while len(unconnected_sets) > 0 and hilltries < 50:
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
            print(f"SOLUTION HAS BEEN FOUND after {hilltries} hillclimbs")
            break

        for set in new_all_sets:
            set.disconnect()

        for set in broken_sets:
            set.reconnect()