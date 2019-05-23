from point import Point
from grid import Grid
from wire import Wire

from extra import *
from settings import *
from data import get_data
from instance import Instance

import random
import time
import pickle

import os
import sys
import copy
import pickle

settings = sys.argv[2]
OUTER_LOOPS = int(sys.argv[3])

df = pd.read_excel(filename, sheet_name=0)
var = df.iloc[int(settings)]

## Settings of the Main loop ##
SWAP = True
LOOPS = int(var[9])
SWAPS = int(var[10])
SORT = True
data_file = r"data\nightdata.xlsx"
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


    start_time = time.time()

    # Import data
    ends, starts, tpnum, net_number, SIZE, count_dict = get_data(netlist_number)


    points_to_connect = sort_points2(starts, ends) #, count_dict)

    GENS = 20
    generation = [Instance(Grid(SIZE, starts + ends)) for i in range(GENS)]

    for gen in generation:
        Wires, connected, not_connected = get_wires(gen.main,
                                                    points_to_connect)
        # A star algo
        gen.start((Wires, not_connected))
        # Reset value grid
        gen.main.value_grid = second_value(SIZE)

    loops = 20
    swaps = 3
    fifty_mark = 0.15
    delta_t = fifty_mark**(1/(loops/2))

    swap_list = [ i+1 * swaps for i in range(len(generation))]
    temp_list = [ (i*(1/len(generation)))+0.1 for i in range(len(generation))]
    # temp_list = [(i*(0.5/len(generation)))+0.5 for i in range(len(generation))]

    for iter in range(20):
        scrore_board = [i.score1() for i in generation]
        scrore_board.sort()
        scrore_board.reverse()
        print(f'{iter}. Current scores:', scrore_board)


        for i, gen in enumerate(generation):
            SWAPS = swap_list[scrore_board.index(gen.score1())]
            TEMP = temp_list[scrore_board.index(gen.score1())]
            for i in range(20):
                gen.main, new_wires , new_not_con = swap_wiresA_P(gen.gwires(),
                                                            gen.gnotc(),
                                                            gen.main,
                                                            SWAPS,
                                                            gen.t*TEMP)

                new_wires = shuffle(new_wires)
                new_not_con = shuffle(new_not_con)

                gen.snotc(new_not_con)
                gen.swires(new_wires)

                gen.t = update_temperature(gen.t, delta_t)



        generation.sort(key=sortit)
        generation.reverse()

        shortest = generation[0].score1()

        short_list = []
        for gen in generation:
            if gen.score1() == shortest:
                short_list.append(gen)

        short_list.sort(key=shortestit)
        X = short_list[0]
        Y = short_list[1]

        generation = [Instance(Grid(SIZE, starts + ends)) for i in range(GENS)]
        for geni in generation[:int(GENS/2)]:
            geni.snotc([i for i in X.not_connected])
            new_wire = []
            for i,w in enumerate(X.wires):
                new_wire.append(Wire(w.start, w.end, w.route))
                geni.main.add_wire(new_wire[i])
            geni.swires(new_wire)

        for geni in generation[int(GENS/2):]:
            geni.snotc([i for i in Y.not_connected])
            new_wire = []
            for i,w in enumerate(Y.wires):
                new_wire.append(Wire(w.start, w.end, w.route))
                geni.main.add_wire(new_wire[i])
            geni.swires(new_wire)

    print(Check(X.wires))
    connected = tpnum - len(X.not_connected)

    # Print lenght + minimal lenght
    cal_time = time.time() - start_time
    score = length_score(data_file,
                         X.wires,
                         connected / tpnum,
                         X.not_connected,
                         cal_time,
                         net_number,
                         points_to_connect)

    # Time!
    print(f'We found this sollution in: {cal_time}')
    print([i.score2() for i in short_list])

    X.main.plot_wire(X.wires)
