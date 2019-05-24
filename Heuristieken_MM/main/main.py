from Classes.point import Point
from init import *
from Data.make_data import *
from Data.make_plot import *
from cli import menu
from connect import *
from dynamic import *
from Preprocessing.sort import *
from hillclimber import *
import numpy as np
import sys

# run the choice menu
A_star,order,iterative,options,tries, netlist, grid = menu()

counter = 0

while counter < tries:
    counter +=1
    # make the points and sets ready
    connections = get_connections(netlist)
    gridpoints = make_grid(grid)
    matrix = make_matrix(gridpoints,connections)
    to_be_connected = make_conlist(connections, matrix)

    # choosing type of A-algorithm
    if A_star == 1:
        # Dynamic turns off heuristic values
        dynamic(matrix)
    elif A_star == 2:
        # keep A_STAR heuristics on
        pass


    # choosing the order type
    if order == 1:
        to_be_connected = dir_order(to_be_connected,"random")
    elif order == 2:
        to_be_connected = appearence_order(to_be_connected)
    else:
        np.random.shuffle(to_be_connected)

    # make wires from gate to gate
    all_sets, connected_sets, unconnected_sets = connect(to_be_connected)

    # choosing the iterative algorithm
    if iterative == 1:
        solved_sets = simulsolve(500, all_sets, connected_sets, unconnected_sets, matrix)
    elif iterative == 2:
        simulated_annealing(100, all_sets, 30)
    else:
        pass

    # extra options
    if 1 in options:
        make_plot(all_sets)
    if 2 in options:
        make_xlsx(all_sets,matrix,f"netlist_{netlist}", "initial try")

# new_connections = []
#
# if len(unconnected_sets) == 0:
#     # make_plot(connected_sets)
#     #
#     # Dynamic turns off heuristic values
#     # dynamic(matrix)
#     # hillimprove(100, all_sets)
#     # simulated_annealing(100, all_sets, 30)
#     # print("eerste try")
#     # make_plot(connected_sets)
#     make_xlsx(all_sets,matrix,netlistname, "initial try")
# else:
#     print("niet eerste try")
#
#
#
#     print(len(solved_sets))
#     # make_plot(solved_sets)
#     print(len(solved_sets))
#     make_xlsx(all_sets,matrix,netlistname, "initial try")
#     # make_plot(connected_sets)
#     hillimprove(500, solved_sets)
#     make_xlsx(all_sets,matrix,netlistname, "with hillimprove not dynamic")
#     # dynamic(matrix)
#     # if solved_sets != None:
#     #     simulated_annealing(100, solved_sets, 30)
#
#     collisions = 0
#     all_locations = []
#     for set in all_sets:
#         for routepoint in set.get_route():
#             if routepoint.get_location() in all_locations:
#                 collisions += 1
#                 all_locations.append(routepoint.get_location())
#     print(f"END OF PROGRAM, AMOUNT OF COLLISIONS: {collisions}")
