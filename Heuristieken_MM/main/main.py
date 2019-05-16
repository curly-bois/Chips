from Classes.point import Point
from init import *
from Data.make_data import *
from connect import *
from Preprocessing.sort_connections import *
from hillclimber import *
# !!! hillclimb steeds duurste weghalen of andere heuristieken
# !!! vanuit terminal kunnen kiezen hoe je het runt
# !!! alles in functies en modulair
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import sys

counter = 0
connections = get_connections(netlist_6)
gridpoints = make_grid(grid_2)

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

solved_sets = hillsolve(50, matrix, all_sets, unconnected_sets, connected_sets)
