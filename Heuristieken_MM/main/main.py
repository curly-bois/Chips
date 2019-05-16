from Classes.point import Point
from init import *
from Data.make_data import *
from Data.make_plot import *
from connect import *
from Preprocessing.sort_connections import *
import numpy as np
import sys

counter = 0
netlistname = "netlist_2"
grid = grid_1
connections = get_connections(netlist_2)
gridpoints = make_grid(grid)

def disconnect_sets(sets_to_disconnect):
    for set in sets_to_disconnect:
        set.disconnect()

while counter < 1:
    # initializing the grid and making the points
    counter += 1
    matrix = make_matrix(gridpoints)
    to_be_connected = make_conlist(connections, matrix)

    all_sets, connected_sets, unconnected_sets = connect(make_order(to_be_connected))
    new_connections = []
    print(f"THIS MANY IS LEFT: {int(len(unconnected_sets) / len(all_sets) * 100)}%")

    # Breaks 15 % of connected sets and combines them with the unconnected sets to run the A algorithm on again

    ## Hier heb je toch al een lijst van --> Unconnected??
    for set in all_sets:
        if not set.is_it_connected():
            new_connections.append(set)

    hilltries = 0

    #
    # while len(unconnected_sets) > 0 and hilltries < 20:
    #     np.random.shuffle(connected_sets)
    #     hilltries += 1
    #     new_connections = []
    #     broken_sets = []
    #
    #     for set in unconnected_sets:
    #         new_connections.append(set)
    #
    #     ## Hard coded?
    #     sets_to_be_broken = int(len(connected_sets) * 0.2)
    #     for i in range(sets_to_be_broken):
    #         connected_sets[i].disconnect()
    #         new_connections.append(connected_sets[i])
    #         broken_sets.append(connected_sets[i])
    #         np.random.shuffle(new_connections)
    #     new_all_sets, new_connected_sets, new_unconnected_sets = connect(new_connections)
    #
    #     print(f"After this {int(len(new_unconnected_sets) / len(all_sets) * 100)}% is unconnected")
    #     if len(new_unconnected_sets) == 0:
    #         wire_pieces = 0
    #         for three_dimensions in matrix:
    #             for two_dimensions in three_dimensions:
    #                 for point in two_dimensions:
    #                     if point.get_attribute() == "wire":
    #                         wire_pieces += 1
    #         print(f"SOLUTION HAS BEEN FOUND after {hilltries} hillclimbs, IT TOOK {wire_pieces} pieces of wire")
    #         break
    #
    #     for set in new_connected_sets:
    #         set.disconnect()
    #
    #     for set in broken_sets:
    #         set.reconnect()


    make_plot(all_sets)
    make_xlsx(all_sets,matrix,netlistname)
