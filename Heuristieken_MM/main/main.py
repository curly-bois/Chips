from Classes.point import Point
from init import *
from Data.make_data import *
from Data.make_plot import *
from connect import *
from dynamic import *
from Preprocessing.sort_connections import *
from hillclimber import *
import numpy as np
import sys

counter = 0
netlistname = "netlist_2"
grid = grid_1
connections = get_connections(netlist_2)
gridpoints = make_grid(grid)
print(len(connections))
while counter < 1:
    print(f"CURRENT LOOP: {counter}")
    # initializing the grid and making the points
    counter += 1

    matrix = make_matrix(gridpoints)
    to_be_connected = make_conlist(connections, matrix)

    print(len(to_be_connected))

    np.random.shuffle(to_be_connected)

    # A algorithm
    all_sets, connected_sets, unconnected_sets = connect(to_be_connected)
    print(len(all_sets))
    new_connections = []

    if len(unconnected_sets) == 0:
        make_plot(connected_sets)

        # Dynamic turns off heuristic values
        dynamic(matrix)
        # hillimprove(100, all_sets)
        simulated_annealing(100, all_sets, 30)
        print("eerste try")
        make_plot(connected_sets)
        make_xlsx(all_sets,connected_sets,matrix,netlistname,unconnected_sets)
    else:
        print("niet eerste try")
        solved_sets = hillsolve(50, matrix, all_sets, unconnected_sets, connected_sets)
        print(len(solved_sets))

        # make_plot(connected_sets)
        make_plot(solved_sets)
        # hillimprove(100, solved_sets)
        dynamic(matrix)
        if solved_sets != None:
            simulated_annealing(100, solved_sets, 30)
            make_plot(solved_sets)
            print(len(solved_sets))
            make_xlsx(all_sets,connected_sets,matrix,netlistname,unconnected_sets)
