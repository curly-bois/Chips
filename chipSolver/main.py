from point import Point
from grid import Grid
from wire import Wire

from extra import *
from settings import *
from data import get_data
from viz_test import plot_anam

import random
import time

import os
import sys

settings = sys.argv[2]
OUTER_LOOPS = int(sys.argv[3])

df = pd.read_excel(filename, sheet_name=0)
var = df.iloc[int(settings)]

## Settings of the Main loop ##
SWAP = True
LOOPS = int(var[9])
SWAPS = int(var[10])
SORT = False
data_file = 'nightdata.xlsx'
###############################

if __name__ == '__main__':
    # Get input from command line
    try:
        netlist_number = sys.argv[1]
    except:
        print('usage: python main.py #netlist_number')
        sys.exit()

    if not int(netlist_number):
        print('usage: python main.py #netlist_number')
        sys.exit()
    else:
        netlist_number = int(netlist_number)

    print(f'Solving the following netlist #{netlist_number}')

    for loop in range(OUTER_LOOPS):
        # Notify the current Loop
        print(f'This is loop #{loop+1}')
        start_time = time.time()

        # Import data
        ends, starts, total_poits_number, net_number, SIZE = get_data(netlist_number)

        # Normal order, or custom order
        if SORT:
            points_to_connect = sort_points(starts, ends) #
        else:
            points_to_connect = sort_points_random(starts, ends)


        # Initialize the grid
        mainGrid = Grid(SIZE, starts + ends)

        # A star algo
        wires, connected, not_connected = get_wires(mainGrid, points_to_connect)

        # Reset value grid
        mainGrid.value_grid = second_value(SIZE)

        # # swap wires
        if SWAP:
            for i in range(LOOPS):
                # print('Swap #', i, 'points to connect:', len(not_connected))
                mainGrid, wires, not_connected = swap_wires(wires,
                                                            not_connected,
                                                            mainGrid,
                                                            SWAPS)
                if len(not_connected) == 0:
                    break

            if len(not_connected) != 0:
                print(len(not_connected))
                break
            else:
                print(len(wires))


            print(sum([len(i.route) for i in wires]))
            for i in range(100):
                mainGrid, wires, not_connected = swap_wires_for_score(wires,
                                                                  not_connected,
                                                                  mainGrid,
                                                                  SWAPS*3)
                print('..', sum([len(i.route) for i in wires]), '..', end='\r')
            for i in range(300):
                mainGrid, wires, not_connected = swap_wires_for_score(wires,
                                                                  not_connected,
                                                                  mainGrid,
                                                                  SWAPS)
                print('..', sum([len(i.route) for i in wires]), '..', end='\r')

        print(len(wires))
        connected = total_poits_number - len(not_connected)

        all = []
        pointss = []
        for i in wires:
            all += i.route
            pointss.append(i.start)
            pointss.append(i.end)
        all_wire = []
        for a in all:
            if not a in pointss:
                all_wire.append(a)

        print(len(all_wire))
        print(len(set(all_wire)))


        # Print lenght + minimal lenght
        cal_time = time.time() - start_time
        score = length_score(data_file,
                             wires,
                             connected / total_poits_number,
                             not_connected,
                             cal_time,
                             net_number,
                             points_to_connect)

        # Time!
        print(f'We found this sollution in: {cal_time}')

    else:
        # Plots result
        # plot_anam(wires, SIZE)
        mainGrid.plot_wire(wires)
