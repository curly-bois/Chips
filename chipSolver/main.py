# Classes
from point import Point
from grid import Grid
from wire import Wire

# Own modules
from extra import *
from settings import *
from data import get_data
from instance import Instance
from heuristics import  plant_prop, plant_prop_lite, sim_annealing, hill_climber
from settings import second_value

# External modules
import random
import time
import pickle
import os
import sys
import copy
import matplotlib.pyplot as plt

# Data file location
data_file = r"data\new.xlsx"
filename = r"data\options.xlsx"
print('printing is NOT disabled')

def init(GENS, netlist_number):
    # prepare the data
    ends, starts, tpnum, net_number, SIZE, count_dict = get_data(netlist_number)
    points_to_connect = sort_points2(starts, ends) #, count_dict)

    # create Instances
    generation = [Instance(Grid(SIZE, starts + ends)) for i in range(GENS)]

    # For every instance, connect the grid (deepcopy??)
    for gen in generation:
        # A algorithm
        wires = pickle.load( open( "wires.p", "rb" ) )
        not_connected  = [((1, 3, 0), (9, 10, 0))]
        gen.snotc([i for i in not_connected])
        new_wire = []
        for i,w in enumerate(wires):
            new_wire.append(Wire(w.start, w.end, w.route))
            gen.main.add_wire(new_wire[i])
        gen.swires(new_wire)

        # Wires, connected, not_connected = get_wires(gen.main,
        #                                             points_to_connect)
        # # Link it to the instance
        # gen.start((Wires, not_connected))
        gen.main.value_grid = second_value(SIZE)

    return generation, tpnum, SIZE, starts+ends

if __name__ == '__main__':
    # Get input from command line and check if it's oke.
    try:
        # Read system vars
        netlist_number = int(sys.argv[1])
        repetions = int(sys.argv[3])
        test = sys.argv[4]
        settings = int(sys.argv[2])

        # Read the options file
        options = get_options(settings)

    except:
        print('usage: python main.py #netlist_number #option #loops test_method')
        sys.exit()


    print(f'Solving the following netlist #{netlist_number}')
    for rep in range(int(repetions)):
        start_time = time.time()

        if test == 'plant' or test == 'local':
            GENS = 10
        else:
            GENS = 1

        # Import data
        generation, tpnum, size, all_points = init(GENS, netlist_number)
        print('Instances Done')

        # Select the method you want to use
        if test == 'plant':
            sollution = plant_prop(generation, options, size, all_points)
        if test == 'local':
            sollution = plant_prop_lite(generation, options)
        elif test == 'sima':
            sollution, data = sim_annealing(generation[0], options)
        elif test == 'hill':
            sollution, data = hill_climber(generation[0], options)

        # Extract the sollution
        Wires = sollution.wires
        not_connected = sollution.not_connected

        y = range(len(data))
        w = [i[0] for i in data]
        c = [i[1]for i in data]
        wl = [i[0]/max(w) for i in data]
        cl = [i[1]/max(c) for i in data]
        plt.plot(y, wl, label='length')
        plt.plot(y, cl, label='connected')
        plt.legend()
        plt.show()

        # Check if the wires are not crossing
        print('Wires are not crossing', Check(Wires))
        connected = tpnum - len(not_connected)

        # Calc the Calc time
        cal_time = time.time() - start_time

        # Document all the items
        score = length_score(data_file,
                             Wires,
                             connected / tpnum,
                             not_connected,
                             cal_time,
                             netlist_number,
                             [])

        # Time!
        print(f'We found this sollution in: {cal_time}')

    # Plot the sollution

    sollution.main.plot_wire(Wires)
