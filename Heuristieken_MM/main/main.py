from Classes.point import Point
from Data.make_data import *
from Data.make_plot import *
from Preprocessing.sort import *
from Preprocessing.init import *
from options.cli import *
from Algorithms.connect import *
from Algorithms.hillclimber import *
from Algorithms.dynamic import *
from Algorithms.collision import *
import numpy as np
import sys

# run the choice menu
A_star, order, iterative, options, tries, netlist, grid, evalutions = menu()

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
    solved_sets = simulsolve(500, all_sets, connected_sets, unconnected_sets, matrix)

    # choosing the iterative algorithm
    if iterative == 1:
        hillimprove(100, all_sets)
    elif iterative == 2:
        simulated_annealing(100, all_sets)
    else:
        pass

    # Check for collisions
    collisions = collision_check(all_sets)

    # extra options
    if 1 in options:
        make_plot(all_sets)
    if 2 in options:
        make_xlsx(all_sets, matrix, f"netlist_{netlist}", collisions, "initial try")
