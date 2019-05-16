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
netlistname = "netlist_1"
grid = grid_1
connections = get_connections(netlist_1)
gridpoints = make_grid(grid)

while counter < 1:
    # initializing the grid and making the points
    counter += 1

    matrix = make_matrix(gridpoints)
    to_be_connected = make_conlist(connections, matrix)
    np.random.shuffle(to_be_connected)

    all_sets, connected_sets, unconnected_sets = connect(to_be_connected)
    new_connections = []
    print(f"THIS MANY IS LEFT: {int(len(unconnected_sets) / len(all_sets) * 100)}%")

<<<<<<< HEAD
if len(unconnected_sets) == 0:
    # hillimprove(100, all_sets)
    simulated_annealing(100, solved_sets, 30)
    print("eerste try")
    make_plot(connected_sets)
    make_xlsx(connected_sets,matrix,netlistname)
else:
    print("niet eerste try")
    solved_sets = hillsolve(50, matrix, all_sets, unconnected_sets, connected_sets)
    make_plot(solved_sets)
    # hillimprove(100, solved_sets)
    simulated_annealing(100, solved_sets, 30)
    make_plot(solved_sets)
    make_xlsx(solved_sets,matrix,netlistname)
=======
    if len(unconnected_sets) == 0:
        print("eerste try")
        make_xlsx(connected_sets,matrix,netlistname)
<<<<<<< HEAD

    make_plot(connected_sets)
    # else:
    #     print("niet eerste try")
    #     solved_sets = hillsolve(50, matrix, all_sets, unconnected_sets, connected_sets)
    #     make_plot(solved_sets)
    #     make_xlsx(solved_sets,matrix,netlistname)
=======
    else:
        print("niet eerste try")
        solved_sets = hillsolve(25, matrix, all_sets, unconnected_sets, connected_sets)
        make_plot(solved_sets)
        make_xlsx(solved_sets,matrix,netlistname)
>>>>>>> 0a15de1b59e2cedc286aca75e792cfa1c21a1092
>>>>>>> f12d17939e1b5c5f18c3eac32e41f8edef83052d
