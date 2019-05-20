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

data_file = r"data\nightdata.xlsx"
###############################

def init(GENS, netlist_number):
    ## Get vars
    settings = sys.argv[2]
    type = int(sys.argv[3])

    df = pd.read_excel(filename, sheet_name=0)
    var = df.iloc[int(settings)]

    ## Settings of the Main loop ##
    SWAPS = int(var[10])
    SORT = True

    ends, starts, tpnum, net_number, SIZE, count_dict = get_data(netlist_number)
    points_to_connect = sort_points2(starts, ends) #, count_dict)

    generation = [Instance(Grid(SIZE, starts + ends)) for i in range(GENS)]

    for gen in generation:
        Wires, connected, not_connected = get_wires(gen.main,
                                                    points_to_connect)
        # A star algo
        gen.start((Wires, not_connected))
        # Reset value grid
        gen.main.value_grid = second_value(SIZE)

    return generation, tpnum, SWAPS

def plant_prop_lite(generation, swaps, loops):
    fifty_mark = float(var[10])
    delta_t = fifty_mark**(1/(loops/2))

    swap_list = [ i+1 * swaps for i in range(len(generation))]
    temp_list = [ (i*(1/len(generation)))+0.1 for i in range(len(generation))]

    for iter in range(int(loops/8)): #50

        scrore_board = [i.score1() for i in generation]
        scrore_board.sort()
        scrore_board.reverse()
        print(f'{iter}. Current scores:', scrore_board)


        for i, gen in enumerate(generation):

            SWAPS = swap_list[scrore_board.index(gen.score1())]
            TEMP = temp_list[scrore_board.index(gen.score1())]

            t = 1
            for i in range(loops): #100
                gen.main, new_wires , new_not_con = swap_wiresA_P(gen.gwires(),
                                                            gen.gnotc(),
                                                            gen.main,
                                                            SWAPS,
                                                            t*TEMP)

                new_wires = shuffle(new_wires)
                new_not_con = shuffle(new_not_con)

                gen.snotc(new_not_con)
                gen.swires(new_wires)

                t = update_temperature(t, delta_t)



    generation.sort(key=sortit)
    generation.reverse()

    shortest = generation[0].score1()

    short_list = []
    for gen in generation:
        if gen.score1() == shortest:
            short_list.append(gen)

    short_list.sort(key=shortestit)
    return short_list[0]

def sim_annealing(main, swaps, loops):
    mainGrid = main.main
    Wires = main.gwires()
    not_connected = main.gnotc()

    fifty_mark = float(var[10])
    delta_t = fifty_mark**(1/(loops/2))

    print('Start loop 1')
    t = 1.01
    for i in range(loops):
        mainGrid, Wires, not_connected = swap_wiresA(Wires,
                                                    not_connected,
                                                    mainGrid,
                                                    swaps,
                                                    t)

        Wires = shuffle(Wires)
        t = update_temperature(t, delta_t)

        if len(not_connected) == 0:
            break

    if len(not_connected) != 0:
        print('Not found all')
        print('Not crossing', Check(Wires))
    else:
        print('Found all')
        print('Not crossing', Check(Wires))

    print('Start loop 2')
    t= 1.01
    for i in range(loops):
        mainGrid, Wires, not_connected = swap_wires_for_scoreA(Wires,
                                                          not_connected,
                                                          mainGrid,
                                                          swaps,
                                                          t)
        # print('..', sum([len(i.route) for i in Wires]), '..', end='\r')
        Wires = shuffle(Wires)
        t = update_temperature(t, delta_t)


    print('Not crossing', Check(Wires))

    main.main = mainGrid
    main.swires(Wires)
    main.snotc(not_connected)

    return main

def hill_climber(main, swaps, loops):
    mainGrid = main.main
    Wires = main.gwires()
    not_connected = main.gnotc()

    for i in range(loops):
        mainGrid, Wires, not_connected = swap_wires(Wires,
                                                    not_connected,
                                                    mainGrid,
                                                    swaps)

        Wires = shuffle(Wires)
        if len(not_connected) == 0:
            break

    if len(not_connected) != 0:
        print('Not found all')
        print('Not crossing', Check(Wires))
    else:
        print('Found all')
        print('Not crossing', Check(Wires))


    for i in range(loops):
        mainGrid, Wires, not_connected = swap_wires_for_score(Wires,
                                                          not_connected,
                                                          mainGrid,
                                                          1)
        Wires = shuffle(Wires)


    print('Not crossing', Check(Wires))

    main.main = mainGrid
    main.swires(Wires)
    main.snotc(not_connected)

    return main

def plant_prop(generation, swaps, loops):
    fifty_mark = float(var[10])
    delta_t = fifty_mark**(1/(loops/2))
    swap_list = [ i+1 * swaps for i in range(len(generation))]
    temp_list = [ (i*(1/len(generation)))+0.1 for i in range(len(generation))]

    for iter in range(loops): #50

        scrore_board = [i.score1() for i in generation]
        scrore_board.sort()
        scrore_board.reverse()
        print(f'{iter}. Current scores:', scrore_board)


        for i, gen in enumerate(generation):
            SWAPS = swap_list[scrore_board.index(gen.score1())]
            TEMP = temp_list[scrore_board.index(gen.score1())]
            for i in range(loops*4): #100
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

        generation = [Instance(Grid(SIZE, starts + ends)) for i in range(GENS)]
        for geni in generation:
            geni.snotc([i for i in X.not_connected])
            new_wire = []
            for i,w in enumerate(X.wires):
                new_wire.append(Wire(w.start, w.end, w.route))
                geni.main.add_wire(new_wire[i])
            geni.swires(new_wire)

    return X

if __name__ == '__main__':
    # Get input from command line
    try:
        netlist_number = int(sys.argv[1])
        repetions = int(sys.argv[3])
        test = sys.argv[4]
        loops = int(var[9])
        print(float(var[10]))

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
        generation, tpnum, swaps = init(GENS, netlist_number)

        print('Instances Done')

        if test == 'plant':
            sollution = plant_prop(generation, swaps, loops)
        if test == 'local':
            sollution = plant_prop_lite(generation, swaps, loops)
        elif test == 'sima':
            sollution = sim_annealing(generation[0], swaps, loops)
        elif test == 'hill':
            sollution = hill_climber(generation[0], swaps, loops)


        Wires = sollution.wires
        not_connected = sollution.not_connected

        print('Wires are not crossing', Check(Wires))
        connected = tpnum - len(not_connected)

        # Print lenght + minimal lenght
        cal_time = time.time() - start_time

        score = length_score(data_file,
                             Wires,
                             connected / tpnum,
                             not_connected,
                             cal_time,
                             netlist_number,
                             [])

        # Time!
        print(f'We found this sollution in: {cal_time}')

    print('printing is disabled')
    # sollution.main.plot_wire(Wires)
