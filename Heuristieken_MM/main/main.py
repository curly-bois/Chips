from Classes.point import Point
from init import *
from Data.make_data import *
from Data.make_plot import *
from connect import *
from dynamic import *
from Preprocessing.sort_connections import *
from collision import *
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
netlistname = "netlist_6"
grid = grid_2
connections = get_connections(netlist_6)
gridpoints = make_grid(grid)

while counter < 1:
    counter += 1
    matrix = make_matrix(gridpoints)
    to_be_connected = make_conlist(connections, matrix)
    to_be_connected = make_order(to_be_connected)

    # dynamic(matrix)

    # A algorithm
    all_sets, connected_sets, unconnected_sets = connect(to_be_connected)
    print("")
    print(f"Using A*, you managed to connect {len(connected_sets) / len(all_sets) * 100}% of the netlist :(")
    make_plot(all_sets)
    exit()
    print(len(all_sets))
    new_connections = []

    if len(unconnected_sets) == 0:

        # Collision check
        collisions = collision_check(all_sets)

        print(f"AMOUNT OF COLLISIONS: {collisions}")





        # make_plot(connected_sets)
        #
        # Dynamic turns off heuristic values
        # dynamic(matrix)
        # hillimprove(100, all_sets)
        # simulated_annealing(100, all_sets, 30)
        # print("eerste try")
        # make_plot(connected_sets)

        dynamic(matrix)
        simulated_annealing(900, all_sets)
        # Collision check
        collisions = collision_check(all_sets)

        print(f"AMOUNT OF COLLISIONS: {collisions}")

        make_xlsx(all_sets,matrix,netlistname, "hillclimb 900 evaluations + dynamic")
    else:
        print("niet eerste try")
        solved_sets = simulsolve(500, all_sets, connected_sets, unconnected_sets, matrix)

        # Collision check
        collisions = collision_check(all_sets)

        print(f"AMOUNT OF COLLISIONS: {collisions}")

        dynamic(matrix)
        simulated_annealing(900, all_sets)
        # Collision check
        collisions = collision_check(all_sets)

        print(f"AMOUNT OF COLLISIONS: {collisions}")

        make_xlsx(all_sets,matrix,netlistname, "hillclimb 900 evaluations + dynamic")
