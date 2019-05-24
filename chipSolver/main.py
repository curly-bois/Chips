# Classes
from point import Point
from grid import Grid
from wire import Wire

# Own modules
from extra import *
from settings import *
from data import get_data
from instance import Instance
from heuristics import  *
from settings import second_value

# External modules
import random
import time
import pickle
import os
import sys


# Data file location for deposit of data
data_file = r"data\new.xlsx"
# Data file for extratcion of data/settings
filename = r"data\options.xlsx"
# Make new wires or get old ones
new = True

def init(GENS, netlist_number):
    # prepare the data
    ends, starts, tpnum, net_number, SIZE, count_dict = get_data(netlist_number)
    points_to_connect = sort_points_random(starts, ends) #, count_dict)

    # create Instances
    generation = [Instance(Grid(SIZE, starts + ends)) for i in range(GENS)]

    # For every instance, connect the grid (deepcopy??)
    if new:
        for gen in generation:
            # A algorithm
            Wires, connected, not_connected = get_wires(gen.main,
                                                        points_to_connect)
            # Link it to the instance
            gen.start((Wires, not_connected))
            gen.main.value_grid = second_value(SIZE)
    else:
        # Loads wires from wire file
        data_path = "data\\pre_made_wires\\6"
        wire_names = os.listdir('data\\pre_made_wires\\6')

        # Add wire paths to the name, if wire name contains wire
        wire_paths = [data_path+"\\"+i for i in wire_names if 'wire' in i]
        for i, gen in enumerate(generation):
            # Load for every wire and reset the grid
            gen = load_gen(gen, name = wire_paths[i], excel_data =  [((1, 3, 0), (9, 10, 0))])
            gen.main.value_grid = second_value(SIZE)

    return generation, tpnum, SIZE, starts+ends

if __name__ == '__main__':
    # Avalible methods
    methods = {
                'plantsima':plant_prop_sima,
                'platn':plant_prop,
                'local':local_sima,
                'hill':hill_climber,
                'sima':sim_annealing
    }

    # Get input from command line and check if it's oke.
    try:
        # Read system vars
        netlist_number = int(sys.argv[1])
        repetions = int(sys.argv[3])
        test = sys.argv[4]
        settings = int(sys.argv[2])

        # Read the options file
        options = get_options(settings)
        plot = bool(options['plot'])
    except:
        # PRint usage and exit when not used correct
        print('usage: python main.py #netlist_number #option #loops test_method')
        sys.exit()

    if not test in methods:
        print("please select one of these methods:\n", str(methods.keys()))

    avg_data = []
    all_wires = []
    for rep in range(int(repetions)):
        start_time = time.time()

        # if generation based algorithems are used, the amount of generations is
        # set, else is it 1.
        if test == 'plants' or test == 'local' or test == 'plant':
            GENS = int(options['generations'])
        else:
            GENS = 1

        # Import data from the given files
        generation, tpnum, size, all_points = init(GENS, netlist_number)
        print(f'Starting with {test}')

        sollution, data = methods[test](generation, options, size, all_points, tpnum)

        # Extract the sollutions variables
        Wires = sollution.wires
        not_connected = sollution.not_connected

        # Make fancy plots about gathered data, itteration and score
        make_fig(data, f"{netlist_number}_{rep}", test, Wires)

        # Check if the wires are not crossing
        print('Wires are not crossing == ', Check(Wires))

        # Recalculated the connected wires
        connected = tpnum - len(not_connected)

        # Calc the Calc time
        cal_time = time.time() - start_time

        # Show time
        print(f'We found this sollution in: {cal_time}')

        # Document all the items to the export file
        score = length_score(data_file,
                             Wires,
                             connected / tpnum,
                             not_connected,
                             cal_time,
                             netlist_number,
                             [])

        # Save data to the avg_data file, later to be plotten
        avg_data.append(data)
        all_wires.append(Wires)

    if int(repetions) > 1:
        # Take average from all the runs
        data = make_avg_data(avg_data)
        make_fig(data, f'{netlist_number}_avg', test, Wires)

    # Plot the best result
    if not plot:
        pass
    else:
        all_wires.sort(key=best_wire)
        sollution.main.plot_wire(all_wires[0])
