from Classes.point import Point
from init import *
from Data.make_data import *
from Data.make_plot import *
from connect import *
from Preprocessing.sort_connections import *
from hillclimber import *
import numpy as np
import sys

counter = 0
netlistname = "netlist_6"
grid = grid_2
connections = get_connections(netlist_6)
gridpoints = make_grid(grid)

while counter < 1:
    # initializing the grid and making the points
    counter += 1

    matrix = make_matrix(gridpoints)
    to_be_connected = make_conlist(connections, matrix)

    all_sets, connected_sets, unconnected_sets = connect(make_order(to_be_connected))
    new_connections = []
    print(f"THIS MANY IS LEFT: {int(len(unconnected_sets) / len(all_sets) * 100)}%")

if len(unconnected_sets) == 0:
    print("eerste try")
    make_plot(connected_sets)
    make_xlsx(connected_sets,matrix,netlistname)
else:
    print("niet eerste try")
    solved_sets = hillsolve(50, matrix, all_sets, unconnected_sets, connected_sets)
    make_plot(solved_sets)
    make_xlsx(solved_sets,matrix,netlistname)
