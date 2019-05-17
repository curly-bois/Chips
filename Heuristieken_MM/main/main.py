from Classes.point import Point
from init import *
from Data.make_data import *
from Data.make_plot import *
from connect import *
from Preprocessing.sort_connections import *
from hillclimber import *
import numpy as np
import sys

# netlists = [netlist_1,netlist_2,netlist_3,netlist_4,netlist_5,netlist_6]
# grids = [grid_1,grid_2]
#
# for i , netlist in enumerate(netlists):
#     if i > 2:
#         grid = grid_2
#         print(i)
#     else:
#         grid = grid_1
#         print(i)

counter = 0
netlistname = f"netlist_1"
connections = get_connections(netlist_4)
gridpoints = make_grid(grid_2)

while counter < 1:
    matrix = make_matrix(gridpoints)
    to_be_connected = make_conlist(connections, matrix)
    to_be_connected = make_order(to_be_connected)
    exit()

    all_sets, connected_sets, unconnected_sets = connect(to_be_connected)
    new_connections = []
    make_plot(all_sets)

    if len(unconnected_sets) == 0:
        # hillimprove(100, all_sets)
        # simulated_annealing(100, solved_sets, 30)
        print("eerste try")
        make_plot(connected_sets)
        make_xlsx(all_sets,connected_sets,matrix,netlistname,unconnected_sets)
    else:
        print("niet eerste try")
        # solved_sets = hillsolve(50, matrix, all_sets, unconnected_sets, connected_sets)
        # make_plot(solved_sets)
        # hillimprove(100, solved_sets)
        # simulated_annealing(100, solved_sets, 30)
    #   make_plot(solved_sets)
        make_xlsx(all_sets,connected_sets,matrix,netlistname,unconnected_sets)
    # print(counter)
    counter += 1
