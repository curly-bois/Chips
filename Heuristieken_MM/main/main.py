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

# max_tries = int(input("How many times do you want to run the program?"))
# netlist = input("Which netlist? choose 'netlist_1' until 'netlist_6'")
# print(netlist)
# input("Do you want to use an iterative algorithm that tries to find a random solution?")
# input("If a solution was found, do you want to use an iterative algorithm to improve that solution?")
# input("Choose between 'hill climber' or 'simulated annealing'")
# input("Do you want to turn on dynamic heuristics?")




counter = 0
netlistname = "netlist_1"
grid = grid_1
connections = get_connections(netlist_1)
gridpoints = make_grid(grid)

while counter < 1:
    counter += 1
    matrix = make_matrix(gridpoints,connections)
    to_be_connected = make_conlist(connections, matrix)
    # to_be_connected = make_order(to_be_connected)
    to_be_connected = new_order(to_be_connected)


    # A algorithm
    all_sets, connected_sets, unconnected_sets = connect(to_be_connected)
    new_connections = []

    if len(unconnected_sets) == 0:
        # make_plot(connected_sets)
        #
        # Dynamic turns off heuristic values
        # dynamic(matrix)
        # hillimprove(100, all_sets)
        # simulated_annealing(100, all_sets, 30)
        # print("eerste try")
        # make_plot(connected_sets)
        make_xlsx(all_sets,matrix,netlistname, "initial try")
    else:
        print("niet eerste try")
        solved_sets = simulsolve(500, all_sets, connected_sets, unconnected_sets, matrix)


        print(len(solved_sets))
        # make_plot(solved_sets)
        print(len(solved_sets))
        make_xlsx(all_sets,matrix,netlistname, "initial try")
        # make_plot(connected_sets)
        hillimprove(500, solved_sets)
        make_xlsx(all_sets,matrix,netlistname, "with hillimprove not dynamic")
        # dynamic(matrix)
        # if solved_sets != None:
        #     simulated_annealing(100, solved_sets, 30)

        collisions = 0
        all_locations = []
        for set in all_sets:
            for routepoint in set.get_route():
                if routepoint.get_location() in all_locations:
                    collisions += 1
                    all_locations.append(routepoint.get_location())
        print(f"END OF PROGRAM, AMOUNT OF COLLISIONS: {collisions}")
